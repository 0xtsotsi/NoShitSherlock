import asyncio
import logging
import os
import sys
import threading
import time
from pathlib import Path
from typing import Any

# Immediate startup logging
print("=" * 60, flush=True)
print("INVESTIGATE WORKER STARTING UP", flush=True)
print(f"Python executable: {sys.executable}", flush=True)
print(f"Python version: {sys.version}", flush=True)
print(f"Current working directory: {os.getcwd()}", flush=True)
print(f"Script path: {os.path.abspath(__file__)}", flush=True)
print("Environment variables:", flush=True)
print(
    f"  PROMPT_CONTEXT_STORAGE: {os.environ.get('PROMPT_CONTEXT_STORAGE', 'NOT SET')}", flush=True
)
print(f"  SKIP_DYNAMODB_CHECK: {os.environ.get('SKIP_DYNAMODB_CHECK', 'NOT SET')}", flush=True)
print(f"  LOCAL_TESTING: {os.environ.get('LOCAL_TESTING', 'NOT SET')}", flush=True)
print("=" * 60, flush=True)

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configure logging immediately
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)

logger.info("Starting imports...")
try:
    from temporalio.client import Client

    logger.info("  ✓ Imported temporalio.client.Client")
except ImportError as e:
    logger.error("  ✗ Failed to import temporalio.client.Client: %s", e)
    raise

try:
    from temporalio.worker import Worker

    logger.info("  ✓ Imported temporalio.worker.Worker")
except ImportError as e:
    logger.error("  ✗ Failed to import temporalio.worker.Worker: %s", e)
    raise

try:
    from temporalio.service import TLSConfig

    logger.info("  ✓ Imported temporalio.service.TLSConfig")
except ImportError as e:
    logger.error("  ✗ Failed to import temporalio.service.TLSConfig: %s", e)
    raise

try:
    from temporalio.contrib.pydantic import pydantic_data_converter

    logger.info("  ✓ Imported temporalio.contrib.pydantic.pydantic_data_converter")
except ImportError as e:
    logger.error("  ✗ Failed to import temporalio.contrib.pydantic.pydantic_data_converter: %s", e)
    raise

try:
    from workflows.investigate_repos_workflow import InvestigateReposWorkflow

    logger.info("  ✓ Imported InvestigateReposWorkflow")
except ImportError as e:
    logger.error("  ✗ Failed to import InvestigateReposWorkflow: %s", e)
    raise

try:
    from workflows.investigate_single_repo_workflow import InvestigateSingleRepoWorkflow

    logger.info("  ✓ Imported InvestigateSingleRepoWorkflow")
except ImportError as e:
    logger.error("  ✗ Failed to import InvestigateSingleRepoWorkflow: %s", e)
    raise


try:
    from activities.investigate_activities import (
        analyze_repository_structure_activity,
        analyze_with_claude_context,
        cache_dependencies_activity,
        cleanup_repository_activity,
        clone_repository_activity,
        get_prompts_config_activity,
        read_dependencies_activity,
        read_prompt_file_activity,
        read_repos_config,
        retrieve_all_results_activity,
        save_prompt_context_activity,
        save_to_arch_hub,
        update_repos_list,
        write_analysis_result_activity,
    )

    logger.info("  ✓ Imported investigate activities")
except ImportError as e:
    logger.error("  ✗ Failed to import investigate activities: %s", e)
    raise

try:
    from activities.investigation_cache_activities import (
        check_if_repo_needs_investigation,
        save_investigation_metadata,
    )

    logger.info("  ✓ Imported investigation cache activities")
except ImportError as e:
    logger.error("  ✗ Failed to import investigation cache activities: %s", e)
    raise

try:
    from activities.dynamodb_health_check_activity import (
        check_dynamodb_health,
        cleanup_old_health_checks,
    )

    logger.info("  ✓ Imported DynamoDB health check activities")
except ImportError as e:
    logger.error("  ✗ Failed to import DynamoDB health check activities: %s", e)
    raise

logger.info("All imports successful!")

# Health check file for ECS
HEALTH_FILE = Path("/tmp/worker_health")


def update_health_file():
    """Update the health check file to indicate the worker is alive."""
    try:
        HEALTH_FILE.touch()
        logger.debug("Updated health file: %s", HEALTH_FILE)
    except OSError as e:
        logger.error("Failed to update health file: %s", e)


def health_check_thread():
    """Background thread that updates the health file periodically."""
    logger.info("Starting health check thread...")
    while True:
        update_health_file()
        time.sleep(10)  # Update every 10 seconds


def get_temporal_config():
    """Get Temporal configuration from environment variables."""
    config = {
        "server_url": os.getenv("TEMPORAL_SERVER_URL", "localhost:7233"),
        "namespace": os.getenv("TEMPORAL_NAMESPACE", "default"),
        "task_queue": os.getenv("TEMPORAL_TASK_QUEUE", "investigate-task-queue"),
        "identity": os.getenv("TEMPORAL_IDENTITY", "investigate-worker"),
        "api_key": os.getenv("TEMPORAL_API_KEY"),  # Get API key from environment
    }

    # Log the configuration (masking sensitive data)
    logger.info("=" * 60)
    logger.info("TEMPORAL CONFIGURATION:")
    logger.info("  Server URL: %s", config["server_url"])
    logger.info("  Namespace: %s", config["namespace"])
    logger.info("  Task Queue: %s", config["task_queue"])
    logger.info("  Identity: %s", config["identity"])
    logger.info("  API Key Present: %s", bool(config["api_key"]))
    if config["api_key"]:
        logger.info("  API Key Length: %s chars", len(config["api_key"]))
        preview = config["api_key"][:10] + "..." if len(config["api_key"]) > 10 else "Key too short"
        logger.info("  API Key Preview: %s", preview)
    logger.info("=" * 60)

    return config


async def main():
    """Main function to run the Temporal worker for investigation workflows."""
    logger.info("=" * 60)
    logger.info("STARTING TEMPORAL WORKER")
    logger.info("Python version: {sys.version}")
    logger.info("Current directory: {os.getcwd()}")
    logger.info("Script location: %s", os.path.abspath(__file__))
    logger.info("=" * 60)

    try:
        logger.info("Step 1: Getting Temporal configuration...")
        config = get_temporal_config()

        logger.info("Step 2: Preparing connection parameters...")
        logger.info("  Connecting to: %s", config["server_url"])
        logger.info("  Namespace: %s", config["namespace"])
        logger.info("  Task queue: %s", config["task_queue"])

        # Configure connection based on server URL and whether we have an API key
        connection_kwargs: dict[str, Any] = {}
        is_localhost = config["server_url"].startswith("localhost")

        if not is_localhost and config["api_key"]:
            logger.info("Step 3: Configuring TLS for Temporal Cloud...")
            logger.info("  Creating TLS configuration...")
            tls_config = TLSConfig()
            logger.info("  TLS configuration created successfully")
            connection_kwargs = {
                "api_key": config["api_key"],
                "tls": tls_config,
            }
            logger.info("  Connection parameters configured for Temporal Cloud")
        else:
            logger.info("Step 3: Configuring for local Temporal server...")
            if is_localhost:
                logger.info("  Detected localhost - using insecure connection (no TLS)")
            else:
                logger.info("  No API key provided, using unsecured connection")

        # Create client connected to server at the given address
        logger.info("Step 4: Attempting to connect to Temporal server...")
        logger.info("  Connection URL: %s", config["server_url"])
        logger.info("  Namespace: %s", config["namespace"])
        logger.info("  Identity: %s", config["identity"])

        client = await Client.connect(
            config["server_url"],
            namespace=config["namespace"],
            identity=config["identity"],
            data_converter=pydantic_data_converter,
            **connection_kwargs,
        )
        logger.info("✓ Successfully connected to Temporal server!")

        # Start health check thread after successful connection
        logger.info("Starting health check mechanism...")
        health_thread = threading.Thread(target=health_check_thread, daemon=True)
        health_thread.start()
        update_health_file()  # Create initial health file
        logger.info("✓ Health check mechanism started")

        # Run the worker for investigation workflows
        logger.info("Step 5: Creating worker instance...")
        logger.info("  Task queue: %s", config["task_queue"])
        workflow_names = [
            w.__name__ for w in [InvestigateReposWorkflow, InvestigateSingleRepoWorkflow]
        ]
        logger.info("  Workflows: %s", workflow_names)
        all_activities = [
            save_to_arch_hub,
            read_repos_config,
            update_repos_list,
            save_prompt_context_activity,
            analyze_with_claude_context,
            retrieve_all_results_activity,
            clone_repository_activity,
            analyze_repository_structure_activity,
            get_prompts_config_activity,
            read_prompt_file_activity,
            write_analysis_result_activity,
            cleanup_repository_activity,
            check_if_repo_needs_investigation,
            save_investigation_metadata,
            check_dynamodb_health,
            cleanup_old_health_checks,
            read_dependencies_activity,
            cache_dependencies_activity,
        ]
        activity_names = [a.__name__ for a in all_activities]
        logger.info("  Activities: %s", activity_names)

        worker = Worker(
            client,
            task_queue=config["task_queue"],
            workflows=[InvestigateReposWorkflow, InvestigateSingleRepoWorkflow],
            activities=all_activities,
        )
        logger.info("✓ Worker instance created successfully!")

        logger.info("Step 6: Starting worker run loop...")
        logger.info("=" * 60)
        logger.info("TEMPORAL WORKER IS RUNNING")
        logger.info("Listening on task queue: %s", config["task_queue"])
        logger.info("Waiting for workflows...")
        logger.info("=" * 60)

        await worker.run()

    except ImportError as e:
        logger.error("Import error - missing dependency: %s", e, exc_info=True)
        logger.error("Make sure all required packages are installed")
        raise
    except ConnectionError as e:
        logger.error("Connection error - could not connect to Temporal: %s", e, exc_info=True)
        logger.error("Check your Temporal server URL and network connectivity")
        raise
    except Exception as e:
        logger.error("Unexpected error during startup: %s", e, exc_info=True)
        logger.error("Error type: %s", type(e).__name__)
        raise


if __name__ == "__main__":
    try:
        print(f"Starting worker from __main__ at {os.getcwd()}", flush=True)
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Worker stopped by user", flush=True)
        sys.exit(0)
    except (ConnectionError, RuntimeError, OSError) as e:
        print(f"FATAL ERROR: {e}", flush=True)
        print(f"Error type: {type(e).__name__}", flush=True)
        import traceback

        traceback.print_exc()
        sys.exit(1)
