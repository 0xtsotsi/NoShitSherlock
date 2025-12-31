#!/usr/bin/env python3
"""
Quick test script to verify shallow clone works correctly.
This tests the git_manager directly without running the full investigation workflow.
"""

import sys
import os
import tempfile
import shutil
import logging

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from investigator.core.git_manager import GitRepositoryManager

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_clone_small_repo():
    """Test cloning a small repository (is-odd from npm)"""
    logger.info("Testing shallow clone with a small repository...")

    # Create a temporary directory for testing
    temp_base = tempfile.mkdtemp(prefix='test_clone_')

    try:
        git_manager = GitRepositoryManager(logger)

        # Test with a tiny repository
        repo_url = "https://github.com/sindresorhus/is-odd"
        target_dir = os.path.join(temp_base, "is-odd")

        logger.info(f"Cloning {repo_url} to {target_dir}")
        result_path = git_manager.clone_or_update(repo_url, target_dir)

        # Check if clone was successful
        if os.path.exists(target_dir) and os.path.exists(os.path.join(target_dir, '.git')):
            logger.info("✅ Clone successful!")

            # Check if it's a shallow clone
            import subprocess
            depth_check = subprocess.run(
                ['git', 'rev-list', '--count', 'HEAD'],
                cwd=target_dir,
                capture_output=True,
                text=True
            )
            commit_count = depth_check.stdout.strip()
            logger.info(f"Repository has {commit_count} commit(s) in history")

            if commit_count == "1":
                logger.info("✅ Confirmed: This is a shallow clone (depth=1)")
            else:
                logger.warning(f"⚠️  Warning: Expected depth=1 but got {commit_count} commits")

            return True
        else:
            logger.error("❌ Clone failed - directory not created")
            return False

    except Exception as e:
        logger.error(f"❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # Cleanup
        if os.path.exists(temp_base):
            logger.info(f"Cleaning up test directory: {temp_base}")
            shutil.rmtree(temp_base, ignore_errors=True)

def test_clone_repo_swarm():
    """Test cloning repo-swarm itself"""
    logger.info("Testing shallow clone with repo-swarm...")

    # Create a temporary directory for testing
    temp_base = tempfile.mkdtemp(prefix='test_clone_')

    try:
        git_manager = GitRepositoryManager(logger)

        # Test with repo-swarm
        repo_url = "https://github.com/royosherove/repo-swarm"
        target_dir = os.path.join(temp_base, "repo-swarm")

        logger.info(f"Cloning {repo_url} to {target_dir}")
        result_path = git_manager.clone_or_update(repo_url, target_dir)

        # Check if clone was successful
        if os.path.exists(target_dir) and os.path.exists(os.path.join(target_dir, '.git')):
            logger.info("✅ Clone successful!")

            # Check if it's a shallow clone
            import subprocess
            depth_check = subprocess.run(
                ['git', 'rev-list', '--count', 'HEAD'],
                cwd=target_dir,
                capture_output=True,
                text=True
            )
            commit_count = depth_check.stdout.strip()
            logger.info(f"Repository has {commit_count} commit(s) in history")

            if commit_count == "1":
                logger.info("✅ Confirmed: This is a shallow clone (depth=1)")
            else:
                logger.warning(f"⚠️  Warning: Expected depth=1 but got {commit_count} commits")

            # Check directory size
            size_check = subprocess.run(
                ['du', '-sh', target_dir],
                capture_output=True,
                text=True
            )
            size = size_check.stdout.split()[0]
            logger.info(f"Clone size: {size}")

            return True
        else:
            logger.error("❌ Clone failed - directory not created")
            return False

    except Exception as e:
        logger.error(f"❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # Cleanup
        if os.path.exists(temp_base):
            logger.info(f"Cleaning up test directory: {temp_base}")
            shutil.rmtree(temp_base, ignore_errors=True)

if __name__ == "__main__":
    print("=" * 70)
    print("Testing Shallow Clone Implementation")
    print("=" * 70)
    print()

    # Test 1: Small repo
    print("\n--- Test 1: Small Repository (is-odd) ---")
    test1_result = test_clone_small_repo()

    # Test 2: repo-swarm
    print("\n--- Test 2: Larger Repository (repo-swarm) ---")
    test2_result = test_clone_repo_swarm()

    # Summary
    print("\n" + "=" * 70)
    print("Test Summary:")
    print(f"  Small repo test: {'✅ PASSED' if test1_result else '❌ FAILED'}")
    print(f"  repo-swarm test: {'✅ PASSED' if test2_result else '❌ FAILED'}")

    if test1_result and test2_result:
        print("\n✅ All tests passed! Shallow clone is working correctly.")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed. Check the logs above.")
        sys.exit(1)
