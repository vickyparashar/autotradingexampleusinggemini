from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Define prompt
prompt = PromptTemplate.from_template("Explain lion in one line.")

# Set up OllamaLLM
llm = OllamaLLM(model="gemma3:1b")  # pick a model you’ve pulled locally

# Parser
parser = StrOutputParser()

# Build the chain
chain = prompt | llm | parser

# Run it
response = chain.invoke({"concept": "webhooks"})
print(response)