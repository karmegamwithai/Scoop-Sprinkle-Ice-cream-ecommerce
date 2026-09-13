// Simple quantity stepper used on product/cart pages
document.addEventListener('click', function (e) {
  if (e.target.matches('[data-step]')) {
    const input = document.querySelector(e.target.getAttribute('data-target'));
    if (!input) return;
    const step = parseInt(e.target.getAttribute('data-step'), 10);
    const newVal = Math.max(1, (parseInt(input.value, 10) || 1) + step);
    input.value = newVal;
  }
});

// Auto-hide flash messages after a few seconds
document.addEventListener('DOMContentLoaded', function () {
  const messages = document.querySelectorAll('.messages li');
  messages.forEach(function (msg) {
    setTimeout(function () {
      msg.style.transition = 'opacity .4s ease';
      msg.style.opacity = '0';
      setTimeout(function () { msg.remove(); }, 400);
    }, 3500);
  });
});
