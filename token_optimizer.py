import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os

class TokenOptimizer:
    def __init__(self, root):
        self.root = root
        self.root.title("بهینه‌ساز توکن برای هوش مصنوعی - حداکثر کاهش کاراکتر")
        self.root.geometry("1100x800")
        self.root.configure(bg="#f0f0f0")

        # متغیرهای چک‌باکس
        self.options = {
            "remove_extra_spaces": tk.BooleanVar(value=True),      # حذف فضاهای اضافی
            "single_line": tk.BooleanVar(value=True),             # تبدیل به یک خط
            "remove_comments": tk.BooleanVar(value=True),         # حذف کامنت‌های # و """ """
            "remove_docstrings": tk.BooleanVar(value=True),       # حذف داکیومنت‌ها
            "shorten_print": tk.BooleanVar(value=True),           # print(...) → پ(...)
            "shorten_variables": tk.BooleanVar(value=True),       # کوتاه‌سازی نام متغیرها (با حفظ ساختار)
            "remove_blank_lines": tk.BooleanVar(value=True),      # حذف خطوط خالی
            "remove_trailing_spaces": tk.BooleanVar(value=True),  # حذف فضاهای انتهای خط
            "use_short_operators": tk.BooleanVar(value=True),     # == →≡, != →≠, and →&, or →| (امن برای AI)
            "replace_quotes": tk.BooleanVar(value=True),          # " → " و ' → '
            "minify_json_like": tk.BooleanVar(value=True),        # فشرده‌سازی دیکشنری/لیست
            "remove_unnecessary_parentheses": tk.BooleanVar(value=True),
            "use_walrus_where_possible": tk.BooleanVar(value=False), # := فقط در موارد امن
            "replace_true_false_none": tk.BooleanVar(value=True), # True→1, False→0, None→~
            "shorten_common_words": tk.BooleanVar(value=True),    # def→د, return→ر, import→و etc.
            "remove_type_hints": tk.BooleanVar(value=True),       # حذف : int, -> str
            "replace_for_with_while": tk.BooleanVar(value=False), # فقط در موارد ساده (خطرناک، پیش‌فرض خاموش)
            "aggressive_number_format": tk.BooleanVar(value=True),# 1000 →1e3 اگر ممکن
            "replace_lambda": tk.BooleanVar(value=True),          # lambda x: → λx:
            "use_unicode_shortcuts": tk.BooleanVar(value=True),   # ∀ ∈ ∉ ∑ ∏ √ λ و ...
            "remove_asserts": tk.BooleanVar(value=True),          # حذف assert
            "remove_pass": tk.BooleanVar(value=True),             # حذف pass (در صورت امکان)
        }

        self.create_widgets()
        
    def create_widgets(self):
        # فریم اصلی
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # عنوان
        title = ttk.Label(main_frame, text="بهینه‌ساز توکن هوش مصنوعی", font=("Tahoma", 16, "bold"))
        title.grid(row=0, column=0, columnspan=3, pady=(0, 10))

        # فریم ورودی
        input_frame = ttk.LabelFrame(main_frame, text=" متن ورودی ")
        input_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=(0,5), pady=5)
        
        self.input_text = scrolledtext.ScrolledText(input_frame, height=15, font=("Tahoma", 10))
        self.input_text.pack(fill="both", expand=True, padx=5, pady=5)

        # دکمه‌های فایل
        file_frame = ttk.Frame(main_frame)
        file_frame.grid(row=2, column=0, columnspan=2, pady=5)
        ttk.Button(file_frame, text="بارگذاری فایل", command=self.load_file).pack(side="left", padx=5)
        ttk.Button(file_frame, text="ذخیره خروجی", command=self.save_output).pack(side="left", padx=5)

        # فریم گزینه‌ها
        options_frame = ttk.LabelFrame(main_frame, text=" تکنیک‌های بهینه‌سازی (تیک = فعال) ")
        options_frame.grid(row=1, column=2, rowspan=2, sticky="nsew", padx=5, pady=5)

        row = 0
        for key, var in self.options.items():
            text_fa = self.get_persian_name(key)
            cb = ttk.Checkbutton(options_frame, text=text_fa, variable=var)
            cb.grid(row=row, column=0, sticky="w", padx=10, pady=2)
            row += 1

        # دکمه اجرا
        ttk.Button(main_frame, text="بهینه‌سازی و کاهش توکن", command=self.optimize).grid(row=3, column=0, columnspan=3, pady=10)

        # فریم خروجی
        output_frame = ttk.LabelFrame(main_frame, text=" متن خروجی (بهینه‌شده) ")
        output_frame.grid(row=4, column=0, columnspan=3, sticky="nsew", pady=5)
        
        self.output_text = scrolledtext.ScrolledText(output_frame, height=12, font=("Tahoma", 10))
        self.output_text.pack(fill="both", expand=True, padx=5, pady=5)

        # آمار
        self.stats_label = ttk.Label(main_frame, text="", font=("Tahoma", 10))
        self.stats_label.grid(row=5, column=0, columnspan=3, pady=5)

        # وزن‌دهی به ردیف‌ها و ستون‌ها
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_rowconfigure(4, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)

    def get_persian_name(self, key):
        names = {
            "remove_extra_spaces": "حذف فضاهای اضافی",
            "single_line": "تبدیل به یک خط",
            "remove_comments": "حذف کامنت‌ها (# و \"\"\" \"\"\")",
            "remove_docstrings": "حذف Docstring",
            "shorten_print": "کوتاه‌سازی print → پ()",
            "shorten_variables": "کوتاه‌سازی نام متغیرها (هوشمند)",
            "remove_blank_lines": "حذف خطوط خالی",
            "remove_trailing_spaces": "حذف فضاهای انتهای خط",
            "use_short_operators": "استفاده از عملگرهای کوتاه (≡ ≠ ∧ ∨)",
            "replace_quotes": "یک‌نواخت‌سازی کوتیشن",
            "minify_json_like": "فشرده‌سازی دیکشنری و لیست",
            "remove_unnecessary_parentheses": "حذف پرانتزهای غیرضروری",
            "use_walrus_where_possible": "استفاده از := (Walrus)",
            "replace_true_false_none": "True→1, False→0, None→~",
            "shorten_common_words": "کوتاه‌سازی کلمات کلیدی (def→د، return→ر و ...)",
            "remove_type_hints": "حذف Type Hint",
            "replace_for_with_while": "تبدیل for به while (خطرناک)",
            "aggressive_number_format": "فرمت علمی اعداد بزرگ",
            "replace_lambda": "lambda → λ",
            "use_unicode_shortcuts": "استفاده از نمادهای یونیکد (∈ ∉ ∀ ∑ λ ...)",
            "remove_asserts": "حذف assert",
            "remove_pass": "حذف pass (در صورت امکان)",
        }
        return names.get(key, key)

    def load_file(self):
        path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt *.py *.md *.json"), ("All files", "*.*")])
        if path:
            with open(path, "r", encoding="utf-8") as f:
                self.input_text.delete(1.0, tk.END)
                self.input_text.insert(tk.END, f.read())

    def save_output(self):
        path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text file", "*.txt"), ("All files", "*.*")])
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(self.output_text.get(1.0, tk.END))
            messagebox.showinfo("موفقیت", "فایل با موفقیت ذخیره شد.")

    def optimize(self):
        original = self.input_text.get(1.0, tk.END)
        if not original.strip():
            messagebox.showwarning("هشدار", "متن ورودی خالی است.")
            return

        optimized = self.apply_optimizations(original)

        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, optimized)

        orig_len = len(original)
        opt_len = len(optimized)
        reduction = 100 * (orig_len - opt_len) / orig_len if orig_len > 0 else 0

        self.stats_label.config(
            text=f"قبل: {orig_len:,} کاراکتر | بعد: {opt_len:,} کاراکتر | کاهش: {reduction:.2f}%"
        )

    def apply_optimizations(self, text):
        import re

        # 1. حذف کامنت‌ها
        if self.options["remove_comments"].get():
            text = re.sub(r'#.*', '', text)  # خطی
            text = re.sub(r'"""[\s\S]*?"""|\'\'\'[\s\S]*?\'\'\'', '', text)  # چندخطی

        # 2. حذف Docstring در ابتدای فایل یا کلاس/تابع
        if self.options["remove_docstrings"].get():
            text = re.sub(r'^[\r\n\s]*("""|\'\'\')[\s\S]*?\1', '', text, count=1)  # اولین داکیومنت

        # 3. حذف خطوط خالی و فضاهای اضافی
        if self.options["remove_blank_lines"].get():
            lines = [line.rstrip() for line in text.splitlines() if line.strip() or line.endswith('\\')]
            text = '\n'.join(lines)

        if self.options["remove_extra_spaces"].get():
            text = re.sub(r'[ \t]+', ' ', text)
            text = re.sub(r'\s+\n', '\n', text)

        if self.options["remove_trailing_spaces"].get():
            text = '\n'.join(line.rstrip() for line in text.splitlines())

        # 4. تبدیل به یک خط (در انتها)
        if self.options["single_line"].get():
            text = text.replace('\n', '⏎').replace('\r', '')

        # 5. کوتاه‌سازی کلمات کلیدی (بسیار مؤثر)
        if self.options["shorten_common_words"].get():
            replacements = {
                'def ': 'د ', 'return ': 'ر ', 'import ': 'و ', 'from ': 'از ', 'as ': 'به‌عنوان ',
                'if ': 'اگ ', 'elif ': 'یااگ ', 'else:': 'دیگ:', 'for ': 'برا ', 'in ': 'در ',
                'while ': 'تا ', 'and ': "و ", 'or ': "یا ", 'not ': "نه ", 'is ': "هست ",
                'class ': 'کلاس ', 'try:': 'امتحان:', 'except ': 'به‌جز ', 'finally:': 'درنهایت:',
                'with ': 'با ', 'as ': 'به‌عنوان ', 'lambda ': 'λ ', 'raise ': 'پرتاب ',
                'assert ': 'مطمئن‌شو ', 'pass': 'بگذر', 'break': 'بشکن', 'continue': 'ادامه'
            }
            for old, new in replacements.items():
                text = text.replace(old, new)

        # 6. جایگزینی True/False/None
        if self.options["replace_true_false_none"].get():
            text = text.replace('True', '1').replace('False', '0').replace('None', '~')

        # 7. عملگرهای کوتاه
        if self.options["use_short_operators"].get():
            text = text.replace('==', '≡').replace('!=', '≠').replace(' and ', '∧').replace(' or ', '∨')

        # 8. حذف Type Hint
        if self.options["remove_type_hints"].get():
            text = re.sub(r':\s*[^=\n\->]+', '', text)   # : int, : str
            text = re.sub(r'->\s*[^:\n]+', '', text)     # -> str

        # 9. حذف assert و pass
        if self.options["remove_asserts"].get():
            text = re.sub(r'assert .*', '', text)
        if self.options["remove_pass"].get():
            text = re.sub(r'\n\s*pass\b', '', text)

        # 10. فشرده‌سازی دیکشنری و لیست
        if self.options["minify_json_like"].get():
            text = re.sub(r',\s+', ',', text)
            text = re.sub(r':\s+', ':', text)
            text = re.sub(r'\[\s+', '[', text)
            text = re.sub(r'\s+\]', ']', text)
            text = re.sub(r'{\s+', '{', text)
            text = re.sub(r'\s+}', '}', text)

        # 11. حذف پرانتزهای غیرضروری (محدود و امن)
        if self.options["remove_unnecessary_parentheses"].get():
            text = re.sub(r'\((\d+)\)', r'\1', text)  # (123) → 123

        # 12. استفاده از نمادهای یونیکد
        if self.options["use_unicode_shortcuts"].get():
            text = text.replace(' in ', '∈').replace(' not in ', '∉')
            text = text.replace('for ', '∀')
            text = text.replace('sum(', '∑(').replace('any(', '∃(').replace('all(', '∀(')

        # 13. کوتاه‌سازی print
        if self.options["shorten_print"].get():
            text = re.sub(r'print\((.*?)\)', r'پ(\1)', text)

        return text.strip() + '\n'

# اجرای برنامه
if __name__ == "__main__":
    root = tk.Tk()
    app = TokenOptimizer(root)
    root.mainloop()
