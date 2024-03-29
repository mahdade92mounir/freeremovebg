import os
import base64
from typing import List, Union
from PIL import Image
import numpy as np
from io import BytesIO


def base64_to_image(base64_string: str) -> Image.Image:
    """Returns a PIL image as a base64 encoded string."""

    if ";base64," in base64_string:
        split = base64_string.split(";base64")
        # mime_type = split[0]
        base64_string = split[1]

    image_bytes = base64.b64decode(base64_string)
    buffer = BytesIO(image_bytes)
    image = Image.open(buffer)
    return image


def image_to_base64(
    image: Union[str, Image.Image, np.ndarray], 
    _format: str = "jpeg",
    myme: bool = True,
) -> str:
    """Returns a base64 string from a PIL Image."""
    if isinstance(image, str):
        return image

    if isinstance(image, np.ndarray):
        image = Image.fromarray(image)

    # if image.mode == "RGBA":
    #     image = image.convert("RGB")

    buffer = BytesIO()
    image.save(buffer, format=_format)
    buffer.seek(0)
    encoded_image = base64.b64encode(buffer.getvalue()).decode("utf-8")

    if myme:
        myme_type = f"data:image/{_format};base64,"
        encoded_image = f"{myme_type}{encoded_image}"

    return encoded_image


def parse_image(image: Union[str, Image.Image, np.ndarray]):
    """Returns an image as PIL image"""
    if isinstance(image, str):
        image = base64_to_image(image)

    if isinstance(image, np.ndarray):
        image = Image.fromarray(image)

    return image


def parse_list_of_images(images: List) -> List[Image.Image]:
    """Converts a list of images as PIL image"""
    results = [parse_image(image) for image in images]
    return results


def save_list_of_images(images: List, filepath: str, prefix: str = None):
    """Save list of images."""
    for index, image in enumerate(images):
        prefix = f"{prefix}_" if prefix is not None else ""
        name = f"{prefix}{index}.jpeg"
        fullfilepath = os.path.join(filepath, name)
        image = parse_image(image)
        image.save(fullfilepath)

def bytes_to_base64(bytes, _format):
    base64_str = base64.b64encode(bytes).decode('utf-8')
    myme_type = f"data:image/{_format};base64,"
    encoded_image = f"{myme_type}{base64_str}"
    return encoded_image

def base64_to_bytes(encoded_image: str) -> bytes:
    """Converts a base64-encoded image string from JSON to bytes."""
    try:
        # Supprimez les éventuels en-têtes de type MIME (par exemple, 'data:image/jpeg;base64,')
        if encoded_image.startswith('data:'):
            _, encoded_image = encoded_image.split(',', 1)

        decoded_bytes = base64.b64decode(encoded_image)
        return decoded_bytes
    except Exception as e:
        # Gérez les erreurs de décodage base64 ici
        print(f"Erreur lors du décodage base64 : {str(e)}")
        return b''