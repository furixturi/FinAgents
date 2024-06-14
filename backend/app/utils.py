import bleach
from fastapi import HTTPException, UploadFile


def validate_file_type(file: UploadFile, allowed_types: list[str]):
    return file.content_type in allowed_types
        
def sanitize_text(text: str) -> str:
    """Sanitize user input text to remove HTML tags and strip leading and trailing whitespaces."""
    return bleach.clean(text, strip=True) if text else text