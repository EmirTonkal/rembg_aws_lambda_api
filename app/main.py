from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import Response, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from rembg import remove
from mangum import Mangum

app = FastAPI(title="Background Removal API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    return JSONResponse({"status": "ok"})

@app.post("/remove-bg")
async def remove_bg(file: UploadFile = File(...)):
    try:
        if file.content_type not in {"image/jpeg", "image/png", "image/webp"}:
            raise HTTPException(status_code=400, detail="Only JPEG/PNG/WEBP accepted")
        data = await file.read()
        if len(data) == 0:
            raise HTTPException(status_code=400, detail="Empty file")
        out = remove(data)
        return Response(content=out, media_type="image/png")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

handler = Mangum(app)
