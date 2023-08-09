from flask import Flask, request, jsonify
import openai

app = Flask(__name__)

# Set your OpenAI API key here
openai.api_key = "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"

@app.route('/get_answer', methods=['POST'])
def get_answer():
    user_input = request.json['user_input']
    
    response = openai.Completion.create(
        engine="curie",
        prompt=user_input,
        max_tokens=200  # Adjust as needed
    )
    
    answer = response.choices[0].text.strip()
    return jsonify({"answer": answer})

if __name__ == '__main__':
    app.run()
