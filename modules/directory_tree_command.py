import subprocess


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
