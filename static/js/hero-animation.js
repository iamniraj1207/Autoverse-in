/**
 * hero-animation.js — AutoVerse
 * Simplified video management for cinematic backgrounds.
 */
document.addEventListener('DOMContentLoaded', () => {
    const video = document.getElementById('hero-video');
    if (!video) return;

    // Ensure playback continuity
    video.play().catch(error => {
        console.log("Autoplay check:", error);
    });
});
