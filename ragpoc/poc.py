import os
from pathlib import Path
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.docstore.document import Document
from langchain_ollama import OllamaLLM
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# 1. Set your API key
os.environ["GOOGLE_API_KEY"] = "AIzaSyDf9GjmDLWHlqmUI5nwHZ39xKVOk39kOh4"

# 2. Paths
file_path = r"C:\VickyJD\Tools\sampletool\ragpoc\data\datastore.txt"
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
    docs = [
        Document(page_content=line, metadata={"source": "datastore.txt", "line": i})
        for i, line in enumerate(lines, 1)
    ]
    vector_store = FAISS.from_documents(docs, embeddings)
    vector_store.save_local(str(index_path))
    print("✅ Index saved to disk.")

# 5. Load Ollama LLM
llm = OllamaLLM(model="gemma3:4b")  # Swap with mistral, llama3:8b, etc.

# 6. Custom prompt
prompt = PromptTemplate.from_template(
    "You are a helpful assistant. Use the following context to answer the question.\n\n{context}\n\nQuestion: {question}\nAnswer:"
)

# 7. Ask question
query = input("Ask me something: ")

# 8. Fallback loop with increasing k
fallback_k_values = [5, 10, 20]
final_answer = None
final_docs = []

for k in fallback_k_values:
    retriever = vector_store.as_retriever(search_kwargs={"k": k})
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": prompt},
        return_source_documents=True
    )
    response = qa_chain.invoke({"query": query})
    answer = response["result"].strip().lower()
    final_docs = response["source_documents"]

    # Check if answer is valid
    if answer and answer != "i don't know." and len(answer) > 10:
        final_answer = response["result"]
        break

# 9. Print final result
if final_answer:
    print("\n🧠 Answer from Ollama:\n", final_answer)
else:
    print("\n🤖 Fallback: No confident answer from LLM.")
    print("📄 Showing top retrieved document instead:\n")
    print(final_docs[0].page_content)

# 10. Print retrieved docs
print("\n📄 Retrieved Docs:")
for i, doc in enumerate(final_docs, 1):
    source = doc.metadata.get("source", "unknown")
    line = doc.metadata.get("line", "N/A")
    print(f"{i}. [Line {line}] {doc.page_content}")