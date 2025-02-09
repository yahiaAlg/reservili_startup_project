document.addEventListener("DOMContentLoaded", function () {
  // Select all heart buttons
  const favoriteButtons = document.querySelectorAll(".favorite-btn");

  favoriteButtons.forEach((button) => {
    button.addEventListener("click", function (event) {
      event.preventDefault(); // Prevent any default behavior

      // Toggle the heart icon
      const icon = this.querySelector("i");
      if (icon.classList.contains("far")) {
        icon.classList.remove("far");
        icon.classList.add("fas");
      } else {
        icon.classList.remove("fas");
        icon.classList.add("far");
      }
    });
  });
});
