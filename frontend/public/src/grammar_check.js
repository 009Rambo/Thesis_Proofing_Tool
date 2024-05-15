//Both of these functions now in App.js
//This file may be redundant. We'll see.

async function handleFileUpload(event) {
  const file = event.target.files[0];

  // Create FormData object to send file to backend
  const formData = new FormData();
  formData.append("file", file);

  try {
    // Send file to backend
    const response = await fetch("http://localhost:8002/check-grammar", {
      method: "POST",
      body: formData,
      mode: "no-cors", // remove this line when not using this locally
    });

    // Parse JSON response
    const data = await response.json();

    // Display grammar check results
    displayResults(data);
  } catch (error) {
    console.error("Error:", error);
  }
}

// Function to display grammar check results
function displayResults(results) {
  const resultsContainer = document.getElementById("results");
  resultsContainer.innerHTML = ""; // Clear previous results

  results.forEach((result) => {
    const resultElement = document.createElement("div");
    resultElement.innerHTML = `
            <p><strong>Message:</strong> ${result.message}</p>
            <p><strong>Context:</strong> ${result.context}</p>
            <p><strong>Suggested Correction:</strong> ${result.suggested_correction}</p>
            <hr>
        `;
    resultsContainer.appendChild(resultElement);
  });
}

// Add event listener to file input
document
  .getElementById("fileInput")
  .addEventListener("change", handleFileUpload);
