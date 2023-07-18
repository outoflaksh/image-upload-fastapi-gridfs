from fastapi import FastAPI, File, UploadFile, HTTPException

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
