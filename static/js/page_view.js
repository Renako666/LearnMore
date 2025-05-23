document.addEventListener('DOMContentLoaded', function() {
    // Initialize progress bar
    const progressBar = document.querySelector('.progress-bar');
    if (progressBar) {
        const progress = progressBar.getAttribute('data-progress');
        progressBar.style.width = progress + '%';
    }

    // Get navigation data
    const navigationData = document.getElementById('navigationData');
    if (navigationData) {
        const prevUrl = navigationData.getAttribute('data-prev-url');
        const nextUrl = navigationData.getAttribute('data-next-url');

        // Add keyboard navigation
        document.addEventListener('keydown', function(e) {
            if (e.key === 'ArrowLeft' && prevUrl) {
                window.location.href = prevUrl;
            } else if (e.key === 'ArrowRight' && nextUrl) {
                window.location.href = nextUrl;
            }
        });

        // Add click handlers for navigation buttons
        const prevButton = document.getElementById('prevPageBtn');
        const nextButton = document.getElementById('nextPageBtn');

        if (prevButton && prevUrl) {
            prevButton.addEventListener('click', function(e) {
                e.preventDefault();
                window.location.href = prevUrl;
            });
        }

        if (nextButton && nextUrl) {
            nextButton.addEventListener('click', function(e) {
                e.preventDefault();
                window.location.href = nextUrl;
            });
        }
    }
}); 