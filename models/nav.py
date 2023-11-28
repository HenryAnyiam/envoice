#!/usr/bin/python3
import customtkinter


class NavFrame(customtkinter.CTkFrame):
    """Navigation Frame"""
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid()

        """add due buttons and label"""
        self.name = customtkinter.CTkLabel(self, text='E-Invoice', fg_color='transparent',
                                           font=('Times New Roman', 17), anchor='center',
                                           text_color='#484848', corner_radius=0)
        self.name.grid(row=0, column=0, padx=2, pady=20, sticky='ew')

        self.info = customtkinter.CTkButton(self, text="User Info", font=('Times New Roman', 17),
                                            hover_color='#00a9ff', hover=True, fg_color='transparent',
                                            text_color='#484848', anchor='w', corner_radius=0, border_spacing=5)
        self.info.grid(row=1, column=0, padx=2, sticky='ew')

        self.invoice = customtkinter.CTkButton(self, text='Generate Invoice', font=('Times New Roman', 17),
                                               hover_color='#00a9ff', hover=True, fg_color='transparent',
                                               text_color='#484848', anchor='w', corner_radius=0, border_spacing=5)
        self.invoice.grid(row=2, column=0, padx=2, sticky='ew')

        self.sales = customtkinter.CTkButton(self, text='View Sales', font=('Times New Roman', 17),
                                             hover_color='#00a9ff', hover=True, fg_color='transparent',
                                             text_color='#484848', anchor='w', corner_radius=0, border_spacing=5)
        self.sales.grid(row=3, column=0, padx=2, sticky='ew')