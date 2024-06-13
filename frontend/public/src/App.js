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
  setLoading(true);
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
    setLoading(false);
  }
};

const displayResults = (data) => {
  //format and display what backend spits out
  document.getElementById("fileInfo").style.visibility = "visible";
  document.getElementById("reportDashboard").style.visibility = "visible";

  document.getElementById("message").innerText = data.message;
  document.getElementById("fileName").innerText = data.file_name;
  document.getElementById("reportFileName").innerText = data.file_name;
  document.getElementById("pagesAmount").innerText = data.pages_amount;

  document.getElementById("statedEqualsActual").innerText =
    data.stated_equals_actual;

  renderResults.renderFontsTable(data.text_blocks);

  // User doesn't need to see these
  //renderResults.renderTextBlocks(data.text_blocks); //Renders all text in doc in blocks sorted by font
  //document.getElementById("pdfContent").innerText = data.text_content; //Displays all text in doc

  renderAuthors(data.found_authors, data.referenced_authors);
  renderLabelValidation(data.correct_labels_count, data.incorrect_labels);
  renderUrlHealth(data.found_urls[0]);
  renderAllUrls(data.found_urls[0]);

  renderReferencedAuthors(data.referenced_authors);

  setLoading(false);
  //Reveal tab buttons
  const tabBtns = document.getElementsByClassName("tabButton");
  for (let i = 0; i < tabBtns.length; i++) {
    tabBtns[i].style.display = "block";
  }
  //Open file info tab
  document.getElementById("infoTabButton").click();

  document.getElementById("fileInfo").style.display = "block";
  document.getElementById("reportDashboard").style.display = "block";
};

//Displays loading ball animation
//Call: setLoading(true/false)
const setLoading = (loading) => {
  let isLoading = loading;
  if (isLoading) {
    document.getElementById("loadingBall").style.display = "block";
  } else {
    document.getElementById("loadingBall").style.display = "none";
  }
};

function renderAuthors(foundAuthors, allAuthors) {
  const authorsTable = document.getElementById("foundAuthorsTable");
  document.getElementById("allAuthorsFound").innerHTML = "";
  authorsTable.innerHTML = "";
  authorsTable.innerHTML += `<tr>
  <th>Author</th>
  <th>Occurences</th>
</tr>`;
  let authorCounter = 0;
  allAuthors.sort();
  //This lists only Authors with 0 occurrences
  if (allAuthors.length > 0) {
    for (const index in allAuthors) {
      const author = allAuthors[index];
      if (Object.keys(foundAuthors).includes(author)) {
        //const occurrences = foundAuthors[author];
        //const authorItem = `<tr><td>${author}</td><td>${occurrences.length}</td></tr>`;
        //authorsTable.innerHTML += authorItem;
      } else {
        const authorItem = `<tr><td>${author}</td><td>0</td></tr>`;
        authorsTable.innerHTML += authorItem;
        authorCounter += 1;
      }
    }
    if (authorCounter == 0) {
      document.getElementById("allAuthorsFound").innerHTML =
        "All referenced authors found in text! 👍";
    }
    document.getElementById("foundAuthorsDiv").style.display = "block";
    document.getElementById("repAuthors").innerHTML = `Authors found in text: ${
      allAuthors.length - authorCounter
    }, total authors: ${allAuthors.length}`;
  }
}

function renderLabelValidation(correctLabelsCount, incorrectLabels) {
  const correctLabelsCountElement =
    document.getElementById("correctLabelsCount");
  correctLabelsCountElement.innerText = `Number of Correct Labels: ${correctLabelsCount}`;
  document.getElementById("labelsOk").innerText = "";

  //For report tab
  let totalLabels = correctLabelsCount + incorrectLabels.length;
  document.getElementById(
    "reportLabelsCount"
  ).innerText = `Correct labels: ${correctLabelsCount}, total labels: ${totalLabels}`;

  const incorrectLabelsTable = document.getElementById("incorrectLabelsTable");
  incorrectLabelsTable.innerHTML = "";
  incorrectLabelsTable.innerHTML += `<tr><th>Label</th><tr>`;
  if (incorrectLabels.length > 0) {
    incorrectLabels.forEach((label) => {
      const tableItem = `<tr><td>${label}</td></tr>`;
      incorrectLabelsTable.innerHTML += tableItem;
    });
  } else {
    document.getElementById("labelsOk").innerText =
      "All labels are correct! 👍";
  }
  document.getElementById("incorrectLabelsDiv").style.display = "block";
}

const renderUrlHealth = (referenceUrls) => {
  const referencedUrlsTable = document.getElementById("referencedUrlsTable");
  document.getElementById("allUrlsOk").innerHTML = "";
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

        const tableItem = `<tr><td><a href="${currentUrl}" target="_blank" rel="noopener noreferrer">${currentUrl}</a></td><td>${errorMessage}</td></tr>`;
        referencedUrlsTable.innerHTML += tableItem;
      } else {
        okUrlCounter += 1;
      }
      totalUrlCounter += 1;
    }
  }
  if (totalUrlCounter == okUrlCounter) {
    document.getElementById("allUrlsOk").innerHTML =
      "All referenced URLs ok. 👍";
  }
  document.getElementById("referencedUrlsDiv").style.display = "block";
  document.getElementById(
    "okUrls"
  ).innerText = `Working URLs: ${okUrlCounter}, total URLs: ${totalUrlCounter}`;
  document.getElementById(
    "repOkUrls"
  ).innerText = `Working URLs: ${okUrlCounter}, total URLs: ${totalUrlCounter}`;
};

//-----------REPORT TAB RENDERERS-----------//

const renderAllUrls = (urls) => {
  const urlsTable = document.getElementById("allUrlsTable");
  urlsTable.innerHTML = "";
  urlsTable.innerHTML = `<tr><th>URL</th></tr>`;

  if (Object.keys(urls).length > 0) {
    for (const item in urls) {
      const currentUrl = urls[item][0].url;
      const tableItem = `<tr><td><a href="${currentUrl}" target="_blank" rel="noopener noreferrer">${currentUrl}</a></td></tr>`;
      urlsTable.innerHTML += tableItem;
    }
    document.getElementById("allFoundUrlsDiv").style.display = "block";
  }
};

const renderReferencedAuthors = (authors) => {
  const allAuthorsTable = document.getElementById("allAuthorsTable");
  allAuthorsTable.innerHTML = "";
  allAuthorsTable.innerHTML += `<tr><th>Author</th></tr>`;
  if (authors.length > 0) {
    authors.forEach((author) => {
      const authorItem = `<tr><td>${author}</td></tr>`;
      allAuthorsTable.innerHTML += authorItem;
    });
  } else {
    allAuthorsTable.innerHTML += "No referenced authors found";
  }
};

//-----------EVENT LISTENERS-----------//
document.getElementById("fileButton").addEventListener("click", uploadFile);

document.getElementById("infoTabButton").addEventListener("click", () => {
  document.getElementById("infoTab").style.display = "block";
  document.getElementById("reportTab").style.display = "none";
});

document.getElementById("reportTabButton").addEventListener("click", () => {
  document.getElementById("infoTab").style.display = "none";
  document.getElementById("reportTab").style.display = "block";
});
