from tkinter import *
import main as sc

tk = Tk()
tk.title('TRP calculator')
Label(tk, text='Name of the show : ').grid(row=0, padx=20, pady=10)

e1 = Entry(tk)
e1.grid(row=0, column=1)

trpScore = ""


# Define a function to show the popup message
def show_msg():
    score = sc.start_processing(e1.get())
    print("\n\n\n getting value compoundScore ----> ", score)
    label.config(text=f'Final TRP of the show is : {score}')
    return score


button = Button(tk, text='Calculate', width=25, command=show_msg)
button.grid(row=1, column=1, padx=20, pady=10)

label = Label(tk)
label.grid(column=1, padx=20, pady=10)

mainloop()
