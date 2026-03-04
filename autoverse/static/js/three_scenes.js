/**
 * AutoVerse Three.js Scenes
 * Premium Particle Backgrounds
 */

class AutoVerseThree {
    constructor(canvasId, type) {
        this.canvas = document.getElementById(canvasId);
        if (!this.canvas) return;

        this.type = type;
        this.scene = new THREE.Scene();
        this.camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        this.renderer = new THREE.WebGLRenderer({
            canvas: this.canvas,
            alpha: true,
            antialias: true
        });

        this.renderer.setSize(window.innerWidth, window.innerHeight);
        this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

        this.particles = null;
        this.init();
        this.animate();

        window.addEventListener('resize', () => this.onWindowResize());
        document.addEventListener('visibilitychange', () => this.handleVisibilityChange());
    }

    init() {
        const geometry = new THREE.BufferGeometry();
        const count = this.type === 'home' ? 3000 : 2000;
        const positions = new Float32Array(count * 3);

        for (let i = 0; i < count * 3; i++) {
            positions[i] = (Math.random() - 0.5) * 15;
        }

        geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));

        const color = this.type === 'academy' ? 0x1abc9c : 0xe83a3a;
        const material = new THREE.PointsMaterial({
            color: color,
            size: 0.02,
            transparent: true,
            opacity: 0.6,
            blending: THREE.AdditiveBlending
        });

        this.particles = new THREE.Points(geometry, material);
        this.scene.add(this.particles);

        this.camera.position.z = 5;
    }

    onWindowResize() {
        this.camera.aspect = window.innerWidth / window.innerHeight;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(window.innerWidth, window.innerHeight);
    }

    handleVisibilityChange() {
        if (document.hidden) {
            this.paused = true;
        } else {
            this.paused = false;
        }
    }

    animate() {
        if (this.paused) {
            requestAnimationFrame(() => this.animate());
            return;
        }

        requestAnimationFrame(() => this.animate());

        if (this.particles) {
            if (this.type === 'home') {
                this.particles.rotation.y += 0.0005;
                this.particles.rotation.x += 0.0002;
            } else if (this.type === 'academy') {
                this.particles.rotation.y += 0.001;
            } else {
                // Blur effect
                const positions = this.particles.geometry.attributes.position.array;
                for (let i = 0; i < positions.length; i += 3) {
                    positions[i] += 0.02; // Move X
                    if (positions[i] > 10) positions[i] = -10;
                }
                this.particles.geometry.attributes.position.needsUpdate = true;
            }
        }

        this.renderer.render(this.scene, this.camera);
    }
}

// Initialize on Load
document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('homepage-hero-canvas')) {
        new AutoVerseThree('homepage-hero-canvas', 'home');
    }
    if (document.getElementById('academy-particles')) {
        new AutoVerseThree('academy-particles', 'academy');
    }
    if (document.getElementById('car-detail-particles')) {
        new AutoVerseThree('car-detail-particles', 'detail');
    }
});
