const chartCanvas1 = document.getElementById("chart1");
const canvas2 = document.getElementById("chart2");
const filterForm = document.getElementById("filterForm");
const startDate = document.getElementById("startDate");
const endDate = document.getElementById("endDate");
const filterBtn = document.getElementById("filterBtn");
const clearBtn = document.getElementById("clearBtn");
const expenseNumField = document.getElementById("expenseNumField");
const expenseSumField = document.getElementById("expenseSumField");
const expenseNumFieldFiltered = document.getElementById(
  "expenseNumFieldFiltered"
);
const expenseSumFieldFiltered = document.getElementById(
  "expenseSumFieldFiltered"
);
const barChartFiltered = document.getElementById("barChartFiltered");

function numberFormatter(num) {
  return Number(num).toLocaleString("en-IN", {
    maximumFractionDigits: 2,
    style: "currency",
    currency: "INR",
  });
}

const renderBarChart = (canvas, data, labels) => {
  return new Chart(canvas, {
    type: "bar",
    data: {
      labels: labels,
      datasets: [
        {
          data: data,
          borderWidth: 2,
          backgroundColor: "rgba(90, 212, 90, 0.3)",
          borderColor: "rgba(90, 212, 90, 0.9)",
        },
      ],
    },
    options: {
      plugins: {
        legend: {
          display: false,
        },
      },
      title: {
        display: true,
        text: "Expenses per category",
      },
      responsive: true,
      maintainAspectRatio: false,
      layout: {
        padding: {
          left: 10,
          right: 25,
          top: 15,
          bottom: 0,
        },
      },
      scales: {
        x: {
          grid: {
            display: false,
          },
        },
        y: {
          grid: {
            display: false,
          },
        },
      },
    },
  });
};

const renderLineChart = (canvas, data1, data2, labels) => {
  return new Chart(canvas, {
    type: "line",
    data: {
      labels: labels,
      datasets: [
        {
          data: data1,
          label: "Expense",
          borderWidth: 2,
          backgroundColor: "rgba(13, 163, 5,1.0)",
          borderColor: "rgba(13, 163, 5,0.3)",
        },
        {
          data: data2,
          label: "Income",
          borderWidth: 2,
          backgroundColor: "rgba(0,0,255,1.0)",
          borderColor: "rgba(0,0,255,0.3)",
        },
      ],
    },
    options: {
      title: {
        display: true,
        text: "Income - Expense",
      },
      responsive: true,
      maintainAspectRatio: false,
      layout: {
        padding: {
          left: 10,
          right: 25,
          top: 15,
          bottom: 0,
        },
      },
    },
  });
};

barChartFiltered.style.display = "none";
expenseNumFieldFiltered.style.display = "none";
expenseSumFieldFiltered.style.display = "none";

fetch("stats-data", { method: "GET" })
  .then((res) => res.json())
  .then((data) => {
    expenseNumField.innerHTML = `<span>${data.expense_count}</span>`;
    expenseSumField.innerHTML = `<span>${numberFormatter(
      data.expense_sum
    )}</span>`;

    const totalByCategoryData = [];
    const categoryLabels = Object.keys(data.expense_by_category);
    const values = Object.values(data.expense_by_category);
    values.forEach((item) => {
      totalByCategoryData.push(Number(item));
    });

    const monthlyData = data.monthly_data;
    const lineChartLabels = [];
    const expenseData = [];
    const incomeData = [];
    monthlyData.forEach((element) => {
      lineChartLabels.push(element.month);
      expenseData.push(Number(element.expense));
      incomeData.push(Number(element.income));
    });

    renderBarChart(chartCanvas1, totalByCategoryData, categoryLabels);
    renderLineChart(canvas2, expenseData, incomeData, lineChartLabels);
  });

let barChart;
filterBtn.addEventListener("click", (e) => {
  e.preventDefault();
  if (!startDate.value && !endDate.value) {
    return;
  }
  if (startDate.value && endDate.value && startDate.value > endDate.value) {
    console.log("Start date must be less than end date");
    return;
  }
  fetch("filter-stats", {
    method: "POST",
    body: JSON.stringify({
      startDate: startDate.value,
      endDate: endDate.value,
    }),
  })
    .then((res) => res.json())
    .then((data) => {
      expenseNumField.style.display = "none";
      expenseSumField.style.display = "none";
      expenseNumFieldFiltered.style.display = "block";
      expenseSumFieldFiltered.style.display = "block";
      expenseNumFieldFiltered.innerHTML = `<span>${data.expense_count}</span>`;
      expenseSumFieldFiltered.innerHTML = `<span>${data.expense_sum}</span>`;

      chartCanvas1.style.display = "none";
      barChartFiltered.style.display = "block";
      const totalByCategoryFilteredData = [];
      const categoryLabels = Object.keys(data.expense_by_category);
      const values = Object.values(data.expense_by_category);
      values.forEach((item) => {
        totalByCategoryFilteredData.push(Number(item));
      });
      if (barChart) barChart.destroy();
      barChart = renderBarChart(
        barChartFiltered,
        totalByCategoryFilteredData,
        categoryLabels
      );
    });
});

clearBtn.addEventListener("click", (e) => {
  e.preventDefault();
  filterForm.reset();
  expenseNumField.style.display = "block";
  expenseSumField.style.display = "block";
  expenseNumFieldFiltered.style.display = "none";
  expenseSumFieldFiltered.style.display = "none";
  chartCanvas1.style.display = "block";
  barChartFiltered.style.display = "none";
});
