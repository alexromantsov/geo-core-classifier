// showToast.js

export function showToast(message, type = 'default') {
  var toastElement = document.getElementById('customToast');
  var toastHeader = toastElement.querySelector('.toast-header');
  var toastMessageContent = document.getElementById('toast-message-content');
  var toastCountdown = document.getElementById('toastCountdown');

  // Очистка предыдущих классов
  toastHeader.className = 'toast-header';

  // Установка цветовой темы в зависимости от типа уведомления
  if (type === 'success') {
    toastHeader.classList.add('bg-success', 'text-white');
  } else if (type === 'warning') {
    toastHeader.classList.add('bg-warning', 'text-dark');
  } else if (type === 'error') {
    toastHeader.classList.add('bg-danger', 'text-white');
  }

  toastMessageContent.textContent = message;

  var toast = new bootstrap.Toast(toastElement, { delay: 5000 });
  toast.show();

}
