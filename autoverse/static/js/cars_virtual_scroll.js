let page = 0;
const pageSize = 50;
let allCars = [];
let filteredCars = [];

async function loadCars() {
    const res = await fetch('/api/cars');
    allCars = await res.json();
    filteredCars = [...allCars];
    renderPage(0, true);
}

function createCarCard(car) {
    const div = document.createElement('div');
    div.className = 'car-card-wrap';
    div.setAttribute('data-aos', 'fade-up');

    // Stats formatted for the pro "car guy" look
    const hp = car.horsepower ? Math.round(car.horsepower) : '---';
    const accel = car.acceleration ? Number(car.acceleration).toFixed(1) : '---';
    const price = car.price_usd ? '$' + Math.round(car.price_usd).toLocaleString() : 'Price on Request';

    // Performance bar calculations
    const hpFill = Math.min((car.horsepower / 15) || 0, 100);
    const accFill = Math.min(((10 - (car.acceleration || 10)) / 10 * 100), 100);

    div.innerHTML = `
        <div class="car-card" data-car-id="${car.id}" data-brand="${car.brand}" data-hp="${hp}" data-acc="${accel}" onclick="window.location='/cars/${car.id}'">
            <div class="card-speed-sweep"></div>
            <div class="card-img-wrap">
                <img src="${car.image_exterior || car.image_url}" 
                     data-brand="${car.brand}"
                     data-model="${car.model}"
                     alt="${car.brand} ${car.model}"
                     loading="lazy"
                     class="car-photo">
                
                <div class="card-hover-overlay">
                    <div class="perf-bars">
                        <div class="perf-bar-item">
                            <span class="pb-label">POWER</span>
                            <div class="pb-track"><div class="pb-fill" style="width: ${hpFill}%"></div></div>
                            <span class="pb-val">${hp} HP</span>
                        </div>
                        <div class="perf-bar-item">
                            <span class="pb-label">0-100</span>
                            <div class="pb-track"><div class="pb-fill" style="width: ${accFill}%"></div></div>
                            <span class="pb-val">${accel}s</span>
                        </div>
                    </div>
                    <div class="card-actions">
                        <button class="ca-btn ca-garage" onclick="event.stopPropagation(); addToGarage(${car.id})">+ GARAGE</button>
                        <button class="ca-btn ca-compare" onclick="event.stopPropagation(); addToCompare(${car.id}, '${car.model}', '${car.brand}', ${hp}, ${accel}, '${car.image_exterior || car.image_url}')">COMPARE</button>
                    </div>
                </div>
                <div class="card-category-badge">${car.category || car.fuel_type || 'SPORT'}</div>
            </div>
            <div class="card-body">
                <div class="card-brand">${car.brand.toUpperCase()}</div>
                <div class="card-model">${car.model}</div>
                <div class="card-year-row">
                    <span class="card-year">${car.year}</span>
                    <div class="rev-lights">
                        <div class="rev-light rl-green"></div><div class="rev-light rl-green"></div><div class="rev-light rl-yellow"></div><div class="rev-light rl-yellow"></div><div class="rev-light rl-red"></div>
                    </div>
                </div>
                <div class="card-stat-strip">
                    <div class="css-item"><span class="css-v">${hp}</span><span class="css-k">HP</span></div>
                    <div class="css-divider"></div>
                    <div class="css-item"><span class="css-v">${accel}</span><span class="css-k">0-100s</span></div>
                    <div class="css-divider"></div>
                    <div class="css-item"><span class="css-v">${(car.fuel_type || 'GAS').substring(0, 3).toUpperCase()}</span><span class="css-k">FUEL</span></div>
                </div>
            </div>
        </div>
    `;

    // Initialize error handling for the new image
    const img = div.querySelector('img');
    img.onerror = () => { if (typeof handleImageError === 'function') handleImageError(img); };

    return div;
}

function renderPage(pageNum, clear = false) {
    const grid = document.getElementById('cars-grid');
    if (clear) {
        grid.innerHTML = '';
        page = 0;
    }

    const start = pageNum * pageSize;
    const slice = filteredCars.slice(start, start + pageSize);

    slice.forEach(car => {
        grid.appendChild(createCarCard(car));
    });

    if (typeof AOS !== 'undefined') {
        AOS.refresh();
    }
    page = pageNum;
}

// Filtering
function applyFilters() {
    const search = document.getElementById('search-input').value.toLowerCase();
    const brand = document.getElementById('filter-brand').value;
    const category = document.getElementById('filter-category').value;

    filteredCars = allCars.filter(car => {
        const matchSearch = (car.brand + ' ' + car.model).toLowerCase().includes(search);
        const matchBrand = !brand || car.brand === brand;
        const matchCat = !category || car.category === category;
        return matchSearch && matchBrand && matchCat;
    });

    renderPage(0, true);
}

// Sorting
function applySort() {
    const sort = document.getElementById('sort-select').value;

    if (sort === 'fastest') {
        filteredCars.sort((a, b) => (b.horsepower || 0) - (a.horsepower || 0));
    } else if (sort === 'quickest') {
        filteredCars.sort((a, b) => (a.acceleration || 99) - (b.acceleration || 99));
    } else if (sort === 'newest') {
        filteredCars.sort((a, b) => (b.year || 0) - (a.year || 0));
    } else if (sort === 'price-high') {
        filteredCars.sort((a, b) => (b.price_usd || 0) - (a.price_usd || 0));
    } else {
        filteredCars = [...allCars]; // Default/Alphabetical (mostly)
    }

    renderPage(0, true);
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadCars();

    // Search listener
    document.getElementById('search-input').addEventListener('input', applyFilters);

    // Intersection Observer for infinite scroll
    const sentinel = document.getElementById('scroll-sentinel');
    const observer = new IntersectionObserver(entries => {
        if (entries[0].isIntersecting && (page + 1) * pageSize < filteredCars.length) {
            renderPage(page + 1);
        }
    });
    observer.observe(sentinel);
});
