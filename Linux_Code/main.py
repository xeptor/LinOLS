from ui import LinOLS
from customtkinter import CTk

if __name__ == "__main__":
    window = CTk(className='LinOLS')
    app = LinOLS(window)
    window.mainloop()