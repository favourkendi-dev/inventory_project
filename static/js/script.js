// script.js - My JavaScript for Inventory Management System

let allItems = [];

window.onload = function() {
    loadInventory();
};

// Load all items from backend
async function loadInventory() {
    try {
        const response = await fetch('/items');
        const data = await response.json();
        
        allItems = data.items || [];
        updateDashboard(allItems);
        displayItems(allItems);
    } catch (error) {
        console.error("Error loading inventory:", error);
        document.getElementById('inventory-list').innerHTML = 
            '<p class="text-red-500 text-center py-8">Failed to load inventory.</p>';
    }
}

// Update dashboard stats
function updateDashboard(items) {
    const totalItems = items.length;
    let totalValue = 0;
    let lowStockCount = 0;

    items.forEach(item => {
        totalValue += (item.quantity * item.price);
        if (item.quantity < 5) {
            lowStockCount++;
        }
    });

    document.getElementById('total-items').textContent = totalItems;
    document.getElementById('total-value').textContent = 'Ksh ' + totalValue.toFixed(2);
    document.getElementById('low-stock').textContent = lowStockCount;
}

// Display items in table
function displayItems(items) {
    const container = document.getElementById('inventory-list');
    
    if (items.length === 0) {
        container.innerHTML = `
            <p class="text-gray-500 text-center py-12">
                No items in inventory yet. Add some above!
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

// Filter items based on local search
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

// Add new item
document.getElementById('addForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const name = document.getElementById('name').value.trim();
    const quantity = parseInt(document.getElementById('quantity').value) || 1;
    const price = parseFloat(document.getElementById('price').value) || 0;

    if (!name) {
        alert("Item name is required!");
        return;
    }

    try {
        const response = await fetch('/items', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                name: name,
                quantity: quantity,
                price: price
            })
        });

        const result = await response.json();
        
        if (response.ok) {
            alert(result.message || "Item added successfully!");
            document.getElementById('addForm').reset();
            loadInventory();
        } else {
            alert(result.error || "Failed to add item.");
        }
    } catch (error) {
        alert("Failed to add item. Please check if server is running.");
    }
});

// Search OpenFoodFacts
document.getElementById('searchForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const query = document.getElementById('searchQuery').value.trim();
    const resultDiv = document.getElementById('searchResult');
    
    if (!query) {
        resultDiv.innerHTML = '<p class="text-red-600 p-4">Please enter a search term.</p>';
        return;
    }

    resultDiv.innerHTML = `
        <div class="flex items-center justify-center py-8">
            <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-green-600"></div>
            <span class="ml-3 text-gray-500">Searching...</span>
        </div>
    `;

    try {
        const response = await fetch(`/search?q=${encodeURIComponent(query)}`);
        const data = await response.json();

        if (data.success) {
            resultDiv.innerHTML = `
                <div class="bg-green-50 p-5 rounded-2xl border border-green-100">
                    <p class="font-medium text-green-800">Found: ${data.product.name}</p>
                    <p class="text-sm text-gray-600 mt-1">Brand: ${data.product.brand || 'N/A'}</p>
                    <button onclick="addFromExternal('${data.product.barcode || query}')" 
                            class="mt-4 bg-green-600 hover:bg-green-700 text-white px-6 py-2.5 rounded-xl text-sm font-medium transition">
                        Add to My Inventory
                    </button>
                </div>
            `;
        } else {
            resultDiv.innerHTML = `
                <div class="bg-red-50 p-4 rounded-xl border border-red-100">
                    <p class="text-red-600">${data.error || 'Product not found'}</p>
                    <p class="text-sm text-gray-500 mt-2">Try searching with a different name or barcode.</p>
                </div>
            `;
        }
    } catch (error) {
        resultDiv.innerHTML = `
            <div class="bg-red-50 p-4 rounded-xl border border-red-100">
                <p class="text-red-600">Could not connect to search service.</p>
            </div>
        `;
    }
});

// Add from external search result
async function addFromExternal(barcode) {
    try {
        const response = await fetch('/items/from-external', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ barcode: barcode, quantity: 1 })
        });
        
        const result = await response.json();
        
        if (response.ok) {
            alert(result.message);
            loadInventory();
            document.getElementById('searchResult').innerHTML = '';
        } else {
            alert(result.error || "Failed to add item.");
        }
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
        
        if (response.ok) {
            alert(result.message);
            loadInventory();
        } else {
            alert(result.error || "Failed to delete item.");
        }
    } catch (error) {
        alert("Failed to delete item.");
    }
}

// Local search event listener
document.getElementById('localSearch').addEventListener('input', filterItems);