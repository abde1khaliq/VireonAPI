// Replace the entire script section with this updated code
document.addEventListener('DOMContentLoaded', function () {
    // Tab switching functionality
    const tabs = document.querySelectorAll('.testing-tab');
    const tabPanes = document.querySelectorAll('.tab-pane');

    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const tabId = tab.getAttribute('data-tab');

            // Update active tab
            tabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');

            // Show corresponding tab pane
            tabPanes.forEach(pane => pane.classList.remove('active'));
            document.getElementById(`${tabId}-tab`).classList.add('active');
        });
    });

    // Image upload functionality
    const imageUploadArea = document.getElementById('image-upload-area');
    const imageInput = document.getElementById('image-input');
    const imagePreview = document.getElementById('image-preview');
    const previewImg = document.getElementById('preview-img');
    const removeImageBtn = document.getElementById('remove-image');
    const analyzeImageBtn = document.getElementById('analyze-image');

    imageUploadArea.addEventListener('click', () => {
        imageInput.click();
    });

    imageInput.addEventListener('change', function () {
        if (this.files && this.files[0]) {
            const reader = new FileReader();

            reader.onload = function (e) {
                previewImg.src = e.target.result;
                imageUploadArea.style.display = 'none';
                imagePreview.style.display = 'block';
                analyzeImageBtn.disabled = false;
            }

            reader.readAsDataURL(this.files[0]);
        }
    });

    removeImageBtn.addEventListener('click', function (e) {
        e.stopPropagation();
        imageInput.value = '';
        imageUploadArea.style.display = 'block';
        imagePreview.style.display = 'none';
        analyzeImageBtn.disabled = true;
    });

    // Analysis functionality with real API calls
    const analyzeTextBtn = document.getElementById('analyze-text');
    const resultStatus = document.getElementById('result-status');
    const resultsContent = document.getElementById('results-content');

    analyzeTextBtn.addEventListener('click', analyzeTextContent);
    analyzeImageBtn.addEventListener('click', analyzeImageContent);

    // Function to analyze text content
    async function analyzeTextContent() {
        const textInput = document.getElementById('text-input').value.trim();

        if (!textInput) {
            return;
        }

        // Show loading state
        resultsContent.innerHTML = `
            <div class="loading">
                <div class="loading-spinner"></div>
                Analyzing text content...
            </div>
        `;

        try {
            // Make API call with proper authorization
            const response = await fetch('http://127.0.0.1:8000/v1/analyze/content/', {
                method: 'POST',
                headers: {
                    'Authorization': 'Bearer 2cf82c1764f44f13d2bd2adcadc1b2b312eeb908e0e76f0c7497e340284642c9',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ user_input: textInput })
            });

            if (!response.ok) {
                throw new Error(`API error: ${response.status}`);
            }

            const data = await response.json();

            // Display results using the correct API response structure
            displayResults(data, 'text');
        } catch (error) {
            console.error('Error analyzing text:', error);
            resultsContent.innerHTML = `
                <div class="result-item">
                    <span class="result-label">Error</span>
                    <span class="result-value">Failed to analyze text: ${error.message}</span>
                </div>
            `;
        }
    }

    // Function to analyze image content
    async function analyzeImageContent() {
        if (!imageInput.files[0]) {
            alert('Please upload an image to analyze');
            return;
        }

        // Show loading state
        resultsContent.innerHTML = `
            <div class="loading">
                <div class="loading-spinner"></div>
                Analyzing image content...
            </div>
        `;

        try {
            const formData = new FormData();
            formData.append('image', imageInput.files[0]);

            // Make API call with proper authorization for image
            const response = await fetch('http://127.0.0.1:8000/v1/analyze/content/', {
                method: 'POST',
                headers: {
                    'Authorization': 'Bearer 2cf82c1764f44f13d2bd2adcadc1b2b312eeb908e0e76f0c7497e340284642c9'
                },
                body: formData
            });

            if (!response.ok) {
                throw new Error(`API error: ${response.status}`);
            }

            const data = await response.json();

            // Display results using the correct API response structure
            displayResults(data, 'image');
        } catch (error) {
            console.error('Error analyzing image:', error);
            resultsContent.innerHTML = `
                <div class="result-item">
                    <span class="result-label">Error</span>
                    <span class="result-value">Failed to analyze image: ${error.message}</span>
                </div>
            `;
        }
    }

    // Function to display results based on your API response structure
    function displayResults(data, type) {
        // Extract the result object from the response
        const result = data.result || data;

        // Update status badge based on violation flag
        if (!result.violation) {
            resultStatus.innerHTML = '<span class="status-badge safe">Safe Content</span>';
        } else {
            resultStatus.innerHTML = '<span class="status-badge unsafe">Content Flagged</span>';
        }

        // Create results HTML based on type and API response
        let resultsHTML = '';

        // For both text and image, show the relevant information from your API response
        resultsHTML = `
            <div class="result-item">
                <span class="result-label">Violation Detected</span>
                <span class="result-value">${result.violation ? 'Yes' : 'No'}</span>
            </div>
            <div class="result-item">
                <span class="result-label">Harm Type</span>
                <span class="result-value">${result.harm_type.join(', ')}</span>
            </div>
            <div class="result-item">
                <span class="result-label">Confidence</span>
                <span class="result-value">
                    <div class="confidence-meter">
                        <div class="confidence-fill" style="width: ${result.confidence * 100}%"></div>
                    </div>
                    ${(result.confidence * 100).toFixed(1)}%
                </span>
            </div>
            <div class="result-item">
                <span class="result-label">Severity</span>
                <span class="result-value">${result.severity}</span>
            </div>
            <div class="result-item">
                <span class="result-label">Reasoning</span>
                <span class="result-value">${result.reasoning}</span>
            </div>
        `;

        // Update results content
        resultsContent.innerHTML = resultsHTML;

        // Animate confidence score
        const confidenceElements = document.querySelectorAll('.confidence-fill');
        confidenceElements.forEach(el => {
            // Reset animation
            const width = el.style.width;
            el.style.width = '0%';

            // Trigger reflow
            void el.offsetWidth;

            // Animate to actual width
            el.style.width = width;
        });
    }
});

document.addEventListener('DOMContentLoaded', function () {
    const faqQuestions = document.querySelectorAll('.faq-question');

    faqQuestions.forEach(question => {
        question.addEventListener('click', () => {
            const answer = question.nextElementSibling;
            const isActive = answer.classList.contains('active');

            // Close all answers
            document.querySelectorAll('.faq-answer').forEach(ans => {
                ans.classList.remove('active');
            });

            document.querySelectorAll('.faq-question').forEach(q => {
                q.classList.remove('active');
            });

            // Open clicked answer if it wasn't already active
            if (!isActive) {
                question.classList.add('active');
                answer.classList.add('active');
            }
        });
    });
});