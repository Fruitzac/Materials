#-----------------Module Imports---------------------------
import random, time, math, sys, subprocess
import charclass  #Characters and their skills

print("Turn based game: Perform moves with characters")
   
#---------------------------Universal functions because idk how to put it under the class---------------
def remfrlineup(lineup): # Checks if any character in a lineup is alive, keep them in lineup
    newlineup = []
    for x in lineup:
        if x.hp > 0:
            newlineup.append(x)
    return newlineup

def lostcheck(lineup):    #Check if all characters are dead
    if len(lineup) == 0:
        return True
    return False



def clear_screen():    #To create a function that clears the screen (suitable for multiple platforms)
    #Note: This only works in console and does work in IDLE when testing so....
    operating_system = sys.platform

    if operating_system == 'win32':
        subprocess.run('cls', shell=True)

    elif operating_system == 'linux' or operating_system == 'darwin':
        subprocess.run('clear',shell=True)

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

def makebars(value,maxvalue, barnumber):
    barvalue = maxvalue / barnumber
    neededbars = math.ceil(value / barvalue)
    airbars = barnumber - neededbars
    return f"[{neededbars*'=' + airbars*' '}]"





class BattleSequence():
    def __init__(self, playerteam, enemyteam, loot):
        self.teamcomp = playerteam
        self.enemycomp = enemyteam
        self.loot = loot

    def statprintout(self,char):
        print(f"--------{char.name}--------")
        if char.getattribute('hp') <= 0:
            print("Fallen")
        else:
            print(f"Hp:{makebars(char.getattribute('hp'), char.getattribute('maxhp'), 15)} {char.getattribute('hp')}/{char.getattribute('maxhp')}")
            print(f"Strength: {char.getattribute('strength')}")
            print(f"Defense: {char.getattribute('defense')}")
            for x in char.stats.keys():  #Obtain all the keys of the stats
                try:
                    char.maxstats[x]
                except:
                    print(f"{x}: {char.stats[x]}")
                else:
                    print(f"{x}:{makebars(char.stats[x], char.maxstats[x],15)} {char.stats[x]}/{char.maxstats[x]}")
        return
    
    def tempstatcount(self,lineup: list):   
        #Reduces the turns of the tempstat of every character in the given lineup
        for a in lineup:
            a.tempstats.attricounter()
        return

    def win(self):
        print(f"Yay player wins, and earns {self.loot}")

    def lose():
        print(f"How did bro lose")

    def play(self):    #The fight function
        #0 means enemy wins, 1 means player wins
        initialteams = [self.teamcomp, self.enemycomp]  #Clone of mainteams to track the stats
        mainteams = [self.teamcomp, self.enemycomp]
        turn = 1
        while True:
            #Phase 1: Preparations
            time.sleep(2)
            print(f"--------------Statistics----------------------------")
            print("---------Your Team-----------")
            for n in initialteams[0]: 
                self.statprintout(n)
            print("---------Enemy Team----------")
            for n in initialteams[1]:
                self.statprintout(n)
            time.sleep(1)

            #Phase 2: Player turn to attack
            print(f"---------------Player turn {turn}------------------")
            time.sleep(0.2)
            for x in mainteams[0]:
                print(f"----{x.name}----")   #Character turn
                print(x.displayattacks)    #Show the list of moves available
                if x.getattribute('stunned') <= 0:   #If not stunned...
                    while True:
                        attackchoice = input(f"Pick an attack 1 to {len(x.attacklist)}: ")
                        if not(validatenumber(attackchoice, len(x.attacklist))):  #The input is wrong
                            print("Not a valid number...")
                            continue
                        attackchoice = int(attackchoice)
                        if not(x.attacklist[attackchoice-1].movecost(x.stats)): #If there is a requirement to be met, (e.g. Charge) AND it is not met
                            print(x.attacklist[attackchoice-1].costfail)   #Do something
                        else:     
                            time.sleep(0.2)
                            break
                    x.attacklist[attackchoice - 1].activate(x, mainteams)    #Perform the attack on the enemy team
                    # x.stats = x.attacklist[attackchoice - 1].movecost(x.stats, False)
                else:
                    print("Unable to perform actions this turn...")    
                time.sleep(1)

                #Completely remove the need for external attacklist (All built into character)
                mainteams[1] = remfrlineup(mainteams[1])    #Check if any enemy needs to be removed (defeated enemies)
                if lostcheck(mainteams[1]):    #If no more enemies, win
                    return self.win()
            
            self.tempstatcount(mainteams[1])   #Reduce all effects by one turn

            print(f"---------------Enemy turn {turn} -------------------")
            for x in mainteams[1]:
                print(f"----{x.name}----")   #Enemy character turn 
                if x.getattribute("stunned") <= 0:   #Check if enemy stunned
                    attackchoice = random.randint(1,2)
                    x.attacklist[attackchoice - 1].activate(x, mainteams)
                    
                else:
                    print("Unable to perform actions this turn...") 
                time.sleep(1)

                mainteams[0] = remfrlineup(mainteams[0])   #Check if any player character needs to be removed + reset attack list
                if lostcheck(mainteams[0]):   #If character lineup no more heroes, lose
                    return self.lose()

            mainteams[1] = remfrlineup(mainteams[1])    #If enemy lineup empty, win
            if lostcheck(mainteams[1]):   #Safety in case player wins after enemy turn (poison inflicted)
                return self.win()


            time.sleep(3)
            self.tempstatcount(mainteams[0])
            nextturn = input("Next turn?(Input anything):")
            turn += 1
            clear_screen()




#-----------------------Battle sequence--------------------------------------
p1 = charclass.Warrior("Player","Weiner", 40, 4, 0, 10, 9)
p2 = charclass.Warrior("Player","Robles", 30, 6, 0, 10, 4)
p3 = charclass.Warrior("Player","Reynerd", 35, 5, 0, 10, 5)
teamcomp = [p1,p2,p3]   #Idea of a lineup, the one at the front takes damage(aka list index 0)

e1 = charclass.Warrior("Enemy","Fit", 50, 4, 0, 10, 4)
e2 = charclass.Warrior("Enemy","Foo", 30, 3, 0 , 10, 5)
enemycomp = [e1,e2]


#-----The actual fight-------  (Turn it into a function thats under a class called "Dungeon")
fightscene = BattleSequence(teamcomp,enemycomp, "banana")
fightscene.play()
    
