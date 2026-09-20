import os
import sys

if __package__ in (None, ""):
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

import customtkinter as ctk
from classes.team import Team
import random
from functions import utility

class team_options_frame(ctk.CTkFrame):
    def __init__(self,parent, controller, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.controller = controller
        heading_font=ctk.CTkFont(size=24)
        self.configure(border_width=2, border_color="#4133AB")
        self.columnconfigure(0,weight=1)  
        self.rowconfigure(0,weight=2)
        self.rowconfigure(1,weight=12)
        self.rowconfigure(2,weight=18)
        self.grid(row=0,column=0,columnspan=3,sticky="nsew",padx=5,pady=5)
        self.grid_propagate(False)
        medium_font=ctk.CTkFont(size=20)
        default_font=ctk.CTkFont(size=16)

        self.team_box_title=ctk.CTkLabel(self,text="Team Options", font=heading_font, border_width=2, border_color="#4133AB", corner_radius=5)
        self.team_box_title.grid(row=0,column=0,sticky="nsew",padx=10,pady=(10,5))

        #region top team frame
        self.top_team_frame=ctk.CTkFrame(self, border_width=2, border_color="#4133AB")
        self.top_team_frame.columnconfigure((0,1),weight=1)
        self.top_team_frame.rowconfigure((0,1,2),weight=1)
        self.top_team_frame.grid(row=1,column=0,sticky="nsew",padx=10,pady=5)
        self.top_team_frame.grid_propagate(False)

        self.number_of_teams_frame=ctk.CTkFrame(self.top_team_frame, border_width=2, border_color="#4133AB")
        self.number_of_teams_frame.grid(row=0,column=0,sticky="nsew",padx=(10,5),pady=10)
        self.number_of_teams_frame.columnconfigure((0,1,2),weight=1)
        self.number_of_teams_frame.rowconfigure(0,weight=1)
        self.teams_slider=ctk.CTkSlider(self.number_of_teams_frame, from_=2, to=32, number_of_steps=31, command=self.load_teams, variable=self.controller.number_of_teams)
        self.teams_slider.set(4)
        self.teams_slider.grid(row=0,column=0,columnspan=2,sticky="ew",padx=(10,5))
        self.teams_slider_label=ctk.CTkLabel(self.number_of_teams_frame,text="4 Teams", width=90)
        self.teams_slider_label.grid(row=0,column=2,sticky="ew",padx=(5,10))

        self.number_on_team_frame=ctk.CTkFrame(self.top_team_frame, border_width=2, border_color="#4133AB")
        self.number_on_team_frame.grid(row=1,rowspan=2,column=0,sticky="nsew",padx=(10,5),pady=(0,10))
        self.number_on_team_frame.columnconfigure((0,1,2,3,4),weight=1)
        self.number_on_team_frame.rowconfigure((0,1,2,3,4),weight=1)
        self.number_on_team_title=ctk.CTkLabel(self.number_on_team_frame,text="Team Members", font=medium_font)
        self.number_on_team_title.grid(row=0,column=0,columnspan=5,sticky="ew",padx=10,pady=(10,0))
        self.number_on_team_slider=ctk.CTkSlider(self.number_on_team_frame, from_=2, to=16, number_of_steps=15, variable=self.controller.number_on_team, command=self.number_on_team_update)
        self.number_on_team_slider.set(2)
        self.number_on_team_slider.grid(row=1, rowspan=2,column=0,columnspan=4,sticky="ew",padx=(10,0))
        self.number_on_team_slider_label=ctk.CTkLabel(self.number_on_team_frame,text="2 per Team", width=110)
        self.number_on_team_slider_label.grid(row=1, rowspan=2,column=4,padx=(0,10),sticky="nsew")
        self.custom_number_on_team_checkbox=ctk.CTkCheckBox(self.number_on_team_frame,text="Custom by Team", command=self.team_number,  variable=self.controller.custom_or_uniform)
        self.custom_number_on_team_checkbox.grid(row=3, rowspan=2,column=0,columnspan=5,sticky="w",padx=10,pady=(0,5))


        self.custom_team_entry_frame=ctk.CTkFrame(self.top_team_frame, border_width=2, border_color="#4133AB")
        self.custom_team_entry_frame.grid(row=0,rowspan=2,column=1,sticky="nsew",padx=(5,10),pady=10)
        self.custom_team_entry_frame.columnconfigure((0,1),weight=1)
        self.custom_team_entry_frame.rowconfigure((0,1,2),weight=1)
        self.custom_team_label=ctk.CTkLabel(self.custom_team_entry_frame,text="Team Captains", font=medium_font)
        self.custom_team_label.grid(row=0,column=0,columnspan=2,padx=10,pady=(5,0))

        self.custom_team_name_frame=ctk.CTkFrame(self.custom_team_entry_frame, fg_color="transparent")
        self.custom_team_name_frame.columnconfigure((0,1),weight=1)
        self.custom_team_name_frame.rowconfigure(0,weight=1)
        self.custom_team_name_frame.grid(row=1,column=0,rowspan=2,sticky="nsew",padx=2,pady=(0,5))
        self.custom_name_entry=ctk.CTkEntry(self.custom_team_name_frame,placeholder_text="Enter Name")
        self.custom_name_entry.grid(row=0,column=0,sticky="nsew",padx=(10,5),pady=10)
        self.custom_name_entry.bind("<Return>", self.team_captain_entry) 
        self.custom_name_removal=ctk.CTkEntry(self.custom_team_name_frame,placeholder_text="Remove Name")
        self.custom_name_removal.grid(row=0,column=1,sticky="nsew",padx=(5,10),pady=10)
        self.custom_name_removal.bind("<Return>", self.team_captain_removal) 

        self.reset_team_settings=ctk.CTkButton(self.top_team_frame, fg_color="#AB4133", text="Reset Team Settings", command=self.reset_team_settings_func, font=default_font)
        self.reset_team_settings.grid(row=2,column=1, sticky="nsew", padx=(5,10), pady=(5,10))
        #endregion


        #region bottom team frame
        self.bottom_team_frame=ctk.CTkScrollableFrame(self, border_width=2, border_color="#4133AB", fg_color="transparent")
        self.bottom_team_frame.columnconfigure(0,weight=1)
        self.bottom_team_frame.rowconfigure(list(range(32)),weight=1)
        self.bottom_team_frame.grid(row=2,column=0,columnspan=2,sticky="nsew",padx=10,pady=(5,10))

        #variable to track how many teams are currently loaded
        self.current_number_of_teams=0
        #create a list to store team names
        self.team_name_list=[None]*32
        for i in range(32):
            self.team_name_list[i]=f"Team {i+1}"
        #create a list to store the created teams
        self.team=[None]*32
        #endregion

        self.load_teams()

#region methods

    def load_teams(self, value=None):
        number_of_teams = int(float(value)) if value is not None else self.controller.number_of_teams.get()
        self.teams_slider_label.configure(text=f"{number_of_teams} Teams")

        if number_of_teams > self.current_number_of_teams:
            for team_number in range(self.current_number_of_teams + 1, number_of_teams + 1):
                team_index = team_number - 1
                self.team[team_index] = Team(parent=self.bottom_team_frame, controller=self.controller, team_number=team_number, border_width=2, border_color="#4133AB")
                self.team[team_index].grid(column=0, row=team_index, sticky="ew", padx=10, pady=5)
        elif number_of_teams < self.current_number_of_teams:
            for team_number in range(self.current_number_of_teams, number_of_teams, -1):
                team = self.team[team_number - 1]
                if team is not None:
                    team.destroy()
                    removed_members = self.controller.team_members_list[team_number - 1]
                    for name in removed_members:
                        if name in self.controller.static_team_members_list:
                            self.controller.static_team_members_list.remove(name)
                        if name in self.controller.team_captains_list:
                            self.controller.team_captains_list.remove(name)

                    self.team[team_number - 1] = None
                    self.controller.team_members_list[team_number-1]=[]
        self.current_number_of_teams = number_of_teams
        if self.controller.custom_or_uniform.get() == 0:
            self.number_on_team_update(self.controller.number_on_team.get(), number_of_teams)

    def reset_team_settings_func(self):
        #first deal with controller variables
        self.controller.team_names=[]
        self.controller.number_of_teams.set(4)
        self.teams_slider.set(4)
        self.number_on_team_slider.set(2)
        self.controller.number_on_team.set(2)
        self.controller.custom_or_uniform.set(0)
        self.controller.number_on_team_list=[2]*32
        self.controller.team_members_list=[[] for _ in range(32)]
        self.controller.static_team_members_list=[]
        self.controller.team_captains_list=[]

        #clear any currently displayed team member content before rebuilding the frame
        for team in self.team[:self.current_number_of_teams]:
            if team is not None:
                team.destroy()
        self.team=[None]*32

        self.current_number_of_teams=0
        self.load_teams()

        #deal with team captains


    def team_number(self):
        if self.controller.custom_or_uniform.get() == 1:
            for i in range(self.current_number_of_teams):
                self.team[i].custom_team_number_menu.configure(state="normal")
        else:
            for i in range(self.current_number_of_teams):
                self.team[i].custom_team_number_menu.configure(state="normal")
                self.team[i].custom_team_number_menu.set(str(self.controller.number_on_team.get()))
                self.controller.number_on_team_list[i] = self.controller.number_on_team.get()
                self.team[i].custom_team_number_menu.configure(state="disabled")

    #number on team slider command
    def number_on_team_update(self, value, number_of_teams=None):
    #function for number on team slider to update the label and the controller variables to the new slider value
        self.number_on_team_slider_label.configure(text=f"{int(float(value))} per Team")
        if self.controller.custom_or_uniform.get()==0:
            team_count = self.current_number_of_teams if number_of_teams is None else number_of_teams #if number of teams exists, team count is that, otherwise is the controller variable
            for i in range(team_count):
                number_on_team = int(float(value))
                self.team[i].custom_team_number_menu.set(str(number_on_team))
                self.controller.number_on_team_list[i] = number_on_team

    def team_captain_entry(self, event=None):
        name=self.custom_name_entry.get().strip()
        if utility.is_valid_name(name)==False:
            return
        #create a list of all the names already in a team to ensure no duplicates occur
        all_team_members=[]
        for team in self.controller.team_members_list:
            all_team_members.extend(team)
        #check that the entered text has proper text, and that it isn't already on a team
        if name and name not in all_team_members:
            #create a list of the indexes of teams which have no team captain and are not full
            index_list=[]
            for index in range(self.controller.number_of_teams.get()):
                #if there is space in the team and there isn't already a team captain in the team
                if len(self.controller.team_members_list[index])<self.controller.number_on_team_list[index] and all(name not in self.controller.team_captains_list for name in self.controller.team_members_list[index]):
                    #add the index of teams without a team captain to the index list
                    index_list.append(index)
                else: pass
            #if there is some team without a team captain, randomly add one
            if len(index_list)!=0:
                random_index=random.choice(index_list)
                #if there aren't any slots left, do nothing
                if name not in self.controller.name_list and not self.controller.numerical_list:
                    self.custom_name_entry.delete(0,"end")
                    return
                self.controller.team_members_list[random_index].append(name)
                #configure the internal team variables and widgets
                self.team[random_index].team_members.configure(state="normal")
                try:
                    self.team[random_index].team_members.insert(f"{self.team[random_index].team_member_number_list[0]+1}.0", name)
                    self.team[random_index].team_member_list[self.team[random_index].team_member_number_list[0]] = name
                    self.team[random_index].team_member_number_list.pop(0)
                    self.controller.static_team_members_list.append(name)
                    self.controller.team_captains_list.append(name)
                finally:
                    self.team[random_index].team_members.configure(state="disabled")
                    self.custom_name_entry.delete(0,"end")
                #add the name to the name list if it has not been already
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
            #if all teams have a captain, do nothing
            else: pass 
            #delete the text in the box
            self.custom_name_entry.delete(0,"end")
        else: pass
        return "break"

    def team_captain_removal(self, event=None):
        name=self.custom_name_removal.get().strip()
        #check the text is valid
        if name:
            #search for the name to be removed
            for index in range(self.controller.number_of_teams.get()):
                self.team[index].team_members.configure(state="normal")
                try:
                    while name in self.controller.team_members_list[index]:
                        name_index = self.team[index].team_member_list.index(name)
                        self.team[index].team_member_list[name_index]=None
                        self.controller.team_members_list[index].remove(name)
                        self.team[index].team_members.delete(f"{name_index+1}.0",f"{name_index+2}.0")
                        self.team[index].team_members.insert("15.0","\n")
                        self.team[index].team_member_number_list.append(name_index)
                        self.team[index].team_member_number_list.sort()
                        if name in self.controller.static_team_members_list:
                            self.controller.static_team_members_list.remove(name)
                        if name in self.controller.team_captains_list:
                            self.controller.team_captains_list.remove(name)
                finally:
                    self.team[index].team_members.configure(state="disabled")
                    self.team[index].custom_removal.delete(0,"end")
                    #the placeholder text is deleted, so readd it (don't know why it was deleted, but must be dealt with)
                    self.team[index].custom_removal.configure(placeholder_text="Remove Name")
                    self.team[index].custom_entry.configure(placeholder_text="Enter Name")
        else: pass
#endregion
