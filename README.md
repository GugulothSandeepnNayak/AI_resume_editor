# 🚀 Career-Pilot AI: Local-First Resume Optimization

> **AI-powered resume tailoring application that works completely locally for privacy and cost-effectiveness**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![Ollama](https://img.shields.io/badge/Ollama-Local%20AI-orange.svg)](https://ollama.ai/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🌟 **Features**

- **🤖 Multi-Agent AI System**: Specialized AI agents for job analysis, content generation, and ATS scoring
- **🔒 Privacy-First**: All processing happens locally using Ollama - no data leaves your machine
- **📊 ATS Optimization**: Comprehensive scoring system to ensure your resume passes ATS screening
- **🎯 Smart Tailoring**: AI-powered resume customization based on job requirements
- **📁 Multi-Format Support**: Upload PDF, TXT, or MD resume files
- **💡 Intelligent Recommendations**: Get specific suggestions to improve your resume
- **⚡ Real-time Processing**: Fast AI-powered analysis and generation

## 🏗️ **Architecture**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   AI Services   │
│   (React-like)  │◄──►│   (FastAPI)     │◄──►│   (Ollama)      │
│                 │    │                 │    │                 │
│ - Modern UI     │    │ - REST API      │    │ - LLM Models    │
│ - Real-time     │    │ - Business Logic│    │ - Embeddings    │
│ - ATS Scoring   │    │ - Data Processing│   │ - Vector DB     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 **Quick Start**

### **Prerequisites**

1. **Python 3.8+** installed
2. **Ollama** installed and running
3. **Git** for cloning the repository

### **Installation**

```bash
# Clone the repository
git clone https://github.com/yourusername/career-pilot-ai.git
cd career-pilot-ai

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Pull required AI models
ollama pull llama3
ollama pull mxbai-embed-large
```

### **Running the Application**

```bash
# Terminal 1: Start Backend
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000

# Terminal 2: Start Frontend
cd frontend
python3 server.py
```

### **Access the Application**

Open your browser and navigate to: **http://localhost:3000**

## 📋 **Usage Guide**

### **1. Upload Your Resume**
- Drag and drop or click "Choose File"
- Supported formats: PDF, TXT, MD
- Wait for upload confirmation

### **2. Enter Job Description**
- Paste the complete job description
- Include specific requirements and responsibilities
- Click "Generate Tailored Resume"

### **3. Review Results**
- View your AI-tailored resume
- Check ATS score and breakdown
- Review improvement recommendations
- Copy the optimized content

## 🧠 **AI System Components**

### **Job Analyzer Agent**
- Extracts key skills and responsibilities from job descriptions
- Uses structured prompts for consistent analysis
- Outputs JSON-formatted data for processing

### **Content Synthesizer Agent**
- Generates tailored resume content
- Integrates job-specific keywords
- Creates professional summaries and experience sections

### **ATS Scorer Agent**
- Multi-factor scoring system (Keyword, Skills, Experience, Format)
- Provides detailed analysis and recommendations
- Identifies missing keywords and skills

### **Vector Search Engine**
- Semantic similarity search using ChromaDB
- Finds relevant experience from your master resume
- Uses AI embeddings for intelligent matching

## 🛠️ **Technology Stack**

### **Backend**
- **FastAPI**: Modern, fast web framework
- **Python 3.8+**: Core programming language
- **Uvicorn**: ASGI server
- **ChromaDB**: Vector database for semantic search
- **Pydantic**: Data validation

### **AI/ML**
- **Ollama**: Local LLM inference engine
- **Llama3**: Primary language model
- **mxbai-embed-large**: Embedding model
- **Vector Search**: Semantic similarity

### **Frontend**
- **Vanilla JavaScript**: Core functionality
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with animations
- **Responsive Design**: Mobile-friendly interface

## 📊 **ATS Scoring System**

The application uses a comprehensive 4-factor scoring system:

| Component | Weight | Description |
|-----------|--------|-------------|
| **Keyword Match** | 35% | Job-specific terminology and requirements |
| **Skill Alignment** | 30% | Technical and soft skill comparison |
| **Experience Relevance** | 25% | AI-powered relevance analysis |
| **Format Compliance** | 10% | ATS-friendly formatting |

## 🔧 **Configuration**

### **Environment Variables**
```bash
OLLAMA_HOST=http://localhost:11434
CHROMA_DB_PATH=./chroma_db
LLM_MODEL=llama3
EMBEDDING_MODEL=mxbai-embed-large
```

### **Model Configuration**
- **LLM Model**: Llama3 for text generation and analysis
- **Embedding Model**: mxbai-embed-large for vector operations
- **Temperature Settings**: Optimized for consistency and creativity

## 📁 **Project Structure**

```
career-pilot-ai/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration management
│   ├── agents.py            # AI agent implementations
│   ├── mcp_orchestrator.py  # Workflow orchestration
│   ├── resume_processor.py  # Resume processing logic
│   ├── ats_scorer.py        # ATS scoring algorithm
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── index.html           # Main HTML structure
│   ├── styles.css           # CSS styling
│   ├── script.js            # JavaScript functionality
│   └── server.py            # Development server
├── docs/
│   ├── TECHNICAL_DOCUMENTATION.md
│   ├── FUNCTIONAL_DOCUMENTATION.md
│   └── AI_SYSTEM_EXPLANATION.md
├── README.md                # This file
├── requirements.txt         # Root dependencies
└── .gitignore              # Git ignore rules
```

## 🚀 **API Endpoints**

### **Resume Management**
- `POST /ingest-resume/` - Upload and process resume
- `POST /tailor-resume/` - Generate tailored resume
- `GET /check-ollama-status/` - System status check

### **Response Format**
```json
{
  "tailored_resume": "Generated content...",
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

## 🔒 **Privacy & Security**

- **Local Processing**: All AI operations happen on your machine
- **No Cloud Dependencies**: No data transmission to external services
- **Model Security**: Local LLM inference with Ollama
- **Data Privacy**: Your resume and job data never leave your system

## 🎯 **Performance Optimization**

### **System Requirements**
- **Minimum**: 8GB RAM, 10GB storage
- **Recommended**: 16GB RAM, 20GB storage
- **CPU**: Multi-core processor
- **GPU**: Not required (CPU-only operation)

### **Optimization Tips**
- Close unnecessary applications to free up RAM
- Use SSD storage for faster operations
- Keep Ollama running to avoid model reloading
- Optimize resume file size (under 2MB)

## 🐛 **Troubleshooting**

### **Common Issues**

**"uvicorn command not found"**
```bash
source venv/bin/activate
pip install uvicorn
```

**"Ollama connection failed"**
```bash
ollama serve
ollama list
```

**"Port already in use"**
```bash
pkill -f "uvicorn main:app"
pkill -f "python.*server.py"
```

**"Models not found"**
```bash
ollama pull llama3
ollama pull mxbai-embed-large
```

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 **Acknowledgments**

- **Ollama** for local AI inference capabilities
- **FastAPI** for the excellent web framework
- **ChromaDB** for vector database functionality
- **Llama3** for powerful language model capabilities

## 📞 **Support**

- **Issues**: [GitHub Issues](https://github.com/yourusername/career-pilot-ai/issues)
- **Documentation**: [Technical Docs](docs/TECHNICAL_DOCUMENTATION.md)
- **AI System**: [AI Explanation](docs/AI_SYSTEM_EXPLANATION.md)

---

**Made with ❤️ for job seekers who want AI-powered resume optimization without compromising privacy.**

⭐ **Star this repository if you find it helpful!** 