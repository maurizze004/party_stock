// Fetch and dynamically generate drink cards
async function fetchDrinks() {
    const response = await fetch('/drinks/get_all'); // Replace with actual API endpoint
    const drinks = await response.json();

    // Drinks container where cards will be added
    const drinksContainer = document.getElementById('drinks-container');

    drinksContainer.innerHTML = ''; // Clear any existing cards
    drinks.forEach(drink => {

        const { name, price, old_price } = drink;
        // Determine the price trend

        const trend = getPriceTrend(price, old_price);
        // Create Drink Card
        const card = `
            <div class="col-md-6 col-lg-4 mb-4">
                <div class="card drink-card border-${trend.color}">
                    <div class="card-body d-flex align-items-center">
                        <!-- Arrow -->
                        <i class="card-icon bi ${trend.icon}" id="trendArrow"></i>
                        <!-- Content -->
                        <div>
                            <h5 class="card-title">${name}</h5>
                            <p class="price">${price.toFixed(2)}&nbsp;&euro;</p>
                        </div>
                    </div>
                </div>
            </div>
        `;
        drinksContainer.insertAdjacentHTML('beforeend', card);
    });

}
// Get price trend (arrow icon & border color)
function getPriceTrend(price, oldPrice) {
    if (price > oldPrice) {
        return { icon: 'bi-arrow-up arrow-up', color: 'danger' }; // Red for price increase
    } else if (price < oldPrice) {
        return { icon: 'bi-arrow-down arrow-down', color: 'success' }; // Green for price decrease
    } else {
        return { icon: 'bi-arrow-right arrow-unchanged', color: 'secondary' }; // Gray for no change
    }

}

// Initialize the page with data
fetchDrinks();