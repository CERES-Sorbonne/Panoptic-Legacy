import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from core import find_similar, IMAGE_DIRECTORY, get_all_images, make_clusters

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set the directory where your images are stored

app.mount('/static/', StaticFiles(directory=IMAGE_DIRECTORY), name="static")


@app.get("/images/")
async def get_images():
    return [[{**x, 'name': '/static/' + x['name']} for x in get_all_images()]]


@app.get("/images/{image_name}")
async def get_image(image_name: str):
    # Check if the image exists in the directory
    if not os.path.exists(os.path.join(IMAGE_DIRECTORY, image_name)):
        return {"error": "Image not found"}

    # Return the image as a response
    return os.path.join(IMAGE_DIRECTORY, image_name)


@app.get("/images/similar/{image_name}")
async def get_similar_images(image_name: str):
    if not os.path.exists(os.path.join(IMAGE_DIRECTORY, image_name)):
        return {"error": "Image not found"}
    return [[{**x, 'name': '/static/' + x['name']} for x in find_similar(image_name)]]


@app.get("/clusters/")
async def get_clusters():
    return make_clusters()