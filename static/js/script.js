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
  document.querySelectorAll(".card img").forEach((img) => {
    img.addEventListener("click", () => showCard(img));
  });
     
  }

  // Function to add items to the cart
  function addToCart(productId) {
    fetch("/cart", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ productId: productId }),
    })
      .then((response) => response.json())
      .then((data) => {
        alert("Product added to cart: " + data.message);
      })
      .catch((error) => {
        console.error("Error adding product to cart:", error);
        alert("Failed to add product to cart. Please try again.");
      });
  }
  
  document.querySelectorAll(".btn-success").forEach((btn) => {
    btn.addEventListener("click", () => {
      const productId = btn.getAttribute("data-product-id");
      if (productId) {
        addToCart(productId);
      } else {
        console.error("No product ID found on button");
      }
    });
  });
  

  // Function to handle Buy Now button
  function buyNow(productId) {
    document.querySelectorAll(".btn-warning").forEach(function (btn) {
      btn.addEventListener("click", function (event) {
        event.preventDefault();
        window.location.href = "payments.html";
      });
    });
  }
  

  // Adding event listeners to product images
  document.querySelectorAll(".card img").forEach((img) => {
    img.addEventListener("click", () => showCard(img));
  });

  // Adding event listeners to "Add to Cart" and "Buy Now" buttons
  document.querySelectorAll(".btn-success").forEach((btn) => {
    btn.addEventListener("click", () =>
      addToCart(btn.getAttribute("data-product-id"))
    );
  });

  document.querySelectorAll(".btn-warning").forEach((btn) => {
    btn.addEventListener("click", () =>
      buyNow(btn.getAttribute("data-product-id"))
    );
  });

  // Profile photo upload event
  document
    .getElementById("profile-photo-upload")
    .addEventListener("change", function () {
      // You can add your file upload logic here
      this.form.submit(); // This will submit the form automatically after file selection
    });
});
