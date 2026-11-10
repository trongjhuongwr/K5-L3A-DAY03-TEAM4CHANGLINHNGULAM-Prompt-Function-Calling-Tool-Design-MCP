from __future__ import annotations

import ast
import math
import operator
from typing import Any

from tools._shared import err

SAFE_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}

SAFE_FUNCTIONS = {
    "abs": abs,
    "round": round,
    "sqrt": math.sqrt,
    "log": math.log,
    "log10": math.log10,
    "exp": math.exp,
    "ceil": math.ceil,
    "floor": math.floor,
}


def _eval_node(node: ast.AST) -> float:
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return float(node.value)
    if isinstance(node, ast.BinOp):
        op_type = type(node.op)
        if op_type in SAFE_OPERATORS:
            left = _eval_node(node.left)
            right = _eval_node(node.right)
            return SAFE_OPERATORS[op_type](left, right)
    if isinstance(node, ast.UnaryOp):
        op_type = type(node.op)
        if op_type in SAFE_OPERATORS:
            operand = _eval_node(node.operand)
            return SAFE_OPERATORS[op_type](operand)
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
        func_name = node.func.id
        if func_name in SAFE_FUNCTIONS:
            args = [_eval_node(arg) for arg in node.args]
            return float(SAFE_FUNCTIONS[func_name](*args))

    raise ValueError(f"Unsupported syntax or unsafe operation in expression: {ast.dump(node)}")


def calculate(expression: str = "") -> dict[str, Any]:
    """Tính toán biểu thức số học an toàn."""
    try:
        expr = (expression or "").strip()
        if not expr:
            return {"tool": "calculator", "error": "ValueError", "message": "Expression cannot be empty"}

        # Replace common mathematical symbols
        cleaned = expr.replace("^", "**").replace("×", "*").replace("÷", "/")
        parsed = ast.parse(cleaned, mode="eval")
        result = _eval_node(parsed.body)

        # Format integer results cleanly
        if isinstance(result, float) and result.is_integer():
            formatted_result: int | float = int(result)
        else:
            formatted_result = round(result, 6)

        return {
            "tool": "calculator",
            "expression": expr,
            "result": formatted_result,
            "status": "success",
        }
    except Exception as exc:
        return err("calculator", exc)