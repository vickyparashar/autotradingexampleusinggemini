import os
from pathlib import Path
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.docstore.document import Document

# 1. Set your API key
os.environ["GOOGLE_API_KEY"] = "AIzaSyDf9GjmDLWHlqmUI5nwHZ39xKVOk39kOh4"

# 2. Paths
file_path = r"C:\Users\jparasha\OneDrive - Capgemini\Vicky\CG\Pass\dailynotes\AllDailyNotesOne.txt"
index_path = Path("faiss_index")

# 3. Create embeddings
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

# 4. Load or create FAISS index
if index_path.exists():
    print("🔄 Loading existing FAISS index...")
    vector_store = FAISS.load_local(str(index_path), embeddings, allow_dangerous_deserialization=True)
else:
    print("⚡ Creating new FAISS index...")
    with open(file_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
    docs = [Document(page_content=line) for line in lines]
    vector_store = FAISS.from_documents(docs, embeddings)
    vector_store.save_local(str(index_path))
    print("✅ Index saved to disk.")

# 5. Run similarity search
query = input("Ask me something: ")
results = vector_store.similarity_search(query)

# 6. Print top result
print("🔍 Top match:\n", results[0].page_content)