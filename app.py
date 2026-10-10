import customtkinter as ctk
from tkinterdnd2 import TkinterDnD, DND_ALL
import gen_certs
import os


class App(ctk.CTk, TkinterDnD.DnDWrapper):
    def __init__(self):
        super().__init__()
        self.TkdndVersion = TkinterDnD._require(self)
        
        self.title("CustomTkinter Drag & Drop")
        self.geometry("500x350")
        self.resizable(False, False)

        ctk.set_appearance_mode("dark")
        
        self.label = ctk.CTkLabel(
            self, 
            text="Перетащите файл или папку сюда", 
            width=400, 
            height=300,
            fg_color="#2b2b2b",
            corner_radius=8
        )
        self.label.pack(padx=20, pady=5, fill="both", expand=False)
        
        self.apply = ctk.CTkLabel(
            self, 
            text="", 
            width=400, 
            height=10,
        )
        self.apply.pack(padx=20, pady=5, fill="both", expand=True)
        
        self.label.drop_target_register(DND_ALL)
        self.label.dnd_bind("<<Drop>>", self.handle_drop)

    def handle_drop(self, event):
        data = event.data
        result = gen_certs.excel_to_pdfs(data, os.path.expanduser(os.path.join('~/Documents', 'certs')))
        if result == 0:
            self.apply.configure(text="Файл сохранен в папку Documents/certs")
        else:
            self.apply.configure(text="Произошла ошибка при обработке файла")

if __name__ == "__main__":
    app = App()
    app.mainloop()