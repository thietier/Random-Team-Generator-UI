import os

def banned_pairs_path():
        project_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(project_dir, "banned_pairs.json")

def is_valid_banned_pair(pair):
        if not isinstance(pair, (list, tuple)) or len(pair) != 2: #check if the given pair is a list or tuple of length 2
                return False
        if not all(isinstance(name, str) for name in pair): #check both elements are strings
                return False
        if any(ord(character)<32 or ord(character)==127 #ord relates to the unicode of the characters
                       for name in pair for character in name): #don't allow characters which could break the string
                #quotation marks not covered as json.dump handles them
                return False
        first_name = pair[0].strip() #check if the names are empty
        second_name = pair[1].strip()
        if not first_name or not second_name or first_name == second_name: 
                return False
        return True

def is_valid_name(name):
        if not isinstance(name, str): #check name is a string
                return False
        if any(ord(character)<32 or ord(character)==127 for character in name):
                return False
        return bool(name.strip()) #return true if name isn't empty
