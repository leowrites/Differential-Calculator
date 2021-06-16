import tkinter as tk
import derivative
import parser

class app():
    def __init__(self):
        self.w = tk.Tk()
        self.w.title('Derivative Calculator For Mr Klassen')
        self.w.geometry("1000x500")

        self.main_c = tk.Canvas(self.w)
        self.main_c.pack()

        self.bottom = tk.Label(
            master=self.main_c, text="Leo's Derivative Calculator")
        self.bottom.config(font=('', 30))
        self.bottom.grid(row=0, column=0)
        
        self.bottom = tk.Label(master=self.main_c, text="What's Decimals? -- Mr.Sharp")
        self.bottom.config(font=('',30))
        self.bottom.grid(row=5,column=0)

        self.in_r = tk.Entry(master=self.main_c)
        self.in_r.grid(row=1, column=0)
        self.in_r.focus_set()

        self.in_b = tk.Button(master=self.main_c, text='derive :)', width=20, command=self.update_text)
        self.in_b.grid(row=1, column=1)

        self.dis_in = tk.Label(master=self.main_c, text='Your Input: ')
        self.dis_in.grid(row=2, column=0)
        self.dis_uin = tk.Label(master=self.main_c, text='')
        self.dis_uin.grid(row=2, column=1)
        self.dis_text = tk.Label(master=self.main_c, text='Derivative: ')
        self.dis_text.grid(row=3, column=0)
        self.dis_out = tk.Label(master=self.main_c, text='')
        self.dis_out.grid(row=3, column=1)

    def main(self):
        self.w.mainloop()

    def update_text(self):
        """
        get an equation and update text
        """
        inp = self.in_r.get()
        self.dis_uin['text'] = inp
        answer = self.fun(inp)
        if answer == None:
            self.dis_out['text'] = 'Error! Try Again'
        else:
            self.dis_out['text'] = answer
        self.in_r.delete(0,'end')
    
    def info_update(self):
        pass
    
    def fun(self, equation):
        d = derivative.Differential(equation)
        try:
            result = d.derive()
        except TypeError:
            return 'Error! Try Again'
        d.print_tree()
        return result
