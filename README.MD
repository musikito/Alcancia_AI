# OpenAI Budget Assistant

This project is an asynchronous web assistant built using `aiohttp` that interacts with the OpenAI API to provide finance-related information and recommendations.

## Features

- Asynchronous handling of user queries.
- Interaction with OpenAI's GPT-4o model.
- Simple HTTP server to serve the frontend.

## Prerequisites

- Python 3.7 or higher
- OpenAI API key

## Setup

### Step 1: Clone the Repository

Clone this repository to your local machine:

```bash
git clone https://github.com/musikito/Alcancia_AI.git
```
### Step 2: Create and Activate a Virtual Environment 
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```
### Step 3: Install the required packages:
``` bash
pip install -r requirements.txt
```
### Step 4: Create a .env file and add your OpenAI API key:
```bash
OPEN_AI_KEY=your-openai-api-key
```
### Step 4: Run the application:
```bash
python app.py
```

