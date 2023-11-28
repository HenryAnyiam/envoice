#!/usr/bin/python3
from customtkinter import *
import json
from datetime import datetime


class SalesView(CTkScrollableFrame):
    """frame holding sales view page"""

    __file_path = 'file.json'
    __details = {}
    __sales_data = []

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_rowconfigure(0, weight=1)
        self.grid()
        self.reload()

        self.searchBar = CTkEntry(self, placeholder_text="Input Date",
                                  placeholder_text_color='#484848', width=400, height=40,
                                  corner_radius=3, border_color='#00a9ff', border_width=1,
                                  fg_color='#fff')
        self.searchBar.grid(row=0, column=0, columnspan=2, padx=(10, 2), pady=10)

        self.search = CTkButton(self, text='Search', width=80, height=40, corner_radius=5,
                                hover=True, hover_color='#3bc8ff', fg_color='#00a9ff',
                                text_color='white', anchor='center', border_spacing=5, command=self.search_ledger)
        self.search.grid(row=0, column=2, padx=2, pady=10)

        self.show_all = CTkButton(self, text='Show all', width=80, height=40, corner_radius=5,
                                  hover=True, hover_color='#3bc8ff', fg_color='#00a9ff',
                                  text_color='white', anchor='center', border_spacing=5, command=self.ShowAll)
        self.show_all.grid(row=0, column=3, padx=10, pady=10)

        self.NoData = CTkLabel(self, text='You Currently Have No Stored Sales', corner_radius=0, 
                               fg_color='transparent', font=('Times New Roman', 17),
                               text_color='#484848', anchor='center')
        self.NoData.grid_forget()
        self.ShowAll()

    def ShowAll(self):
        """show all from ledger"""
        self.reload()
        Ledger = self.__details.get('Ledger', {})
        if len(Ledger) == 0:
            self.NoData.grid(row=1, column=0, columnspan=3, padx=10, pady=50)
        else:
            self.NoData.grid_forget()
            self.list_sales(Ledger)
        self.row = 0

    def list_sales(self, data):
        """plot sales view"""

        for i in self.__sales_data:
            i.grid_forget()
        self.__sales_data.clear()
        self.row = 0

        data_keys = list(data.keys())
        data_keys.sort(key=self.sorting_function, reverse=True)
        for i in data_keys:
            data_header_label = CTkLabel(self, text=i, font=('Times New Roman', 22, 'bold'),
                                         fg_color='transparent', corner_radius=0,
                                         text_color='#484848', anchor='center')
            self.__sales_data.append(data_header_label)
            self.row += 1
            self.__sales_data[-1].grid(row=self.row, column=0, columnspan=4, padx=10, pady=10)
            details = data[i]
            self.row += 1
            table_items = CTkLabel(self, text='Items', font=('Times New Roman', 18, 'bold'),
                                   fg_color='transparent', corner_radius=0, width=200,
                                   text_color='#484848', anchor='center')
            self.__sales_data.append(table_items)
            self.__sales_data[-1].grid(row=self.row, column=0, padx=5, pady=10)
            table_price = CTkLabel(self, text='Price', font=('Times New Roman', 18, 'bold'),
                                   fg_color='transparent', corner_radius=0, width=100,
                                   text_color='#484848', anchor='center')
            self.__sales_data.append(table_price)
            self.__sales_data[-1].grid(row=self.row, column=1, padx=5, pady=10)
            table_qty = CTkLabel(self, text='Qty', font=('Times New Roman', 18, 'bold'),
                                 fg_color='transparent', corner_radius=0, width=100,
                                 text_color='#484848', anchor='center')
            self.__sales_data.append(table_qty)
            self.__sales_data[-1].grid(row=self.row, column=2, padx=5, pady=10)
            table_total = CTkLabel(self, text='Total', font=('Times New Roman', 18, 'bold'),
                                   fg_color='transparent', corner_radius=0, width=100,
                                   text_color='#484848', anchor='center')
            self.__sales_data.append(table_total)
            self.__sales_data[-1].grid(row=self.row, column=3, padx=5, pady=10)
            for j in details:
                self.row += 1
                item = CTkLabel(self, text=j.get('item'), font=('Times New Roman', 16),
                                fg_color='transparent', corner_radius=0, width=200,
                                text_color='#484848', anchor='center')
                self.__sales_data.append(item)
                self.__sales_data[-1].grid(row=self.row, column=0, padx=5, pady=2)
                price = CTkLabel(self, text=j.get('price'), font=('Times New Roman', 16),
                                   fg_color='transparent', corner_radius=0, width=100,
                                   text_color='#484848', anchor='center')
                self.__sales_data.append(price)
                self.__sales_data[-1].grid(row=self.row, column=1, padx=5, pady=2)
                qty = CTkLabel(self, text=j.get('qty'), font=('Times New Roman', 16),
                               fg_color='transparent', corner_radius=0, width=100,
                               text_color='#484848', anchor='center')
                self.__sales_data.append(qty)
                self.__sales_data[-1].grid(row=self.row, column=2, padx=5, pady=2)
                total = CTkLabel(self, text=j.get('total'), font=('Times New Roman', 16),
                                 fg_color='transparent', corner_radius=0, width=100,
                                 text_color='#484848', anchor='center')
                self.__sales_data.append(total)
                self.__sales_data[-1].grid(row=self.row, column=3, padx=5, pady=2)

    
    def search_ledger(self):
        """search ledger for a particular date"""
        search = self.searchBar.get()
        self.searchBar.delete(0, (len(search) + 1))
        retrieved = {}
        self.reload()
        Ledger = self.__details.get('Ledger', {})
        if search != '':
            for i in Ledger:
                if search in i:
                    retrieved[i] = Ledger[i]
            self.list_sales(retrieved)



    def reload(self):
        """reloads user details from file storage"""
        try:
            with open(self.__file_path, 'r', encoding="UTF-8") as my_file:
                self.__details = json.load(my_file)
        except Exception:
            pass

    def sorting_function(self, x):
        """function to sort ledger dictionary"""
        Date = x.replace('th', '').replace('nd', '').replace('rd', '')
        if Date[2:4] == 'st':
            Date = Date[0:2] + Date[4:]
        Date = datetime.strptime(Date, '%d %B %Y')
        return Date