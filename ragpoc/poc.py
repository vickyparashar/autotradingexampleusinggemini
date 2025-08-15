import os
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.docstore.document import Document

# 1. Set your API key
os.environ["GOOGLE_API_KEY"] = "AIzaSyDf9GjmDLWHlqmUI5nwHZ39xKVOk39kOh4"

# 2. Load file and split by line
file_path = r"C:\VickyJD\Tools\sampletool\ragpoc\data\datastore.txt"
with open(file_path, "r", encoding="utf-8") as f:
    lines = [line.strip() for line in f if line.strip()]

# 3. Create one Document per line
docs = [Document(page_content=line) for line in lines]

# 4. Create embeddings
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

# 5. Build FAISS index
vector_store = FAISS.from_documents(docs, embeddings)

# 6. Run similarity search
query = "What is the azure mysql hostname?"
results = vector_store.similarity_search(query)

# 7. Print top result
print("🔍 Top match:\n", results[0].page_content)