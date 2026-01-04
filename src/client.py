import asyncio
import json
import logging
import os
import sys
import uuid
from datetime import UTC, datetime, timedelta

from temporalio.client import Client
from temporalio.contrib.pydantic import pydantic_data_converter
from temporalio.service import TLSConfig

# pylint: disable=wrong-import-position
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# pylint: enable=wrong-import-position

from activities.investigate_activities import read_repos_config
from models import ConfigOverrides, InvestigateReposRequest, InvestigateSingleRepoRequest
from workflows.investigate_repos_workflow import InvestigateReposWorkflow
from workflows.investigate_single_repo_workflow import InvestigateSingleRepoWorkflow

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def run_investigate_repos_workflow(
    client: Client,
    force: bool = False,
    claude_model: str | None = None,
    max_tokens: int | None = None,
    sleep_hours: float | None = None,
    chunk_size: int | None = None,
):
    """Run the InvestigateReposWorkflow. Runs continuously every X hours.

    Args:
        client: Temporal client instance
        force: If True, forces investigation of all repos ignoring cache on first iteration
        claude_model: Optional Claude model override
        max_tokens: Optional max tokens override
        sleep_hours: Optional sleep hours override (supports fractional hours)
        chunk_size: Optional chunk size override (number of repos processed in parallel)
    """
    task_queue = os.getenv("TEMPORAL_TASK_QUEUE", "investigate-task-queue")

    # Generate unique workflow ID with timestamp to avoid conflicts
    timestamp = datetime.now(UTC).strftime("%Y%m%d-%H%M%S")
    workflow_id = f"investigate-repos-workflow-{timestamp}"

    logger.info("Starting InvestigateReposWorkflow on task queue: %s", task_queue)
    logger.info("Using workflow ID: %s", workflow_id)
    logger.info("Mode: Continuous (runs every X hours)")

    if force:
        logger.info(
            "🚀 Force flag enabled - will force investigation of all repositories on first run"
        )

    # Create Pydantic request model instead of dictionary
    request = InvestigateReposRequest(
        force=force,
        claude_model=claude_model,
        max_tokens=max_tokens,
        sleep_hours=sleep_hours,
        chunk_size=chunk_size,
        iteration_count=0,
    )

    if claude_model:
        logger.info("🔧 Claude model override: %s", claude_model)

    if max_tokens:
        logger.info("🔧 Max tokens override: %s", max_tokens)

    if sleep_hours:
        logger.info("🔧 Sleep hours override: %s", sleep_hours)

    if chunk_size:
        logger.info("🔧 Chunk size override: %s", chunk_size)

    result = await client.execute_workflow(
        InvestigateReposWorkflow.run,
        request,
        id=workflow_id,
        task_queue=task_queue,
        task_timeout=timedelta(minutes=60),  # 60 minutes for workflow task execution
        execution_timeout=timedelta(days=365),  # Long timeout for continuous mode
    )
    logger.info("InvestigateReposWorkflow result: %s", result)
    return result


async def run_investigate_single_repo_workflow(
    client: Client,
    repo_identifier: str,
    force: bool = False,
    claude_model: str | None = None,
    max_tokens: int | None = None,
    repo_type: str | None = None,
    force_section: str | None = None,
):
    """Run the InvestigateSingleRepoWorkflow for a specific repository.

    Args:
        client: Temporal client instance
        repo_identifier: Repository name (from repos.json) or direct URL
        force: If True, forces investigation ignoring cache
        claude_model: Optional Claude model override
        max_tokens: Optional max tokens override
        repo_type: Optional repository type override
        force_section: Optional section name to force re-execution
    """
    task_queue = os.getenv("TEMPORAL_TASK_QUEUE", "investigate-task-queue")

    # Determine if repo_identifier is a URL or a name from repos.json
    repo_name = None
    repo_url = None
    detected_repo_type = "generic"

    if repo_identifier.startswith("http"):
        # Direct URL provided
        repo_url = repo_identifier
        # Extract repo name from URL (last part after /)
        repo_name = repo_url.rstrip("/").split("/")[-1]
        if repo_name.endswith(".git"):
            repo_name = repo_name[:-4]
    else:
        # Repository name provided - look it up in repos.json
        try:
            repos_data = await read_repos_config()

            if "error" in repos_data:
                logger.error("Failed to read repos.json: %s", repos_data["error"])
                return {
                    "status": "failed",
                    "error": f"Failed to read repos.json: {repos_data['error']}",
                }

            repositories = repos_data.get("repositories", {})

            if repo_identifier not in repositories:
                # Filter out comment keys that start with underscore
                available_repos = [key for key in repositories if not key.startswith("_")]

                # Create a user-friendly error message
                error_msg = f"\n❌ Repository '{repo_identifier}' not found in repos.json\n"
                error_msg += f"\n📋 Available repository keys ({len(available_repos)}):\n"
                error_msg += "   " + ", ".join(sorted(available_repos))
                error_msg += "\n\n💡 Tip: You can also use a direct GitHub URL instead of a key"
                error_msg += "\n    Example: mise investigate-one https://github.com/user/repo\n"

                logger.error(error_msg)
                print(error_msg, file=sys.stderr)

                return {"status": "failed", "error": error_msg}

            repo_info = repositories[repo_identifier]
            repo_name = repo_identifier
            repo_url = repo_info.get("url")
            detected_repo_type = repo_info.get("type", "generic")

            if not repo_url:
                logger.error("No URL found for repository: %s", repo_identifier)
                return {
                    "status": "failed",
                    "error": f"No URL found for repository: {repo_identifier}",
                }

        except (json.JSONDecodeError, OSError) as e:
            logger.error("Error reading repos.json: %s", e)
            return {"status": "failed", "error": f"Error reading repos.json: {e!s}"}

    if not repo_url:
        logger.error("No URL found for repository: %s", repo_identifier)
        return {"status": "failed", "error": f"No URL found for repository: {repo_identifier}"}

    # Use provided repo_type or fall back to detected type
    final_repo_type = repo_type or detected_repo_type

    # Generate a unique workflow ID for this investigation
    workflow_id = f"investigate-single-repo-{repo_name}-{uuid.uuid4().hex[:8]}"

    logger.info("Starting InvestigateSingleRepoWorkflow on task queue: %s", task_queue)
    logger.info("Using workflow ID: %s", workflow_id)
    logger.info("Repository: %s (%s)", repo_name, final_repo_type)
    logger.info("URL: %s", repo_url)

    if force:
        logger.info("🚀 Force flag enabled - will investigate regardless of cache")

    # Create config overrides if needed
    config_overrides = None
    if claude_model or max_tokens or force_section:
        config_overrides = ConfigOverrides(
            claude_model=claude_model, max_tokens=max_tokens, force_section=force_section
        )

        if claude_model:
            logger.info("🔧 Claude model override: %s", claude_model)

        if max_tokens:
            logger.info("🔧 Max tokens override: %s", max_tokens)

        if force_section:
            logger.info("🚀 Force section override: %s", force_section)

    # Create Pydantic request model instead of dictionary
    request = InvestigateSingleRepoRequest(
        repo_name=repo_name,
        repo_url=repo_url,
        repo_type=final_repo_type,
        force=force,
        config_overrides=config_overrides,
    )

    result = await client.execute_workflow(
        InvestigateSingleRepoWorkflow.run,
        request,
        id=workflow_id,
        task_queue=task_queue,
        task_timeout=timedelta(minutes=60),  # 60 minutes for workflow task execution
        execution_timeout=timedelta(hours=2),  # 2 hours max for single repo investigation
    )
    logger.info("InvestigateSingleRepoWorkflow result: %s", result)
    return result


async def main():
    """Main function to run the workflow client."""
    # Get Temporal configuration from environment variables or use local defaults
    temporal_server_url = os.getenv("TEMPORAL_SERVER_URL", "localhost:7233")
    temporal_namespace = os.getenv("TEMPORAL_NAMESPACE", "default")
    temporal_api_key = os.getenv("TEMPORAL_API_KEY")

    logger.info("Connecting to Temporal server: %s", temporal_server_url)
    logger.info("Using namespace: %s", temporal_namespace)
    logger.info("API Key present: %s", "Yes" if temporal_api_key else "No")

    # Configure connection parameters based on environment
    # Only use TLS and API key for non-localhost connections (Temporal Cloud)
    is_localhost = temporal_server_url.startswith("localhost")

    if not is_localhost and temporal_api_key:
        logger.info("Configuring for Temporal Cloud with TLS...")
        # Create client with TLS and API key
        client = await Client.connect(
            temporal_server_url,
            namespace=temporal_namespace,
            data_converter=pydantic_data_converter,
            tls=TLSConfig(),
            api_key=temporal_api_key,
        )
    else:
        if is_localhost:
            logger.info("Detected localhost - using insecure connection (no TLS)")

        # Create client connected to server
        client = await Client.connect(
            temporal_server_url,
            namespace=temporal_namespace,
            data_converter=pydantic_data_converter,
        )

    # Get command line arguments
    if len(sys.argv) > 1:
        workflow_name = sys.argv[1].lower()

        if workflow_name == "investigate":
            # Parse configuration overrides from command line
            force = "--force" in sys.argv
            claude_model = None
            max_tokens = None
            sleep_hours = None
            chunk_size = None

            for arg in sys.argv[2:]:
                if arg.startswith("--claude-model="):
                    claude_model = arg.split("=", 1)[1]
                elif arg.startswith("--max-tokens="):
                    try:
                        max_tokens = int(arg.split("=", 1)[1])
                    except ValueError:
                        logger.error(
                            "Invalid max-tokens value: %s. Must be an integer.",
                            arg.split("=", 1)[1],
                        )
                        return
                elif arg.startswith("--sleep-hours="):
                    try:
                        sleep_hours = float(arg.split("=", 1)[1])
                    except ValueError:
                        logger.error(
                            "Invalid sleep-hours value: %s. Must be a number.", arg.split("=", 1)[1]
                        )
                        return
                elif arg.startswith("--chunk-size="):
                    try:
                        chunk_size = int(arg.split("=", 1)[1])
                    except ValueError:
                        logger.error(
                            "Invalid chunk-size value: %s. Must be an integer.",
                            arg.split("=", 1)[1],
                        )
                        return

            await run_investigate_repos_workflow(
                client,
                force=force,
                claude_model=claude_model,
                max_tokens=max_tokens,
                sleep_hours=sleep_hours,
                chunk_size=chunk_size,
            )
        elif workflow_name == "investigate-single":
            # Parse repository identifier and configuration overrides
            if len(sys.argv) < 3:
                logger.error("Repository name or URL is required for investigate-single")
                logger.info(
                    "Usage: python client.py investigate-single REPO_NAME_OR_URL "
                    "[--force] [--claude-model=MODEL] [--max-tokens=NUM] [--repo-type=TYPE]"
                )
                return

            repo_identifier = sys.argv[2]
            force = "--force" in sys.argv
            claude_model = None
            max_tokens = None
            repo_type = None
            force_section = None

            for arg in sys.argv[3:]:
                if arg.startswith("--claude-model="):
                    claude_model = arg.split("=", 1)[1]
                elif arg.startswith("--max-tokens="):
                    try:
                        max_tokens = int(arg.split("=", 1)[1])
                    except ValueError:
                        logger.error(
                            "Invalid max-tokens value: %s. Must be an integer.",
                            arg.split("=", 1)[1],
                        )
                        return
                elif arg.startswith("--repo-type="):
                    repo_type = arg.split("=", 1)[1]
                elif arg.startswith("--force-section="):
                    force_section = arg.split("=", 1)[1]

            await run_investigate_single_repo_workflow(
                client,
                repo_identifier,
                force=force,
                claude_model=claude_model,
                max_tokens=max_tokens,
                repo_type=repo_type,
                force_section=force_section,
            )
        else:
            logger.error("Unknown workflow: %s", workflow_name)
            logger.info("Available workflows: investigate, investigate-single")
            logger.info(
                "Usage: python client.py investigate [--force] "
                "[--claude-model=MODEL] [--max-tokens=NUM] "
                "[--sleep-hours=NUM] [--chunk-size=NUM]"
            )
            logger.info("Usage: python client.py investigate-single REPO_NAME_OR_URL [options]")
    else:
        # Default to investigate workflow
        logger.info("No arguments provided. Running investigate workflow.")
        logger.info("The workflow will run continuously every X hours.")
        logger.info(
            "Use 'python client.py investigate --force' to force investigation of all repos."
        )
        logger.info(
            "Config overrides: --claude-model=MODEL --max-tokens=NUM "
            "--sleep-hours=NUM --chunk-size=NUM"
        )
        logger.info(
            "For single repository investigation: "
            "python client.py investigate-single REPO_NAME_OR_URL [options]"
        )
        await run_investigate_repos_workflow(client)


if __name__ == "__main__":
    asyncio.run(main())
