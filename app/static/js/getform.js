droparea = document.getElementById("drop-area");
droparea.addEventListener("click", function () {
  openFileInput();
});
function openFileInput() {
  document.getElementById("fileInput").click();
}

function handleDragOver(event) {
  event.preventDefault();
  event.dataTransfer.dropEffect = "copy";
}

function handleDragEnter(event) {
  event.preventDefault();
  document.getElementById("drop-area").classList.add("highlight");
}

function handleDragLeave(event) {
  event.preventDefault();
  document.getElementById("drop-area").classList.remove("highlight");
}

function handleDrop(event) {
  event.preventDefault();
  document.getElementById("drop-area").classList.remove("highlight");
  const files = event.dataTransfer.files;
  handleFiles(files);
}

function handleFiles(files) {
  for (const file of files) {
    console.log("File name:", file.name);
    console.log("File type:", file.type);
    console.log("File size:", file.size, "bytes");
    // You can perform further processing with the file here
  }
}

document.getElementById("fileInput").addEventListener("change", function () {
  const files = this.files;
  handleFiles(files);
});
