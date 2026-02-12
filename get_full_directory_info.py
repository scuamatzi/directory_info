"""
Directory Information Script
Generates information about directory provided including total file counts,
size of folders and 'tree command' structure.
"""

import datetime
from modules.directory_file_types import file_types
from modules.directory_size import get_directory_size, format_size
from modules.directory_tree_command import run_tree_command
from modules.count_total_files_in_directory import count_total_files
import os
import sys


def main():
    print("\n" + "=" * 60)
    print("DIRECTORY INFORMATION")
    print("=" * 60)

    # Get directory to analyze
    directory = input("\nEnter full path to analyze: ").strip()

    if not directory:
        print("Full path can not be empty. Aborting.")
        sys.exit(1)

    # Get current date for filename
    current_date = datetime.datetime.now().strftime("%Y%m%d")

    # Ask if tree command is needed
    tree_command_selection = input("\nDo you need tree command info? (y/n) ").strip()

    if tree_command_selection in ["y", "Y", "yes"]:
        # Ask for filename prefix
        filename_prefix = input("\nEnter filename for tree command results: ").strip()

        if not filename_prefix:
            filename_prefix = "tree_output"

        # Generate tree filenames
        tree_files = {
            1: f"{filename_prefix}_L1_{current_date}.txt",
            2: f"{filename_prefix}_L2_{current_date}.txt",
            3: f"{filename_prefix}_L3_{current_date}.txt",
        }

    print("\n" + "-" * 60)
    print("FILE COUNTS")
    print("-" * 60)

    # Count files in directory
    directory_total_files = count_total_files(directory)
    print(f"\nNumber of files in directory: {directory_total_files}")

    # Count files in each subfolder
    print("\nNumber of files in each subfolder:")
    subfolders = []
    try:
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            if os.path.isdir(item_path):
                file_count = count_total_files(item_path)
                subfolders.append((item, item_path, file_count))
    except PermissionError:
        print("Permission denied accessing some directories!")

    sorted_subfolders = sorted(subfolders)
    for folder, _, file_count in sorted_subfolders:
        print(f"  {folder}/: {file_count} files")

    print("\n")

    # Count by file type
    if directory_total_files > 0:
        print("\nTop 10 extension files ")
        file_types(directory)

    print("\n" + "-" * 60)
    print("DIRECTORY SIZES")
    print("-" * 60)

    # Get size of directory
    directory_size = get_directory_size(directory)
    print(f"\nSize of directory: {format_size(directory_size)}")

    # Get size of each subfolder
    if sorted_subfolders:
        print("\nSize of each subfolder:")
        for folder_name, folder_path, _ in sorted_subfolders:
            folder_size = get_directory_size(folder_path)
            print(f"  {folder_name}/: {format_size(folder_size)}")

    if tree_command_selection in ["y", "Y", "yes"]:
        print("\n" + "-" * 60)
        print("TREE STRUCTURE OUTPUT")
        print("-" * 60)

        # Generate tree outputs
        print("\nGenerating tree command output...")

        for level, filename in tree_files.items():
            print(f"\nLevel {level}:")
            run_tree_command(level, filename, directory)

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"• Directory analyzed: {directory}")
    print(f"• Files in directory: {directory_total_files}")
    print(f"• Total size: {format_size(directory_size)}")
    if tree_command_selection in ["y", "Y", "yes"]:
        print("• Tree outputs generated:")
        for level, filename in tree_files.items():
            if os.path.exists(filename):
                print(f" - Leveln {level}: {filename}")

    print("\nScript completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
