from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv

load_dotenv()

def create_vectorstore():
    try:
        print("🚀 Starting FAISS vector store setup")
        
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        print("🌐 Embeddings initialized")

        loader = TextLoader("main/lung_cancer.txt")
        docs = loader.load()
        print(f"📄 Loaded {len(docs)} documents")

        # Create FAISS vector store from documents and embeddings
        db = FAISS.from_documents(docs, embeddings)
        print("✅ FAISS vector store created")

        # No persistence needed; returns retriever directly
        return db.as_retriever(search_kwargs={'k': 10})
    
    except Exception as e:
        print("🚨 Vector store creation failed:", e)
        return None

retriever = create_vectorstore()
