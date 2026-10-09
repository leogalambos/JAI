(() => {
  function initHomeFooterReveal() {
    const anchor = document.querySelector('.ai-home-footer-anchor-v31');
    if (!anchor || anchor.dataset.footerRevealInit === '1') return;
    anchor.dataset.footerRevealInit = '1';
    let ticking = false;
    const update = () => {
      ticking = false;
      const rect = anchor.getBoundingClientRect();
      // Keep the footer in normal flow until its own anchor reaches the viewport.
      // From that point to the document end, pin it to the lower viewport edge.
      const reached = rect.top < window.innerHeight;
      anchor.classList.toggle('is-pinned', reached);
    };
    const schedule = () => {
      if (!ticking) {
        ticking = true;
        requestAnimationFrame(update);
      }
    };
    window.addEventListener('scroll', schedule, { passive: true });
    window.addEventListener('resize', schedule, { passive: true });
    update();
  }
  if (typeof document$ !== 'undefined' && document$.subscribe) {
    document$.subscribe(initHomeFooterReveal);
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initHomeFooterReveal, { once: true });
  } else {
    initHomeFooterReveal();
  }
})();
