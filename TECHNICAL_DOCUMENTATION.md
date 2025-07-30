# Career-Pilot AI: Technical Documentation

## Table of Contents
1. [System Architecture](#system-architecture)
2. [Technology Stack](#technology-stack)
3. [Backend Architecture](#backend-architecture)
4. [Frontend Architecture](#frontend-architecture)
5. [Data Flow](#data-flow)
6. [Key Components](#key-components)
7. [API Design](#api-design)
8. [Database Design](#database-design)
9. [AI/ML Implementation](#aiml-implementation)
10. [Security Considerations](#security-considerations)
11. [Performance Optimization](#performance-optimization)
12. [Deployment Strategy](#deployment-strategy)

---

## System Architecture

### Overview
Career-Pilot AI is a **local-first, AI-powered resume tailoring application** that uses a microservices-inspired architecture with clear separation of concerns.

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   AI Services   │
│   (React-like)  │◄──►│   (FastAPI)     │◄──►│   (Ollama)      │
│                 │    │                 │    │                 │
│ - UI Components │    │ - API Endpoints │    │ - LLM Models    │
│ - State Mgmt    │    │ - Business Logic│    │ - Embeddings    │
│ - HTTP Client   │    │ - Data Processing│   │ - Vector DB     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Architecture Principles
- **Local-First**: All processing happens locally using Ollama
- **Modular Design**: Clear separation between UI, API, and AI layers
- **Scalable**: Easy to add new AI models or features
- **Privacy-Focused**: No data leaves the user's machine

---

## Technology Stack

### Backend Technologies
- **FastAPI**: Modern, fast web framework for building APIs
- **Python 3.8+**: Core programming language
- **Uvicorn**: ASGI server for running FastAPI
- **Pydantic**: Data validation and serialization
- **ChromaDB**: Vector database for semantic search

### AI/ML Technologies
- **Ollama**: Local LLM inference engine
- **Llama3**: Primary language model for text generation
- **mxbai-embed-large**: Embedding model for vector operations
- **ChromaDB**: Vector similarity search

### Frontend Technologies
- **Vanilla JavaScript**: Core functionality
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with gradients and animations
- **Font Awesome**: Icon library
- **Google Fonts**: Typography

### Development Tools
- **Python Virtual Environment**: Dependency isolation
- **Git**: Version control
- **HTTP Server**: Local development server

---

## Backend Architecture

### Project Structure
```
backend/
├── main.py              # FastAPI application entry point
├── config.py            # Configuration management
├── agents.py            # AI agent implementations
├── mcp_orchestrator.py  # Workflow orchestration
├── resume_processor.py  # Resume processing logic
├── ats_scorer.py        # ATS scoring algorithm
└── chroma_db/           # Vector database storage
```

### Core Components

#### 1. FastAPI Application (`main.py`)
```python
# Key Features:
- CORS middleware for frontend communication
- File upload handling with validation
- JSON API endpoints
- Error handling and status codes
- Health check endpoints
```

**Key Endpoints:**
- `GET /`: Health check
- `POST /ingest-resume/`: Resume upload and processing
- `POST /tailor-resume/`: Resume tailoring workflow
- `GET /check-ollama-status/`: System status check

#### 2. Configuration Management (`config.py`)
```python
class Config:
    OLLAMA_HOST = "http://localhost:11434"
    CHROMA_DB_PATH = "./chroma_db"
    LLM_MODEL = "llama3"
    EMBEDDING_MODEL = "mxbai-embed-large"
```

**Design Pattern:** Singleton configuration class with environment variable support.

#### 3. Resume Processor (`resume_processor.py`)
```python
class ResumeProcessor:
    def __init__(self, db_path, collection_name):
        self.client = chromadb.PersistentClient(path=db_path)
        self.collection = self.client.get_or_create_collection(name=collection_name)
    
    def _chunk_resume(self, resume_content: str) -> list[str]:
        # Semantic chunking algorithm
        # Splits resume into meaningful segments
    
    def ingest_resume(self, resume_content: str):
        # 1. Chunk the resume
        # 2. Generate embeddings
        # 3. Store in ChromaDB
    
    def retrieve_relevant_experience(self, query_text: str, n_results: int = 5):
        # 1. Generate query embedding
        # 2. Perform similarity search
        # 3. Return relevant chunks
```

**Key Algorithms:**
- **Chunking Strategy**: Line-based with minimum length filtering
- **Embedding Generation**: Using Ollama's embedding API
- **Similarity Search**: Vector-based retrieval with ChromaDB

#### 4. AI Agents (`agents.py`)

##### Job Analyzer Agent
```python
class JobAnalyzerAgent:
    def analyze_job_description(self, job_description: str) -> dict:
        # 1. Extract skills and responsibilities using LLM
        # 2. Parse JSON response
        # 3. Return structured data
```

**Prompt Engineering:**
- Structured JSON output format
- Temperature control (0.3) for consistency
- Error handling for malformed responses

##### Content Synthesizer Agent
```python
class ContentSynthesizerAgent:
    def generate_tailored_content(self, job_description: str, relevant_experiences: list[str]) -> str:
        # 1. Combine job description and relevant experiences
        # 2. Generate tailored resume sections
        # 3. Return formatted content
```

**Content Generation Strategy:**
- Professional summary creation
- Experience bullet point rewriting
- Skills section prioritization
- Keyword optimization

#### 5. MCP Orchestrator (`mcp_orchestrator.py`)
```python
class MCPOrcestrator:
    def tailor_resume_workflow(self, job_desc: JobDescription) -> dict:
        # Phase 1: Job Analysis
        analysis_result = self.job_analyzer.analyze_job_description(job_description_text)
        
        # Phase 2: Experience Retrieval
        relevant_chunks = self.resume_processor.retrieve_relevant_experience(search_query)
        
        # Phase 3: Content Synthesis
        tailored_resume_content = self.content_synthesizer.generate_tailored_content(
            job_description_text, relevant_chunks
        )
        
        # Phase 4: ATS Scoring
        ats_results = self.ats_scorer.calculate_ats_score(job_description_text, tailored_resume_content)
        
        return {"tailored_resume": tailored_resume_content, "ats_score": ats_results}
```

**Workflow Design:**
- **Sequential Processing**: Each phase depends on previous results
- **Error Handling**: Graceful degradation at each step
- **Modular Design**: Easy to add new phases or modify existing ones

#### 6. ATS Scorer (`ats_scorer.py`)
```python
class ATSScorer:
    def calculate_ats_score(self, job_description: str, tailored_resume: str) -> Dict:
        # 1. Extract keywords and skills
        job_keywords = self._extract_keywords(job_description)
        resume_keywords = self._extract_keywords(tailored_resume)
        
        # 2. Calculate component scores
        keyword_score = self._calculate_keyword_score(job_keywords, resume_keywords)
        skill_score = self._calculate_skill_score(job_skills, resume_skills)
        experience_score = self._calculate_experience_relevance(job_description, tailored_resume)
        format_score = self._calculate_format_score(tailored_resume)
        
        # 3. Calculate weighted overall score
        overall_score = self._calculate_overall_score(keyword_score, skill_score, experience_score, format_score)
```

**Scoring Algorithm:**
- **Keyword Match (35%)**: Exact and semantic keyword matching
- **Skill Alignment (30%)**: Technical and soft skill comparison
- **Experience Relevance (25%)**: AI-powered relevance analysis
- **Format Compliance (10%)**: ATS-friendly format checking

---

## Frontend Architecture

### Project Structure
```
frontend/
├── index.html          # Main HTML structure
├── styles.css          # CSS styling and animations
├── script.js           # JavaScript functionality
└── server.py           # Development server
```

### Component Design

#### 1. HTML Structure (`index.html`)
```html
<!-- Modular sections for different functionality -->
- Header with branding
- Status indicator
- File upload section
- Job description input
- Results display with ATS scoring
- Loading overlay
- Toast notifications
```

**Design Principles:**
- **Semantic HTML**: Proper use of HTML5 elements
- **Accessibility**: ARIA labels and keyboard navigation
- **Responsive Design**: Mobile-first approach

#### 2. CSS Architecture (`styles.css`)
```css
/* Design System */
- Color palette with gradients
- Typography scale
- Spacing system
- Animation library
- Responsive breakpoints

/* Component Styles */
- Glassmorphism effects
- Interactive hover states
- Loading animations
- Score bar animations
```

**Key Features:**
- **CSS Grid & Flexbox**: Modern layout techniques
- **CSS Variables**: Consistent theming
- **Animations**: Smooth transitions and micro-interactions
- **Media Queries**: Responsive design

#### 3. JavaScript Architecture (`script.js`)
```javascript
// Module Pattern
const CareerPilotAI = {
    // Configuration
    API_BASE_URL: 'http://localhost:8000',
    
    // State Management
    state: {
        resumeUploaded: false,
        currentResumeFile: null
    },
    
    // Event Handlers
    setupEventListeners() {
        // File upload handlers
        // Form validation
        // API communication
    },
    
    // API Communication
    async uploadResume(file) {
        // FormData creation
        // HTTP POST request
        // Error handling
    },
    
    // UI Updates
    displayResults(data) {
        // Handle both string and object responses
        // Update ATS score display
        // Animate score bars
    }
};
```

**Key Patterns:**
- **Event-Driven Architecture**: Responsive to user interactions
- **Promise-based API calls**: Async/await for clean code
- **Error Handling**: Graceful degradation
- **State Management**: Centralized application state

---

## Data Flow

### 1. Resume Upload Flow
```
User Upload → File Validation → PDF Text Extraction → 
Chunking → Embedding Generation → ChromaDB Storage
```

### 2. Resume Tailoring Flow
```
Job Description → Keyword Extraction → Semantic Search → 
Content Generation → ATS Scoring → Results Display
```

### 3. ATS Scoring Flow
```
Job + Resume → Keyword Analysis → Skill Comparison → 
Experience Relevance → Format Check → Weighted Score
```

---

## API Design

### RESTful Endpoints

#### 1. Resume Ingestion
```http
POST /ingest-resume/
Content-Type: multipart/form-data

Parameters:
- resume_file: File upload (.txt, .md, .pdf)

Response:
{
    "status": "success",
    "message": "Resume ingested successfully."
}
```

#### 2. Resume Tailoring
```http
POST /tailor-resume/
Content-Type: application/json

Request Body:
{
    "text": "Job description text"
}

Response:
{
    "tailored_resume": "Generated resume content",
    "ats_score": {
        "overall_score": 85.5,
        "keyword_score": 90.0,
        "skill_score": 85.0,
        "experience_score": 80.0,
        "format_score": 95.0,
        "missing_keywords": ["kubernetes", "docker"],
        "analysis": "Detailed analysis...",
        "recommendations": ["Add missing keywords..."]
    }
}
```

#### 3. System Status
```http
GET /check-ollama-status/

Response:
{
    "ollama_running": true,
    "available_models": ["llama3", "mxbai-embed-large"],
    "required_models_pulled": {
        "llama3": true,
        "mxbai-embed-large": true
    }
}
```

---

## Database Design

### ChromaDB Schema
```python
# Collection: resume_collection
{
    "ids": ["resume_chunk_0", "resume_chunk_1", ...],
    "embeddings": [[0.1, 0.2, ...], [0.3, 0.4, ...], ...],
    "documents": ["chunk text 1", "chunk text 2", ...],
    "metadatas": [{"source": "resume"}, {"source": "resume"}, ...]
}
```

**Design Considerations:**
- **Vector Dimensions**: Compatible with embedding model
- **Chunking Strategy**: Optimal for semantic search
- **Metadata**: Source tracking and filtering
- **Indexing**: Efficient similarity search

---

## AI/ML Implementation

### 1. Language Model Integration
```python
# Ollama Integration
response = ollama.chat(
    model=Config.LLM_MODEL,
    messages=[{'role': 'user', 'content': prompt}],
    options={'temperature': 0.3}
)
```

**Model Selection Criteria:**
- **Llama3**: Balanced performance and speed
- **Temperature Control**: Consistency vs. creativity
- **Prompt Engineering**: Structured output formats

### 2. Embedding Generation
```python
# Vector Embeddings
response = ollama.embeddings(
    model=Config.EMBEDDING_MODEL, 
    prompt=text_chunk
)
embedding = response['embedding']
```

**Embedding Strategy:**
- **Model**: mxbai-embed-large for quality
- **Chunking**: Semantic boundaries
- **Storage**: ChromaDB for similarity search

### 3. Semantic Search
```python
# Similarity Search
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=5,
    include=['documents']
)
```

**Search Algorithm:**
- **Cosine Similarity**: Vector similarity metric
- **Top-K Retrieval**: Configurable result count
- **Relevance Ranking**: Score-based ordering

---

## Security Considerations

### 1. Local-First Architecture
- **No Cloud Dependencies**: All processing local
- **Data Privacy**: No data transmission to external services
- **Model Security**: Local LLM inference

### 2. Input Validation
```python
# File Type Validation
if not resume_file.filename.endswith(('.txt', '.md', '.pdf')):
    raise HTTPException(status_code=400, detail="Invalid file type")

# Content Validation
if not resume_content.strip():
    raise HTTPException(status_code=400, detail="Empty file")
```

### 3. Error Handling
- **Graceful Degradation**: System continues with partial functionality
- **User Feedback**: Clear error messages
- **Logging**: Debug information for troubleshooting

---

## Performance Optimization

### 1. Backend Optimizations
- **Async Processing**: Non-blocking I/O operations
- **Caching**: ChromaDB for fast vector search
- **Chunking**: Efficient text processing
- **Connection Pooling**: Database connection management

### 2. Frontend Optimizations
- **Lazy Loading**: Load components on demand
- **Debouncing**: Reduce API calls during typing
- **Caching**: Browser cache for static assets
- **Minification**: Compressed CSS and JavaScript

### 3. AI Model Optimizations
- **Model Selection**: Balance between quality and speed
- **Batch Processing**: Efficient embedding generation
- **Memory Management**: Proper cleanup of large objects

---

## Deployment Strategy

### 1. Development Environment
```bash
# Backend
cd backend
source ../venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000

# Frontend
cd frontend
python3 server.py
```

### 2. Production Considerations
- **Containerization**: Docker for consistent deployment
- **Load Balancing**: Multiple backend instances
- **Monitoring**: Health checks and logging
- **Backup**: ChromaDB data persistence

### 3. Scaling Strategy
- **Horizontal Scaling**: Multiple backend instances
- **Database Sharding**: Distributed ChromaDB
- **CDN**: Static asset delivery
- **Caching**: Redis for session management

---

## Interview Talking Points

### Technical Highlights
1. **Local-First AI**: Privacy-focused architecture using Ollama
2. **Vector Search**: Semantic similarity using ChromaDB
3. **Multi-Agent System**: Specialized AI agents for different tasks
4. **ATS Scoring**: Comprehensive resume optimization algorithm
5. **Modern Web Stack**: FastAPI + Vanilla JavaScript

### Architecture Decisions
1. **Why FastAPI?**: Performance, automatic docs, type safety
2. **Why Ollama?**: Local processing, privacy, cost-effective
3. **Why ChromaDB?**: Vector similarity, local storage, easy setup
4. **Why Vanilla JS?**: No framework overhead, full control

### Problem-Solving Examples
1. **Embedding Dimension Mismatch**: Collection recreation strategy
2. **PDF Processing**: PyPDF2 integration for text extraction
3. **Error Handling**: Graceful degradation and user feedback
4. **Performance**: Async processing and caching strategies

### Future Enhancements
1. **Multi-Model Support**: Different LLMs for different tasks
2. **Advanced Chunking**: NLP-based semantic chunking
3. **Real-time Collaboration**: WebSocket integration
4. **Mobile App**: React Native or Flutter implementation 