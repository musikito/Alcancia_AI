import os
import openai
from dotenv import load_dotenv
import time
import logging


# Load environment variables from .env file
load_dotenv()

# Get the API key from the environment variable
openai_api_key = os.getenv('OPEN_AI_KEY')
# openai.api_key = os.getenv.get("OPEN_AI_KEY")

client = openai.Client(
    api_key = openai_api_key,
)
## Model that we going to use
model = "gpt-4o"

## Create the assistant
# budget_assistant = client.beta.assistants.create(
#     name="Budget Assistant",
#     instructions="You are a financial expert assistant, creating budgets and financial advise for individuals. You have helped many people get out of debt and plan their retirement. Help them paying their debts and improve their credit score in the way of Dave Ramsey.",
#     model=model,
# )
# assistant_id = budget_assistant.id
# print(assistant_id)

# # Create the Thread
# thread = client.beta.threads.create(
#     messages=[{
#         "role": "user",
#         "content": "Create a budget for me.",
#     }],
# )
# thread_id = thread.id
# print(thread_id)

assistant_id = os.getenv('ASSISTANT_ID')
thread_id = os.getenv('THREAD_ID')


# Create the messages
# message = "How much money do I need to save to retire at 65?"
message = input("Ask me questions about how to improve your financial situation: ")
message = client.beta.threads.messages.create(
    thread_id=thread_id,
    role="user",
    content=message,
)

# Run the assistant
run = client.beta.threads.runs.create(
    assistant_id=assistant_id,
    thread_id=thread_id,
    instructions="You are a financial expert assistant, creating budgets and financial advise for individuals. You have helped many people get out of debt and plan their retirement. Help them paying their debts and improve their credit score in the way of Dave Ramsey.",
)
 ## helper function to do the runs
def wait_for_run_completion(client, thread_id, run_id, sleep_interval=5):
    """

    Waits for a run to complete and prints the elapsed time.:param client: The OpenAI client object.
    :param thread_id: The ID of the thread.
    :param run_id: The ID of the run.
    :param sleep_interval: Time in seconds to wait between checks.
    """
    while True:
        try:
            run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
            if run.completed_at:
                elapsed_time = run.completed_at - run.created_at
                formatted_elapsed_time = time.strftime(
                    "%H:%M:%S", time.gmtime(elapsed_time)
                )
                print(f"Run completed in {formatted_elapsed_time}")
                logging.info(f"Run completed in {formatted_elapsed_time}")
                # Get messages here once Run is completed!
                messages = client.beta.threads.messages.list(thread_id=thread_id)
                last_message = messages.data[0]
                response = last_message.content[0].text.value
                print(f"Assistant Response: {response}")
                break
        except Exception as e:
            logging.error(f"An error occurred while retrieving the run: {e}")
            break
        logging.info("Waiting for run to complete...")
        time.sleep(sleep_interval)


# === Run ===
wait_for_run_completion(client=client, thread_id=thread_id, run_id=run.id)

# ==== Steps --- Logs ==
# run_steps = client.beta.threads.runs.steps.list(thread_id=thread_id, run_id=run.id)
# print(f"Steps---> {run_steps.data[0]}")

