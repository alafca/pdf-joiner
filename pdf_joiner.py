import os
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

try:
    from tkinterdnd2 import TkinterDnD, DND_FILES
    DND_AVAILABLE = True
except ImportError:
    DND_AVAILABLE = False

from pypdf import PdfWriter


def move(items, sel, delta):
    """Shift the selected indices of items by delta in place; return the new selection.

    A row blocked by the list edge, or by a selected row that is itself blocked, stays put.
    """
    new_sel = []
    for i in sorted(sel, reverse=delta > 0):
        j = i + delta
        if j < 0 or j >= len(items) or j in new_sel:
            new_sel.append(i)
            continue
        items[i], items[j] = items[j], items[i]
        new_sel.append(j)
    return new_sel


class PdfJoinerApp:
    def __init__(self, root):
        self.root = root
        root.title("PDF Joiner")
        root.geometry("600x440")
        root.minsize(440, 320)

        self.files = []  # list[Path]
        self._build_ui()

    def _build_ui(self):
        hint = (
            "Drag PDFs into the list below, or click 'Add files...'"
            if DND_AVAILABLE
            else "Click 'Add files...' to add PDFs"
        )
        ttk.Label(self.root, text=hint, padding=(12, 10, 12, 4)).pack(anchor="w")

        main = ttk.Frame(self.root, padding=(12, 4, 12, 4))
        main.pack(fill="both", expand=True)

        list_frame = ttk.Frame(main)
        list_frame.pack(side="left", fill="both", expand=True)

        self.listbox = tk.Listbox(
            list_frame, selectmode="extended", activestyle="dotbox"
        )
        self.listbox.pack(side="left", fill="both", expand=True)

        sb = ttk.Scrollbar(list_frame, orient="vertical", command=self.listbox.yview)
        sb.pack(side="right", fill="y")
        self.listbox.config(yscrollcommand=sb.set)

        if DND_AVAILABLE:
            self.listbox.drop_target_register(DND_FILES)
            self.listbox.dnd_bind("<<Drop>>", self._on_drop)

        side = ttk.Frame(main, padding=(10, 0, 0, 0))
        side.pack(side="left", fill="y")

        ttk.Button(side, text="Add files...", command=self._add_files).pack(
            fill="x", pady=2
        )
        ttk.Button(side, text="Remove", command=self._remove_selected).pack(
            fill="x", pady=2
        )
        ttk.Separator(side, orient="horizontal").pack(fill="x", pady=6)
        ttk.Button(side, text="Move up", command=lambda: self._move(-1)).pack(
            fill="x", pady=2
        )
        ttk.Button(side, text="Move down", command=lambda: self._move(1)).pack(
            fill="x", pady=2
        )
        ttk.Separator(side, orient="horizontal").pack(fill="x", pady=6)
        ttk.Button(side, text="Clear all", command=self._clear).pack(fill="x", pady=2)

        bottom = ttk.Frame(self.root, padding=12)
        bottom.pack(fill="x")
        self.status = ttk.Label(bottom, text="", foreground="#666")
        self.status.pack(side="left")
        ttk.Button(bottom, text="Join PDFs", command=self._join).pack(side="right")

    def _render(self):
        self.listbox.delete(0, "end")
        self.listbox.insert("end", *(p.name for p in self.files))
        self._refresh_status()

    def _add_paths(self, paths):
        for raw in paths:
            p = Path(raw)
            if p.suffix.lower() != ".pdf" or not p.is_file():
                continue
            if p in self.files:
                continue
            self.files.append(p)
        self._render()

    def _add_files(self):
        paths = filedialog.askopenfilenames(
            title="Select PDF files",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
        )
        self._add_paths(paths)

    def _on_drop(self, event):
        paths = self.root.tk.splitlist(event.data)
        self._add_paths(paths)

    def _remove_selected(self):
        for idx in reversed(self.listbox.curselection()):
            del self.files[idx]
        self._render()

    def _move(self, delta):
        sel = move(self.files, self.listbox.curselection(), delta)
        self._render()
        for i in sel:
            self.listbox.selection_set(i)
        if sel:
            self.listbox.see(sel[0])

    def _clear(self):
        self.files.clear()
        self._render()

    def _refresh_status(self):
        n = len(self.files)
        self.status.config(text=f"{n} file{'s' if n != 1 else ''} ready" if n else "")

    def _join(self):
        if len(self.files) < 2:
            messagebox.showinfo("PDF Joiner", "Add at least two PDFs to join.")
            return
        out_path = filedialog.asksaveasfilename(
            title="Save merged PDF as...",
            defaultextension=".pdf",
            initialfile="merged.pdf",
            filetypes=[("PDF files", "*.pdf")],
        )
        if not out_path:
            return

        self.status.config(text="Merging...")
        self.root.update_idletasks()
        # Write to a temp file first so a failure never truncates an existing file.
        tmp = out_path + ".part"
        current = ""
        try:
            writer = PdfWriter()
            for p in self.files:
                current = p.name
                writer.append(str(p))
            current = Path(out_path).name
            writer.write(tmp)
            os.replace(tmp, out_path)
        except Exception as e:
            Path(tmp).unlink(missing_ok=True)
            self._refresh_status()
            messagebox.showerror("PDF Joiner", f"Failed on {current}:\n{e}")
            return

        self.status.config(text="Done.")
        if messagebox.askyesno(
            "Done",
            f"Merged {len(self.files)} PDFs into:\n{out_path}\n\nOpen the file now?",
        ):
            try:
                os.startfile(out_path)
            except OSError as e:
                messagebox.showerror("PDF Joiner", f"Couldn't open the file:\n{e}")


def main():
    root = TkinterDnD.Tk() if DND_AVAILABLE else tk.Tk()
    PdfJoinerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
