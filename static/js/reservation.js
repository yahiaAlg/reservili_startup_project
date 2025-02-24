// Handle checkbox and quantity inputs for restaurant menu items
document.addEventListener("DOMContentLoaded", function () {
  const checkboxesInputs = document.querySelectorAll(".form-check-input");
  checkboxesInputs.forEach((checkbox) => {
    checkbox.addEventListener("change", function () {
      const quantityInput = this.closest(".form-check").querySelector(
        'input[type="number"]'
      );
      if (quantityInput) {
        quantityInput.disabled = !this.checked;
        if (!this.checked) {
          quantityInput.value = "";
        }
      }
    });
  });

  // Select all checkboxes within form-check containers
  const checkboxes = document.querySelectorAll(
    '.form-check input[type="checkbox"]'
  );
  const formChecks = document.querySelectorAll(".form-check");
  // adding a form-switch class to each form-check
  formChecks.forEach((formCheck) => {
    formCheck.classList.add("form-switch");
    formCheck.classList.add("mb-2");
  });

  // adding a gap between form-checks

  // Generic toggle function
  function toggleCheckboxClasses(checkbox) {
    const container = checkbox.closest(".form-check");
    const label = checkbox.nextElementSibling;

    if (checkbox.checked) {
      container.classList.add("active", "checked");
      label.classList.add("active", "text-primary");
    } else {
      container.classList.remove("active", "checked");
      label.classList.remove("active", "text-primary");
    }
  }

  // Initialize all checkboxes
  checkboxes.forEach((checkbox) => {
    // Set initial state
    checkbox.classList.remove("form-control");
    checkbox.classList.add("form-check-input");
    toggleCheckboxClasses(checkbox);

    // Add event listeners
    checkbox.addEventListener("change", () => {
      toggleCheckboxClasses(checkbox);
    });

    // Optional: Add animation end listener
    checkbox.addEventListener("transitionend", () => {
      // Handle post-animation effects if needed
    });
  });
});
