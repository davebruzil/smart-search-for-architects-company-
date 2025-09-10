#!/usr/bin/env python3
"""
RAG Processor for Israeli Company Database
Enhances company data with AI-generated descriptions and embeddings
"""

import json
import re
import time
import numpy as np
from typing import Dict, List, Any, Optional
from openai import OpenAI
from sklearn.metrics.pairwise import cosine_similarity
from tqdm import tqdm
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class RAGProcessor:
    def __init__(self, api_key: str):
        """Initialize RAG processor with OpenAI API key"""
        self.client = OpenAI(api_key=api_key)
        self.companies = []
        self.enriched_companies = []
        
    def load_company_data(self, file_path: str) -> None:
        """Load company data from JSON file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            self.companies = data.get('companies', [])
            self.regions = data.get('regions', [])  
            self.company_types = data.get('companyTypes', [])
            
            logger.info(f"Loaded {len(self.companies)} companies, {len(self.regions)} regions, {len(self.company_types)} company types")
            
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            raise
    
    def enrich_company_description(self, company: Dict[str, Any]) -> Dict[str, Any]:
        """Generate AI-enhanced description for a single company"""
        try:
            # Create context for GPT
            company_context = f"""
Company Name: {company.get('companyName', 'Unknown')}
Type: {company.get('companyType', 'Unknown')}
Region: {company.get('region', 'Unknown')}
Comment: {company.get('comment', 'N/A')}

This is an Israeli company that may need architectural services.
"""
            
            prompt = f"""Analyze this Israeli company for architectural opportunities:

{company_context}

Based on the company type and context, provide a detailed analysis in Hebrew including:

1. What types of architectural projects they likely need
2. Specializations that would be valuable for architects
3. Project complexity and typical scale
4. Current trends affecting this sector in Israel
5. How architects typically collaborate with this type of organization

Please respond with a JSON object in the following format:
{{
  "aiDescription": "detailed Hebrew description of architectural opportunities",
  "projectTypes": ["list", "of", "likely", "project", "types"],
  "architectSpecialties": ["relevant", "architectural", "specializations"],
  "complexity": "low/medium/high",
  "typicalScale": "small/medium/large",
  "collaborationStyle": "typical approach for working with this organization",
  "marketTrends": "current relevant trends in Israeli market"
}}

Ensure all text is in Hebrew and relevant to the Israeli architectural market."""

            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=1000
            )
            
            # Parse the response
            ai_data = json.loads(response.choices[0].message.content)
            
            # Add AI enhancements to company data
            enhanced_company = company.copy()
            enhanced_company.update(ai_data)
            
            # Create searchable text for embedding
            searchable_text = f"""
            {company.get('companyName', '')}
            {company.get('companyType', '')}
            {company.get('region', '')}
            {ai_data.get('aiDescription', '')}
            {' '.join(ai_data.get('projectTypes', []))}
            {' '.join(ai_data.get('architectSpecialties', []))}
            {ai_data.get('collaborationStyle', '')}
            {ai_data.get('marketTrends', '')}
            """
            enhanced_company['searchableText'] = searchable_text.strip()
            
            return enhanced_company
            
        except Exception as e:
            logger.error(f"Error enriching company {company.get('companyName', 'Unknown')}: {e}")
            # Return original company with minimal enhancement
            enhanced_company = company.copy()
            enhanced_company.update({
                'aiDescription': f"חברה מסוג {company.get('companyType', 'לא ידוע')} הממוקמת ב{company.get('region', 'לא ידוע')}",
                'projectTypes': [],
                'architectSpecialties': [],
                'complexity': 'medium',
                'typicalScale': 'medium',
                'searchableText': f"{company.get('companyName', '')} {company.get('companyType', '')} {company.get('region', '')}"
            })
            return enhanced_company
    
    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for given text using OpenAI"""
        try:
            response = self.client.embeddings.create(
                model="text-embedding-3-small",
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            # Return zero vector as fallback
            return [0.0] * 1536  # text-embedding-3-small dimension
    
    def batch_enrich_companies(self, batch_size: int = 10) -> None:
        """Enrich all companies with AI descriptions and embeddings"""
        logger.info(f"Starting to enrich {len(self.companies)} companies...")
        
        # Process companies in batches to avoid rate limits
        for i in tqdm(range(0, len(self.companies), batch_size), desc="Processing companies"):
            batch = self.companies[i:i + batch_size]
            
            for company in batch:
                try:
                    # Enrich with AI description
                    enhanced_company = self.enrich_company_description(company)
                    
                    # Generate embedding
                    embedding = self.generate_embedding(enhanced_company['searchableText'])
                    enhanced_company['embedding'] = embedding
                    
                    self.enriched_companies.append(enhanced_company)
                    
                    # Small delay to respect rate limits
                    time.sleep(0.5)
                    
                except Exception as e:
                    logger.error(f"Failed to process company {company.get('companyName', 'Unknown')}: {e}")
                    # Add company without enhancements
                    fallback_company = company.copy()
                    fallback_company['embedding'] = [0.0] * 1536
                    self.enriched_companies.append(fallback_company)
            
            # Longer delay between batches
            if i + batch_size < len(self.companies):
                logger.info(f"Processed {i + batch_size} companies. Waiting...")
                time.sleep(2)
    
    def semantic_search(self, query: str, top_k: int = 20) -> List[Dict[str, Any]]:
        """Perform semantic search using embeddings"""
        if not self.enriched_companies:
            logger.error("No enriched companies available. Run batch_enrich_companies first.")
            return []
        
        try:
            # Generate query embedding
            query_embedding = self.generate_embedding(query)
            
            # Calculate similarities
            company_embeddings = [comp['embedding'] for comp in self.enriched_companies]
            similarities = cosine_similarity([query_embedding], company_embeddings)[0]
            
            # Add similarity scores and sort
            results = []
            for i, company in enumerate(self.enriched_companies):
                if similarities[i] > 0.3:  # Relevance threshold
                    company_with_score = company.copy()
                    company_with_score['similarity_score'] = float(similarities[i])
                    results.append(company_with_score)
            
            # Sort by similarity and return top k
            results.sort(key=lambda x: x['similarity_score'], reverse=True)
            return results[:top_k]
            
        except Exception as e:
            logger.error(f"Error in semantic search: {e}")
            return []
    
    def save_enhanced_data(self, output_file: str) -> None:
        """Save enriched data to JSON file"""
        try:
            enhanced_data = {
                'regions': self.regions,
                'companyTypes': self.company_types,
                'companies': self.enriched_companies,
                'metadata': {
                    'total_companies': len(self.enriched_companies),
                    'rag_enhanced': True,
                    'embedding_model': 'text-embedding-3-small',
                    'processed_at': time.strftime('%Y-%m-%d %H:%M:%S')
                }
            }
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(enhanced_data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Enhanced data saved to {output_file}")
            
        except Exception as e:
            logger.error(f"Error saving enhanced data: {e}")
            raise
    
    def test_search(self, test_queries: List[str]) -> None:
        """Test the semantic search with sample queries"""
        logger.info("Testing semantic search...")
        
        for query in test_queries:
            logger.info(f"\nQuery: {query}")
            results = self.semantic_search(query, top_k=5)
            
            if results:
                logger.info(f"Found {len(results)} results:")
                for i, result in enumerate(results[:3], 1):
                    logger.info(f"{i}. {result.get('companyName', 'Unknown')} "
                              f"({result.get('companyType', 'Unknown')}) "
                              f"- Similarity: {result['similarity_score']:.3f}")
            else:
                logger.info("No results found")

def main():
    """Main function to run RAG processing"""
    import os
    from dotenv import load_dotenv
    
    # Load environment variables
    load_dotenv()
    
    # Get API key from environment variable
    API_KEY = os.getenv('OPENAI_API_KEY')
    if not API_KEY:
        raise ValueError("OPENAI_API_KEY environment variable not set. Please set it in .env file or environment.")
    
    # Initialize processor
    processor = RAGProcessor(API_KEY)
    
    try:
        # Load original data
        processor.load_company_data('map-clean.json')
        
        # Process first 5 companies as a quick test
        logger.info("Processing first 5 companies as a quick test...")
        test_companies = processor.companies[:5]
        processor.companies = test_companies
        
        # Enrich companies with AI descriptions and embeddings
        processor.batch_enrich_companies(batch_size=5)
        
        # Save enhanced data
        processor.save_enhanced_data('map-enhanced.json')
        
        # Test semantic search
        test_queries = [
            "בתי ספר",
            "בתי חולים",
            "פרויקטי תשתית",
            "עיריות",
            "מוסדות תרבות"
        ]
        processor.test_search(test_queries)
        
        logger.info("RAG processing completed successfully!")
        
    except Exception as e:
        logger.error(f"Error in main processing: {e}")
        raise

if __name__ == "__main__":
    main()