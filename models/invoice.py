#!/usr/bin/python3
from customtkinter import *
from tkinter import filedialog
from PIL import Image
import json
from os import path
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import date
import locale


class Invoice_Form(CTkScrollableFrame):
    """frame to hold details to generate invoice"""

    __invoice_data = {}
    __items = []
    __table_data = []
    __file_path = 'file.json'

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)
        self.grid()
        self.reload()

        self.getCustomerName = CTkEntry(self, placeholder_text="Input Customer Name",
                                        placeholder_text_color='#484848', width=400, height=40,
                                        corner_radius=3, border_color='#00a9ff', border_width=1,
                                        fg_color='#fff', text_color='black')
        self.getCustomerName.grid(row=0, column=0, columnspan=3, padx=10, pady=(30, 10))

        self.getCustomerAddress = CTkEntry(self, placeholder_text="Input Customer Address",
                                           placeholder_text_color='#484848', width=400, height=40,
                                           corner_radius=3, border_color='#00a9ff', border_width=1,
                                           fg_color='#fff', text_color='black')
        self.getCustomerAddress.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

        self.getCustomerPhone = CTkEntry(self, placeholder_text="Input Customer Phone Number",
                                         placeholder_text_color='#484848', width=400, height=40,
                                         corner_radius=3, border_color='#00a9ff', border_width=1,
                                         fg_color='#fff', text_color='black')
        self.getCustomerPhone.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

        self.row = 3
        self.getItem = CTkEntry(self, placeholder_text="Input Item", text_color='black',
                                placeholder_text_color='#484848', width=400, height=40,
                                corner_radius=3, border_color='#00a9ff', border_width=1,
                                fg_color='#fff')
        self.getItem.grid(row=(self.row + 1), column=0, columnspan=3, padx=10, pady=10)

        self.getPrice = CTkEntry(self, placeholder_text="Input Unit Price", text_color='black',
                                 placeholder_text_color='#484848', width=150, height=40,
                                 corner_radius=3, border_color='#00a9ff', border_width=1,
                                 fg_color='#fff')
        self.getPrice.grid(row=(self.row + 2), column=0, padx=(40, 2), pady=10)

        self.getQty = CTkEntry(self, placeholder_text="Qty", text_color='black',
                               placeholder_text_color='#484848', width=60, height=40,
                               corner_radius=3, border_color='#00a9ff', border_width=1,
                               fg_color='#fff')
        self.getQty.grid(row=(self.row + 2), column=1, padx=2, pady=10)

        self.getType = CTkEntry(self, placeholder_text="Type", text_color='black',
                                placeholder_text_color='#484848', width=100, height=40,
                                corner_radius=3, border_color='#00a9ff', border_width=1,
                                fg_color='#fff')
        self.getType.grid(row=(self.row + 2), column=2, padx=(2, 30), pady=10)

        self.deleteLast = CTkButton(self, text='Delete Last Entry', width=80, height=40, corner_radius=5,
                                    hover=True, hover_color='#3bc8ff', fg_color='#00a9ff',
                                    text_color='white', anchor='center', border_spacing=5, command=self.delete_last)
        self.deleteLast.grid(row=(self.row + 3), column=0, padx=(10, 2), pady=10)

        self.add = CTkButton(self, text='Add Entry', width=80, height=40, corner_radius=5,
                             hover=True, hover_color='#3bc8ff', fg_color='#00a9ff',
                             text_color='white', anchor='center', border_spacing=5, command=self.add_item)
        self.add.grid(row=(self.row + 3), column=1, padx=2, pady=10)
        
        self.clearList = CTkButton(self, text='Clear Entries', width=100, height=40, corner_radius=5,
                                   hover=True, hover_color='#3bc8ff', fg_color='#00a9ff',
                                   text_color='white', anchor='center', border_spacing=5, command=self.clear_list)
        self.clearList.grid(row=(self.row + 3), column=2, padx=(2, 30), pady=10)

        self.status = CTkOptionMenu(self, width=100, height=40,
                                    values=['Part Payment', 'Paid', 'Not Paid'], text_color='#484848',
                                    fg_color='white', corner_radius=5, hover=True,
                                    button_hover_color='#3bc8ff', dropdown_fg_color='white',
                                    dropdown_hover_color='#3bc8ff', button_color='#00a9ff',
                                    dropdown_text_color='#484848', dynamic_resizing=False)
        self.status.set('Status')
        self.status.grid(row=(self.row + 4), column=0, padx=(10, 2), pady=10)

        self.Warranty = CTkOptionMenu(self, width=105, height=40,
                                      values=['One Year', '6 Months', 'None'], text_color='#484848',
                                      fg_color='white', corner_radius=5, hover=True,
                                      button_hover_color='#3bc8ff', dropdown_fg_color='white',
                                      dropdown_hover_color='#3bc8ff', button_color='#00a9ff',
                                      dropdown_text_color='#484848', dynamic_resizing=False)
        self.Warranty.set('Warranty')
        self.Warranty.grid(row=(self.row + 4), column=1, padx=2, pady=10)

        self.Installation = CTkEntry(self, placeholder_text="Installation", text_color='black',
                                     placeholder_text_color='#484848', width=120, height=40,
                                     corner_radius=3, border_color='#00a9ff', border_width=1,
                                     fg_color='#fff')
        self.Installation.grid(row=(self.row + 4), column=2, padx=(2, 40), pady=10)

        self.preview = CTkButton(self, text='Preview Items', width=100, height=40, corner_radius=5,
                                 hover=True, hover_color='#3bc8ff', fg_color='#00a9ff',
                                 text_color='white', anchor='center', border_spacing=5, command=self.PreviewItem)
        self.preview.grid(row=(self.row + 5), column=0, padx=(30, 2), pady=(10, 30))

        self.addToLedger = CTkButton(self, text='Add to Ledger', width=80, height=40, corner_radius=5,
                                     hover=True, hover_color='#3bc8ff', fg_color='#00a9ff',
                                     text_color='white', anchor='center', border_spacing=5, 
                                     command=self.add_to_ledger)
        self.addToLedger.grid(row=(self.row + 5), column=1, padx=2, pady=(10, 30))

        self.generate = CTkButton(self, text='Generate Invoice', width=80, height=40, corner_radius=5,
                                  hover=True, hover_color='#3bc8ff', fg_color='#00a9ff',
                                  text_color='white', anchor='center', border_spacing=5, command=self.generate_pdf)
        self.generate.grid(row=(self.row + 5), column=2, padx=(2, 40), pady=(10, 30))

    def reload(self):
        """reloads user details from file storage"""
        try:
            with open(self.__file_path, 'r', encoding="UTF-8") as my_file:
                self.__invoice_data = json.load(my_file)
        except Exception:
            pass

    def save(self):
        """saved serialized user details to __file_path"""
        with open(self.__file_path, 'w', encoding="UTF-8") as my_file:
            json.dump(self.__invoice_data, my_file)

    def add_to_ledger(self):
        """save current stock"""
        Ledger = self.__invoice_data.get('Ledger', {})
        Date = date.today().strftime("%dth %B %Y")
        if Date[1] == '1':
                Date = Date.replace('th', 'st')
        elif Date[1] == '2':
            Date = Date.replace('th', 'nd')
        elif Date[1] == '3':
            Date = Date.replace('th', 'rd')
        sales = Ledger.get(Date, [])
        sales.extend(self.__items)
        Ledger[Date] = sales
        self.__invoice_data['Ledger'] = Ledger
        self.save()

    def delete_last(self):
        """delete last entered entry"""
        del self.__items[-1]
        self.__table_data[-1].grid_forget()
        del self.__table_data[-1]
        self.row -= 1
        self.rearrange()

    def rearrange(self):
        """rearrange the grid as it should be"""
        self.getItem.grid_forget()
        self.getItem.grid(row=(self.row + 1), column=0, columnspan=3, padx=10, pady=10)
        self.getPrice.grid_forget()
        self.getPrice.grid(row=(self.row + 2), column=0, padx=(40, 2), pady=10)
        self.getQty.grid_forget()
        self.getQty.grid(row=(self.row + 2), column=1, padx=2, pady=10)
        self.getType.grid_forget()
        self.getType.grid(row=(self.row + 2), column=2, padx=(2, 30), pady=10)
        self.add.grid_forget()
        self.add.grid(row=(self.row + 3), column=1, padx=2, pady=10)
        self.deleteLast.grid_forget()
        self.deleteLast.grid(row=(self.row + 3), column=0, padx=(10, 2), pady=10)
        self.clearList.grid_forget()
        self.clearList.grid(row=(self.row + 3), column=2, padx=(2, 30), pady=10)
        self.status.grid_forget()
        self.status.grid(row=(self.row + 4), column=0, padx=(10, 2), pady=10)
        self.Warranty.grid_forget()
        self.Warranty.grid(row=(self.row + 4), column=1, padx=2, pady=10)
        self.Installation.grid_forget()
        self.Installation.grid(row=(self.row + 4), column=2, padx=(2, 40), pady=10)
        self.preview.grid_forget()
        self.preview.grid(row=(self.row + 5), column=0, padx=(30, 2), pady=(10, 30))
        self.addToLedger.grid_forget()
        self.addToLedger.grid(row=(self.row + 5), column=1, padx=2, pady=(10, 30))
        self.generate.grid_forget()
        self.generate.grid(row=(self.row + 5), column=2, padx=(2, 40), pady=(10, 30))
        

    def add_item(self):
        """add item to distionary"""
        new = {}
        item = self.getItem.get()
        price = self.getPrice.get()
        qty = self.getQty.get()
        type = self.getType.get()
        p_length = len(price)
        q_length = len(qty)

        if price != '':
            try:
                price = int(price)
            except ValueError:
                self.getPrice.delete(0, (p_length + 1))
                price = ''

        if qty != '':
            try:
                qty = int(qty)
            except ValueError:
                self.getQty.delete(0, (q_length + 1))
                qty = ''
        else:
            qty = 1

        if (item != '') and (price != ''):
            new['item'] = item
            new['price'] = price
            new['qty'] = qty
            if type != '':
                new['qty'] = f'{qty}{type}'
                self.getType.delete(0, (len(type) + 1))
            new['total'] = price * qty
            self.getPrice.delete(0, (p_length + 1))
            self.getQty.delete(0, (q_length + 1))
            self.getItem.delete(0, (len(item) + 1))
            self.__items.append(new)
            data = f'{new["qty"]} of {new["item"]} at {new["price"]} each'
            data_label = CTkLabel(self, text=data, font=('Times New Roman', 17),
                                  fg_color='transparent', corner_radius=0,
                                  text_color='#484848', anchor='center')
            self.__table_data.append(data_label)
            self.__table_data[-1].grid(row=self.row, column=0, columnspan=3, padx=10, pady=2)
            self.row += 1
            self.grid_rowconfigure((self.row + 3), weight=1)
            self.rearrange()

    def generate_pdf(self):
        """generate PDF"""

        self.reload()
        file_path = filedialog.asksaveasfilename(title="Save Invoice",
                                                 filetypes=(("PDF files", ".pdf"), ("All files", "*.*")))
        if file_path:
            if not file_path.endswith('.pdf'):
                file_path = f'{file_path}.pdf'
            pdf = canvas.Canvas(file_path, pagesize=letter)
            company_logo_path = self.__invoice_data.get('Logo_Path')
            if company_logo_path and path.exists(company_logo_path):
                pdf.drawInlineImage(company_logo_path, 50, 700, width=150, height=64)
            compMotto = self.__invoice_data.get('Motto')
            if compMotto:
                pdf.setFont("Times-Italic", 10)
                pdf.drawString(50, 690, compMotto)

            name = self.getCustomerName.get()
            self.getCustomerName.delete(0, (len(name) + 1))
            address = self.getCustomerAddress.get()
            self.getCustomerAddress.delete(0, (len(address) + 1))
            phone = self.getCustomerPhone.get()
            self.getCustomerPhone.delete(0, (len(phone) + 1))
            y_cord = 660
            pdf.setFont("Times-Bold", 14)
            pdf.drawString(50, y_cord, name)
            pdf.setFont("Times-Roman", 12)
            if address != '':
                y_cord -= 20
                pdf.drawString(50, y_cord, address)
            if phone != '':
                y_cord -= 20
                pdf.drawString(50, y_cord, phone)
            compName = self.__invoice_data.get('Company_Name')
            compAdd = self.__invoice_data.get('Company_Address')
            compState = self.__invoice_data.get('State')
            compEmail = self.__invoice_data.get('Email_Address')
            compPhone = self.__invoice_data.get('Phone')
            y_cord = 740
            pdf.setFont("Times-Bold", 14)
            if compName:
                pdf.drawString(430, y_cord, compName)
                y_cord -= 20
            pdf.setFont("Times-Roman", 12)
            if compAdd:
                pdf.drawString(430, y_cord, compAdd)
                y_cord -= 20
            if compState:
                pdf.drawString(430, y_cord, compState)
                y_cord -= 20
            if compEmail:
                pdf.drawString(430, y_cord, compEmail)
                y_cord -= 20
            if compPhone:
                pdf.drawString(430, y_cord, compPhone)
                y_cord -= 20

            Date = date.today().strftime("%dth %B %Y")
            if Date[1] == '1':
                Date = Date.replace('th', 'st')
            elif Date[1] == '2':
                Date = Date.replace('th', 'nd')
            elif Date[1] == '3':
                Date = Date.replace('th', 'rd')
            pdf.drawString(430, y_cord, f'Date: {Date}')
            y_cord = 530
            if len(self.__items) > 10:
                y_cord = 600

            pdf.setFont("Times-Bold", 14)
            pdf.drawString(220, y_cord, "Sales Invoice")
            y_cord -= 30

            pdf.setFont("Times-Bold", 12)
            pdf.drawString(50, y_cord, "Item")
            pdf.drawString(300, y_cord, "Qty")
            pdf.drawString(350, y_cord, "Price")
            pdf.drawString(450, y_cord, "Total")
            pdf.setFont("Times-Roman", 12)

            total = 0
            y_cord -= 30
            for item in self.__items:
                locale.setlocale(locale.LC_ALL, '')
                pdf.drawString(50, y_cord, item['item'])
                pdf.drawString(300, y_cord, f"{item['qty']}")
                f_price = locale.format_string("%d", item['price'], grouping=True)
                pdf.drawString(350, y_cord, f_price)
                f_total = locale.format_string("%d", item['total'], grouping=True)
                pdf.drawString(450, y_cord, f_total)
                total += item['total']
                y_cord -= 20

            service = self.Installation.get()
            if service != '':
                try:
                    length = len(service)
                    service = int(service)
                except ValueError:
                    pass
                else:
                    total += service
                    pdf.drawString(350, y_cord, "Installation:")
                    f_service = locale.format_string("%d", service, grouping=True)
                    pdf.drawString(450, y_cord, f"#{f_service}")
                self.Installation.delete(0, (length + 1))
                y_cord -= 20
            pdf.setFont("Times-Bold", 14)
            hex_color = '#00a9ff'
            custom_color = tuple(int(hex_color[i:i + 2], 16) / 255.0 for i in (1, 3, 5))
            pdf.setFillColorRGB(*custom_color)
            y_cord -= 10
            pdf.drawString(350, y_cord, "Total Amount:")
            f_total = locale.format_string("%d", total, grouping=True)
            pdf.drawString(450, y_cord, f"#{f_total}")

            y_cord -= 50
            if y_cord > 300:
                y_cord = 300
            pdf.setFillColorRGB(0, 0, 0)
            pdf.setFont("Times-Roman", 12)
            warranty = self.Warranty.get()
            if (warranty != '') and (warranty != 'Warranty') and (warranty != 'None'):
                full_warranty = f'This purchase includes a {warranty} warranty service.'
                pdf.drawString(50, y_cord, full_warranty)
                pdf.setFont("Times-Italic", 12)
                y_cord -= 20
                pdf.drawString(50, y_cord, '(Terms and conditions apply).')
                pdf.setFont("Times-Roman", 12)
                y_cord -= 20
                self.Warranty.set('Warranty')
            status = self.status.get()
            if (status != '') and (status != 'Status'):
                pdf.drawString(50, y_cord, f'Payment Status: {status}')
                y_cord -= 20
                self.status.set('Status')
            pdf.drawString(50, y_cord, 'For any inquiries or assistance, Contact us.')
            y_cord -= 20
            pdf.drawString(50, y_cord, f"Thank you for choosing {self.__invoice_data.get('Company_Name', 'us')}.")
            pdf.save()
            for i in self.__table_data:
                i.grid_forget()
            self.__table_data.clear()
            self.__items.clear()
            self.row = 3
            self.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)
            self.rearrange()
    
    def clear_list(self):
        """clears current list"""
        for i in self.__table_data:
                i.grid_forget()
        self.__table_data.clear()
        self.__items.clear()
        self.row = 3
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)
        self.rearrange()

    def PreviewItem(self):
        """top level frame for item preview"""
        New = CTkToplevel(self)
        New.title('Preview Added Items')
        New.grid_columnconfigure(0, weight=1)
        New.grid_rowconfigure(0, weight=1)

        ItemFrame = CTkScrollableFrame(New, fg_color='#a0e9ff', width=650, height=300,
                                       border_width=1, border_color='#00a9ff', corner_radius=0,
                                       scrollbar_button_hover_color='#00a9ff')
        ItemFrame.grid(row=0, column=0, sticky='nesw')
        table_items = CTkLabel(ItemFrame, text='Items', font=('Times New Roman', 18, 'bold'),
                                fg_color='transparent', corner_radius=0, width=200,
                                text_color='#484848', anchor='center')
        table_items.grid(row=0, column=0, padx=5, pady=10)
        table_price = CTkLabel(ItemFrame, text='Price', font=('Times New Roman', 18, 'bold'),
                                fg_color='transparent', corner_radius=0, width=100,
                                text_color='#484848', anchor='center')
        table_price.grid(row=0, column=1, padx=5, pady=10)
        table_qty = CTkLabel(ItemFrame, text='Qty', font=('Times New Roman', 18, 'bold'),
                                fg_color='transparent', corner_radius=0, width=100,
                                text_color='#484848', anchor='center')
        table_qty.grid(row=0, column=2, padx=5, pady=10)
        table_total = CTkLabel(ItemFrame, text='Total', font=('Times New Roman', 18, 'bold'),
                                fg_color='transparent', corner_radius=0, width=100,
                                text_color='#484848', anchor='center')
        table_total.grid(row=0, column=3, padx=5, pady=10)
        Trow = 0
        ftotal = 0
        for j in self.__items:
            Trow += 1
            item = CTkLabel(ItemFrame, text=j.get('item'), font=('Times New Roman', 16),
                            fg_color='transparent', corner_radius=0, width=200,
                            text_color='#484848', anchor='center')
            item.grid(row=Trow, column=0, padx=5, pady=2)
            price = CTkLabel(ItemFrame, text=j.get('price'), font=('Times New Roman', 16),
                                fg_color='transparent', corner_radius=0, width=100,
                                text_color='#484848', anchor='center')
            price.grid(row=Trow, column=1, padx=5, pady=2)
            qty = CTkLabel(ItemFrame, text=j.get('qty'), font=('Times New Roman', 16),
                            fg_color='transparent', corner_radius=0, width=100,
                            text_color='#484848', anchor='center')
            qty.grid(row=Trow, column=2, padx=5, pady=2)
            total = CTkLabel(ItemFrame, text=j.get('total'), font=('Times New Roman', 16),
                                fg_color='transparent', corner_radius=0, width=100,
                                text_color='#484848', anchor='center')
            total.grid(row=Trow, column=3, padx=5, pady=2)
            ftotal += int(j.get('total'))
        service = self.Installation.get()
        if service != '':
            try:
                service = int(service)
            except ValueError:
                pass
            else:
                ftotal += service
                installation_label = CTkLabel(ItemFrame, text='Installation:', font=('Times New Roman', 18, 'bold'),
                                              fg_color='transparent', corner_radius=0, width=200,
                                              text_color='#484848', anchor='center')
                Trow += 1
                installation_label.grid(row=Trow, column=0, padx=5, pady=(30, 2))
                installation_price = CTkLabel(ItemFrame, text=locale.format_string("%d", service, grouping=True),
                                              fg_color='transparent', corner_radius=0, width=200,
                                              text_color='#484848', anchor='center',  font=('Times New Roman', 18, 'bold'))
                installation_price.grid(row=Trow, column=1, padx=5, pady=(30, 2))
        Trow += 1
        final_total_label = CTkLabel(ItemFrame, text='Total:', font=('Times New Roman', 18, 'bold'),
                                fg_color='transparent', corner_radius=0, width=200,
                                text_color='#484848', anchor='center')
        
        final_total = CTkLabel(ItemFrame, text=locale.format_string("%d", ftotal, grouping=True),
                                fg_color='transparent', corner_radius=0, width=200,
                                text_color='#484848', anchor='center',  font=('Times New Roman', 18, 'bold'))
        if service == '':
            final_total_label.grid(row=Trow, column=0, padx=5, pady=30)
            final_total.grid(row=Trow, column=1, padx=5, pady=30)
        else:
            final_total_label.grid(row=Trow, column=0, padx=5, pady=(2, 30))
            final_total.grid(row=Trow, column=1, padx=5, pady=(2, 30))