// Scroll-triggered animations
document.addEventListener("scroll", () => {
  const elements = document.querySelectorAll(".fade-in");
  elements.forEach((el) => {
    if (el.getBoundingClientRect().top < window.innerHeight * 0.8) {
      el.classList.add("active");
    }
  });
});

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
  anchor.addEventListener("click", function (e) {
    e.preventDefault();
    document.querySelector(this.getAttribute("href")).scrollIntoView({
      behavior: "smooth",
    });
  });
});
