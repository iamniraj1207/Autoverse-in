/**
 * cinematic_hero.js — AutoVerse Pagani-Style Reveal Orchestration
 * Handles: Headlight beam ignition and Three.js environmental particles
 */
(function () {
    'use strict';

    window.AutoVerse = window.AutoVerse || {};
    window.AutoVerse.canRun3D = function () {
        try {
            const canvas = document.createElement('canvas');
            const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
            return !!gl;
        } catch (e) {
            return false;
        }
    };

    /* ─── LAYER 7 — HEADLIGHT BEAM IGNITION ─── */
    function initHeadlightBeams() {
        // Fire after car reveal completes (approx 4s)
        setTimeout(() => {
            const beams = document.getElementById('headlight-beams');
            if (beams) beams.classList.add('ignited');
        }, 4200);
    }

    /* ─── THREE.JS PARTICLE BURST — ATMOSPHERIC SPARKS ─── */
    function initParticleBurst() {
        if (!window.AutoVerse.canRun3D() || typeof THREE === 'undefined') return;

        setTimeout(() => {
            const canvas = document.getElementById('hero-particles-canvas');
            if (!canvas) return;

            const scene = new THREE.Scene();
            const cam = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 50);
            cam.position.set(0, 0, 5);

            const renderer = new THREE.WebGLRenderer({
                canvas, alpha: true, antialias: false,
                powerPreference: 'low-power'
            });
            renderer.setSize(window.innerWidth, window.innerHeight);
            renderer.setPixelRatio(Math.min(devicePixelRatio, 1.2));
            renderer.setClearColor(0x000000, 0);

            const count = 400;
            const pos = new Float32Array(count * 3);
            const vel = new Float32Array(count * 3);
            const col = new Float32Array(count * 3);
            const life = new Float32Array(count);

            function spawnParticle(i) {
                const i3 = i * 3;
                // Scatter sparks mostly on the floor behind the car
                pos[i3] = (Math.random() - 0.5) * 8;
                pos[i3 + 1] = -1.5 + (Math.random() - 0.5) * 0.2;
                pos[i3 + 2] = (Math.random() - 0.5) * 4;

                vel[i3] = (Math.random() - 0.5) * 0.01;
                vel[i3 + 1] = Math.random() * 0.015;
                vel[i3 + 2] = (Math.random() - 0.5) * 0.01;

                const t = Math.random();
                col[i3] = 1;
                col[i3 + 1] = t > 0.6 ? 0.6 : t * 0.4;
                col[i3 + 2] = t > 0.8 ? 0.2 : 0.0;

                life[i] = Math.random() * 150 + 50;
            }

            for (let i = 0; i < count; i++) spawnParticle(i);

            const geo = new THREE.BufferGeometry();
            const posAttr = new THREE.BufferAttribute(pos, 3);
            const colAttr = new THREE.BufferAttribute(col, 3);
            geo.setAttribute('position', posAttr);
            geo.setAttribute('color', colAttr);

            const mat = new THREE.PointsMaterial({
                size: 0.015, vertexColors: true,
                transparent: true, opacity: 0.6,
                sizeAttenuation: true, depthWrite: false
            });

            scene.add(new THREE.Points(geo, mat));

            let frame = 0;
            let rafId;

            function tick() {
                rafId = requestAnimationFrame(tick);
                frame++;

                for (let i = 0; i < count; i++) {
                    const i3 = i * 3;
                    life[i]--;

                    if (life[i] <= 0) {
                        spawnParticle(i);
                    }

                    pos[i3] += vel[i3];
                    pos[i3 + 1] += vel[i3 + 1];
                    pos[i3 + 2] += vel[i3 + 2];

                    vel[i3 + 1] *= 0.99; // Air resistance
                }

                posAttr.needsUpdate = true;
                colAttr.needsUpdate = true;
                renderer.render(scene, cam);
            }

            tick();

            window.addEventListener('resize', () => {
                cam.aspect = window.innerWidth / window.innerHeight;
                cam.updateProjectionMatrix();
                renderer.setSize(window.innerWidth, window.innerHeight);
            });

        }, 3000); // Start sparks after initial reveal burst
    }

    function init() {
        initHeadlightBeams();
        initParticleBurst();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
