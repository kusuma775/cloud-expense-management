from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.database import get_connection

app = FastAPI(title="Cloud Expense Management System")


class Expense(BaseModel):
    user_id: int
    category_id: int
    amount: float
    description: str
    expense_date: str


@app.get("/")
def home():
    return {
        "message": "Cloud Expense Management System is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.post("/expenses")
def add_expense(expense: Expense):

    connection = get_connection()
    cursor = connection.cursor()

    query = """
        INSERT INTO expenses
        (user_id, category_id, amount, description, expense_date)
        VALUES (%s, %s, %s, %s, %s)
    """

    values = (
        expense.user_id,
        expense.category_id,
        expense.amount,
        expense.description,
        expense.expense_date
    )

    cursor.execute(query, values)
    connection.commit()

    expense_id = cursor.lastrowid

    cursor.close()
    connection.close()

    return {
        "message": "Expense added successfully",
        "expense_id": expense_id
    }