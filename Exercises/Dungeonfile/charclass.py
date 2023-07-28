import time, math, random
import skillclass
import tempstatclass

#---------------------------Universal functions------------------------------
def damagecalc(char, strengthscale: int, rage: bool):
    if rage:
        return f"-math.floor(attacker.getattribute('strength') * {strengthscale} * (attacker.stats['rage']*0.1 + 1))"
    else:
        return f"-math.floor(attacker.getattribute('strength') * {strengthscale})"
    
def targetsystem(team, targetting):   #targetting will either be 0 (Enemyteam) or 1(OwnTeam)
    #Determine what team the character is on, adjust the targetting system
    if team == "Enemy":
        #Flip the team target index
        if targetting == 0:
            targetting = 1
        else:
            targetting = 0
    return targetting
    
#----------------------------Character Classes------------------------------
    

class character():   #The parent class of every character in the game regardless of a side
    def __init__(self, team, name, hitpoints, strength, defense):
        #Team
        self.team = team  #Either "Enemy" / "Player"

        #Basic attributes 
        self.name = name
        self.hp = hitpoints
        self.strength = strength
        self.defense = defense    #Reduces damage by 10% every count of defense
        self.stats = {}


        #Capped out attributes (Maxed)
        self.maxstats = {}
        self.maxhp = hitpoints

        #Extra attributes
        self.stunned = 0   #As long as stun is not 0, the character is stunned

        #Tempstats -- Important for buff/debuffs
        self.tempstats = tempstatclass.tempstat()

    def death(self):
        print(f"<>{self.name} died<>")
        return

    def setattribute(self, value, attribute):   #changes the value of an attribute (hp)
        #If attribute is health, apply the use of defense stats (One def = 10% damage reduction)
        if attribute == "hp":
            if value < 0:   #If value is an attack (Else dont apply defense or no healing rip)
                value -= value*(self.getattribute('defense') / 10)
                if value > 0:    #Prevent attacks from becoming healing
                    value = 0 
    
        setattr(self, attribute, getattr(self,attribute) + round(value))
        self.caphealth()
        #Insert max attribute here???
        if value > 0:
            print(f"<>{self.name}'s {attribute} : Increased by +{value}<>")
        elif value < 0:
            print(f"<>{self.name}'s {attribute} : Decreased by {value}<>")
        else:
            print(f"<>{self.name}'s {attribute} receives no change in value<>")
        
        #Check for death (Usually only hp)
        if self.hp <= 0:
            self.death()
        return
    
    def getattribute(self, attriname: str):   #Get the certain value of attribute WITH its temp stats
        totaltemp = 0
        try:
            for i in self.tempstats.tempattri[attriname]:
                totaltemp += i[0]
            return getattr(self, attriname) + totaltemp
        except:
            return getattr(self, attriname)

    
    def caphealth(self):
        #If health exceeds the  max or is less than zero, set it to the boundary value
        if self.hp > self.maxhp:
            self.hp = self.maxhp
        elif self.hp < 0:
            self.hp = 0
        return
    
    def capstats(self): 
        #If stats exceeds max(If it has one) or is less than zero, set to boundary value
        for x in self.stats.keys():  #Obtain all the keys of the stats
            try:
                self.maxstats[x]
            except:
                pass
            else:
                if self.stats[x] > self.maxstats[x]:
                    self.stats[x] = self.maxstats[x]
                elif self.stats[x] < 0:
                    self.stats[x] = 0
        return       
        
    
    
        

#-------------------------------Hero class-----------------------
class Warrior(character):
    def __init__(self, team, name, hitpoints, strength, defense, stamina, rage):
        super().__init__(team, name, hitpoints, strength,defense)
        #Statistics 
        self.stats = {"stamina" : stamina / 2, "rage" : rage}     #Starts with half stamina
        self.maxstats = {"stamina" : stamina}
        

        #Skills
        self.basic = skillclass.skill( [f"{self.name} USES blade", f"pokes the enemy" , "super not effective"],              
                            [0.3, 0.4, 0.3],                                                           
                            {"hp":[0, damagecalc(self,1,True),0]},
                            {},
                            {"Team": targetsystem(self.team, 1), "Targets": [0]},
                            {"stamina": 1, "rage": -1},  #Costs 1 stamina to perform, Gives 1 rage if performed
                            [f"Relax, why keep fighting when you can relax... Needs 1 stamina"])              
        self.heavy = skillclass.skill( [f"{self.name} spins in a circle", f"the blade smacks someone on accident"],
                            [0.4, 0.3],
                            {"hp":[0, damagecalc(self,1.5,True)]},
                            {},
                            {"Team": targetsystem(self.team, 1), "Targets": [0]},
                            {"stamina": 4, "rage": -3},
                            [f"Too much takoyaki to perform this move, needs 4 stamina"])
        self.ulti = skillclass.skill( [f"{self.name} unleashes the blade", "RAWRRR", "slashing down on the opponent", "you hear a combo yes you hear it", "slash", "slash", "slash","ok im done"],
                                     [0.6, 0.4, 0.1, 0.7, 0.1, 0.1, 0.1, 0.5],
                                     {"hp": [0, 0, damagecalc(self,2.0,True), 0,damagecalc(self,1,True),damagecalc(self,1,True),damagecalc(self,1,True),0 ]},
                                     {},
                                     {"Team": targetsystem(self.team, 1), "Targets": [0]},
                                     {"stamina": 5, "rage": 9},
                                     [f"Bro really tried to ult, needs 9 Rage, needs 5 stamina"])
        self.block = skillclass.skill( [f"{self.name} put arm in face", "Protection 100"],
                                      [0.4,0.4],
                                      {},
                                      {"defense": {"values": [3,0],"turns": 1}},
                                      {"Team": targetsystem(self.team, 0), "Targets": ["self"]},
                                      {"stamina": -1})
        self.rest = skillclass.skill( [f"{self.name} chooses relaxation yay"],
                                     [1],
                                     {},
                                     {},
                                     {"Team": targetsystem(self.team, 0), "Targets": ["self"]},
                                     {"stamina": -6})

        #Moveset of skills
        self.attacklist = [self.basic, self.heavy, self.ulti, self.block, self.rest]
        self.displayattacks = ["1. Poke", "2.SpinnyDisk", "3. Slashcombo", "4. Block", "5. Rest"]


# testman = Warrior("BobJr", "Player", 30, 5, 0, 10, 4)
# print(testman.getattribute("defense"))
# testman.tempstats.addtempattri({"defense": {"values": [2,3], "turns": 2}})
# print(testman.getattribute("defense") + 4)