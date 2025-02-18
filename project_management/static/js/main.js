// Initialize tooltips
var tooltipTriggerList = [].slice.call(
  document.querySelectorAll('[data-bs-toggle="tooltip"]')
);
var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
  return new bootstrap.Tooltip(tooltipTriggerEl);
});

// File upload handling
document
  .querySelector(".upload-area")
  .addEventListener("dragover", function (e) {
    e.preventDefault();
    this.classList.add("border-primary");
  });

document
  .querySelector(".upload-area")
  .addEventListener("dragleave", function (e) {
    e.preventDefault();
    this.classList.remove("border-primary");
  });

document.querySelector(".upload-area").addEventListener("drop", function (e) {
  e.preventDefault();
  this.classList.remove("border-primary");
  // Handle file upload
});

// Logout function
function logout() {
  // Add your logout logic here
  window.location.href = "login.html";
}

// Add this to your existing JavaScript
document.addEventListener("DOMContentLoaded", function () {
  const dropZone = document.querySelector(".upload-area");
  const projectImages = new Set();

  // Prevent default drag behaviors
  ["dragenter", "dragover", "dragleave", "drop"].forEach((eventName) => {
    dropZone.addEventListener(eventName, preventDefaults, false);
    document.body.addEventListener(eventName, preventDefaults, false);
  });

  // Highlight drop zone when item is dragged over it
  ["dragenter", "dragover"].forEach((eventName) => {
    dropZone.addEventListener(eventName, highlight, false);
  });

  ["dragleave", "drop"].forEach((eventName) => {
    dropZone.addEventListener(eventName, unhighlight, false);
  });
  const uploadProfileImgBtn = document.querySelector("#uploadProfileImgBtn");
  uploadProfileImgBtn.onclick = function () {
    document.querySelector("#profilePhotoInput").click();
  };
  // Handle dropped files
  dropZone.addEventListener("drop", handleDrop, false);

  function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
  }

  function highlight(e) {
    dropZone.classList.add("border-primary", "bg-light");
  }

  function unhighlight(e) {
    dropZone.classList.remove("border-primary", "bg-light");
  }

  function handleDrop(e) {
    const dt = e.dataTransfer;
    const files = dt.files;
    handleFiles(files);
  }

  function handleFiles(files) {
    [...files].forEach(previewFile);
  }

  function previewFile(file) {
    if (!file.type.startsWith("image/")) {
      alert("Please upload only image files.");
      return;
    }

    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onloadend = function () {
      const img = document.createElement("img");
      img.src = reader.result;
      img.classList.add("img-thumbnail", "m-2");
      img.style.maxWidth = "150px";

      const container = document.createElement("div");
      container.classList.add("position-relative", "d-inline-block");

      const removeBtn = document.createElement("button");
      removeBtn.innerHTML = "×";
      removeBtn.classList.add(
        "btn",
        "btn-danger",
        "btn-sm",
        "position-absolute",
        "top-0",
        "end-0"
      );
      removeBtn.onclick = function () {
        container.remove();
        projectImages.delete(file);
      };

      container.appendChild(img);
      container.appendChild(removeBtn);

      // Add preview container before the drop zone
      dropZone.parentNode.insertBefore(container, dropZone);
      projectImages.add(file);
    };
  }

  // Also handle file input selection
  dropZone.onclick = function () {
    const input = document.createElement("input");
    input.type = "file";
    input.multiple = true;
    input.accept = "image/*";
    input.onchange = function () {
      handleFiles(this.files);
    };
    input.click();
  };
});

document.addEventListener("DOMContentLoaded", function () {
  const fileDropZone = document.querySelector(".upload-file-area");
  const acceptedFiles = new Set();

  // Prevent default drag behaviors
  ["dragenter", "dragover", "dragleave", "drop"].forEach((eventName) => {
    fileDropZone.addEventListener(eventName, preventDefaults, false);
    document.body.addEventListener(eventName, preventDefaults, false);
  });

  // Highlight drop zone when item is dragged over it
  ["dragenter", "dragover"].forEach((eventName) => {
    fileDropZone.addEventListener(eventName, highlight, false);
  });

  ["dragleave", "drop"].forEach((eventName) => {
    fileDropZone.addEventListener(eventName, unhighlight, false);
  });

  fileDropZone.addEventListener("drop", handleDrop, false);

  function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
  }

  function highlight(e) {
    fileDropZone.classList.add("border-primary", "bg-light");
  }

  function unhighlight(e) {
    fileDropZone.classList.remove("border-primary", "bg-light");
  }

  function handleDrop(e) {
    const dt = e.dataTransfer;
    const files = dt.files;
    handleFiles(files);
  }

  function handleFiles(files) {
    [...files].forEach(previewFile);
  }

  function previewFile(file) {
    const allowedTypes = [
      "application/pdf",
      "application/vnd.ms-powerpoint",
      "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    ];
    if (!allowedTypes.includes(file.type)) {
      alert("Please upload only PDF or PPT files.");
      return;
    }

    const container = document.createElement("div");
    container.classList.add(
      "position-relative",
      "d-inline-block",
      "p-2",
      "border",
      "rounded",
      "m-2"
    );

    const fileName = document.createElement("p");
    fileName.textContent = file.name;
    fileName.classList.add("mb-1", "text-truncate");

    const removeBtn = document.createElement("button");
    removeBtn.innerHTML = "×";
    removeBtn.classList.add(
      "btn",
      "btn-danger",
      "btn-sm",
      "position-absolute",
      "top-0",
      "end-0"
    );
    removeBtn.onclick = function () {
      container.remove();
      acceptedFiles.delete(file);
    };

    container.appendChild(fileName);
    container.appendChild(removeBtn);

    // Add preview container before the drop zone
    fileDropZone.parentNode.insertBefore(container, fileDropZone);
    acceptedFiles.add(file);
  }

  // Also handle file input selection
  fileDropZone.onclick = function () {
    const input = document.createElement("input");
    input.type = "file";
    input.multiple = true;
    input.accept = ".pdf,.ppt,.pptx";
    input.onchange = function () {
      handleFiles(this.files);
    };
    input.click();
  };
});
