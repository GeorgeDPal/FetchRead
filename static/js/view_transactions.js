document.addEventListener("DOMContentLoaded", function () {
    const filterForm = document.getElementById("filter-form");
    const transactionList = document.getElementById("transaction-list");

    filterForm.addEventListener("submit", function (event) {
      event.preventDefault();

      const formData = new FormData(filterForm);

      fetch("/filter_transactions/", {
        method: "POST",
        body: formData,
        headers: {
          "X-CSRFToken": getCookie("csrftoken"),
        },
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.html) {
            // Update the transaction list with the filtered results
            transactionList.innerHTML = data.html;
          } else {
            alert("Failed to fetch filtered transactions.");
          }
        })
        .catch((error) => {
          console.error("Error:", error);
          alert("An error occurred while fetching filtered transactions.");
        });
    });

    // Function to get the CSRF token from cookies
    function getCookie(name) {
      const cookieValue = document.cookie.match(
        "(^|;)\\s*" + name + "\\s*=\\s*([^;]+)"
      );
      return cookieValue ? cookieValue.pop() : "";
    }
  });