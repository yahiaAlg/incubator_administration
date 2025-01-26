document.addEventListener("DOMContentLoaded", function () {
  // get all the buttons and make them full width inside
  var buttons = document.querySelectorAll("button");
  buttons.forEach(function (button) {
    button.style.width = "100%";
    button.style.marginBottom = "0.5rem";
    // get the reset button and add a BS5 class btn-danger to it
    if (button.type =="reset") {
        button.classList.remove("btn-primary");
        button.classList.add("btn-danger");
    }
  });

});
