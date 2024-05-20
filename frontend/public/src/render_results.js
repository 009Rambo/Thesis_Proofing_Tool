//Functions to render textblocks etc analysis results go here

export function renderTextBlocks(textBlocks) {
  const textGroups = groupTextBlocksByFont(textBlocks);

  const paragraphsList = document.getElementById("paragraphsList");
  const headingsList = document.getElementById("headingsList");

  paragraphsList.innerHTML = "";
  headingsList.innerHTML = "";

  // Render paragraphs
  if (textGroups.paragraphs) {
    for (const fontKey in textGroups.paragraphs) {
      const fontBlocks = textGroups.paragraphs[fontKey];
      const fontDetails = fontBlocks[0]; // Use the first block to get font details

      const paragraphItem = document.createElement("li");
      paragraphItem.innerText = fontBlocks
        .map((block) => block.text)
        .join("\n");
      paragraphsList.appendChild(paragraphItem);

      const paragraphDetails = document.createElement("span");
      paragraphDetails.innerText = `(Font Size: ${fontDetails.font_size}, Font Name: ${fontDetails.font_name})`;
      paragraphDetails.style.fontWeight = "bold";
      paragraphItem.appendChild(paragraphDetails);
    }
    document.getElementById("paragraphsDiv").style.display = "block";
  }

  // Render headings
  if (textGroups.headings) {
    for (const fontKey in textGroups.headings) {
      const fontBlocks = textGroups.headings[fontKey];
      const fontDetails = fontBlocks[0]; // Use the first block to get font details

      const headingItem = document.createElement("li");
      headingItem.innerText = fontBlocks.map((block) => block.text).join("\n");
      headingsList.appendChild(headingItem);

      const headingDetails = document.createElement("span");
      headingDetails.innerText = `(Font Size: ${fontDetails.font_size}, Font Name: ${fontDetails.font_name})`;
      headingDetails.style.fontWeight = "bold";
      headingItem.appendChild(headingDetails);
    }
    document.getElementById("headingsDiv").style.display = "block";
  }

  // Render numbers
  if (textBlocks.numbers) {
    const numbersList = document.getElementById("numbersList");
    numbersList.innerHTML = "";
    for (const number of textBlocks.numbers) {
      const numberItem = document.createElement("li");
      numberItem.innerText = number.text;
      numbersList.appendChild(numberItem);
    }
    document.getElementById("numbersDiv").style.display = "block";
  }

  // Render table of contents
  if (textBlocks.table_of_contents) {
    const tocList = document.getElementById("tocList");
    tocList.innerHTML = "";
    for (const toc of textBlocks.table_of_contents) {
      const tocItem = document.createElement("li");
      tocItem.innerText = toc.text;
      tocList.appendChild(tocItem);
    }
    document.getElementById("tocDiv").style.display = "block";
  }
}

function groupTextBlocksByFont(textBlocks) {
  const textGroups = {
    paragraphs: {},
    headings: {},
  };

  textBlocks.paragraphs.forEach((block) => {
    const key = `${block.font_size}-${block.font_name}`;
    if (!textGroups.paragraphs[key]) {
      textGroups.paragraphs[key] = [];
    }
    textGroups.paragraphs[key].push(block);
  });

  textBlocks.headings.forEach((block) => {
    const key = `${block.font_size}-${block.font_name}`;
    if (!textGroups.headings[key]) {
      textGroups.headings[key] = [];
    }
    textGroups.headings[key].push(block);
  });

  return textGroups;
}

