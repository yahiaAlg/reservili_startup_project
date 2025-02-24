document.addEventListener("DOMContentLoaded", function () {
  const starsContainer = document.querySelector(".stars-container");
  const stars = document.querySelectorAll(".fa-star");
  const ratingValue = document.querySelector(".rating-value");
  const listingType = starsContainer.getAttribute("data-listing-type"); // hotel, restaurant, or agency
  const listingId = starsContainer.getAttribute("data-listing-id");
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

  starsContainer.addEventListener("click", async (e) => {
    if (e.target.classList.contains("fa-star")) {
      selectedRating = parseInt(e.target.getAttribute("data-value"));
      ratingValue.textContent = selectedRating;
      setActiveStars(selectedRating);
      
      try {
        const response = await updateRating(selectedRating);
        if (!response.ok) {
          throw new Error('Failed to update rating');
        }
        const data = await response.json();
        // Update the UI with the new average rating if returned
        if (data.average_rating) {
          ratingValue.textContent = Number(data.average_rating).toFixed(1);
        }
      } catch (error) {
        console.error('Error updating rating:', error);
        // Optionally show error message to user
        alert('Failed to update rating. Please try again.');
        // Reset to previous state
        resetStars();
      }
    }
  });

  async function updateRating(rating) {
    // Get CSRF token from cookie
    const csrftoken = getCookie('csrftoken');
    
    // Construct the appropriate endpoint based on listing type
    const endpoints = {
      'hotel': '/listings/api/hotels/',
      'restaurant': '/listings/api/restaurants/',
      'carrentalagency': '/listings/api/car-rental-agencies/'
    };
    
    const endpoint = `${endpoints[listingType]}${listingId}/rate/`;

    return fetch(endpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken,
      },
      body: JSON.stringify({
        rating: rating
      }),
      credentials: 'same-origin' // Required for sending cookies
    });
  }

  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

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