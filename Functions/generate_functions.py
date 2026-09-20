import os
import sys
import random

if __package__ in (None, ""):
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

from functions import utility


def greedy_initialisation(ban_pair_list, name_list, team_members_list, number_of_teams, number_on_team):
    "add names in banned pairings to the list to make a starting point for the minimum conflicts algorithm. returns a list of lists of names in a"
    "somewhat optimised order."

    #create a list of names (which appear in the main list) and a list of numbers to show how many times they are paired up in the ban menu
    ban_name_list=[]
    numerical_list=[]
    #make a deep copy of team_members_list to modify and return
    modified_team_members_list=[item.copy() for item in team_members_list]
    # Track full teams so placement does not add more members to them.
    full_teams_list=[]

    for pair in ban_pair_list:
        if not utility.is_valid_banned_pair(pair):
            continue
        for i in range(2):
            name = str(pair[i]).strip()
            #if the name already appears in the list and main name list , add 1 to the same index of the numerical list
            if name in ban_name_list and name in name_list:
                index=ban_name_list.index(name)
                numerical_list[index]+=1
            if name not in ban_name_list and name in name_list:
                ban_name_list.append(name)
                numerical_list.append(1)
            else: pass

    #clean the list for duplicate pairs
    for pair in ban_pair_list:
        while ban_pair_list.count(pair)>1:
            ban_pair_list.remove(pair)

    #add the names in a banned pairing to a team randomly, starting with the ones with the most pairings in the list. this may not always result in a legal 
    #configuration, but will act as an optimised starting point for the next algorithm.
    for i in range(len(ban_name_list)):
        index = numerical_list.index(max(numerical_list))
        name=ban_name_list[index]
        #generate a list of the teams with the total number of bannings
        team_bannings=[0 for _ in range(number_of_teams)]
        #go through each team in turn and total up how many banned pairings exist between the name and all members of each team
        for num in range(number_of_teams):
            bannings=0
            for member in modified_team_members_list[num]:
                pair=[f"{name}", member]
                pair.sort()
                if pair in ban_pair_list:
                    bannings+=1
            team_bannings[num]=bannings
        # Keep counts before the indexed search marks entries as None.
        original_team_bannings=team_bannings.copy()
        for num in range(number_of_teams):
            if len(modified_team_members_list[num]) >= number_on_team[num]:
                # Avoid duplicate indexes as this scan runs for every name.
                if num not in full_teams_list:
                    full_teams_list.append(num)
        # Stop placement but continue to the display section.
        if len(full_teams_list)==number_of_teams:
            break
        #add the name to a random team with the joint lowest number of pairings
        team_num_list=[]
        #+1 so as to not exclude the maximum
        for num in range(max(team_bannings)+1):
            #if there is a team with that many pairings and not all teams with that many pairings are full
            if num in team_bannings and not all(team_bannings.index(num) in full_teams_list for num in team_bannings):
                while num in team_bannings:
                    team_num_list.append(team_bannings.index(num))
                    team_bannings[team_bannings.index(num)]=None
            #remove all full teams from team_bannings
            for team in full_teams_list:
                if team in team_num_list:
                    team_num_list.remove(team)
            if team_num_list:
                break #only use the lowest possible number, so finish this loop as soon as one is found

        #fall back to the best available team if the indexed search found none.
        if not team_num_list:
            available_teams = [team for team in range(number_of_teams)
            if team not in full_teams_list]
            if not available_teams:
                break
            lowest_bannings = min(original_team_bannings[team] for team in available_teams)
            team_num_list = [team for team in available_teams
            if original_team_bannings[team] == lowest_bannings]
        selected_team=random.choice(team_num_list)
        
        #remove the name from the lists so it cannot be placed again
        ban_name_list.pop(index)
        numerical_list.pop(index)
        name_list.remove(name)
        #add to the team
        modified_team_members_list[selected_team].append(name)
        #if this makes the team full, add it to the list of full teams
        if len(modified_team_members_list[selected_team])==number_on_team[selected_team] and selected_team not in full_teams_list:
            full_teams_list.append(selected_team)
            full_teams_list.sort()

    return modified_team_members_list, name_list

def min_conflicts_alg(modified_team_members_list, static_team_members_list, number_of_teams, number_on_team, ban_pair_list):
    "apply the minimum conflicts algorithm to the input team members list and return a sorted version of that,"
    "and the number of conflicts in the list"
    #have the algorithm go through a variable number of steps, equal to the number of conflicts. as each step
    #reduces this by at least one, this is always an upper bound, and generally a good one
    total_conflicts=0
    for team in modified_team_members_list:
        for member in team:
            total_conflicts+=member_conflicts_in_team(member, team, ban_pair_list)/2
    total_conflicts=int(total_conflicts)
    for step in range(total_conflicts):
        conflicting_member_list=conflicting_members(team_members_list=modified_team_members_list, number_of_teams=number_of_teams, ban_pair_list=ban_pair_list)
        #remove team captains and set team members from the list so they cannot be moved
        for member in static_team_members_list:
            if member in conflicting_member_list:
                conflicting_member_list.remove(member)

        if not conflicting_member_list:
            break
        #choose some person currently violating a pairing
        #this is less computationally expensive than checking every possibility,
        #and reduces the chance of getting stuck in a local minimum
        candidate=random.choice(conflicting_member_list)
        #find the team the candidate is currently in
        current_team=None
        for team in modified_team_members_list:
            if candidate in team:
                current_team=modified_team_members_list.index(team)
                break

        if current_team is None:
            break

        #create variables to determine the best action to minimise conflicts
        best_action=None
        #(delta to mean change)
        min_conflict_delta = float("inf")

        for next_team in range(number_of_teams):
            #when the same team is selected, skip the loop
            if next_team == current_team:
                continue

            #evaluate moving the candidate to a team with space
            if len(modified_team_members_list[next_team]) < number_on_team[next_team]:
                old_conflicts=member_conflicts_in_team(candidate, modified_team_members_list[current_team], ban_pair_list)
                new_conflicts=member_conflicts_in_team(candidate, modified_team_members_list[next_team], ban_pair_list)

                move_delta = new_conflicts-old_conflicts
                if move_delta < min_conflict_delta and move_delta<0:
                    min_conflict_delta=move_delta
                    best_action=("Move", next_team)

            #see if swapping the member is best
            for swap_partner in list(modified_team_members_list[next_team]):
                #ensure the swap_partner is not a team captain
                if swap_partner in static_team_members_list:
                    continue

                old_conflicts=(member_conflicts_in_team(candidate, modified_team_members_list[current_team], ban_pair_list)
                +member_conflicts_in_team(swap_partner, modified_team_members_list[next_team], ban_pair_list))

                # Simulate the swap on copied inner lists, leaving real teams unchanged.
                temporary_list=[item.copy() for item in modified_team_members_list]

                temporary_list[current_team].remove(candidate)
                temporary_list[next_team].remove(swap_partner)
                new_conflicts=(member_conflicts_in_team(candidate, temporary_list[next_team], ban_pair_list)
                +member_conflicts_in_team(swap_partner, temporary_list[current_team], ban_pair_list))

                swap_delta=new_conflicts-old_conflicts
                if swap_delta < min_conflict_delta and swap_delta < 0:
                    min_conflict_delta=swap_delta
                    best_action=("Swap", next_team, swap_partner)

        #carry out the best action
        if best_action is None:
            break

        if best_action[0]=="Move":
            target_team=best_action[1]
            modified_team_members_list[current_team].remove(candidate)
            modified_team_members_list[target_team].append(candidate)
        elif best_action[0]=="Swap":
            target_team, swap_partner = best_action[1], best_action[2]
            modified_team_members_list[current_team].remove(candidate)
            modified_team_members_list[target_team].remove(swap_partner)
            modified_team_members_list[current_team].append(swap_partner)
            modified_team_members_list[target_team].append(candidate)

    #calculate the number of conflicts in the list
    total_conflicts=0
    for team in modified_team_members_list:
        for member in team:
            total_conflicts+=member_conflicts_in_team(member, team, ban_pair_list)/2
    total_conflicts=int(total_conflicts)

    #return the list and the number of conflicts in the list
    return modified_team_members_list, total_conflicts

def member_conflicts_in_team(m, team, ban_pair_list):
    #how many conflicts a member has with a selected team
    return sum(1 for other_member in team if sorted([m, other_member]) in ban_pair_list)

def conflicting_members(team_members_list, number_of_teams, ban_pair_list):
    #list of conflicting names
    conflicts=[]
    for index in range(number_of_teams):
        #check there are at least two members in the team
        if len(team_members_list[index])>=2:
            for member in team_members_list[index]:
                for other_member in team_members_list[index]:
                    pair=[member, other_member]
                    pair.sort()
                    if pair in ban_pair_list:
                        if member not in conflicts:
                            conflicts.append(member)
                        if other_member not in conflicts:
                            conflicts.append(other_member)
        else: pass
    return conflicts
