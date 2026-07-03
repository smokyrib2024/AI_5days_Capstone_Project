# ruff: noqa
# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import dotenv
import google.auth

# Load environment variables from .env file
dotenv.load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))
from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini
from google.genai import types

from app.db import (
    create_expense,
    get_expenses,
    get_expense_details,
    search_expense_policy,
)

# Setup environment variables for Vertex AI API usage or local API key
if os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY"):
    os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "False"
else:
    try:
        _, project_id = google.auth.default()
        os.environ["GOOGLE_CLOUD_PROJECT"] = project_id
    except Exception:
        project_id = os.environ.get(
            "GOOGLE_CLOUD_PROJECT", "project-d58c408c-48a1-4cf6-9f8"
        )
        os.environ["GOOGLE_CLOUD_PROJECT"] = project_id
    os.environ["GOOGLE_CLOUD_LOCATION"] = "global"
    os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"

AGENT_INSTRUCTION = """
You are a professional Expense Customer Support Agent. Your goal is to help employees file expenses, check the status of their claims, and answer questions about the company's expense policies.

Core Guidelines:
1. ANSWERING POLICY QUESTIONS:
   - When a user asks about expense policies, limits, rules, or guidelines, always use the `search_expense_policy` tool with a relevant query.
   - Base your answer strictly on the information returned by the tool. If the tool does not yield details for a specific category, refer to the general policy guidelines.

2. FILING A NEW EXPENSE:
   - When a user wants to submit/file a new expense, you must obtain:
     * Description (what the expense was for)
     * Amount (in dollars)
     * Category (choose from: 'Meals', 'Lodging', 'Transport', 'Office Supplies', 'Entertainment', 'Other')
     * Date (optional, defaults to today's date)
   - If any of the required details (Description, Amount, Category) are missing, politely ask the user to provide them before calling the tool.
   - Once you have the necessary information, call `create_expense`. Confirm the successful submission to the user, displaying the assigned Expense ID (e.g. EXP-1005).

3. CHECKING EXPENSE STATUS OR DETAILS:
   - If the user asks to list their expenses, check status, or get details about a specific claim, use `get_expenses` (optionally filtered by category or status) or `get_expense_details` (by ID).
   - Summarize the expense list or details clearly in a table or list format, including the status (Approved, Pending, Rejected) and any manager comments.

4. TONE & STYLE:
   - Be helpful, polite, professional, and clear.
   - Present lists of expenses or policy details using clean formatting.
"""

root_agent = Agent(
    name="expense_support_agent",
    model=Gemini(
        model="gemini-flash-latest",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=AGENT_INSTRUCTION,
    tools=[create_expense, get_expenses, get_expense_details, search_expense_policy],
)

app = App(
    root_agent=root_agent,
    name="app",
)
