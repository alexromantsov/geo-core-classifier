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


function updateAnalysisResults(data) {
  const resultsContainer = document.querySelector('.results-content');
  const cardElement = document.querySelector('.card');
  if (!resultsContainer || !cardElement) return;

  let resultsHtml = '';
  const data_info = data
  const responseData = data_info.data.response_data;

  if (responseData) {
    if (responseData.lithotype) {
      resultsHtml += `<p>Литотип: ${responseData.lithotype}</p>`;
    }
    if (responseData.color) {
      resultsHtml += `<p>Цвет: ${responseData.color.join('; ')}</p>`;
    }
    if (responseData.structure) {
      resultsHtml += `<p>Структура: ${responseData.structure.join('; ')}</p>`;
    }
    if (responseData.features) {
      resultsHtml += `<p>Особенности: ${responseData.features.join('; ')}</p>`;
    }
  }

  if (resultsHtml === '') {
    const errorMessage = data_info.message;
    resultsContainer.innerHTML = `<p class="error-message">${errorMessage}</p>`;
    cardElement.classList.add('unavailable');
  } else {
    resultsContainer.innerHTML = resultsHtml;
    cardElement.classList.remove('unavailable');
  }
}


function handleSubmit() {
  var description = document.getElementById('core-description').value;
  var model = document.getElementById('model-selection').value;

    // Индикация загрузки
    const resultsContainer = document.querySelector('.results-content');
    if (resultsContainer) {
      resultsContainer.innerHTML = '<p class="loading-text">Загрузка<span class="loading-dots"></span></p>';
      let dotCount = 0;

      const loadingInterval = setInterval(() => {
        dotCount = (dotCount + 1) % 4;  // Циклически увеличиваем количество точек от 0 до 3
        document.querySelector('.loading-dots').textContent = '.'.repeat(dotCount);
      }, 500);  // Обновляем каждые 500 мс

      // Сохраняем интервал в элементе, чтобы можно было его остановить позже
      resultsContainer.loadingInterval = loadingInterval;
    }


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
      let delayDuration = data.code == 200 ? 3500 : 0; // 3.5 секунды для успеха, 2.5 секунды для ошибки

      setTimeout(() => {
          // Остановка анимации загрузки
        if (resultsContainer && resultsContainer.loadingInterval) {
          clearInterval(resultsContainer.loadingInterval);
        }
        if (data.code == 500) {
          messageType = 'error';
        } else if (data.code == 200) {
          messageType = 'success';
          updateButton(data.data.available_requests);
          updateAnalysisResults(data); // Обновляем результаты анализа
        } else {
          messageType = 'warning';
          updateAnalysisResults(data); // Обновляем результаты анализа
        }
        showToast(data.message, messageType);
      }, delayDuration);
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