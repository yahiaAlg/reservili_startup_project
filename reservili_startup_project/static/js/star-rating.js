document.addEventListener("DOMContentLoaded", function () {
  const starsContainer = document.querySelector(".stars-container");
  const stars = document.querySelectorAll(".fa-star");
  const ratingValue = document.querySelector(".rating-value");
  let selectedRating = 0;

  starsContainer.addEventListener("mouseover", (e) => {
    if (e.target.classList.contains("fa-star")) {
      const hoverValue = parseInt(e.target.getAttribute("data-value"));
      highlightStars(hoverValue);
    }
  });

  starsContainer.addEventListener("mouseleave", () => {
    resetStars();
  });

  starsContainer.addEventListener("click", (e) => {
    if (e.target.classList.contains("fa-star")) {
      selectedRating = parseInt(e.target.getAttribute("data-value"));
      ratingValue.textContent = selectedRating;
      setActiveStars(selectedRating);
    }
  });

  function highlightStars(value) {
    stars.forEach((star) => {
      const starValue = parseInt(star.getAttribute("data-value"));
      star.classList.toggle("hover", starValue <= value);
    });
  }

  function resetStars() {
    stars.forEach((star) => star.classList.remove("hover"));
    if (selectedRating > 0) {
      setActiveStars(selectedRating);
    }
  }

  function setActiveStars(value) {
    stars.forEach((star) => {
      const starValue = parseInt(star.getAttribute("data-value"));
      star.classList.toggle("active", starValue <= value);
    });
  }
});
