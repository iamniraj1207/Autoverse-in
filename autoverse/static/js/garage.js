/**
 * garage.js — Garage persistence and toast notifications
 */

async function addToGarage(carId) {
    const btn = document.querySelector(`[data-car-id="${carId}"]`);
    if (!btn) return;

    const originalText = btn.innerHTML;
    btn.disabled = true;
    btn.innerHTML = '<span class="spinner"></span> Adding...';

    try {
        const response = await fetch('/api/garage/add', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ car_id: carId })
        });

        const data = await response.json();

        if (response.ok) {
            btn.innerHTML = '✓ In Garage';
            btn.classList.remove('btn-outline');
            btn.classList.add('btn-success');
            showToast('Vehicle added to your garage!', 'success');
        } else {
            throw new Error(data.error || 'Failed to add');
        }
    } catch (error) {
        console.error('Garage Error:', error);
        btn.disabled = false;
        btn.innerHTML = originalText;

        if (error.message.includes('login')) {
            showToast('Please login to save cars.', 'error');
        } else {
            showToast(error.message, 'error');
        }
    }
}

async function removeFromGarage(carId) {
    if (!confirm('Remove this vehicle from your garage?')) return;

    try {
        const response = await fetch('/api/garage/remove', {
            method: 'DELETE',
            headers: { 'Content-Type': 'application/json' },
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
