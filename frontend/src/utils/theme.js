// src/utils/theme.js
const STORAGE_KEY = "theme"; // "light" | "dark"

export function getStoredTheme() {
  return localStorage.getItem(STORAGE_KEY);
}

export function applyTheme(next) {
  const root = document.documentElement;
  // ativa transição global rapidinha
  root.classList.add("theme-switching");

  root.classList.toggle("dark", next === "dark");
  localStorage.setItem("theme", next);

  // remove depois de ~250ms
  window.setTimeout(() => {
    root.classList.remove("theme-switching");
  }, 250);
}

export function initTheme() {
  const saved = getStoredTheme();
  const prefersDark = window.matchMedia?.("(prefers-color-scheme: dark)").matches;
  applyTheme(saved ?? (prefersDark ? "dark" : "light"));
}
