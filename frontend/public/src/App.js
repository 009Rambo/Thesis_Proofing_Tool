//App.js

const uploadFile = async (event) => {
    //uploading file to backend goes here
    const file = event.target.files[0];
    
    const formData = new FormData();
    formData.append("file", file);

    try {
        const resp = await fetch("http://localhost:5000/upload", {
            method: "POST",
            body: formData,
        })

        const data = await resp.json();

        displayResults(data);
    } catch (error) {
        console.error(error);
    }
}

const displayResults = (data) => {
    //format and display what backend spits out
    const resultsContainer = document.getElementById("results");
    resultsContainer.innerHTML = `<h2>${data.message}</h2>`
}

document.getElementById("fileInput").addEventListener("change", uploadFile);