# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an AI-enhanced freelance architect platform for the Israeli market. It transforms a database of 2,000+ Israeli companies into a sophisticated AI-powered search and matching system that connects architects with relevant opportunities.

## Project Structure

- `index.html` - Single-page application with AI search interface
- `map-public.json` - Original database of Israeli companies, regions, and company types (7,320 lines)
- `map-clean.json` - Cleaned version of company database (processed by RAG)
- `map-enhanced.json` - AI-enhanced company data with embeddings and descriptions
- `rag_processor.py` - Python script for AI enhancement of company data
- `requirements.txt` - Python dependencies for RAG processing

## Key Features

The platform includes:
- Hebrew/English bilingual search with RTL support
- AI-powered semantic search using OpenAI GPT integration
- Smart matching algorithms for architects and companies
- Real-time search suggestions and autocomplete
- Advanced filtering by region and company type

## Data Structure

### Regions (5 total)
- Nationwide (כלל ארצי)
- North (צפון) 
- Center (מרכז)
- South (דרום)
- Jerusalem (ירושלים)

### Company Types (13 total)
Including government offices, municipalities, regional councils, hospitals, educational institutions, and non-profits.

### Company Records
Each company has: id, regionId, region, typeId, companyType, companyName, tel, site, comment

## Development Commands

### Running the Application
```bash
# Serve locally (Python)
python -m http.server 8000

# Or with Node.js
npx serve .
```

### Python RAG Processor
```bash
# Install dependencies
pip install -r requirements.txt

# Run RAG processing (enhances company data with AI)
python rag_processor.py

# Note: Requires OpenAI API key in rag_processor.py
```

### Testing
The application runs entirely in the browser - no build process required. Test by opening `index.html` in a web browser.

## Architecture Notes

### AI Integration
- Optional OpenAI API key for GPT-powered search
- Fallback to local semantic search algorithms
- Smart query processing with Hebrew NLP support
- Relevance scoring and ranking algorithms

### Search Modes
- **Smart Search**: Uses OpenAI GPT-3.5-turbo for query understanding
- **Semantic Search**: Enhanced local algorithms with semantic mapping

### Hebrew Language Support
The platform is primarily Hebrew-focused with:
- RTL text direction
- Hebrew tokenization and search
- Bilingual query support
- Israeli market specialization

## Important Implementation Details

### Search Algorithm
The search scoring system includes:
- Exact phrase matching (100 points)
- Individual word matches (10 points)
- Company name matches (20 points bonus)
- Company type matches (15 points bonus) 
- Architecture-specific term mapping (25 points bonus)
- AI context bonuses (30 points)

### Data Loading
The JSON file uses non-standard format with trailing commas - cleaned using regex before parsing:
```javascript
const cleanedText = text.replace(/,(\s*[}\]])/g, '$1');
```

### Error Handling
Graceful fallback from AI search to local search on API failures or missing API key.

## RAG Processing Architecture

### Data Enhancement Pipeline
The `rag_processor.py` script enhances company data through:
- AI-generated Hebrew descriptions for each company
- Project type predictions based on company type and context
- Architectural specialty recommendations
- Text embeddings for semantic search using OpenAI's text-embedding-3-small
- Batch processing with rate limiting (0.5s delay between requests)

### Enhanced Data Structure
Processed companies include additional fields:
- `aiDescription` - Hebrew description of architectural opportunities
- `projectTypes` - Array of likely project types
- `architectSpecialties` - Relevant architectural specializations
- `complexity` - Project complexity level (low/medium/high)
- `typicalScale` - Typical project scale (small/medium/large)
- `searchableText` - Concatenated searchable text for embeddings
- `embedding` - 1536-dimensional vector for semantic search

### Semantic Search
- Uses cosine similarity on embeddings for relevance scoring
- Minimum similarity threshold of 0.3
- Returns up to 20 most relevant results
- Fallback to traditional keyword search if embeddings unavailable