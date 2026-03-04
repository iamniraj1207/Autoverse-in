const CompareSystem = {
  maxCars: 4,
  selected: [],

  init() {
    this.selected = JSON.parse(localStorage.getItem('av_compare') || '[]');
    this.updateBar();
  },

  add(carId, carName, brand, hp, acc, imageUrl) {
    if (this.selected.length >= this.maxCars) {
      this.showMessage(`Maximum ${this.maxCars} cars allowed.`);
      return false;
    }
    if (this.selected.find(c => c.id === carId)) {
      this.showMessage(`${carName} is already selected.`);
      return false;
    }
    this.selected.push({ id: carId, name: carName, brand, hp, acc, image: imageUrl });
    this.save();
    this.updateBar();
    this.showMessage(`${carName} added to comparison.`);
    return true;
  },

  remove(carId) {
    this.selected = this.selected.filter(c => c.id !== carId);
    this.save();
    this.updateBar();
  },

  clear() {
    this.selected = [];
    this.save();
    this.updateBar();
  },

  save() {
    localStorage.setItem('av_compare', JSON.stringify(this.selected));
  },

  updateBar() {
    const bar = document.getElementById('compare-bar');
    const slots = document.getElementById('compare-slots');
    const count = document.getElementById('compare-count');
    const goBtn = document.getElementById('compare-go-btn');

    if (!bar) return;

    if (this.selected.length === 0) {
      bar.classList.remove('visible');
      return;
    }

    bar.classList.add('visible');
    count.textContent = `${this.selected.length}/4 cars selected`;
    goBtn.disabled = this.selected.length < 2;

    if (slots) {
      let html = this.selected.map(car => `
        <div class="compare-slot">
          <img src="${car.image}" onerror="this.src='/static/img/car_placeholder.svg'" alt="${car.name}"/>
          <span class="cs-name">${car.brand}</span>
          <button onclick="CompareSystem.remove(${car.id})" class="cs-remove">×</button>
        </div>
      `).join('');

      const empty = this.maxCars - this.selected.length;
      for (let i = 0; i < empty; i++) {
        html += `<div class="compare-slot compare-slot-empty"><span>+ ADD CAR</span></div>`;
      }
      slots.innerHTML = html;
    }
  },

  goTo() {
    if (this.selected.length < 2) return;
    const ids = this.selected.map(c => c.id).join(',');
    window.location.href = `/compare?ids=${ids}`;
  },

  showMessage(msg) {
    const existing = document.querySelector('.compare-toast');
    if (existing) existing.remove();

    const toast = document.createElement('div');
    toast.className = 'compare-toast';
    toast.textContent = msg;
    document.body.appendChild(toast);

    requestAnimationFrame(() => toast.classList.add('show'));
    setTimeout(() => {
      toast.classList.remove('show');
      setTimeout(() => toast.remove(), 300);
    }, 2500);
  }
};

function addToCompare(id, name, brand, hp, acc, imageUrl) {
  CompareSystem.add(id, name, brand, hp, acc, imageUrl);
}

function removeFromCompare(id) {
  CompareSystem.remove(id);
  // If on compare page, refresh
  if (window.location.pathname === '/compare') {
    const ids = CompareSystem.selected.map(c => c.id).join(',');
    if (ids) window.location.href = `/compare?ids=${ids}`;
    else window.location.href = '/cars';
  }
}

function goToCompare() { CompareSystem.goTo(); }
function clearCompare() { CompareSystem.clear(); }

document.addEventListener('DOMContentLoaded', () => CompareSystem.init());
