import math
import sys
from lexer import MiniJSError, lex
from parser import Parser

UNINIT = object()


class Environment:
    def __init__(self, parent=None):
        self.parent, self.values = parent, {}

    def declare(self, name):
        if name in self.values:
            raise MiniJSError(f"Runtime error: '{name}' already declared")
        self.values[name] = UNINIT

   
    def get(self, name):
        env = self
        while env is not None:
            values = env.values
            if name in values:
                value = values[name]
                if value is UNINIT:
                    raise MiniJSError(
                        f"Runtime error: '{name}' accessed before initialization"
                    )
                return value
            env = env.parent
        raise MiniJSError(f"Runtime error: undefined variable '{name}'")

    def assign(self, name, value):
        env = self
        while env is not None:
            values = env.values
            if name in values:
                if values[name] is UNINIT:
                    raise MiniJSError(
                        f"Runtime error: '{name}' accessed before initialization"
                    )
                values[name] = value
                return
            env = env.parent
        raise MiniJSError(f"Runtime error: assignment to undefined variable '{name}'")



def truthy(v):
    if isinstance(v, bool):
        return v
    if isinstance(v, str):
        return bool(v)
    return v != 0 and not math.isnan(v)


def number(v, op):
    if type(v) is not float:
        raise MiniJSError(f"Runtime error: operator {op} requires Number operands")
    return v


def div(a, b):
    if math.isnan(a) or math.isnan(b) or (a == 0 and b == 0):
        return math.nan
    if b == 0:
        return math.copysign(math.inf, a * math.copysign(1, b))
    return a / b


def rem(a, b):
    if math.isnan(a) or math.isnan(b) or math.isinf(a) or b == 0:
        return math.nan
    if math.isinf(b):
        return a
    return math.fmod(a, b)


def equal(a, b):
    if type(a) is not type(b):
        return False
    if isinstance(a, float) and (math.isnan(a) or math.isnan(b)):
        return False
    return a == b


def evaluate(n, env):
    typ = n[0]
    if typ in {"number", "string", "boolean"}:
        return n[1]
    if typ == "variable":
        return env.get(n[1])
    if typ == "unary":
        op, v = n[1], evaluate(n[2], env)
        if op == "!":
            return not truthy(v)
        return number(v, op) if op == "+" else -number(v, op)
    if typ == "binary":
        op, left, right = n[1:]
        a = evaluate(left, env)
        if op == "&&":
            return evaluate(right, env) if truthy(a) else a
        if op == "||":
            return a if truthy(a) else evaluate(right, env)
        b = evaluate(right, env)
        if op in {"===", "!=="}:
            result = equal(a, b)
            return result if op == "===" else not result
        a, b = number(a, op), number(b, op)
        if op == "+": return a + b
        if op == "-": return a - b
        if op == "*": return a * b
        if op == "/": return div(a, b)
        if op == "%": return rem(a, b)
        if op == "<": return a < b
        if op == "<=": return a <= b
        if op == ">": return a > b
        if op == ">=": return a >= b
    raise MiniJSError("Internal interpreter error")


def execute_block(node, env, out, new_scope=True):
    scope = Environment(env) if new_scope else env
    for stmt in node[1]:
        execute(stmt, scope, out)


def execute(n, env, out):
    typ = n[0]
    if typ == "block":
        execute_block(n, env, out)
    elif typ == "let":
        _, name, expr = n
        env.declare(name)
        value = evaluate(expr, env)
        env.values[name] = value
    elif typ == "assign":
        env.assign(n[1], evaluate(n[2], env))
    elif typ == "print":
        out.append(format_value(evaluate(n[1], env)))
    elif typ == "if":
        cond = evaluate(n[1], env)
        if truthy(cond):
            execute(n[2], env, out)
        elif n[3] is not None:
            execute(n[3], env, out)
    
    
    elif typ == "while":
        body = n[2]

        if body[0] == "block":
            loop_env = Environment(env)
            statements = body[1]

            while truthy(evaluate(n[1], env)):
                loop_env.values.clear()
                for stmt in statements:
                    execute(stmt, loop_env, out)
        else:
            while truthy(evaluate(n[1], env)):
                execute(body, env, out)


    else:
        raise MiniJSError("Internal interpreter error")


def format_value(v):
    if isinstance(v, str):
        return v
    if isinstance(v, bool):
        return "true" if v else "false"
    if math.isnan(v):
        return "NaN"
    if math.isinf(v):
        return "Infinity" if v > 0 else "-Infinity"
    if v == 0:
        return "0"
    s = repr(v)
    return s[:-2] if s.endswith(".0") else s


def main(argv):
    if len(argv) != 2:
        print("Usage: interpreter.py path/to/program.mjs", file=sys.stderr)
        return 2
    try:
        with open(argv[1], encoding="utf-8-sig") as f:
            tree = Parser(lex(f.read())).parse()
        out = []
        execute_block(tree, Environment(), out, new_scope=False)
        if out:
            print("\n".join(out))
        return 0
    except (MiniJSError, OSError, UnicodeError, ValueError, OverflowError) as e:
        print(str(e), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
