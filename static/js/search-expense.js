jQuery(function () {
  const showNumOfItems = $("#showNumOfItems");
  const mainTable = $("#mainTable");
  const outputTable = $("#resultsTable");
  const outputTableBody = $("#output-table-body");
  const paginationContainer = $(".pagination-container");
  $("#searchClrBtn").hide();
  $("#searchBtn").on("click", function (e) {
    e.preventDefault();
    var searchString = $("#searchField").val();
    if (searchString.trim().length > 0) {
      $("#searchClrBtn").show();
      $.ajax({
        url: "/expense/search-expense",
        type: "POST",
        data: JSON.stringify({ searchText: searchString }),
        success: function (response) {
          var expensesHTML = "";
          $.each(response, function (index, expense) {
            mainTable.hide();
            paginationContainer.hide();
            outputTable.show();
            showNumOfItems.show();
            if (response.length === 0)
              showNumOfItems.html("<p>Showing 0 record</p>");
            else if (response.length === 1)
              showNumOfItems.html("<p>Showing 1 record</p>");
            else
              showNumOfItems.html(`<p>Showing ${response.length} records</p>`);
            expensesHTML += "<tr>";
            expensesHTML += "<td>" + expense.category + "</td>";
            expensesHTML += "<td>" + expense.amount + "</td>";
            expensesHTML += "<td>" + expense.description + "</td>";
            expensesHTML += "<td>" + expense.date + "</td>";
            expensesHTML += `<td class="d-flex flex-row border-0">
                        <a
                          href="update-expense/${expense.id}"
                          class="btn btn-sm btn-dark me-2"
                          ><i class="bi bi-pencil-square"></i
                        ></a>
                        <a
                          href="delete-expense/${expense.id}"
                          class="btn btn-sm btn-danger"
                          ><i class="bi bi-trash3"></i
                        ></a>
                        </td>`;
            expensesHTML += "</tr>";
          });
          outputTableBody.html(expensesHTML);
        },
        error: function (xhr, status, error) {
          console.error("Error:", error);
        },
      });
    }
    $("#searchClrBtn").on("click", function () {
      $("#searchField").val("");
      mainTable.show();
      paginationContainer.show();
      outputTable.hide();
      showNumOfItems.hide();
    });
  });
});
