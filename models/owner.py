#!/usr/bin/python3
from customtkinter import *
from tkinter import filedialog
from PIL import Image
import json
from os import path


class Owner(CTkFrame):
    """frame holding user input details"""

    __file_path = 'file.json'
    __details = {}

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10), weight=1)
        self.grid()
        self.reload()

        self.Logo = CTkLabel(self, text=f'Company Logo: ', corner_radius=0,
                             fg_color='transparent', font=('Times New Roman', 17),
                             text_color='#484848', anchor='center')
        self.display()
        self.Logo.grid(row=0, column=0, padx=(10, 0), pady=20)

        self.set_logo = CTkButton(self, text='Select Logo', width=50, height=40, corner_radius=5,
                                  hover=True, hover_color='#3bc8ff', fg_color='#00a9ff',
                                  text_color='#484848', anchor='center', border_spacing=5, command=self.save_logo)
        self.set_logo.grid(row=0, column=1, padx=(0, 10), pady=20)

        self.CompanyName = CTkLabel(self, text=f'Company Name: {self.__details.get("Company_Name", "None Set")}',
                                    fg_color='transparent', font=('Times New Roman', 17),
                                    text_color='#484848', corner_radius=0, anchor='center')
        self.CompanyName.grid(row=1, column=0, padx=10, pady=(10, 1))

        self.setCompanyName = CTkEntry(self, placeholder_text="Input Company Name",
                                       placeholder_text_color='#484848', width=400, height=40,
                                       corner_radius=3, border_color='#00a9ff', border_width=1,
                                       fg_color='#fff')
        self.setCompanyName.grid(row=2, column=0, padx=(10, 0), pady=(1, 10))

        self.saveCompanyName = CTkButton(self, text='Save', width=80, height=40, corner_radius=5,
                                         hover=True, hover_color='#3bc8ff', fg_color='#00a9ff',
                                         text_color='#484848', anchor='center', border_spacing=5,
                                         command=self.save_name)
        self.saveCompanyName.grid(row=2, column=1, padx=(0, 10), pady=(1, 10))

        self.CompanyAddress = CTkLabel(self,
                                       text=f'Company Address: {self.__details.get("Company_Address", "None Set")}',
                                       fg_color='transparent', font=('Times New Roman', 17),
                                       text_color='#484848', corner_radius=0, anchor='center')
        self.CompanyAddress.grid(row=3, column=0, padx=10, pady=(10, 1))

        self.setCompanyAddress = CTkEntry(self, placeholder_text="Input Company Address",
                                          placeholder_text_color='#484848', width=400, height=40,
                                          corner_radius=3, border_color='#00a9ff', border_width=1,
                                          fg_color='#fff')
        self.setCompanyAddress.grid(row=4, column=0, padx=(10, 0), pady=(1, 10))

        self.saveCompanyAddress = CTkButton(self, text='Save', width=80, height=40, corner_radius=5,
                                            hover=True, hover_color='#3bc8ff', fg_color='#00a9ff',
                                            text_color='#484848', anchor='center', border_spacing=5,
                                            command=self.save_address)
        self.saveCompanyAddress.grid(row=4, column=1, padx=(0, 10), pady=(1, 10))

        self.State = CTkLabel(self, text=f'State: {self.__details.get("State", "None Set")}',
                              fg_color='transparent', font=('Times New Roman', 17),
                              text_color='#484848', corner_radius=0, anchor='center')
        self.State.grid(row=5, column=0, padx=10, pady=(10, 1))

        self.setState = CTkEntry(self, placeholder_text="Input State and Country",
                                 placeholder_text_color='#484848', width=400, height=40,
                                 corner_radius=3, border_color='#00a9ff', border_width=1,
                                 fg_color='#fff')
        self.setState.grid(row=6, column=0, padx=(10, 0), pady=(1, 10))

        self.saveState = CTkButton(self, text='Save', width=80, height=40, corner_radius=5,
                                   hover=True, hover_color='#3bc8ff', fg_color='#00a9ff',
                                   text_color='#484848', anchor='center', border_spacing=5, command=self.save_state)
        self.saveState.grid(row=6, column=1, padx=(0, 10), pady=(1, 10))

        self.Email = CTkLabel(self, text=f'Email Address: {self.__details.get("Email_Address", "None Set")}',
                              fg_color='transparent', font=('Times New Roman', 17),
                              text_color='#484848', corner_radius=0, anchor='center')
        self.Email.grid(row=7, column=0, padx=10, pady=(10, 1))

        self.setEmail = CTkEntry(self, placeholder_text="Input Company Email Address(es)",
                                 placeholder_text_color='#484848', width=400, height=40,
                                 corner_radius=3, border_color='#00a9ff', border_width=1,
                                 fg_color='#fff')
        self.setEmail.grid(row=8, column=0, padx=(10, 0), pady=(1, 10))

        self.saveEmail = CTkButton(self, text='Save', width=80, height=40, corner_radius=5,
                                   hover=True, hover_color='#3bc8ff', fg_color='#00a9ff',
                                   text_color='#484848', anchor='center', border_spacing=5, command=self.save_email)
        self.saveEmail.grid(row=8, column=1, padx=(0, 10), pady=(1, 10))

        self.Phone = CTkLabel(self, text=f'Phone: {self.__details.get("Phone", "None Set")}',
                              fg_color='transparent', font=('Times New Roman', 17),
                              text_color='#484848', corner_radius=0, anchor='center')
        self.Phone.grid(row=9, column=0, padx=20, pady=(10, 1))

        self.setPhone = CTkEntry(self, placeholder_text="Input Company phone Number(s)",
                                 placeholder_text_color='#484848', width=400, height=40,
                                 corner_radius=3, border_color='#00a9ff', border_width=1,
                                 fg_color='#fff')
        self.setPhone.grid(row=10, column=0, padx=(10, 0), pady=(1, 10))

        self.savePhone = CTkButton(self, text='Save', width=80, height=40, corner_radius=5,
                                   hover=True, hover_color='#3bc8ff', fg_color='#00a9ff',
                                   text_color='#484848', anchor='center', border_spacing=5, command=self.save_phone)
        self.savePhone.grid(row=10, column=1, padx=(0, 10), pady=(1, 10))

        self.Motto = CTkLabel(self, text=f'Motto: {self.__details.get("Motto", "None Set")}',
                              fg_color='transparent', font=('Times New Roman', 17),
                              text_color='#484848', corner_radius=0, anchor='center')
        self.Motto.grid(row=11, column=0, padx=20, pady=(10, 1))

        self.setMotto = CTkEntry(self, placeholder_text="Input Company Motto",
                                 placeholder_text_color='#484848', width=400, height=40,
                                 corner_radius=3, border_color='#00a9ff', border_width=1,
                                 fg_color='#fff')
        self.setMotto.grid(row=12, column=0, padx=(10, 0), pady=(1, 30))

        self.saveMotto = CTkButton(self, text='Save', width=80, height=40, corner_radius=5,
                                   hover=True, hover_color='#3bc8ff', fg_color='#00a9ff',
                                   text_color='#484848', anchor='center', border_spacing=5, command=self.save_motto)
        self.saveMotto.grid(row=12, column=1, padx=(0, 10), pady=(1, 30))

    def reload(self):
        """reloads user details from file storage"""
        try:
            with open(self.__file_path, 'r', encoding="UTF-8") as my_file:
                self.__details = json.load(my_file)
        except Exception:
            pass

    def save(self):
        """saved serialized user details to __file_path"""
        with open(self.__file_path, 'w', encoding="UTF-8") as my_file:
            json.dump(self.__details, my_file)

    def save_name(self):
        """get company name from input and save"""
        comp_name = self.setCompanyName.get()
        if comp_name != '':
            self.__details['Company_Name'] = comp_name
            self.save()
            self.setCompanyName.delete(0, (len(comp_name) + 1))
            self.CompanyName.configure(text=f'Company Name: {self.__details.get("Company_Name", "None Set")}')

    def save_address(self):
        """gets company address from input and save"""
        comp_add = self.setCompanyAddress.get()
        if comp_add != '':
            self.__details['Company_Address'] = comp_add
            self.save()
            self.setCompanyAddress.delete(0, (len(comp_add) + 1))
            self.CompanyAddress.configure(text=f'Company Address: {self.__details.get("Company_Address", "None Set")}')

    def save_state(self):
        """get state and country from input and save"""
        state = self.setState.get()
        if state != '':
            self.__details['State'] = state
            self.save()
            self.setState.delete(0, (len(state) + 1))
            self.State.configure(text=f'State: {self.__details.get("State", "None Set")}')

    def save_email(self):
        """get email from input and save"""
        email = self.setEmail.get()
        if email != '':
            self.__details['Email_Address'] = email
            self.save()
            self.setEmail.delete(0, (len(email) + 1))
            self.Email.configure(text=f'Email Address: {self.__details.get("Email_Address", "None Set")}')

    def save_phone(self):
        """get phone from input and save"""
        phone = self.setPhone.get()
        if phone != '':
            self.__details['Phone'] = phone
            self.save()
            self.setPhone.delete(0, (len(phone) + 1))
            self.Phone.configure(text=f'Phone: {self.__details.get("Phone", "None Set")}')

    def save_motto(self):
        """get motto from input and save"""
        motto = self.setMotto.get()
        if motto != '':
            self.__details['Motto'] = motto
            self.save()
            self.setMotto.delete(0, (len(motto) + 1))
            self.Motto.configure(text=f'Motto: {self.__details.get("Motto", "None Set")}')

    def save_logo(self):
        """get logo path and save"""
        image_path = filedialog.askopenfilename(title='open logo',
                                                filetypes=(('PNG', '.png'), ('JPEG', '.jpeg')))
        if image_path:
            self.__details['Logo_Path'] = image_path
            self.save()
            self.display()

    def display(self):
        """displays logo or provides a text if none is given"""
        image_path = self.__details.get("Logo_Path")
        if (image_path is not None) and (path.exists(image_path)):
            get_image = CTkImage(Image.open(image_path).resize((250, 106), Image.LANCZOS), size=(150, 64))
            self.Logo.configure(image=get_image, text='')
        else:
            self.Logo.configure(text="Company Logo: None Set")