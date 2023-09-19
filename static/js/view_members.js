document.addEventListener("DOMContentLoaded", function () {
    const deleteButtons = document.querySelectorAll(".delete-member");

    deleteButtons.forEach((button) => {
      button.addEventListener("click", function () {
        const memberId = button.getAttribute("data-member-id");

        if (confirm("Are you sure you want to delete this member?")) {
          // Send an AJAX request to delete the member
          fetch(`/delete_member/${memberId}/`, {
            method: "POST",
            headers: {
              "X-CSRFToken": getCookie("csrftoken"),
            },
          })
            .then((response) => response.json())
            .then((data) => {
              if (data.status === "success") {
                // Reload the page after successful deletion
                window.location.reload();
              } else {
                alert(data.message || "Failed to delete the member.");
              }
            })
            .catch((error) => {
              console.error("Error:", error);
              alert("An error occurred while deleting the member.");
            });
        }
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