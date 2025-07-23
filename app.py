
from flask import Flask, request, render_template
import openai

app = Flask(__name__)

openai.api_key = "YOUR_OPENAI_API_KEY"

po_data = {
    "4500122023": {"status": "Delivered", "amount": "₹2,34,000", "vendor": "Tata Steel"},
    "4500122024": {"status": "Pending Approval", "amount": "₹1,50,000", "vendor": "L&T"},
}

@app.route('/', methods=['GET', 'POST'])
def chatbot():
    response = ""
    if request.method == 'POST':
        user_input = request.form['user_input']
        po_id = next((word for word in user_input.split() if word.isdigit() and word in po_data), None)
        if po_id:
            info = po_data[po_id]
            response = f"PO {po_id}: {info['status']} | Vendor: {info['vendor']} | Amount: {info['amount']}"
        else:
            openai_resp = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": f"Answer like a SAP assistant: {user_input}"}]
            )
            response = openai_resp['choices'][0]['message']['content']
    return render_template('chat.html', response=response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    