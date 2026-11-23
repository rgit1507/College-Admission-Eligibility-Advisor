import tkinter as tk
from tkinter import ttk, messagebox

from engine import advise
from knowledge_base import KnowledgeBase


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("College Admission Eligibility Advisor")
        self.geometry("680x460")
        self.kb = KnowledgeBase()

        form = ttk.Frame(self, padding=10)
        form.pack(fill="x")

        ttk.Label(form, text="Marks (%)").grid(row=0, column=0, sticky="w")
        self.marks = ttk.Entry(form, width=10)
        self.marks.grid(row=0, column=1, padx=8)

        ttk.Label(form, text="Rank").grid(row=0, column=2, sticky="w")
        self.rank = ttk.Entry(form, width=10)
        self.rank.grid(row=0, column=3, padx=8)

        ttk.Label(form, text="Category").grid(row=0, column=4, sticky="w")
        self.category = ttk.Combobox(form, width=10, state="readonly",
                                     values=[c.name for c in self.kb.categories()])
        self.category.current(0)
        self.category.grid(row=0, column=5, padx=8)

        ttk.Button(form, text="Check eligibility", command=self.check).grid(row=0, column=6, padx=8)

        self.output = tk.Text(self, wrap="word", padx=10, pady=10)
        self.output.pack(fill="both", expand=True)
        self.output.tag_configure("yes", foreground="#1a7f37")
        self.output.tag_configure("no", foreground="#b42318")

    def check(self):
        try:
            results, _ = advise(float(self.marks.get()), int(self.rank.get()), self.category.get(), self.kb)
        except ValueError as err:
            messagebox.showerror("Input error", f"Please enter valid numbers.\n\n{err}")
            return
        self.output.delete("1.0", "end")
        for _, ok, reason in results:
            self.output.insert("end", ("YES  " if ok else "NO   ") + reason + "\n\n", "yes" if ok else "no")
        names = ", ".join(r[0] for r in results if r[1]) or "none"
        self.output.insert("end", f"Eligible branches: {names}")


if __name__ == "__main__":
    App().mainloop()
