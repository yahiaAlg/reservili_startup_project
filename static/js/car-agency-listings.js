// Sample data
const listings = [
  {
    id: 1,
    name: "AUTO DZ LOC",
    location: "KOUBA, ALGER",
    price: 6000,
    rating: 4.0,
    reviews: 120,
    image: "https://picsum.photos/800/500?random=1",
  },
  {
    id: 2,
    name: "LOCATION NUMBER ONE",
    location: "Draria, ALGER",
    price: 35000,
    rating: 4.0,
    reviews: 120,
    image: "https://picsum.photos/800/500?random=2",
  },
  // Add more listings as needed
];

// View switching functionality
const viewToggles = document.querySelectorAll(".view-toggle button");
const listingsContainer = document.getElementById("listingsContainer");

viewToggles.forEach((button) => {
  button.addEventListener("click", () => {
    viewToggles.forEach((btn) => btn.classList.remove("active"));
    button.classList.add("active");
    const view = button.dataset.view;
    listingsContainer.className = view + "-view";
    renderListings(listings);
  });
});

// Filtering functionality
function filterListings() {
  const maxPrice = parseInt(document.getElementById("priceRange").value);
  const location = document.getElementById("locationFilter").value;
  const rating = document.getElementById("ratingFilter").value;

  const filtered = listings.filter((item) => {
    const priceMatch = item.price <= maxPrice;
    const locationMatch = !location || item.location.includes(location);
    const ratingMatch = !rating || item.rating >= parseFloat(rating);
    return priceMatch && locationMatch && ratingMatch;
  });

  renderListings(filtered);
}

// Render listings
function renderListings(items) {
  const isGridView = listingsContainer.classList.contains("grid-view");
  console.log(isGridView);
  listingsContainer.innerHTML =
    `<div class="${isGridView ? "row row-cols-1 row-cols-md-3" : "row"}">` +
    items
      .map(
        (item) => `
                <div class="${
                  isGridView ? "col-12 col-md-6 col-lg-4 col-xl-3" : "col-12"
                }">
                  <div class="rental-card position-relative">
                    <div class="image-container">
                      <a href="./listing-detail-car-agency.html">
                        <img src="${item.image}" class="card-image" alt="${
          item.name
        }">
                      </a>
                    </div>
                      <button class="favorite-btn">
                          <i class="far fa-heart"></i>
                      </button>
                      <div class="card-content">
                          <div class="d-flex flex-column justify-content-sm-start align-items-sm-start py-2 px-3">
                              <div class="flex-column mb-2">
                                  <div class="rating justify-content-sm-start">
                                      <span>${item.rating}</span>
                                      <i class="fas fa-star"></i>
                                      <small class="text-muted">(${
                                        item.reviews
                                      } Reviews)</small>
                                  </div>
                                  <h5 class="mb-0">${item.name}</h5>
                              </div>
                              <p class="location mb-2">
                                  <i class="fas fa-map-marker-alt me-1"></i>
                                  ${item.location}
                              </p>
                              <p class="price-tag mb-0">
                                  ${item.price} دج / يوم
                              </p>
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

// Price range functionality
const priceRange = document.getElementById("priceRange");
const priceValue = document.getElementById("priceValue");
priceRange.addEventListener("input", function () {
  priceValue.textContent = `${this.value} دج`;
  filterListings();
});

// Add event listeners for filters
document
  .getElementById("locationFilter")
  .addEventListener("change", filterListings);
document
  .getElementById("ratingFilter")
  .addEventListener("change", filterListings);

// Initial render
renderListings(listings);
