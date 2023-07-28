#Module imports
import time, math, random
import tempstatclass, charclass


#---------Universal functions---------
def validatenumber(playerinput, ranger: int):   #Ranger is the range of the list
    #To test if an input is a number and is within a given range
    try:
        playerinput = int(playerinput)
    except:
        return False #Not an integer input
    else:
        if playerinput > 0 and playerinput <= ranger:
            return True
        return False
    
def targetselect(index: dict, attacker, lineups: list):    #Gives me the targets in the format and the entire lists of characters
    if index["Targets"][0] == "all":
        targets = []
        for x in range(len(lineups[index["Team"]])):   #Appends the number of indexes in ascending order of the targetted team
            targets.append(x) 
    elif index["Targets"][0] == "choose":
        targets = []
        for x in range(index["Targets"][1]):
            target = int(input("Choose target (Index): "))
            targets.append(target)
    elif index["Targets"][0] == "self": #Do "self"
        targets = []
        targets.append(lineups[index["Team"]].index(attacker))   #Locate the performer of the move in the correct lineup
    else:
        targets = index["Targets"]
    return targets



#------------------Skill classes in general----------------------
class skill():
    def __init__(self, activatetext: list,
                       timing: list,
                       valueoutput: dict,  #E.g. Permanant stat changes (usually hp) {"hp": [4,5], "strength":[3,4]}
                       tempoutput: dict,   #The temp stat changes (with a turn counter to see how long it lasts)
                                           #E.g. {"defense": {"values": [-2,0], "turns": 2}}  Which is decrease def by 2 for 2 turns
                       targetindex: list, 
                       statschange: dict = {},
                       costfail = []):

        #These are three synced list   
        self.text = activatetext   #In a list
        self.timing = timing      #In seconds
        self.outputlist = valueoutput      #Scales off strength of the player
        self.tempoutput = tempoutput

        self.statschange = statschange   #Stats that will change when skill is performed (Requirements)
        self.costfail= costfail  #The text to print out when requirements not met

        #Dictionary form 
        #{"Team": 0 or 1, "Targets": []}
        #Team--> 0 Represents player, 1 represents enemy
        #Targets can be ["choose", 2], choose two targets to affect
        #Targets can be ["all"] hit all targets
        #Others: "self", note: "self" cannot go with enemy lineup (1)
        #Can be [0,1] Hits index 0 and 1 of the lineup
        #[0] hits first target in lineup
        self.targetindex = targetindex



    #Implement drain stats upon move use
    def movecost(self, stats: dict = {}, check = True):   #Check = True --> Check move, Check = False --> Deduct stats to use move
        for x in self.statschange.keys():
            if check:   #Check stats are suitable to perform move
                if stats[x] >= self.statschange[x]:
                    pass
                else:
                    return False
                return True
            if not(check):
                if self.statschange[x] < 0:
                    print(f"+{-self.statschange[x]} {x}")
                else:
                    print(f"-{self.statschange[x]} {x}")
                stats[x] -= self.statschange[x]
        return stats

    def activate(self, attacker, lineups):   #Lineups consist of player team and enemy team, attacker is who is performing the move
        totaldmg = 0   #The entire damage
        for x in range(len(self.text)):
            print(self.text[x])
            for n in self.outputlist.keys():
                if self.outputlist[n][x] == 0:  #Check if the value of attack here is zero
                    pass   #Dont bother printing out anything
                else:
                    outputvalue = eval(self.outputlist[n][x])  #Evaluate the damage statement
                    print(f"{outputvalue} {n} done to target")
                    totaldmg += outputvalue
            time.sleep(self.timing[x])
        #The actual damage part
        for x in targetselect(self.targetindex, attacker, lineups):
            for n in self.outputlist.keys():
                #obtain the total damage value from the list to affect the targetted attribute
                #Permanent stat changes
                lineups[self.targetindex["Team"]][x].setattribute(totaldmg, n)
            lineups[self.targetindex["Team"]][x].tempstats.addtempattri(self.tempoutput)
            #Add display message
            
        attacker.stats = self.movecost(attacker.stats, False)
        attacker.capstats()

        return
        
