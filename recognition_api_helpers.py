import base64
import io
import time
from typing import Dict, Tuple
from datetime import datetime

from requests import Session, Response
from PIL import Image

API_ROOT_URL = "https://recognition.services.tiliter.com/"


def setup_api_session(api_key: str):
    session = Session()
    session.headers.update({"tiliter-api-key": api_key})  # add API key  header to every request
    return session


def process_image(image_data: str):
    """process image data to format required by the API request"""
    # Remove the data prefix for JPEG and PNG images
    image_data = image_data.replace("data:image/jpeg;base64,", "")
    image_data = image_data.replace("data:image/png;base64,", "")

    # Decode the base64 image data and resize it
    image_data_bytes = base64.b64decode(image_data)
    image = Image.open(io.BytesIO(image_data_bytes))
    image = image.resize((400, 240))

    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode()


def prepare_api_request_data(image_data: str):
    """prepare API request body"""
    current_datetime = datetime.now()
    data = {
        "device_id": "demo",
        "images": [{"image": image_data, "camera_type": "generic", "capture_time": current_datetime.isoformat(), }],
        "include_scores": True,
        "score_threshold": None,
    }
    return data


def send_api_request_and_get_response_time(data: Dict, session: Session) -> Tuple[Response, float]:
    """send API request and calculate response time"""
    api_start_time = time.time()
    response = session.post(API_ROOT_URL + "recognition/", json=data)
    api_response_time = round(time.time() - api_start_time, 2)
    return response, api_response_time


def load_product_mapping(session: Session) -> Dict[str, str]:
    """loads the demo products from the API so we can map the product ids to their names"""
    # Fetch the product mapping information from the API
    product_mapping = {}
    response = session.get(API_ROOT_URL + "products/")
    if response.status_code == 200:
        # Store the mapping information in a dictionary
        product_list = response.json()["products"]
        for product in product_list:
            product_mapping[product["product_id"]] = product["product_name"]
    else:
        print("Failed to fetch product mapping information.")
    return product_mapping
