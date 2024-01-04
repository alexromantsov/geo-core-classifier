// rockSample.js

import { showToast } from './showToast.js';

function updateButton(availableRequests) {
  const button = document.querySelector('.btn-primary.w-100');
  if (availableRequests > 0) {
    button.textContent = `Remaining requests: ${availableRequests}`;
    button.disabled = false;
    button.style.backgroundColor = ''; // Return to original color
    button.style.borderColor = '';
  } else {
    button.textContent = 'Daily request limit exhausted';
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
  const data_info = data;
  const responseData = data_info.data.response_data;

  if (responseData) {
    if (responseData.lithotype) {
      resultsHtml += `<p>Lithotype: ${responseData.lithotype}</p>`;
    }
    if (responseData.color) {
      resultsHtml += `<p>Color: ${responseData.color.join('; ')}</p>`;
    }
    if (responseData.structure) {
      resultsHtml += `<p>Structure: ${responseData.structure.join('; ')}</p>`;
    }
    if (responseData.features) {
      resultsHtml += `<p>Features: ${responseData.features.join('; ')}</p>`;
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

    // Loading indication
    const resultsContainer = document.querySelector('.results-content');
    if (resultsContainer) {
      resultsContainer.innerHTML = '<p class="loading-text">Loading<span class="loading-dots"></span></p>';
      let dotCount = 0;

      const loadingInterval = setInterval(() => {
        dotCount = (dotCount + 1) % 4;  // Cyclically increase the number of dots from 0 to 3
        document.querySelector('.loading-dots').textContent = '.'.repeat(dotCount);
      }, 500);  // Update every 500 ms

      // Store the interval in the element for later stopping
      resultsContainer.loadingInterval = loadingInterval;
    }


  // Get the URL from the data attribute
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
      let delayDuration = data.code == 200 ? 3500 : 0; // 3.5 seconds for success, 2.5 seconds for error

      setTimeout(() => {
          // Stop loading animation
        if (resultsContainer && resultsContainer.loadingInterval) {
          clearInterval(resultsContainer.loadingInterval);
        }
        if (data.code == 500) {
          messageType = 'error';
        } else if (data.code == 200) {
          messageType = 'success';
          updateButton(data.data.available_requests);
          updateAnalysisResults(data); // Update analysis results
        } else {
          messageType = 'warning';
          updateAnalysisResults(data); // Update analysis results
        }
        showToast(data.message, messageType);
      }, delayDuration);
    })
  .catch((error) => {
    console.error('Error:', error);
    showToast("Request error", 'error'); // for error notifications
  });
}

document.getElementById("random-description-btn").addEventListener("click", function() {
  const containerDiv = document.querySelector('div[data-random-description-url]');
  const randomDescriptionUrl = containerDiv.getAttribute('data-random-description-url');

  // Example: setting desired language
  const languageData = {
    language: 'en' // or any other language of your choice
  };

  fetch(randomDescriptionUrl, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(languageData)
  })
  .then(response => {
    if (response.ok) {
      return response.json();
    } else {
      throw new Error('Failed to retrieve description');
    }
  })
  .then(data => {
    document.getElementById("core-description").value = data.description;
  })
  .catch(error => {
    console.error('Error:', error);
  });
});


document.addEventListener("DOMContentLoaded", function() {
  var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
  var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
  });
});

// Make handleSubmit globally available
window.handleSubmit = handleSubmit;
