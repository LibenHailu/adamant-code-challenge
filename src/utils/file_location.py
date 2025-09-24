import os
import uuid


def get_random_file_location(original_filename: str, upload_dir: str = "uploads") -> str:
    # Extract extension from original filename
    ext = os.path.splitext(original_filename)[1]
    random_name = f"{uuid.uuid4().hex}{ext}"
    return os.path.join(upload_dir, random_name)
