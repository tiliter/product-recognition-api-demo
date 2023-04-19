# Tiliter Recognition Demo

This repository contains a simple web application that demonstrates the functionality of the Tiliter recognition API. The application allows users to drag and drop an image onto the web page, and the application will recognize items in the image and display the recognition results.

## Prerequisites

- Python 3.6 or later
- A Tiliter API key. You can obtain one from the [Tiliter website](https://www.tiliter.com/).

## Installation

1. Clone this repository:
    ```
    git clone {path_to_respository}
    ```
   
2. Navigate to the project directory:
    ```
    cd product-recognition-api-demo
    ```
   
3. Create a virtual environment:
    ```
    python3 -m venv venv
    ```
   
4. Activate the virtual environment:

   - On Linux or macOS:

     ```
     source venv/bin/activate
     ```

   - On Windows:

     ```
     venv\Scripts\activate
     ```

5. Install the required dependencies:
    ```
    pip install -r requirements.txt
    ```
   
## Configuration

1. Set the Tiliter API key as an environment variable:
    ```
    export TILITER_API_KEY={your_api_key}
    ```
   
    Replace `{your_api_key}` with your actual Tiliter API key.
    
    Note: On Windows, use the `set` command instead of `export`.

## Running the Application

1. Start the Flask development server:
    ```
    python app.py
    ```
   
2. Open a web browser and navigate to `http://127.0.0.1:5000`.

3. Drag and drop an image onto the web page to test the Tiliter recognition API.

## Application Structure

- `app.py`: The main Flask application script that handles the API requests and server-side processing.
- `index.html`: The HTML template for the main page of the web application.
- `app.js`: The JavaScript file that handles the drag and drop functionality and communicates with the server.
- `requirements.txt`: A list of Python dependencies required to run the application.
- `static/`: A directory containing static assets such as CSS, JavaScript, and images.
- `templates/`: A directory containing the HTML templates used by the Flask application.

## License

This project is licensed under the Apache 2.0 license. See the [LICENSE](LICENSE) file for details.
