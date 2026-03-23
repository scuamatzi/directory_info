"""
Directory Information Script
Generates information about directory provided including total file counts,
size of folders and 'tree command' structure.
"""

import datetime
import os
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
import sys

from modules.directory_tools import (
    file_types,
    get_directory_size,
    format_size,
    run_tree_command,
    count_total_files,
)

console = Console()


def create_tree_filenames():
    # Get current date for filenames
    current_date = datetime.datetime.now().strftime("%Y%m%d")

    filename_prefix = input("\nEnter filename for tree command results: ").strip()

    if not filename_prefix:
        filename_prefix = "tree_output"

    # Generate tree filenames
    tree_file_names = {
        1: f"{filename_prefix}_L1_{current_date}.txt",
        2: f"{filename_prefix}_L2_{current_date}.txt",
        3: f"{filename_prefix}_L3_{current_date}.txt",
    }
    return tree_file_names


def get_total_files_per_subfolder(directory):
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
    return sorted_subfolders


def main():
    # print("\n" + "=" * 60)
    # print("DIRECTORY INFORMATION")
    # print("=" * 60)

    print("\n")
    console.print(
        Panel(
            "- Total files inside directory\n"
            + "- Total files inside each subfolder\n"
            + "- Top 10 file extensions in directory (the extension and how many)\n"
            + "- Total size of directory\n"
            + "- Total size of each subdirectory\n"
            "- [Optional] write down 'tree' command for directory with 3 levels",
            title="DIRECTORY INFORMATION",
        ),
        style="dodger_blue2",
    )

    # Get directory to analyze
    directory = input("\nEnter full path to analyze: ").strip()

    if not directory:
        console.print("Full path can not be empty. Aborting.", style="dark_orange")
        sys.exit(1)

    # Ask if tree command is needed
    tree_command_selection = input("\nDo you need tree command info? (y/n) ").strip()

    if tree_command_selection in ["y", "Y", "yes"]:
        tree_file_names = create_tree_filenames()

    # print("\n" + "-" * 60)
    # print("FILE COUNTS")
    # print("-" * 60)

    print("\n")
    console.print(Panel("\tFILE COUNTS", style="dodger_blue2"))

    # Count files in directory
    directory_total_files = count_total_files(directory)
    console.print(
        f"\nTotal files in {directory}: [bold]{directory_total_files}[/bold]\n",
        style="turquoise4",
    )

    # Count files in each subfolder

    subfolders = get_total_files_per_subfolder(directory)

    if subfolders:
        # table_files_per_subfolder = Table(title="\nNumber of files in each subfolder")
        table_files_per_subfolder = Table(
            title="\nFiles in each subfolder", show_lines=True
        )

        table_files_per_subfolder.add_column("Folder", justify="center")
        table_files_per_subfolder.add_column("# Files", justify="center")
        # print("\nNumber of files in each subfolder:")

        for folder, _, file_count in subfolders:
            table_files_per_subfolder.add_row(f"{folder}", f"{file_count}")
            # table_files_per_subfolder.add_row(f"{file_count}")

        console.print(table_files_per_subfolder)
        # print(f"  {folder}/: {file_count} files")

        # print("\n")

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
    if subfolders:
        print("\nSize of each subfolder:")
        for folder_name, folder_path, _ in subfolders:
            folder_size = get_directory_size(folder_path)
            print(f"  {folder_name}/: {format_size(folder_size)}")

    if tree_command_selection in ["y", "Y", "yes"]:
        print("\n" + "-" * 60)
        print("TREE STRUCTURE OUTPUT")
        print("-" * 60)

        # Generate tree outputs
        print("\nGenerating tree command output...")

        for level, filename in tree_file_names.items():
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
        for level, filename in tree_file_names.items():
            if os.path.exists(filename):
                print(f" - Level {level}: {filename}")

    print("\nScript completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
