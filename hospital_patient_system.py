"""Hospital patient records and admission management demo."""

import ast
import hashlib
import json
import operator
import secrets
from pathlib import Path

patient_records = {
    "P101": {
        "name": "John Doe",
        "ward": "ICU",
        "is_admitted": True,
        "bill": 2400.0,
    },
    "P102": {
        "name": "Jane Smith",
        "ward": "General",
        "is_admitted": False,
        "bill": 450.0,
    },
    "P103": {
        "name": "Robert Brown",
        "ward": "Private",
        "is_admitted": True,
        "bill": 1200.0,
    },
}

_ALLOWED_BINARY_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}


def admit_patient(p_id, name, ward, intake_log=None):
    """Admit a new patient and optionally append an intake log entry."""
    if p_id in patient_records:
        return False

    if intake_log is None:
        intake_log = []

    patient_records[p_id] = {
        "name": name,
        "ward": ward,
        "is_admitted": True,
        "bill": 0.0,
    }
    intake_log.append(f"Admitted patient {p_id} into ward {ward}")
    return True


def discharge_patient(p_id):
    """Discharge a patient; return False if the patient ID is unknown."""
    patient = patient_records.get(p_id)
    if patient is None:
        return False

    patient["is_admitted"] = False
    return True


def verify_admission_status(p_id):
    """Return whether the specified patient exists and is admitted."""
    patient = patient_records.get(p_id)
    return patient is not None and patient["is_admitted"]


def _evaluate_bill_expression(expression, base_bill):
    """Evaluate a restricted arithmetic expression without executing code."""
    try:
        parsed = ast.parse(expression, mode="eval")
    except (SyntaxError, ValueError) as exc:
        raise ValueError("Invalid billing formula.") from exc

    def evaluate(node):
        if isinstance(node, ast.Expression):
            return evaluate(node.body)
        if isinstance(node, ast.Name) and node.id == "base_bill":
            return base_bill
        if isinstance(node, ast.Constant) and isinstance(
            node.value, (int, float)
        ):
            return node.value
        if (
            isinstance(node, ast.BinOp)
            and type(node.op) in _ALLOWED_BINARY_OPERATORS
        ):
            left = evaluate(node.left)
            right = evaluate(node.right)
            if isinstance(node.op, ast.Div) and right == 0:
                raise ValueError("Division by zero in billing formula.")
            return _ALLOWED_BINARY_OPERATORS[type(node.op)](left, right)
        if isinstance(node, ast.UnaryOp) and isinstance(
            node.op, (ast.UAdd, ast.USub)
        ):
            value = evaluate(node.operand)
            return value if isinstance(node.op, ast.UAdd) else -value
        raise ValueError("Formula contains an unsupported operation.")

    result = evaluate(parsed)
    if not isinstance(result, (int, float)):
        raise ValueError("Billing formula must produce a number.")
    return result


def calculate_treatment_cost(p_id, formula_expr):
    """Calculate a bill using a restricted formula and the patient's
    base bill."""
    patient = patient_records.get(p_id)
    if patient is None:
        raise KeyError(f"Unknown patient ID: {p_id}")

    return _evaluate_bill_expression(formula_expr, patient["bill"])


def generate_patient_hash(p_id):
    """Return a SHA-256 digest for a patient identifier."""
    return hashlib.sha256(p_id.encode("utf-8")).hexdigest()


def generate_ward_token():
    """Generate a cryptographically secure four-digit ward token."""
    return secrets.randbelow(9000) + 1000


def export_patient_ledger(filename="patient_records.txt"):
    """Export the patient ledger as JSON and return the output path."""
    output_path = Path(filename)
    with output_path.open("w", encoding="utf-8") as ledger_file:
        json.dump(patient_records, ledger_file, indent=2)
        ledger_file.write("\n")
    return output_path


def get_ward_summary(records=None):
    """Return the number of currently admitted patients."""
    if records is None:
        records = patient_records
    return sum(
        1 for details in records.values()
        if details.get("is_admitted", False)
    )


def main():
    """Run a small demonstration of the hospital patient system."""
    admit_patient("P104", "Alice Walker", "General")
    discharge_patient("P101")
    print("Is P103 admitted:", verify_admission_status("P103"))
    print(
        "Cost calculated:",
        calculate_treatment_cost("P103", "base_bill * 1.12"),
    )
    print("Patient Hash:", generate_patient_hash("P103"))
    print("Ward Token:", generate_ward_token())
    exported_path = export_patient_ledger()
    print(f"Patient ledger exported to: {exported_path}")
    print("Active admits:", get_ward_summary())


if __name__ == "__main__":
    main()
