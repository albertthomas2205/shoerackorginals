jQuery(document).ready(function() {
    var taxRate = 0.05;
    var shippingRate = 15.00;
    var fadeTime = 300;
    // var linePrice = price * quantity;
    /* Assign actions */
    $('.product-quantity').change(function() {
      updateQuantity(this);
    });
   
    // $('.product-removal button').click(function() {
    //   removeItem(this);
    // });
  
    /* Recalculate cart */
    function recalculateCart() {
      var subtotal = 0;
  
      /* Sum up row totals */
      $('.product2').each(function () {
        subtotal += parseFloat($(this).children('.product-price').text());
      });
      console.log(subtotal);
      /* Calculate totals */
      var tax = subtotal * taxRate;
      var shipping = (subtotal > 0 ? shippingRate : 0);
      var total = subtotal + shipping;
      console.log(subtotal);
      /* Update totals display */
      $('.totals-value').addClass('fade-out'); // Add the fade-out class
      $('#cart-subtotal').html(subtotal.toFixed(2));
      $('#cart-tax').html(tax.toFixed(2));
      $('#cart-shipping').html(shipping.toFixed(2));
      $('#cart-total').html(total.toFixed(2));
      if (total == 0) {
        $('.checkout').fadeOut(fadeTime);
      } else {
        $('.checkout').fadeIn(fadeTime);
      }
      $('.totals-value').removeClass('fade-out'); // Remove the fade-out class
    }
  
    /* Update quantity */
    function updateQuantity(quantityInput) {
      var productRow = $(quantityInput).parent().parent().parent()
      var price = parseFloat(productRow.children('.product-price').text());
      var quantity = $(quantityInput).children(0).val()
      var linePrice = price * quantity;
      console.log(linePrice)
  
      /* Update line price display and recalc cart totals */
      productRow.children('.product-line-price').each(function () {
        $(this).addClass('fade-out'); // Add the fade-out class
        $(this).text(linePrice.toFixed(2));
        recalculateCart();
        $(this).removeClass('fade-out'); // Remove the fade-out class
      });
    }
  
    /* Remove item from cart */
    function removeItem(removeButton) {
      var productRow = $(removeButton).parent().parent();
      productRow.slideUp(fadeTime, function() {
        productRow.remove();
        recalculateCart();
      });
    }
  });