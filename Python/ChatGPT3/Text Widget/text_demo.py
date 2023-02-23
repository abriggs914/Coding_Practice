import tkinter as tk

class CustomText(tk.Text):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text = tk.StringVar(value=self.get("1.0", tk.END))
        self.bind("<<CustomTextChanged>>", self._on_text_changed)
        
    def _on_text_changed(self, event):
        self.delete("1.0", tk.END)
        self.insert("1.0", self.text.get())
        
    def insert(self, index, text):
        super().insert(index, text)
        self._update_text_variable()
        
    def delete(self, index1, index2=None):
        super().delete(index1, index2)
        self._update_text_variable()
        
    def _update_text_variable(self):
        self.text.set(self.get("1.0", tk.END))
        self.event_generate("<<CustomTextChanged>>")
        
class DemoWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Demo Window")
        self.geometry("300x300")
        
        custom_text = CustomText(self)
        custom_text.pack(fill=tk.BOTH, expand=True)
        
        text_label = tk.Label(self, textvariable=custom_text.text)
        text_label.pack()
        
if __name__ == "__main__":
    app = DemoWindow()
    app.mainloop()