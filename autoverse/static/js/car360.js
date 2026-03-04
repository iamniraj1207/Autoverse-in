/**
 * car360.js  — Interactive 360° car viewer using Three.js
 * Renders a real-time 3D camera orbit around the car image
 * mapped onto a plane, with full mouse drag + touch support.
 */
(function () {
    'use strict';

    const CONTAINER_ID = 'car-360-viewport';

    function init() {
        const container = document.getElementById(CONTAINER_ID);
        if (!container || typeof THREE === 'undefined') return;

        const W = container.offsetWidth;
        const H = container.offsetHeight;

        /* ── Scene ── */
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x05070a);

        const camera = new THREE.PerspectiveCamera(45, W / H, 0.1, 100);
        camera.position.set(0, 0.6, 3.8);

        const renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
        renderer.setSize(W, H);
        renderer.shadowMap.enabled = true;
        container.appendChild(renderer.domElement);

        /* ── Lights ── */
        scene.add(new THREE.AmbientLight(0xffffff, 0.4));

        const keyLight = new THREE.DirectionalLight(0xffffff, 1.2);
        keyLight.position.set(4, 6, 4);
        keyLight.castShadow = true;
        scene.add(keyLight);

        const rimLight = new THREE.DirectionalLight(0xe83a3a, 0.6);
        rimLight.position.set(-4, 2, -3);
        scene.add(rimLight);

        const fillLight = new THREE.DirectionalLight(0x4488ff, 0.3);
        fillLight.position.set(0, -2, 4);
        scene.add(fillLight);

        /* ── Reflective ground plane ── */
        const groundGeo = new THREE.PlaneGeometry(12, 8);
        const groundMat = new THREE.MeshStandardMaterial({
            color: 0x080a10, metalness: 0.8, roughness: 0.4
        });
        const ground = new THREE.Mesh(groundGeo, groundMat);
        ground.rotation.x = -Math.PI / 2;
        ground.position.y = -0.8;
        ground.receiveShadow = true;
        scene.add(ground);

        /* ── Grid overlay on ground ── */
        const grid = new THREE.GridHelper(12, 24, 0xe83a3a, 0x1e2535);
        grid.position.y = -0.79;
        grid.material.opacity = 0.25;
        grid.material.transparent = true;
        scene.add(grid);

        /* ── Load car image as textured plane OR show 3D box geometry ── */
        const imgSrc = window.CAR_IMAGE_EXTERIOR || null;
        const loader = new THREE.TextureLoader();

        let carMesh;

        function buildCarPlane(texture) {
            /* Fit texture aspect ratio */
            const aspect = texture ? (texture.image.width / texture.image.height) : (16 / 9);
            const planeH = 1.4;
            const planeW = planeH * aspect;

            const geo = new THREE.PlaneGeometry(planeW, planeH, 1, 1);
            const mat = texture
                ? new THREE.MeshStandardMaterial({ map: texture, transparent: true, metalness: 0.1, roughness: 0.6 })
                : new THREE.MeshStandardMaterial({ color: 0x1a1a2e, metalness: 0.5, roughness: 0.4 });

            carMesh = new THREE.Mesh(geo, mat);
            carMesh.castShadow = true;
            carMesh.position.y = -0.05;
            scene.add(carMesh);
        }

        if (imgSrc) {
            loader.load(imgSrc, tex => buildCarPlane(tex), undefined, () => buildCarPlane(null));
        } else {
            buildCarPlane(null);
        }

        /* ── Particle sparks (exhaust) ── */
        const sparkN = 300;
        const sparkPos = new Float32Array(sparkN * 3);
        const sparkCol = new Float32Array(sparkN * 3);
        for (let i = 0; i < sparkN; i++) {
            sparkPos[i * 3] = (Math.random() - 0.5) * 6;
            sparkPos[i * 3 + 1] = (Math.random() - 0.5) * 4;
            sparkPos[i * 3 + 2] = (Math.random() - 0.5) * 3;
            sparkCol[i * 3] = 1;
            sparkCol[i * 3 + 1] = Math.random() * 0.4;
            sparkCol[i * 3 + 2] = 0;
        }
        const sparkGeo = new THREE.BufferGeometry();
        sparkGeo.setAttribute('position', new THREE.BufferAttribute(sparkPos, 3));
        sparkGeo.setAttribute('color', new THREE.BufferAttribute(sparkCol, 3));
        const sparkMat = new THREE.PointsMaterial({ size: 0.025, vertexColors: true, transparent: true, opacity: 0.35 });
        const sparks = new THREE.Points(sparkGeo, sparkMat);
        scene.add(sparks);

        /* ── Orbit state ── */
        let isDragging = false;
        let prevX = 0, prevY = 0;
        let rotX = 0, rotY = 0;  // current rotation angles
        let velX = 0, velY = 0;  // inertia velocities
        let radius = 3.8;

        function getXY(e) {
            if (e.touches) return { x: e.touches[0].clientX, y: e.touches[0].clientY };
            return { x: e.clientX, y: e.clientY };
        }

        function onDown(e) {
            isDragging = true;
            const p = getXY(e);
            prevX = p.x; prevY = p.y;
            velX = 0; velY = 0;
        }
        function onMove(e) {
            if (!isDragging) return;
            e.preventDefault();
            const p = getXY(e);
            const dx = p.x - prevX;
            const dy = p.y - prevY;
            rotY += dx * 0.008;
            rotX += dy * 0.005;
            rotX = Math.max(-0.6, Math.min(0.6, rotX));
            velX = dy * 0.005;
            velY = dx * 0.008;
            prevX = p.x; prevY = p.y;
        }
        function onUp() { isDragging = false; }

        // Wheel zoom
        container.addEventListener('wheel', e => {
            e.preventDefault();
            radius = Math.max(1.8, Math.min(7, radius + e.deltaY * 0.005));
        }, { passive: false });

        renderer.domElement.addEventListener('mousedown', onDown);
        window.addEventListener('mousemove', onMove);
        window.addEventListener('mouseup', onUp);
        renderer.domElement.addEventListener('touchstart', onDown, { passive: true });
        renderer.domElement.addEventListener('touchmove', onMove, { passive: false });
        renderer.domElement.addEventListener('touchend', onUp);

        /* ── Render loop ── */
        let last = 0;
        function animate(t) {
            requestAnimationFrame(animate);
            if (t - last < 16) return; last = t;

            if (!isDragging) {
                velX *= 0.92;
                velY *= 0.92;
                rotX += velX;
                rotY += velY;
                // Slow auto-rotate when idle
                rotY += 0.003;
                rotX = Math.max(-0.6, Math.min(0.6, rotX));
            }

            // Orbit camera
            const camX = Math.sin(rotY) * Math.cos(rotX) * radius;
            const camY = Math.sin(rotX) * radius + 0.6;
            const camZ = Math.cos(rotY) * Math.cos(rotX) * radius;
            camera.position.set(camX, camY, camZ);
            camera.lookAt(0, 0, 0);

            // Spark drift
            const sp = sparkGeo.attributes.position.array;
            for (let i = 0; i < sparkN; i++) {
                sp[i * 3 + 1] += 0.006;
                if (sp[i * 3 + 1] > 2.5) sp[i * 3 + 1] = -2;
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

        /* ── Hint overlay ── */
        const hint = document.getElementById('car-360-hint');
        renderer.domElement.addEventListener('mousedown', () => {
            if (hint) { hint.style.opacity = '0'; hint.style.pointerEvents = 'none'; }
        }, { once: true });
    }

    document.addEventListener('DOMContentLoaded', init);
})();
