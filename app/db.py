import json
import os
from datetime import datetime

DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "expenses.json")

# Pre-populated mock policy guidelines
POLICY_GUIDELINES = {
    "meals": (
        "Daily meal allowance is capped at $75 per day total across breakfast, lunch, and dinner. "
        "Detailed receipts are required for any single meal exceeding $25. "
        "Alcohol is strictly non-reimbursable and must be itemized out of meal receipts."
    ),
    "lodging": (
        "Standard lodging allowance is up to $250 per night. "
        "Any hotel bookings exceeding $250 per night require pre-approval from your manager. "
        "Itemized hotel folios must be uploaded with the expense claim."
    ),
    "transport": (
        "Flights must be booked in economy/coach class. Business or first-class flights are not allowed without executive exception. "
        "Taxi, rideshare (Uber/Lyft), and public transit are fully reimbursable. "
        "Rideshare claims exceeding $50 require a receipt. "
        "Personal vehicle mileage is reimbursed at $0.65 per mile; odometer readings or Google Maps route screenshot must be provided."
    ),
    "entertainment": (
        "Client entertainment or team building events require pre-approval. "
        "A list of all attendees and their company affiliations must be included in the expense description. "
        "The limit is $100 per person."
    ),
    "office supplies": (
        "Home office equipment or general office supplies are reimbursable up to $200 per year. "
        "Receipts are mandatory for all equipment/supplies claims."
    ),
    "general": (
        "All expenses must be submitted within 30 days of the transaction date. "
        "Receipts are mandatory for all claims exceeding $25, except for mileage and public transit under $10. "
        "Standard processing time for reimbursement is 5 to 7 business days once approved by your manager."
    ),
}

# Pre-populated mock expenses
DEFAULT_EXPENSES = [
    {
        "id": "EXP-1001",
        "description": "Team lunch at Mario's Pizzeria",
        "amount": 124.50,
        "category": "Meals",
        "date": "2026-06-15",
        "status": "Approved",
        "comment": "Manager approved. Attendees listed: 5 team members.",
    },
    {
        "id": "EXP-1002",
        "description": "Taxi ride to JFK airport",
        "amount": 65.00,
        "category": "Transport",
        "date": "2026-06-20",
        "status": "Pending",
        "comment": "Waiting for receipt verification.",
    },
    {
        "id": "EXP-1003",
        "description": "Hotel stay at Hyatt Regency (2 nights)",
        "amount": 490.00,
        "category": "Lodging",
        "date": "2026-06-22",
        "status": "Approved",
        "comment": "Under the $250/night limit.",
    },
    {
        "id": "EXP-1004",
        "description": "Premium noise-canceling headphones",
        "amount": 299.99,
        "category": "Office Supplies",
        "date": "2026-06-28",
        "status": "Rejected",
        "comment": "Exceeds the $200 yearly home office supplies limit.",
    },
]


def load_expenses() -> list[dict]:
    """Loads expenses from the JSON database file, initializing it if necessary."""
    if not os.path.exists(DB_FILE):
        save_expenses(DEFAULT_EXPENSES)
        return DEFAULT_EXPENSES
    try:
        with open(DB_FILE) as f:
            return json.load(f)
    except Exception:
        return DEFAULT_EXPENSES


def save_expenses(expenses: list[dict]):
    """Saves expenses to the JSON database file."""
    with open(DB_FILE, "w") as f:
        json.dump(expenses, f, indent=2)


def create_expense(
    description: str, amount: float, category: str, date: str | None = None
) -> dict:
    """Creates a new expense record in the database.

    Args:
        description: Description of the expense (e.g. 'Dinner with client').
        amount: Total cost in dollars (e.g. 45.50).
        category: Category of expense. Allowed: 'Meals', 'Lodging', 'Transport', 'Office Supplies', 'Entertainment', 'Other'.
        date: Date in YYYY-MM-DD format. Defaults to today's date if not specified.

    Returns:
        The created expense dict.
    """
    expenses = load_expenses()

    # Generate unique ID
    new_id = f"EXP-{len(expenses) + 1001}"

    if not date:
        date = datetime.now().strftime("%Y-%m-%d")

    new_expense = {
        "id": new_id,
        "description": description,
        "amount": round(float(amount), 2),
        "category": category,
        "date": date,
        "status": "Pending",
        "comment": "Submitted via Expense Support Agent.",
    }

    expenses.append(new_expense)
    save_expenses(expenses)
    return new_expense


def get_expenses(category: str | None = None, status: str | None = None) -> list[dict]:
    """Retrieves list of expenses, optionally filtered by category or status.

    Args:
        category: Filter by category (e.g. 'Meals', 'Transport'). Optional.
        status: Filter by status (e.g. 'Pending', 'Approved', 'Rejected'). Optional.

    Returns:
        A list of matching expense dicts.
    """
    expenses = load_expenses()
    filtered = expenses
    if category:
        filtered = [e for e in filtered if e["category"].lower() == category.lower()]
    if status:
        filtered = [e for e in filtered if e["status"].lower() == status.lower()]
    return filtered


def get_expense_details(expense_id: str) -> dict:
    """Retrieves full details of a specific expense by its ID.

    Args:
        expense_id: The unique ID of the expense (e.g., 'EXP-1001').

    Returns:
        A dictionary containing the expense details, or an error message if not found.
    """
    expenses = load_expenses()
    for e in expenses:
        if e["id"].lower() == expense_id.strip().lower():
            return e
    return {"error": f"Expense with ID {expense_id} not found."}


def search_expense_policy(query: str) -> str:
    """Searches the company expense policy for a given topic or keyword.

    Args:
        query: Keyword or topic to query (e.g. 'meals', 'hotel', 'mileage', 'limits').

    Returns:
        A text explanation of the corresponding policy.
    """
    query_lower = query.lower()
    matches = []
    for key, text in POLICY_GUIDELINES.items():
        if key in query_lower or query_lower in key:
            matches.append(f"[{key.capitalize()} Policy]: {text}")

    if not matches:
        # Check general guidelines as fallback
        return f"[General Policy]: {POLICY_GUIDELINES['general']}"

    return "\n\n".join(matches)
