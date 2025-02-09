/*by sharing the the text*/
// let styles = document.querySelector("style").outerHTML;
// let content = document.body.querySelector(".container").outerHTML;
// const page = styles + content;
// // Initialize components when document is ready
// document.addEventListener("DOMContentLoaded", function () {
//   // Add event listeners
//   document.getElementById("downloadPDF").addEventListener("click", generatePDF);
//   document
//     .getElementById("shareButton")
//     .addEventListener("click", showShareModal);
// });

// // Generate PDF function
// async function generatePDF() {
//   const element = document.body.querySelector(".container");
//   const buttons = element.querySelectorAll(".action-button");

//   // Hide buttons before generating PDF
//   buttons.forEach((btn) => (btn.style.display = "none"));

//   const options = {
//     margin: [10, 10],
//     filename: "ticket-000085752257.pdf",
//     image: { type: "jpeg", quality: 0.98 },
//     html2canvas: {
//       scale: 2,
//       useCORS: true,
//       logging: true,
//     },
//     jsPDF: {
//       unit: "mm",
//       format: "a4",
//       orientation: "portrait",
//     },
//   };

//   try {
//     const pdf = await html2pdf().set(options).from(element).save();
//     console.log("PDF generated successfully");
//   } catch (error) {
//     console.error("Error generating PDF:", error);
//   } finally {
//     // Show buttons again
//     buttons.forEach((btn) => (btn.style.display = "flex"));
//   }
// }

// // Show share modal
// function showShareModal() {
//   const modal = new bootstrap.Modal(document.getElementById("shareModal"));
//   modal.show();
// }

// // Share ticket function
// function shareTicket(platform) {
//   const ticketNumber = "000085752257";
//   const shareText = `${page}`;
//   const currentUrl = window.location.href;

//   switch (platform) {
//     case "whatsapp":
//       window.open(
//         `https://api.whatsapp.com/send?text=${encodeURIComponent(
//           shareText + "\n" + currentUrl
//         )}`
//       );
//       break;
//     case "telegram":
//       window.open(
//         `https://t.me/share/url?url=${encodeURIComponent(
//           currentUrl
//         )}&text=${encodeURIComponent(`hello there`)}`
//       );
//       break;
//     case "gmail":
//       window.open(
//         `mailto:?subject=${encodeURIComponent(
//           "تذكرة حجز"
//         )}&body=${encodeURIComponent(shareText + "\n\n" + currentUrl)}`
//       );
//       break;
//   }
// }

// // Go back function
// function goBack() {
//   window.history.back();
// }

// // Error handler
// window.onerror = function (msg, url, lineNo, columnNo, error) {
//   console.error(
//     "Error: " +
//       msg +
//       "\nURL: " +
//       url +
//       "\nLine: " +
//       lineNo +
//       "\nColumn: " +
//       columnNo +
//       "\nError object: " +
//       JSON.stringify(error)
//   );
//   return false;
// };

/*by sharing the pdf as an image*/
// let styles = document.querySelector("style").outerHTML;
// let content = document.body.querySelector(".container").outerHTML;

// document.addEventListener("DOMContentLoaded", function () {
//   document.getElementById("downloadPDF").addEventListener("click", generatePDF);
//   document
//     .getElementById("shareButton")
//     .addEventListener("click", showShareModal);
// });

// // Function to generate PDF (for download button)
// async function generatePDF() {
//   const element = document.body.querySelector(".container");
//   const buttons = element.querySelectorAll(".action-button");

//   buttons.forEach((btn) => (btn.style.display = "none"));

//   const options = {
//     margin: [10, 10],
//     filename: "ticket-000085752257.pdf",
//     image: { type: "jpeg", quality: 0.98 },
//     html2canvas: {
//       scale: 2,
//       useCORS: true,
//       logging: true,
//     },
//     jsPDF: {
//       unit: "mm",
//       format: "a4",
//       orientation: "portrait",
//     },
//   };

//   try {
//     await html2pdf().set(options).from(element).save();
//     console.log("PDF generated successfully");
//   } catch (error) {
//     console.error("Error generating PDF:", error);
//   } finally {
//     buttons.forEach((btn) => (btn.style.display = "flex"));
//   }
// }

// // Function to generate image from the container
// async function generateImage() {
//   const element = document.body.querySelector(".container");
//   const buttons = element.querySelectorAll(".action-button");

//   try {
//     // Hide buttons before capturing
//     buttons.forEach((btn) => (btn.style.display = "none"));

//     // Generate canvas
//     const canvas = await html2canvas(element, {
//       scale: 2,
//       logging: false,
//       useCORS: true,
//       allowTaint: true,
//     });

//     // Convert canvas to blob
//     return new Promise((resolve) => {
//       canvas.toBlob(
//         (blob) => {
//           resolve(blob);
//         },
//         "image/jpeg",
//         0.95
//       );
//     });
//   } catch (error) {
//     console.error("Error generating image:", error);
//     return null;
//   } finally {
//     // Show buttons again
//     buttons.forEach((btn) => (btn.style.display = "flex"));
//   }
// }

// function showShareModal() {
//   const modal = new bootstrap.Modal(document.getElementById("shareModal"));
//   modal.show();
// }

// // Modified share ticket function to share image
// async function shareTicket(platform) {
//   const imageBlob = await generateImage();

//   if (!imageBlob) {
//     alert("Error generating image for sharing");
//     return;
//   }

//   const imageFile = new File([imageBlob], "ticket-000085752257.jpg", {
//     type: "image/jpeg",
//   });

//   switch (platform) {
//     case "whatsapp":
//       try {
//         if (navigator.share && navigator.canShare({ files: [imageFile] })) {
//           await navigator.share({
//             files: [imageFile],
//             title: "Ticket",
//             text: "Here is your ticket",
//           });
//         } else {
//           // Fallback for desktop or unsupported browsers
//           const imageUrl = URL.createObjectURL(imageBlob);
//           window.open(
//             `https://api.whatsapp.com/send?text=${encodeURIComponent(
//               "Here is your ticket: " + window.location.href
//             )}`
//           );
//           URL.revokeObjectURL(imageUrl);
//         }
//       } catch (error) {
//         console.error("Error sharing to WhatsApp:", error);
//         alert("Unable to share directly. Please download and share manually.");
//       }
//       break;

//     case "telegram":
//       try {
//         if (navigator.share && navigator.canShare({ files: [imageFile] })) {
//           await navigator.share({
//             files: [imageFile],
//             title: "Ticket",
//             text: "Here is your ticket",
//           });
//         } else {
//           // Fallback for desktop or unsupported browsers
//           const imageUrl = URL.createObjectURL(imageBlob);
//           window.open(
//             `https://t.me/share/url?url=${encodeURIComponent(
//               window.location.href
//             )}`
//           );
//           URL.revokeObjectURL(imageUrl);
//         }
//       } catch (error) {
//         console.error("Error sharing to Telegram:", error);
//         alert("Unable to share directly. Please download and share manually.");
//       }
//       break;

//     case "gmail":
//       try {
//         const reader = new FileReader();
//         reader.onload = function () {
//           const base64Data = reader.result.split(",")[1];
//           const mailtoLink = `mailto:?subject=${encodeURIComponent(
//             "تذكرة حجز"
//           )}&body=${encodeURIComponent(
//             "Please find the ticket attached."
//           )}&attachment=ticket.jpg;base64,${base64Data}`;
//           window.location.href = mailtoLink;
//         };
//         reader.readAsDataURL(imageBlob);
//       } catch (error) {
//         console.error("Error sharing via email:", error);
//         alert(
//           "Error sharing via email. Please try downloading and sharing manually."
//         );
//       }
//       break;
//   }
// }

// function goBack() {
//   window.history.back();
// }

// window.onerror = function (msg, url, lineNo, columnNo, error) {
//   console.error(
//     "Error: " +
//       msg +
//       "\nURL: " +
//       url +
//       "\nLine: " +
//       lineNo +
//       "\nColumn: " +
//       columnNo +
//       "\nError object: " +
//       JSON.stringify(error)
//   );
//   return false;
// };

/* converting the pdf to image */
// let styles = document.querySelector("style").outerHTML;
// let content = document.body.querySelector(".container").outerHTML;

// document.addEventListener("DOMContentLoaded", function () {
//   document.getElementById("downloadPDF").addEventListener("click", generatePDF);
//   document
//     .getElementById("shareButton")
//     .addEventListener("click", showShareModal);
// });

// // Function to generate PDF blob
// async function generatePDFBlob() {
//   const element = document.body.querySelector(".container");
//   const buttons = element.querySelectorAll(".action-button");

//   buttons.forEach((btn) => (btn.style.display = "none"));

//   const options = {
//     margin: [10, 10],
//     filename: "ticket-000085752257.pdf",
//     image: { type: "jpeg", quality: 0.98 },
//     html2canvas: {
//       scale: 2,
//       useCORS: true,
//       logging: true,
//     },
//     jsPDF: {
//       unit: "mm",
//       format: "a4",
//       orientation: "portrait",
//     },
//   };

//   try {
//     const pdfBlob = await html2pdf().set(options).from(element).output("blob");
//     return pdfBlob;
//   } catch (error) {
//     console.error("Error generating PDF:", error);
//     return null;
//   } finally {
//     buttons.forEach((btn) => (btn.style.display = "flex"));
//   }
// }

// // Function to convert PDF to Image
// async function convertPDFtoImage(pdfBlob) {
//   try {
//     // Load the PDF data
//     const pdfUrl = URL.createObjectURL(pdfBlob);
//     const loadingTask = pdfjsLib.getDocument(pdfUrl);
//     const pdf = await loadingTask.promise;

//     // Get the first page
//     const page = await pdf.getPage(1);

//     // Set the scale for better quality
//     const viewport = page.getViewport({ scale: 2.0 });

//     // Prepare canvas
//     const canvas = document.createElement("canvas");
//     const context = canvas.getContext("2d");
//     canvas.height = viewport.height;
//     canvas.width = viewport.width;

//     // Render PDF page to canvas
//     const renderContext = {
//       canvasContext: context,
//       viewport: viewport,
//     };

//     await page.render(renderContext).promise;

//     // Convert canvas to blob
//     return new Promise((resolve) => {
//       canvas.toBlob(
//         (blob) => {
//           URL.revokeObjectURL(pdfUrl);
//           resolve(blob);
//         },
//         "image/jpeg",
//         0.95
//       );
//     });
//   } catch (error) {
//     console.error("Error converting PDF to image:", error);
//     return null;
//   }
// }

// // Function to download PDF
// async function generatePDF() {
//   const pdfBlob = await generatePDFBlob();
//   if (pdfBlob) {
//     const url = URL.createObjectURL(pdfBlob);
//     const link = document.createElement("a");
//     link.href = url;
//     link.download = "ticket-000085752257.pdf";
//     document.body.appendChild(link);
//     link.click();
//     document.body.removeChild(link);
//     URL.revokeObjectURL(url);
//   }
// }

// function showShareModal() {
//   const modal = new bootstrap.Modal(document.getElementById("shareModal"));
//   modal.show();
// }

// // Modified share ticket function
// async function shareTicket(platform) {
//   // First generate PDF
//   const pdfBlob = await generatePDFBlob();
//   if (!pdfBlob) {
//     alert("Error generating ticket");
//     return;
//   }

//   // Convert PDF to image
//   const imageBlob = await convertPDFtoImage(pdfBlob);
//   if (!imageBlob) {
//     alert("Error processing ticket");
//     return;
//   }

//   const imageFile = new File([imageBlob], "ticket-000085752257.jpg", {
//     type: "image/jpeg",
//   });

//   switch (platform) {
//     case "whatsapp":
//       try {
//         if (navigator.share && navigator.canShare({ files: [imageFile] })) {
//           await navigator.share({
//             files: [imageFile],
//             title: "Ticket",
//             text: "Here is your ticket",
//           });
//         } else {
//           const imageUrl = URL.createObjectURL(imageBlob);
//           window.open(
//             `https://api.whatsapp.com/send?text=${encodeURIComponent(
//               "Here is your ticket: " + window.location.href
//             )}`
//           );
//           URL.revokeObjectURL(imageUrl);
//         }
//       } catch (error) {
//         console.error("Error sharing to WhatsApp:", error);
//         alert("Unable to share directly. Please download and share manually.");
//       }
//       break;

//     case "telegram":
//       try {
//         if (navigator.share && navigator.canShare({ files: [imageFile] })) {
//           await navigator.share({
//             files: [imageFile],
//             title: "Ticket",
//             text: "Here is your ticket",
//           });
//         } else {
//           const imageUrl = URL.createObjectURL(imageBlob);
//           window.open(
//             `https://t.me/share/url?url=${encodeURIComponent(
//               window.location.href
//             )}`
//           );
//           URL.revokeObjectURL(imageUrl);
//         }
//       } catch (error) {
//         console.error("Error sharing to Telegram:", error);
//         alert("Unable to share directly. Please download and share manually.");
//       }
//       break;

//     case "gmail":
//       try {
//         const reader = new FileReader();
//         reader.onload = function () {
//           const base64Data = reader.result.split(",")[1];
//           const mailtoLink = `mailto:?subject=${encodeURIComponent(
//             "تذكرة حجز"
//           )}&body=${encodeURIComponent(
//             "Please find the ticket attached."
//           )}&attachment=ticket.jpg;base64,${base64Data}`;
//           window.location.href = mailtoLink;
//         };
//         reader.readAsDataURL(imageBlob);
//       } catch (error) {
//         console.error("Error sharing via email:", error);
//         alert(
//           "Error sharing via email. Please try downloading and sharing manually."
//         );
//       }
//       break;
//   }
// }

// function goBack() {
//   window.history.back();
// }

// window.onerror = function (msg, url, lineNo, columnNo, error) {
//   console.error(
//     "Error: " +
//       msg +
//       "\nURL: " +
//       url +
//       "\nLine: " +
//       lineNo +
//       "\nColumn: " +
//       columnNo +
//       "\nError object: " +
//       JSON.stringify(error)
//   );
//   return false;
// };
