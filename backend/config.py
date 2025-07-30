import os

class Config:
    OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", os.path.join(os.path.dirname(__file__), "chroma_db"))
    LLM_MODEL = os.getenv("LLM_MODEL", "llama3")
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "mxbai-embed-large")
    # You might want to add API keys for external scrapers here,
    # but for a local-first app, it's better to pass them from the frontend if needed.
