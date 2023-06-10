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
          url: "/income/search-income",
          type: "POST",
          data: JSON.stringify({ searchText: searchString }),
          success: function (response) {
            var incomesHTML = "";
            $.each(response, function (index, income) {
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
              incomesHTML += "<tr>";
              incomesHTML += "<td>" + income.source + "</td>";
              incomesHTML += "<td>" + income.amount + "</td>";
              incomesHTML += "<td>" + income.description + "</td>";
              incomesHTML += "<td>" + income.date + "</td>";
              incomesHTML += `<td class="d-flex flex-row border-0">
                          <a
                            href="update-income/${income.id}"
                            class="btn btn-sm btn-dark me-2"
                            ><i class="bi bi-pencil-square"></i
                          ></a>
                          <a
                            href="delete-income/${income.id}"
                            class="btn btn-sm btn-danger"
                            ><i class="bi bi-trash3"></i
                          ></a>
                          </td>`;
              incomesHTML += "</tr>";
            });
            outputTableBody.html(incomesHTML);
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
  