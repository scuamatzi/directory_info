import os
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
