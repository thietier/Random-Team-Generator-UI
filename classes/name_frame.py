import os
import sys

if __package__ in (None, ""):
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

import customtkinter as ctk
from classes import ban_menu_exe as ban_menu
from classes.generated_teams_exe import generated_teams
from functions import utility_exe as utility

class name_options_frame(ctk.CTkFrame):
    def __init__(self,parent, controller, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.controller = controller
        heading_font=ctk.CTkFont(size=24)
        default_font=ctk.CTkFont(size=16)
        self.columnconfigure(0,weight=1)
        self.rowconfigure((0,1,2,3,4,5),weight=1)
        self.grid(row=0,column=3,sticky="nsew",padx=5,pady=5)
        self.grid_propagate(False)

        #name options frame title
        self.name_options_title=ctk.CTkLabel(self,text="Name Options", font=heading_font, border_width=2, border_color="#4133AB",corner_radius=5)
        self.name_options_title.grid(row=0,column=0,sticky="nsew",padx=10,pady=(10,5))

        #access the banned pairings menu
        self.banned_button=ctk.CTkButton(self,text="Banned Pairings", command=self.banned,fg_color="#4133AB", height=60, font=default_font)
        self.banned_button.grid(row=1,column=0,sticky="ew",padx=10,pady=5)

        #enter and remove names from the textbox and name list
        self.entry=ctk.CTkEntry(self,placeholder_text="Enter Names Here", height=60, font=default_font )
        self.entry.bind("<Return>", self.entry_enter_bind) #bind the Enter (Return) key to a function
        self.entry.grid(row=2,column=0, sticky="ew", padx=10, pady=5)
        self.removal=ctk.CTkEntry(self,placeholder_text="Remove Names Here", height=60, font=default_font)
        self.removal.bind("<Return>", self.removal_enter_bind)
        self.removal.grid(row=3,column=0, sticky="ew", padx=10, pady=5)

        self.reset_button=ctk.CTkButton(self, text="Reset List", command=self.reset, fg_color="#AB4133", height=60, font=default_font)
        self.reset_button.grid(row=4,column=0,sticky="ew", padx=10, pady=5)

        self.generate_button=ctk.CTkButton(self,text="Generate Pairs",command=lambda:generated_teams(parent=self, controller=controller), fg_color="#4133AB", height=60, font=default_font)
        self.generate_button.grid(row=5,column=0,sticky="ew",padx=10, pady=5)


#region methods
    def banned(self):
        ban_screen=ban_menu.ban_menu(self)

    def entry_enter_bind(self, event=None): 
        """
        Place the entered name into the earliest possible line, and remove the line number from the indicator list to avoid it being pasted over.
        Add the name to the list of names for random selection.
        """
        name=self.entry.get().strip()
        #ensure no duplicate names are added
        if name not in self.controller.name_list and utility.is_valid_name(name)==True:
            #if there aren't any slots left, do nothing
            if not self.controller.numerical_list:
                self.entry.delete(0,"end")
                return
            self.controller.name_box.configure(state="normal") #set the textbox to be editable
            try:
                self.controller.name_box.insert(f"{self.controller.numerical_list[0]+1}.0",f"{name}") #add the name to the textbox (+1 as textbox starts from 1)
                self.controller.name_list[self.controller.numerical_list[0]]=name #add the name to the index
                self.controller.numerical_list.pop(0) #remove the 1st item
            finally:
                self.controller.name_box.configure(state="disabled") #set the textbox to be uneditable
                self.entry.delete(0,"end") #delete widget text
                self.controller.counter.configure(text=f"Names: {512-len(self.controller.numerical_list)}")
        else: pass

    def removal_enter_bind(self, event=None):
        """
        Remove the name from all times it occurs in list/textbox, and add the respective indexes back to the numerical list.
        """
        self.controller.name_box.configure(state="normal") #set the textbox to be editable
        try:
            while self.removal.get().strip() in self.controller.name_list:
                index = self.controller.name_list.index(self.removal.get().strip()) #return the index of the first occurence in the list
                self.controller.name_list[index]=None #remove the name
                self.controller.name_box.delete(f"{index+1}.0",f"{index+2}.0") #delete all text on the textbox line
                self.controller.name_box.insert("511.0","\n") #replace the deleted line with a blank line at the end of the textbox (to avoid the textbox being shorter than 512 lines)
                self.controller.numerical_list.append(index) #add the value to the numerical list, then sort the list into order
                self.controller.numerical_list.sort()
        finally:
            self.controller.name_box.configure(state="disabled") #set the textbox to be uneditable
            self.removal.delete(0,"end")
            self.controller.counter.configure(text=f"Names: {512-len(self.controller.numerical_list)}")

    def reset(self, event=None):
        """
        Reset all lists and boxes.
        """
        self.controller.numerical_list=list(range(512))
        self.controller.name_list=[None]*512
        self.controller.name_box.configure(state="normal")
        try:
            self.controller.name_box.delete("0.0","end")
            self.controller.name_box.insert("0.0","\n"*511) #make the textbox have 512 lines
        finally:
            self.controller.name_box.configure(state="disabled")
        self.controller.counter.configure(text=f"Names: {512-len(self.controller.numerical_list)}")

#endregion