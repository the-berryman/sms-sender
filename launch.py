"""
Launch script for the SMS Sender application.
This script should be placed in the root directory.
"""

import os
import sys
from pathlib import Path


def setup_environment():
    """Set up the Python path to include our source directory"""
    # Get the directory containing this script
    project_root = Path(__file__).parent.absolute()

    # Add the project root to Python path
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
        print(f"Added {project_root} to Python path")


def main():
    # Set up the environment
    setup_environment()

    # Import and run the application
    try:
        from src.main import main
        main()
    except ImportError as e:
        print(f"Error: {e}")
        print("\nDebug information:")
        print("Python path:")
        for path in sys.path:
            print(f"  - {path}")
        sys.exit(1)


if __name__ == "__main__":
    main()