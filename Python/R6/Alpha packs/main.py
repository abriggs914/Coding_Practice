import easygui
import csv
from utility import *
from classes import *


rarities_list = ["NO_RARITY", "Common", "Uncommon", "Rare", "Epic", "Legendary"]
# code_list = ["NO_CODE", "UN", "HG", "WP", "WS", "WU", "CH"]
# gun_code_list = ["NO_CODE", "SNP", "DMR", "ASR", "SMG", "LMG", "SHG", "HDG", "MPL"]
code_list = {
    "NO_CODE": "NO_CODE", 
    "UN": "uniform",
    "HG": "headgear",
    "WP": "primary weapon",
    "WS": "secondary weapon",
    "WU": "universal weapon skin",
    "CH": "charm"
    }

gun_code_list = {
    "NO_CODE": "NO_CODE",
    "SNP": "sniper",
    "DMR": "marksman rifle",
    "ASR": "assault rifle",
    "SMG": "sub-machine gun",
    "LMG": "light machine gun",
    "SHG": "shotgun",
    "HDG": "handgun",
    "MPL": "machine pistol",
    "SHD": "riot shield"
    }


def msgbox(msg, title, choices, default_choice, cancel_choice):
    c = easygui.buttonbox(msg=msg, title=title, choices=choices, default_choice=default_choice, cancel_choice=cancel_choice)
    return c


def enterbox(msg, title, default):
    c = easygui.enterbox(msg=msg, title=title, strip=True)
    return c


def ynbox(msg, title, choices, default, cancel):
    c = easygui.ynbox(msg=msg, title=title, choices=choices, default_choice=default, cancel_choice=cancel)
    return c


def integerbox(msg, title, default, lowerbound, upperbound):
    c = easygui.integerbox(msg=msg, title=title, lowerbound=lowerbound, upperbound=upperbound)
    return c

def choicebox(msg, title, choices, preselect):
    c = easygui.choicebox(msg=msg, title=title, choices=choices, preselect=preselect)
    return c

def gather_data():
    msg_rarities = "Select Rarity:"
    title_rarities = "Select Rarity"
    choices_raritites = rarities_list[1:].copy()
    default_choice_rarities = rarities_list[0]
    cancel_choice_rarities = rarities_list[0]
    selection_rarity = msgbox(msg_rarities, title_rarities, choices_raritites, default_choice_rarities, cancel_choice_rarities)
    
    msg_name = "Reward Name:"
    title_name = "Enter Reward Name"
    default_choice_name = "NO_NAME"
    selection_name = enterbox(msg_name, title_name, default_choice_name)
    
    msg_description = "Reward Description:"
    title_description = "Enter Reward Description"
    default_choice_description = "NO_DESCRIPTION"
    selection_description = enterbox(msg_description, title_description, default_choice_description)

    msg_duplicate = "Is this a Duplicate Reward?"
    title_duplicate = "Duplicate Status"
    choices_duplicate = ["Yes", "No"]
    default_choice_duplicate = choices_duplicate[1]
    cancel_choice_duplicate = choices_duplicate[1]
    selection_duplicate = ynbox(msg_duplicate, title_duplicate, choices_duplicate, default_choice_duplicate, cancel_choice_duplicate)

    selection_renown = 0
    msg_renown = "Renown Received for Duplicate Reward:"
    title_renown = "Duplicate Renown Gain"
    default_choice_renown = 0
    lowerbound_renown = 0
    upperbound_renown = 25000
    if selection_duplicate:
        selection_renown = integerbox(msg=msg_renown, title=title_renown, default=default_choice_renown, lowerbound=lowerbound_renown, upperbound=upperbound_renown)
    
    msg_availibility = "Reward Availibility:"
    title_availibility = "Enter Reward Availibility"
    default_choice_availibility = "NO_AVAILIBILITY"
    selection_availibility = enterbox(msg_availibility, title_availibility, default_choice_availibility)
    
    msg_code = "Select Code:"
    title_code = "Select Code"
    choices_code = list(map(str.title, code_list.values()))[1:]
    default_choice_code = list(map(str.title, code_list.values()))[0]
    cancel_choice_code = list(code_list.values())[0]
    selection_code = msgbox(msg_code, title_code, choices_code, default_choice_code, cancel_choice_code).lower()

    operators_list = list(map(str, (attackers.copy() + defenders.copy())))
    operators_list.sort()
    operators_list = ["NO_OPERATOR"] + operators_list
    # selection_operator = operators_list[0]
    # if selection_code in code_list[1:3]:
    #     msg_operator = "Select All Operators that Have Access to this Reward"
    #     title_operator = "Operators"
    #     choices_operator = operators_list.copy()
    #     choices_operator.sort()
    #     choices_operator = ["NO_OPERATOR"] + choices_operator
    #     preselect_operator = 0
    #     selection_operator = choicebox(msg_operator, title_operator, choices_operator, preselect_operator)

    guns_list = attackers.copy() + defenders.copy()
    selection_operator = operators_list[0]
    selection_gun = "NO_WEAPON"
    if selection_code in list(code_list.values())[1:3]:
        msg_operator = "Select All Operators that Have Access to this Reward"
        title_operator = "Operators"
        choices_operator = list(map(str, operators_list.copy()))
        choices_operator.sort()
        choices_operator = operators_list
        preselect_operator = 0
        selection_operator = choicebox(msg_operator, title_operator, choices_operator, preselect_operator)
    elif selection_code in list(code_list.values())[3:-2]:
        msg_gun = "Select a Weapon that Has Access to this Reward"
        title_gun = "Weapons"
        choices_gun = list(map(str, weapons["Primary"] + weapons["Secondary"]))
        if len(choices_gun) > 1:
            choices_gun.sort()
            choices_gun = ["NEW_WEAPON", "UNIVERSAL"] + choices_gun
            preselect_gun = 0
            selection_gun = choicebox(msg_gun, title_gun, choices_gun, preselect_gun)
        else:
            selection_gun = "NEW_WEAPON"
        if selection_gun == "NEW_WEAPON":
            msg_new_weapon_name = "Enter New Weapon's Name"
            msg_new_weapon_pri_sec = "Is the New Weapon a Primary or Secondary Weapon?"
            msg_new_weapon_code = "What is this Weapon's Class?"
            title_new_weapon_name = "New Weapon"
            title_new_weapon_pri_sec = "New Weapon"
            title_new_weapon_code = "New Weapon"
            choices_new_weapon_pri_sec = ["Primary", "Secondary"]
            choices_new_weapon_code = list(map(str.title, gun_code_list.values()))[1:]
            default_new_weapon_pri_sec = choices_new_weapon_pri_sec[0]
            default_choice_new_weapon_name = "NO_WEAPON"
            default_choice_new_weapon_code = list(gun_code_list.values())[0]
            cancel_new_weapon_pri_sec = choices_new_weapon_pri_sec[0]
            cancel_new_weapon_code = list(gun_code_list.values())[0]
            selection_new_weapon_pri_sec = ynbox(msg_new_weapon_pri_sec, title_new_weapon_pri_sec, choices_new_weapon_pri_sec, default_new_weapon_pri_sec, cancel_new_weapon_pri_sec)
            selection_new_weapon_name = enterbox(msg_new_weapon_name, title_new_weapon_name, default_choice_new_weapon_name)
            selection_new_weapon_code = msgbox(msg_new_weapon_code, title_new_weapon_code, choices_new_weapon_code, default_choice_new_weapon_code, cancel_new_weapon_code).lower()
            
            selection_new_weapon_code = {v.lower() : k for k, v in gun_code_list.items()}[selection_new_weapon_code]

            selection_gun = add_weapon(selection_new_weapon_name, selection_new_weapon_pri_sec, selection_new_weapon_code)
        else:
            selection_gun = lookup_weapon(selection_gun)
    elif selection_code in list(code_list.values())[-2:]:
        selection_gun = "UNIVERSAL"
    
    selection_code = {v.lower() : k for k, v in code_list.items()}[selection_code]
    return selection_rarity, selection_name, selection_description, selection_duplicate, selection_renown, selection_availibility, selection_code, selection_operator, selection_gun
    

with open("results.csv", "a") as results:
    loop = True
    while loop:
        loop = ynbox(msg="What would you like to do?", title="Continue?", choices=["Create Another Entry", "Quit"], default="Quit", cancel="Quit")
        if not loop:
            continue
        data = gather_data()
        print(data)
        results.write("\n" + " ; ".join(list(map(str, data))))

print("Input done. Beginning analysis...")

with open("results.csv", "r") as resf:
    res_dict = csv.DictReader(resf, delimiter=";")
    # lst = [{k.strip() : v.strip() for k, v in dct.items()} for dct in res_dict]


    duplicates = []
    rarities = {k: [] for k in rarities_list}
    codes = {k: [] for k in code_list}
    rewards = []
    for entry in res_dict:
        reward = Reward(*[e.strip() for e in entry.values()])
        rewards.append(reward)
        if reward.duplicate:
            duplicates.append(reward)
        rarities[reward.rarity].append(reward)
        codes[reward.code].append(reward)
        # print(reward)

    renown_gained = sum([r.renown_gain for r in duplicates])

    t = len(rewards)
    print("Rarities classificaton, " + str(t) + " rewards")
    for rarity, rarity_rewards in rarities.items():
        n = len(rarity_rewards)
        p = n / t
        print("#######################################################################################\n" + rarity + ", " + str(n) + " / " + str(t) + " rewards, " + percent(p) + "\n")
        for r in rarity_rewards:
            print(r)
        print("\n#######################################################################################")
    
    print("Codes classificaton, " + str(t) + " rewards")
    for code, code_rewards in codes.items():
        n = len(code_rewards)
        p = n / t
        print("#######################################################################################\n" + code + ", " + str(n) + " / " + str(t) + " rewards, " + percent(p) + "\n")
        for c in code_rewards:
            print(c)
        print("\n#######################################################################################")
    

    d = len(duplicates)
    p = d / t
    print("\n\nDuplicates classificaton, " + str(d) + " / " + str(t) + " rewards, " + percent(p))
    print("#######################################################################################\n")
    for dup in duplicates:
        print(dup)
    print("\n#######################################################################################")

    print("return on renown: " + str(renown_gained))
    