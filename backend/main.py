from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from mcp_orchestrator import MCPOrcestrator, JobDescription
import os

app = FastAPI(
    title="Career-Pilot AI Local-First Backend",
    description="Local-first AI resume tailoring application powered by Ollama and ChromaDB."
)

# Configure CORS to allow communication from your frontend (e.g., Tauri/Electron app)
origins = [
    "http://localhost:3000",  # Example for a React/Svelte dev server
    "tauri://localhost",      # For Tauri development
    "http://127.0.0.1:8000",  # Or whatever your frontend's origin might be in production
    "app://localhost", # For Electron production build
    "capacitor://localhost" # For mobile if you ever go there
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For initial development, allow all. Restrict in production.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the MCP Orchestrator
mcp = MCPOrcestrator()

@app.get("/")
async def read_root():
    return {"message": "Welcome to Career-Pilot AI Local-First Backend! Status: Running."}

@app.post("/ingest-resume/")
async def ingest_resume(resume_file: UploadFile = File(...)):
    """
    Endpoint to upload and ingest the master resume into ChromaDB.
    """
    if not resume_file.filename.endswith(('.txt', '.md', '.pdf')): # Basic file type check
        raise HTTPException(status_code=400, detail="Only .txt, .md, or .pdf files are supported for resume upload.")
    
    try:
        file_content = await resume_file.read()
        file_extension = resume_file.filename.split('.')[-1].lower()
        
        # Handle different file types
        if file_extension == 'pdf':
            resume_content = extract_text_from_pdf(file_content)
        else:
            # For .txt and .md files
            resume_content = file_content.decode("utf-8")
        
        if not resume_content.strip():
            raise HTTPException(status_code=400, detail="The uploaded file appears to be empty or could not be processed.")
        
        result = mcp.ingest_master_resume(resume_content)
        return JSONResponse(content=result, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to ingest resume: {e}")

def extract_text_from_pdf(pdf_content: bytes) -> str:
    """
    Extract text from PDF content using PyPDF2.
    """
    try:
        import PyPDF2
        import io
        
        pdf_file = io.BytesIO(pdf_content)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        
        return text.strip()
    except Exception as e:
        raise Exception(f"Failed to extract text from PDF: {e}")

@app.post("/tailor-resume/")
async def tailor_resume(job_description: JobDescription):
    """
    Endpoint to trigger the resume tailoring workflow for a given job description.
    """
    if not job_description.text:
        raise HTTPException(status_code=400, detail="Job description text cannot be empty.")

    try:
        result = mcp.tailor_resume_workflow(job_description)
        return JSONResponse(content=result, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to tailor resume: {e}")

# If you want a way to check if models are loaded (requires more Ollama API interaction)
@app.get("/check-ollama-status/")
async def check_ollama_status():
    try:
        # This is a very basic check. A real check would list models.
        # Requires 'ollama' Python library to interact with Ollama API
        import ollama
        models = ollama.list()
        # Check if required models are present
        from config import Config
        required_models = [Config.LLM_MODEL, Config.EMBEDDING_MODEL]
        loaded_models = [m['model'] for m in models.get('models', [])]
        
        status = {
            "ollama_running": True,
            "available_models": loaded_models,
            "required_models_pulled": {model: model in loaded_models for model in required_models}
        }
        return JSONResponse(content=status, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ollama check failed: {e}. Is Ollama running and models pulled?") 