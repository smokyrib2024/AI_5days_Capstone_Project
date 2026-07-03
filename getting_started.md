# Getting Started: Expense Customer Support Agent

This guide provides instructions on how to set up, run, and test the Expense Customer Support Agent on your local machine.

---

## 🛠️ Prerequisites

Make sure you have `uv` installed. If you don't, install it following the [Astral UV installation guide](https://docs.astral.sh/uv/getting-started/installation/).

`agents-cli` is also required. You can install it using:
```bash
uv tool install google-agents-cli
```

---

## 🚀 Setup Instructions

1. **Environment Variables Configuration (.env)**
   Ensure you have a `.env` file at the root of the project containing your Google AI Studio API key:
   ```env
   GEMINI_API_KEY=your_google_ai_studio_api_key
   GOOGLE_API_KEY=your_google_ai_studio_api_key
   ```

2. **Install Dependencies**
   Run the following command at the root of the project to initialize the virtual environment and install all packages:
   ```bash
   agents-cli install
   ```

---

## 💬 Running the Agent

### 1. Web Playground (Interactive Chat)
To open a beautiful web-based chat interface to talk to your agent:
```bash
agents-cli playground
```
This will spin up a local server and give you a link (usually [http://127.0.0.1:8080](http://127.0.0.1:8080)) to open in your browser.

### 2. Single-Turn CLI Prompts
You can query the agent directly from the command line using single quotes:
* **Check a policy rule:**
  ```bash
  agents-cli run 'what is the daily limit for hotel stays?'
  ```
* **File a new expense claim:**
  ```bash
  agents-cli run 'file an expense of $45.50 for dinner under Meals today'
  ```
* **List existing expenses:**
  ```bash
  agents-cli run 'list my current expenses'
  ```

---

## 🧪 Testing and Linting

* **Run Pytest Suite:**
  To execute all unit and integration tests:
  ```bash
  uv run pytest
  ```
* **Run Lint and Formatting Checks:**
  To ensure the code is clean and compliant:
  ```bash
  agents-cli lint
  ```
