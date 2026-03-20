import os
import subprocess
import sys


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
