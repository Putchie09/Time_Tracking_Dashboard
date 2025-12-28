const toggleBtn = document.getElementById("toggle-btn");
const sidebar = document.getElementById("sidebar");
const navbar = document.querySelector(".navbar");
const content = document.getElementById("main-content");

toggleBtn.addEventListener("click", () => {
  sidebar.classList.toggle("collapsed");
  navbar.classList.toggle("collapsed");
  content.classList.toggle("collapsed");
});

// Perfil desplegable
const profileBtn = document.getElementById("profile-btn");
const profileMenu = document.getElementById("profile-menu");

profileBtn.addEventListener("click", () => {
  profileMenu.style.display =
    profileMenu.style.display === "block" ? "none" : "block";
});

document.addEventListener("click", (e) => {
  if (!profileBtn.contains(e.target) && !profileMenu.contains(e.target)) {
    profileMenu.style.display = "none";
  }
});
