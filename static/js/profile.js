document.addEventListener("DOMContentLoaded", function () {
  setTimeout(() => {
    document.querySelector(".category-tabs a").click();
  }, 200);
  // Add event listeners for the bottom navigation links
  document.querySelectorAll(".category-tabs a").forEach((link) => {
    link.addEventListener("click", (event) => {
      /*make the latest clicked category button with active class and remove it from the previous one */
      const previous = document
        .querySelector(".category-tabs a.active")
        .classList.remove("active");

      /* get the latest clicked element index in the list */
      const latest = Array.prototype.indexOf.call(
        document.querySelectorAll(".category-tabs a"),
        event.target
      );

      /* make the latest clicked category button with active class and hide the sections which have an index other than it in the secitons list  */
      const sections = [...document.querySelectorAll("section")];
      console.log(sections);
      for (let i = 0, len = sections.length; i < len; i++) {
        if (i !== latest) {
          sections[i].style.display = "none";
        } else {
          sections[i].style.display = "block";
        }
      }
      /*make the latest clicked category button with active class*/
      event.target.classList.add("active");
    });
  });
});
