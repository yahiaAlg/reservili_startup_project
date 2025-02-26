/*by sharing the the text*/
let content = document.body.querySelector(".status-card").textContent;
const page = content;
console.log(content);
// Initialize components when document is ready
document.addEventListener("DOMContentLoaded", function () {
  // Add event listeners
  document.getElementById("downloadPDF").addEventListener("click", generatePDF);
  document
    .getElementById("shareButton")
    .addEventListener("click", showShareModal);
});

// Generate PDF function
async function generatePDF() {
  const element = document.body.querySelector(".container");
  const buttons = element.querySelectorAll(".action-button");

  // Hide buttons before generating PDF
  buttons.forEach((btn) => (btn.style.display = "none"));

  const options = {
    margin: [10, 10],
    filename: "ticket-000085752257.pdf",
    image: { type: "jpeg", quality: 0.98 },
    html2canvas: {
      scale: 2,
      useCORS: true,
      logging: true,
    },
    jsPDF: {
      unit: "mm",
      format: "a4",
      orientation: "portrait",
    },
  };

  try {
    const pdf = await html2pdf().set(options).from(element).save();
    console.log("PDF generated successfully");
  } catch (error) {
    console.error("Error generating PDF:", error);
  } finally {
    // Show buttons again
    buttons.forEach((btn) => (btn.style.display = "flex"));
  }
}

// Show share modal
function showShareModal() {
  const modal = new bootstrap.Modal(document.getElementById("shareModal"));
  modal.show();
}

// Utility function to create a canvas from an HTML element
async function htmlToCanvas(element) {
  try {
    // Get the computed styles
    const computedStyle = window.getComputedStyle(element);
    const padding = {
      left: parseInt(computedStyle.paddingLeft),
      right: parseInt(computedStyle.paddingRight),
      top: parseInt(computedStyle.paddingTop),
      bottom: parseInt(computedStyle.paddingBottom),
    };

    // Calculate proper dimensions including padding
    const width = element.offsetWidth + padding.left + padding.right;
    const height = element.offsetHeight + padding.top + padding.bottom;

    // Create the PNG with proper dimensions and scale
    const dataUrl = await domtoimage.toPng(element, {
      width: width * 2,
      height: height * 2,
      style: {
        transform: "scale(1)",
        transformOrigin: "top left",
        width: width + "px",
        height: height + "px",
        margin: "0",
        padding: "0",
      },
      quality: 1.0,
      // Ensure we capture the full width
      cacheBust: true,
      imagePlaceholder: undefined,
      // Add some extra space around the element
      bgcolor: "white",
      height: height + 40, // Add extra padding
      width: width + 40, // Add extra padding
    });

    // Create an image from the data URL
    const img = new Image();
    await new Promise((resolve, reject) => {
      img.onload = resolve;
      img.onerror = reject;
      img.src = dataUrl;
    });

    // Create canvas with proper dimensions
    const canvas = document.createElement("canvas");
    const context = canvas.getContext("2d");
    canvas.width = width * 2 + 80; // Add padding and scale
    canvas.height = height * 2 + 80; // Add padding and scale

    // Fill background
    context.fillStyle = "white";
    context.fillRect(0, 0, canvas.width, canvas.height);

    // Draw the image with padding
    context.drawImage(img, 40, 40, width * 2, height * 2);

    return canvas;
  } catch (error) {
    console.error("Error converting HTML to canvas:", error);
    throw error;
  }
}

// Function to get image blob from canvas
async function canvasToBlob(canvas) {
  return new Promise((resolve) => {
    canvas.toBlob(resolve, "image/png", 1.0);
  });
}

// Function to capture the ticket
async function captureTicket() {
  try {
    // Select the ticket container
    const ticketContainer = document.querySelector(".status-card");

    // Temporarily hide the action buttons
    const actionButtons = ticketContainer.querySelectorAll(".action-button");
    actionButtons.forEach((button) => (button.style.display = "none"));

    // Ensure the container is at its natural size
    const originalStyle = ticketContainer.getAttribute("style") || "";
    ticketContainer.style.width = getComputedStyle(ticketContainer).width;
    ticketContainer.style.maxWidth = "none";

    // Capture the element
    const dataUrl = await domtoimage.toPng(ticketContainer, {
      bgcolor: "white",
      quality: 1.0,
      style: {
        margin: "0",
        padding: "2rem",
      },
    });

    // Restore original styles
    ticketContainer.setAttribute("style", originalStyle);
    actionButtons.forEach((button) => (button.style.display = ""));

    // Convert dataUrl to blob
    const response = await fetch(dataUrl);
    const blob = await response.blob();

    return blob;
  } catch (error) {
    console.error("Error capturing ticket:", error);
    throw error;
  }
}

// Function to handle PDF download
async function handleDownload() {
  try {
    const blob = await captureTicket();
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = "ticket-000085752257.png";
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  } catch (error) {
    console.error("Error downloading ticket:", error);
    alert("عذراً، حدث خطأ أثناء تحميل التذكرة. يرجى المحاولة مرة أخرى.");
  }
}

// Function to handle sharing
async function shareTicket(platform) {
  try {
    const blob = await captureTicket();
    const file = new File([blob], "ticket-000085752257.png", {
      type: "image/png",
    });

    switch (platform) {
      case "whatsapp":
        if (navigator.share && navigator.canShare({ files: [file] })) {
          await navigator.share({
            files: [file],
            title: "تذكرة الحجز",
            text: "مرفق تذكرة الحجز الخاصة بك",
          });
        } else {
          window.open(
            `https://wa.me/?text=${encodeURIComponent(
              "مرفق تذكرة الحجز الخاصة بك"
            )}`
          );
        }
        break;

      case "telegram":
        if (navigator.share && navigator.canShare({ files: [file] })) {
          await navigator.share({
            files: [file],
            title: "تذكرة الحجز",
            text: "مرفق تذكرة الحجز الخاصة بك",
          });
        } else {
          window.open(`https://t.me/share/url?url=${encodeURIComponent(page)}`);
        }
        break;

      case "gmail":
        const reader = new FileReader();
        reader.onload = () => {
          const base64Data = reader.result.split(",")[1];
          const mailtoLink = `mailto:?subject=${encodeURIComponent(
            "تذكرة حجز"
          )}&body=${encodeURIComponent(page)}`;
          window.location.href = mailtoLink;
        };
        reader.readAsDataURL(blob);
        break;
    }
  } catch (error) {
    console.error("Error sharing ticket:", error);
    alert("عذراً، فشلت عملية المشاركة. يرجى المحاولة مرة أخرى.");
  }
}

// Event Listeners
document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("downloadPDF").addEventListener("click", generatePDF);
  document.getElementById("shareButton").addEventListener("click", () => {
    const modal = new bootstrap.Modal(document.getElementById("shareModal"));
    modal.show();
  });
});

// Error handling
window.addEventListener("error", (event) => {
  console.error("Global error:", event.error);
  return false;
});
