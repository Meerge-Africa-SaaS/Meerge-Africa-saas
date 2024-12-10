from .base import *

import cloudinary
import cloudinary.uploader
import cloudinary.api

CLOUDINARY = {
    'cloud_name': os.getenv("CLOUDINARY_CLOUD_NAME"),
    'api_key': os.getenv("CLOUDINARY_API_KEY"),
    'api_secret': os.getenv("CLOUDINARY_API_SECRET"),
}

print(f"loading. .. {__file__}")
