# MiniJS 1.0 — README

## 1. Project overview

MiniJS is a small interpreter written in Python. It reads a MiniJS program from a `.mjs` file, checks the syntax, executes the program, and prints the results.

This project is separated into three Python files so each part is easier to understand:

- **`lexer.py`** — reads characters and groups them into tokens.
- **`parser.py`** — checks the token order and builds an Abstract Syntax Tree (AST).
- **`interpreter.py`** — evaluates the AST, manages variables and scopes, runs statements, and prints output.

The implementation uses the Python standard library. No third-party packages are required.

## 2. Files and responsibilities

### `lexer.py` — Lexical analysis

The lexer reads the program character by character and creates tokens.

It recognizes the keywords `let`, `if`, `else`, `while`, `true`, `false`, and `print`; identifiers; decimal/integer numeric literals; operators and punctuation. It skips whitespace, `//` line comments, and `/* ... */` block comments.

If it finds an unsupported character or an unterminated block comment, it reports a lexical error.

### `parser.py` — Syntax analysis

The parser consumes the tokens from the lexer and builds an AST, which represents the program's structure.

The current implementation supports:
- Variable declarations with `let`
- Variable assignment
- `print(expression);`
- `if (...) { ... }` and `else { ... }`
- `while (...) { ... }`
- Nested blocks
- Numeric and Boolean expressions
- Unary operators: `!`, `+`, `-`
- Arithmetic operators: `+`, `-`, `*`, `/`, `%`
- Comparisons: `<`, `<=`, `>`, `>=`
- Strict equality operators: `===`, `!==`
- Logical operators: `&&`, `||`
- Parentheses for grouping expressions

Statements must follow the syntax expected by this parser, including semicolons after declarations, assignments, and `print` statements.

### `interpreter.py` — Runtime and execution

The interpreter runs the AST produced by the parser. It implements:
- Variable environments and parent scopes
- Duplicate declaration checks within a scope
- Errors for undefined variables and access before initialization
- Truthiness for the supported value types
- Short-circuit behavior for `&&` and `||`
- Number formatting, including `NaN`, `Infinity`, and `-Infinity`
- Runtime errors for invalid numeric operands

## 3. Requirements

- Python 3
- No external Python packages

Check Python is installed:

```powershell
python --version
```

## 4. Folder layout

Keep these files together in one folder:

```text
minijs_split/
├── lexer.py
├── parser.py
├── interpreter.py
├── README.md
└── test.mjs
```

`test.mjs` is your MiniJS input program. You create this file yourself.

## 5. Create a test program

Create a file named `test.mjs` in the same folder as the three Python files. Paste this example into it:

```javascript
// Variables and arithmetic
let x = 10;
let y = 5;
print(x + y);

// Comparison
print(x > y);

// Loop
let i = 1;
while (i <= 3) {
    print(i);
    i = i + 1;
}
```

Expected output:

```text
15
true
1
2
3
```

## 6. Run the program in Windows PowerShell

Open PowerShell and move to the folder where you extracted the files. For example, if you extracted them to the Desktop:

```powershell
cd "$HOME\Desktop\minijs_split"
```

Then run:

```powershell
python .\interpreter.py .\test.mjs
```

The first path is the Python interpreter file. The second path is the MiniJS program to execute.

You can run another program by replacing `test.mjs` with its filename, for example:

```powershell
python .\interpreter.py .\all_examples.mjs
```

Run the command from the folder containing `lexer.py`, `parser.py`, and `interpreter.py`, or make sure Python can find those modules.

## 7. How one program runs

1. `interpreter.py` reads the `.mjs` source file.
2. `lexer.py` converts source text into tokens.
3. `parser.py` checks the token sequence and builds an AST.
4. `interpreter.py` evaluates the AST and collects `print` output.
5. If execution succeeds, the output is printed to the terminal. Errors are printed to standard error.

The parser processes the whole program before execution starts, so a syntax error prevents earlier statements from running.

## 8. Error messages

- **Lexical error** — an unsupported character, malformed number, or unterminated block comment.
- **Syntax error** — the program does not match the grammar, such as a missing semicolon or closing brace.
- **Runtime error** — a problem while executing, such as an undefined variable or an invalid operand for a numeric operator.

The message normally includes a character position to help locate the problem.

## 9. Current limitations

This README describes the uploaded interpreter after splitting it into files. It does not claim full JavaScript compatibility.

In particular:
- String literals such as `"hello"` are not supported by the current lexer/parser.
- Equality uses `===` and `!==`; `==` and `!=` are not supported.
- Functions, arrays, objects, `for` loops, and browser/Node.js APIs are not implemented.
- Only the language features listed above should be assumed to work.

## 10. Quick troubleshooting

**Error: `can't open file`**
- Check the folder path and filename.
- Use `dir` in PowerShell to see the files in the current folder.

**Error: `No such file or directory` for `test.mjs`**
- Create `test.mjs` in the current folder or pass its correct path.

**Error: `No module named 'lexer'` or `No module named 'parser'`**
- Keep `lexer.py`, `parser.py`, and `interpreter.py` together in the same folder.

**A string such as `"Adult"` gives a lexical error**
- String literals are not supported in this version. Try printing a number, Boolean expression, or variable instead.

## 11. Run your existing correctness tests

If your project includes the public checker at `src\minijs\correctness_test.py` and you want to test the original project layout, run the checker using the original interpreter and its expected command. For example, from your original project root:

```powershell
python .\src\minijs\correctness_test.py -- python .\src\interpreter.py
```

The three-file split is a separate layout. The README does not claim that the original 1049-test result has been repeated against the split version; run your checker against the split interpreter if your checker supports that arrangement.

## 12. Summary

- `lexer.py` = characters to tokens.
- `parser.py` = tokens to AST.
- `interpreter.py` = AST to program execution.
- Run programs with `python .\interpreter.py .\test.mjs`.
