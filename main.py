from flask import Flask, request, jsonify
import os
import openai
from dotenv import load_dotenv
import time


# Load environment variables from .env file
load_dotenv()

# Get the API key from the environment variable
openai_api_key = os.getenv('OPEN_AI_KEY')
client = openai.Client(
    api_key = openai_api_key,
)

# Pre-defined Assistant and Thread IDs (replace with yours)
assistant_id = "asst_YOUR_ASSISTANT_ID"  # Replace with your assistant ID
thread_id = "thread_YOUR_THREAD_ID"     # Replace with your thread ID

# Model (consider using a config file)
model = "gpt-4o"

app = Flask(__name__)

## helper function to do the runs
def wait_for_run_completion(client, thread_id, run_id):
    """
    Waits for a run to complete and returns the assistant's response.

    Args:
        client: The OpenAI client object.
        thread_id: The ID of the thread.
        run_id: The ID of the run.

    Returns:
        The assistant's response as a string.
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
            print(f"An error occurred while retrieving the run: {e}")
            return "An error occurred. Please try again later."
        time.sleep(5)

"""
Serves the HTML page for user interaction.
"""
@app.route("/", methods=["GET"])
def index():
  return app.send_static_file("index.html")

"""
Receives a user's question from a web form, sends it to an OpenAI assistant, and returns the assistant's response as JSON.

This route handles POST requests to the "/ask" endpoint. It retrieves the user's question from the request body, creates a message for the assistant in the specified thread, creates a run for the assistant to generate a response, and waits for the run to complete. Once the response is available, it is returned as a JSON response.

Args:
    user_question (str): The question submitted by the user.

Returns:
    dict: A JSON response containing the assistant's response.
"""
@app.route("/ask", methods=["POST"])
def ask():
  """
  Receives user question from the web form and sends it to the assistant.
  Returns the assistant's response as JSON.
  """
  user_question = request.json["question"]
  message = client.beta.threads.messages.create(
      thread_id=thread_id,
      role="user",
      content=user_question,
  )
  run = client.beta.threads.runs.create(
      assistant_id=assistant_id,
      thread_id=thread_id,
      instructions="You are a financial expert assistant, creating budgets and financial advise for individuals. You have helped many people get out of debt and plan their retirement. Help them paying their debts and improve their credit score in the way of Dave Ramsey.",
  )
  assistant_response = wait_for_run_completion(client, thread_id, run.id)
  return jsonify({"response": assistant_response})

if __name__ == "__main__":
  app.run(debug=True)

