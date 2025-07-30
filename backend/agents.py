import ollama
from config import Config
import json

class JobAnalyzerAgent:
    def __init__(self):
        self.model = Config.LLM_MODEL

    def analyze_job_description(self, job_description: str) -> dict:
        """
        Analyzes a job description to extract key skills and responsibilities.
        """
        print("Agent 1: Analyzing job description...")
        prompt = f"""You are an expert HR analyst. Analyze this job description and extract the 5 most critical skills and the top 3 responsibilities. Output this as a structured JSON object with two keys: 'skills' (a list of strings) and 'responsibilities' (a list of strings).

        JOB DESCRIPTION:
        ---
        {job_description}
        ---

        Output JSON:
        """
        
        try:
            response = ollama.chat(
                model=self.model,
                messages=[{'role': 'user', 'content': prompt}],
                options={'temperature': 0.3} # Keep output more consistent
            )
            content = response['message']['content']
            # Attempt to parse JSON. Sometimes LLMs might add conversational text.
            json_start = content.find('{')
            json_end = content.rfind('}') + 1
            if json_start != -1 and json_end != -1:
                json_str = content[json_start:json_end]
                return json.loads(json_str)
            else:
                print(f"Warning: Could not find valid JSON in response: {content}")
                return {"skills": [], "responsibilities": []}
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from Job Analyzer: {e}\nRaw content: {content}")
            return {"skills": [], "responsibilities": []}
        except Exception as e:
            print(f"Error in JobAnalyzerAgent: {e}")
            return {"skills": [], "responsibilities": []}


class ContentSynthesizerAgent:
    def __init__(self):
        self.model = Config.LLM_MODEL

    def generate_tailored_content(self, job_description: str, relevant_experiences: list[str]) -> str:
        """
        Generates tailored resume content based on the job description and relevant experiences.
        """
        print("Agent 2: Synthesizing and generating tailored content...")
        
        retrieved_docs_str = "\n".join([f"- {exp}" for exp in relevant_experiences])

        prompt = f"""
        You are a professional resume writer. Your task is to tailor resume sections for the following job description, leveraging the provided relevant experiences.

        **JOB DESCRIPTION:**
        ---
        {job_description}
        ---

        Here are the most relevant experiences from the candidate's master resume:
        **RELEVANT EXPERIENCES:**
        ---
        {retrieved_docs_str}
        ---

        Based on this, perform the following actions:
        1.  Write a new 2-3 sentence Professional Summary that directly targets this job. Focus on impact and key skills.
        2.  Rewrite the relevant experience bullet points from 'RELEVANT EXPERIENCES' to use keywords from the job description, quantify achievements where possible, and highlight relevance. For each provided relevant experience, generate 1-2 tailored bullet points.
        3.  Create a prioritized 'Skills' section (e.g., Technical Skills, Soft Skills, Tools) based on the job's requirements and the candidate's inferred abilities. List 8-12 key skills.

        Output the complete, tailored resume sections, clearly labeled (e.g., "Professional Summary", "Experience", "Skills").
        """
        
        try:
            response = ollama.chat(
                model=self.model,
                messages=[{'role': 'user', 'content': prompt}],
                options={'temperature': 0.7} # Allow for more creative generation
            )
            return response['message']['content']
        except Exception as e:
            print(f"Error in ContentSynthesizerAgent: {e}")
            return "An error occurred during content generation."
