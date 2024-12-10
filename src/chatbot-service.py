from flask import Flask, request, jsonify
from google.cloud import dialogflowcx_v3beta1 as dialogflowcx
import os

# Initialize Flask app
app = Flask(__name__)

# Set project details
PROJECT_ID = "your-project-id"
LOCATION = "your-region"  # e.g., "us-central1"
AGENT_ID = "your-agent-id"

# Create a Dialogflow CX session client
def create_session_client():
    try:
        session_client = dialogflowcx.SessionsClient()
        session_path = session_client.session_path(
            project=PROJECT_ID,
            location=LOCATION,
            agent=AGENT_ID,
            session="local-session"  # Unique session ID for your local service
        )
        return session_client, session_path
    except Exception as e:
        print(f"Failed to create session client: {e}")
        return None, None

# Handle Dialogflow CX interactions
def detect_intent_text(session_client, session_path, text, language_code="en"):
    try:
        text_input = dialogflowcx.TextInput(text=text)
        query_input = dialogflowcx.QueryInput(text=text_input, language_code=language_code)

        response = session_client.detect_intent(
            session=session_path,
            query_input=query_input
        )
        return {
            "query_text": response.query_result.text,
            "response_text": response.query_result.response_messages[0].text.text[0],
            "confidence": response.query_result.match.confidence
        }
    except Exception as e:
        print(f"Error detecting intent: {e}")
        return {"error": str(e)}

# Flask route for chatting with Dialogflow CX
@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message", "")
    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    session_client, session_path = create_session_client()
    if not session_client or not session_path:
        return jsonify({"error": "Failed to create Dialogflow session client"}), 500

    # Get response from Dialogflow CX
    response = detect_intent_text(session_client, session_path, user_input)
    return jsonify(response)

# Run the Flask app
if __name__ == "__main__":
    # Ensure authentication credentials are set
    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        print("Please set the GOOGLE_APPLICATION_CREDENTIALS environment variable.")
        exit(1)

    app.run(host="0.0.0.0", port=5000)


# curl -X POST -H "Content-Type: application/json" \
#                 -d '{"message": "Hello"}' http://localhost:5000/chat