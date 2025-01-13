from customtkinter import CTk
from ui import LinOLS

if __name__ == "__main__":
    window = CTk()
    app = LinOLS(window)
    window.mainloop()
