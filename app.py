
from flask import Flask, request, render_template
import openai
import os

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/', methods=['GET', 'POST'])
def chatbot():
    response = ""
    if request.method == 'POST':
        user_input = request.form['user_input'].strip().lower()

        if user_input == "hi":
            response = "Hi, how can I help?"
        elif user_input == "what’s the status of po 4500122023?" or user_input == "what is the status of po 4500122023?":
            response = "Delivered, Vendor: Tata Steel, ₹2,34,000"
        else:
            try:
                openai_resp = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": f"Answer like a SAP assistant: {user_input}"}]
                )
                response = openai_resp['choices'][0]['message']['content']
            except Exception as e:
                response = "Sorry, I couldn't process that right now. Please try again later."

    return render_template('chat.html', response=response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
