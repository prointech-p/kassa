import requests
import json
from flask import Flask, request, send_file, jsonify
import os
from dotenv import load_dotenv
from paykassa import PayKassa


load_dotenv()  # Загружает переменные из .env


app = Flask(__name__)
app.config['PAYKASSA_SCI_ID'] = os.environ.get('PAYKASSA_SCI_ID', 'ID123456')
app.config['PAYKASSA_SCI_KEY'] = os.environ.get('PAYKASSA_SCI_KEY', 'KEY123456')
app.config['PAYKASSA_DOMAIN'] = os.environ.get('PAYKASSA_DOMAIN', 'DOMAIN123456')


@app.route('/paykassa-pro-link', methods=['GET', 'POST'])
def get_paykassa_pro_link():
    paykassa = PayKassa(
        sci_id=app.config['PAYKASSA_SCI_ID'] ,
        sci_key=app.config['PAYKASSA_SCI_KEY'],
        domain=app.config['PAYKASSA_DOMAIN'],
        test=True
    )

    # Generate payment link
    response = paykassa.sci_create_order(
        order_id="12345",
        amount="100",
        currency="BTC",
        system=11,  # BTC
        comment="Test payment"
    )

    print(response['data']['url'])
    print(response)  # Check response for payment URL
    return jsonify(response)


@app.route('/paykassa_confirm', methods=['GET', 'POST'])
def paykassa_confirm():
    # Read GET parameters
    get_params = request.args.to_dict()

    # Read POST parameters (form data)
    post_params = request.form.to_dict()

    # Read JSON data if sent as JSON
    json_data = request.get_json(silent=True)  # Returns None if no JSON data

    # Print parameters for debugging
    print("GET Params:", get_params)
    print("POST Params:", post_params)
    print("JSON Data:", json_data)

    return jsonify({
        "GET Params": get_params,
        "POST Params": post_params,
        "JSON Data": json_data
    })


@app.route('/')
def hello_world():
    return 'Hello from Flask!'


if __name__ == "__main__":
    app.run(debug=True)
