# webhook_receiver.py
from flask import Flask, request, jsonify
from data_processor import process_webhook_data
import os

def create_app():
    app = Flask(__name__)

    @app.route('/webhook', methods=['POST'])
    def webhook():
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data received'}), 400

        # Pass the data to the data processor
        result = process_webhook_data(data)

        if 'error' in result:
            return jsonify(result), 500
        else:
            return jsonify(result), 200

    return app