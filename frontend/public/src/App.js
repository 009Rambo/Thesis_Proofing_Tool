//App.js - Upload file to backend & display results
//NOTE! Due to us working in vanilla JS, imports must be made like this
//because other types of importing might not work in all browsers
import * as renderBlocks from "./render_results.js";

const uploadFile = async (event) => {
  //uploading file to backend goes here
  const fileInput = document.getElementById("fileInput");
  const file = fileInput.files[0];

  if (!file) {
    document.getElementById("message").innerText = "Please select a file.";
    return;
  }

  const formData = new FormData();
  formData.append("file", file);

  try {
    const resp = await fetch("http://localhost:5000/upload", {
      method: "POST",
      body: formData,
    });

    const data = await resp.json();

    if (resp.ok) {
      displayResults(data);
    }
  } catch (error) {
    console.error("Error uploading file:", error);
    document.getElementById("message").innerText = "Error uploading file.";
  }
};

const displayResults = (data) => {
  //format and display what backend spits out
  document.getElementById("message").innerText = data.message;

  document.getElementById("fileName").innerText = data.file_name;
  document.getElementById("filePath").innerText = data.file_path;
  document.getElementById("pagesAmount").innerText = data.pages_amount;

  document.getElementById("statedEqualsActual").innerText =
    data.stated_equals_actual;

  renderBlocks.renderTextBlocks(data.text_blocks);
  document.getElementById("pdfContent").innerText = data.text_content;
  document.getElementById("fileInfo").style.display = "block";
};

document.getElementById("fileButton").addEventListener("click", uploadFile);
