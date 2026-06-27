const userForm = document.getElementById('userForm');
const userList = document.getElementById('userList');
const API_BASE = '/users';

// Fetch and display users
async function fetchUsers() {
    try {
        const response = await fetch(API_BASE);
        const users = await response.json();
        renderUsers(users);
    } catch (error) {
        console.error('Error fetching users:', error);
    }
}

// Render users to the DOM
function renderUsers(users) {
    userList.innerHTML = '';
    
    if (users.length === 0) {
        userList.innerHTML = '<div class="empty-state">No users found. Add one above!</div>';
        return;
    }

    users.forEach(user => {
        const card = document.createElement('div');
        card.className = 'user-card';
        card.innerHTML = `
            <div class="user-info">
                <h3>${user.name} <span style="font-weight:400; font-size:0.9rem; color:#6b7280;">(Age: ${user.age})</span></h3>
                <p>${user.email}</p>
            </div>
            <button class="delete-btn" onclick="deleteUser(${user.id})">Delete</button>
        `;
        userList.appendChild(card);
    });
}

// Add a new user
userForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const age = parseInt(document.getElementById('age').value);

    try {
        const response = await fetch(API_BASE, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ name, email, age })
        });

        if (response.ok) {
            userForm.reset();
            fetchUsers();
        } else {
            const err = await response.json();
            alert(`Error: ${err.detail || 'Could not add user'}`);
        }
    } catch (error) {
        console.error('Error adding user:', error);
    }
});

// Delete a user
async function deleteUser(id) {
    if (!confirm('Are you sure you want to delete this user?')) return;
    
    try {
        const response = await fetch(`${API_BASE}/${id}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            fetchUsers();
        } else {
            alert('Error deleting user');
        }
    } catch (error) {
        console.error('Error deleting user:', error);
    }
}

// Initial fetch
fetchUsers();
