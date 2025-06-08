document.addEventListener('DOMContentLoaded', function() {
    // Enhanced price parsing function
    function parsePrice(price) {
        if (!price) return 0;
        
        // Handle Django price objects
        if (typeof price === 'object' && price !== null) {
            price = price.amount || price.original_amount || 0;
        }
        
        // Convert string to number, removing any non-numeric characters except decimal point
        const num = parseFloat(price.toString().replace(/[^0-9.]/g, ''));
        return isNaN(num) ? 0 : num;
    }

    // Cart configuration
    let cart = [];
    const currencySymbol = '₦';
    const cartSidebar = document.querySelector('.cart-sidebar');
    const cartOverlay = document.querySelector('.cart-overlay');
    const cartItemsContainer = document.querySelector('.cart-items');
    const emptyCartMessage = document.querySelector('.empty-cart-message');
    const subtotalAmount = document.querySelector('.subtotal-amount');
    const totalAmount = document.querySelector('.total-amount');
    const checkoutForm = document.getElementById('checkout-form');

    // Add email input to checkout form if it doesn't exist
    if (checkoutForm && !document.getElementById('checkout-email')) {
        const emailInput = document.createElement('input');
        emailInput.type = 'email';
        emailInput.name = 'email';
        emailInput.id = 'checkout-email';
        emailInput.placeholder = 'Your email address';
        emailInput.required = true;
        emailInput.className = 'checkout-email-input';
        checkoutForm.insertBefore(emailInput, checkoutForm.firstChild);
    }

    // Initialize cart from localStorage
    function loadCart() {
        try {
            const savedCart = localStorage.getItem('wallflowerCart');
            if (savedCart) {
                cart = JSON.parse(savedCart);
                // Validate cart items
                cart = cart.filter(item => item && !isNaN(parsePrice(item.price)));
                updateCartUI();
            }
        } catch (e) {
            console.error('Error loading cart:', e);
            cart = [];
        }
    }

    // Save cart to localStorage
    function saveCart() {
        localStorage.setItem('wallflowerCart', JSON.stringify(cart));
    }

    // Add to cart functionality
    document.querySelectorAll('.btn-add-to-cart').forEach(button => {
        button.addEventListener('click', function() {
            const productId = this.getAttribute('data-product');
            const productName = this.getAttribute('data-name');
            const productPrice = parsePrice(this.getAttribute('data-price'));
            const productImage = this.getAttribute('data-image');
            
            addToCart({
                id: productId,
                name: productName,
                price: productPrice,
                image: productImage,
                quantity: 1
            });
            
            updateCartUI();
            openCart();
        });
    });

    // Quick view functionality
    document.querySelectorAll('.quick-view').forEach(button => {
        button.addEventListener('click', function() {
            const productId = this.getAttribute('data-product');
            openQuickView(productId);
        });
    });

    // Cart management functions
    function addToCart(product) {
        if (isNaN(product.price)) {
            console.error('Invalid product price:', product);
            return;
        }
        
        const existingItem = cart.find(item => item.id === product.id);
        if (existingItem) {
            existingItem.quantity += product.quantity;
        } else {
            cart.push(product);
        }
        saveCart();
    }

    function removeFromCart(productId) {
        cart = cart.filter(item => item.id !== productId);
        saveCart();
        updateCartUI();
    }

    function updateCartUI() {
        cartItemsContainer.innerHTML = '';
        
        if (cart.length === 0) {
            emptyCartMessage.style.display = 'block';
            subtotalAmount.textContent = `${currencySymbol}0.00`;
            totalAmount.textContent = `${currencySymbol}0.00`;
            return;
        }
        
        emptyCartMessage.style.display = 'none';
        let subtotal = 0;
        
        cart.forEach(item => {
            const itemTotal = (item.price || 0) * item.quantity;
            subtotal += itemTotal;
            
            const cartItemElement = document.createElement('div');
            cartItemElement.className = 'cart-item';
            cartItemElement.dataset.id = item.id;
            cartItemElement.dataset.name = item.name;
            cartItemElement.dataset.price = item.price;
            cartItemElement.dataset.image = item.image;
            
            cartItemElement.innerHTML = `
                <div class="cart-item-image">
                    <img src="${item.image}" alt="${item.name}">
                </div>
                <div class="cart-item-details">
                    <h4>${item.name}</h4>
                    <div class="cart-item-price">${currencySymbol}${(item.price || 0).toFixed(2)}</div>
                    <div class="cart-item-quantity">
                        <button class="decrease-quantity" data-id="${item.id}">-</button>
                        <input type="number" value="${item.quantity}" min="1" class="quantity-input" data-id="${item.id}">
                        <button class="increase-quantity" data-id="${item.id}">+</button>
                    </div>
                    <button class="remove-item" data-id="${item.id}">Remove</button>
                </div>
            `;
            cartItemsContainer.appendChild(cartItemElement);
        });
        
        subtotalAmount.textContent = `${currencySymbol}${subtotal.toFixed(2)}`;
        totalAmount.textContent = `${currencySymbol}${subtotal.toFixed(2)}`;
        
        // Update hidden cart data for form submission
        if (document.getElementById('cart-data')) {
            document.getElementById('cart-data').value = JSON.stringify(
                cart.map(item => ({
                    id: item.id,
                    price: item.price,
                    quantity: item.quantity
                }))
            );
        }
        
        // Add event listeners for dynamic elements
        addCartEventListeners();
    }

    function addCartEventListeners() {
        document.querySelectorAll('.decrease-quantity').forEach(button => {
            button.addEventListener('click', function() {
                const productId = this.getAttribute('data-id');
                const item = cart.find(item => item.id === productId);
                if (item.quantity > 1) {
                    item.quantity--;
                    saveCart();
                    updateCartUI();
                }
            });
        });
        
        document.querySelectorAll('.increase-quantity').forEach(button => {
            button.addEventListener('click', function() {
                const productId = this.getAttribute('data-id');
                const item = cart.find(item => item.id === productId);
                item.quantity++;
                saveCart();
                updateCartUI();
            });
        });
        
        document.querySelectorAll('.remove-item').forEach(button => {
            button.addEventListener('click', function() {
                const productId = this.getAttribute('data-id');
                removeFromCart(productId);
            });
        });
    }

    // Cart visibility functions
    function openCart() {
        cartSidebar.classList.add('active');
        cartOverlay.classList.add('active');
        document.body.style.overflow = 'hidden';
    }

    function closeCart() {
        cartSidebar.classList.remove('active');
        cartOverlay.classList.remove('active');
        document.body.style.overflow = '';
    }

    // Quick view modal functions
    function openQuickView(productId) {
        const productCard = document.querySelector(`[data-product="${productId}"]`)?.closest('.product-card');
        if (!productCard) return;

        const productName = productCard.querySelector('h3')?.textContent || 'Product';
        const priceElement = productCard.querySelector('.product-price');
        let productPrice = '0.00';
        
        // Handle different price display formats
        if (priceElement) {
            if (priceElement.querySelector('.sale-price')) {
                productPrice = priceElement.querySelector('.sale-price').textContent.replace(currencySymbol, '');
            } else {
                productPrice = priceElement.textContent.replace(currencySymbol, '');
            }
        }
        
        const productImage = productCard.querySelector('img')?.src || '';
        const productDescription = productCard.querySelector('.product-description')?.textContent || '';
        
        const modalContent = document.querySelector('.modal-product-details');
        modalContent.innerHTML = `
            <div class="modal-product-image">
                <img src="${productImage}" alt="${productName}">
            </div>
            <div class="modal-product-info">
                <h2>${productName}</h2>
                <div class="modal-product-price">${currencySymbol}${productPrice}</div>
                <p>${productDescription}</p>
                <div class="modal-add-to-cart">
                    <div class="quantity-selector">
                        <button class="decrease-qty">-</button>
                        <input type="number" value="1" min="1" class="qty-input">
                        <button class="increase-qty">+</button>
                    </div>
                    <button class="btn btn-add-to-cart-modal" 
                            data-id="${productId}" 
                            data-name="${productName}"
                            data-price="${parsePrice(productPrice)}"
                            data-image="${productImage}">
                        Add to Cart
                    </button>
                </div>
            </div>
        `;
        
        // Add modal event listeners
        document.querySelector('.decrease-qty')?.addEventListener('click', function() {
            const input = document.querySelector('.qty-input');
            if (parseInt(input.value) > 1) input.value = parseInt(input.value) - 1;
        });
        
        document.querySelector('.increase-qty')?.addEventListener('click', function() {
            const input = document.querySelector('.qty-input');
            input.value = parseInt(input.value) + 1;
        });
        
        document.querySelector('.btn-add-to-cart-modal')?.addEventListener('click', function() {
            addToCart({
                id: this.getAttribute('data-id'),
                name: this.getAttribute('data-name'),
                price: parsePrice(this.getAttribute('data-price')),
                image: this.getAttribute('data-image'),
                quantity: parseInt(document.querySelector('.qty-input').value) || 1
            });
            updateCartUI();
            closeQuickView();
            openCart();
        });
        
        document.querySelector('.quick-view-modal').classList.add('active');
        document.body.style.overflow = 'hidden';
    }

    function closeQuickView() {
        document.querySelector('.quick-view-modal').classList.remove('active');
        document.body.style.overflow = '';
    }

    // Close cart handlers
    document.querySelector('.close-cart')?.addEventListener('click', closeCart);
    cartOverlay?.addEventListener('click', closeCart);
    document.querySelector('.close-modal')?.addEventListener('click', closeQuickView);

    // Initialize cart
    loadCart();

    // Enhanced Paystack payment handling
    if (checkoutForm) {
        checkoutForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const email = document.getElementById('checkout-email').value;
            if (!email) {
                alert('Please enter your email address');
                return;
            }

            // Disable button during processing
            const submitBtn = document.getElementById('checkout-button');
            submitBtn.disabled = true;
            submitBtn.textContent = 'Processing...';

            try {
                // Send cart data to server for payment initialization
                const response = await fetch(checkoutForm.action, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                    },
                    body: new URLSearchParams({
                        'cart_data': document.getElementById('cart-data').value,
                        'email': email
                    })
                });

                const data = await response.json();
                
                if (data.status && data.data.authorization_url) {
                    // Redirect to Paystack payment page
                    window.location.href = data.data.authorization_url;
                } else {
                    alert('Payment initialization failed: ' + (data.message || 'Unknown error'));
                    submitBtn.disabled = false;
                    submitBtn.textContent = 'Proceed to Checkout';
                }
            } catch (error) {
                console.error('Payment error:', error);
                alert('An error occurred during payment processing');
                submitBtn.disabled = false;
                submitBtn.textContent = 'Proceed to Checkout';
            }
        });
    }

    // Filter form submission
    const filters = ['category', 'price', 'sort'];
    filters.forEach(filterId => {
        document.getElementById(filterId)?.addEventListener('change', function() {
            this.closest('form')?.submit();
        });
    });
});