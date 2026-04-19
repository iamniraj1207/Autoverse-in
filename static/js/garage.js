/**
 * garage.js — Garage persistence and toast notifications
 */

async function addToGarage(carId) {
    const btn = document.querySelector(`button[onclick*="addToGarage(${carId})"]`);
    const originalText = btn ? btn.innerHTML : 'ACQUIRE ASSET';
    
    if (btn) {
        btn.disabled = true;
        btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> PROCESING...';
    }

    const csrfToken = document.querySelector('meta[name="csrf-token"]')?.content;

    try {
        const response = await fetch('/api/garage/add', {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'X-CSRF-Token': csrfToken
            },
            body: JSON.stringify({ car_id: carId })
        });

        const data = await response.json();

        if (response.ok) {
            if (btn) {
                btn.innerHTML = '✓ ASSET SECURED';
                btn.classList.remove('btn-outline-light');
                btn.classList.add('btn-success');
            }
            showToast('Vehicle added to your garage!', 'success');
        } else {
            throw new Error(data.message || 'Failed to add');
        }
    } catch (error) {
        console.error('Garage Error:', error);
        if (btn) {
            btn.disabled = false;
            btn.innerHTML = originalText;
        }

        if (error.message.toLowerCase().includes('login')) {
            showToast('Please login to save cars.', 'error');
        } else {
            showToast(error.message, 'error');
        }
    }
}

async function removeFromGarage(carId) {
    if (!confirm('Remove this vehicle from your garage?')) return;

    const csrfToken = document.querySelector('meta[name="csrf-token"]')?.content;

    try {
        const response = await fetch('/api/garage/remove', {
            method: 'DELETE',
            headers: { 
                'Content-Type': 'application/json',
                'X-CSRF-Token': csrfToken
            },
            body: JSON.stringify({ car_id: carId })
        });

        if (response.ok) {
            const card = document.querySelector(`.car-card[data-id="${carId}"]`);
            if (card) {
                card.style.opacity = '0';
                card.style.transform = 'scale(0.9)';
                setTimeout(() => card.remove(), 400);
            }
            showToast('Vehicle removed.', 'success');
        } else {
            const data = await response.json();
            showToast(data.message || 'Failed to remove car.', 'error');
        }
    } catch (error) {
        showToast('Failed to remove car.', 'error');
    }
}

/**
 * Toast Notification System
 */
function showToast(message, type = 'success') {
    // Remove existing toast if any
    const existing = document.querySelector('.toast');
    if (existing) existing.remove();

    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;

    const icon = type === 'success' ? '✓' : '✕';
    toast.innerHTML = `<span class="toast-icon">${icon}</span> <span class="toast-msg">${message}</span>`;

    document.body.appendChild(toast);

    // Trigger entrance
    setTimeout(() => toast.classList.add('visible'), 10);

    // Auto-remove
    setTimeout(() => {
        toast.classList.remove('visible');
        setTimeout(() => toast.remove(), 300);
    }, 4000);
}

// Global reveal for the function
window.addToGarage = addToGarage;
window.removeFromGarage = removeFromGarage;
window.showToast = showToast;
