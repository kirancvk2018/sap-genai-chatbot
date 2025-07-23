
from flask import Flask, request, jsonify
import re

app = Flask(__name__)

# Mock database for PO details
purchase_orders = {
    "4500000001": {
        "status": "Created",
        "supplier": "USSU-VSF04",
        "currency": "USD",
        "items": [
            {"material": "MZ-RM-R300-01", "desc": "BKR-300 Frame", "qty": 49, "net_price": 1730.19},
            {"material": "MZ-RM-R300-02", "desc": "BKR-300 Handle Bars", "qty": 49, "net_price": 86.51},
            {"material": "MZ-RM-R300-03", "desc": "BKR-300 Seat", "qty": 49, "net_price": 86.51}
        ]
    }
}

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "").strip().lower()

    if user_input == "hi":
        return jsonify({"response": "Hi how can I help you"})

    # Extract PO number
    match = re.search(r'po\s*(\d{10})', user_input, re.IGNORECASE)
    if match:
        po_number = match.group(1)
        po_data = purchase_orders.get(po_number)
        if po_data:
            return jsonify({
                "response": f"PO {po_number} is currently in '{po_data['status']}' status for supplier {po_data['supplier']} with {len(po_data['items'])} items."
            })
        else:
            return jsonify({
                "response": f"No PO found for order number {po_number}."
            })

    return jsonify({
        "response": "Please ask a valid question like 'What’s the status of PO 4500000001?' or say 'hi'."
    })

if __name__ == "__main__":
    app.run(debug=True)
