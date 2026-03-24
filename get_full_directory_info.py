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
        console.print(
            "Permission denied accessing some directories!", style="dark_orange"
        )

    sorted_subfolders = sorted(subfolders)
    return sorted_subfolders


def main():
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
        table_files_per_subfolder = Table(
            title="\nFiles in each subfolder", show_lines=True
        )

        table_files_per_subfolder.add_column("Folder", justify="center")
        table_files_per_subfolder.add_column("# Files", justify="center")

        for folder, _, file_count in subfolders:
            table_files_per_subfolder.add_row(f"{folder}", f"{file_count}")

        console.print(table_files_per_subfolder)

    # Count by file type
    print("\n")
    if directory_total_files > 0:
        console.print(Panel("\tTop 10 extension files "), style="dodger_blue2")
        file_types(directory)

    print("\n")
    console.print(Panel("\tDIRECTORY SIZES"), style="dodger_blue2")

    # Get size of directory
    directory_size = get_directory_size(directory)
    console.print(
        f"\nSize of {directory}: [bold]{format_size(directory_size)}[/bold]\n",
        style="turquoise4",
    )

    # Get size of each subfolder
    if subfolders:
        table_subfolders_size = Table(title="Size of each subfolder", show_lines=True)

        table_subfolders_size.add_column("Subfolder", justify="center")
        table_subfolders_size.add_column("Size", justify="center")

        for folder_name, folder_path, _ in subfolders:
            folder_size = get_directory_size(folder_path)
            table_subfolders_size.add_row(
                f"{folder_name}", f"{format_size(folder_size)}"
            )

        console.print(table_subfolders_size)

    if tree_command_selection in ["y", "Y", "yes"]:
        console.print(Panel("\tTREE STRUCTURE OUTPUT"), style="dodger_blue2")

        for level, filename in tree_file_names.items():
            with console.status(""):
                console.print(f"\nLevel {level}:", style="turquoise4")
                run_tree_command(level, filename, directory)

    print("\n")
    console.print(Panel("\tSUMMARY"), style="dodger_blue2")

    console.print(f"• Directory analyzed: [bold]{directory}[/bold]", style="turquoise4")
    console.print(
        f"• Files in directory: [bold]{directory_total_files}[/bold]",
        style="turquoise4",
    )
    console.print(
        f"• Total size: [bold]{format_size(directory_size)}[/bold]", style="turquoise4"
    )

    if tree_command_selection in ["y", "Y", "yes"]:
        print("• Tree outputs generated:")
        for level, filename in tree_file_names.items():
            if os.path.exists(filename):
                console.print(
                    f" - Level {level}: [bold]{filename}[/bold]", style="turquoise4"
                )

    print("\nScript completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
