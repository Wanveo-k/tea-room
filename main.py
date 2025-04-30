from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image, PngImagePlugin
from io import BytesIO
from fastapi.responses import Response

app = FastAPI()

# Pour éviter les erreurs CORS si besoin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/secure-upload")
async def secure_upload(file: UploadFile = File(...), uploader_id: str = Form(...)):
    contents = await file.read()
    img = Image.open(BytesIO(contents))

    metadata = PngImagePlugin.PngInfo()
    metadata.add_text("Uploader_ID", uploader_id)

    output = BytesIO()
    img.save(output, format="PNG", pnginfo=metadata)
    output.seek(0)

    return Response(output.read(), media_type="image/png")

@app.post("/read-uploader")
async def read_uploader(file: UploadFile = File(...)):
    contents = await file.read()
    img = Image.open(BytesIO(contents))
    uploader = img.info.get("Uploader_ID", "Inconnu")
    return JSONResponse({"uploader_id": uploader})
