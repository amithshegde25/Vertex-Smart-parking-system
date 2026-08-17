// Smart Parking Management System - Client Script

document.addEventListener('DOMContentLoaded', () => {
  // Auto dismiss alert messages after 6 seconds
  const alerts = document.querySelectorAll('.alert');
  alerts.forEach((alert) => {
    setTimeout(() => {
      alert.style.opacity = '0';
      alert.style.transition = 'opacity 0.5s ease-out';
      setTimeout(() => alert.remove(), 500);
    }, 6000);
  });

  // Client-side Registration Form Validation
  const registerForm = document.querySelector('#register-form');
  if (registerForm) {
    registerForm.addEventListener('submit', (e) => {
      const password = document.querySelector('#password').value;
      const confirmPassword = document.querySelector('#confirm_password').value;
      const email = document.querySelector('#email').value;

      // Email format check
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(email)) {
        e.preventDefault();
        alert('Please enter a valid email address.');
        return;
      }

      // Password match check
      if (password !== confirmPassword) {
        e.preventDefault();
        alert('Passwords do not match. Please try again.');
        return;
      }

      if (password.length < 6) {
        e.preventDefault();
        alert('Password must be at least 6 characters long.');
        return;
      }
    });
  }

  // Visual Parking Layout Interactive Filters (if layout page)
  const filterButtons = document.querySelectorAll('[data-filter]');
  if (filterButtons.length > 0) {
    filterButtons.forEach((btn) => {
      btn.addEventListener('click', () => {
        const filter = btn.getAttribute('data-filter');
        const slots = document.querySelectorAll('.slot-card');

        filterButtons.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');

        slots.forEach((slot) => {
          if (filter === 'all') {
            slot.style.display = 'block';
          } else {
            if (slot.classList.contains(`status-${filter}`)) {
              slot.style.display = 'block';
            } else {
              slot.style.display = 'none';
            }
          }
        });
      });
    });
  }
});
