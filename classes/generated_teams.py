import os
import sys

if __package__ in (None, ""):
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

import customtkinter as ctk
import json
import random
from tkinter import messagebox

from functions import utility_exe as utility
from functions import generate_functions_exe as generate_functions


class generated_teams(ctk.CTkToplevel):
    def __init__(self, parent, controller, *args, fg_color = None, **kwargs):
        super().__init__(parent, *args, fg_color=fg_color, **kwargs)
        self.controller = controller
        self.parent_window = parent.winfo_toplevel()
        self.title("Generated Teams")
        self.geometry("800x600")
        self.resizable(False,False)

        self.transient(self.parent_window) #set the window to be a child of the main window
        self.lift()
        self.focus_force()

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.teams_container=ctk.CTkScrollableFrame(self, border_width=2, border_color="#4133AB", fg_color="transparent")
        self.teams_container.grid(row=0, column=0, sticky="nsew")

        self.teams_container.columnconfigure(0, weight=1)

        number_of_teams=self.controller.number_of_teams.get()
        for team_number in range(number_of_teams):
            self.teams_container.rowconfigure(team_number, weight=1)

        # Work on independent lists so generation does not alter the controller state.
        name_list=[name for name in self.controller.name_list if name is not None and name not in self.controller.static_team_members_list]
        self.team_members_list=[item.copy() for item in self.controller.team_members_list]
        number_on_team=self.controller.number_on_team_list.copy()
        static_team_members_list=self.controller.static_team_members_list.copy()

        #resolve the data file from this module's location, not the launch directory.
        pairs_path = utility.banned_pairs_path()
        if not os.path.exists(pairs_path):
            with open(pairs_path, "w", encoding="utf-8") as file:
                json.dump([], file, indent=4)

        try:
            with open(pairs_path,"r",encoding="utf-8") as file:
                self.ban_pair_list=json.load(file)
            if not isinstance(self.ban_pair_list, list):
                self.ban_pair_list = []
            self.ban_pair_list = [pair for pair in self.ban_pair_list if utility.is_valid_banned_pair(pair)]
        except (json.JSONDecodeError, OSError):
            self.ban_pair_list = []
            messagebox.showerror("Banned Pairs Error","Banned pairs could not be loaded. Proceeding without them.",parent=self)

        #set up a loop with starting points and finding the best one, terminating if a conflict-less solution is found
        best_minimum=None
        number_of_conflicts=float("inf")

        #let the loop have 10 restarts to find the best minimum. if a 0-minimum is found, it will instantly be selected
        for num in range(10):
            restart_name_list=name_list.copy()
            modified_team_members_list, restart_name_list= generate_functions.greedy_initialisation(self.ban_pair_list, restart_name_list, self.team_members_list, number_of_teams, number_on_team)
            modified_team_members_list, conflicts_temporary=generate_functions.min_conflicts_alg(modified_team_members_list, static_team_members_list, number_of_teams, number_on_team, self.ban_pair_list)
            if float(conflicts_temporary)<number_of_conflicts:
                best_minimum=modified_team_members_list
                number_of_conflicts=float(conflicts_temporary)
                remaining_name_list=restart_name_list
            if number_of_conflicts==0:
                break
        self.team_members_list=best_minimum

        #region add names
        #add names without any bannings
        # Rebuild this after moves and swaps because team capacity may have changed.
        full_teams_list = [team for team in range(number_of_teams)
            if len(self.team_members_list[team]) >= number_on_team[team]]
        for name in remaining_name_list:
            #create a list of not full teams
            candidate_teams=list(range(number_of_teams))
            for team in full_teams_list:
                candidate_teams.remove(team)
            #finish adding names if all teams are full
            if len(candidate_teams)==0:
                break

            team=random.choice(candidate_teams)

            self.team_members_list[team].append(name)
            # Record newly filled teams so later names cannot be placed there.
            if len(self.team_members_list[team]) >= number_on_team[team] and team not in full_teams_list:
                full_teams_list.append(team)
        #endregion

        #region teams
        #add the teams last so the member names are correctly put into the text box
        self.display_team=[None]*32
        for team_number in range(number_of_teams):
            team_name = controller.team_options_frame.team[team_number].team_name.get()
            if utility.is_valid_name(team_name)==False:
                team_name = f"Team {team_number + 1}"
            #display generated assignments
            self.display_team[team_number]=team_display(self.teams_container, team_members_list=self.team_members_list, team_number=team_number, team_name=team_name)
            self.display_team[team_number].grid(column=0, row=team_number, sticky="ew", padx=10, pady=5)

        #let the user know if there are unassigned names (if the space on teams is less than number of names). cant use len for name_list as it contains None entries
        unnassigned_members=sum(self.controller.number_on_team_list[index] for index in range(self.controller.number_of_teams.get()))-sum(name is not None for name in self.controller.name_list)
        if unnassigned_members<0:
            #keeps the message at the top until it is dismisses
            messagebox.showwarning("Unassigned Names",f"There are {-unnassigned_members} unassigned names due to insufficient team space.",parent=self,)

class team_display(ctk.CTkFrame):
    def __init__(self, parent, team_members_list, team_number, team_name, fg_color="transparent", border_width=2, border_color="#4133AB", height=80):
        super().__init__(parent , fg_color=fg_color, border_width=border_width, border_color=border_color, height=height)

        self.columnconfigure((0,1), weight=1)
        self.rowconfigure(0, weight=1)

        big_font=ctk.CTkFont(size=30)
        name_font=ctk.CTkFont(size=20)

        self.team_name_label=ctk.CTkLabel(self, text=f"{team_name}", border_width=2, border_color="#4133AB", font=big_font)
        self.team_name_label.grid(row=0, column=0, padx=(10,5), pady=10, sticky="nsew")

        member_names = team_members_list[team_number]
        self.member_names_box=ctk.CTkTextbox(self, border_width=2, border_color="#4133AB", font=name_font)
        self.member_names_box.grid(row=0, column=1, padx=(5,10), pady=10, sticky="nsew")
        if member_names:
            self.member_names_box.insert("1.0", "\n".join(member_names))
        self.member_names_box.configure(state="disabled")
