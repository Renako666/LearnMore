document.addEventListener("DOMContentLoaded", () => {
  // Page navigation functionality
  const pageLinks = document.querySelectorAll(".page-link")
  const pageContents = document.querySelectorAll(".page-content")
  const prevButton = document.querySelector(".prev-page")
  const nextButton = document.querySelector(".next-page")
  let currentPageIndex = 0

  // Function to update navigation buttons
  function updateNavButtons() {
    prevButton.disabled = currentPageIndex === 0
    nextButton.disabled = currentPageIndex === pageLinks.length - 1
  }

  // Function to show a specific page
  function showPage(index) {
    // Hide all pages
    pageLinks.forEach((link) => link.classList.remove("active"))
    pageContents.forEach((content) => content.classList.add("d-none"))

    // Show selected page
    pageLinks[index].classList.add("active")
    pageContents[index].classList.remove("d-none")
    currentPageIndex = index

    // Update navigation buttons
    updateNavButtons()

    // Record page view if user is logged in
    const pageId = pageLinks[index].dataset.pageId
    const courseId = pageLinks[index].dataset.courseId
    if (pageId && courseId) {
      fetch(`/courses/${courseId}/page/${pageId}/view/`, {
        method: "POST",
        headers: {
          "X-CSRFToken": getCookie("csrftoken"),
          "Content-Type": "application/json",
        },
        body: JSON.stringify({}),
      })
    }
  }

  // Set up page link click handlers
  pageLinks.forEach((link, index) => {
    link.addEventListener("click", (e) => {
      e.preventDefault()
      showPage(index)
    })
  })

  // Set up navigation button click handlers
  prevButton.addEventListener("click", () => {
    if (currentPageIndex > 0) {
      showPage(currentPageIndex - 1)
    }
  })

  nextButton.addEventListener("click", () => {
    if (currentPageIndex < pageLinks.length - 1) {
      showPage(currentPageIndex + 1)
    }
  })

  // Initialize navigation buttons
  updateNavButtons()

  // Helper function to get CSRF token
  function getCookie(name) {
    let cookieValue = null
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";")
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim()
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
          break
        }
      }
    }
    return cookieValue
  }

  // Print functionality
  const printButton = document.getElementById("print-course")
  if (printButton) {
    printButton.addEventListener("click", () => {
      window.print()
    })
  }
})
