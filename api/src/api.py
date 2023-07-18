from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from bson.objectid import ObjectId

import base64
import io

from . import db

app = FastAPI()


@app.get("/")
def read_index():
    return "Hello there!"


@app.post("/upload")
async def upload_image_file(img: UploadFile = File(...)):
    content = await img.read()

    try:
        fs = db.get_fs()
        file_id = fs.put(content, filename=img.filename)
    except:
        raise HTTPException(
            status_code=500,
            detail="Something went wrong...",
        )

    return {
        "success": True,
        "image_file_id": str(file_id),
    }


@app.get("/img/{id}")
async def fetch_image(id: str):
    try:
        fs = db.get_fs()
        image_object = fs.get(ObjectId(id))
        content = image_object.read()

        return StreamingResponse(io.BytesIO(content))
    except:
        raise HTTPException(
            status_code=404,
            detail="Image not found!",
        )
