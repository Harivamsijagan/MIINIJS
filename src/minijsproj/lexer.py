
import re
from dataclasses import dataclass


class MiniJSError(Exception):
    pass


KEYWORDS = {"let", "if", "else", "while", "true", "false", "print"}
OPS = ("===", "!==", "<=", ">=", "&&", "||",
       "+", "-", "*", "/", "%", "!", "<", ">", "=",
       ";", "(", ")", "{", "}", ",", "[", "]")


@dataclass
class Token:
    kind: str
    value: object
    pos: int


def lex(source):
    source = source.lstrip("\ufeff")
    tokens, i, n = [], 0, len(source)

    while i < n:
        c = source[i]

        if c.isspace():
            i += 1
            continue

        if source.startswith("//", i):
            end = source.find("\n", i)
            i = n if end < 0 else end + 1
            continue

        if source.startswith("/*", i):
            end = source.find("*/", i + 2)
            if end < 0:
                raise MiniJSError(f"Lexical error: unterminated comment at {i}")
            i = end + 2
            continue

        if c in "\"'":
            start, quote, chars = i, c, []
            i += 1
            while i < n and source[i] != quote:
                if source[i] in "\r\n":
                    raise MiniJSError(f"Lexical error: unterminated string at {start}")
                if source[i] == "\\":
                    i += 1
                    if i >= n:
                        raise MiniJSError(f"Lexical error: unterminated string at {start}")
                    escapes = {"n": "\n", "t": "\t", "r": "\r",
                               "\\": "\\", "'": "'", '"': '"'}
                    if source[i] not in escapes:
                        raise MiniJSError(f"Lexical error: invalid escape at {i}")
                    chars.append(escapes[source[i]])
                else:
                    chars.append(source[i])
                i += 1
            if i == n:
                raise MiniJSError(f"Lexical error: unterminated string at {start}")
            tokens.append(Token("STRING", "".join(chars), start))
            i += 1
            continue

        if c.isascii() and (c.isalpha() or c in "_$"):
            start = i
            i += 1
            while i < n and source[i].isascii() and (source[i].isalnum() or source[i] in "_$"):
                i += 1
            word = source[start:i]
            tokens.append(Token(word if word in KEYWORDS else "IDENT", word, start))
            continue

        if c.isascii() and c.isdigit():
            start = i
            while i < n and source[i].isascii() and source[i].isdigit():
                i += 1
            if i < n and source[i] == ".":
                if i + 1 == n or not source[i + 1].isascii() or not source[i + 1].isdigit():
                    raise MiniJSError(f"Lexical error: malformed number at {start}")
                i += 1
                while i < n and source[i].isascii() and source[i].isdigit():
                    i += 1
            tokens.append(Token("NUMBER", float(source[start:i]), start))
            continue

        op = next((op for op in OPS if source.startswith(op, i)), None)
        if op:
            tokens.append(Token(op, op, i))
            i += len(op)
            continue

        raise MiniJSError(f"Lexical error: unexpected character {c!r} at position {i}")

    tokens.append(Token("EOF", None, n))
    return tokens
