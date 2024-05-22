//App.js - Upload file to backend & display results
//NOTE! Due to us working in vanilla JS, imports must be made like this
//because other types of importing might not work in all browsers
import * as renderResults from "./render_results.js";

const uploadFile = async (event) => {
  //uploading file to backend
  const fileInput = document.getElementById("fileInput");
  const file = fileInput.files[0];

  const message = document.getElementById("message");

  if (!file) {
    message.innerText = "Please select a file.";
    message.style.color = "red";
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
      message.style.color = "green";
      displayResults(data);
    }
  } catch (error) {
    console.error("Error uploading file:", error);
    message.innerText = "Error uploading file.";
    message.style.color = "red";
  }
};

const displayResults = (data) => {
  //format and display what backend spits out
  document.getElementById("fileInfo").style.visibility = "visible";

  document.getElementById("message").innerText = data.message;

  document.getElementById("fileName").innerText = data.file_name;
  document.getElementById("pagesAmount").innerText = data.pages_amount;

  document.getElementById("statedEqualsActual").innerText = data.stated_equals_actual;
  console.log(data.found_urls[0])

  renderResults.renderTextBlocks(data.text_blocks);
  renderReferencedAuthors(data.referenced_authors);
  renderFoundAuthors(data.found_authors);
  renderLabelValidation(data.correct_labels_count, data.incorrect_labels);
  renderUrlHealth(data.found_urls[0])
  document.getElementById("pdfContent").innerText = data.text_content;
  document.getElementById("fileInfo").style.display = "block";
};

function renderReferencedAuthors(authors) {
  const referencedAuthorsList = document.getElementById('referencedAuthorsList');
  referencedAuthorsList.innerHTML = '';
  if (authors.length > 0) {
      authors.forEach(author => {
          const authorItem = document.createElement('li');
          authorItem.innerText = author;
          referencedAuthorsList.appendChild(authorItem);
      });
      document.getElementById('referencedAuthorsDiv').style.display = 'block';
  } else {
    referencedAuthorsList.innerHTML = "No referenced authors found";
  }
}

function renderFoundAuthors(foundAuthors) {
  const foundAuthorsList = document.getElementById('foundAuthorsList');
  foundAuthorsList.innerHTML = '';
  if (Object.keys(foundAuthors).length > 0) {
      for (const author in foundAuthors) {
          const occurrences = foundAuthors[author];
          const authorItem = document.createElement('li');
          authorItem.innerText = `${author} (Occurrences: ${occurrences.length})`;
          foundAuthorsList.appendChild(authorItem);
      }
      document.getElementById('foundAuthorsDiv').style.display = 'block';
  }
}

function renderLabelValidation(correctLabelsCount, incorrectLabels) {
  const correctLabelsCountElement = document.getElementById('correctLabelsCount');
  correctLabelsCountElement.innerText = `Number of Correct Labels: ${correctLabelsCount}`;

  const incorrectLabelsList = document.getElementById('incorrectLabelsList');
  incorrectLabelsList.innerHTML = '';
  if (incorrectLabels.length > 0) {
    incorrectLabels.forEach(label => {
      const li = document.createElement('li');
      li.innerText = label;
      incorrectLabelsList.appendChild(li);
    });
    document.getElementById('incorrectLabelsDiv').style.display = 'block';
  } else {
    incorrectLabelsList.innerHTML = "All labels are correct";
  }
}


function renderUrlHealth(referenceUrls) {
  const referencedUrlsList = document.getElementById('referencedUrlsList');
  referencedUrlsList.innerHTML = '';
  if (Object.keys(referenceUrls).length > 0) {
    for (const item in referenceUrls) {
      const currentUrl = referenceUrls[item][0].url;
      const currentResp = referenceUrls[item][1].resp;
      const listItem = document.createElement('li');
      listItem.innerText = `${currentUrl} Code: ${currentResp}`;
      referencedUrlsList.append(listItem);
    }
    document.getElementById('referencedUrlsDiv').style.display = 'block';
  }
}

document.getElementById("fileButton").addEventListener("click", uploadFile);
