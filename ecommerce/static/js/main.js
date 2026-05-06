// Auto-hide messages after 3 seconds
document.addEventListener('DOMContentLoaded', function () {
  const messages = document.querySelectorAll('.message');
  messages.forEach(msg => {
    setTimeout(() => { msg.style.display = 'none'; }, 3000);
  });
});