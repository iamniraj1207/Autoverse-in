(function () {
    const scene = document.getElementById('car-scene');
    const motionLines = document.getElementById('motion-lines');
    if (!scene || !motionLines) return;

    // Create motion lines periodically while car animates
    let lineInterval;

    function createMotionLine() {
        const line = document.createElement('div');
        line.className = 'motion-line';
        // Random vertical position near car height
        line.style.bottom = (20 + Math.random() * 60) + 'px';
        line.style.right = (Math.random() * 40 + 5) + '%';
        line.style.width = (60 + Math.random() * 140) + 'px';
        motionLines.appendChild(line);
        setTimeout(() => line.remove(), 800);
    }

    // Only run when car animation is active
    // Car animation is 12s cycle
    function startLines() {
        lineInterval = setInterval(createMotionLine, 120);
    }

    startLines();

    // Pause on tab hidden
    document.addEventListener('visibilitychange', () => {
        if (document.hidden) {
            clearInterval(lineInterval);
        } else {
            startLines();
        }
    });
})();
