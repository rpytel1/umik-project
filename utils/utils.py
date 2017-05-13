from io import BytesIO
import base64
from PIL import Image

def get_image_from_string(base_string):
    buffer = BytesIO()
    buffer.write(base64.b64decode(base_string))
    buffer.seek(0)
    return Image.open(buffer)

def maxx(list):
    return max(list) if len(list) != 0 else 0