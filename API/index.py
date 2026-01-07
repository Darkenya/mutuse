import os
from flask import Flask, render_template, request, jsonify
from intasend import APIService

app = Flask(__name__, template_folder='../templates')

# CONFIGURATION - Use your keys from IntaSend Sandbox
# In Vercel, we set these in the dashboard settings later
API_PUBLISHABLE_KEY = os.getenv("ISPubKey_test_8b8b0b11-e054-4629-8d11-b6e33488befb", "ISPubKey_test_8b8b0b11-e054-4629-8d11-b6e33488befb")
API_TOKEN = os.getenv("ISSecretKey_test_34c570cf-0024-4d97-9f02-11d573113bcf", "ISSecretKey_test_34c570cf-0024-4d97-9f02-11d573113bcf")

service = APIService(token=API_TOKEN, publishable_key=API_PUBLISHABLE_KEY, test=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/initiate-payment', methods=['POST'])
def initiate_payment():
    data = request.json
    phone = data.get('phone')
    amount = data.get('amount')

    try:
        response = service.collect.mpesa_stk_push(
            phone_number=phone,
            amount=amount,
            narrative="Fuliza Boost Fee"
        )
        return jsonify({"success": True, "response": response}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

# Required for Vercel
if __name__ == "__main__":
    app.run()