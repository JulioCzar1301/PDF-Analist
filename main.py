"""
Main entry point for PDF analysis application.

This module initializes the CLI argument parser and controller
to orchestrate PDF extraction, cleaning, and analysis operations.
"""

from src.cli import create_parser
from src.controller import Controller


def main():
    """Parse command-line arguments and execute controller logic."""
    args = create_parser()
    controller = Controller()
    controller.run(args)


if __name__ == "__main__":
    main()
