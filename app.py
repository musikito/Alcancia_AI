from flask import Flask, request, jsonify
import os
import openai
from dotenv import load_dotenv
import time
import logging

# Load environment variables from .env file
load_dotenv()

# Get the API key from the environment variable
openai_api_key = os.getenv('OPEN_AI_KEY')
openai.api_key = openai_api_key

# Helper function to do the runs
def wait_for_run_completion(client, thread_id, run_id, sleep_interval=5):
  """
  Waits for a run to complete and returns the assistant response.

  Args:
      client: The OpenAI client object.
      thread_id: The ID of the thread.
      run_id: The ID of the run.
      sleep_interval: Time in seconds to wait between checks.

  Returns:
      The assistant response from the last message or None if error occurs.
  """
  while True:
    try:
      run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
      if run.completed_at:
        messages = client.beta.threads.messages.list(thread_id=thread_id)
        last_message = messages.data[0]
        response = last_message.content[0].text.value
        return response
    except Exception as e:
      logging.error(f"An error occurred while retrieving the run: {e}")
      return None
    logging.info("Waiting for run to complete...")
    time.sleep(sleep_interval)

# Initialize Flask app
app = Flask(__name__)

# Assistant and Thread IDs (assuming these are pre-created and stored)
assistant_id = os.getenv('ASSISTANT_ID')
thread_id = os.getenv('THREAD_ID')

client = openai.Client(
    api_key = openai_api_key,
)

# Route to handle user questions
@app.route("/ask", methods=["POST"])
def ask_assistant():
  # Get user question from request body
  data = request.get_json()
  if not data or "question" not in data:
    return jsonify({"error": "Missing question in request body"}), 400

  user_question = data["question"]

  # Create message for the thread
  message = client.beta.threads.messages.create(
      thread_id=thread_id,
      role="user",
      content=user_question,
  )

  # Run the assistant
  run = client.beta.threads.runs.create(
      assistant_id=assistant_id,
      thread_id=thread_id,
      instructions="You are a financial expert assistant, creating budgets and financial advise for individuals. You have helped many people get out of debt and plan their retirement. Help them paying their debts and improve their credit score in the way of Dave Ramsey.",
  )

  # Wait for run completion and get response
  assistant_response = wait_for_run_completion(client, thread_id, run.id)

  if assistant_response:
    return jsonify({"response": assistant_response}), 200
  else:
    return jsonify({"error": "Error occurred during assistant interaction"}), 500

# Run the Flask app
if __name__ == "__main__":
  logging.basicConfig(level=logging.INFO)
  app.run(debug=True)
