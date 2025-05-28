# server.py

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import easyocr
import requests
import shutil
import os
from uuid import uuid4

app = FastAPI()

reader = easyocr.Reader(['en'], gpu=False)

class OCRRequest(BaseModel):
    imageUrl: str

@app.post("/ocr")
async def perform_ocr(data: OCRRequest):
    try:
        # Download the image
        image_url = data.imageUrl
        img_response = requests.get(image_url, stream=True)
        if img_response.status_code != 200:
            raise HTTPException(status_code=400, detail="Image download failed")

        # Save temporarily
        temp_filename = f"/tmp/{uuid4().hex}.jpg"
        with open(temp_filename, 'wb') as out_file:
            shutil.copyfileobj(img_response.raw, out_file)

        # Perform OCR
        result = reader.readtext(temp_filename, detail=0)

        # Clean up
        os.remove(temp_filename)

        return {"success": True, "text": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OCR failed: {str(e)}")
