import re
import json
import datetime


class ASTNode:
    pass


class UnaryOp(ASTNode):
    def __init__(self, op, expr):
        self.op = op
        self.expr = expr


class BinOp(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right


class Num(ASTNode):
    def __init__(self, value):
        self.value = value


class RegexOp(ASTNode):
    def __init__(self, attr, pattern):
        self.attr = attr
        self.pattern = pattern


class Interpreter:
    def evaluate(self, equation, value):
        self.current_value = value
        tokens = self.tokenize(equation)
        self.tokens = iter(tokens)
        self.current_token = next(self.tokens, None)

        if "Regex" in equation:
            regex_result = self.parse_regex_expression()
            return self.visit_RegexOp(regex_result, value)

        ast = self.parse_expression()
        return self.visit(ast, value)

    def tokenize(self, equation):
        tokens = re.findall(
            r"\d+\.?\d*|[+\-*/()^]|Regex|ATTR|\'[^\']*\'|[a-zA-Z_]\w*",
            equation.replace(" ", ""),
        )
        return tokens

    def parse_regex_expression(self):
        self.eat("Regex")
        self.eat("(")
        if self.current_token == "ATTR":
            self.eat("ATTR")
        else:
            raise ValueError("Expected 'ATTR' in Regex expression")

        pattern_token = self.current_token
        if pattern_token.startswith("'") and pattern_token.endswith("'"):
            self.eat(pattern_token)
        else:
            raise ValueError("Expected regex pattern in single quotes")

        self.eat(")")
        return RegexOp(attr="ATTR", pattern=pattern_token[1:-1])  # Remove quotes

    def eat(self, token_type):
        if self.current_token == token_type:
            self.current_token = next(self.tokens, None)
        else:
            raise ValueError(
                f"Unexpected token: {self.current_token}, expected: {token_type}"
            )

    def parse_expression(self):
        node = self.parse_term()
        while self.current_token in ("+", "-"):
            op = self.current_token
            self.eat(op)
            node = BinOp(left=node, op=op, right=self.parse_term())
        return node

    def parse_term(self):
        node = self.parse_factor()
        while self.current_token in ("*", "/"):
            op = self.current_token
            self.eat(op)
            node = BinOp(left=node, op=op, right=self.parse_factor())
        return node

    def parse_factor(self):
        node = self.parse_base()
        while self.current_token == "^":
            op = self.current_token
            self.eat(op)
            node = BinOp(left=node, op=op, right=self.parse_base())
        return node

    def parse_base(self):
        token = self.current_token

        if token is None:
            raise ValueError("Unexpected end of input")

        if token == "(":
            self.eat("(")
            node = self.parse_expression()
            self.eat(")")
            return node
        elif re.match(r"^\d+\.?\d*$", token):
            self.eat(token)
            return Num(float(token))
        elif token in ("+", "-"):
            self.eat(token)
            expr = self.parse_base()
            return UnaryOp(op=token, expr=expr)
        elif token == "ATTR":
            self.eat(token)
            return Num(float(self.current_value))
        else:
            raise ValueError(f"Unexpected token: {token}")

    def visit(self, node, value):
        if isinstance(node, UnaryOp):
            return self.visit_UnaryOp(node, value)
        elif isinstance(node, BinOp):
            return self.visit_BinOp(node, value)
        elif isinstance(node, Num):
            return self.visit_Num(node, value)
        elif isinstance(node, RegexOp):
            return self.visit_RegexOp(node, value)

    def visit_UnaryOp(self, node, value):
        if node.op == "+":
            return +self.visit(node.expr, value)
        elif node.op == "-":
            return -self.visit(node.expr, value)

    def visit_BinOp(self, node, value):
        left = self.visit(node.left, value)
        right = self.visit(node.right, value)
        op = node.op

        if op == "+":
            return left + right
        elif op == "-":
            return left - right
        elif op == "*":
            return left * right
        elif op == "/":
            if right == 0:
                raise ValueError("Division by zero")
            return left / right
        elif op == "^":
            return left**right
        else:
            raise Exception(f"Unsupported operator: {op}")

    def visit_Num(self, node, value):
        return float(node.value)

    def visit_RegexOp(self, node, value):
        attr_value = str(value)
        pattern = node.pattern
        match = re.match(pattern, attr_value)
        return match is not None

    def json_response(self, asset_id, attribute_id, value):
        try:
            response = {
                "asset_id": asset_id,
                "attribute_id": attribute_id,
                "timestamp": datetime.datetime.now().isoformat() + "Z",
                "value": value,
            }
            return json.dumps(response)
        except TypeError as e:
            print(f"Error evaluating expression '{value}' with value {value}: {e}")
            return None


# Example usage
if __name__ == "__main__":
    interpreter = Interpreter()

    # Example arithmetic evaluation
    arithmetic_result = interpreter.evaluate("ATTR + 50 * (ATTR / 10)", "100")
    print(
        f"Arithmetic Result: {arithmetic_result}"
    ) 

    # Example regex evaluation
    regex_result = interpreter.evaluate("Regex(ATTR, '^dog')", "doghouse")
    print(
        f"Regex Result: {regex_result}"
    )  

    # Example JSON response
    json_response = interpreter.json_response(
        "asset_123", "attr_456", arithmetic_result
    )
    print(json_response)
