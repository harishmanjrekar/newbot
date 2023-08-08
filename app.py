from flask import Flask, render_template, request
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import Chroma
import openai

app = Flask(__name__)

# Initialize embedding model
embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

# Initialize Chroma vector index
db = Chroma(persist_directory="vector_index_directory")

# Set your OpenAI API key
openai.api_key = "YOUR_OPENAI_API_KEY"

@app.route("/", methods=["GET", "POST"])
def index():
    answer = None

    if request.method == "POST":
        user_query = request.form["query"]
        answer = search_or_generate_answer(user_query)

    return render_template("index.html", answer=answer)

def search_or_generate_answer(query):
    # Search for similar vectors in the Chroma index
    similar_vectors = db.retrieve_similar(embeddings.embed(query))

    if similar_vectors:
        # Retrieve answers based on similar vectors
        similar_answers = [db.retrieve(id)[0] for id in similar_vectors]
        return similar_answers
    else:
        # Use OpenAI API to generate answer
        generated_answer = generate_answer_with_openai(query)
        # Embed and store the generated answer in the Chroma index
        embedded_answer = embeddings.embed(generated_answer)
        db.insert({"generated_answer": embedded_answer})
        return [generated_answer]

def generate_answer_with_openai(query):
    # Call OpenAI API to generate answer
    response = openai.Completion.create(
        engine="davinci-codex",
        prompt=query,
        max_tokens=50
    )
    return response.choices[0].text.strip()

if __name__ == "__main__":
    app.run(debug=True)
