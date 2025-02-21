function downloadPDF() {
  // Get all values from the form using DOM
  const getFormValue = (id) => document.getElementById(id)?.value || "";
  const getMultiSelectValues = (id) => {
    const select = document.getElementById(id);
    if (!select) return "";
    return Array.from(select.selectedOptions)
      .map((option) => option.value)
      .join(", ");
  };

  // Extract all form values
  const formValues = {
    projectName: getFormValue("projectName"),
    description: getFormValue("description"),
    startDate: getFormValue("startDate"),
    endDate: getFormValue("endDate"),
    priority: getFormValue("priority"),
    status: getFormValue("status"),
    teamLeader: getFormValue("teamLeader"),
    teamMembers: getMultiSelectValues("teamMembers"),
    faculty: getFormValue("faculty"),
    specialty: getFormValue("specialty"),
    budget: getFormValue("budget"),
    department: getFormValue("department"),
    notes: getFormValue("notes"),
  };

  // Create new jsPDF instance
  const { jsPDF } = window.jspdf;
  const doc = new jsPDF();

  // Set initial y position for text
  let yPos = 20;

  // Add title
  doc.setFontSize(16);
  doc.setFont("helvetica", "bold");
  doc.text("Project Details", 20, yPos);
  yPos += 10;

  // Reset font for content
  doc.setFontSize(12);
  doc.setFont("helvetica", "normal");

  // Basic Information
  doc.setFont("helvetica", "bold");
  doc.text("Basic Information:", 20, yPos);
  doc.setFont("helvetica", "normal");
  yPos += 10;

  doc.text(`Project Name: ${formValues.projectName}`, 25, yPos);
  yPos += 7;

  const splitDescription = doc.splitTextToSize(
    `Description: ${formValues.description}`,
    170
  );
  doc.text(splitDescription, 25, yPos);
  yPos += splitDescription.length * 7 + 5;

  doc.text(`Start Date: ${formValues.startDate}`, 25, yPos);
  yPos += 7;
  doc.text(`End Date: ${formValues.endDate}`, 25, yPos);
  yPos += 10;

  // Project Details
  doc.setFont("helvetica", "bold");
  doc.text("Project Details:", 20, yPos);
  doc.setFont("helvetica", "normal");
  yPos += 10;

  doc.text(`Priority: ${formValues.priority}`, 25, yPos);
  yPos += 7;
  doc.text(`Status: ${formValues.status}`, 25, yPos);
  yPos += 10;

  // Team Information
  doc.setFont("helvetica", "bold");
  doc.text("Team Information:", 20, yPos);
  doc.setFont("helvetica", "normal");
  yPos += 10;

  doc.text(`Team Leader: ${formValues.teamLeader}`, 25, yPos);
  yPos += 7;

  const splitTeamMembers = doc.splitTextToSize(
    `Team Members: ${formValues.teamMembers}`,
    170
  );
  doc.text(splitTeamMembers, 25, yPos);
  yPos += splitTeamMembers.length * 7 + 5;

  // Additional Information
  doc.setFont("helvetica", "bold");
  doc.text("Additional Information:", 20, yPos);
  doc.setFont("helvetica", "normal");
  yPos += 10;

  doc.text(`Faculty: ${formValues.faculty}`, 25, yPos);
  yPos += 7;
  doc.text(`Specialty: ${formValues.specialty}`, 25, yPos);
  yPos += 7;
  doc.text(`Budget: ${formValues.budget}`, 25, yPos);
  yPos += 7;
  doc.text(`Department: ${formValues.department}`, 25, yPos);
  yPos += 7;

  if (formValues.notes) {
    const splitNotes = doc.splitTextToSize(`Notes: ${formValues.notes}`, 170);
    doc.text(splitNotes, 25, yPos);
  }

  // Save the PDF
  doc.save("project-details.pdf");
}
