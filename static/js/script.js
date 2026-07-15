// script.js
// My JavaScript for the Inventory Management System

// Store all items for filtering
let allItems = [];

// Load inventory when the page is ready
window.onload = function() {
    loadInventory();
};

// My function to calculate and update dashboard stats
function updateDashboard(items) {
    const totalItems = items.length;
    
    let totalValue = 0;
    items.forEach(item => {
        totalValue += (item.quantity * item.price);
    });
    
    let lowStockCount = 0;
    items.forEach(item => {
        if (item.quantity < 5) {
            lowStockCount++;
        }
    });
    
    document.getElementById('total-items').textContent = totalItems;
    document.getElementById('total-value').textContent = 'Ksh ' + totalValue.toFixed(2);
    document.getElementById('low-stock').textContent = lowStockCount;
}

// My function to display items in the table
function displayItems(items) {
    const container = document.getElementById('inventory-list');
    
    if (items.length === 0) {
        container.innerHTML = `
            <p class="text-gray-500 text-center py-12">
                No items found matching your search.
            </p>`;
        return;
    }

    let html = `
        <table class="w-full">
            <thead>
                <tr class="bg-gray-50 border-b">
                    <th class="px-6 py-4 text-left font-medium">ID</th>
                    <th class="px-6 py-4 text-left font-medium">Name</th>
                    <th class="px-6 py-4 text-left font-medium">Quantity</th>
                    <th class="px-6 py-4 text-left font-medium">Price</th>
                    <th class="px-6 py-4 text-left font-medium">Actions</th>
                </tr>
            </thead>
            <tbody class="divide-y">
    `;

    items.forEach(item => {
        html += `
            <tr>
                <td class="px-6 py-4">${item.id}</td>
                <td class="px-6 py-4 font-medium">${item.name}</td>
                <td class="px-6 py-4">${item.quantity}</td>
                <td class="px-6 py-4">Ksh ${item.price}</td>
                <td class="px-6 py-4">
                    <button onclick="deleteItem(${item.id})" 
                            class="bg-red-600 hover:bg-red-700 text-white px-5 py-1.5 rounded-lg text-sm transition">
                        Delete
                    </button>
                </td>
            </tr>`;
    });

    html += '</tbody></table>';
    container.innerHTML = html;
}

// Load all items from the backend
async function loadInventory() {
    try {
        const response = await fetch('/items');
        const data = await response.json();
        
        // Store items for filtering
        allItems = data.items;
        
        // Update dashboard stats
        updateDashboard(allItems);
        
        // Display all items
        displayItems(allItems);

    } catch (error) {
        console.error("Error loading inventory:", error);
    }
}

// My function to filter items based on search input
function filterItems() {
    const searchTerm = document.getElementById('localSearch').value.toLowerCase().trim();
    
    if (searchTerm === '') {
        displayItems(allItems);
        return;
    }
    
    const filtered = allItems.filter(item => {
        return item.name.toLowerCase().includes(searchTerm);
    });
    
    displayItems(filtered);
}

// Add event listener for local search
document.getElementById('localSearch').addEventListener('input', filterItems);

// Handle adding new item
document.getElementById('addForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const name = document.getElementById('name').value.trim();
    const quantity = document.getElementById('quantity').value || 1;
    const price = document.getElementById('price').value || 0;

    try {
        const response = await fetch('/items', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                name: name,
                quantity: parseInt(quantity),
                price: parseFloat(price)
            })
        });

        const result = await response.json();
        alert(result.message || "Item added successfully!");
        
        document.getElementById('addForm').reset();
        loadInventory();
    } catch (error) {
        alert("Failed to add item. Please check if server is running.");
    }
});

// Search from OpenFoodFacts
document.getElementById('searchForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const query = document.getElementById('searchQuery').value.trim();
    const resultDiv = document.getElementById('searchResult');
    
    if (!query) return;

    try {
        const response = await fetch(`/search?q=${encodeURIComponent(query)}`);
        const data = await response.json();

        if (data.success) {
            resultDiv.innerHTML = `
                <div class="bg-green-50 p-5 rounded-2xl border border-green-100">
                    <p class="font-medium text-green-800">Found: ${data.product.name}</p>
                    <button onclick="addFromExternal('${data.product.barcode || query}')" 
                            class="mt-4 bg-green-600 hover:bg-green-700 text-white px-6 py-2.5 rounded-xl text-sm font-medium transition">
                        Add to My Inventory
                    </button>
                </div>
            `;
        } else {
            resultDiv.innerHTML = `<p class="text-red-600 p-4">${data.error}</p>`;
        }
    } catch (error) {
        resultDiv.innerHTML = `<p class="text-red-600 p-4">Could not connect to search service.</p>`;
    }
});

// Add searched product to inventory
async function addFromExternal(barcode) {
    try {
        const response = await fetch('/items/from-external', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ barcode: barcode, quantity: 1 })
        });
        
        const result = await response.json();
        alert(result.message);
        loadInventory();
        document.getElementById('searchResult').innerHTML = '';
    } catch (error) {
        alert("Failed to add item from external source.");
    }
}

// Delete an item
async function deleteItem(id) {
    if (!confirm("Are you sure you want to delete this item?")) {
        return;
    }
    
    try {
        const response = await fetch(`/items/${id}`, {
            method: 'DELETE'
        });
        
        const result = await response.json();
        alert(result.message);
        loadInventory();
    } catch (error) {
        alert("Failed to delete item.");
    }
}