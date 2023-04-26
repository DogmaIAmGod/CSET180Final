let complaintCount = parseInt(localStorage.getItem('complaintCount') || '0');
let reviewCount = parseInt(localStorage.getItem('reviewCount') || '0');

function updateIDs() {
  // Generate complaint ID with leading zeros
  const complaintId = (complaintCount + 1).toString().padStart(6, '0');

  // Generate review ID with leading zeros
  const reviewId = (reviewCount + 1).toString().padStart(6, '0');

  // Set input values with generated IDs
  document.getElementById('complaint-id').value = complaintId;
  document.getElementById('review-id').value = reviewId;
}

function submitForm(event) {
  event.preventDefault();

  // Get form values
  const name = document.getElementById('name').value;
  const email = document.getElementById('email').value;
  const complaintType = document.getElementById('complaint-type').value;
  const complaintText = document.getElementById('complaint-text').value;

  // Display submitted values in console
  console.log(`Complaint ID: ${document.getElementById('complaint-id').value}`);
  console.log(`Review ID: ${document.getElementById('review-id').value}`);
  console.log(`Name: ${name}`);
  console.log(`Email: ${email}`);
  console.log(`Complaint Type: ${complaintType}`);
  console.log(`Complaint Text: ${complaintText}`);

  // Increment complaint and review counts
  complaintCount++;
  reviewCount++;

  // Update counts in localStorage
  localStorage.setItem('complaintCount', complaintCount);
  localStorage.setItem('reviewCount', reviewCount);

  // Reset form and update IDs
  document.getElementById('complaint-form').reset();
  updateIDs();
}

function updateIDs() {
  // Generate complaint ID with leading zeros
  const complaintId = complaintCount.toString().padStart(6, '0');

  // Generate review ID with leading zeros
  const reviewId = reviewCount.toString().padStart(6, '0');

  // Set input values with generated IDs
  document.getElementById('complaint-id').value = complaintId;
  document.getElementById('review-id').value = reviewId;
}

  