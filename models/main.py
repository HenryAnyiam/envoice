#!/usr/bin/python3
from customtkinter import *
from nav import NavFrame
from owner import Owner
from invoice import Invoice_Form


class MainFrame(CTk):

    def __init__(self):
        super().__init__()

        self.title("Powerbaze e-invoice")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid()

        self.NavFrame = NavFrame(master=self, fg_color='#a0e9ff', corner_radius=0)
        self.NavFrame.grid(row=0, column=0, sticky='nsew')
        self.NavFrame.info.configure(fg_color='#00a9ff', command=self.show_user)
        self.NavFrame.invoice.configure(fg_color='transparent', command=self.show_invoice_tab)

        self.WorkFrame = CTkFrame(self, fg_color='white')
        self.WorkFrame.grid(row=0, column=1, sticky='nsew')

        self.HomeFrame = Owner(master=self.WorkFrame, fg_color='white',
                               border_width=1, border_color='#00a9ff', corner_radius=5)
        self.HomeFrame.grid(row=0, column=0, sticky='nesw', padx=40, pady=40)

        self.InvoiceFrame = Invoice_Form(master=self.WorkFrame, fg_color='white', width=500, height=500,
                                         border_width=1, border_color='#00a9ff', corner_radius=5,
                                         scrollbar_button_hover_color='#00a9ff')


    def show_user(self):
        """show user data tab"""
        self.InvoiceFrame.grid_forget()
        self.WorkFrame.grid_forget()
        self.WorkFrame.grid(row=0, column=1, sticky='nsew')
        self.HomeFrame.grid(row=0, column=0, sticky='nesw', padx=40, pady=40)
        self.NavFrame.info.configure(fg_color='#00a9ff')
        self.NavFrame.invoice.configure(fg_color='transparent')

    def show_invoice_tab(self):
        """show invoice tab"""
        self.HomeFrame.grid_forget()
        self.WorkFrame.grid_forget()
        self.WorkFrame.grid(row=0, column=1, sticky='nsew')
        self.InvoiceFrame.grid(row=0, column=0, sticky='nesw', padx=40, pady=40)
        self.NavFrame.info.configure(fg_color='transparent')
        self.NavFrame.invoice.configure(fg_color='#00a9ff')

if __name__ == "__main__":

    app = MainFrame()
    app.mainloop()