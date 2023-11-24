console.log('It works!!')

// new
// Get Stripe publishable key

fetch('/payment/config/')
.then((result) => { return result.json(); })
.then((data) => {
    // Initialize Stripe.js
    const stripe = Stripe(data.publicKey);
    
    // new
    // Event handler
    document.querySelector("#submitBtn").addEventListener("click", () => {
        //console.log('yeeeeeeee')
        const productPk = document.querySelector("#submitBtn").getAttribute('product-pk');
        //console.log(typeof(productPk));
        // Get Checkout session ID
        fetch(`/payment/create-checkout-session/${productPk}/`)
        .then((result) => { return result.json(); })
        .then((data) => {
            try {
                redirectToCheckout = stripe.redirectToCheckout({sessionId: data.sessionId})
                console.log(data)
                return redirectToCheckout
                
            } catch (error) {
                console.log(data)
            }
            
            // Redirect to Stripe Checkout
            
        })
        .then((res) => {
            console.log(res);
        });
    });
});
