import os
from pathlib import Path
# fixed import: chat model moved to langchain_community
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document
from langchain.chains import RetrievalQA

# 1. API key
os.environ["GOOGLE_API_KEY"] = "AIzaSyDf9GjmDLWHlqmUI5nwHZ39xKVOk39kOh4"

# 2. Paths
INDEX_PATH = Path("faiss_index")
DATA_FILE = Path("datastore.txt")  # make sure this file exists

# 3. Create embeddings
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

# 4. Load or create FAISS index
vectorstore = None
if INDEX_PATH.exists():
    print("🔄 Loading existing FAISS index from disk...")
    vectorstore = FAISS.load_local(str(INDEX_PATH), embeddings, allow_dangerous_deserialization=True)
else:
    print("⚡ Creating new FAISS index from datastore.txt...")
    docs = []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                docs.append(Document(page_content=line))
    vectorstore = FAISS.from_documents(docs, embeddings)
    vectorstore.save_local(str(INDEX_PATH))
    print("✅ Index saved to disk.")

# 5. Gemini LLM (LangChain)
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)

# 6. RetrievalQA chain
qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever(),
    return_source_documents=False
)

# 7. Interactive loop
while True:
    query = input("\nAsk me something (or 'exit' to quit): ").strip()
    if query.lower() in ("exit", "quit"):
        break
    result = qa.invoke(query)
    print("\nAnswer:", result)