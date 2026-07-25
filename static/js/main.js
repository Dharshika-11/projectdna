/* PROJECTDNA NEXUS Client Logic */
document.addEventListener('DOMContentLoaded', function () {
  // Sidebar Mobile Toggle
  const sidebarToggler = document.getElementById('sidebarToggle');
  const sidebar = document.querySelector('.nexus-sidebar');
  if (sidebarToggler && sidebar) {
    sidebarToggler.addEventListener('click', function () {
      sidebar.classList.toggle('active');
    });
  }

  // Auto-dismiss Alerts
  const alerts = document.querySelectorAll('.alert-dismissible');
  alerts.forEach(function (alert) {
    setTimeout(function () {
      const bsAlert = new bootstrap.Alert(alert);
      bsAlert.close();
    }, 5000);
  });
});

// Helper for rendering Chart.js Radar Vectors
function renderDNARadarChart(canvasId, labels, dataPoints) {
  const ctx = document.getElementById(canvasId);
  if (!ctx) return;

  new Chart(ctx, {
    type: 'radar',
    data: {
      labels: labels,
      datasets: [{
        label: 'DNA Vector Fingerprint Metrics',
        data: dataPoints,
        backgroundColor: 'rgba(78, 115, 223, 0.25)',
        borderColor: '#4e73df',
        pointBackgroundColor: '#4e73df',
        pointBorderColor: '#fff',
        pointHoverBackgroundColor: '#fff',
        pointHoverBorderColor: '#4e73df',
        borderWidth: 2,
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        r: {
          angleLines: { color: 'rgba(0, 0, 0, 0.1)' },
          grid: { color: 'rgba(0, 0, 0, 0.05)' },
          suggestedMin: 0,
          suggestedMax: 100
        }
      }
    }
  });
}
