document.addEventListener("DOMContentLoaded", function () {
  // Tab switching functionality
  const tabButtons = document.querySelectorAll(".tab-button");
  const forms = {
    hotel: document.getElementById("hotelForm"),
    restaurant: document.getElementById("restaurantForm"),
    car: document.getElementById("carForm"),
  };
  tabButtons.forEach((button) => {
    button.addEventListener("click", () => {
      const tab = button.dataset.tab;

      // Update active tab
      tabButtons.forEach((btn) => btn.classList.remove("active"));
      button.classList.add("active");

      // Show corresponding form
      Object.values(forms).forEach((form) => {
        if (form) {
          form.style.display = "none";
        }
      });
      if (forms[tab]) {
        forms[tab].style.display = "block";
      }
    });
  });

  const recentSections = {
    hotel: document.getElementById("hotelsRecent"),
    restaurant: document.getElementById("restaurantsRecent"),
    car: document.getElementById("carsRecent"),
  };

  tabButtons.forEach((button) => {
    button.addEventListener("click", () => {
      const tab = button.dataset.tab;

      // Update active tab
      tabButtons.forEach((btn) => btn.classList.remove("active"));
      button.classList.add("active");

      // Show corresponding recent section
      Object.values(recentSections).forEach((section) => {
        if (section) section.style.display = "none";
      });

      if (recentSections[tab]) recentSections[tab].style.display = "block";
    });
  });
});
