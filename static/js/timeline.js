/**
 * timeline.js — Fetch and render timeline events for drivers/brands
 * Expects a #timeline-container with data-entity-type and data-entity-id.
 */

async function renderTimeline() {
    const container = document.getElementById('timeline-container');
    if (!container) return;

    const entityType = container.dataset.entityType;
    const entityId = container.dataset.entityId;
    if (!entityType || !entityId || entityId === '0') {
        container.innerHTML = '<p class="loading">No timeline available.</p>';
        return;
    }

    try {
        const res = await fetch(`/api/timeline/${entityType}/${entityId}`);
        const events = await res.json();

        if (!events.length) {
            container.innerHTML = '<p class="loading">No timeline events found.</p>';
            return;
        }

        const html = `
      <div class="timeline">
        ${events.map(ev => `
          <div class="timeline-item">
            <div class="timeline-year">${ev.year}</div>
            <div class="timeline-title">${ev.title}</div>
            ${ev.description ? `<div class="timeline-desc">${ev.description}</div>` : ''}
          </div>
        `).join('')}
      </div>`;

        container.innerHTML = html;

        // Stagger animation
        container.querySelectorAll('.timeline-item').forEach((item, i) => {
            item.style.opacity = '0';
            item.style.transform = 'translateY(10px)';
            item.style.transition = `opacity 0.4s ease ${i * 80}ms, transform 0.4s ease ${i * 80}ms`;
            requestAnimationFrame(() => {
                item.style.opacity = '1';
                item.style.transform = 'none';
            });
        });

    } catch {
        container.innerHTML = '<p class="loading">Failed to load timeline.</p>';
    }
}

document.addEventListener('DOMContentLoaded', renderTimeline);
