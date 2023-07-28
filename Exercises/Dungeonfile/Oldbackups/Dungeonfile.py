#-----------------Module Imports---------------------------
import random
import time
import math
import sys, subprocess

print("Hi welcome to game. You have a team of characters and you fight enemy team with characters. This is a turn-based game ok take turns and fight")

#-----------------------------Player classes--------------------------
class person:
    def __init__(self, name, hitpoints, strength, stamina, defense):
        self.name = name
        self.hp = hitpoints
        self.maxhp = hitpoints
        self.stamina = stamina
        self.maxstamina = stamina + 10
        self.charge = 0     #The stuff needed to perform some special skills
        self.strength = strength
        self.defense = defense   #Reduces damage by certain %, not coded in yet cuz im lazy
        self.stunned = 0   #Every value represents turns character is stunned
        self.moveset = [self.basic]   #Their moves (This is used for inputs later on)
        self.displaymoveset = ["1. Basic"]   #Idk how to display the moveset in a better way to the players
    
    def win(self):    
        if self.hp < self.maxhp / 5:
            print("Close fight!!!")
            return
        print("Easy dubs")
        return

    def lose(self):
        print(f"{self.name} died")
        return
    
    def basic(self, lineup):
        damage = self.strength
        print(f"{self.name} punches {lineup[0].name}")
        self.stamina += 1
        time.sleep(0.5)
        lineup[0].hurt(damage)
        return

    def guard(self):   #To be added cuz uk
        pass

    def hurt(self, damaged):
        self.hp -= damaged
        if self.hp <= 0:
            self.lose()
            return
        print(f"{self.name} got damaged for {damaged}")
        return

class Warrior(person):   #Idea: Strong but not tanky, gets stronger over time if rage is stacked
    def __init__(self, name, hitpoints, strength, stamina, defense, rage):
        super().__init__(name, hitpoints,strength,stamina, defense)
        self.moveset = [self.basic, self.heavy, self.ult]
        self.displaymoveset = ["1. Slash", "2. Heavy slash", "3. Slash combo"]
        #The idea of rage, increases damage by 10%, however damage always rounds down so
        self.rage = rage   #Replaces charge btw

    def basic(self,check, lineup):  
        if check == 1:
            return True
        damage = math.floor(self.strength * (1 + self.rage/10))
        print(f"{self.name} slashes {lineup[0].name}")
        time.sleep(0.2)
        print("+1 Rage, +1 Stamina")
        self.stamina += 1
        self.rage += 1
        lineup[0].hurt(damage)
        return 
        
    def heavy(self,check, lineup):
        if check == 1:
            return True
        fatigue = 1
        if self.stamina < 4:
            print(f"Lethargic, tired, stamina drained, {self.name} weakens in power")
            fatigue = 0.5
        else:
            print("-4 Stamina")
            self.stamina -= 4
        time.sleep(0.3)
        damage = math.floor((self.strength*2 * fatigue) * (1 + self.rage/10))
        if damage < 0:   #Avoid healing your opponents 
            damage = 0
        print("+2 Rage")
        time.sleep(0.4)
        self.rage += 2
        print(f"{self.name} swing your blade at {lineup[0].name}!")
        lineup[0].hurt(damage)
        return

    def ult(self,check, lineup):
        #Any way to organise my text? theres too much going on
        if self.rage < 9:
            print("Inadequate rage. Requires 9 rage")
            return False
        elif check == 1:
            return True
        self.rage -= 9
        print(f"Dashing towards {lineup[0].name}")
        time.sleep(1)
        print(f"{self.name} slash them into the air")
        damage = random.randint(self.strength, self.strength + 2)
        print(f"-{damage}")
        time.sleep(0.7)
        print("Jumping into the air above them")
        time.sleep(0.4)
        print(f"{self.name} holding their blade over their head and...")
        time.sleep(1)
        print("!!!BOOOMM!!!")
        time.sleep(1)
        print(f"{self.name} smashed them into the ground")
        tempdam = random.randint(self.strength*5, self.strength*7)
        print(f"-{tempdam}")
        time.sleep(0.4)
        print("-9 Rage")
        damage += tempdam
        lineup[0].hurt(damage)
        return


        
#----------------------Enemy classes---------------------------- 
class enemy:
    def __init__(self, name, hitpoints, strength):
        self.name = name
        self.hp = hitpoints
        self.strength = strength
        self.stunned = 0
        
    def death(self):
        print(f"{self.name} has fallen")
        return
        
    def hurt(self, damaged):
        self.hp -= damaged
        print(f"{self.name} got hurt for {damaged}")
        time.sleep(0.3)
        if self.hp <= 0:
            self.death()
            return
        print(f"{self.name} left with {self.hp} hp")
        return

class Robber(enemy):
    def __init__(self, name, hitpoints, strength):
        super().__init__(name, hitpoints,strength)
        self.moveset = [self.light, self.heavy, self.area, self.special]
        
    def light(self, lineup):
        damage = random.randint(self.strength, self.strength + 3)
        print(f"{self.name} punches {lineup[0].name}")
        lineup[0].hurt(damage)
        return

    def heavy(self, lineup):
        print(f"{self.name} charges at {lineup[0].name}...")
        time.sleep(0.5)
        print(f"Grabbing {lineup[0].name},")
        time.sleep(0.2)
        print(f"He slams {lineup[0].name} to the ground!")
        damage = random.randint(math.floor(self.strength*1.5), self.strength *3)
        lineup[0].hurt(damage)
        return

    def area(self,lineup):   #Max hit two players
        print(f"{self.name} throws a rock at {lineup[0].name}")
        time.sleep(0.4)
        toattack = 1
        if len(lineup) > 1:
            print(f"But it ricochets and hits {lineup[1].name}")
            time.sleep(0.5)
            toattack = 2
        for n in range(toattack):
            damage = random.randint(math.floor(self.strength/2), self.strength)
            lineup[n].hurt(damage)
        return

    def special(self,lineup):   #Runs away like a wimp
        print(f"{self.name} flees from the scene")
        time.sleep(0.5)
        self.hurt(self.hp)
        return

class Brawler(enemy):
    def __init__(self, name, hitpoints, strength):
        super().__init__(name, hitpoints,strength)
        self.moveset = [self.light, self.heavy, self.area, self.special]

    def light(self, lineup):
        damage = random.randint(self.strength, self.strength + 3)
        print(f"{self.name} punches {lineup[0].name}")
        time.sleep(0.5)
        lineup[0].hurt(damage)
        return

    def heavy(self, lineup):
        print(f"{self.name} lifts their hammer,")
        time.sleep(0.5)
        print(f"Smashing down on {lineup[0].name}, stunning the hero...")
        time.sleep(0.5)
        lineup[0].stunned += 1
        damage = random.randint(self.strength, self.strength * 3)
        lineup[0].hurt(damage)
        return

    def area(self,lineup):  #Hits all
        print(f"{self.name} spins their hammer, hitting everyone in the team")
        time.sleep(0.5)
        for n in range(len(lineup)):
            damage = random.randint(math.floor(self.strength/2), self.strength)
            lineup[n].hurt(damage)
        return
            
    def special(self, lineup):
        print(f"{self.name} dashes forward, grabbing {lineup[0].name}.")
        time.sleep(1)
        print(f"Leaping into the air, {self.name} smashes {lineup[0].name} into the ground,")
        time.sleep(0.1)
        damage = random.randint(self.strength, math.floor(self.strength*1.2))
        print(f"-{damage}")
        time.sleep(0.7)
        print(f"following up with the hammer descending upon {lineup[0].name}...")
        time.sleep(0.1)
        tempdam = random.randint(self.strength * 3, self.strength * 7)
        print(f"-{tempdam}")
        time.sleep(0.5)
        damage += tempdam
        lineup[0].hurt(damage)
        return
            
#---------------------------Universal functions because idk how to put it under the class---------------
def remfrlineup(lineup): # Checks if any character in a lineup is dead, removes them from lineup
    newlineup = []
    newattacklineup = []
    for x in range(len(lineup)):
        if lineup[x].hp > 0:
            newlineup.append(lineup[x])
            newattacklineup.append(lineup[x].moveset)
    return newlineup, newattacklineup

def lostcheck(lineup):    #Check if all characters are dead
    if len(lineup) == 0:
        return True
    return False

def attacklist(lineup):    #Creates the moveset from a character, so i can call them later on in the fight
    attacks = []
    for i in lineup:
        attacks.append(i.moveset)
    return attacks

def clear_screen():    #To create a function that clears the screen (suitable for multiple platforms)
    #Note: This only works in console and does work in IDLE when testing so....
    operating_system = sys.platform

    if operating_system == 'win32':
        subprocess.run('cls', shell=True)

    elif operating_system == 'linux' or operating_system == 'darwin':
        subprocess.run('clear',shell=True)

def validatenumber(playerinput, ranger):   #Ranger is the range of the list
    try:
        playerinput = int(playerinput)
    except:
        return False #Not an integer input
    else:
        if playerinput > 0 and playerinput < len(ranger):
            return True
        return False
    #Check if within range

def fightsequence(lineup, enemylineup):    #The fight function
    #0 means enemy wins, 1 means player wins
    turn = 1
    attacks = attacklist(lineup)   #The moves of every character
    eattacks = attacklist(enemylineup)   #The moves of every enemy character
    while True:
        time.sleep(2)
        print(f"--------------Statistics----------------------------")
        print("---------Your Team-----------")
        for n in lineup:
            print(f"----{n.name}-----")
            print(f"Hp: {n.hp} / {n.maxhp}")
            print(f"Defense: {n.defense}")
            print(f"Stamina: {n.stamina} / {n.maxstamina}")
            print(f"Strength: {n.strength}")
            print(f"Rage: {n.rage}")
        time.sleep(1)

        print(f"---------------Player turn {turn}------------------")
        time.sleep(0.2)
        for x in range(len(lineup)):
            print(f"----{lineup[x].name}----")   #Character turn
            print(lineup[x].displaymoveset)    #Show the list of moves available
            if lineup[x].stunned <= 0:   #If not stunned...
                attack = input(f"Pick an attack 1 to {len(attacks[x])}: ")
                while True:
                    while not(validatenumber(attack, attacks[x])):
                        attack = input(f"Pick an attack 1 to {len(attacks[x])}: ")
                    attack = int(attack)




            
                    time.sleep(0.2)
                    if attacks[x][attack-1](1, enemylineup) == False:    #If there is a requirement to be met, (e.g. Charge) AND it is not met
                        pass
                    else:     
                        break
                attacks[x][attack-1](0, enemylineup)    #Perform the attack on the enemy team
            else:
                print("Unable to perform actions this turn...")    
                lineup[x].stunned -= 1   #Stun removed by 1 
            time.sleep(1)

            enemylineup, eattacks = remfrlineup(enemylineup)    #Check if any enemy needs to be removed (defeated enemies)
            if lostcheck(enemylineup):    #If no more enemies, win
                return 1

        print(f"---------------Enemy turn {turn} -------------------")
        for x in range(len(enemylineup)):
            print(f"----{enemylineup[x].name}----")   #Enemy character turn 
            if enemylineup[x].stunned <= 0:   #Check if enemy stunned
                if turn % 9 == 0:    #If turn is a multiple of 9
                    rng = len(eattacks[x]) - 1    #Set attack to special
                else:
                    rng = random.randint(0, len(eattacks[x]) - 2)   #Randomize attack from the given moveset
                eattacks[x][rng](lineup)    #Perform attack on player team
                
            else:
                print("Unable to perform actions this turn...") 
                enemylineup[x].stunned -= 1   #Remove stunned counter by 1
            time.sleep(1)

            lineup, attacks = remfrlineup(lineup)   #Check if any player character needs to be removed + reset attack list
            if lostcheck(lineup):   #If character lineup no more heroes, lose
                return 0

        enemylineup, eattacks = remfrlineup(enemylineup)    #If enemy lineup empty, win
        if lostcheck(enemylineup):   #Safety in case player wins after enemy turn (poison inflicted)
            return 1


        time.sleep(1)
        turn += 1
        clear_screen()



#-----------------------Battle sequence--------------------------------------
p1 = Warrior("Chadwin", 40, 4, 10, 3, 4)
p2 = Warrior("Robles", 30, 6, 10, 3, 4)
p3 = Warrior("Reyrey", 35, 5, 12, 4, 5)
lineup = [p1,p2,p3]   #Idea of a lineup, the one at the front takes damage(aka list index 0)

e1 = Brawler("The goat", 300, 4)
e2 = Robber("The sheep", 100, 6)
enemylineup = [e1,e2]


#-----The actual fight-------  (Turn it into a function thats under a class called "Dungeon")
fightscene = fightsequence(lineup, enemylineup)
if fightscene == 1:
    print("Player wins...")
else:
    print("Enemy wins...")
    
