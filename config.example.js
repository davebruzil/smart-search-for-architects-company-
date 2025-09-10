// Configuration file template
// Copy this to config.js and fill in your actual API keys

const CONFIG = {
    OPENAI_API_KEY: 'your-openai-api-key-here',
    
    // Other configuration options
    DEFAULT_SEARCH_LIMIT: 50,
    SPEECH_RECOGNITION_TIMEOUT: 5000,
    DEBOUNCE_DELAY: 300
};

// Make config available globally
window.CONFIG = CONFIG;