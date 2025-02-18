// Initialize DataTable with modified columns
$(document).ready(function () {
  const table = $("#projectsTable").DataTable({
    responsive: true,
    order: [[0, "asc"]],
    pageLength: 10,
    language: {
      search: "Search: ",
      lengthMenu: "Show _MENU_ entries per page",
      info: "Showing _START_ to _END_ of _TOTAL_ projects",
    },
  });

  // CSV Export functionality
  $("#exportCSV").on("click", function () {
    // Create CSV content
    let csv = "Project Name,Team Leader,Start Date,Status\n";

    // Get all data from DataTable
    const data = table.rows().data();

    data.each(function (row) {
      // Clean and format the data
      const projectName = row[0].replace(/,/g, " ");
      const teamLeader = row[1].replace(/,/g, " ");
      const startDate = row[2];
      // Extract status text from span element
      const status = $(row[3]).text();

      csv += `${projectName},${teamLeader},${startDate},${status}\n`;
    });

    // Create download link
    const blob = new Blob([csv], { type: "text/csv" });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.setAttribute("hidden", "");
    a.setAttribute("href", url);
    a.setAttribute("download", "projects_export.csv");
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  });
});
