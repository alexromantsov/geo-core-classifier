// analysisResults.js

document.addEventListener('DOMContentLoaded', function() {
  var resultsContainer = document.querySelector('.results-content');
  if (resultsContainer) {
    resultsContainer.innerHTML = '<p>Литотип: ...</p><p>Цвет: ...</p>';
  }

  var modelSelectElement = document.querySelector('.form-select');
  if (modelSelectElement) {
    modelSelectElement.addEventListener('change', function() {
      var selectedModel = this.value;
      var resultsContainer = document.querySelector('.results-content');
      var resultsHtml = '';

      if (selectedModel === 'standard') {
        resultsHtml = '<p>Литотип: ...</p><p>Цвет: ...</p>';
      } else if (selectedModel === 'standard_plus') {
        resultsHtml = '<p>Литотип: ...</p><p>Цвет: ...</p><p>Структура: ...</p><p>Особенности: ...</p>';
      }

      if (resultsContainer) {
        resultsContainer.innerHTML = resultsHtml;
      }
      // Делаем блок доступным
      // var cardElement = document.querySelector('.card');
      // if (cardElement) {
      //   cardElement.classList.remove('unavailable');
      // }
    });
  }
});
