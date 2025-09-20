from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from flask_cors import CORS
import pickle
import numpy as np
import os
import sys

# Initialize the Flask app
app = Flask(__name__)
# Enable CORS for the app to allow requests from different origins
CORS(app)

# Define the file path for the pickled model. 
# This makes it easier to change if the file location moves.
MODEL_FILE_PATH = 'healthcare_chatbot_model.pkl'

# Load the chatbot model once when the application starts
# This is a critical step to avoid reloading the model for every request.
# The try-except block ensures the app doesn't crash if the file is missing.
try:
    with open(MODEL_FILE_PATH, 'rb') as model_file:
        model = pickle.load(model_file)
    print("Chatbot model loaded successfully!")
except FileNotFoundError:
    print(f"Error: The model file '{MODEL_FILE_PATH}' was not found.")
    print("Please ensure the model file is in the same directory as app.py.")
    model = None
except Exception as e:
    print(f"An unexpected error occurred while loading the model: {e}")
    model = None

# A placeholder function to get a response from your model.
# You MUST replace this with your actual model's prediction logic.
# The `incoming_msg` variable is the text from the user.
def get_chatbot_response(incoming_msg):
    """
    This function processes the incoming user message and returns a chatbot response.
    
    Args:
        incoming_msg (str): The text message sent by the user.
        
    Returns:
        str: The response from the chatbot.
    """
    if not model:
        # Return a fallback message if the model failed to load
        return "I am sorry, the chatbot is currently unavailable."
    
    try:
        # In a real-world scenario, you would preprocess the incoming message
        # (e.g., lowercase, remove punctuation) and then feed it to your model.
        
        # This is a placeholder for your actual model's prediction logic.
        # For example, if your model classifies intents:
        # intent = model.predict(preprocess(incoming_msg))
        # response = get_response_for_intent(intent)
        
        # For this example, we'll return a simple, conversational response.
        if "fever" in incoming_msg.lower() or "flu" in incoming_msg.lower():
            return "A fever can be a sign of many things, including the flu. I am not a doctor. Please consult a healthcare professional for a proper diagnosis."
        elif "headache" in incoming_msg.lower():
            return "Headaches can have various causes. If it is severe or persistent, please seek medical advice."
        elif "help" in incoming_msg.lower() or "hi" in incoming_msg.lower():
            return "Hello! I am Veda, your healthcare assistant. How can I help you today?"
        else:
            return "I can provide general information about common diseases. What are your symptoms?"
            
    except Exception as e:
        print(f"Error during chatbot response generation: {e}")
        return "I am unable to process that message right now. Please try again later."


# The webhook endpoint that Twilio will send requests to.
# This function receives and handles all incoming messages.
@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    """
    Handles incoming messages from Twilio.
    """
    # Print a message to the console to confirm a request was received
    print("Webhook received a new request.")
    
    # Get the incoming message body from the POST request
    # Twilio sends data as form-urlencoded, which Flask accesses via request.values
    incoming_msg = request.values.get('Body', None)
    
    # Get the sender's number for potential logging or tracking
    sender_number = request.values.get('From', None)
    
    print(f"Message received from {sender_number}: '{incoming_msg}'")
    
    # Create a TwiML response object
    resp = MessagingResponse()
    
    # Check if a message was actually received
    if incoming_msg is None:
        print("Error: No message body received in the webhook.")
        resp.message("An error occurred. No message received.")
        return str(resp)

    # Get the chatbot's response
    chatbot_response = get_chatbot_response(incoming_msg)
    
    # Add the chatbot's response to the TwiML object
    resp.message(chatbot_response)
    
    print(f"Replying with: '{chatbot_response}'")
    
    # Return the TwiML response as a string
    return str(resp)

if __name__ == "__main__":
    # Run the Flask app
    # host='0.0.0.0' makes the app accessible on your network, crucial for ngrok.
    # port=5000 is the standard Flask port, matching your ngrok tunnel.
    # debug=True provides helpful error messages during development.
    app.run(host='0.0.0.0', port=5000, debug=True)