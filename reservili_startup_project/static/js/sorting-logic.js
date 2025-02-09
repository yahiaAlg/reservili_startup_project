document.addEventListener("DOMContentLoaded", function () {
  const tabs = [
    ...document.querySelectorAll(":not(.bottom-nav) .nav-link"),
  ].slice(0, 2);
  console.log(tabs);
  const bookingsContainer = document.getElementById("bookings-container");

  // Function to show empty state
  function showEmptyState(filterType) {
    const emptyStateDiv = document.createElement("div");
    emptyStateDiv.className = "text-center py-5";
    emptyStateDiv.id = "empty-state";
    emptyStateDiv.innerHTML = `
            <p class="text-muted">لا توجد حجوزات ${
              filterType === "upcoming" ? "قادمة" : "قديمة"
            }</p>
        `;
    bookingsContainer.appendChild(emptyStateDiv);
  }

  // Function to handle filtering
  function filterBookings(filterType) {
    const bookings = document.querySelectorAll(".booking-card");
    let visibleCount = 0;

    // Remove any existing empty state
    const existingEmptyState = document.getElementById("empty-state");
    if (existingEmptyState) {
      existingEmptyState.remove();
    }

    bookings.forEach((booking) => {
      if (booking.dataset.type === filterType) {
        booking.style.display = "block";
        visibleCount++;
      } else {
        booking.style.display = "none";
      }
    });

    // Show empty state if no bookings are visible
    if (visibleCount === 0) {
      showEmptyState(filterType);
    }
  }

  // Add click handlers to tabs
  tabs.forEach((tab) => {
    tab.addEventListener("click", function (e) {
      e.preventDefault();

      // Update active state of tabs
      tabs.forEach((t) => {
        t.classList.remove("active");
        t.style.color = "#999";
      });

      this.classList.add("active");
      this.style.color = "#00bcd4";

      // Filter bookings
      const filterType = this.dataset.filter;
      filterBookings(filterType);
    });
  });

  // Initialize with upcoming bookings
  filterBookings("upcoming");
});
