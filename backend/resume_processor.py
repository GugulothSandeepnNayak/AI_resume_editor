import ollama
import chromadb
from chromadb.utils import embedding_functions
from config import Config

class ResumeProcessor:
    def __init__(self, db_path: str = Config.CHROMA_DB_PATH, 
                 collection_name: str = "resume_collection"):
        self.client = chromadb.PersistentClient(path=db_path)
        # ChromaDB can use an Ollama embedding function
        # Note: This might require specific ChromaDB versions or configurations.
        # For simplicity and direct control, we will use Ollama's `generate_embeddings` directly.
        
        self.collection = self.client.get_or_create_collection(
            name=collection_name
        )
        print(f"Initialized ChromaDB client at {db_path} with collection '{collection_name}'")

    def _chunk_resume(self, resume_content: str) -> list[str]:
        """
        Breaks down the resume content into smaller, meaningful chunks.
        This is a basic example; more sophisticated chunking could use NLP libraries.
        """
        # Simple chunking by lines/bullet points for demonstration
        chunks = [line.strip() for line in resume_content.split('\n') if line.strip()]
        # Filter out very short or non-informative lines
        chunks = [chunk for chunk in chunks if len(chunk) > 10] 
        return chunks

    def ingest_resume(self, resume_content: str):
        """
        Ingests the master resume: chunks it, embeds it, and stores it in ChromaDB.
        """
        print("Starting resume ingestion...")
        chunks = self._chunk_resume(resume_content)
        print(f"Chunked resume into {len(chunks)} pieces.")

        # Clear existing data and recreate collection to avoid dimension issues
        try:
            self.client.delete_collection(name=self.collection.name)
            print("Deleted existing collection.")
        except Exception as e:
            print(f"Could not delete collection (might not exist): {e}")
        
        # Recreate collection
        self.collection = self.client.create_collection(name=self.collection.name)
        print(f"Recreated collection '{self.collection.name}'")

        embeddings_data = []
        documents_to_add = []
        ids_to_add = []

        for i, chunk in enumerate(chunks):
            try:
                # Use ollama embeddings
                response = ollama.embeddings(model=Config.EMBEDDING_MODEL, prompt=chunk)
                if 'embedding' in response:
                    embeddings_data.append(response['embedding'])
                    documents_to_add.append(chunk)
                    ids_to_add.append(f"resume_chunk_{i}")
                else:
                    print(f"Warning: No embedding found for chunk {i}. Skipping.")
            except Exception as e:
                print(f"Error generating embedding for chunk {i}: {e}")
        
        if documents_to_add:
            print(f"Adding {len(documents_to_add)} documents to ChromaDB.")
            self.collection.add(
                documents=documents_to_add,
                embeddings=embeddings_data,
                ids=ids_to_add
            )
            print("Resume ingestion complete.")
        else:
            print("No valid chunks or embeddings to add to ChromaDB.")

    def retrieve_relevant_experience(self, query_text: str, n_results: int = 5) -> list[str]:
        """
        Queries ChromaDB to find the most relevant resume chunks based on a query.
        """
        print(f"Querying ChromaDB for: '{query_text}'")
        try:
            # First, get embeddings for the query
            query_response = ollama.embeddings(model=Config.EMBEDDING_MODEL, prompt=query_text)
            if 'embedding' not in query_response:
                print("Warning: Could not generate embedding for query. Using fallback.")
                return []
            
            query_embedding = query_response['embedding']
            
            # Query using embeddings
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                include=['documents']
            )
            relevant_docs = results['documents'][0] if results and 'documents' in results and results['documents'] else []
            print(f"Retrieved {len(relevant_docs)} relevant chunks.")
            return relevant_docs
            
        except Exception as e:
            print(f"Error querying ChromaDB: {e}")
            return []
