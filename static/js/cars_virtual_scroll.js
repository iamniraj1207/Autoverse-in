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

function createCarCard(car, index = 0) {
    const div = document.createElement('div');
    div.className = 'car-card-wrap';
    div.setAttribute('data-aos', 'fade-up');
    div.setAttribute('data-aos-delay', String((index % 12) * 50));

    const hp = car.horsepower ? Math.round(car.horsepower) : '---';
    const accel = car.acceleration ? Number(car.acceleration).toFixed(1) : '---';
    // High-fidelity price synchronization (1 Cr = $120,000 USD / ₹10M INR)
    let rawPriceUSD = 0;
    let rawPriceINR = 0;
    const dbPrice = String(car.price_usd || '1.5 Cr').toLowerCase();
    
    if (dbPrice.includes('cr')) {
        const val = parseFloat(dbPrice);
        rawPriceUSD = val * 120000;
        rawPriceINR = val * 10000000; // 1 Crore = 10,000,000
    } else {
        rawPriceUSD = parseFloat(dbPrice) || 50000;
        rawPriceINR = rawPriceUSD * 83.5;
    }
    
    const priceDisplay = `$${Math.round(rawPriceUSD).toLocaleString()} | ₹${(rawPriceINR/10000000).toFixed(2)} Cr`;

    const hpFill = Math.min((car.horsepower / 15) || 0, 100);
    const accFill = Math.min(((10 - (car.acceleration || 10)) / 10 * 100), 100);

    div.innerHTML = `
        <div class="car-card" data-car-id="${car.id}" data-brand="${car.brand}" data-hp="${hp}" data-acc="${accel}" onclick="window.location='/cars/${car.id}'">
            <div class="card-speed-sweep"></div>
            <div class="card-img-wrap">
                <img src="${car.image_url}" 
                     alt="${car.brand} ${car.model}"
                     loading="lazy"
                     class="car-photo"
                     onerror="this.onerror=null;this.src='https://cdn.imagin.studio/getImage?customer=img&make=${car.brand.toLowerCase().replace(/ /g,'-')}&modelFamily=${car.model.split(' ')[0].toLowerCase()}&zoomType=fullscreen&paintId=25&angle=01';">
                
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
                </div>
                <div class="card-category-badge">${car.category || 'SPORT'}</div>
            </div>
            <div class="card-body">
                <div class="card-brand">${car.brand.toUpperCase()}</div>
                <div class="card-model">${car.model}</div>
                <div class="card-price-row" style="margin-top: 10px; text-align: center;">
                    <span class="price-val" style="font-family: 'DM Mono', monospace; font-size: 12px; color: #e83a3a; letter-spacing: 1px;">${priceDisplay}</span>
                </div>
            </div>
        </div>
    `;

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

    slice.forEach((car, index) => {
        grid.appendChild(createCarCard(car, index));
    });

    if (typeof AOS !== 'undefined') { AOS.refresh(); }
    initTilt();
    page = pageNum;
}

function initTilt() {
    const cards = document.querySelectorAll('.car-card');
    cards.forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            const rotateX = ((y - centerY) / centerY) * -5;
            const rotateY = ((x - centerX) / centerX) * 5;
            card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-10px) scale(1.02)`;
        });
        card.addEventListener('mouseleave', () => {
            card.style.transform = `perspective(1000px) rotateX(0deg) rotateY(0deg) translateY(0) scale(1)`;
        });
    });
}

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

document.addEventListener('DOMContentLoaded', () => {
    loadCars();
    document.getElementById('search-input').addEventListener('input', applyFilters);
    const sentinel = document.getElementById('scroll-sentinel');
    const observer = new IntersectionObserver(entries => {
        if (entries[0].isIntersecting && (page + 1) * pageSize < filteredCars.length) {
            renderPage(page + 1);
        }
    });
    observer.observe(sentinel);
});
