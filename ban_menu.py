import os
import sys

if __package__ in (None, ""):
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

import customtkinter as ctk
import json
from functions import utility

class ban_menu(ctk.CTkToplevel):
        def __init__(self,parent, *args,**kwargs):
                #make the fullscreen window a child of the main window
                self.parent_window = parent.winfo_toplevel()
                super().__init__(self.parent_window,*args,**kwargs)
                self.title("Banned Pairings")
                self.geometry("600x400")
                self.resizable(False,False)

                self.transient(self.parent_window) #set the window to be a child of the main window
                self.lift()
                self.focus_force()

                self.rowconfigure((0,1),weight=1)
                self.rowconfigure(2,weight=3)
                self.columnconfigure((0,1,2,3),weight=1)

                #file path for the json file
                self.pairs_file_path=utility.banned_pairs_path()

                self.add_entry_1=ctk.CTkEntry(self,placeholder_text="First Name to Add")
                self.add_entry_1.bind("<Return>",self.add_entry_1_func)
                self.add_entry_1.grid(row=0,column=0,sticky="nsew",padx=(10,5),pady=5)
                self.add_entry_2=ctk.CTkEntry(self,placeholder_text="Second Name to Add")
                self.add_entry_2.bind("<Return>",self.add)
                self.add_entry_2.grid(row=0,column=1,sticky="nsew",padx=5,pady=5)
                self.add_button=ctk.CTkButton(self,text="Add Pair to List",command=self.add)
                self.add_button.grid(row=0,column=2,sticky="nsew",padx=5,pady=5)

                self.off=ctk.CTkButton(self,text="Off",fg_color="#AB4133", command=self.destroy)
                self.off.grid(row=0,column=3,sticky="nsew",padx=(5,10),pady=5)
                self.reset_button=ctk.CTkButton(self,text="Reset List",command=self.reset, fg_color="#AB4133")
                self.reset_button.grid(row=1,column=3,sticky="nsew",padx=(5,10),pady=5)

                self.remove_entry_1=ctk.CTkEntry(self,placeholder_text="First Name to Remove")
                self.remove_entry_1.bind("<Return>",self.remove_entry_1_func)
                self.remove_entry_1.grid(row=1,column=0,sticky="nsew",padx=(10,5),pady=5)
                self.remove_entry_2=ctk.CTkEntry(self,placeholder_text="Second Name to Remove")
                self.remove_entry_2.bind("<Return>",self.remove)
                self.remove_entry_2.grid(row=1,column=1,sticky="nsew",padx=5,pady=5)
                self.remove_button=ctk.CTkButton(self,text="Remove Pair from List",command=self.remove, fg_color="#4133AB")
                self.remove_button.grid(row=1,column=2,sticky="nsew",padx=5,pady=5)

                self.textbox_container=ctk.CTkTextbox(self,corner_radius=5, border_width=2, border_color="#4133AB")
                self.textbox_container.grid(row=2,column=0,columnspan=4,sticky="nsew",padx=10,pady=(5,10))
                self.textbox_container.configure(state="disabled")
                #place all pre-existing pair entries into the textbox
                self.load_pairs()
                
        def load_pairs(self):
                pairs_path = utility.banned_pairs_path()
                if not os.path.exists(pairs_path):
                        with open(pairs_path, "w", encoding="utf-8") as file:
                                json.dump([], file, indent=4)

                self.textbox_container.configure(state="normal")
                self.textbox_container.delete("0.0","end") #clear the textbox
                index=0
                try:
                        with open(pairs_path,"r",encoding="utf-8") as file:
                                pair_list=json.load(file)
                except (json.JSONDecodeError, OSError): #if the file doesn't exist, pair list is empty
                        pair_list=[]

                valid_pairs = [pair for pair in pair_list if utility.is_valid_banned_pair(pair)] #check the validity of pairs, and remove them if invalid
                if len(valid_pairs) != len(pair_list):
                        with open(pairs_path, "w", encoding="utf-8") as file:
                                json.dump(valid_pairs, file, indent=4)

                for pair in valid_pairs:
                        self.textbox_container.insert(f"{index}.0",f"{pair[0]}, {pair[1]}\n")
                        index += 1
                self.textbox_container.configure(state="disabled")

        def add(self, event=None):
                self.textbox_container.configure(state="normal")
                pair=[self.add_entry_1.get().strip(),self.add_entry_2.get().strip()]
                if pair[0] and pair[1]: #ensure the pair actually has correct entries
                        if utility.is_valid_banned_pair(pair): #if the pair is valid
                                pair = sorted(pair)
                                pairs_path = self.pairs_file_path
                                #utf-8 prevents special character error
                                with open(pairs_path,"r",encoding="utf-8") as file:
                                        pair_list=json.load(file) #retrieve the list of banned pairs
                                #check the pair isn't already in the list
                                if pair in pair_list:
                                        return
                                pair_list.append(pair) #add the new pair
                                valid_pairs = [valid_pair for valid_pair in pair_list if utility.is_valid_banned_pair(valid_pair)]
                                with open(pairs_path,"w",encoding="utf-8") as file: 
                                        json.dump(valid_pairs,file,indent=4) #write the updated list back to the file
                                self.load_pairs() #reload the textbox with the updated list
                        else:
                                pass
                else:
                        pass
                self.textbox_container.configure(state="disabled")

                #remove text from entry boxes
                self.add_entry_1.delete(0,"end")
                self.add_entry_2.delete(0,"end")

        def remove(self, event=None):
                self.textbox_container.configure(state="normal")
                pair=[self.remove_entry_1.get().strip(),self.remove_entry_2.get().strip()]
                if pair[0] and pair[1]:
                        if utility.is_valid_banned_pair(pair): 
                                pair = sorted(pair)
                                pairs_path = self.pairs_file_path
                                with open(pairs_path,"r",encoding="utf-8") as file:
                                        pair_list=json.load(file)
                                while pair in pair_list:
                                        pair_list.remove(pair)
                                valid_pairs = [valid_pair for valid_pair in pair_list if utility.is_valid_banned_pair(valid_pair)]
                                with open(pairs_path,"w",encoding="utf-8") as file:
                                        json.dump(valid_pairs,file,indent=4)
                                self.load_pairs() #reload the textbox with the updated list
                        else:
                                pass
                else:
                        pass
                self.textbox_container.configure(state="disabled")

                #remove text from entry boxes
                self.remove_entry_1.delete(0,"end")
                self.remove_entry_2.delete(0,"end")

        def reset(self):
                self.textbox_container.configure(state="normal")
                with open(self.pairs_file_path,"w",encoding="utf-8") as file:
                        json.dump([],file,indent=4) #write an empty list to the file
                self.load_pairs() #reload the textbox with the updated list
                self.textbox_container.configure(state="disabled")

        def add_entry_1_func(self, event=None):
                self.add_entry_2.focus() #move focus to entry_2

        def remove_entry_1_func(self, event=None):
                self.remove_entry_2.focus() #move focus to entry_2 
