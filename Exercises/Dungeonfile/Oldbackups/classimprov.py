#To build a skill class
#To build a parent class where players and enemies share
#Note: Damage values are raw numbers, so damage must be negative numbers, healing positive
import time, math, random

#------------------Skill classes in general----------------------
class skill():
    def __init__(self, activatetext: list, timing: list
                 , valueoutput: dict,  #E.g. {"hp": [4,5], "strength":[3,4]}
                   targetindex: list, 
                 costs: dict = {}, costfail = []):

        #These are three synced list   
        self.text = activatetext   #In a list
        self.timing = timing      #In seconds
        self.outputlist = valueoutput      #Scales off strength of the player

        self.costs = costs   #The requirements to perform the skill
        self.costfail= costfail  #The text to print out when requirements not met

        #Defaulted to index = [0], affects first character in lineup
        #If index = ["all"], affects every character in lineup
        #If index = ["choose"], let character choose the target
        #If index is [0,1], affects first two characters in lineup
        self.targetindex = targetindex

    def costcheck(self, stats: dict):   
        #To check if the requirements are met to use a skill
        for x in self.costs.keys():
            if stats[x] >= self.costs[x]:
                pass
            else:
                return False
        return True

    #Implement drain stats upon move use
    def costused(self, stats: dict = {}):
        for x in self.costs.keys():
            print(x)
            stats[x] -= self.costs[x]
        return stats

    def activate(self, targetlineup, indextarget: list):   #indextarget are the enemies to affected. E.g. [0,1] is the first two targets in a lineup
        for x in range(len(self.text)):
            print(self.text[x])
            for n in self.outputlist.keys():
                if self.outputlist[n][x] == 0:  #Check if the value of attack here is zero
                    pass   #Dont bother printing out anything
                else:
                    outputvalue = 0 - self.outputlist[n][x]  #To flip the damage sign over
                    #This way damage will look like -5 (Attribute) and healing will be 5 (Attribute2)
                    print(f"{self.outputlist[n][x]} {n}")
            time.sleep(self.timing[x])
        for x in indextarget:
            for n in self.outputlist.keys():
                #obtain the total damage value from the list to affect the targetted attribute
                targetlineup[x].setattribute(sum(self.outputlist[n]), n)  
        return
        

#----------------------------Character Classes------------------------------
    

class character():   #The parent class of every character in the game regardless of a side
    def __init__(self, name, hitpoints, strength, defense):
        #Basic attributes 
        self.name = name
        self.hp = hitpoints
        self.strength = strength
        self.defense = defense    #Reduces damage by 10% every count of defense


        #Capped out attributes (Maxed)
        self.maxhp = hitpoints
        self.defaultstr = strength    #The default strength value for the character
        self.defaultdef = defense   #The default defense value for the character

        #Extra attributes
        self.stuncount = 0

    def death(self):
        print(f"{self.name} died")
        return

    def setattribute(self, value, attribute):   #changes the value of an attribute (hp)
        setattr(self, attribute, getattr(self,attribute) + value)
        if value > 0:
            print(f"{self.name}'s {attribute} : +{value}")
        elif value < 0:
            print(f"{self.name}'s {attribute} : {value}")
        else:
            print(f"{self.name}'s {attribute} receives no change in value")
        print(f"{self.name} {attribute} is now {getattr(self, attribute)}")
        
        #Check for death (Usually only hp)
        if self.hp <= 0:
            self.death()

        return
    
    
        

#-------------------------------Hero class-----------------------
class Warrior(character):
    def __init__(self, name, hitpoints, strength, defense, stamina, rage):
        super().__init__(name, hitpoints, strength,defense)
        #Statistics
        self.stats = {"stamina" : stamina, "rage" : rage}
        #Skills
        self.basic = skill( [f"{self.name} USES blade", f"pokes the enemy" , "super not effective"],    
                            [0.3, 0.4, 0.3],                                                           
                            {"hp":[0, -math.floor(self.strength* (self.stats["rage"]*0.1 + 1)),0]},
                            [0])                
        self.heavy = skill( [f"{self.name} spins in a circle", f"the blade smacks someone on accident"],
                            [0.4, 0.3],
                            {"hp":[0, -math.floor(self.strength*1.5 * (self.stats["rage"] *0.1 + 1))]},
                            [0],
                            {"stamina": 4},
                            [f"Too much takoyaki to perform this move, needs 4 stamina"])
        #Moveset of skills
        self.attacklist = [self.basic, self.heavy]
        self.displayattacks = ["1. Poke", "2.Spinning Wrath"]
        


a = Warrior("bob", 20, 4, 0, 5, 3)
b = Warrior("Hames", 20, 3, 0, 10,4)
c = Warrior("Chadwin",20, 3, 0, 10,5)
d = Warrior("John", 15, 2, 0 , 5, 4)
player = [a,c]
enemy = [b,d]
while len(player) > 0 and len(enemy) > 0:
    for x in player:
        print(x.displayattacks)
        attackchoice = int(input(f"Pick an attack from 1 to {len(x.attacklist)}: "))
        time.sleep(0.4)
        if x.attacklist[attackchoice-1].costcheck(x.stats):
            #The idea of attack: pick an attack the attacklist through index, activate, fill in parameters
            x.attacklist[attackchoice - 1].activate(enemy, x.attacklist[attackchoice - 1].targetindex)
        time.sleep(1)
        for j in enemy:
            if j.hp <= 0:
                enemy.remove(j)
    for n in enemy:
        time.sleep(0.4)
        attackchoice = random.randint(0,1)
        n.attacklist[attackchoice].activate(player, n.attacklist[attackchoice].targetindex)
        time.sleep(1)
        for j in player:
            if j.hp <= 0:
                player.remove(j)
        



