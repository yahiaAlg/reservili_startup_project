document.addEventListener("DOMContentLoaded", function () {
  // select the checked radio button and add event listener on change of the radio group
  const radioButtons = document.querySelectorAll('input[name="paymentMethod"]');
  const paymentMethod = document.querySelector("input[name='payment_method']");
  radioButtons.forEach(function (radio) {
    radio.addEventListener("change", function () {
      if (radio.checked) {
        paymentMethod.value = radio.id;
        console.log(paymentMethod.value);
      }
    });
  });

  console.log("The selected payment method is: ", paymentMethod.value);
  document.body.classList.remove("bg-light");
  // Show/hide card details based on payment method selection
  document.querySelectorAll('input[name="payment_method"]').forEach((radio) => {
    radio.addEventListener("change", function () {
      const cardSection = document.querySelector(".card-section");
      if (this.value === "visa" || this.value === "mastercard") {
        cardSection.style.display = "block";
      } else {
        cardSection.style.display = "none";
      }
    });
  });

  // Show/hide card form when using saved card
  const useSavedCardCheckbox = document.querySelector(
    'input[name="use_saved_card"]'
  );
  if (useSavedCardCheckbox) {
    useSavedCardCheckbox.addEventListener("change", function () {
      const cardSection = document.querySelector(".card-section");
      cardSection.style.display = this.checked ? "none" : "block";
    });
  }
  // click on the checked radio button to select it
  paymentMethod.value = document.querySelector(
    "input[type='radio']:checked"
  ).id;
  paymentMethod.value;
  console.log(paymentMethod.value);
});
