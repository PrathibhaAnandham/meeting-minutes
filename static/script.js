document.getElementById('uploadBtn').addEventListener('click', function() {
    const fileInput = document.getElementById('audioFile');
    const file = fileInput.files[0];

    if (!file) {
        alert('Please upload a file first!');
        return;
    }

    let formData = new FormData();
    formData.append('file', file);

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert('Error: ' + data.error);
        } else {
            document.getElementById('transcription').textContent = data.transcription || "Transcription not available.";
            document.getElementById('summary').textContent = data.summary || "Summary not available.";
            document.getElementById('sentiment').textContent = "Sentiment: " + (data.sentiment || "Not available.");
            
            // Display key points
            let keyPointsList = document.getElementById('keyPoints');
            keyPointsList.innerHTML = "";
            if (data.key_points && data.key_points.length > 0) {
                data.key_points.forEach(point => {
                    let li = document.createElement('li');
                    li.innerText = point;
                    keyPointsList.appendChild(li);
                });
            } else {
                keyPointsList.innerHTML = "<li>No key points extracted.</li>";
            }

            // Display action items
            let actionItemsList = document.getElementById('actionItems');
            actionItemsList.innerHTML = "";
            if (data.action_items && data.action_items.length > 0) {
                data.action_items.forEach(item => {
                    let li = document.createElement('li');
                    li.innerText = item;
                    actionItemsList.appendChild(li);
                });
            } else {
                actionItemsList.innerHTML = "<li>No action items extracted.</li>";
            }
        }
    })
    .catch(error => console.error('Error:', error));
});
