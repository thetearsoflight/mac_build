from __future__ import annotations

import argparse
import sys
from pathlib import Path
import tkinter as tk
from tkinter import messagebox

MAX_INPUT_CHARS = 2000


def format_with_blank_lines(text: str, insert_space_line: bool = True) -> str:
    """Insert one extra line after each existing line in a text string."""
    lines = text.splitlines()
    spacer = " " if insert_space_line else ""
    return "".join(f"{line}\n{spacer}\n" for line in lines)


def add_blank_lines(input_path: Path, output_path: Path, insert_space_line: bool = True) -> None:
    """Write a copy of the file with an extra blank line after each line."""
    text = input_path.read_text(encoding="utf-8")
    output_path.write_text(format_with_blank_lines(text, insert_space_line), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Insert a blank line after every line in a text file, or launch GUI.",
    )
    parser.add_argument(
        "input",
        nargs="?",
        type=Path,
        default=None,
        help="Path to the source .txt file",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="Output file path",
    )
    parser.add_argument(
        "--gui",
        action="store_true",
        help="Force launch the desktop GUI",
    )
    parser.add_argument(
        "--no-space-line",
        action="store_true",
        help="Use fully empty inserted lines (default inserts a single-space line)",
    )
    return parser.parse_args()


class BlankLineApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("小红书分行助手")
        self.geometry("760x640")
        self.resizable(False, False)

        self.space_line_var = tk.BooleanVar(value=True)
        self.char_count_var = tk.StringVar(value=f"0/{MAX_INPUT_CHARS}")

        self._build_ui()

    def _build_ui(self) -> None:
        pad_x = 16
        content_width = 94

        tk.Label(self, text="原文（粘贴文章，最多 2000 字）").pack(anchor="w", padx=pad_x, pady=(16, 6))
        self.input_text = tk.Text(self, height=10, width=content_width, wrap="word")
        self.input_text.pack(padx=pad_x)
        self.input_text.bind("<KeyRelease>", self._update_char_count)

        count_row = tk.Frame(self)
        count_row.pack(fill="x", padx=pad_x, pady=(6, 0))
        tk.Label(count_row, textvariable=self.char_count_var).pack(side="right")

        tk.Checkbutton(
            self,
            text="插入的空行包含一个空格（推荐用于小红书防吞行）",
            variable=self.space_line_var,
        ).pack(anchor="w", padx=pad_x, pady=(12, 8))

        action_row = tk.Frame(self)
        action_row.pack(fill="x", padx=pad_x)
        tk.Button(action_row, text="添加分行", command=self._run, height=2).pack(side="left", fill="x", expand=True)
        tk.Button(action_row, text="一键复制结果", command=self._copy_output, height=2).pack(side="left", fill="x", expand=True, padx=(8, 0))

        tk.Label(self, text="处理结果").pack(anchor="w", padx=pad_x, pady=(14, 6))
        self.output_text = tk.Text(self, height=12, width=content_width, wrap="word")
        self.output_text.pack(padx=pad_x)

    def _get_input_text(self) -> str:
        return self.input_text.get("1.0", "end-1c")

    def _update_char_count(self, event: tk.Event | None = None) -> None:
        char_count = len(self._get_input_text())
        self.char_count_var.set(f"{char_count}/{MAX_INPUT_CHARS}")
        if char_count > MAX_INPUT_CHARS:
            self.char_count_var.set(f"{char_count}/{MAX_INPUT_CHARS}（已超限）")

    def _validate_input_length(self) -> bool:
        char_count = len(self._get_input_text())
        if char_count > MAX_INPUT_CHARS:
            messagebox.showerror("超出限制", f"输入内容为 {char_count} 字，已超过 {MAX_INPUT_CHARS} 字上限。")
            return False
        return True

    def _run(self) -> None:
        input_text = self._get_input_text()

        if not input_text.strip():
            messagebox.showerror("错误", "请先粘贴文章内容")
            return
        if not self._validate_input_length():
            return

        result = format_with_blank_lines(
            text=input_text,
            insert_space_line=self.space_line_var.get(),
        )

        self.output_text.delete("1.0", "end")
        self.output_text.insert("1.0", result)

    def _copy_output(self) -> None:
        output = self.output_text.get("1.0", "end-1c")
        if not output.strip():
            messagebox.showwarning("提示", "还没有可复制的结果，请先点击“添加分行”。")
            return

        self.clipboard_clear()
        self.clipboard_append(output)
        self.update()
        messagebox.showinfo("完成", "结果已复制到剪贴板")


def launch_gui() -> None:
    app = BlankLineApp()
    app.mainloop()


def main() -> None:
    args = parse_args()

    # Launch GUI when no CLI paths are provided.
    if args.gui or (len(sys.argv) == 1):
        launch_gui()
        return

    input_path: Path = args.input if args.input is not None else Path("input.txt")
    output_path: Path = args.output if args.output is not None else Path("output.txt")

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    add_blank_lines(
        input_path=input_path,
        output_path=output_path,
        insert_space_line=not args.no_space_line,
    )
    print(f"Wrote file with blank lines: {output_path}")


if __name__ == "__main__":
    main()
