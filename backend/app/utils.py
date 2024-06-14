from fastapi import APIRouter, Depends, HTTPException, UploadFile

def validate_image(file: UploadFile):
    if file.content_type not in ["image/jpeg", "image/png", "image/gif"]:
        raise HTTPException(
            status_code=400, detail="Only JPEG, PNG, and GIF images are allowed."
        )