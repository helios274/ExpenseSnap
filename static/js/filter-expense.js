const minAmount = document.getElementById("minAmount");
const maxAmount = document.getElementById("maxAmount");
const startDate = document.getElementById("startDate");
const endDate = document.getElementById("endDate");
const filterBtn = document.getElementById("filterBtn");
const clearBtn = document.getElementById("clearBtn");
const filterForm = document.getElementById("filterForm");
var categories = document.querySelectorAll('input[type="checkbox"]');
var checkedCategories = [];

const mainTable = document.getElementById("mainTable");
const showNumOfItems = document.getElementById("showNumOfItems");
const outputTable = document.getElementById("resultsTable");
const outputTableBody = document.getElementById("output-table-body");
const paginationContainer = document.querySelector(".pagination-container")

// Current date
let currentDate = new Date().toJSON().slice(0, 10); 
startDate.setAttribute("max", currentDate);
endDate.setAttribute("max", currentDate);

outputTable.style.display = "none";
showNumOfItems.style.display = "none";

filterBtn.addEventListener("click", (e) => {
  e.preventDefault();
  if (checkedCategories.length !== 0) checkedCategories = [];
  categories.forEach(function (category) {
    if (category.checked) {
      checkedCategories.push(category.value);
    }
  });
  if (
    checkedCategories.length === 0 &&
    !minAmount.value &&
    !maxAmount.value &&
    !startDate.value &&
    !endDate.value
  ) {
    return;
  }

  if (
    minAmount.value &&
    maxAmount.value &&
    Number(minAmount.value) > Number(maxAmount.value)
  ) {
    console.log("Min amount must be less than max amount");
    return;
  }
  if (startDate.value && endDate.value && startDate.value > endDate.value) {
    console.log("Start date must be less than end date");
    return;
  }
  showNumOfItems.style.display = "block";
  fetch("filter-expense", {
    method: "POST",
    body: JSON.stringify({
      categories: checkedCategories,
      minAmount: minAmount.value,
      maxAmount: maxAmount.value,
      startDate: startDate.value,
      endDate: endDate.value,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      outputTableBody.innerHTML = "";
      mainTable.style.display = "none";
      if (paginationContainer) paginationContainer.style.display = "none";
      outputTable.style.display = "block";
      if (data.length === 0) {
        outputTable.style.display = "none";
        showNumOfItems.innerHTML = `<p>${"Showing 0 record"}</p>`;
      } else {
        if (data.length === 1) {
          showNumOfItems.innerHTML = `<p>${"Showing 1 record"}</p>`;
        } else {
          showNumOfItems.innerHTML = `<p>${
            "Showing " + data.length + " records"
          }</p>`;
        }
        data.forEach((item) => {
          outputTableBody.innerHTML += `
          <tr>
          <td>${item.category}</td>
          <td>${item.amount}</td>
          <td>${item.description}</td>
          <td>${item.date}</td>
          <td class="d-flex flex-row border-0">
          <a
          href="update-expense/${item.id}"
          class="btn btn-sm btn-dark me-2"
          ><i class="bi bi-pencil-square"></i></a>
          <a
            href="delete-expense/${item.id}"
            class="btn btn-sm btn-danger"
          ><i class="bi bi-trash3"></i></a>
          </td>
          </tr>`;
        });
      }
    });
});

clearBtn.addEventListener("click", (e) => {
  e.preventDefault();
  filterForm.reset();
  outputTable.style.display = "none";
  showNumOfItems.style.display = "none";
  mainTable.style.display = "block";
  paginationContainer.style.display = "block";
});
