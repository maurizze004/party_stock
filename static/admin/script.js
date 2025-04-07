// Select the <tbody> element where products will be rendered
const productTableBody = document.getElementById('product-table');
// Function to fetch product data from the API and display it in the table
async function fetchProducts() {
    try {
        // Fetch data from your backend API (adjust the endpoint as required)
        const response = await fetch('/drinks/get_all');

        // Check if the response is successful
        if (!response.ok) {
            throw new Error(`Error fetching products! Status: ${response.status}`);
        }

        // Convert the JSON response to JavaScript array
        const products = await response.json();

        // Render the product data in the table
        renderProductTable(products);
    } catch (error) {
        console.error('Error:', error);
    }
}
// Function to render the table dynamically based on the fetched product data
function renderProductTable(products) {
    // Clear the table body before appending new rows
    productTableBody.innerHTML = '';

    // Loop through the array of products and append rows to the table
    products.forEach((product) => {
        const row = document.createElement('tr');

        // Create table rows dynamically with product data
        row.innerHTML = `
            <td>${product.id}</td>
            <td>${product.name}</td>
            <td>&euro;&nbsp;${product.price.toFixed(2)}</td>
            <td>${product.amount_sold}&nbsp;Fl.</td>
        `;

        // Append the row to the table body
        productTableBody.appendChild(row);
    });
}


// Add
async function addProduct(event) {
    event.preventDefault(); // Prevent the form from reloading the page

    // Select the input fields
    const name = document.getElementById('add-name').value.trim();
    const price = parseFloat(document.getElementById('add-price').value);
    const amountSold = parseInt(document.getElementById('add-amount-sold').value);

    // Validate the input data
    if (!name || isNaN(price) || isNaN(amountSold) || price <= 0 || amountSold < 0) {
        alert('Please fill all fields correctly (price must be positive, amount sold cannot be negative).');
        return;
    }

    try {
        // Send the product data to the server
        const response = await fetch('/drinks/create', {
            method: 'POST', // HTTP method for adding a new resource
            headers: {
                'Content-Type': 'application/json', // Specify JSON format
            },
            body: JSON.stringify({
                name: name,
                price: price,
                amount_sold: amountSold,
            }), // Convert the product data to JSON
        });

        if (!response.ok) {
            throw new Error(`Failed to add product. HTTP status: ${response.status}`);
        }

        const newProduct = await response.json(); // Get the response data if needed

        // Display success message
        alert('Product added successfully!');

        // Reset the form fields
        document.getElementById('add-form').reset();

        // Optionally close the modal
        const addModal = bootstrap.Modal.getInstance(document.getElementById('addModal'));
        if (addModal) {
            addModal.hide();
        }

        // Refresh the product table
        fetchProducts(); // Fetch and re-render the updated product table
    } catch (error) {
        console.error('Error adding product:', error);
        alert('An error occurred while adding the product. Please try again.');
    }
}
// Delete
async function deleteProduct(event) {
    event.preventDefault(); // Prevent the form from submitting normally

    // Get the product ID from the Delete modal
    const productId = document.getElementById('delete-id').value.trim();

    // Check if a product ID is provided
    if (!productId) {
        alert('Please provide a valid product ID.');
        return;
    }

    try {
        // Send DELETE request to the backend API
        const response = await fetch(`/drinks/delete/${productId}`, {
            method: 'DELETE', // Specify HTTP DELETE method
        });

        if (!response.ok) {
            throw new Error(`Failed to delete product. HTTP status: ${response.status}`);
        }

        // Display success message
        alert('Product deleted successfully!');

        // Close the modal using Bootstrap's modal instance
        const deleteModal = bootstrap.Modal.getInstance(document.getElementById('deleteModal'));
        if (deleteModal) {
            deleteModal.hide();
        }

        // Refresh the product table
        fetchProducts(); // Fetch updated product list
    } catch (error) {
        console.error('Error deleting product:', error);
        alert('An error occurred while deleting the product. Please try again.');
    }
}
// Modify
async function modifyProduct(event) {
    event.preventDefault(); // Prevent the form from submitting normally

    // Retrieve the input values from the Modify modal fields
    const productId = document.getElementById('modify-id').value.trim();
    const name = document.getElementById('modify-name').value.trim();
    const price = parseFloat(document.getElementById('modify-price').value);
    const amountSold = parseInt(document.getElementById('modify-amount-sold').value);

    // Validate the input data
    if (!productId || !name || isNaN(price) || isNaN(amountSold) || price <= 0 || amountSold < 0) {
        alert('Please fill out all fields correctly (price must be positive, amount sold cannot be negative).');
        return;
    }

    try {
        // Send the updated product data to the backend API
        const response = await fetch(`/drinks/modify/${productId}`, {
            method: 'PUT', // Or 'PATCH' if your API supports partial updates
            headers: {
                'Content-Type': 'application/json', // Specify JSON format
            },
            body: JSON.stringify({
                name: name,
                price: price,
                amount_sold: amountSold,
            }), // Convert the updated product details to JSON
        });

        if (!response.ok) {
            throw new Error(`Failed to modify product. HTTP status: ${response.status}`);
        }

        // Display success message
        alert('Product modified successfully!');

        // Optionally close the modal
        const modifyModal = bootstrap.Modal.getInstance(document.getElementById('modifyModal'));
        if (modifyModal) {
            modifyModal.hide();
        }

        // Refresh the product table with updated data
        fetchProducts();
    } catch (error) {
        console.error('Error modifying product:', error);
        alert('An error occurred while modifying the product. Please try again.');
    }
}



// Handling the button
document.getElementById('add_product').addEventListener('click', addProduct);
document.getElementById('del_product').addEventListener('click', deleteProduct);
document.getElementById('mod_product').addEventListener('click', modifyProduct)

// Fetch and Display Products when screen loaded
// Reset Modals
document.addEventListener('DOMContentLoaded', () => {
    fetchProducts();

    // Setup event listeners for dynamically clicking "Modify" and "Delete" buttons
    document.querySelector('.btn-success[data-bs-target="#addModal"]').addEventListener('click', () => {
        // Reset the Add Product form when opening the modal
        document.getElementById('add-form').reset();
    });

    document.querySelector('.btn-warning[data-bs-target="#modifyModal"]').addEventListener('click', () => {
        document.getElementById('modify-form').reset();
    });

    document.querySelector('.btn-danger[data-bs-target="#deleteModal"]').addEventListener('click', () => {
        document.getElementById('delete-form').reset();
    });
});