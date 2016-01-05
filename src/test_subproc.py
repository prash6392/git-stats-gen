import os
import subprocess as subproc

class Developer(object):
    def __init__(self,name):
        self.name = name
        

class Team(object):
    def __init__(self):
        self.developer_list = []
        self.count = 0

    def addDeveloper(self,name):
        self.developer_list.append(Developer(name))
        self.count += 1

    def removeDeveloper(self,name):
        for developer in self.developer_list:
            if (developer.name == name):
                self.developer_list.remove(developer)
                self.count -= 1
                break
        

    def getNumDevelopers(self):
        return self.count
    
def main():
    team = Team()
    team.addDeveloper("Amuru")
    print(team.getNumDevelopers())
    team.addDeveloper("Prashanth")
    print(team.getNumDevelopers())
    team.removeDeveloper("Prashanth")
    print(team.getNumDevelopers())

if __name__== '__main__':
    main()
