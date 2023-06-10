const messages = document.getElementById("messages");
const expenseDate = document.getElementById("expenseDate");
const incomeDate = document.getElementById("incomeDate");
var currentPath = window.location.pathname;
var links = document.querySelectorAll(".nav-link");

links.forEach((link) => {
  var href = link.getAttribute("href");
  if (currentPath === href || currentPath.startsWith(href + "/")) {
    link.setAttribute("aria-current", "page");
  }
});
let today = new Date().toJSON().slice(0, 10); 
// Disable future dates
if(incomeDate) incomeDate.setAttribute("max", today);
if(expenseDate) expenseDate.setAttribute("max", today);

if (messages) {
  setTimeout(function () {
    messages.classList.add("d-none");
  }, 3000);
}
