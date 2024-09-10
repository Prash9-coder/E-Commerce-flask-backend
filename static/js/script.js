document.addEventListener("DOMContentLoaded", () => {
  // Explore button
  document
    .getElementById("explore-btn")
    .addEventListener("click", function (event) {
      event.preventDefault(); // Prevent the default link behavior
      window.location.href = "https://www.flipkart.com/"; // Redirect to Flipkart
    });

  // Function to show product details
  function showCard(img) {
    let newImg = document.getElementById("cartImg");
    newImg.src = img.src;
  }
  
  // Adding event listeners to product images
  document.querySelectorAll(".card img").forEach((img) => {
    img.addEventListener("click", () => showCard(img));
  });


  // Profile photo upload event
  document
    .getElementById("profile-photo-upload")
    .addEventListener("change", function () {
      // You can add your file upload logic here
      this.form.submit(); // This will submit the form automatically after file selection
    });
});

document.addEventListener('DOMContentLoaded', function() {
  const links = document.querySelectorAll('nav ul li a');
  const currentURL = window.location.pathname; // Get the current URL path

  links.forEach(link => {
    if (link.getAttribute('href') === currentURL) {
      link.classList.add('active');
    } else {
      link.classList.remove('active');
    }
  });
});

    document.querySelector('form').addEventListener('submit', function() {
        var productId = document.querySelector('input[name="product_id"]').value;
        console.log('Product ID:', productId);
    });


