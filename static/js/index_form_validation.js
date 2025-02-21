// Initialize DataTable
$(document).ready(function () {
  $("#projectsTable").DataTable({
    responsive: true,
    order: [[0, "asc"]],
    pageLength: 10,
    language: {
      search: "Search: ",
      lengthMenu: "Show _MENU_ entries per page",
      info: "Showing _START_ to _END_ of _TOTAL_ projects",
    },
  });
});

// Form validation
document
  .getElementById("addProjectForm")
  .addEventListener("submit", function (e) {
    e.preventDefault();
    // Add your form submission logic here
  });

document
  .getElementById("editProjectForm")
  .addEventListener("submit", function (e) {
    e.preventDefault();
    // Add your form submission logic here
  });
