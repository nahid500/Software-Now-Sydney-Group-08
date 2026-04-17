def evaluate_file(input_path: str) -> list[dict]:
    def format_number(value):
        if isinstance(value, float) and value.is_integer():
            return str(int(value))
        return str(value)

    def format_result(value):
        if isinstance(value, str):
            return value
        if float(value).is_integer():
            return str(int(value))
        return f"{value:.4f}"

    def tokenize(expr):
        tokens = []
        i = 0
        prev_type = None
        n = len(expr)

        while i < n:
            ch = expr[i]

            if ch.isspace():
                i += 1
                continue

            # implicit multiplication: e.g. 3(4+5)
            if ch == '(' and prev_type in ('NUM', 'RPAREN'):
                tokens.append(('OP', '*'))
                prev_type = 'OP'
                continue

            if ch == '(':
                tokens.append(('LPAREN', '('))
                prev_type = 'LPAREN'
                i += 1
                continue

            if ch == ')':
                tokens.append(('RPAREN', ')'))
                prev_type = 'RPAREN'
                i += 1
                continue

            if ch in '+*/':
                tokens.append(('OP', ch))
                prev_type = 'OP'
                i += 1
                continue

            if ch == '-':
                # unary negation is allowed at start, after '(', or after operator
                tokens.append(('OP', '-'))
                prev_type = 'OP'
                i += 1
                continue

            if ch.isdigit() or ch == '.':
                start = i
                dot_count = 0

                if ch == '.':
                    dot_count = 1
                    i += 1
                    if i >= n or not expr[i].isdigit():
                        raise ValueError("Invalid number")
                else:
                    i += 1

                while i < n and (expr[i].isdigit() or expr[i] == '.'):
                    if expr[i] == '.':
                        dot_count += 1
                        if dot_count > 1:
                            raise ValueError("Invalid number")
                    i += 1

                number_text = expr[start:i]
                number_value = float(number_text)

                # implicit multiplication: e.g. 2 3 or )3
                if prev_type in ('NUM', 'RPAREN'):
                    tokens.append(('OP', '*'))

                tokens.append(('NUM', number_value))
                prev_type = 'NUM'
                continue

            raise ValueError("Invalid character")

        tokens.append(('END', ''))
        return tokens

    def tokens_to_string(tokens):
        parts = []
        for token_type, value in tokens:
            if token_type == 'NUM':
                parts.append(f"[NUM:{format_number(value)}]")
            elif token_type == 'OP':
                parts.append(f"[OP:{value}]")
            elif token_type == 'LPAREN':
                parts.append("[LPAREN:(]")
            elif token_type == 'RPAREN':
                parts.append("[RPAREN:)]")
            elif token_type == 'END':
                parts.append("[END]")
        return " ".join(parts)

    def tree_to_string(node):
        node_type = node[0]

        if node_type == 'num':
            return format_number(node[1])

        if node_type == 'neg':
            return f"(neg {tree_to_string(node[1])})"

        if node_type == 'bin':
            op = node[1]
            left = tree_to_string(node[2])
            right = tree_to_string(node[3])
            return f"({op} {left} {right})"

    def evaluate_tree(node):
        node_type = node[0]

        if node_type == 'num':
            return node[1]

        if node_type == 'neg':
            return -evaluate_tree(node[1])

        if node_type == 'bin':
            op = node[1]
            left = evaluate_tree(node[2])
            right = evaluate_tree(node[3])

            if op == '+':
                return left + right
            elif op == '-':
                return left - right
            elif op == '*':
                return left * right
            elif op == '/':
                return left / right

        raise ValueError("Invalid tree")

    def parse(tokens):
        pos = 0

        def current():
            return tokens[pos]

        def parse_expression():
            nonlocal pos
            node = parse_term()

            while current()[0] == 'OP' and current()[1] in ('+', '-'):
                op = current()[1]
                pos += 1
                right = parse_term()
                node = ('bin', op, node, right)

            return node

        def parse_term():
            nonlocal pos
            node = parse_factor()

            while current()[0] == 'OP' and current()[1] in ('*', '/'):
                op = current()[1]
                pos += 1
                right = parse_factor()
                node = ('bin', op, node, right)

            return node

        def parse_factor():
            nonlocal pos
            token_type, value = current()

            if token_type == 'OP' and value == '-':
                pos += 1
                operand = parse_factor()
                return ('neg', operand)

            if token_type == 'NUM':
                pos += 1
                return ('num', value)

            if token_type == 'LPAREN':
                pos += 1
                node = parse_expression()

                if current()[0] != 'RPAREN':
                    raise ValueError("Missing closing parenthesis")

                pos += 1
                return node

            raise ValueError("Unexpected token")

        tree = parse_expression()

        if current()[0] != 'END':
            raise ValueError("Extra tokens")

        return tree

    import os

    results = []

    with open(input_path, "r", encoding="utf-8") as file:
        expressions = [line.rstrip("\n") for line in file]

    output_lines = []

    for expr in expressions:
        entry = {
            "input": expr,
            "tree": "ERROR",
            "tokens": "ERROR",
            "result": "ERROR"
        }

        try:
            tokens = tokenize(expr)
            tree = parse(tokens)
            value = evaluate_tree(tree)

            entry["tree"] = tree_to_string(tree)
            entry["tokens"] = tokens_to_string(tokens)
            entry["result"] = float(value)

            output_lines.append(f"Input: {expr}")
            output_lines.append(f"Tree: {entry['tree']}")
            output_lines.append(f"Tokens: {entry['tokens']}")
            output_lines.append(f"Result: {format_result(value)}")
            output_lines.append("")

        except Exception:
            output_lines.append(f"Input: {expr}")
            output_lines.append("Tree: ERROR")
            output_lines.append("Tokens: ERROR")
            output_lines.append("Result: ERROR")
            output_lines.append("")

        results.append(entry)

    if output_lines and output_lines[-1] == "":
        output_lines.pop()

    output_path = os.path.join(os.path.dirname(input_path), "output.txt")
    with open(output_path, "w", encoding="utf-8") as file:
        file.write("\n".join(output_lines))

    return results