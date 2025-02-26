// Restaurant listings data
const listings = [
  {
    id: 1,
    name: "Arabesque Alger",
    location: "Bd Mouloud BEL HOUCHETE, Sidi M'Hamed 16000",
    price: 1200,
    priceUnit: "ابتداءا من",
    rating: 4.0,
    reviews: 120,
    image: "https://picsum.photos/800/500?random=5",
  },
  {
    id: 2,
    name: "Le Gibier d'Algérie",
    location: "riad el feth, Bois des Arcades, Local 02, El Madania 16015",
    price: 1400,
    priceUnit: "ابتداءا من",
    rating: 4.0,
    reviews: 120,
    image: "https://picsum.photos/800/500?random=6",
  },
  {
    id: 3,
    name: "Frais Maison",
    location: "El Biar",
    price: 1000,
    priceUnit: "ابتداءا من",
    rating: 4.0,
    reviews: 120,
    image: "https://picsum.photos/800/500?random=7",
  },
  {
    id: 4,
    name: "Mbfood",
    location: "Bd Maache Malek, Bir Mourad Rais 16000",
    price: 1100,
    priceUnit: "ابتداءا من",
    rating: 4.0,
    reviews: 120,
    image: "https://picsum.photos/800/500?random=8",
  },
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
    /* render the listing based on the type*/

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

  listingsContainer.innerHTML =
    `<div class="${isGridView ? "row row-cols-1 row-cols-md-3 " : "row"}">` +
    items
      .map(
        (item) => `
        <div class="${
          isGridView ? "col-12 col-md-6 col-lg-4 col-xl-3" : "col-12"
        }">
            <div class="rental-card">
                <div class="image-container">
                 <a href="./listing-detail-hotel.html">
                    <img src="${item.image}" class="card-image" alt="${
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
                        <span class="reviews">(${item.reviews} Reviews)</span>
                    </div>
                    <h3 class="rental-name">${item.name}</h3>
                    <div class="location">
                        <i class="fas fa-map-marker-alt"></i>
                        <span class="text-end">${item.location}</span>
                    </div>
                    <div class="price">
                        ${item.price} دج <span class="period">/ ${
          item.priceUnit
        }</span>
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
