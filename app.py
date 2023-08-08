from flask import Flask, render_template, request, jsonify
from azure.storage.blob import BlobServiceClient
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM 
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import Chroma
import openai

app = Flask(__name__)

# Replace with your actual Azure Blob Storage connection string
connection_string = "YOUR_AZURE_BLOB_CONNECTION_STRING"
container_name = "your-container-name"

# Initialize BlobServiceClient
blob_service_client = BlobServiceClient.from_connection_string(connection_string)

# Initialize tokenizer and model for LLM
checkpoint = "LaMini-T5-738M"
tokenizer = AutoTokenizer.from_pretrained(checkpoint)
base_model = AutoModelForSeq2SeqLM.from_pretrained(checkpoint)

# Initialize SentenceTransformer embeddings and Chroma vector store
embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
persist_directory = "vector_index"
db = Chroma(persist_directory=persist_directory, embedding_function=embeddings)

# Initialize OpenAI API key
openai.api_key = "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"

# Function to store data in Azure Blob Storage
def store_in_blob(data, filename):
    container_client = blob_service_client.get_container_client(container_name)
    blob_client = container_client.get_blob_client(filename)
    blob_client.upload_blob(data)

# Function to retrieve data from Azure Blob Storage
def retrieve_from_blob(filename):
    container_client = blob_service_client.get_container_client(container_name)
    blob_client = container_client.get_blob_client(filename)
    data = blob_client.download_blob().readall()
    return data

# Function to search for answer using Chroma
def search_answer_in_vector_database(question):
    retrieved_documents = db.retrieve([question])
    if retrieved_documents:
        retrieved_answer = list(retrieved_documents.values())[0]
        return retrieved_answer
    else:
        return None

# Function to generate answer using OpenAI API
def generate_answer_with_openai(question):
    response = openai.Completion.create(
        engine="davinci-codex", prompt=question, max_tokens=50
    )
    generated_text = response.choices[0].text.strip()
    return generated_text

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_question = request.form["user_question"]
        
        # Search for answer in the vector database
        answer = search_answer_in_vector_database(user_question)
        
        if answer:
            response = answer
        else:
            # Generate answer using OpenAI API and save it to the vector database
            generated_text = generate_answer_with_openai(user_question)
            response = generated_text
            db.store({user_question: generated_text})
        
        return jsonify({"response": response})
    
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
