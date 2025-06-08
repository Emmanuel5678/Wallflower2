document.addEventListener('DOMContentLoaded', function() {
    const slides = document.querySelectorAll('.slide');
    const dotsContainer = document.querySelector('.slider-dots');
    let currentSlide = 0;
    const slideInterval = 5000; // 5 seconds

    // Create dots
    slides.forEach((slide, index) => {
        const dot = document.createElement('div');
        dot.classList.add('dot');
        if (index === 0) dot.classList.add('active');
        dot.addEventListener('click', () => goToSlide(index));
        dotsContainer.appendChild(dot);
    });

    const dots = document.querySelectorAll('.dot');

    // Next slide function
    function nextSlide() {
        goToSlide((currentSlide + 1) % slides.length);
    }

    // Go to specific slide
    function goToSlide(n) {
        slides[currentSlide].classList.remove('active');
        dots[currentSlide].classList.remove('active');
        currentSlide = n;
        slides[currentSlide].classList.add('active');
        dots[currentSlide].classList.add('active');
    }

    // Auto slide
    let slideTimer = setInterval(nextSlide, slideInterval);

    // Pause on hover
    const sliderContainer = document.querySelector('.slider-container');
    sliderContainer.addEventListener('mouseenter', () => {
        clearInterval(slideTimer);
    });

    sliderContainer.addEventListener('mouseleave', () => {
        slideTimer = setInterval(nextSlide, slideInterval);
    });

    // Navigation buttons
    document.querySelector('.prev').addEventListener('click', () => {
        clearInterval(slideTimer);
        goToSlide((currentSlide - 1 + slides.length) % slides.length);
        slideTimer = setInterval(nextSlide, slideInterval);
    });

    document.querySelector('.next').addEventListener('click', () => {
        clearInterval(slideTimer);
        nextSlide();
        slideTimer = setInterval(nextSlide, slideInterval);
    });
});