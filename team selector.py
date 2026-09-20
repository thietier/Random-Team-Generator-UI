import os
import sys

if __package__ in (None, ""):
    project_root = os.path.dirname(os.path.abspath(__file__))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

import customtkinter as ctk
from classes import ban_menu_exe as ban_menu
from classes import team_frame_exe as team_frame
from classes import name_frame_exe as name_frame

#the design of the randomisation algorithm with respect to bannings prioritises speed over an ideal solution- let an upper limit on the number of bannings
#be 3-4 per person in general for a group of 30

ctk.set_default_color_theme("dark-blue")
root=ctk.CTk()
root.geometry("1200x600")

root.title("Team Randomiser")
root.state("zoomed")
root.resizable(False,False)
root.grid_columnconfigure((0,1,2,3,4),weight=1)
root.grid_rowconfigure(0,weight=1)

#controller
class debate_pair_randomiser:
    def __init__(self, root):
        #region variables

        #keeps track of which rows in the textbox are unnassigned
        self.numerical_list=list(range(512))
        #keeps track of all entered names-must be the same order as they are in the textbox (list length 512 with None as the values)
        self.name_list=[None]*512
        #keeps track of the number of names entered
        self.name_count=0
        #keeps track of team names
        self.team_names=[]
        #number of teams
        self.number_of_teams=ctk.IntVar(value=4)
        #number of members of teams
        self.number_on_team=ctk.IntVar(value=2)
        #custom or uniform number of team members
        self.custom_or_uniform=ctk.IntVar(value=0)
        #actual number of members of teams
        self.number_on_team_list=[2]*32
        #list of names on each team
        self.team_members_list=[[] for _ in range(32)] #need to use in range as using [[]]*32 will update every sub-list
        #list of immutable team members (could remove this and just derive it when needed, but already built it this way)
        self.static_team_members_list=[]
        #list of team captains (also included in the static team members list)
        self.team_captains_list=[]
        #endregion

        #big font for headings
        heading_font=ctk.CTkFont(size=24)
        default_font=ctk.CTkFont(size=16)

        self.team_options_frame=team_frame.team_options_frame(parent=root, controller=self, border_width=2, border_color="#4133AB")
        name_options_frame=name_frame.name_options_frame(parent=root, controller=self, border_width=2, border_color="#4133AB")


        #region name_box_frame textbox
        self.name_box_frame=ctk.CTkFrame(root, border_width=2, border_color="#4133AB")
        self.name_box_frame.columnconfigure((0,1),weight=1)
        self.name_box_frame.rowconfigure(0,weight=1)
        self.name_box_frame.rowconfigure(1,weight=13)
        self.name_box_frame.grid(row=0,column=4,sticky="nsew",padx=5,pady=5)

        self.name_box_title=ctk.CTkLabel(self.name_box_frame,text="Name List", font=heading_font, border_width=2, border_color="#4133AB", corner_radius=5)
        self.name_box_title.grid(row=0,column=0,sticky="nsew",padx=10,pady=(10,15))

        #textbox to display the names
        self.name_box=ctk.CTkTextbox(self.name_box_frame, font=default_font)
        self.name_box.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=5)
        self.name_box.insert("1.0","\n"*511) #make the textbox have 512 lines
        self.name_box.configure(state="disabled") #make the textbox uneditable

        #display the number of names entered
        self.counter=ctk.CTkLabel(self.name_box_frame,text="Names: 0", font=default_font)   
        self.counter.grid(row=0,column=1,sticky="nsew",padx=10,pady=(10,15))
        #endregion

main_frame=debate_pair_randomiser(root)

root.mainloop()

