document.addEventListener("DOMContentLoaded", function () {
  // Select all heart buttons
  const favoriteButtons = document.querySelectorAll(".favorite-btn");

  favoriteButtons.forEach((button) => {
    button.addEventListener("click", function (event) {
      event.preventDefault(); // Prevent any default behavior

      const listingType = this.getAttribute("data-listing-type");
      const objectId = this.getAttribute("data-object-id");

      fetch(`/listings/toggle/${listingType}/${objectId}/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({}),
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.success) {
            const icon = this.querySelector("i");
            if (data.favorited) {
              // If now favourited, display the solid heart
              icon.classList.remove("fa-regular");
              icon.classList.add("fa-solid");
            } else {
              // If unfavourited, revert to regular heart
              icon.classList.remove("fa-solid");
              icon.classList.add("fa-regular");
            }
          }
        })
        .catch((error) => console.error("Error toggling favorite:", error));
    });
  });
});

// Helper function to retrieve the CSRF token from cookies
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let cookie of cookies) {
      cookie = cookie.trim();
      if (cookie.startsWith(name + "=")) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
