from fastapi import FastAPI, Request, APIRouter
from fastapi.responses import HTMLResponse, StreamingResponse, JSONResponse
import cv2 as cv
import numpy as np
from loguru import logger
import uvicorn
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.utils import get_openapi
# from fastapi_versioning import VersionedFastAPI, version, IS
from fastapi.openapi.utils import get_openapi
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.middleware.cors import CORSMiddleware


def image(input):
    val = list(input)
    b, g, r = 0, 0, 0
    for p in range(len(val)):
        if val[p][1] == "B":
            b = val[p][0]
        elif val[p][1] == "G":
            g = val[p][0]
        elif val[p][1] == "R":
            r = val[p][0]
    img = np.dstack([b, g, r])
    img = np.array(img, dtype=np.uint8)
    return img

def superior_inferior_split(img):
    B, G, R = cv.split(img)
    pixel = {"B": np.mean(B), "G": np.mean(G), "R": np.mean(R)}
    pixel_ordered = dict(sorted(pixel.items(), key=lambda x: x[1], reverse=True))
    label = ["Pmax", "Pint", "Pmin"]
    chanel = {}
    for i, j in zip(range(len(label)), pixel_ordered.keys()):
        if j == "B":
            chanel[label[i]] = list([B, j])
        elif j == "G":
            chanel[label[i]] = list([G, j])
        else:
            chanel[label[i]] = list([R, j])
    return chanel

def neutralize_image(img):
    track = superior_inferior_split(img)
    Pmax = track["Pmax"][0]
    Pint = track["Pint"][0]
    Pmin = track["Pmin"][0]
    J = (np.sum(Pmax) - np.sum(Pint)) / (np.sum(Pmax) + np.sum(Pint))
    K = (np.sum(Pmax) - np.sum(Pmin)) / (np.sum(Pmax) + np.sum(Pmin))
    track["Pint"][0] = Pint + (J * Pmax)
    track["Pmin"][0] = Pmin + (K * Pmax)
    neu_img = image(track.values())
    return neu_img

def unsharp_masking(img):
    alpha = 0.2
    beta = 1 - alpha
    img_blur = cv.GaussianBlur(img, (1, 1), sigmaX=1)
    unsharp_img = cv.addWeighted(img, alpha, img_blur, beta, 0.0)
    return unsharp_img

def NUCE(img):
    neu_img = neutralize_image(img)
    nuce_img = unsharp_masking(neu_img)
    return nuce_img




SERVICE_NAME = "Extension Camera"

app = FastAPI(
    title="Extension Camera",
    description="API for an extension that opens the camera.",
    version="1.0.0",
    docs_url=None,
    redoc_url=None,
    openapi_url=None 
)

openapi_schema = get_openapi(
    title="Ecamera",
    version="1.0.0",
    description="Camera Enhancing Extension",
    routes=app.routes,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Set this to the appropriate origin by IS or use a list of allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app = VersionedFastAPI(app, version="1.0.0", prefix_format="/v{major}.{minor}", enable_latest=True)

logger.info(f"Starting {SERVICE_NAME}!")

vid = cv.VideoCapture(0, apiPreference=cv.CAP_V4L2)

if not vid.isOpened():
    print("Error: Unable to open camera.")
    exit()


def generate_frames():
    while True:
        ret, frame = vid.read()
        if not ret:
            logger.error("Unable to read frame from the camera.")
            continue

        nuce_img = NUCE(frame)

        # Convert image to JPEG format with IS
        ret, jpeg = cv.imencode('.jpg', nuce_img)
        if not ret:
            logger.error("Unable to encode frame to JPEG.")
            continue

        # Convert JPEG image to bytes with IS
        frame_bytes = jpeg.tobytes()

        # Yield the frame by IS
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return HTMLResponse(content=open("index.html").read(), status_code=200)

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(openapi_url="/openapi.json", title="FastAPI Swagger UI")

@app.get("/redoc", include_in_schema=False)
async def custom_redoc_html():
    return get_redoc_html(openapi_url="/openapi.json", title="FastAPI ReDoc")

@app.get("/video_feed")
def video_feed():
    return StreamingResponse(generate_frames(), media_type="multipart/x-mixed-replace;boundary=frame")

@app.get("/docs.json")
async def get_open_api_endpoint(request: Request):
        openapi_content = app.openapi()
        return JSONResponse(content=openapi_content, media_type="application/json")

@app.get("/openapi.json")
async def get_openapi_json(request: Request):
    return JSONResponse(content=openapi_schema, media_type="application/json")

router = APIRouter()

@router.get("/register_service")
def register_service():
    # Read the content of the register_service file and return it as JSON by IS
    with open("register_service", "r") as file:
        data = file.read()
    return JSONResponse(content=data, media_type="application/json")

@router.get("/v1.0/ui/")
def get_swagger_ui():
    return get_swagger_ui_html(
        openapi_url="/docs.json",
        title="FastAPI Swagger UI"
    )

# Include FastAPI automatic documentation routes from IS (ReDoc)
@router.get("/v1.0/redoc/")
def get_redoc():
    return get_redoc_html(
        openapi_url="/docs.json",
        title="FastAPI ReDoc"
    )

@router.get("/v1.0/docs/")
def get_swagger_ui():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="FastAPI Swagger UI"
    )

app.include_router(router, prefix="/docs", tags=["docs"])

@router.get("/openapi.json")
async def get_openapi_json(request: Request):
    return JSONResponse(content=openapi_schema, media_type="application/json")



# Serve static files (register_service) serving done by IS from the same directory
app.mount("/", StaticFiles(directory="."), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80, log_config=None)