from resume_processor import ResumeProcessor
from agents import JobAnalyzerAgent, ContentSynthesizerAgent
from ats_scorer import ATSScorer
from pydantic import BaseModel
from typing import Optional

class JobDescription(BaseModel):
    url: Optional[str] = None
    text: str

class MCPOrcestrator:
    def __init__(self):
        self.resume_processor = ResumeProcessor()
        self.job_analyzer = JobAnalyzerAgent()
        self.content_synthesizer = ContentSynthesizerAgent()
        self.ats_scorer = ATSScorer()

    def ingest_master_resume(self, resume_content: str):
        """Initial ingestion of the master resume."""
        self.resume_processor.ingest_resume(resume_content)
        return {"status": "success", "message": "Resume ingested successfully."}

    def tailor_resume_workflow(self, job_desc: JobDescription) -> str:
        """
        Orchestrates the resume tailoring workflow.
        """
        print("\n--- Starting MCP Workflow ---")
        
        job_description_text = job_desc.text
        # If a URL is provided, you'd integrate a scraper here.
        # For this local-first design, the job_desc.text is assumed to be pre-scraped.
        # Example for future integration:
        # if job_desc.url:
        #     job_description_text = self._scrape_job_description(job_desc.url) 
        #     if not job_description_text:
        #         return "Error: Could not scrape job description."

        # Phase 1: Analyze Job Description
        print("MCP: Calling Job Analyzer Agent...")
        analysis_result = self.job_analyzer.analyze_job_description(job_description_text)
        
        extracted_skills = analysis_result.get("skills", [])
        extracted_responsibilities = analysis_result.get("responsibilities", [])
        
        # Combine extracted keywords for a better search query
        search_query = " ".join(extracted_skills + extracted_responsibilities)
        if not search_query:
            print("Warning: No skills or responsibilities extracted. Using generic search.")
            search_query = job_description_text[:100] # Use a part of the job description

        # Phase 2: Retrieve Relevant Experience
        print("MCP: Retrieving relevant experience from ChromaDB...")
        relevant_chunks = self.resume_processor.retrieve_relevant_experience(search_query)
        
        if not relevant_chunks:
            print("Warning: No relevant resume chunks found. Generating content with limited context.")
            # Fallback: if no relevant chunks, provide original resume content if available (not implemented here)
            # Or inform the user.
            relevant_chunks = ["No specific relevant experience found in your master resume for this job based on extracted keywords. Please ensure your master resume is comprehensive or try adjusting the job description."]

        # Phase 3: Synthesize and Generate Tailored Content
        print("MCP: Calling Content Synthesizer Agent...")
        tailored_resume_content = self.content_synthesizer.generate_tailored_content(
            job_description_text,
            relevant_chunks
        )
        
        # Phase 4: Calculate ATS Score
        print("MCP: Calculating ATS score...")
        ats_results = self.ats_scorer.calculate_ats_score(job_description_text, tailored_resume_content)
        
        print("--- MCP Workflow Complete ---")
        
        return {
            "tailored_resume": tailored_resume_content,
            "ats_score": ats_results
        }
    
    # Placeholder for scraping, if integrated directly into backend (less ideal for local-first)
    # def _scrape_job_description(self, url: str) -> Optional[str]:
    #     """
    #     A placeholder for a web scraping function. 
    #     In a real app, this would use Bright Data, Apify, or a similar service.
    #     This part would require an internet connection and potentially API keys.
    #     """
    #     print(f"Attempting to scrape job description from: {url}")
    #     # Example using requests and BeautifulSoup (very basic, might be blocked by sites)
    #     try:
    #         import requests
    #         from bs4 import BeautifulSoup
    #         response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    #         response.raise_for_status() # Raise an exception for HTTP errors
    #         soup = BeautifulSoup(response.text, 'html.parser')
    #         # You'll need to inspect the job site's HTML to find the correct selector for the job description.
    #         # This is highly site-dependent and why a dedicated scraping API is often better.
    #         job_desc_element = soup.find('div', class_='job-description') # Example selector
    #         if job_desc_element:
    #             return job_desc_element.get_text(separator='\n', strip=True)
    #         else:
    #             print("Could not find job description element on the page.")
    #             return None
    #     except requests.exceptions.RequestException as e:
    #         print(f"Scraping failed: {e}")
    #         return None
    #     except Exception as e:
    #         print(f"An unexpected error occurred during scraping: {e}")
    #         return None 