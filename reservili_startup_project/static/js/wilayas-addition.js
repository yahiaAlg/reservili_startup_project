document.addEventListener("DOMContentLoaded", function () {
  // Array of all Algerian wilayas in Arabic
  const wilayas = [
    "أدرار",
    "الشلف",
    "الأغواط",
    "أم البواقي",
    "باتنة",
    "بجاية",
    "بسكرة",
    "بشار",
    "بليدة",
    "بويرة",
    "تمنراست",
    "تبسة",
    "تلمسان",
    "تيارت",
    "تيزي وزو",
    "الجزائر",
    "الجلفة",
    "جيجل",
    "سطيف",
    "سعيدة",
    "سكيكدة",
    "سيدي بلعباس",
    "عنابة",
    "قالمة",
    "قسنطينة",
    "المدية",
    "مستغانم",
    "المسيلة",
    "معسكر",
    "ورقلة",
    "وهران",
    "البيض",
    "إليزي",
    "برج بوعريريج",
    "بومرداس",
    "الطارف",
    "تندوف",
    "تسمسيلت",
    "الوادي",
    "خنشلة",
    "سوق أهراس",
    "تيبازة",
    "ميلة",
    "عين الدفلى",
    "نأامة",
    "عين تموشنت",
    "غرداية",
    "غليزان",
  ];

  // Find all select elements with the class .wilayas-choices
  document.querySelectorAll(".wilayas-choices").forEach(function (select) {
    // Optionally, clear any existing options
    select.innerHTML = "";

    // Optionally add a default placeholder option
    var defaultOption = document.createElement("option");
    defaultOption.textContent = "اختر ولاية";
    defaultOption.value = "";
    defaultOption.disabled = true;
    defaultOption.selected = true;
    select.appendChild(defaultOption);

    // Append an option for each wilaya in the array
    wilayas.forEach(function (wilaya) {
      var option = document.createElement("option");
      option.value = wilaya;
      option.textContent = wilaya;
      select.appendChild(option);
    });
  });
});
