// rockSample.js

import { showToast } from './showToast.js';

function updateButton(availableRequests) {
  const button = document.querySelector('.btn-primary.w-100');
  if (availableRequests > 0) {
    button.textContent = `Осталось запросов: ${availableRequests}`;
    button.disabled = false;
    button.style.backgroundColor = ''; // Вернуть оригинальный цвет
    button.style.borderColor = '';
  } else {
    button.textContent = 'Израсходован дневной лимит запросов';
    button.disabled = true;
    button.style.backgroundColor = 'grey';
    button.style.borderColor = 'grey';
  }
}

function handleSubmit() {
  var description = document.getElementById('core-description').value;
  var model = document.getElementById('model-selection').value;

  // Получаем URL из data атрибута
  var analysisUrl = document.querySelector('.col-md-6').getAttribute('data-core-analysis-url');

  fetch(analysisUrl, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({description: description, model: model})
  })
  .then(response => response.json())
  .then(data => {
    let messageType;
      // console.log(data.code)
    if (data.code == 500) {
      messageType = 'error'; // ошибка
    } else if (data.code == 200) {
      messageType = 'success';
      updateButton(data.data.available_requests);
    } else {
      messageType = 'warning'; // предупреждение или неопределенный статус
    }
      // console.log(messageType)
    showToast(data.message, messageType);
  })
  .catch((error) => {
    console.error('Error:', error);
    showToast("Ошибка запроса", 'error'); // для уведомлений об ошибках
  });
}


document.addEventListener("DOMContentLoaded", function() {
  var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
  var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
  });
});

// Делаем handleSubmit глобально доступной
window.handleSubmit = handleSubmit;