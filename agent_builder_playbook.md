# Agent Builder Playbook: Expense Support Agent

This playbook outlines the architectural design, tool structure, and extension guidelines for the Expense Customer Support Agent.

---

## 🏗️ Architecture Overview

The agent is built using the **Google Agent Development Kit (ADK)** and runs locally using **Google AI Studio (Gemini)** API keys.

```
AI_5days_Capstone_Project/
├── app/
│   ├── agent.py            # Agent definition, system instructions, and tool bindings
│   ├── db.py               # Mock database handling, policy data, CRUD operations
│   ├── expenses.json       # In-memory/file-based mock database storage
│   └── fast_api_app.py     # FastAPI server exposing the agent
└── tests/                  # Integration, unit, and end-to-end tests
```

---

## 🛠️ Tool Specifications

The agent is equipped with 4 primary tools defined in `app/db.py`:

### 1. `create_expense`
* **Purpose:** Creates a new expense claim.
* **Arguments:**
  * `description` (str): Text explaining what was purchased.
  * `amount` (float): Cost in USD.
  * `category` (str): Must be one of: `Meals`, `Lodging`, `Transport`, `Office Supplies`, `Entertainment`, `Other`.
  * `date` (str, optional): `YYYY-MM-DD` date. Defaults to current date if omitted.

### 2. `get_expenses`
* **Purpose:** Fetches list of expenses.
* **Arguments:**
  * `category` (str, optional): Filter by category.
  * `status` (str, optional): Filter by status (`Pending`, `Approved`, `Rejected`).

### 3. `get_expense_details`
* **Purpose:** Retrieves full details (including comments) of a specific expense by ID.
* **Arguments:**
  * `expense_id` (str): Unique identifier (e.g., `EXP-1001`).

### 4. `search_expense_policy`
* **Purpose:** Ground the model's responses to company policies.
* **Arguments:**
  * `query` (str): Category/keyword to search (e.g. `meals`, `hotel`, `limit`).

---

## 📝 System Instruction Strategy

The agent prompt in `app/agent.py` uses structured prompt engineering divided into clear phases:
1. **Role & Goal:** Explicitly declares it as an Expense Customer Support agent.
2. **Policy Inquiries:** Forces the agent to query the `search_expense_policy` tool before answering any policy questions.
3. **Filing Rules:** Restricts the agent from submitting incomplete claims. It must proactively ask the user for details if description, amount, or category are missing.
4. **Output formatting:** Standardizes formatting (lists and tables) for expense listings.

---

## 🚀 How to Extend the Agent

### 1. Adding a New Policy Category
To add support for a new category (e.g. `Education/Training`):
1. Open `app/db.py`.
2. Add your policy text to `POLICY_GUIDELINES`:
   ```python
   "education": "Annual training allowance is up to $1,000 per employee. Requires invoice and course completion certificate."
   ```
3. Update the description comments in the docstrings of `create_expense` to inform the model about the new category.

### 2. Adding a Manager Approval Tool
If you want to add support for approving claims:
1. Create a function in `app/db.py`:
   ```python
   def approve_expense(expense_id: str, manager_comment: str) -> dict:
       """Approves a pending expense claim.
       
       Args:
           expense_id: The ID of the expense (e.g., 'EXP-1002').
           manager_comment: Rejection reason or approval feedback.
       """
       # Update status in expenses.json to 'Approved' and save...
   ```
2. Bind the new function to `tools` list in `app/agent.py`.
