const dropArea = document.getElementById('drop-area');
const droppedImage = document.getElementById('dropped-image');
const dropText = document.getElementById('drop-text');
const recognizedItems = document.getElementById('recognized-items');
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
        xhr.open('POST', '/predict');
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.onload = () => {
            if (xhr.status === 200) {
                // Display the recognized items
                const response = JSON.parse(xhr.responseText);
                const items = response.items;
                recognizedItems.innerHTML = '';

                if (items.length > 0) {
                    for (let i = 0; i < items.length; i++) {
                        const item = document.createElement('li');
                        item.textContent = items[i];
                        recognizedItems.appendChild(item);
                    }
                } else {
                    const item = document.createElement('li');
                    item.textContent = 'Unrecognized';
                    recognizedItems.appendChild(item);
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
