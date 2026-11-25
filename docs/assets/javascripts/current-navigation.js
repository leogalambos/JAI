// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
// Keep the current entry visible by scrolling only the primary navigation.
(() => {
  const panel = document.querySelector(".md-sidebar--primary .md-sidebar__scrollwrap");
  if (!panel) return;

  let current = panel.querySelector("a.md-nav__link--active");
  const profileParent = document.querySelector("a.ai-current-profile-parent");

  // Generated profiles are reached through the chapter index. Give the open
  // profile its own sidebar entry without listing every profile on every page.
  if (!current && profileParent) {
    const parentLink = [...panel.querySelectorAll(".md-nav a.md-nav__link")]
      .find(link => link.href === profileParent.href);
    const heading = document.querySelector("article h1");
    if (parentLink && heading) {
      const parentItem = parentLink.closest("li.md-nav__item");
      const item = document.createElement("li");
      item.className = "md-nav__item md-nav__item--active";
      current = document.createElement("a");
      current.className = "md-nav__link md-nav__link--active";
      current.href = location.pathname;
      current.textContent = heading.textContent.replace(/\s*¶\s*$/, "").trim();
      item.append(current);
      parentItem.after(item);

      for (let section = parentItem.parentElement; section && section !== panel;
        section = section.parentElement) {
        if (!section.matches("li.md-nav__item--nested")) continue;
        const toggle = section.querySelector(":scope > input.md-nav__toggle");
        if (toggle) {
          toggle.classList.add("ai-nav-current-ancestor");
          toggle.checked = true;
        }
        section.classList.add("md-nav__item--active");
        section.querySelector(":scope > nav")?.setAttribute("aria-expanded", "true");
      }
    }
  }

  if (!current) return;
  current.setAttribute("aria-current", "page");

  function revealCurrent() {
    let viewportElement = panel;
    for (let ancestor = current.parentElement; ancestor && ancestor !== panel;
      ancestor = ancestor.parentElement) {
      if (["auto", "scroll"].includes(getComputedStyle(ancestor).overflowY)) {
        viewportElement = ancestor;
        break;
      }
    }
    const viewport = viewportElement.getBoundingClientRect();
    const entry = current.getBoundingClientRect();
    if (!viewport.height || !entry.height) return;
    if (entry.top >= viewport.top + 8 && entry.bottom <= viewport.bottom - 8) return;
    viewportElement.scrollTop += (entry.top + entry.bottom - viewport.top - viewport.bottom) / 2;
  }

  const align = () => requestAnimationFrame(() => requestAnimationFrame(revealCurrent));
  window.addEventListener("pageshow", align);
  document.querySelector("#__drawer")?.addEventListener("change", event => {
    if (event.target.checked) align();
  });
  revealCurrent();
  align();
})();
