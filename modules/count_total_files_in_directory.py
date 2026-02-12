import os
import sys


def count_total_files(directory):
    """
    Recursively count allf files inside directory and subdirectories
    Args:
        directory: Path to the directory to count files in

    Returns:
        Total number of files in directory
    """
    file_count = 0

    try:
        for root, dirs, files in os.walk(directory):
            file_count += len(files)
    except PermissionError:
        print(f"Warning: Permission denied accesing {root}", file=sys.stderr)
    except Exception as e:
        print(f"Error accesing {root}: {e}", file=sys.stderr)

    return file_count
