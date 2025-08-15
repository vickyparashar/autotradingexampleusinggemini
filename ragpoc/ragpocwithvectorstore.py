import os
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document
from langchain.chains import RetrievalQA

# 1. API key
os.environ["GOOGLE_API_KEY"] = "AIzaSyDf9GjmDLWHlqmUI5nwHZ39xKVOk39kOh4"


# 2. Load documents from datastore.txt
docs = []
with open("datastore.txt", "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if line:  # skip blank lines
            docs.append(Document(page_content=line))

# 3. Create embeddings & FAISS store
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
vectorstore = FAISS.from_documents(docs, embeddings)

# 4. Gemini LLM
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)

# 5. RetrievalQA chain
qa = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectorstore.as_retriever(),
    return_source_documents=False
)

# 6. Ask a question interactively
query = input("Ask me something: ")
result = qa.invoke(query)   # ✅ updated to avoid deprecation warning

# 7. Show answer + sources
print("\nAnswer:", result["result"])
print("\nSources:")
