(function () {
  "use strict";

  const root = document.documentElement;
  const loader = document.getElementById("pageLoader");
  const navbar = document.getElementById("siteNavbar");
  const backToTop = document.getElementById("backToTop");
  const toastEl = document.getElementById("appToast");
  const toast = toastEl && window.bootstrap ? new bootstrap.Toast(toastEl) : null;

  const savedTheme = localStorage.getItem("learnhub-theme");
  if (savedTheme) root.setAttribute("data-theme", savedTheme);

  window.addEventListener("load", () => {
    loader?.classList.add("loaded");
    if (window.AOS) AOS.init({ duration: 700, once: true, offset: 80 });
  });

  const syncChrome = () => {
    navbar?.classList.toggle("nav-scrolled", window.scrollY > 12);
    backToTop?.classList.toggle("show", window.scrollY > 420);
  };
  syncChrome();
  window.addEventListener("scroll", syncChrome, { passive: true });

  document.getElementById("themeToggle")?.addEventListener("click", function () {
    const next = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
    root.setAttribute("data-theme", next);
    localStorage.setItem("learnhub-theme", next);
    this.innerHTML = next === "dark" ? '<i class="fa-solid fa-sun"></i>' : '<i class="fa-solid fa-moon"></i>';
  });

  backToTop?.addEventListener("click", () => window.scrollTo({ top: 0, behavior: "smooth" }));

  document.querySelectorAll(".btn-ripple").forEach((button) => {
    button.addEventListener("click", (event) => {
      const circle = document.createElement("span");
      const rect = button.getBoundingClientRect();
      circle.className = "ripple";
      circle.style.left = `${event.clientX - rect.left}px`;
      circle.style.top = `${event.clientY - rect.top}px`;
      button.appendChild(circle);
      window.setTimeout(() => circle.remove(), 600);
    });
  });

  document.querySelectorAll(".needs-validation").forEach((form) => {
    form.addEventListener("submit", (event) => {
      if (!form.checkValidity()) {
        event.preventDefault();
        event.stopPropagation();
      } else if (!form.hasAttribute("data-server-submit") && (!form.action || form.action === window.location.href)) {
        event.preventDefault();
        form.querySelector(".form-success")?.classList.remove("d-none");
        showToast("Form validated successfully.");
      }
      form.classList.add("was-validated");
    });
  });

  document.querySelectorAll(".password-toggle").forEach((toggle) => {
    toggle.addEventListener("click", () => {
      const input = toggle.closest(".password-field")?.querySelector("input");
      if (!input) return;
      const showing = input.type === "text";
      input.type = showing ? "password" : "text";
      toggle.innerHTML = showing ? '<i class="fa-regular fa-eye"></i>' : '<i class="fa-regular fa-eye-slash"></i>';
    });
  });

  document.querySelectorAll(".password-strength-input").forEach((input) => {
    input.addEventListener("input", () => {
      const wrap = input.closest(".col-12, form")?.querySelector(".password-strength span") || document.querySelector(".password-strength span");
      if (!wrap) return;
      const score = [
        input.value.length >= 8,
        /[A-Z]/.test(input.value),
        /[0-9]/.test(input.value),
        /[^A-Za-z0-9]/.test(input.value)
      ].filter(Boolean).length;
      const widths = ["12%", "35%", "60%", "82%", "100%"];
      const colors = ["#ef4444", "#f97316", "#f59e0b", "#14b8a6", "#22c55e"];
      wrap.style.width = widths[score];
      wrap.style.background = colors[score];
    });
  });

  document.querySelectorAll("[data-otp] input").forEach((input, index, inputs) => {
    input.addEventListener("input", () => {
      input.value = input.value.replace(/\D/g, "");
      if (input.value && inputs[index + 1]) inputs[index + 1].focus();
    });
    input.addEventListener("keydown", (event) => {
      if (event.key === "Backspace" && !input.value && inputs[index - 1]) inputs[index - 1].focus();
    });
  });

  const counters = document.querySelectorAll(".counter");
  if (counters.length) {
    const runCounter = (counter) => {
      const target = Number(counter.dataset.count || 0);
      let current = 0;
      const step = Math.max(1, Math.ceil(target / 70));
      const timer = window.setInterval(() => {
        current += step;
        if (current >= target) {
          current = target;
          window.clearInterval(timer);
        }
        counter.textContent = current.toLocaleString();
      }, 18);
    };
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting && !entry.target.dataset.done) {
          entry.target.dataset.done = "true";
          runCounter(entry.target);
        }
      });
    }, { threshold: .45 });
    counters.forEach((counter) => observer.observe(counter));
  }

  const typingText = document.getElementById("typingText");
  if (typingText) {
    const words = ["expert-led courses", "hands-on projects", "career-ready skills"];
    let wordIndex = 0;
    let charIndex = 0;
    let deleting = false;
    const type = () => {
      const word = words[wordIndex];
      typingText.textContent = deleting ? word.slice(0, charIndex--) : word.slice(0, charIndex++);
      if (!deleting && charIndex > word.length + 6) deleting = true;
      if (deleting && charIndex < 0) {
        deleting = false;
        wordIndex = (wordIndex + 1) % words.length;
      }
      window.setTimeout(type, deleting ? 60 : 95);
    };
    type();
  }

  const filterButtons = document.querySelectorAll("[data-filter]");
  const courseSearch = document.getElementById("courseSearch");
  const applyCourseFilters = () => {
    const active = document.querySelector("[data-filter].active")?.dataset.filter || "all";
    const query = (courseSearch?.value || "").toLowerCase().trim();
    document.querySelectorAll("[data-course-card]").forEach((card) => {
      const categoryMatch = active === "all" || card.dataset.category === active;
      const searchMatch = !query || (card.dataset.title || "").toLowerCase().includes(query);
      card.closest("[class*='col-']").style.display = categoryMatch && searchMatch ? "" : "none";
    });
  };
  filterButtons.forEach((button) => {
    button.addEventListener("click", () => {
      filterButtons.forEach((item) => item.classList.remove("active"));
      button.classList.add("active");
      applyCourseFilters();
    });
  });
  courseSearch?.addEventListener("input", applyCourseFilters);

  document.querySelectorAll(".newsletter-form").forEach((form) => {
    form.addEventListener("submit", () => {
      if (form.checkValidity()) showToast("Thanks for subscribing.");
    });
  });

  function showToast(message) {
    if (!toastEl || !toast) return;
    toastEl.querySelector(".toast-body").textContent = message;
    toast.show();
  }
})();
