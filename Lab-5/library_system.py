"""Campus library tracker: loans, fines and renewals."""
import ast
import json
import operator
from datetime import datetime

# Global state
loans = {}
loan_dates = {}
FINE_PER_DAY = 2


def add_book_loan(student_id, book_id):
    """Record a loan; return True if stored, False if input is invalid."""
    if not student_id or not isinstance(book_id, str):
        print(f"Rejected loan: student={student_id!r}, book={book_id!r}")
        return False
    loan_dates.setdefault(student_id, []).append(str(datetime.now()))
    loans[student_id] = loans.get(student_id, []) + [book_id]
    print(f"{student_id} borrowed {book_id} "
          f"(loan dates on record: {len(loan_dates[student_id])})")
    return True


def return_book(student_id, book_id):
    """Remove a book from a student's loans, reporting unknown loans."""
    try:
        loans[student_id].remove(book_id)
        if len(loans[student_id]) == 0:
            del loans[student_id]
    except (KeyError, ValueError):
        print(f"No loan of {book_id} for {student_id} on record")


def calculate_fine(days_overdue):
    """Return the fine for days_overdue; never negative."""
    return max(days_overdue, 0) * FINE_PER_DAY


def renew_book(student_id, book_id, extra_days):
    """Announce a renewal; the fine rate is not changed by renewals."""
    print(f"Renewed {book_id} for {student_id} by {extra_days} days")


def load_records(file="loans.json"):
    """Load loan records from a JSON file."""
    with open(file, "r", encoding="utf-8") as handle:
        loans.clear()
        loans.update(json.load(handle))


def save_records(file="loans.json"):
    """Save loan records to a JSON file."""
    with open(file, "w", encoding="utf-8") as handle:
        json.dump(loans, handle)


_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}


def _eval_node(node, days):
    """Evaluate a whitelisted arithmetic AST node."""
    if isinstance(node, ast.Expression):
        return _eval_node(node.body, days)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.Name) and node.id == "days":
        return days
    if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](
            _eval_node(node.left, days), _eval_node(node.right, days))
    raise ValueError("unsupported fine rule")


def fine_from_rule(rule, days):
    """Evaluate an arithmetic fine rule in terms of days, without eval."""
    return _eval_node(ast.parse(rule, mode="eval"), days)


def print_report():
    """Print every student with their borrowed books."""
    print("Loan Report")
    for student, books in loans.items():
        print(student, "->", books)


def main():
    """Run the demo scenario."""
    add_book_loan("S101", "B-ALGO")
    add_book_loan("S102", "B-NETW")
    add_book_loan("", "B-DBMS")
    add_book_loan("S103", 4521)  # rejected: book id must be a string
    return_book("S999", "B-NONE")
    renew_book("S101", "B-ALGO", 21)
    print("Fine for 5 days:", calculate_fine(5))
    print("Fine for -3 days:", calculate_fine(-3))
    print("Fine via rule:", fine_from_rule("days * 2 + 10", 4))
    days = input("Days overdue for S102 (press Enter for 0): ") or "0"
    try:
        print("S102 owes:", calculate_fine(int(days)))
    except ValueError:
        print("Days must be a whole number")
    save_records()
    load_records()
    print_report()


if __name__ == "__main__":
    main()
