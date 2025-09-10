# Smart Search for Architects - Israeli Company Database

An AI-enhanced search platform for freelance architects in Israel. This application transforms a database of 2,000+ Israeli companies into a sophisticated AI-powered search and matching system.

## 🚀 Features

- **AI-Powered Speech Search**: Advanced speech recognition with OpenAI integration
- **Semantic Understanding**: Smart query parsing for regional and company type filtering
- **Hebrew Language Support**: Full RTL support with intelligent Hebrew text processing
- **RAG Enhancement**: Retrieval Augmented Generation for enriched company data
- **Real-time Search**: Instant results with smart debouncing
- **Professional UI**: Modern, responsive design

## 🛠 Setup

### 1. Clone the Repository
```bash
git clone https://github.com/davebruzil/smart-search-for-architects-company-.git
cd smart-search-for-architects-company-
```

### 2. Configure API Keys

#### For the Web Application:
1. Copy `config.example.js` to `config.js`
2. Add your OpenAI API key:
```javascript
const CONFIG = {
    OPENAI_API_KEY: 'your-openai-api-key-here',
    // ... other settings
};
```

#### For RAG Processing:
1. Copy `.env.example` to `.env`
2. Add your OpenAI API key:
```
OPENAI_API_KEY=your-openai-api-key-here
```

### 3. Install Python Dependencies (for RAG processing)
```bash
pip install -r requirements.txt
```

## 🎯 Usage

### Running the Web Application
```bash
# Using Python
python -m http.server 8000

# Or using Node.js
npx serve .
```

Then open http://localhost:8000 in your browser.

### Processing Company Data with RAG
```bash
python rag_processor.py
```

This will enhance the company database with AI-generated descriptions and embeddings.

## 📁 Project Structure

- `index.html` - Main application with AI search interface
- `map-public.json` - Original company database (7,320 lines)
- `map-clean.json` - Cleaned database for processing
- `map-enhanced.json` - AI-enhanced database with embeddings
- `rag_processor.py` - Python script for AI data enhancement
- `config.js` - Configuration file (create from config.example.js)
- `CLAUDE.md` - Development guidelines for Claude Code

## 🔧 Configuration Options

### Search Settings
- `DEFAULT_SEARCH_LIMIT`: Maximum search results (default: 50)
- `SPEECH_RECOGNITION_TIMEOUT`: Speech timeout in ms (default: 5000)
- `DEBOUNCE_DELAY`: Search debounce delay in ms (default: 300)

### AI Features
- **Smart Search**: Uses OpenAI GPT-3.5-turbo for query understanding
- **Speech Recognition**: Advanced speech-to-text with contextual parsing
- **Semantic Scoring**: Enhanced relevance algorithms with embeddings

## 🗃 Data Structure

### Regions (5 total)
- Nationwide (כלל ארצי)
- North (צפון)
- Center (מרכז)
- South (דרום)
- Jerusalem (ירושלים)

### Company Types (13 total)
Including government offices, municipalities, regional councils, hospitals, educational institutions, and non-profits.

### Enhanced Company Records
Each company includes:
- Basic info: name, type, region, contact details
- AI enhancements: descriptions, project types, specialties
- Search metadata: embeddings, relevance scores

## 🔐 Security

- API keys are stored in separate config files
- All sensitive files are gitignored
- Example templates provided for easy setup

## 📝 License

This project is created for the Israeli architectural community.

---

🤖 Enhanced with AI by [Claude Code](https://claude.ai/code)