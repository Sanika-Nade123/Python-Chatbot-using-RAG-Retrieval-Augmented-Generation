from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os

model = SentenceTransformer('all-MiniLM-L6-v2')
knowledge_base = []
index = None

def load_knowledge_base():
    global knowledge_base
    knowledge_base = []
    
    # Load all knowledge base files from data directory
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    
    # Load main knowledge base
    kb_path = os.path.join(data_dir, 'knowledge_base.txt')
    if os.path.exists(kb_path):
        with open(kb_path, 'r', encoding='utf-8') as f:
            knowledge_base.extend([p.strip() for p in f.read().split('\n\n') if p.strip()])
    
    # Load topic-specific files
    topics_dir = os.path.join(data_dir, 'topics')
    if os.path.exists(topics_dir):
        for file in os.listdir(topics_dir):
            if file.endswith('.txt'):
                with open(os.path.join(topics_dir, file), 'r', encoding='utf-8') as f:
                    knowledge_base.extend([p.strip() for p in f.read().split('\n\n') if p.strip()])

def initialize_faiss():
    global index, knowledge_base
    if not knowledge_base:
        load_knowledge_base()
    
    embeddings = model.encode(knowledge_base)
    dimension = embeddings.shape[1]
    
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings.astype('float32'))

def get_rag_response(query):
    global index, knowledge_base
    
    try:
        # Initialize if not already done
        if index is None or not knowledge_base:
            initialize_faiss()
        
        # Encode query
        query_vector = model.encode([query])
        
        # Search for top 3 most similar passages
        k = 3
        distances, indices = index.search(query_vector.astype('float32'), k)
        
        # Get the most relevant passage
        best_idx = indices[0][0]
        if best_idx < len(knowledge_base):
            return knowledge_base[best_idx]
        
        return "I apologize, but I don't have enough information to answer that question accurately."
        
    except Exception as e:
        print(f"RAG Error: {str(e)}")
        return "I apologize, but I encountered an error while processing your question. Please try again."

# Initialize on module load
try:
    initialize_faiss()
except Exception as e:
    print(f"Initial RAG setup error: {str(e)}")