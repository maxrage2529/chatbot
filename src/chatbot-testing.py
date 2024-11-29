
def detect_intent_with_texts(project_id, agent_id, session_id, texts, language_code):
    # Set the endpoint (use regional endpoint if needed)
    client_options = {"api_endpoint": f"{LOCATION}-dialogflow.googleapis.com"}

    # Create a session client
    session_client = dialogflowcx.SessionsClient(client_options=client_options)

    # Format the session path
    session_path = session_client.session_path(project_id, LOCATION, agent_id, session_id)
    print(f"Session path: {session_path}")

    # Loop over each user input (text) and send it to the agent
    for text in texts:
        text_input = dialogflowcx.TextInput(text=text)
        query_input = dialogflowcx.QueryInput(text=text_input, language_code=language_code)

        # Make the request to detect intent
        request = dialogflowcx.DetectIntentRequest(
            session=session_path,
            query_input=query_input,
        )
        response = session_client.detect_intent(request=request)

        # Print the results
        query_result = response.query_result
        print(f"Query text: {query_result.text}")
        print(f"Response text: {query_result.response_messages[0].text.text}")

if __name__ == "__main__":

    import os
    from google.cloud import dialogflowcx_v3beta1 as dialogflowcx
    import uuid
    # Set your Google Cloud project ID and agent details
    PROJECT_ID = "chatbot-poc-436512"  # Replace with your Google Cloud Project ID
    AGENT_ID = "7df5273f-ca07-4a6f-90cc-5b194c3efaba"     # Replace with your Dialogflow CX Agent ID
    LOCATION = "europe-west1"             # Location, e.g., "global" or "us-central1"
    SESSION_ID = str(uuid.uuid4()) # Session ID (unique for each user/session)
    LANGUAGE_CODE = "en"            # Language code, e.g., "en"
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "D:/Projects/gcpServiceAccounts/chatbot-poc-436512-4e6f37b2acac.json"
    # Define user inputs
    texts = ["what is fog computing"]

    # Call the function with the specified parameters
    detect_intent_with_texts(PROJECT_ID, AGENT_ID, SESSION_ID, texts, LANGUAGE_CODE)
