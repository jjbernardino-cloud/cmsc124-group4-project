
import tkinter as tk
from tkinter import ttk

from lexer.lexer import tokenize
from lexer.errors import format_error


SAMPLE_CODE = '''HAI
BTW This is a comment
I HAS A name ITZ "Carlos"
I HAS A age ITZ 20
VISIBLE "Hello World!"
KTHXBYE'''


def run_lexer():
    source = code_editor.get("1.0", tk.END)
    tokens, errors = tokenize(source)

    # Clear old token results.
    for item in token_table.get_children():
        token_table.delete(item)

    # Display the new tokens.
    for token in tokens:
        token_table.insert(
            "",
            tk.END,
            values=(
                token["type"],
                token["lexeme"],
                token["line"],
                token["column"]
            )
        )

    # Clear and update the error panel.
    error_output.config(state=tk.NORMAL)
    error_output.delete("1.0", tk.END)

    if errors:
        for error in errors:
            error_output.insert(
                tk.END,
                format_error(error) + "\n"
            )
    else:
        error_output.insert(tk.END, "No lexical errors found.")

    error_output.config(state=tk.DISABLED)


def load_sample():
    code_editor.delete("1.0", tk.END)
    code_editor.insert("1.0", SAMPLE_CODE)


def clear_all():
    code_editor.delete("1.0", tk.END)

    for item in token_table.get_children():
        token_table.delete(item)

    error_output.config(state=tk.NORMAL)
    error_output.delete("1.0", tk.END)
    error_output.config(state=tk.DISABLED)


def create_gui():
    global code_editor, token_table, error_output

    root = tk.Tk()
    root.title("LOLCODE Lexical Analyzer")
    root.geometry("1000x750")
    root.minsize(700, 500)

    # Main heading.
    heading = ttk.Label(
        root,
        text="LOLCODE Lexical Analyzer",
        font=("Arial", 18, "bold")
    )
    heading.pack(pady=10)

    # Source code section.
    ttk.Label(
        root,
        text="Source Code",
        font=("Arial", 11, "bold")
    ).pack(anchor="w", padx=12)

    editor_frame = ttk.Frame(root)
    editor_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=5)

    code_editor = tk.Text(
        editor_frame,
        height=10,
        wrap=tk.NONE,
        font=("Consolas", 11),
        undo=True
    )
    editor_scroll = ttk.Scrollbar(
        editor_frame,
        orient=tk.VERTICAL,
        command=code_editor.yview
    )
    code_editor.configure(yscrollcommand=editor_scroll.set)

    code_editor.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    editor_scroll.pack(side=tk.RIGHT, fill=tk.Y)

    # Buttons.
    button_frame = ttk.Frame(root)
    button_frame.pack(fill=tk.X, padx=12, pady=5)

    ttk.Button(
        button_frame,
        text="Run Lexer",
        command=run_lexer
    ).pack(side=tk.LEFT, padx=(0, 5))

    ttk.Button(
        button_frame,
        text="Load Sample",
        command=load_sample
    ).pack(side=tk.LEFT, padx=5)

    ttk.Button(
        button_frame,
        text="Clear",
        command=clear_all
    ).pack(side=tk.LEFT, padx=5)

    # Token results table.
    ttk.Label(
        root,
        text="Tokens",
        font=("Arial", 11, "bold")
    ).pack(anchor="w", padx=12, pady=(8, 2))

    table_frame = ttk.Frame(root)
    table_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=5)

    columns = ("type", "lexeme", "line", "column")

    token_table = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings",
        height=10
    )

    token_table.heading("type", text="Token Type")
    token_table.heading("lexeme", text="Lexeme")
    token_table.heading("line", text="Line")
    token_table.heading("column", text="Column")

    token_table.column("type", width=150, anchor=tk.W)
    token_table.column("lexeme", width=400, anchor=tk.W)
    token_table.column("line", width=70, anchor=tk.CENTER)
    token_table.column("column", width=80, anchor=tk.CENTER)

    table_scroll = ttk.Scrollbar(
        table_frame,
        orient=tk.VERTICAL,
        command=token_table.yview
    )
    token_table.configure(yscrollcommand=table_scroll.set)

    token_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    table_scroll.pack(side=tk.RIGHT, fill=tk.Y)

    # Error output section.
    ttk.Label(
        root,
        text="Lexical Errors",
        font=("Arial", 11, "bold")
    ).pack(anchor="w", padx=12, pady=(8, 2))

    error_output = tk.Text(
        root,
        height=5,
        wrap=tk.WORD,
        font=("Consolas", 10),
        foreground="red",
        state=tk.DISABLED
    )
    error_output.pack(fill=tk.X, padx=12, pady=(0, 12))

    load_sample()
    root.mainloop()
