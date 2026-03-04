function switchAngle(angle) {
    const img = document.getElementById('main-car-img');
    const newSrc = img.dataset[angle];
    if (!newSrc) return;

    img.style.opacity = '0';
    img.style.transform = 'scale(0.98)';

    setTimeout(() => {
        img.src = newSrc;
        img.style.opacity = '1';
        img.style.transform = 'scale(1)';
    }, 200);

    document.querySelectorAll('.gtab').forEach(t =>
        t.classList.remove('active'));

    const activeTab = document.querySelector(`[data-angle="${angle}"]`);
    if (activeTab) activeTab.classList.add('active');
}

// 3D Tilt Effect
document.addEventListener('DOMContentLoaded', () => {
    const heroCard = document.querySelector('.hero-card-3d');
    if (heroCard) {
        heroCard.addEventListener('mousemove', (e) => {
            const rect = heroCard.getBoundingClientRect();
            const x = (e.clientX - rect.left) / rect.width - 0.5;
            const y = (e.clientY - rect.top) / rect.height - 0.5;
            heroCard.style.transform = `perspective(1000px) rotateY(${x * 8}deg) rotateX(${y * -8}deg) scale(1.02)`;
        });

        heroCard.addEventListener('mouseleave', () => {
            heroCard.style.transform = `perspective(1000px) rotateY(0deg) rotateX(0deg) scale(1)`;
        });
    }

    // Counter Animation
    const counters = document.querySelectorAll('.spec-counter');
    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const counter = entry.target;
                const target = +counter.dataset.target;
                const suffix = counter.dataset.suffix || '';
                let current = 0;
                const increment = target / 50;

                const timer = setInterval(() => {
                    current += increment;
                    if (current >= target) {
                        counter.innerText = target + suffix;
                        clearInterval(timer);
                    } else {
                        counter.innerText = Math.round(current);
                    }
                }, 40);
                observer.unobserve(counter);
            }
        });
    }, { threshold: 1 });

    counters.forEach(c => observer.observe(c));
});
