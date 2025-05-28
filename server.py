from fastapi import FastAPI, Request
import easyocr
import numpy as np
from io import BytesIO
from PIL import Image
import requests

app = FastAPI()
reader = easyocr.Reader(['en'], gpu=False)

@app.get("/")
def root():
    return {"message": "EasyOCR ready"}

@app.post("/ocr")
async def ocr(request: Request):
    data = await request.json()
    image_url = data.get("image_url")

    try:
        response = requests.get(image_url)
        image = Image.open(BytesIO(response.content)).convert("RGB")
        result = reader.readtext(np.array(image), detail=0)
        return {"text": result}
    except Exception as e:
        return {"error": str(e)}

