document.addEventListener("DOMContentLoaded", () => {
  // Learner dashboard - Course completion rate chart
  const completionChartEl = document.getElementById("completionChart")
  if (completionChartEl) {
    const completionRate = Number.parseFloat(completionChartEl.dataset.completionRate)

    new Chart(completionChartEl, {
      type: "doughnut",
      data: {
        labels: ["Completed", "In Progress"],
        datasets: [
          {
            data: [completionRate, 100 - completionRate],
            backgroundColor: ["#28a745", "#e9ecef"], // Green for completed
            borderWidth: 0,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        cutout: "75%",
        plugins: {
          legend: {
            position: "bottom",
          },
          tooltip: {
            callbacks: {
              label: (context) => context.label + ": " + context.raw + "%",
            },
          },
        },
      },
    })
  }

  // Instructor dashboard - Course engagement chart
  const engagementChartEl = document.getElementById("engagementChart")
  if (engagementChartEl) {
    const courseLabels = JSON.parse(engagementChartEl.dataset.labels)
    const learnerCounts = JSON.parse(engagementChartEl.dataset.learnerCounts)
    const completionCounts = JSON.parse(engagementChartEl.dataset.completionCounts)

    new Chart(engagementChartEl, {
      type: "bar",
      data: {
        labels: courseLabels,
        datasets: [
          {
            label: "Number of Learners",
            data: learnerCounts,
            backgroundColor: "#28a745", // Green for learners
            borderWidth: 0,
          },
          {
            label: "Completions",
            data: completionCounts,
            backgroundColor: "#20c997", // Lighter green for completions
            borderWidth: 0,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: {
            grid: {
              display: false,
            },
          },
          y: {
            beginAtZero: true,
            ticks: {
              precision: 0,
            },
          },
        },
      },
    })
  }
})
