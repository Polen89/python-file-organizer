import os
import re
import shutil
from datetime import datetime as dt


## Clean up the filename ##
def clean_filename(filename: str) -> str:
    """
    Remove date/time and other numeric characters from the file name.

    Example:
        'Screenshot 2025-11-26 201308.png' -> 'Screenshot.png'
    """

    name, ext = os.path.splitext(filename)

    # Remove date and time from filename (like "2025-11-26 and 201308")
    name = re.sub(r"\(s\*\)", " ", name).strip()

    # Remove any remaining digits anywhere
    name = re.sub(r"\d+", "", name)

    # Remove empty parentheses left over
    name = re.sub(r"\(s\*\)", " ", name).strip()

    # Normalize whitespace
    name = re.sub(r"\s+", " ", name).strip()

    return name + ext

def unique_path(dest_folder: str, filename: str) -> str:
    """
    If filename already exists in the destination folder, append a number to the end of the filename.

    Example: Screenshot.png -> Screenshot (1).png
    """

    base, ext = os.path.splitext(filename)
    candidate = os.path.join(dest_folder, filename)

    if not os.path.exists(candidate):
        return candidate

    i = 1
    while True:
        new_name = f"{base} ({i}){ext}"
        candidate = os.path.join(dest_folder, new_name)
        if not os.path.exists(candidate):
            return candidate

        i += 1


## replace with your path ##
def png_finder(source_dir='.', dest_root=None):
    """
    Find PNG files in src_dir, makes dates folder (YYYY-MM-DD) base on file creation date,
    cleans the filename (removes date/time numbers), and moves them

    Output structure:
      dest_root/
        YYYY-MM-DD/
          Screenshot.png
          Screenshot (1).png
    """
    if dest_root is None:
        dest_root = os.path.join(source_dir, "PNGS")

    png_found = False
    png_moved = 0
    files_skipped = 0

    # Safely get directory contents
    try:
        files = os.listdir(source_dir)
    except Exception as e:
        print(f"Error reading directory: {e}")
        return

    # Iterates files; moves PNGs to date‑based folders
    for png in files:
        path = os.path.join(source_dir, png)

        # Skip non-files
        if not os.path.isfile(path):
            continue

        # Only process PNG files
        if not png.lower().endswith('.png'):
            files_skipped += 1
            continue

        # At least 1 PNG file exists
        png_found = True

        try:
            created_date = dt.fromtimestamp(
                os.path.getctime(path)
            ).strftime('%Y-%m-%d')
        except Exception as e:
            files_skipped += 1
            print(f"Could not read created date for {png}: {e}")
            continue

        # Destination folder: YYYY-MM-DD
        dest_folder = os.path.join(dest_root, created_date)
        os.makedirs(dest_folder, exist_ok=True)

        clean_name = clean_filename(png)
        dest_path = unique_path(dest_folder, clean_name)

        # Move the file
        try:
            shutil.move(path, dest_path)
            png_moved += 1
        except Exception as e:
            print(f"Failed to move {png}: {e}")
            files_skipped += 1

    if not png_found:
        print("No PNG files found. Nothing to do.")
    else:
        print(f"Directory: {source_dir}")
        print(f"PNG found: {png_found}")
        print(f"PNG moved: {png_moved}")
        print(f"Files skipped: {files_skipped}")

png_finder()


