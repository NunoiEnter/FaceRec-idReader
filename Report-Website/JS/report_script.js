
// Function to toggle sidebar
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    const content = document.querySelector('.content');
    if (sidebar.style.left === "0px") {
        sidebar.style.left = "-250px";
        content.style.marginLeft = "0";
    } else {
        sidebar.style.left = "0px";
        content.style.marginLeft = "250px";
    }
}

// Function to close sidebar when clicking outside
document.addEventListener('click', function(event) {
    const sidebar = document.getElementById('sidebar');
    const content = document.querySelector('.content');
    const toggleBtn = document.querySelector('.toggle-btn');
    if (event.target !== sidebar && event.target !== toggleBtn && !sidebar.contains(event.target)) {
        sidebar.style.left = "-250px";
        content.style.marginLeft = "0";
    }
});


var dropdown = document.getElementsByClassName("dropdown-btn");
var i;

for (i = 0; i < dropdown.length; i++) {
  dropdown[i].addEventListener("click", function() {
    this.classList.toggle("active");
    var dropdownContent = this.nextElementSibling;
    if (dropdownContent.style.display === "block") {
      dropdownContent.style.display = "none";
    } else {
      dropdownContent.style.display = "block";
    }
  });
}

document.getElementById('yearDropdown').addEventListener('change', function() {
  var selectedYear = this.value; // Get the selected year from the dropdown
  fetch('/php/chart_data.php?year=' + selectedYear) // Fetch data for the selected year
      .then(response => response.json())
      .then(gender_data => {
          // Update the chart data with the new data
          genderChart.data.datasets[0].data = Object.values(gender_data);
          genderChart.update(); // Update the chart
      })
      .catch(error => console.error('Error fetching gender data:', error));
});