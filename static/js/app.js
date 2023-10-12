const dropArea = document.getElementById('drop-area');
const droppedImage = document.getElementById('dropped-image');
const dropText = document.getElementById('drop-text');
const recognisedProducts = document.getElementById('recognised-products');
const bagDetected = document.getElementById('bag-detected');

// Prevent the default behavior of opening the dropped file in a new tab
document.addEventListener('drop', (event) => {
    event.preventDefault();
    event.stopPropagation();
    return false;
});

document.addEventListener('dragover', (event) => {
    event.preventDefault();
    event.stopPropagation();
    return false;
});

dropArea.addEventListener('dragover', (event) => {
    event.preventDefault();
    event.stopPropagation();
    return false;
});

dropArea.addEventListener('dragenter', (event) => {
    event.preventDefault();
    return false;
});

dropArea.addEventListener('dragleave', (event) => {
    event.preventDefault();
    return false;
});

dropArea.addEventListener('drop', (event) => {
    event.preventDefault();

    // Get the dropped image file
    const file = event.dataTransfer.files[0];

    // Create a FileReader object to read the file contents
    const reader = new FileReader();

    reader.onload = (event) => {
        // Display the dropped image
        droppedImage.src = event.target.result;
        droppedImage.style.display = 'block';
        dropText.style.display = 'none';
        const image_data = event.target.result;

        // Send the image data to the server for recognition
        const xhr = new XMLHttpRequest();
        xhr.open('POST', '/recognition');
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.onload = () => {
            if (xhr.status === 200) {
                const response = JSON.parse(xhr.responseText);
                const resultType = response.product_recognition.result_type;
                const resultTypeContainer = document.getElementById('result-type');
                const productMapping = response.product_mapping;  // New line

                // Display the Result Type
                resultTypeContainer.textContent = mapResultType(resultType);

                // Clear the recognised products list
                recognisedProducts.innerHTML = '';

                // Only display products if the result type is "recognised"
                if (resultType === "recognised") {
                    const products = response.product_recognition.options;

                    for (let i = 0; i < products.length; i++) {
                        const item = document.createElement('li');
                        const productName = productMapping[products[i].product_id] || 'Unknown';  // Updated line
                        item.textContent = productName + ' (' + Math.round(products[i].score * 100) + '%)';
                        recognisedProducts.appendChild(item);
                    }
                }

                // Display the bag detection result
                const bag = response.bag_recognition.present;
                bagDetected.textContent = bag ? "Bag detected" : "No bag detected";

                // Display the API response time
                const apiResponseTimeElement = document.getElementById("api-response-time-value");
                apiResponseTimeElement.style.display = 'block';
                apiResponseTimeElement.textContent = `${response.api_response_time} seconds`;

            } else {
                alert('Error: ' + xhr.status);
            }
        };

        function mapResultType(resultType) {
            const resultTypeMapping = {
                recognised: "Recognised",
                recognised_barcoded_product: "Recognised Barcoded Product",
                no_known_product: "No Known Product",
                obstructed: "Obstructed",
                background: "Background"
            };

            return resultTypeMapping[resultType] || "Unknown Result Type";
        }

        xhr.send(JSON.stringify({image_data: image_data}));
    };

    // Read the file contents as a data URL
    reader.readAsDataURL(file);
    return false;
});
