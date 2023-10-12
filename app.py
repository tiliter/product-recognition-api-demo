from flask import Flask, render_template, request, jsonify
import base64
import os

from recognition_api_helpers import (
    setup_api_session,
    process_image,
    prepare_api_request_data,
    send_api_request_and_get_response_time,
    load_product_mapping,
)

app = Flask(__name__, template_folder="templates", static_folder="static")

# Replace with your API root endpoint
API_KEY = os.environ["TILITER_API_KEY"]  # Retrieve the API key from the 'TILITER_API_KEY' environment variable
session = setup_api_session(API_KEY)
PRODUCT_MAPPING = load_product_mapping(session)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/recognition", methods=["POST"])
def recognition():
    # Get the image data from the request and process it
    image_data = request.json["image_data"]
    try:
        processed_image = process_image(image_data)
    except:
        return jsonify({"error": "Image processing failed, use jpeg or png"}), 500

    # Send the request to the recognition API endpoint and calculate the response time
    data = prepare_api_request_data(processed_image)
    response, api_response_time = send_api_request_and_get_response_time(data, session)

    # Check the response status code
    if response.status_code != 200:
        return (
            jsonify({"error": f"{response.status_code}: API request failed", "api_response_time": api_response_time}),
            500,
        )

    # If the status code is 200, just pass the JSON response through
    response_json = response.json()
    response_json["api_response_time"] = api_response_time  # add the API response time to the response JSON
    return jsonify({**response_json, 'product_mapping': PRODUCT_MAPPING})


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
        response, api_response_time = send_api_request_and_get_response_time(data, session)
        response_times.append(api_response_time)

    min_response_time = round(min(response_times), 2)
    max_response_time = round(max(response_times), 2)
    avg_response_time = round(sum(response_times) / len(response_times), 2)

    return jsonify(
        {
            "min_response_time": min_response_time,
            "max_response_time": max_response_time,
            "avg_response_time": avg_response_time,
        }
    )


if __name__ == "__main__":
    app.run(debug=True)
