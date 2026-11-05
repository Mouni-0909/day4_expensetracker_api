
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Only two categories
categories = ["Food", "Shopping"]

# Two lists to store data
expenses = []
budgets = []

# Expense input
class Expense(BaseModel):
    title: str
    amount: float
    category: str

# Budget input
class Budget(BaseModel):
    category: str
    amount: float


@app.get("/")
def home():
    return {"message": "Welcome to My Expense Tracker"}


# Add budget
@app.post("/add_budget")
def add_budget(budget: Budget):

    if budget.category not in categories:
        return {"message": "Only Food and Shopping categories are allowed"}

    budget_details = {
        "category": budget.category,
        "amount": budget.amount
    }

    budgets.append(budget_details)

    return {
        "message": "Budget added successfully",
        "budget": budget_details
    }


# Add expense
@app.post("/add_expense")
def add_expense(expense: Expense):

    if expense.category not in categories:
        return {"message": "Only Food and Shopping categories are allowed"}

    expense_details = {
        "id": len(expenses) + 1,
        "title": expense.title,
        "amount": expense.amount,
        "category": expense.category
    }

    expenses.append(expense_details)

    return {
        "message": "Expense added successfully",
        "expense": expense_details
    }


# View all expenses
@app.get("/expenses")
def view_expenses():
    return {"expenses": expenses}


# View all budgets
@app.get("/budgets")
def view_budgets():
    return {"budgets": budgets}


# Calculate total expenses
@app.get("/total")
def total_expenses():

    total = 0

    for expense in expenses:
        total = total + expense["amount"]

    return {"total_spent": total}


# Category-wise expense summary
@app.get("/expense_summary")
def expense_summary():

    summary = []

    for category in categories:

        spent = 0
        budget_amount = 0

        for expense in expenses:
            if expense["category"] == category:
                spent = spent + expense["amount"]

        for budget in budgets:
            if budget["category"] == category:
                budget_amount = budget_amount + budget["amount"]

        balance = budget_amount - spent

        summary.append({
            "category": category,
            "budget": budget_amount,
            "spent": spent,
            "remaining": balance
        })

    return {"summary": summary}
