import os


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
