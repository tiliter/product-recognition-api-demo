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
                // Display the Recognised items
                const response = JSON.parse(xhr.responseText);
                const products = response.recognised_products;
                recognisedProducts.innerHTML = '';

                if (products.length > 0) {
                    for (let i = 0; i < products.length; i++) {
                        const item = document.createElement('li');
                        item.textContent = products[i];
                        recognisedProducts.appendChild(item);
                    }
                } else {
                    const item = document.createElement('li');
                    item.textContent = 'Unrecognised';
                    recognisedProducts.appendChild(item);
                }

                // Display the API response time
                const apiResponseTime = response.api_response_time;
                const apiResponseTimeElement = document.getElementById("api-response-time-value");
                apiResponseTimeElement.style.display = 'block';
                apiResponseTimeElement.textContent = `${apiResponseTime} seconds`;

            } else {
                alert('Error: ' + xhr.status);
            }

            // Display the bag detection result
            const bag = JSON.parse(xhr.responseText)["bag_recognition"];
            if (bag) {
                bagDetected.textContent = "Bag detected";
            } else {
                bagDetected.textContent = "No bag detected";
            }
        };

        xhr.send(JSON.stringify({image_data: image_data}));
    };

    // Read the file contents as a data URL
    reader.readAsDataURL(file);
    return false;
});
