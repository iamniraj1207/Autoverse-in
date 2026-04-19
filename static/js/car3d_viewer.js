/**
 * car3d_viewer.js — AutoVerse 360° Interactive Car Viewer
 *
 * Strategy:
 *   1. If a real GLTF model exists for this car's archetype → load it
 *   2. Otherwise → build a procedural Three.js mesh for the archetype
 *
 * Archetypes (8 total):
 *   hypercar    → Pagani, Bugatti, Koenigsegg, Rimac — ultra-low, wide
 *   supercar    → Ferrari, Lamborghini, McLaren      — mid-engine (uses real GLTF)
 *   sportscar   → Porsche 911, BMW M, Ford Mustang   — sharp coupe
 *   grandtourer → Aston Martin, Bentley GT, Maserati — long bonnet GT
 *   suv         → Urus, Cayenne, G63                 — tall, muscular
 *   electric    → Tesla, Rivian, Lucid               — smooth aero
 *   f1          → F1 cars                            — open-wheel, wings
 *   classic     → Vintage / Pre-2000 icons           — upright, rounded
 */

'use strict';

/* ========================
   ARCHETYPE MAPPING TABLE
   ======================== */
const ARCHETYPE_MAP = {
    // By brand
    'pagani': 'hypercar', 'bugatti': 'hypercar', 'koenigsegg': 'hypercar',
    'rimac': 'hypercar', 'zenvo': 'hypercar', 'hennessey': 'hypercar',
    'ferrari': 'supercar', 'lamborghini': 'supercar', 'mclaren': 'supercar',
    'lotus': 'supercar', 'alfa romeo': 'supercar',
    'porsche': 'sportscar', 'bmw': 'sportscar', 'ford': 'sportscar',
    'dodge': 'sportscar', 'chevrolet': 'sportscar', 'nissan': 'sportscar',
    'honda': 'sportscar', 'mazda': 'sportscar', 'subaru': 'sportscar',
    'toyota': 'sportscar', 'mitsubishi': 'sportscar',
    'aston martin': 'grandtourer', 'bentley': 'grandtourer',
    'maserati': 'grandtourer', 'jaguar': 'grandtourer',
    'mercedes': 'grandtourer', 'audi': 'grandtourer',
    'rolls-royce': 'grandtourer', 'rolls royce': 'grandtourer',
    'tesla': 'electric', 'rivian': 'electric', 'lucid': 'electric',
    'polestar': 'electric', 'nio': 'electric',
    // By category
    'hypercar': 'hypercar', 'super car': 'supercar', 'supercar': 'supercar',
    'sports car': 'sportscar', 'sports': 'sportscar', 'coupe': 'sportscar',
    'suv': 'suv', 'crossover': 'suv', 'truck': 'suv',
    'electric': 'electric', 'ev': 'electric',
    'f1': 'f1', 'formula': 'f1',
    'classic': 'classic', 'vintage': 'classic',
    'grand tourer': 'grandtourer', 'gt': 'grandtourer'
};

/* GLTF models available (downloaded to /static/models/cars/) */
const GLTF_MODELS = {
    supercar: '/static/models/cars/supercar.glb',
    hypercar: '/static/models/cars/supercar.glb', // reuse for now
};

const AO_MAP_URL = '/static/models/cars/ferrari_ao.png';

/* ========================
   COLOR PALETTES
   ======================== */
const BRAND_COLORS = {
    ferrari: 0xCC0000, lamborghini: 0xFFAA00, mclaren: 0xFF6600,
    bugatti: 0x1144BB, pagani: 0x333333, koenigsegg: 0x222222,
    mercedes: 0x111111, bmw: 0x003399, porsche: 0xCC0000,
    audi: 0x888888, aston_martin: 0x006633, bentley: 0x444400,
    tesla: 0xCC2200, rimac: 0x003388, maserati: 0x000066,
    rolls_royce: 0x8B8000
};

function getBrandColor(brand) {
    const key = brand.toLowerCase().replace(/[^a-z]/g, '_');
    return BRAND_COLORS[key] || 0xe83a3a;
}

function getArchetype(brand, category) {
    const b = (brand || '').toLowerCase();
    const c = (category || '').toLowerCase();
    return ARCHETYPE_MAP[b] || ARCHETYPE_MAP[c] || 'supercar';
}

/* ========================
   PROCEDURAL BUILDERS
   ======================== */

/**
 * Build a car from scratch using Three.js geometry.
 * Returns a THREE.Group containing detailed body, wheels, glass.
 */
function buildProceduralCar(archetype, color) {
    const group = new THREE.Group();

    const bodyMat = new THREE.MeshStandardMaterial({
        color: new THREE.Color(color),
        metalness: 0.75, roughness: 0.22,
        envMapIntensity: 1.2
    });
    const glassMat = new THREE.MeshStandardMaterial({
        color: 0x112244, transparent: true, opacity: 0.55,
        metalness: 0.1, roughness: 0.05
    });
    const tireMat = new THREE.MeshStandardMaterial({
        color: 0x0a0a0a, metalness: 0.0, roughness: 0.9
    });
    const rimMat = new THREE.MeshStandardMaterial({
        color: 0x888888, metalness: 0.95, roughness: 0.1
    });
    const redMat = new THREE.MeshStandardMaterial({
        color: 0xe83a3a, emissive: 0xe83a3a, emissiveIntensity: 0.4
    });

    if (archetype === 'f1') {
        buildF1(group, bodyMat, tireMat, rimMat, glassMat, redMat);
    } else if (archetype === 'suv') {
        buildSUV(group, bodyMat, glassMat, tireMat, rimMat, redMat);
    } else if (archetype === 'electric') {
        buildElectric(group, bodyMat, glassMat, tireMat, rimMat, redMat);
    } else if (archetype === 'classic') {
        buildClassic(group, bodyMat, glassMat, tireMat, rimMat, redMat);
    } else if (archetype === 'grandtourer') {
        buildGT(group, bodyMat, glassMat, tireMat, rimMat, redMat);
    } else if (archetype === 'hypercar') {
        buildHypercar(group, bodyMat, glassMat, tireMat, rimMat, redMat);
    } else {
        // sportscar default
        buildSportsCar(group, bodyMat, glassMat, tireMat, rimMat, redMat);
    }

    return group;
}

/* ─── HELPER: make a wheel ─── */
function makeWheel(tireMat, rimMat, redMat, radius, thickness) {
    const wg = new THREE.Group();
    // Tire
    const tire = new THREE.Mesh(
        new THREE.TorusGeometry(radius, thickness, 8, 28),
        tireMat
    );
    tire.rotation.y = Math.PI / 2;
    wg.add(tire);
    // Rim disc
    const rim = new THREE.Mesh(
        new THREE.CylinderGeometry(radius * 0.72, radius * 0.72, thickness * 1.05, 28),
        rimMat
    );
    rim.rotation.z = Math.PI / 2;
    wg.add(rim);
    // Spokes (5-spoke design)
    for (let i = 0; i < 5; i++) {
        const sg = new THREE.Mesh(
            new THREE.BoxGeometry(radius * 0.06, radius * 1.3, thickness * 0.6),
            rimMat
        );
        sg.rotation.z = (i / 5) * Math.PI * 2;
        wg.add(sg);
    }
    // Centre cap
    const cap = new THREE.Mesh(
        new THREE.CylinderGeometry(radius * 0.12, radius * 0.12, thickness * 1.2, 10),
        redMat
    );
    cap.rotation.z = Math.PI / 2;
    wg.add(cap);
    return wg;
}

/* ─── SPORTS CAR ─── */
function buildSportsCar(g, bodyMat, glassMat, tireMat, rimMat, redMat) {
    // Main body (low coupe profile)
    const body = new THREE.Mesh(
        new THREE.BoxGeometry(4.4, 0.55, 2.0),
        bodyMat
    );
    body.position.y = 0.35;
    g.add(body);

    // Lower sill/diffuser
    const sill = new THREE.Mesh(new THREE.BoxGeometry(4.2, 0.2, 2.1), bodyMat);
    sill.position.y = 0.05;
    g.add(sill);

    // Cabin (roof)
    const cabin = new THREE.Mesh(new THREE.BoxGeometry(2.4, 0.4, 1.7), bodyMat);
    cabin.position.set(-0.1, 0.78, 0);
    g.add(cabin);

    // Windshield
    const wind = new THREE.Mesh(new THREE.BoxGeometry(0.04, 0.38, 1.6), glassMat);
    wind.rotation.y = 0;
    wind.rotation.z = -0.45;
    wind.position.set(0.98, 0.78, 0);
    g.add(wind);

    // Rear screen
    const rear = new THREE.Mesh(new THREE.BoxGeometry(0.04, 0.36, 1.5), glassMat);
    rear.rotation.z = 0.4;
    rear.position.set(-1.17, 0.78, 0);
    g.add(rear);

    // Side windows
    const sw = new THREE.Mesh(new THREE.BoxGeometry(2.3, 0.28, 0.04), glassMat);
    sw.position.set(-0.1, 0.8, 0.87);
    g.add(sw);
    const sw2 = sw.clone(); sw2.position.z = -0.87; g.add(sw2);

    // Front hood slope
    const hood = new THREE.Mesh(new THREE.BoxGeometry(1.5, 0.12, 1.9), bodyMat);
    hood.rotation.z = 0.12;
    hood.position.set(1.75, 0.62, 0);
    g.add(hood);

    // Headlights
    const hlMat = new THREE.MeshStandardMaterial({ color: 0xffffff, emissive: 0xffffff, emissiveIntensity: 1.2 });
    [-0.72, 0.72].forEach(z => {
        const hl = new THREE.Mesh(new THREE.BoxGeometry(0.25, 0.1, 0.35), hlMat);
        hl.position.set(2.1, 0.42, z);
        g.add(hl);
    });

    // Taillights
    [-0.7, 0.7].forEach(z => {
        const tl = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.14, 0.4), redMat);
        tl.position.set(-2.18, 0.42, z);
        g.add(tl);
    });

    // Wheels
    const wRadius = 0.38, wThick = 0.22;
    const positions = [[1.3, 0, 1.1], [1.3, 0, -1.1], [-1.3, 0, 1.1], [-1.3, 0, -1.1]];
    positions.forEach(([x, y, z]) => {
        const w = makeWheel(tireMat, rimMat, redMat, wRadius, wThick);
        w.position.set(x, y, z);
        g.add(w);
    });

    // Exhaust
    const exMat = new THREE.MeshStandardMaterial({ color: 0x555555, metalness: 0.9, roughness: 0.2 });
    [-0.35, 0.35].forEach(z => {
        const ex = new THREE.Mesh(new THREE.TorusGeometry(0.07, 0.025, 8, 16), exMat);
        ex.rotation.y = Math.PI / 2;
        ex.position.set(-2.22, 0.12, z);
        g.add(ex);
    });

    g.position.y = 0.38;
}

/* ─── HYPERCAR ─── (Pagani-inspired, ultra-low wide body) ─── */
function buildHypercar(g, bodyMat, glassMat, tireMat, rimMat, redMat) {
    // Ultra-flat main body
    const body = new THREE.Mesh(new THREE.BoxGeometry(4.6, 0.35, 2.3), bodyMat);
    body.position.y = 0.3;
    g.add(body);

    // Flared rear haunches
    const rHaunch = new THREE.Mesh(new THREE.BoxGeometry(1.4, 0.3, 2.7), bodyMat);
    rHaunch.position.set(-1.2, 0.28, 0);
    g.add(rHaunch);

    // Low cabin (teardrop)
    const cab = new THREE.Mesh(new THREE.BoxGeometry(1.6, 0.32, 1.5), bodyMat);
    cab.position.set(0, 0.56, 0);
    g.add(cab);

    // Windshield (very raked)
    const ws = new THREE.Mesh(new THREE.BoxGeometry(0.04, 0.3, 1.4), glassMat);
    ws.rotation.z = -0.62;
    ws.position.set(0.78, 0.57, 0);
    g.add(ws);

    // Rear window
    const rw = new THREE.Mesh(new THREE.BoxGeometry(0.04, 0.28, 1.3), glassMat);
    rw.rotation.z = 0.55;
    rw.position.set(-0.77, 0.57, 0);
    g.add(rw);

    // Side windows
    const swH = new THREE.Mesh(new THREE.BoxGeometry(1.5, 0.22, 0.03), glassMat);
    swH.position.set(0, 0.6, 0.77); g.add(swH);
    const swH2 = swH.clone(); swH2.position.z = -0.77; g.add(swH2);

    // Front splitter
    const splitter = new THREE.Mesh(new THREE.BoxGeometry(0.2, 0.05, 2.4), bodyMat);
    splitter.position.set(2.35, 0.05, 0);
    g.add(splitter);

    // Rear diffuser fins
    for (let i = -3; i <= 3; i++) {
        const fin = new THREE.Mesh(new THREE.BoxGeometry(0.4, 0.12, 0.025), bodyMat);
        fin.position.set(-2.2, 0.1, i * 0.3);
        g.add(fin);
    }

    // Headlights — sharp slashes
    const hlMat = new THREE.MeshStandardMaterial({ color: 0xffffff, emissive: 0xffffff, emissiveIntensity: 1.5 });
    [-0.75, 0.75].forEach(z => {
        const hl = new THREE.Mesh(new THREE.BoxGeometry(0.4, 0.06, 0.25), hlMat);
        hl.position.set(2.15, 0.35, z);
        hl.rotation.y = 0.3;
        g.add(hl);
    });

    // Dual taillights
    [-0.8, 0.8].forEach(z => {
        const tl = new THREE.Mesh(new THREE.BoxGeometry(0.06, 0.1, 0.5), redMat);
        tl.position.set(-2.25, 0.32, z);
        g.add(tl);
    });

    // Wide fat wheels
    const positions = [[1.4, 0, 1.2], [1.4, 0, -1.2], [-1.35, 0, 1.3], [-1.35, 0, -1.3]];
    positions.forEach(([x, y, z]) => {
        const w = makeWheel(tireMat, rimMat, redMat, 0.4, 0.28);
        w.position.set(x, y, z);
        g.add(w);
    });

    // Center exhaust quad
    const exMat = new THREE.MeshStandardMaterial({ color: 0x3a3a3a, metalness: 0.95, roughness: 0.1 });
    [-0.2, 0.2].forEach(z => {
        const ex = new THREE.Mesh(new THREE.TorusGeometry(0.065, 0.022, 8, 16), exMat);
        ex.rotation.y = Math.PI / 2;
        ex.position.set(-2.32, 0.1, z);
        g.add(ex);
    });

    g.position.y = 0.4;
}

/* ─── GRAND TOURER ─── (Aston Martin / Bentley) ─── */
function buildGT(g, bodyMat, glassMat, tireMat, rimMat, redMat) {
    // Long bonnet body
    const body = new THREE.Mesh(new THREE.BoxGeometry(5.0, 0.5, 2.0), bodyMat);
    body.position.y = 0.38;
    g.add(body);

    // Long bonnet (front-engine GT)
    const hood = new THREE.Mesh(new THREE.BoxGeometry(2.2, 0.1, 1.9), bodyMat);
    hood.rotation.z = 0.08;
    hood.position.set(1.5, 0.62, 0);
    g.add(hood);

    // Fastback roof
    const roof = new THREE.Mesh(new THREE.BoxGeometry(2.0, 0.38, 1.8), bodyMat);
    roof.position.set(-0.3, 0.74, 0);
    g.add(roof);

    // Windshield
    const ws = new THREE.Mesh(new THREE.BoxGeometry(0.04, 0.36, 1.7), glassMat);
    ws.rotation.z = -0.38;
    ws.position.set(0.82, 0.74, 0);
    g.add(ws);

    // Rear fastback window (raked)
    const rw = new THREE.Mesh(new THREE.BoxGeometry(0.04, 0.4, 1.7), glassMat);
    rw.rotation.z = 0.28;
    rw.position.set(-1.2, 0.74, 0);
    g.add(rw);

    // Side windows
    const sw = new THREE.Mesh(new THREE.BoxGeometry(1.9, 0.3, 0.03), glassMat);
    sw.position.set(-0.3, 0.78, 1.02); g.add(sw);
    const sw2 = sw.clone(); sw2.position.z = -1.02; g.add(sw2);

    // Grille (front face)
    const grille = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.22, 1.3),
        new THREE.MeshStandardMaterial({ color: 0x111111, metalness: 0.5, roughness: 0.4 }));
    grille.position.set(2.51, 0.4, 0);
    g.add(grille);

    // Rounded headlights
    const hlMat = new THREE.MeshStandardMaterial({ color: 0xeeeecc, emissive: 0xffffff, emissiveIntensity: 0.8 });
    [-0.65, 0.65].forEach(z => {
        const hl = new THREE.Mesh(new THREE.CylinderGeometry(0.14, 0.14, 0.1, 12), hlMat);
        hl.rotation.z = Math.PI / 2;
        hl.position.set(2.5, 0.44, z);
        g.add(hl);
    });

    // Taillights
    [-0.65, 0.65].forEach(z => {
        const tl = new THREE.Mesh(new THREE.BoxGeometry(0.07, 0.18, 0.45), redMat);
        tl.position.set(-2.5, 0.4, z);
        g.add(tl);
    });

    // Wheels
    const positions = [[1.6, 0, 1.0], [1.6, 0, -1.0], [-1.5, 0, 1.0], [-1.5, 0, -1.0]];
    positions.forEach(([x, y, z]) => {
        const w = makeWheel(tireMat, rimMat, redMat, 0.4, 0.22);
        w.position.set(x, y, z);
        g.add(w);
    });

    g.position.y = 0.4;
}

/* ─── SUV ─── */
function buildSUV(g, bodyMat, glassMat, tireMat, rimMat, redMat) {
    // Tall body
    const body = new THREE.Mesh(new THREE.BoxGeometry(4.8, 0.7, 2.2), bodyMat);
    body.position.y = 0.8;
    g.add(body);

    // Cabin (tall)
    const cabin = new THREE.Mesh(new THREE.BoxGeometry(2.8, 0.55, 2.1), bodyMat);
    cabin.position.set(-0.2, 1.35, 0);
    g.add(cabin);

    // Roof rails
    const rrMat = new THREE.MeshStandardMaterial({ color: 0x333333, metalness: 0.8, roughness: 0.3 });
    [-0.95, 0.95].forEach(z => {
        const rr = new THREE.Mesh(new THREE.BoxGeometry(2.6, 0.04, 0.06), rrMat);
        rr.position.set(-0.2, 1.65, z);
        g.add(rr);
    });

    // Windshield
    const ws = new THREE.Mesh(new THREE.BoxGeometry(0.04, 0.52, 2.0), glassMat);
    ws.rotation.z = -0.3;
    ws.position.set(0.98, 1.35, 0);
    g.add(ws);

    // Rear glass
    const rg = new THREE.Mesh(new THREE.BoxGeometry(0.04, 0.5, 1.95), glassMat);
    rg.rotation.z = 0.18;
    rg.position.set(-1.58, 1.35, 0);
    g.add(rg);

    // Side windows
    const sw = new THREE.Mesh(new THREE.BoxGeometry(2.6, 0.4, 0.03), glassMat);
    sw.position.set(-0.2, 1.38, 1.08); g.add(sw);
    const sw2 = sw.clone(); sw2.position.z = -1.08; g.add(sw2);

    // Big headlights
    const hlMat = new THREE.MeshStandardMaterial({ color: 0xffffff, emissive: 0xffffff, emissiveIntensity: 1 });
    [-0.72, 0.72].forEach(z => {
        const hl = new THREE.Mesh(new THREE.BoxGeometry(0.2, 0.14, 0.45), hlMat);
        hl.position.set(2.42, 0.88, z);
        g.add(hl);
    });

    // Taillights
    [-0.7, 0.7].forEach(z => {
        const tl = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.22, 0.65), redMat);
        tl.position.set(-2.42, 0.96, z);
        g.add(tl);
    });

    // Big off-road wheels
    const positions = [[1.5, 0, 1.1], [1.5, 0, -1.1], [-1.5, 0, 1.1], [-1.5, 0, -1.1]];
    positions.forEach(([x, y, z]) => {
        const w = makeWheel(tireMat, rimMat, redMat, 0.52, 0.28);
        w.position.set(x, y, z);
        g.add(w);
    });

    // Running boards
    [-1.14, 1.14].forEach(z => {
        const rb = new THREE.Mesh(new THREE.BoxGeometry(3.2, 0.06, 0.2), rrMat);
        rb.position.set(0, 0.44, z);
        g.add(rb);
    });

    g.position.y = 0.52;
}

/* ─── ELECTRIC ─── (Tesla-inspired smooth aero) ─── */
function buildElectric(g, bodyMat, glassMat, tireMat, rimMat, redMat) {
    // Aerodynamic body
    const body = new THREE.Mesh(new THREE.BoxGeometry(4.9, 0.52, 2.1), bodyMat);
    body.position.y = 0.44;
    g.add(body);

    // Panoramic glass roof (distinctive Tesla look)
    const roof = new THREE.Mesh(new THREE.BoxGeometry(2.8, 0.06, 1.8), glassMat);
    roof.position.set(-0.1, 0.84, 0);
    g.add(roof);

    // Cabin under the glass roof
    const cab = new THREE.Mesh(new THREE.BoxGeometry(2.8, 0.38, 1.85), bodyMat);
    cab.position.set(-0.1, 0.64, 0);
    g.add(cab);

    // Windshield (tall, frameless-look)
    const ws = new THREE.Mesh(new THREE.BoxGeometry(0.04, 0.44, 1.96), glassMat);
    ws.rotation.z = -0.32;
    ws.position.set(1.1, 0.64, 0);
    g.add(ws);

    // Rear screen
    const rg = new THREE.Mesh(new THREE.BoxGeometry(0.04, 0.4, 1.9), glassMat);
    rg.rotation.z = 0.22;
    rg.position.set(-1.35, 0.64, 0);
    g.add(rg);

    // Side windows
    const sw = new THREE.Mesh(new THREE.BoxGeometry(2.6, 0.3, 0.03), glassMat);
    sw.position.set(-0.1, 0.68, 1.06); g.add(sw);
    const sw2 = sw.clone(); sw2.position.z = -1.06; g.add(sw2);

    // Full-width LED light bar (front)
    const hlMat = new THREE.MeshStandardMaterial({ color: 0xeeeeff, emissive: 0xffffff, emissiveIntensity: 1.3 });
    const ledFront = new THREE.Mesh(new THREE.BoxGeometry(0.04, 0.05, 1.9), hlMat);
    ledFront.position.set(2.48, 0.52, 0);
    g.add(ledFront);

    // Full-width LED light bar (rear)
    const ledRear = new THREE.Mesh(new THREE.BoxGeometry(0.04, 0.05, 1.85), redMat);
    ledRear.position.set(-2.48, 0.52, 0);
    g.add(ledRear);

    // Flush door handles
    const hdlMat = new THREE.MeshStandardMaterial({ color: 0x222222, metalness: 0.7, roughness: 0.2 });
    [-0.75, 0.75].forEach(z => {
        const hdl = new THREE.Mesh(new THREE.BoxGeometry(0.4, 0.04, 0.04), hdlMat);
        hdl.position.set(0.1, 0.58, z);
        g.add(hdl);
    });

    // Aerodynamic wheels (enclosed design)
    const aerRimMat = new THREE.MeshStandardMaterial({ color: 0xaaaaaa, metalness: 0.9, roughness: 0.08 });
    const positions = [[1.45, 0, 1.06], [1.45, 0, -1.06], [-1.45, 0, 1.06], [-1.45, 0, -1.06]];
    positions.forEach(([x, y, z]) => {
        const w = makeWheel(tireMat, aerRimMat, redMat, 0.42, 0.22);
        w.position.set(x, y, z);
        g.add(w);
    });

    g.position.y = 0.42;
}

/* ─── F1 CAR ─── */
function buildF1(g, bodyMat, glassMat, tireMat, rimMat, redMat) {
    // Nose cone
    const nose = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.2, 1.8, 6), bodyMat);
    nose.rotation.z = Math.PI / 2;
    nose.position.set(2.5, 0.18, 0);
    g.add(nose);

    // Main chassis
    const chassis = new THREE.Mesh(new THREE.BoxGeometry(3.2, 0.28, 0.65), bodyMat);
    chassis.position.set(0, 0.22, 0);
    g.add(chassis);

    // Cockpit surround
    const cockpit = new THREE.Mesh(new THREE.BoxGeometry(0.9, 0.32, 0.7), bodyMat);
    cockpit.position.set(0.1, 0.42, 0);
    g.add(cockpit);

    // Halo
    const haloMat = new THREE.MeshStandardMaterial({ color: 0xccaa00, metalness: 0.9, roughness: 0.1 });
    const halo = new THREE.Mesh(new THREE.TorusGeometry(0.32, 0.018, 8, 20, Math.PI), haloMat);
    halo.rotation.x = Math.PI / 2;
    halo.rotation.z = Math.PI;
    halo.position.set(0.1, 0.62, 0);
    g.add(halo);

    // Visor
    const visor = new THREE.Mesh(new THREE.BoxGeometry(0.5, 0.12, 0.55), glassMat);
    visor.rotation.z = 0.3;
    visor.position.set(0.3, 0.6, 0);
    g.add(visor);

    // FRONT WING
    const fw = new THREE.Mesh(new THREE.BoxGeometry(0.06, 0.04, 2.2), bodyMat);
    fw.position.set(3.0, 0.04, 0);
    g.add(fw);
    // Front wing end plates
    [-1.08, 1.08].forEach(z => {
        const ep = new THREE.Mesh(new THREE.BoxGeometry(0.3, 0.14, 0.04), bodyMat);
        ep.position.set(2.95, 0.08, z);
        g.add(ep);
    });

    // REAR WING
    const rwMain = new THREE.Mesh(new THREE.BoxGeometry(0.06, 0.06, 1.6), bodyMat);
    rwMain.position.set(-2.0, 0.7, 0);
    g.add(rwMain);
    const rwDRS = new THREE.Mesh(new THREE.BoxGeometry(0.04, 0.06, 1.5), bodyMat);
    rwDRS.position.set(-2.0, 0.78, 0);
    g.add(rwDRS);
    // Rear wing pillars
    [-0.7, 0.7].forEach(z => {
        const rp = new THREE.Mesh(new THREE.BoxGeometry(0.06, 0.55, 0.04), bodyMat);
        rp.position.set(-1.95, 0.45, z);
        g.add(rp);
    });

    // Sidepods
    [-0.45, 0.45].forEach(z => {
        const sp = new THREE.Mesh(new THREE.BoxGeometry(1.8, 0.22, 0.28), bodyMat);
        sp.position.set(-0.2, 0.18, z);
        g.add(sp);
    });

    // F1 WHEELS (wide front / wider rear)
    const fwPos = [[1.5, 0, 0.72], [1.5, 0, -0.72]];
    fwPos.forEach(([x, y, z]) => {
        const w = makeWheel(tireMat, rimMat, redMat, 0.33, 0.22);
        w.position.set(x, y, z);
        g.add(w);
    });
    const rwPos = [[-1.5, 0, 0.8], [-1.5, 0, -0.8]];
    rwPos.forEach(([x, y, z]) => {
        const w = makeWheel(tireMat, rimMat, redMat, 0.38, 0.3);
        w.position.set(x, y, z);
        g.add(w);
    });

    // Exhaust (side pod exit)
    const exMat = new THREE.MeshStandardMaterial({ color: 0x555555, metalness: 0.9, roughness: 0.1 });
    const ex = new THREE.Mesh(new THREE.TorusGeometry(0.06, 0.02, 8, 12), exMat);
    ex.rotation.y = Math.PI / 2;
    ex.position.set(-1.2, 0.28, 0.5);
    g.add(ex);

    g.position.y = 0.33;
}

/* ─── CLASSIC ─── */
function buildClassic(g, bodyMat, glassMat, tireMat, rimMat, redMat) {
    // Upright rounded body
    const body = new THREE.Mesh(new THREE.BoxGeometry(4.2, 0.58, 1.8), bodyMat);
    body.position.y = 0.44;
    g.add(body);

    // Rounded cabin
    const cab = new THREE.Mesh(new THREE.BoxGeometry(2.0, 0.52, 1.65), bodyMat);
    cab.position.set(-0.1, 0.86, 0);
    g.add(cab);

    // Long front wings (fenders)
    [-0.9, 0.9].forEach(z => {
        const fw = new THREE.Mesh(new THREE.BoxGeometry(1.8, 0.35, 0.3), bodyMat);
        fw.position.set(1.1, 0.38, z);
        g.add(fw);
    });
    // Long rear wings
    [-0.9, 0.9].forEach(z => {
        const rw = new THREE.Mesh(new THREE.BoxGeometry(1.6, 0.35, 0.3), bodyMat);
        rw.position.set(-1.0, 0.38, z);
        g.add(rw);
    });

    // Windshield (upright)
    const ws = new THREE.Mesh(new THREE.BoxGeometry(0.04, 0.46, 1.55), glassMat);
    ws.rotation.z = -0.18;
    ws.position.set(0.85, 0.86, 0);
    g.add(ws);

    // Rear window
    const rw2 = new THREE.Mesh(new THREE.BoxGeometry(0.04, 0.46, 1.5), glassMat);
    rw2.rotation.z = 0.18;
    rw2.position.set(-0.95, 0.86, 0);
    g.add(rw2);

    // Round headlights
    const hlMat = new THREE.MeshStandardMaterial({ color: 0xffffcc, emissive: 0xffffaa, emissiveIntensity: 0.6 });
    [-0.6, 0.6].forEach(z => {
        const hl = new THREE.Mesh(new THREE.CylinderGeometry(0.14, 0.14, 0.12, 12), hlMat);
        hl.rotation.z = Math.PI / 2;
        hl.position.set(2.15, 0.48, z);
        g.add(hl);
    });

    // Round taillights
    [-0.6, 0.6].forEach(z => {
        const tl = new THREE.Mesh(new THREE.CylinderGeometry(0.1, 0.1, 0.1, 10), redMat);
        tl.rotation.z = Math.PI / 2;
        tl.position.set(-2.14, 0.48, z);
        g.add(tl);
    });

    // Classic chrome bumpers
    const bumpMat = new THREE.MeshStandardMaterial({ color: 0xcccccc, metalness: 0.95, roughness: 0.05 });
    [2.16, -2.16].forEach(x => {
        const bump = new THREE.Mesh(new THREE.BoxGeometry(0.06, 0.1, 1.7), bumpMat);
        bump.position.set(x, 0.3, 0);
        g.add(bump);
    });

    // Wheels with wire rims
    const wireMat = new THREE.MeshStandardMaterial({ color: 0xdddddd, metalness: 0.9, roughness: 0.1 });
    const positions = [[1.3, 0, 0.95], [1.3, 0, -0.95], [-1.25, 0, 0.95], [-1.25, 0, -0.95]];
    positions.forEach(([x, y, z]) => {
        const w = makeWheel(tireMat, wireMat, redMat, 0.42, 0.18);
        w.position.set(x, y, z);
        g.add(w);
    });

    g.position.y = 0.42;
}

/* ========================
   MAIN VIEWER INIT
   ======================== */
(function () {
    const CONTAINER_ID = 'car-360-viewport';

    function init() {
        const container = document.getElementById(CONTAINER_ID);
        if (!container || typeof THREE === 'undefined') return;

        const W = container.offsetWidth || window.innerWidth;
        const H = container.offsetHeight || window.innerHeight;

        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x05070a);
        scene.fog = new THREE.Fog(0x05070a, 18, 35);

        const camera = new THREE.PerspectiveCamera(42, W / H, 0.1, 100);
        camera.position.set(0, 1.8, 7.5);

        const renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
        renderer.setSize(W, H);
        renderer.shadowMap.enabled = true;
        renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        renderer.toneMapping = THREE.ACESFilmicToneMapping;
        renderer.toneMappingExposure = 1.3;
        container.appendChild(renderer.domElement);

        // ── Lights ──
        scene.add(new THREE.AmbientLight(0x404060, 0.5));

        const keyLight = new THREE.DirectionalLight(0xffffff, 2.5);
        keyLight.position.set(5, 8, 4);
        keyLight.castShadow = true;
        keyLight.shadow.mapSize.set(1024, 1024);
        scene.add(keyLight);

        const rimLight = new THREE.DirectionalLight(0xe83a3a, 1.2);
        rimLight.position.set(-5, 2, -4);
        scene.add(rimLight);

        const fillLight = new THREE.PointLight(0x4488ff, 0.6, 20);
        fillLight.position.set(0, 4, 6);
        scene.add(fillLight);

        const groundLight = new THREE.PointLight(0xff6600, 0.3, 8);
        groundLight.position.set(0, 0, 0);
        scene.add(groundLight);

        // ── Reflective floor ──
        const floorMat = new THREE.MeshStandardMaterial({
            color: 0x080a10, metalness: 0.85, roughness: 0.35
        });
        const floor = new THREE.Mesh(new THREE.PlaneGeometry(30, 20), floorMat);
        floor.rotation.x = -Math.PI / 2;
        floor.position.y = 0;
        floor.receiveShadow = true;
        scene.add(floor);

        // ── Grid ──
        const grid = new THREE.GridHelper(30, 40, 0xe83a3a, 0x1a2030);
        grid.position.y = 0.002;
        grid.material.opacity = 0.18;
        grid.material.transparent = true;
        scene.add(grid);

        // ── Spark particles ──
        const sparkN = 180;
        const sparkPos = new Float32Array(sparkN * 3);
        const sparkCol = new Float32Array(sparkN * 3);
        const sparkSpd = new Float32Array(sparkN);
        for (let i = 0; i < sparkN; i++) {
            sparkPos[i * 3] = (Math.random() - 0.5) * 14;
            sparkPos[i * 3 + 1] = Math.random() * 3;
            sparkPos[i * 3 + 2] = (Math.random() - 0.5) * 8;
            sparkCol[i * 3] = 1;
            sparkCol[i * 3 + 1] = Math.random() * 0.4;
            sparkCol[i * 3 + 2] = 0;
            sparkSpd[i] = 0.008 + Math.random() * 0.016;
        }
        const sparkGeo = new THREE.BufferGeometry();
        sparkGeo.setAttribute('position', new THREE.BufferAttribute(sparkPos, 3));
        sparkGeo.setAttribute('color', new THREE.BufferAttribute(sparkCol, 3));
        const sparkMesh = new THREE.Points(sparkGeo,
            new THREE.PointsMaterial({ size: 0.04, vertexColors: true, transparent: true, opacity: 0.45 })
        );
        scene.add(sparkMesh);

        // ── Car ──
        const brand = (window.CAR_BRAND || '').toLowerCase();
        const category = (window.CAR_CATEGORY || '').toLowerCase();
        const archetype = getArchetype(brand, category);
        const color = getBrandColor(brand);
        let carGroup = null;

        // Try GLTF first, fall back to procedural
        if (GLTF_MODELS[archetype] && typeof THREE.GLTFLoader !== 'undefined') {
            const loader = new THREE.GLTFLoader();
            loader.load(
                GLTF_MODELS[archetype],
                (gltf) => {
                    const model = gltf.scene;

                    // Apply brand color to paintwork meshes
                    model.traverse(child => {
                        if (child.isMesh) {
                            child.castShadow = true;
                            child.receiveShadow = true;
                            // The Three.js ferrari model has specific mesh names
                            if (child.name === 'body_Mesh' || child.name.includes('body')) {
                                child.material = new THREE.MeshStandardMaterial({
                                    color: new THREE.Color(color),
                                    metalness: 0.8, roughness: 0.2
                                });
                            }
                        }
                    });

                    // Scale and center
                    const box = new THREE.Box3().setFromObject(model);
                    const size = box.getSize(new THREE.Vector3());
                    const centerY = box.getCenter(new THREE.Vector3()).y;
                    const scale = 4.0 / Math.max(size.x, size.y, size.z);
                    model.scale.setScalar(scale);
                    model.position.y = -centerY * scale;

                    carGroup = model;
                    scene.add(carGroup);
                    document.getElementById('car-360-hint')?.style.setProperty('display', 'flex');
                },
                undefined,
                () => { fallbackToProcedural(); }
            );
        } else {
            fallbackToProcedural();
        }

        function fallbackToProcedural() {
            carGroup = buildProceduralCar(archetype, color);
            scene.add(carGroup);
            document.getElementById('car-360-hint')?.style.setProperty('display', 'flex');
        }

        // ── Orbit controls ──
        let isDragging = false;
        let rotX = 0.12, rotY = 0;
        let velX = 0, velY = 0;
        let prevX = 0, prevY = 0;
        let radius = 7.5;

        function getXY(e) {
            if (e.touches) return { x: e.touches[0].clientX, y: e.touches[0].clientY };
            return { x: e.clientX, y: e.clientY };
        }
        function onDown(e) { isDragging = true; const p = getXY(e); prevX = p.x; prevY = p.y; velX = velY = 0; }
        function onMove(e) {
            if (!isDragging) return;
            e.preventDefault();
            const p = getXY(e);
            const dx = p.x - prevX, dy = p.y - prevY;
            velY = dx * 0.009; velX = dy * 0.006;
            rotY += velY; rotX += velX;
            rotX = Math.max(-0.55, Math.min(0.55, rotX));
            prevX = p.x; prevY = p.y;
        }
        function onUp() { isDragging = false; }

        container.addEventListener('wheel', e => {
            e.preventDefault();
            radius = Math.max(3, Math.min(14, radius + e.deltaY * 0.006));
        }, { passive: false });

        renderer.domElement.addEventListener('mousedown', onDown);
        window.addEventListener('mousemove', onMove);
        window.addEventListener('mouseup', onUp);
        renderer.domElement.addEventListener('touchstart', onDown, { passive: true });
        renderer.domElement.addEventListener('touchmove', onMove, { passive: false });
        renderer.domElement.addEventListener('touchend', onUp);

        // Clear hint on first drag
        renderer.domElement.addEventListener('mousedown', () => {
            const hint = document.getElementById('car-360-hint');
            if (hint) { hint.style.opacity = '0'; hint.style.pointerEvents = 'none'; }
        }, { once: true });

        let lastT = 0;
        function animate(t) {
            requestAnimationFrame(animate);
            if (t - lastT < 14) return; lastT = t;

            if (!isDragging) {
                velX *= 0.90; velY *= 0.90;
                rotX += velX; rotY += velY;
                rotY += 0.003; // auto rotate
                rotX = Math.max(-0.55, Math.min(0.55, rotX));
            }

            const camX = Math.sin(rotY) * Math.cos(rotX) * radius;
            const camY = Math.sin(rotX) * radius + 1.2;
            const camZ = Math.cos(rotY) * Math.cos(rotX) * radius;
            camera.position.set(camX, camY, camZ);
            camera.lookAt(0, 0.6, 0);

            // Update sparks
            const sp = sparkGeo.attributes.position.array;
            for (let i = 0; i < sparkN; i++) {
                sp[i * 3 + 1] += sparkSpd[i];
                if (sp[i * 3 + 1] > 4) sp[i * 3 + 1] = 0;
            }
            sparkGeo.attributes.position.needsUpdate = true;

            renderer.render(scene, camera);
        }
        animate(0);

        window.addEventListener('resize', () => {
            const nW = container.offsetWidth, nH = container.offsetHeight;
            camera.aspect = nW / nH;
            camera.updateProjectionMatrix();
            renderer.setSize(nW, nH);
        });
    }

    document.addEventListener('DOMContentLoaded', init);
})();
