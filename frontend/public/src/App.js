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
  message.innerText = "Uploading, please wait...";
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

  document.getElementById("statedEqualsActual").innerText =
    data.stated_equals_actual;

  renderResults.renderFontsTable(data.text_blocks);
  // Only render blocks of text if debug is active (box is checked)
  // User doesn't need to see these anyway
  if (document.getElementById("debugCheck").checked == true) {
    renderResults.renderTextBlocks(data.text_blocks);
    document.getElementById("pdfContent").innerText = data.text_content;
  }

  //renderReferencedAuthors(data.referenced_authors);
  //renderFoundAuthors(data.found_authors);
  renderAuthors(data.found_authors, data.referenced_authors);
  renderLabelValidation(data.correct_labels_count, data.incorrect_labels);
  renderUrlHealth(data.found_urls[0]);
  console.log(data.found_urls[0]);
  document.getElementById("fileInfo").style.display = "block";
};

function renderAuthors(foundAuthors, allAuthors) {
  const authorsTable = document.getElementById("foundAuthorsTable");
  authorsTable.innerHTML = "";
  authorsTable.innerHTML += `<tr>
  <th>Author</th>
  <th>Occurences</th>
</tr>`;
  allAuthors.sort();
  if (allAuthors.length > 0) {
    for (const index in allAuthors) {
      const author = allAuthors[index];
      if (Object.keys(foundAuthors).includes(author)){
        const occurrences = foundAuthors[author];
        const authorItem = `<tr><td>${author}</td><td>${occurrences.length}</td></tr>`;
        authorsTable.innerHTML += authorItem;
      } else {
        const authorItem = `<tr><td>${author}</td><td>0</td></tr>`;
        authorsTable.innerHTML += authorItem;
      }      
    }    
    document.getElementById("foundAuthorsDiv").style.display = "block";
  }
}

function renderReferencedAuthors(authors) {
  const referencedAuthorsList = document.getElementById(
    "referencedAuthorsList"
  );
  referencedAuthorsList.innerHTML = "";
  if (authors.length > 0) {
    authors.forEach((author) => {
      const authorItem = document.createElement("li");
      authorItem.innerText = author;
      referencedAuthorsList.appendChild(authorItem);
    });
    document.getElementById("referencedAuthorsDiv").style.display = "block";
  } else {
    referencedAuthorsList.innerHTML = "No referenced authors found";
  }
}

function renderFoundAuthors(foundAuthors) {
  const foundAuthorsList = document.getElementById("foundAuthorsList");
  foundAuthorsList.innerHTML = "";
  if (Object.keys(foundAuthors).length > 0) {
    for (const author in foundAuthors) {
      const occurrences = foundAuthors[author];
      const authorItem = document.createElement("li");
      authorItem.innerText = `${author} (Occurrences: ${occurrences.length})`;
      foundAuthorsList.appendChild(authorItem);
    }
    document.getElementById("foundAuthorsDiv").style.display = "block";
  }
}

function renderLabelValidation(correctLabelsCount, incorrectLabels) {
  const correctLabelsCountElement =
    document.getElementById("correctLabelsCount");
  correctLabelsCountElement.innerText = `Number of Correct Labels: ${correctLabelsCount}`;

  const incorrectLabelsList = document.getElementById("incorrectLabelsList");
  incorrectLabelsList.innerHTML = "";
  if (incorrectLabels.length > 0) {
    incorrectLabels.forEach((label) => {
      const li = document.createElement("li");
      li.innerText = label;
      incorrectLabelsList.appendChild(li);
    });
    document.getElementById("incorrectLabelsDiv").style.display = "block";
  } else {
    incorrectLabelsList.innerHTML = "All labels are correct";
  }
}

const renderUrlHealth = (referenceUrls) => {
  const referencedUrlsTable = document.getElementById("referencedUrlsTable");
  //Empty the table and add the headers
  referencedUrlsTable.innerHTML = "";
  referencedUrlsTable.innerHTML += `<tr>
  <th>URL</th>
  <th>Status</th>
</tr>`;

  let okUrlCounter = 0;
  let totalUrlCounter = 0;

  if (Object.keys(referenceUrls).length > 0) {
    for (const item in referenceUrls) {
      const currentUrl = referenceUrls[item][0].url;
      const currentResp = referenceUrls[item][1].resp;
      // If URL doesn't return OK, add it to the table
      if (currentResp != 200) {
        let errorMessage = "";

        if (currentResp >= 400 && currentResp < 500) {
          errorMessage = `Client error (${currentResp})`;
        } else if (currentResp >= 500) {
          errorMessage = `Server error (${currentResp})`;
        } else if (currentResp == 0) {
          errorMessage = "Unknown";
        }

        const tableItem = `<tr><td>${currentUrl}</td><td>${errorMessage}</td></tr>`;
        referencedUrlsTable.innerHTML += tableItem;
      } else {
        okUrlCounter += 1;
      }
      totalUrlCounter += 1;
    }    
  }
  document.getElementById("referencedUrlsDiv").style.display = "block";
  document.getElementById(
    "okUrls"
  ).innerText = `Working URLs: ${okUrlCounter}, total URLs: ${totalUrlCounter}`;
}

document.getElementById("fileButton").addEventListener("click", uploadFile);
