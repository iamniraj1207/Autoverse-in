class F1Timeline {
    constructor(containerId, apiUrl, teamColor) {
        this.container = document.getElementById(containerId);
        this.apiUrl = apiUrl;
        this.teamColor = teamColor || '#e83a3a';
        if (this.container) this.init();
    }

    async init() {
        this.renderSkeleton();
        try {
            const res = await fetch(this.apiUrl);
            if (!res.ok) throw new Error('Failed');
            this.events = await res.json();
            this.render();
            this.animateOnScroll();
        } catch (e) {
            console.error('Timeline error:', e);
            this.container.innerHTML =
                '<p style="color:#5a6070;padding:20px">Timeline unavailable.</p>';
        }
    }

    renderSkeleton() {
        this.container.innerHTML = [1, 2, 3, 4].map(() => `
      <div style="display:flex;gap:16px;margin-bottom:28px">
        <div style="width:20px;height:20px;border-radius:50%;
                    background:#1e2535;flex-shrink:0;margin-top:4px;
                    animation:shimmer 1.5s infinite"></div>
        <div style="flex:1">
          <div style="width:60px;height:24px;background:#1e2535;
                      border-radius:2px;margin-bottom:8px;
                      animation:shimmer 1.5s infinite"></div>
          <div style="width:75%;height:14px;background:#1e2535;
                      border-radius:2px;margin-bottom:6px;
                      animation:shimmer 1.5s infinite"></div>
          <div style="width:90%;height:11px;background:#141820;
                      border-radius:2px;
                      animation:shimmer 1.5s infinite"></div>
        </div>
      </div>
    `).join('');
    }

    getColor(type) {
        return {
            championship: '#f0a500',
            win: '#00d4aa',
            debut: '#3a7bd5',
            record: '#ff6b35',
            transfer: '#8892a4',
            tragedy: '#e83a3a',
            technical: '#b06aff',
            founded: '#e83a3a'
        }[type] || '#8892a4';
    }

    getIcon(type) {
        return {
            championship: '🏆',
            win: '🥇',
            debut: '🏁',
            record: '⚡',
            transfer: '🔄',
            tragedy: '🖤',
            technical: '⚙️',
            founded: '🏗️'
        }[type] || '●';
    }

    render() {
        if (!this.events || !this.events.length) {
            this.container.innerHTML =
                '<p style="color:#5a6070;padding:20px">No timeline data.</p>';
            return;
        }

        this.container.innerHTML = `
      <div class="tl-wrap">
        <div class="tl-line">
          <div class="tl-line-fill" id="tl-fill-${this.container.id}"
               style="background:linear-gradient(to bottom,
               ${this.teamColor},#f0a500)"></div>
        </div>
        <div class="tl-items">
          ${this.events.map((ev, i) => `
            <div class="tl-item" data-index="${i}" 
                 id="tl-item-${this.container.id}-${i}"
                 style="opacity:0; transform: translateX(-20px);">
              <div class="tl-dot-wrap">
                <div class="tl-dot"
                     style="border-color:${this.getColor(ev.milestone_type)}">
                  <div class="tl-dot-inner"
                       style="background:${this.getColor(ev.milestone_type)}">
                  </div>
                </div>
              </div>
              <div class="tl-card">
                <div class="tl-year"
                     style="color:${this.getColor(ev.milestone_type)}">
                  ${ev.year}
                </div>
                <span class="tl-badge"
                      style="border-color:${this.getColor(ev.milestone_type)};
                             color:${this.getColor(ev.milestone_type)}">
                  ${this.getIcon(ev.milestone_type)} 
                  ${(ev.milestone_type || 'event').toUpperCase()}
                </span>
                <div class="tl-title">${ev.title}</div>
                <div class="tl-desc">${ev.description}</div>
              </div>
            </div>
          `).join('')}
        </div>
      </div>
    `;
    }

    animateOnScroll() {
        const items = this.container.querySelectorAll('.tl-item');
        const fill = document.getElementById(
            `tl-fill-${this.container.id}`
        );
        if (!items.length || !fill) return;

        let maxRevealed = -1;

        const observer = new IntersectionObserver(entries => {
            entries.forEach(entry => {
                if (!entry.isIntersecting) return;
                const item = entry.target;
                const idx = parseInt(item.dataset.index);

                // Slide in
                item.style.opacity = '1';
                item.style.transform = 'translateX(0)';

                // Bounce dot
                const dot = item.querySelector('.tl-dot');
                if (dot) dot.style.transform = 'scale(1)';

                // Grow line
                if (idx > maxRevealed) {
                    maxRevealed = idx;
                    const pct = ((idx + 1) / items.length) * 100;
                    fill.style.height = pct + '%';
                }

                observer.unobserve(item);
            });
        }, { threshold: 0.15, rootMargin: '0px 0px -40px 0px' });

        items.forEach(item => observer.observe(item));
    }
}
window.F1Timeline = F1Timeline;
