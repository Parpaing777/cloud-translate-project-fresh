document.getElementById("uploadForm").addEventListener("submit", async function (e) {
    e.preventDefault();
    const fileInput = document.getElementById("file");
    const language = document.getElementById("language").value;

    if (fileInput.files.length === 0) {
        alert("Please upload a file!");
        return;
    }

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);
    formData.append("language", language);

    try {
        const response = await fetch("/upload", {
            method: "POST",
            body: formData,
        });
        const result = await response.json();

        if (result.translated_file_url) {
            // Show success message
            alert(result.message);

            // Show the download button
            const downloadSection = document.getElementById("downloadSection");
            const downloadButton = document.getElementById("downloadButton");

            downloadSection.style.display = "block"; // Make it visible
            downloadButton.onclick = () => {
                // Redirect to the file URL for downloading
                window.location.href = result.translated_file_url;
            };
        } else {
            alert("Translation failed. Please try again.");
        }
    } catch (error) {
        console.error("Error:", error);
        alert("An error occurred while translating the file.");
    }
});