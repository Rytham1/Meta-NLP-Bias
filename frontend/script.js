/* Smooth scrolling for navigation */
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
});

/* Navbar scroll effect */
window.addEventListener('scroll', () => {
    const nav = document.getElementById('nav');
    if (window.scrollY > 50) {
        nav.classList.add('scrolled');
    } else {
        nav.classList.remove('scrolled');
    }
});

/* Get DOM elements */
const analyzeBtn = document.getElementById('analyzeBtn');
const clearBtn = document.getElementById('clearBtn');
const textInput = document.getElementById('textInput');
const resultsDiv = document.getElementById('results');
const btnText = document.getElementById('btnText');
const btnLoader = document.getElementById('btnLoader');

/* Analyze button click handler */
analyzeBtn.addEventListener('click', async () => {
    const text = textInput.value.trim();
    
    if (!text) {
        alert('Please enter some text to analyze');
        return;
    }

    // Show loading state
    setLoadingState(true);
    resultsDiv.style.display = 'none';

    try {
        // Call the API to analyze text
        const result = await analyzeText(text);
        
        // Display results
        displayResults(result.is_biased, result.confidence);
    } catch (error) {
        console.error('Error analyzing text:', error);
        displayError();
    } finally {
        // Reset button state
        setLoadingState(false);
    }
});

/* Clear button handler */
clearBtn.addEventListener('click', () => {
    textInput.value = '';
    resultsDiv.style.display = 'none';
});

/* Enter key to submit */
textInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        analyzeBtn.click();
    }
});

/* Set loading state for the analyze button */
function setLoadingState(isLoading) {
    analyzeBtn.disabled = isLoading;
    btnText.style.display = isLoading ? 'none' : 'inline';
    btnLoader.style.display = isLoading ? 'inline-block' : 'none';
}

/* Analyze text - connects to Gradio backend API */
async function analyzeText(text) {
    const apiUrl = CONFIG.apiUrl || 'http://127.0.0.1:8000';
    
    // Use Gradio's API endpoint with api_name
    const response = await fetch(`${apiUrl}/call/predict`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            data: [text]  // Gradio expects data as an array
        })
    });
    
    if (!response.ok) {
        throw new Error('API request failed');
    }
    
    const result = await response.json();
    const event_id = result.event_id;
    
    // Poll for results
    const statusResponse = await fetch(`${apiUrl}/call/predict/${event_id}`);
    const reader = statusResponse.body.getReader();
    const decoder = new TextDecoder();
    
    let finalData;
    while (true) {
        const { value, done } = await reader.read();
        if (done) break;
        
        const chunk = decoder.decode(value);
        const lines = chunk.split('\n').filter(line => line.trim());
        
        for (const line of lines) {
            if (line.startsWith('data: ')) {
                const data = JSON.parse(line.slice(6));
                if (data.msg === 'process_completed') {
                    finalData = data.output.data;
                }
            }
        }
    }
    
    if (!finalData) {
        throw new Error('No results received');
    }
    
    // Parse Gradio response format
    // finalData is an array: [prediction_label, confidence, probabilities]
    const prediction_label = finalData[0];  // "⚠️ BIASED" or "✅ NOT BIASED"
    const confidence = finalData[1];
    
    return {
        is_biased: prediction_label.includes("BIASED") && !prediction_label.includes("NOT"),
        confidence: confidence
    };
}

/* Simple bias detection logic */
function demoAnalyze(text) {
    const lowerText = text.toLowerCase();
    
    // Bias indicators
    const biasIndicators = [
        'men', 'women', 'male', 'female', 'boys', 'girls',
        'black', 'white', 'asian', 'hispanic', 'race',
        'gay', 'straight', 'lgbtq', 'homosexual',
        'muslim', 'christian', 'jewish', 'religion',
        'always', 'never', 'all', 'typically', 'usually', 'naturally'
    ];
    
    // Stereotype phrases
    const stereotypePhrases = [
        'better at', 'worse at', 'good at', 'bad at',
        'should be', 'belong in', 'are criminals', 
        'are lazy', 'are smart', 'can\'t', 'cannot'
    ];

    let isBiased = false;
    let confidence = 0.5;
    
    // Check for bias
    const hasIndicator = biasIndicators.some(word => lowerText.includes(word));
    const hasStereotype = stereotypePhrases.some(phrase => lowerText.includes(phrase));
    
    if (hasIndicator && hasStereotype) {
        isBiased = true;
        confidence = 0.85;
    } else if (hasStereotype) {
        isBiased = true;
        confidence = 0.72;
    } else if (hasIndicator) {
        isBiased = true;
        confidence = 0.65;
    }

    return {
        is_biased: isBiased,
        confidence: confidence
    };
}

/* Display analysis results */
function displayResults(isBiased, confidence = 0) {
    resultsDiv.style.display = 'block';
    resultsDiv.className = 'results ' + (isBiased ? 'biased' : 'not-biased');
    
    if (isBiased) {
        resultsDiv.innerHTML = `
            <div class="result-icon">⚠️</div>
            <div class="result-text">Bias Detected</div>
        `;
    } else {
        resultsDiv.innerHTML = `
            <div class="result-icon">✅</div>
            <div class="result-text">No Bias Detected</div>
        `;
    }
}

/* Display error message */
function displayError() {
    resultsDiv.style.display = 'block';
    resultsDiv.className = 'results';
    resultsDiv.style.background = '#f8d7da';
    resultsDiv.style.color = '#721c24';
    resultsDiv.innerHTML = `
        <div class="result-icon">❌</div>
        <div class="result-text">Analysis Failed</div>
        <div class="result-description">
            Sorry, we couldn't analyze the text. Please try again later.
        </div>
    `;
}