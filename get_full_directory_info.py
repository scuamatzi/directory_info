"""
Directory Information Script
Generates information about current directory including total file counts,
size of folders and 'tree command' structure.
"""

import os
import subprocess
import sys
import datetime


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


def file_types(directory, top_n=10):
    """
    Count files by their extensions and display top N.

    Args:
        directory: Directory to analyze
        top_n: Number of top extensions to display
    """
    extension_count = {}

    try:
        for root, dirs, files in os.walk(directory):
            for file in files:
                # Split filename and extension
                _, ext = os.path.splitext(file)
                # Use lowercase and handle files without extensions
                ext = ext.lower() if ext else "(no extension)"
                extension_count[ext] = extension_count.get(ext, 0) + 1
    except Exception as e:
        print(f"Error during extension counting: {e}", file=sys.stderr)
        return

    # Sort extensions by count (descending
    sorted_extensions = sorted(
        extension_count.items(), key=lambda x: x[1], reverse=True
    )

    # Display top N
    for i, (ext, count) in enumerate(sorted_extensions[:top_n], 1):
        percentage = (count / sum(extension_count.values())) * 100
        print(f"  {i:2}. {ext:<15} {count:>8,} files ({percentage:.1f}%)")


def get_directory_size(directory_path):
    """Get total size of directory in bytes."""
    total_size = 0

    try:
        for dirpath, dirnames, filenames in os.walk(directory_path):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                try:
                    total_size += os.path.getsize(filepath)
                except (OSError, FileNotFoundError):
                    continue
    except (PermissionError, FileNotFoundError):
        pass

    return total_size


def format_size(size_in_bytes):
    """Format size in human-readable format (MB or GB)."""
    if size_in_bytes == 0:
        return "0 MB"

    # Convert to MegaBytes
    size_mb = size_in_bytes / (1024 * 1024)

    # If larger than 1024 MB, show in GB
    if size_mb >= 1024:
        size_gb = size_mb / 1024
        return f"{size_gb:.2f} GB"
    else:
        return f"{size_mb:.2f} MB"


def run_tree_command(level, filename, path):
    """Execute tree command with specified level and save to file."""
    try:
        # Check if tree command exists
        result = subprocess.run(["tree", "--version"], capture_output=True, text=True)

        # Run tree command with specified level
        cmd = ["tree", "-L", str(level), f"{path}"]
        tree_result = subprocess.run(cmd, capture_output=True, text=True)

        if tree_result.returncode == 0:
            with open(filename, "w") as f:
                f.write(tree_result.stdout)
            print(f"Tree output saved to : {filename}")
            return True
        else:
            print(f"Error running tree command: {tree_result.stderr}")
            return False
    except FileNotFoundError:
        print("  ✗ 'tree' command not found. Please install it first.")
        print("     On Ubuntu/Debian: sudo apt install tree")
        print("     On Fedora/RHEL: sudo dnf install tree")
        print("     On Arch: sudo pacman -S tree")
        return False
    except Exception as e:
        print(f"Error running tree command: {e}")
        return False


def main():
    print("\n" + "=" * 60)
    print("DIRECTORY INFORMATION")
    print("=" * 60)

    # Get current directory
    # current_dir = os.getcwd()
    current_dir = input("\nEnter full path to analyze: ").strip()
    # print(f"\nCurrent directory: {current_dir}")

    if not current_dir:
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

    # Count files in current directory
    current_dir_total_files = count_total_files(current_dir)
    print(f"\nNumber of files in current directory: {current_dir_total_files}")

    # Count files in each subfolder
    print(f"\nNumber of files in each subfolder:")
    subfolders = []
    try:
        for item in os.listdir(current_dir):
            item_path = os.path.join(current_dir, item)
            if os.path.isdir(item_path):
                file_count = count_total_files(item_path)
                print(f"  {item}/: {file_count} files")
                subfolders.append((item, item_path))
    except PermissionError:
        print("Permission denied accessing some directories!")

    # Count by file type
    if current_dir_total_files > 0:
        print("\nTop 10 extension files ")
        file_types(current_dir)

    print("\n" + "-" * 60)
    print("DIRECTORY SIZES")
    print("-" * 60)

    # Get size of current directory
    current_dir_size = get_directory_size(current_dir)
    print(f"\nSize of current directory: {format_size(current_dir_size)}")

    # Get size of each subfolder
    if subfolders:
        print("\nSize of each subfolder:")
        for folder_name, folder_path in subfolders:
            folder_size = get_directory_size(folder_path)
            print(f"  {folder_name}/: {format_size(folder_size)}")

    print("\n" + "-" * 60)
    print("TREE STRUCTURE OUTPUT")
    print("-" * 60)

    if tree_command_selection in ["y", "Y", "yes"]:
        # Generate tree outputs
        print("\nGenerating tree command output...")

        for level, filename in tree_files.items():
            print(f"\nLevel {level}:")
            run_tree_command(level, filename, current_dir)

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"• Current directory: {current_dir}")
    print(f"• Files in current directory: {current_dir_total_files}")
    print(f"• Total size: {format_size(current_dir_size)}")
    if tree_command_selection in ["y", "Y", "yes"]:
        print("• Tree outputs generated:")
        for level, filename in tree_files.items():
            if os.path.exists(filename):
                print(f" - Leveln {level}: {filename}")

    print("\nScript completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
