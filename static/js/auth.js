
// My JavaScript for handling login and registration

// Handle registration form (only if it exists on this page)
const registerForm = document.getElementById('registerForm');
if (registerForm) {
    registerForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const username = document.getElementById('regUsername').value.trim();
        const password = document.getElementById('regPassword').value;
        
        try {
            const response = await fetch('/register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    username: username,
                    password: password
                })
            });
            
            const result = await response.json();
            
            if (result.success) {
                alert(result.message);
                window.location.href = '/login';
            } else {
                alert(result.error || 'Registration failed');
            }
            
        } catch (error) {
            alert('Failed to register. Please try again.');
        }
    });
}

// Handle login form (only if it exists on this page)
const loginForm = document.getElementById('loginForm');
if (loginForm) {
    loginForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const username = document.getElementById('loginUsername').value.trim();
        const password = document.getElementById('loginPassword').value;
        
        try {
            const response = await fetch('/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    username: username,
                    password: password
                })
            });
            
            const result = await response.json();
            
            if (result.success) {
                alert(result.message);
                window.location.href = '/';
            } else {
                alert(result.error || 'Login failed');
            }
            
        } catch (error) {
            alert('Failed to login. Please try again.');
        }
    });
}