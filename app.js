// 1. Live Countdown to 10 October 2026
const eventDate = new Date("October 10, 2026 09:00:00").getTime();

function updateCountdown() {
  const now = new Date().getTime();
  const diff = eventDate - now;

  if (diff > 0) {
    const days = Math.floor(diff / (1000 * 60 * 60 * 24));
    const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const mins = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
    const secs = Math.floor((diff % (1000 * 60)) / 1000);

    document.getElementById("days").innerText = String(days).padStart(2, '0');
    document.getElementById("hours").innerText = String(hours).padStart(2, '0');
    document.getElementById("mins").innerText = String(mins).padStart(2, '0');
    document.getElementById("secs").innerText = String(secs).padStart(2, '0');
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

  // Show Ticket Modal
  document.getElementById("ticketModal").classList.remove("hidden");

  // Pre-configure WhatsApp Redirect Message to Craig Motors (0790 187 400)
  const waText = encodeURIComponent(
    `*TEAM MARK X KADOMA REGISTRATION*\n` +
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
    `Please confirm my spot for the convoy & gate entrance!`
  );

  document.getElementById("sendWhatsAppBtn").onclick = function() {
    window.open(`https://wa.me/263790187400?text=${waText}`, "_blank");
  };
});

function closeModal() {
  document.getElementById("ticketModal").classList.add("hidden");
}