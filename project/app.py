'''
# Names: Rosa Lisa Silipino, Jose Urrutia, Alberto Escalante
# Class: CS 578 Final Project
# File: app.py
# Description: This Flask-based web application provides a simple reminder management system.
It includes a REST API for adding, retrieving, and deleting reminders, with
reminders stored in a JSON file (`reminders.json`). The application supports
secure HTTPS communication and serves a web interface for user interaction.
# Key functionalities:
- GET reminders: Retrieve the list of reminders.
- POST reminders: Add a new reminder.
- DELETE reminders: Remove a specific reminder.
'''

from flask import Flask, render_template, request, jsonify
import json
import os

# Initialize the Flask Application.
app = Flask(__name__)

# File to store reminders
REMINDER_FILE = "reminders.json"

# Function to load reminders.
# This function checks if the file exists and loads its content.
# If the file is missing or corrupted, it returns an empty list.
def load_reminders():
    if os.path.exists(REMINDER_FILE):
        try:
            with open(REMINDER_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("reminders.json is empty or malformed. Initializing as an empty list.")
            return []
    return []


 #This function overwrites the reminders.json file with the latest reminders list.
def save_reminders(reminders):
    with open(REMINDER_FILE, "w") as f:
        json.dump(reminders, f)

# Route to display the web interface
@app.route("/")
def index():
    return render_template("index.html")

# Route to get reminders
@app.route("/reminders", methods=["GET"])
def get_reminders():
    reminders = load_reminders()
    return jsonify(reminders)

# Route to add a reminder
@app.route("/reminders", methods=["POST"])
def add_reminder():
    data = request.get_json()
    reminders = load_reminders()
    reminders.append(data["reminder"])
    save_reminders(reminders)
    return jsonify({"status": "success", "reminders": reminders})

# Route to delete a reminder
@app.route("/reminders", methods=["DELETE"])
def delete_reminder():
    data = request.get_json()
    reminders = load_reminders()
    reminders.remove(data["reminder"])
    save_reminders(reminders)
    return jsonify({"status": "success", "reminders": reminders})

if __name__ == "__main__":
    if __name__ == "__main__":
        app.run(host="0.0.0.0", port=5000, ssl_context=("/home/admin/cs578/cert.pem", "/home/admin/cs578/key.pem"))

