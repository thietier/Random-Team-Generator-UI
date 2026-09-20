import os
import sys

if __package__ in (None, ""):
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

import customtkinter as ctk
from functions import utility_exe as utility

class Team(ctk.CTkFrame):
            def __init__(self,parent,controller, team_number, *args, **kwargs):
                super().__init__(parent, *args, **kwargs)
                self.controller=controller
                self.team_number=team_number
                self.columnconfigure(0, weight=0, minsize=30)
                self.columnconfigure((1,2,3,4,5,6,7,8,9), weight=1)
                self.rowconfigure(0,weight=1)
                self.grid(row=self.team_number-1,column=0,sticky="nsew",padx=10,pady=(5,10))

                self.number_label=ctk.CTkLabel(self,text=f"{self.team_number}", anchor="center")
                self.number_label.grid(row=0,column=0,sticky="nsew",padx=(5,5),pady=10)

                self.team_name=ctk.CTkEntry(self, height=30, width=100, placeholder_text=f"Team {self.team_number}")
                self.team_name.grid(row=0, column=1, padx=5,pady=10)

                if self.team_number==1:
                    self.team_name.insert("0","OG")
                elif self.team_number==2:
                    self.team_name.insert("0","OO")   
                elif self.team_number==3:
                    self.team_name.insert("0","CG") 
                elif self.team_number==4:
                    self.team_name.insert("0","CO")  

                self.custom_name_frame=ctk.CTkFrame(self, width=170, fg_color="transparent")
                self.custom_name_frame.grid(row=0,column=3,columnspan=3,padx=5,pady=10, sticky="ew") 
                self.custom_name_frame.columnconfigure(0,weight=1)
                self.custom_name_frame.rowconfigure((0,1),weight=1)    

                self.custom_entry=ctk.CTkEntry(self.custom_name_frame,placeholder_text="Enter Name")
                self.custom_entry.bind("<Return>", self.custom_name_entry)
                self.custom_entry.grid(row=0,column=0,sticky="ew",padx=10,pady=(10,5))
                self.custom_removal=ctk.CTkEntry(self.custom_name_frame,placeholder_text="Remove Name")
                self.custom_removal.bind("<Return>", self.custom_name_removal)
                self.custom_removal.grid(row=1,column=0,sticky="ew",padx=10,pady=(5,10))

                self.team_member_list=[None]*16
                self.team_member_number_list=list(range(16))
                self.team_member_number=ctk.StringVar(master=self, value="2")

                self.team_members=ctk.CTkTextbox(self, height=90, width=170)
                self.team_members.grid(row=0, column=6, columnspan=3, sticky="nsew", padx=5, pady=10)
                self.team_members.insert("1.0","\n"*15)
                self.team_members.configure(state="disabled")

                self.custom_team_number_menu=ctk.CTkOptionMenu(self, width=80, fg_color="#4133AB", values=[str(i) for i in range(2,17)], variable=self.team_member_number, command=self.custom_team_member_menu_function)
                self.custom_team_number_menu.grid(row=0,column=9, padx=(5,10))
                if self.controller.custom_or_uniform.get()==0:
                    self.custom_team_number_menu.configure(state="disabled")

            def custom_name_entry(self, event=None):
                name = self.custom_entry.get().strip()
                if utility.is_valid_name(name)==False: #if the name isn't valid, do nothing
                    return
                #create a list of all the names already in a team to ensure no duplicates occur
                all_team_members=[]
                for team in self.controller.team_members_list:
                    all_team_members.extend(team)
                #only if there is space in the team for another member and the name doesn't appear on any other team
                if 16-len(self.team_member_number_list)<int(self.team_member_number.get()) and self.custom_entry.get().strip() not in all_team_members:
                    #if there aren't any slots left, do nothing
                    if name not in self.controller.name_list and not self.controller.numerical_list:
                        self.custom_entry.delete(0,"end")
                        return
                    self.team_members.configure(state="normal")
                    try:
                        self.team_members.insert(f"{self.team_member_number_list[0]+1}.0", name)
                        self.team_member_list[self.team_member_number_list[0]] = name
                        self.team_member_number_list.pop(0)
                        self.controller.team_members_list[self.team_number-1].append(name)
                        self.controller.static_team_members_list.append(name)
                    finally:
                        self.team_members.configure(state="disabled")
                        self.custom_entry.delete(0,"end")
                    #if the name is not on the name list, add it
                    if name not in self.controller.name_list:
                        self.controller.name_box.configure(state="normal") #set the textbox to be editable
                        try:
                            self.controller.name_box.insert(f"{self.controller.numerical_list[0]+1}.0",f"{name}") #add the name to the textbox (+1 as textbox starts from 1)
                            self.controller.name_list[self.controller.numerical_list[0]]=name #add the name to the index
                            self.controller.numerical_list.pop(0) #remove the 1st item
                        finally:
                            self.controller.name_box.configure(state="disabled") #set the textbox to be uneditable
                            self.controller.counter.configure(text=f"Names: {512-len(self.controller.numerical_list)}")
                else: pass

            def custom_name_removal(self, event=None):
                self.team_members.configure(state="normal")
                name=self.custom_removal.get().strip()
                try:
                    while name in self.team_member_list:
                        name_index = self.team_member_list.index(name)
                        self.team_member_list.pop(name_index)
                        self.team_member_list.append(None)
                        self.controller.team_members_list[self.team_number-1].remove(name)
                        if name in self.controller.static_team_members_list:
                            self.controller.static_team_members_list.remove(name)
                        self.team_members.delete(f"{name_index+1}.0",f"{name_index+2}.0")
                        self.team_members.insert("15.0","\n")
                        self.team_member_number_list.append(name_index)
                        self.team_member_number_list.sort()
                finally:
                    self.team_members.configure(state="disabled")
                    self.custom_removal.delete(0,"end")

            def custom_team_member_menu_function(self, value=None):
                self.controller.number_on_team_list[self.team_number-1] = int(self.custom_team_number_menu.get())
