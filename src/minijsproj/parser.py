from lexer import MiniJSError


class Parser:
    def __init__(self, tokens):
        self.t, self.i = tokens, 0

    def cur(self):
        return self.t[self.i]

    def check(self, kind):
        return self.cur().kind == kind

    def take(self, kind):
        if not self.check(kind):
            t = self.cur()
            raise MiniJSError(f"Syntax error: expected {kind}, got {t.kind} at {t.pos}")
        t = self.cur()
        self.i += 1
        return t
        

    def parse(self):
        out = []
        while not self.check("EOF"):
            out.append(self.statement())
        return ("block", out)

    def statement(self):
        if self.check("let"):
            self.take("let")
            name = self.take("IDENT").value
            self.take("=")
            e = self.expression()
            self.take(";")
            return ("let", name, e)

        if self.check("IDENT"):
            name = self.take("IDENT").value
            self.take("=")
            e = self.expression()
            self.take(";")
            return ("assign", name, e)

        if self.check("print"):
            self.take("print")
            self.take("(")
            e = self.expression()
            self.take(")")
            self.take(";")
            return ("print", e)

        if self.check("if"):
            self.take("if")
            self.take("(")
            cond = self.expression()
            self.take(")")
            yes = self.block()
            no = None
            if self.check("else"):
                self.take("else")
                no = self.block()
            return ("if", cond, yes, no)

        if self.check("while"):
            self.take("while")
            self.take("(")
            cond = self.expression()
            self.take(")")
            return ("while", cond, self.block())

        if self.check("{"):
            return self.block()

        t = self.cur()
        raise MiniJSError(f"Syntax error: unexpected {t.kind} at {t.pos}")

    def block(self):
        self.take("{")
        out = []
        while not self.check("}"):
            if self.check("EOF"):
                raise MiniJSError(f"Syntax error: unclosed block at {self.cur().pos}")
            out.append(self.statement())
        self.take("}")
        return ("block", out)

    def expression(self):
        return self.binary()

    def binary(self, level=0):
        groups = [
            {"||"}, {"&&"}, {"===", "!=="}, {"<", "<=", ">", ">="},
            {"+", "-"}, {"*", "/", "%"}
        ]
        if level == len(groups):
            return self.unary()

        node = self.binary(level + 1)
        while self.cur().kind in groups[level]:
            op = self.cur().kind
            self.i += 1
            node = ("binary", op, node, self.binary(level + 1))
        return node

    def unary(self):
        if self.cur().kind in {"!", "+", "-"}:
            op = self.cur().kind
            self.i += 1
            return ("unary", op, self.unary())
        return self.primary()

    def primary(self):
        t = self.cur()
        if t.kind in {"NUMBER", "STRING"}:
            self.i += 1
            return ("string" if t.kind == "STRING" else "number", t.value)
        if t.kind in {"true", "false"}:
            self.i += 1
            return ("boolean", t.kind == "true")
        if t.kind == "IDENT":
            self.i += 1
            return ("variable", t.value)
        if t.kind == "(":
            self.i += 1
            e = self.expression()
            self.take(")")
            return e
        raise MiniJSError(f"Syntax error: expected expression at {t.pos}")
