document.addEventListener('DOMContentLoaded', function () {
    const slidesContainer = document.getElementById('carousel-slides');
    const dots = document.querySelectorAll('.dot');
    let currentSlide = 0;
    const totalSlides = dots.length;
    let autoSlideInterval;

    // Function to update slide position
    function updateSlidePosition() {
        slidesContainer.style.transform = `translateX(-${currentSlide * 100}%)`;

        // Update dots
        dots.forEach((dot, index) => {
            if (index === currentSlide) {
                dot.classList.add('bg-secondary');
                dot.classList.remove('bg-gray-300');
            } else {
                dot.classList.remove('bg-secondary');
                dot.classList.add('bg-gray-300');
            }
        });
    }

    // Function to go to next slide
    function nextSlide() {
        currentSlide = (currentSlide + 1) % totalSlides;
        updateSlidePosition();
    }

    // Add click event listeners to dots
    dots.forEach((dot, index) => {
        dot.addEventListener('click', () => {
            currentSlide = index;
            updateSlidePosition();
            resetAutoSlide();
        });
    });

    // Function to start auto-sliding
    function startAutoSlide() {
        autoSlideInterval = setInterval(nextSlide, 5000); // Change slide every 5 seconds
    }

    // Function to reset auto-slide timer
    function resetAutoSlide() {
        clearInterval(autoSlideInterval);
        startAutoSlide();
    }

    // Touch events for mobile swipe
    let touchStartX = 0;
    let touchEndX = 0;

    slidesContainer.addEventListener('touchstart', (e) => {
        touchStartX = e.touches[0].clientX;
    }, false);

    slidesContainer.addEventListener('touchmove', (e) => {
        touchEndX = e.touches[0].clientX;
    }, false);

    slidesContainer.addEventListener('touchend', () => {
        const swipeThreshold = 50; // minimum distance for a swipe
        const difference = touchStartX - touchEndX;

        if (Math.abs(difference) > swipeThreshold) {
            if (difference > 0) {
                // Swipe left - next slide
                currentSlide = (currentSlide + 1) % totalSlides;
            } else {
                // Swipe right - previous slide
                currentSlide = (currentSlide - 1 + totalSlides) % totalSlides;
            }
            updateSlidePosition();
            resetAutoSlide();
        }
    }, false);

    // Initialize carousel
    updateSlidePosition();
    startAutoSlide();
});