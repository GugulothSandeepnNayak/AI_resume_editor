import ollama
import re
from typing import Dict, List, Tuple
from config import Config
import json

class ATSScorer:
    def __init__(self):
        self.model = Config.LLM_MODEL
        
    def calculate_ats_score(self, job_description: str, tailored_resume: str) -> Dict:
        """
        Calculate ATS score by analyzing multiple factors:
        1. Keyword matching
        2. Skill alignment
        3. Experience relevance
        4. Format compliance
        """
        print("ATS Scorer: Analyzing resume against job description...")
        
        # Extract keywords and skills from job description
        job_keywords = self._extract_keywords(job_description)
        job_skills = self._extract_skills(job_description)
        
        # Extract keywords and skills from tailored resume
        resume_keywords = self._extract_keywords(tailored_resume)
        resume_skills = self._extract_skills(tailored_resume)
        
        # Calculate various scores
        keyword_score = self._calculate_keyword_score(job_keywords, resume_keywords)
        skill_score = self._calculate_skill_score(job_skills, resume_skills)
        experience_score = self._calculate_experience_relevance(job_description, tailored_resume)
        format_score = self._calculate_format_score(tailored_resume)
        
        # Calculate weighted overall score
        overall_score = self._calculate_overall_score(keyword_score, skill_score, experience_score, format_score)
        
        # Generate detailed analysis
        analysis = self._generate_detailed_analysis(job_description, tailored_resume, job_keywords, resume_keywords)
        
        return {
            "overall_score": overall_score,
            "keyword_score": keyword_score,
            "skill_score": skill_score,
            "experience_score": experience_score,
            "format_score": format_score,
            "missing_keywords": self._find_missing_keywords(job_keywords, resume_keywords),
            "missing_skills": self._find_missing_skills(job_skills, resume_skills),
            "analysis": analysis,
            "recommendations": self._generate_recommendations(job_keywords, resume_keywords, overall_score)
        }
    
    def _extract_keywords(self, text: str) -> List[str]:
        """
        Extract important keywords from text using AI.
        """
        prompt = f"""
        Extract the 15 most important keywords from this text. Focus on:
        - Technical terms
        - Industry-specific terminology
        - Tools and technologies
        - Action verbs
        - Qualifications and requirements
        
        Text: {text}
        
        Return only the keywords as a JSON array of strings, no explanations.
        """
        
        try:
            response = ollama.chat(
                model=self.model,
                messages=[{'role': 'user', 'content': prompt}],
                options={'temperature': 0.1}
            )
            content = response['message']['content']
            
            # Try to parse JSON
            json_start = content.find('[')
            json_end = content.rfind(']') + 1
            if json_start != -1 and json_end != -1:
                keywords = json.loads(content[json_start:json_end])
                return [kw.lower().strip() for kw in keywords if kw.strip()]
            else:
                # Fallback: extract common keywords
                return self._fallback_keyword_extraction(text)
                
        except Exception as e:
            print(f"Error extracting keywords: {e}")
            return self._fallback_keyword_extraction(text)
    
    def _extract_skills(self, text: str) -> List[str]:
        """
        Extract specific skills from text.
        """
        prompt = f"""
        Extract specific technical and soft skills from this text. Focus on:
        - Programming languages
        - Frameworks and tools
        - Soft skills
        - Certifications
        - Methodologies
        
        Text: {text}
        
        Return only the skills as a JSON array of strings, no explanations.
        """
        
        try:
            response = ollama.chat(
                model=self.model,
                messages=[{'role': 'user', 'content': prompt}],
                options={'temperature': 0.1}
            )
            content = response['message']['content']
            
            json_start = content.find('[')
            json_end = content.rfind(']') + 1
            if json_start != -1 and json_end != -1:
                skills = json.loads(content[json_start:json_end])
                return [skill.lower().strip() for skill in skills if skill.strip()]
            else:
                return self._fallback_skill_extraction(text)
                
        except Exception as e:
            print(f"Error extracting skills: {e}")
            return self._fallback_skill_extraction(text)
    
    def _fallback_keyword_extraction(self, text: str) -> List[str]:
        """
        Fallback keyword extraction using regex patterns.
        """
        # Common technical keywords
        technical_patterns = [
            r'\b(python|java|javascript|react|node\.js|aws|docker|kubernetes|sql|nosql|api|rest|graphql|microservices|agile|scrum|devops|ci/cd|git|jenkins|postgresql|mongodb|redis|elasticsearch|kafka|spark|hadoop|machine learning|ai|data science|cloud|azure|gcp)\b',
            r'\b(lead|manage|develop|implement|design|architect|optimize|deploy|maintain|test|debug|analyze|plan|coordinate|mentor|train|supervise|direct|oversee|facilitate)\b',
            r'\b(senior|junior|principal|staff|lead|manager|director|architect|engineer|developer|analyst|consultant|specialist)\b'
        ]
        
        keywords = []
        for pattern in technical_patterns:
            matches = re.findall(pattern, text.lower())
            keywords.extend(matches)
        
        return list(set(keywords))
    
    def _fallback_skill_extraction(self, text: str) -> List[str]:
        """
        Fallback skill extraction using regex patterns.
        """
        skill_patterns = [
            r'\b(python|java|javascript|typescript|react|angular|vue|node\.js|express|django|flask|fastapi|spring|hibernate|aws|azure|gcp|docker|kubernetes|jenkins|git|postgresql|mysql|mongodb|redis|elasticsearch|kafka|spark|hadoop|tensorflow|pytorch|scikit-learn)\b',
            r'\b(leadership|communication|problem solving|teamwork|collaboration|time management|project management|agile|scrum|kanban|devops|ci/cd|tdd|bdd|code review|mentoring|presentation|negotiation|analytical thinking|creativity)\b'
        ]
        
        skills = []
        for pattern in skill_patterns:
            matches = re.findall(pattern, text.lower())
            skills.extend(matches)
        
        return list(set(skills))
    
    def _calculate_keyword_score(self, job_keywords: List[str], resume_keywords: List[str]) -> float:
        """
        Calculate keyword matching score (0-100).
        """
        if not job_keywords:
            return 0.0
        
        # Find matching keywords
        job_keywords_set = set(job_keywords)
        resume_keywords_set = set(resume_keywords)
        matching_keywords = job_keywords_set.intersection(resume_keywords_set)
        
        # Calculate score
        match_ratio = len(matching_keywords) / len(job_keywords_set)
        score = match_ratio * 100
        
        return min(score, 100.0)
    
    def _calculate_skill_score(self, job_skills: List[str], resume_skills: List[str]) -> float:
        """
        Calculate skill alignment score (0-100).
        """
        if not job_skills:
            return 0.0
        
        # Find matching skills
        job_skills_set = set(job_skills)
        resume_skills_set = set(resume_skills)
        matching_skills = job_skills_set.intersection(resume_skills_set)
        
        # Calculate score with bonus for additional relevant skills
        match_ratio = len(matching_skills) / len(job_skills_set)
        bonus = min(len(resume_skills_set - job_skills_set) * 0.05, 0.2)  # Up to 20% bonus
        score = (match_ratio + bonus) * 100
        
        return min(score, 100.0)
    
    def _calculate_experience_relevance(self, job_description: str, tailored_resume: str) -> float:
        """
        Calculate experience relevance score using AI analysis.
        """
        prompt = f"""
        Analyze how well the experience described in the resume matches the job requirements.
        Consider:
        - Relevance of past roles to the target position
        - Alignment of responsibilities with job requirements
        - Quantifiable achievements that match job needs
        
        Job Description: {job_description[:500]}...
        
        Resume: {tailored_resume[:500]}...
        
        Rate the experience relevance from 0-100 and provide a brief explanation.
        Return as JSON: {{"score": number, "explanation": "string"}}
        """
        
        try:
            response = ollama.chat(
                model=self.model,
                messages=[{'role': 'user', 'content': prompt}],
                options={'temperature': 0.3}
            )
            content = response['message']['content']
            
            json_start = content.find('{')
            json_end = content.rfind('}') + 1
            if json_start != -1 and json_end != -1:
                result = json.loads(content[json_start:json_end])
                return min(result.get('score', 50), 100.0)
            else:
                return 50.0  # Default score
                
        except Exception as e:
            print(f"Error calculating experience relevance: {e}")
            return 50.0
    
    def _calculate_format_score(self, tailored_resume: str) -> float:
        """
        Calculate format compliance score (0-100).
        """
        score = 100.0
        
        # Check for common ATS-friendly format requirements
        checks = [
            (len(tailored_resume) > 100, "Resume has sufficient content"),
            (len(tailored_resume) < 2000, "Resume is not too long"),
            ("experience" in tailored_resume.lower(), "Contains experience section"),
            ("skills" in tailored_resume.lower(), "Contains skills section"),
            (not re.search(r'[^\x00-\x7F]+', tailored_resume), "No special characters"),
            (len(re.findall(r'\b\d{4}\b', tailored_resume)) >= 1, "Contains years/experience"),
        ]
        
        deductions = []
        for check, description in checks:
            if not check:
                deductions.append(description)
                score -= 15
        
        return max(score, 0.0)
    
    def _calculate_overall_score(self, keyword_score: float, skill_score: float, 
                               experience_score: float, format_score: float) -> float:
        """
        Calculate weighted overall ATS score.
        """
        weights = {
            'keyword': 0.35,    # 35% - Most important for ATS
            'skill': 0.30,      # 30% - Skills are crucial
            'experience': 0.25, # 25% - Experience relevance
            'format': 0.10      # 10% - Format compliance
        }
        
        overall_score = (
            keyword_score * weights['keyword'] +
            skill_score * weights['skill'] +
            experience_score * weights['experience'] +
            format_score * weights['format']
        )
        
        return round(overall_score, 1)
    
    def _find_missing_keywords(self, job_keywords: List[str], resume_keywords: List[str]) -> List[str]:
        """
        Find keywords from job description that are missing in resume.
        """
        job_set = set(job_keywords)
        resume_set = set(resume_keywords)
        return list(job_set - resume_set)
    
    def _find_missing_skills(self, job_skills: List[str], resume_skills: List[str]) -> List[str]:
        """
        Find skills from job description that are missing in resume.
        """
        job_set = set(job_skills)
        resume_set = set(resume_skills)
        return list(job_set - resume_set)
    
    def _generate_detailed_analysis(self, job_description: str, tailored_resume: str, 
                                  job_keywords: List[str], resume_keywords: List[str]) -> str:
        """
        Generate detailed analysis of the resume-job match.
        """
        prompt = f"""
        Provide a detailed analysis of how well the tailored resume matches the job description.
        Focus on:
        1. Keyword alignment and coverage
        2. Skill match and gaps
        3. Experience relevance
        4. Overall fit for the position
        
        Job Description Keywords: {job_keywords[:10]}
        Resume Keywords: {resume_keywords[:10]}
        
        Provide a concise analysis (2-3 paragraphs) highlighting strengths and areas for improvement.
        """
        
        try:
            response = ollama.chat(
                model=self.model,
                messages=[{'role': 'user', 'content': prompt}],
                options={'temperature': 0.4}
            )
            return response['message']['content']
        except Exception as e:
            print(f"Error generating analysis: {e}")
            return "Analysis could not be generated due to an error."
    
    def _generate_recommendations(self, job_keywords: List[str], resume_keywords: List[str], 
                                overall_score: float) -> List[str]:
        """
        Generate specific recommendations for improvement.
        """
        recommendations = []
        
        missing_keywords = self._find_missing_keywords(job_keywords, resume_keywords)
        
        if overall_score < 70:
            recommendations.append("Overall ATS score is below optimal. Consider incorporating more job-specific keywords.")
        
        if len(missing_keywords) > 5:
            recommendations.append(f"Add {len(missing_keywords)} missing keywords: {', '.join(missing_keywords[:5])}")
        
        if overall_score < 50:
            recommendations.append("Significantly restructure resume to better align with job requirements.")
        elif overall_score < 80:
            recommendations.append("Make minor adjustments to improve keyword matching and skill alignment.")
        else:
            recommendations.append("Resume is well-optimized for ATS. Focus on interview preparation.")
        
        return recommendations 