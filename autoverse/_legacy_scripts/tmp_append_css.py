import os

css_path = os.path.join('static', 'css', 'style.css')
new_css = """
/* ── Comparison Engine & Visuals ────────────────────────── */
.compare-selectors {
  display: flex;
  gap: 16px;
  margin-bottom: 48px;
  flex-wrap: wrap;
}

.compare-select {
  flex: 1;
  min-width: 200px;
  background: var(--surface);
  border: 1px solid var(--border);
  color: var(--text);
  padding: 12px 16px;
  border-radius: var(--radius);
  font-family: inherit;
  font-size: 13px;
  outline: none;
  transition: border-color 0.2s;
  cursor: pointer;
}

.compare-select:focus {
  border-color: var(--accent);
}

.compare-car-card {
  background: var(--surface);
  border: 1px solid var(--border);
  padding: 24px;
  border-radius: 8px;
  text-align: center;
  position: relative;
  transition: transform 0.3s, border-color 0.3s;
}

.compare-car-card:hover {
  transform: translateY(-5px);
  border-color: var(--accent);
}

.compare-img-scene {
  position: relative;
  height: 120px;
  overflow: hidden;
  border-radius: 4px;
}

.comp-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: opacity 0.4s;
}

.comp-interior-overlay {
  position: absolute;
  inset: 0;
  opacity: 0;
  transition: opacity 0.4s;
  pointer-events: none;
}

.compare-img-scene:hover .ext-img { opacity: 0; }
.compare-img-scene:hover .comp-interior-overlay { opacity: 1; }

.int-label {
  position: absolute;
  bottom: 8px;
  right: 8px;
  background: var(--accent);
  color: #fff;
  font-size: 8px;
  padding: 2px 6px;
  font-weight: 700;
  letter-spacing: 1px;
}

.spec-pill {
  background: var(--surface2);
  border: 1px solid var(--border);
  padding: 12px;
  border-radius: 6px;
  text-align: center;
  font-family: 'DM Mono', monospace;
  font-size: 13px;
  color: var(--muted2);
  transition: all 0.3s;
}

.spec-pill.is-best {
  border-color: var(--gold);
  color: var(--gold);
  background: rgba(240, 165, 0, 0.05);
  box-shadow: 0 0 15px rgba(240, 165, 0, 0.1);
}

/* ── Revolutionized Car Cards ───────────────────────────── */
.car-card {
  position: relative;
  display: block;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1);
}

.car-card-bg-glow {
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at 50% 120%, rgba(232, 58, 58, 0.15), transparent 70%);
  opacity: 0;
  transition: opacity 0.4s;
  pointer-events: none;
}

.car-card:hover {
  transform: translateY(-8px) scale(1.02);
  border-color: rgba(232, 58, 58, 0.4);
  box-shadow: 0 20px 40px rgba(0,0,0,0.4);
}

.car-card:hover .car-card-bg-glow { opacity: 1; }

.car-stats-hover-overlay {
  position: absolute;
  inset: 0;
  background: rgba(8, 10, 15, 0.85);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 24px;
  opacity: 0;
  transition: all 0.4s;
  backdrop-filter: blur(4px);
  pointer-events: none;
}

.car-card:hover .car-stats-hover-overlay { opacity: 1; }

.h-stat { text-align: center; }
.h-val { display: block; font-family: 'Bebas Neue', sans-serif; font-size: 32px; color: var(--accent); line-height: 1; }
.h-label { font-family: 'DM Mono', monospace; font-size: 9px; color: var(--muted2); letter-spacing: 1px; }

.car-price-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 12px;
}

.price-val { font-weight: 700; color: var(--text); }
.arrow-icon { color: var(--accent); transform: translateX(-5px); opacity: 0; transition: 0.3s; }
.car-card:hover .arrow-icon { transform: translateX(0); opacity: 1; }

.bebas { font-family: 'Bebas Neue', sans-serif; }
"""

with open(css_path, 'a', encoding='utf-8') as f:
    f.write(new_css)
print("CSS Updated Successfully!")
