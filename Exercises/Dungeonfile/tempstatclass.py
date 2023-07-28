#To make a class that takes in values of buffs / debuffs as long as their timer in the form of a list
#Apply to main stat E.g. Def: [[+4,2], [-3,1]] Meaning: + 4 for 2 turns, -3 for 1 turn, thus net gain of 1

class tempstat():
    def __init__(self):   #Attributes is in the form of a list 
        self.tempattri = {}

    def addtempattri(self, tempstat: dict):  #Tempstat is E.g. {"defense": {"values": [], "turns": int}}
        #Change something regarding the ability to add tempstats to empty lists
        for j in tempstat.keys():
            tempset = [sum(tempstat[j]["values"]), tempstat[j]["turns"]]   #The set contains two values, the main affecting value of the stat and the turns it last for
            try:
                self.tempattri[j].append(tempset)
            except:
                self.tempattri[j] = [tempset]
        return

    def attricounter(self):   #Reduce the number of turns last by 1, remove from attributes
        #Access the group for a certain stat
        newtemp = {}  #Refreshed list of buffs/debuffs
        for x in self.tempattri.keys():
            newtemp[x] = []
            #Access the list of nested lists
            for n in self.tempattri[x]:
                n[1] -= 1  #Reduce the lasted turns by one
                if n[1] > 0:   #Check if attribute still lasted
                    newtemp[x].append(n)
        self.tempattri = newtemp
        return
    
#Test1 -- pending
# banana = tempstat()
# print(banana.tempattri)
# banana.addtempattri({"defense": {"values": [2,3], "turns": 2}})
# banana.addtempattri({"defense": {"values": [7,0,1], "turns": 3}})
# banana.addtempattri({"strength": {"values": [8,3], "turns": 1}})
# print(banana.tempattri)
# for x in range(3):
#     print(f"-----------------------{x}-----------")
#     banana.attricounter()

#     print(banana.tempattri)
            

        
        
            

