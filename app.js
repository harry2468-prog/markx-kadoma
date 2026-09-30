// 1. Live Countdown to 10 October 2026 (ISO Universal Format)
const eventDate = new Date("2026-10-10T09:00:00").getTime();

function updateCountdown() {
  const now = new Date().getTime();
  const diff = eventDate - now;

  if (diff > 0) {
    const days = Math.floor(diff / (1000 * 60 * 60 * 24));
    const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const mins = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
    const secs = Math.floor((diff % (1000 * 60)) / 1000);

    const dEl = document.getElementById("days");
    const hEl = document.getElementById("hours");
    const mEl = document.getElementById("mins");
    const sEl = document.getElementById("secs");

    if (dEl) dEl.innerText = String(days).padStart(2, '0');
    if (hEl) hEl.innerText = String(hours).padStart(2, '0');
    if (mEl) mEl.innerText = String(mins).padStart(2, '0');
    if (sEl) sEl.innerText = String(secs).padStart(2, '0');
  }
}
setInterval(updateCountdown, 1000);
updateCountdown();

// 2. Tab Switcher for Zimbabwean Payments
let activePaymentMethod = "EcoCash";

function switchPay(method) {
  const tabs = document.querySelectorAll(".tab-btn");
  tabs.forEach(t => t.classList.remove("active"));
  
  document.getElementById("ecocashBox").classList.add("hidden");
  document.getElementById("innbucksBox").classList.add("hidden");
  document.getElementById("cardBox").classList.add("hidden");
  document.getElementById("cashBox").classList.add("hidden");

  if (method === 'ecocash') {
    document.getElementById("ecocashBox").classList.remove("hidden");
    activePaymentMethod = "EcoCash";
  } else if (method === 'innbucks') {
    document.getElementById("innbucksBox").classList.remove("hidden");
    activePaymentMethod = "InnBucks";
  } else if (method === 'card') {
    document.getElementById("cardBox").classList.remove("hidden");
    activePaymentMethod = "Card / POS";
  } else if (method === 'cash') {
    document.getElementById("cashBox").classList.remove("hidden");
    activePaymentMethod = "Cash at Gate";
  }

  event.target.classList.add("active");
}

// 3. Form Submission & Digital Ticket Generation
document.getElementById("regForm").addEventListener("submit", function(e) {
  e.preventDefault();

  const name = document.getElementById("fullName").value.trim();
  const phone = document.getElementById("phoneNumber").value.trim();
  const city = document.getElementById("originCity").value;
  const car = document.getElementById("vehicleGen").value;
  const plate = document.getElementById("regPlate").value.trim() || "N/A";
  const cat = document.getElementById("category").value;
  const ref = document.getElementById("payRef").value.trim() || "Pending";

  // Generate Unique Pass Number
  const passNum = "MKX-" + Math.floor(100000 + Math.random() * 900000);

  // Populate Modal Ticket
  document.getElementById("passName").innerText = name;
  document.getElementById("passCity").innerText = city;
  document.getElementById("passCar").innerText = car + ` (${plate})`;
  document.getElementById("passCat").innerText = cat;
  document.getElementById("passId").innerText = passNum;

  // Show Ticket Modal (Controlled via inline style)
  document.getElementById("ticketModal").style.setProperty("display", "flex", "important");

  // Pre-configured WhatsApp Message sent to +263 77 921 6474
  const waText = encodeURIComponent(
    `Hi, I would like to register for Mark X edition\n\n` +
    `*TEAM MARK X KADOMA PASS DETAILS:*\n` +
    `-----------------------------------\n` +
    `*Pass ID:* ${passNum}\n` +
    `*Name:* ${name}\n` +
    `*Phone:* ${phone}\n` +
    `*Convoy City:* ${city}\n` +
    `*Vehicle:* ${car} [${plate}]\n` +
    `*Category:* ${cat}\n` +
    `*Payment Mode:* ${activePaymentMethod}\n` +
    `*Payment Ref:* ${ref}\n` +
    `-----------------------------------\n` +
    `Please confirm my registration and convoy entrance!`
  );

  document.getElementById("sendWhatsAppBtn").onclick = function() {
    window.open(`https://wa.me/263779216474?text=${waText}`, "_blank");
  };
});

function closeModal() {
  document.getElementById("ticketModal").style.setProperty("display", "none", "important");
}