// analysisResults.js

document.addEventListener('DOMContentLoaded', function() {
  var resultsContainer = document.querySelector('.results-content');
  if (resultsContainer) {
    resultsContainer.innerHTML = '<p>Lithotype: ...</p><p>Color: ...</p>';
  }

  var modelSelectElement = document.querySelector('.form-select');
  if (modelSelectElement) {
    modelSelectElement.addEventListener('change', function() {
      var selectedModel = this.value;
      var resultsContainer = document.querySelector('.results-content');
      var resultsHtml = '';

      if (selectedModel === 'standard') {
        resultsHtml = '<p>Lithotype: ...</p><p>Color: ...</p>';
      } else if (selectedModel === 'standard_plus') {
        resultsHtml = '<p>Lithotype: ...</p><p>Color: ...</p><p>Structure: ...</p><p>Features: ...</p>';
      }

      if (resultsContainer) {
        resultsContainer.innerHTML = resultsHtml;
      }
      // Making the block available
      // var cardElement = document.querySelector('.card');
      // if (cardElement) {
      //   cardElement.classList.remove('unavailable');
      // }
    });
  }
});
