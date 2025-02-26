let globalListings = []; // Define a global variable to store the listings

// Function to fetch and render listings with filtering
async function fetchListings(url, listingsContainer) {
  try {
    console.log("currently fetching data from the url", url);
    const response = await fetch(url);
    const listings = await response.json();
    globalListings = listings; // Store the listings in the global variable

    // Populate filter options based on fetched data
    populateFilters(listings);

    // Initial filtering
    filterListings(listingsContainer);
  } catch (error) {
    console.error("Error fetching listings:", error);
  }
}

// Function to populate filter options dynamically
function populateFilters(listings) {
  const priceRangeInput = document.getElementById("priceRange");
  const locationFilterSelect = document.getElementById("locationFilter");

  // Set price range attributes
  const prices = listings.map(
    (item) => item.price_per_night || item.price_range || item.price_per_day
  );
  priceRangeInput.value = priceRangeInput.max;
  document.getElementById(
    "priceValue"
  ).textContent = `${priceRangeInput.max} دج`;
}

// Filter listings based on the data URL
function filterListings(listingsContainer) {
  const maxPrice = parseInt(document.getElementById("priceRange").value);
  const priceLabel =
    document.querySelector("#priceRange").parentElement.previousElementSibling;
  const location = document.getElementById("locationFilter").value;
  const rating = document.getElementById("ratingFilter").value;
  priceLabel.textContent = `السعر اليومي (${maxPrice} دج) `;
  const filtered = globalListings.filter((item) => {
    const priceMatch =
      item.price_per_night <= maxPrice ||
      item.price_range <= maxPrice ||
      item.price_per_day <= maxPrice;
    const locationMatch = !location || item.address.includes(location);
    const ratingMatch = !rating || item.rating >= parseFloat(rating);
    return priceMatch && locationMatch && ratingMatch;
  });

  renderListings(filtered, listingsContainer);
}

// Render listings
function renderListings(items, listingsContainer) {
  const isGridView = listingsContainer.classList.contains("grid-view");

  listingsContainer.innerHTML =
    `<div class="${isGridView ? "row row-cols-1 row-cols-md-3" : "row"}">` +
    items
      .map(
        (item) => `
          <div class="${
            isGridView ? "col-12 col-md-6 col-lg-4 col-xl-3" : "col-12"
          }">
            <div class="rental-card">
              <div class="image-container">
                <a href="${item.slug}">
                  <img src="${item.image_url}" class="card-image" alt="${
          item.name
        }">
                </a>
                <button class="favorite-btn">
                  <i class="far fa-heart"></i>
                </button>
              </div>
              <div class="card-content d-flex flex-column justify-content-sm-start align-items-sm-start py-2 px-3">
                <div class="rating">
                  <div class="stars">
                    ${'<i class="fas fa-star"></i>'.repeat(5)}
                  </div>
                  <span class="score">${item.rating}</span>
                  <span class="reviews">(Reviews)</span>
                </div>
                <h3 class="rental-name">${item.name}</h3>
                <div class="location">
                  <i class="fas fa-map-marker-alt"></i>
                  <span class="text-end">${item.address}</span>
                </div>
                <div class="price">
                  ${
                    item.price_per_night ||
                    item.price_range ||
                    item.price_per_day
                  } دج / Night
                </div>
              </div>
            </div>
          </div>
        `
      )
      .join("") +
    `</div>`;

  initializeFavoriteButtons();
}

// Initialize favorite buttons
function initializeFavoriteButtons() {
  document.querySelectorAll(".favorite-btn").forEach((btn) => {
    btn.addEventListener("click", function (e) {
      e.preventDefault();
      const icon = this.querySelector("i");
      icon.classList.toggle("far");
      icon.classList.toggle("fas");
      icon.classList.toggle("text-danger");
    });
  });
}

// Fetch and render listings on page load
document.addEventListener("DOMContentLoaded", () => {
  const listingsContainer = document.getElementById("listingsContainer");
  const url = listingsContainer.dataset.url; // Assuming the URL is set as a data attribute
  fetchListings(url, listingsContainer);

  // Add event listeners for filters
  document
    .getElementById("priceRange")
    .addEventListener("input", () => filterListings(listingsContainer));
  document
    .getElementById("locationFilter")
    .addEventListener("change", () => filterListings(listingsContainer));
  document
    .getElementById("ratingFilter")
    .addEventListener("change", () => filterListings(listingsContainer));

  // Add event listeners for view toggles
  const viewToggles = document.querySelectorAll(".view-toggle button");
  viewToggles.forEach((button) => {
    button.addEventListener("click", () => {
      viewToggles.forEach((btn) => btn.classList.remove("active"));
      button.classList.add("active");
      const view = button.dataset.view;
      listingsContainer.className = view + "-view";
      renderListings(globalListings, listingsContainer);
    });
    // click on the grid veiw button
    const gridBtn = document.querySelector("[data-view='grid']");
    console.log(gridBtn);

    setTimeout(() => {
      console.log(globalListings);
      gridBtn.click();
    }, 500);
  });
});
