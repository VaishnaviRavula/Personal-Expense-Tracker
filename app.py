import os
import sqlite3
from datetime import date
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-this-for-production")
DB_PATH = os.environ.get("DATABASE_PATH", os.path.join(os.path.dirname(__file__), "expenses.db"))
CATEGORIES = ["Food", "Transport", "Shopping", "Bills", "Education", "Health", "Entertainment", "Other"]

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    folder = os.path.dirname(DB_PATH)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                category TEXT NOT NULL,
                amount REAL NOT NULL CHECK(amount > 0),
                expense_date TEXT NOT NULL,
                notes TEXT DEFAULT ''
            )
        """)

@app.route("/")
def index():
    category = request.args.get("category", "").strip()
    month = request.args.get("month", "").strip()
    query = "SELECT * FROM expenses WHERE 1=1"
    params = []
    if category in CATEGORIES:
        query += " AND category = ?"
        params.append(category)
    if len(month) == 7 and month[4] == "-":
        query += " AND substr(expense_date, 1, 7) = ?"
        params.append(month)
    query += " ORDER BY expense_date DESC, id DESC"

    with get_db() as conn:
        expenses = conn.execute(query, params).fetchall()
        total = conn.execute("SELECT COALESCE(SUM(amount), 0) FROM expenses").fetchone()[0]
        month_total = conn.execute(
            "SELECT COALESCE(SUM(amount), 0) FROM expenses WHERE substr(expense_date, 1, 7) = ?",
            [date.today().strftime("%Y-%m")]
        ).fetchone()[0]
        category_rows = conn.execute("""
            SELECT category, SUM(amount) AS total
            FROM expenses
            WHERE substr(expense_date, 1, 7) = ?
            GROUP BY category ORDER BY total DESC
        """, [date.today().strftime("%Y-%m")]).fetchall()

    chart_labels = [row["category"] for row in category_rows]
    chart_values = [round(row["total"], 2) for row in category_rows]
    return render_template(
        "index.html", expenses=expenses, total=total, month_total=month_total,
        categories=CATEGORIES, selected_category=category, selected_month=month,
        chart_labels=chart_labels, chart_values=chart_values
    )

@app.route("/add", methods=["POST"])
def add_expense():
    title = request.form.get("title", "").strip()
    category = request.form.get("category", "")
    amount_text = request.form.get("amount", "").strip()
    expense_date = request.form.get("expense_date", "")
    notes = request.form.get("notes", "").strip()

    try:
        amount = float(amount_text)
    except (TypeError, ValueError):
        amount = 0

    if not title or category not in CATEGORIES or amount <= 0 or not expense_date:
        flash("Please enter a title, valid category, positive amount, and date.", "error")
        return redirect(url_for("index"))

    try:
        date.fromisoformat(expense_date)
    except ValueError:
        flash("Please choose a valid date.", "error")
        return redirect(url_for("index"))

    with get_db() as conn:
        conn.execute(
            "INSERT INTO expenses (title, category, amount, expense_date, notes) VALUES (?, ?, ?, ?, ?)",
            (title, category, amount, expense_date, notes)
        )
    flash("Expense added successfully.", "success")
    return redirect(url_for("index"))

@app.route("/delete/<int:expense_id>", methods=["POST"])
def delete_expense(expense_id):
    with get_db() as conn:
        conn.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    flash("Expense deleted.", "success")
    return redirect(url_for("index"))

@app.route("/health")
def health():
    return {"status": "ok"}

init_db()

if __name__ == "__main__":
    app.run(debug=True)
