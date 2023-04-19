from flask import Flask, render_template, request, jsonify
import base64
import os
import requests
import time
from datetime import datetime
import io
from PIL import Image

app = Flask(__name__, template_folder='templates', static_folder='static')

API_ROOT_URL = "https://recognition.services.tiliter.com/"  # Replace with your API root endpoint
API_KEY = os.environ['TILITER_API_KEY']  # Retrieve the API key from the 'TILITER_API_KEY' environment variable
PRODUCT_MAPPING = {}

# Initialize a session object at startup
session = requests.Session()
session.headers.update({"tiliter-api-key": API_KEY})
print("API connected")


def resize_image(image_data):
    """Resize the image to 400x240"""
    image = Image.open(io.BytesIO(image_data))
    image = image.resize((400, 240))
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode()


# Helper function to prepare API request data
def prepare_api_request_data(image_data):
    current_datetime = datetime.now()
    data = {
        "device_id": "demo",
        "images": [
            {
                "image": image_data,
                "camera_type": "generic",
                "capture_time": current_datetime.isoformat()
            }
        ]
    }
    return data


# Helper function to send API request and calculate response time
def send_api_request_and_get_response_time(data):
    api_start_time = time.time()
    response = session.post(API_ROOT_URL + "recognition/", json=data)
    api_response_time = round(time.time() - api_start_time, 2)
    return response, api_response_time


@app.before_first_request
def load_product_mapping():
    global PRODUCT_MAPPING
    # Fetch the product mapping information from the API
    headers = {"tiliter-api-key": API_KEY}
    response = requests.get(API_ROOT_URL + "products/", headers=headers)
    if response.status_code == 200:
        # Store the mapping information in a dictionary
        product_list = response.json()["products"]
        for product in product_list:
            PRODUCT_MAPPING[product["product_id"]] = product["product_name"]
    else:
        print("Failed to fetch product mapping information.")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    # Extract the base64 image data from the request
    image_data = request.json["image_data"]

    # Remove the data prefix for JPEG and PNG images
    image_data = image_data.replace("data:image/jpeg;base64,", "")
    image_data = image_data.replace("data:image/png;base64,", "")

    # Convert base64 string to bytes
    image_data_bytes = base64.b64decode(image_data)
    image_data = resize_image(image_data_bytes)

    # Prepare the API request headers and data
    headers = {"tiliter-api-key": API_KEY}
    data = prepare_api_request_data(image_data)

    # Send the request to the API's recognition endpoint and calculate the API response time
    response, api_response_time = send_api_request_and_get_response_time(data)

    # Check the response status code
    if response.status_code == 200:
        product_recognition = response.json()["product_recognition"]
        if product_recognition["result_type"] == "recognised":
            options = product_recognition["options"]
            if options:
                items = []
                for option in options:
                    product_id = option["product_id"]
                    if product_id in PRODUCT_MAPPING:
                        product_name = PRODUCT_MAPPING[product_id]
                    else:
                        product_name = "Unknown"
                    items.append(product_name)
                bag_recognition = response.json()["bag_recognition"]
                present = bag_recognition.get("present", False)
                return jsonify({"items": items, "bag_recognition": present, "api_response_time": api_response_time})
        return jsonify({"item_name": "Unrecognized", "api_response_time": api_response_time})
    else:
        return jsonify({"error": "API request failed", "api_response_time": api_response_time}), 500


@app.route("/timing_test", methods=["GET"])
def api_timing_test():
    # Get the number of calls from the URL or default to 10 if not provided
    num_calls = int(request.args.get("num_calls", 10))
    response_times = []

    # Read the sample image file from /static/sample_image folder
    sample_image_path = os.path.join("static", "sample_images", "example_image.jpeg")
    with open(sample_image_path, "rb") as image_file:
        sample_image_data = base64.b64encode(image_file.read()).decode()

    for _ in range(num_calls):
        # Prepare the API request data
        data = prepare_api_request_data(sample_image_data)

        # Send the request to the API's recognition endpoint and calculate the API response time
        response, api_response_time = send_api_request_and_get_response_time(data)
        response_times.append(api_response_time)

    min_response_time = round(min(response_times), 2)
    max_response_time = round(max(response_times), 2)
    avg_response_time = round(sum(response_times) / len(response_times), 2)

    return jsonify({
        "min_response_time": min_response_time,
        "max_response_time": max_response_time,
        "avg_response_time": avg_response_time
    })


if __name__ == "__main__":
    app.run(debug=True)
