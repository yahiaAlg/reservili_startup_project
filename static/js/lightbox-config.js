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

lightbox.option({
  resizeDuration: 200,
  wrapAround: true,
  positionFromTop: 100,
  alwaysShowNavOnTouchDevices: true,
  albumLabel: "صورة %1 من %2",
  fitImagesInViewport: true, // Ensures images fit within the viewport
  maxWidth: window.innerWidth * 0.9, // Responsive max width
  maxHeight: window.innerHeight * 0.8, // Responsive max height
});

// Function to update Lightbox dimensions
function updateLightboxDimensions() {
  const lightboxImage = document.querySelector(".lb-image");
  if (lightboxImage) {
    lightboxImage.classList.add("lightbox-image");
  }
}

// Initialize Lightbox with responsive options
lightbox.option({
  resizeDuration: 200,
  wrapAround: true,
  positionFromTop: 100,
  alwaysShowNavOnTouchDevices: true,
  albumLabel: "صورة %1 من %2",
  fitImagesInViewport: true,
  maxWidth: window.innerWidth * 0.9, // 90% of viewport width
  maxHeight: window.innerHeight * 0.8, // 80% of viewport height
});

// Add custom class to Lightbox images
document.addEventListener("lightbox:show", updateLightboxDimensions);

// Update Lightbox dimensions on window resize
window.addEventListener("resize", function () {
  lightbox.option({
    maxWidth: window.innerWidth * 0.9,
    maxHeight: window.innerHeight * 0.8,
  });
  updateLightboxDimensions();
});

// Add a class to Lightbox images after they're loaded
document.addEventListener("lightbox:show", function (event) {
  const lightboxImage = document.querySelector(".lb-image");
  if (lightboxImage) {
    lightboxImage.classList.add("lightbox-image");
  }
});
