import tkinter as tk
#do NOT use this one. Graphical sample.
class Pages(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
    def show(self):
        self.lift()
class LoginPage(Pages):
    def __init__(self, *args, **kwargs):
        Pages.__init__(self, *args, **kwargs)
        label = tk.Label(self, text = "Login Screen")
        label.pack(side="top", fill="both", expand=True)
class QuitPage(Pages):
    def __init__(self, *args, **kwargs):
        Pages.__init__(self, *args, **kwargs)
        label = tk.Label(self, text = "Quit Screen")
        label.pack(side="top", fill="both", expand=True)

class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        p1 = LoginPage(self)
        p2 = QuitPage(self)
        buttonframe = tk.Frame(self)
        container = tk.Frame(self)
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        b1 = tk.Button(buttonframe, text="Page 1", command=p1.lift)
        b2 = tk.Button(buttonframe, text="Page 2", command=p2.lift)
        b1.pack(side="left")
        b2.pack(side="left")

        p1.show()

if __name__ == "__main__":
    root = tk.Tk()
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("400x400")
    root.mainloop()


root = Tk()

w=Label(root, text="Welcome. Please sign in to Lokahi below:")
w.pack()

root.mainloop()