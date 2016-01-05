#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      chandp4
#
# Created:     30-12-2015
# Copyright:   (c) chandp4 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#Section
class Section(object):
    def __init__(self,name):
        self.name = name
        self.num_developers = 0
        self.num_teams = 0
        self.team_list = []

    def addDeveloper(self,name,team_name):
        team_found = False
        developer_found = False
        for team in self.team_list:
            if (team.name.lower() == team_name.lower()):
                team_found = True
                if (team.addDeveloper(name) == True):
                    self.num_developers += 1
                break
        if (team_found == False):
            self.team_list.append(Team(team_name))
            self.team_list[self.num_teams].addDeveloper(name)
            self.num_developers += 1
            self.num_teams += 1

    def getDeveloperCount(self):
        return self.num_developers

    def __str__(self):
        print_str = "Section Name: " + self.name + "\n"
        print_str += "Developer Count: " + self.num_developers.__str__() + "\n"
        print_str += "************************************\n"
        for team in self.team_list:
            print_str += "Team Name: " + team.name + "\n"
            print_str += "Developer Count: " + team.num_developers.__str__() + "\n"
            for developer in team.developer_list:
                print_str += "\tDeveloper Name: " + developer.name + "\n"
            print_str += "************************************\n"
        return print_str
#end Section Class

#Team
class Team(object):
    def __init__(self,name):
        self.num_developers = 0
        self.name = name
        self.developer_list = []

    def addDeveloper(self,developer_name):
        developer_found = False
        ret_val = False
        for developer in self.developer_list:
            if developer.name.lower() == developer_name.lower():
                developer_found = True
                break

        if (developer_found == False):
            self.developer_list.append(Developer(developer_name,self.name))
            self.num_developers += 1
            ret_val = True

        return ret_val

    def removeDeveloper(self,developer_name):
        for developer in self.developer_list:
            if (developer.name == developer_name):
                self.developer_list.remove(developer)
                self.num_developers -= 1
                break

    def getDeveloperCount(self):
        return self.num_developers
#end Team

#Monthly statistics of developer
class MonthlyDevStat(object):
    __monthsInAYear = 12
    def __init__(self):
        self.stats_by_month = []
        for i in range(0,self.__monthsInAYear):
            self.stats_by_month.append(CsnsRepoStats())
        self.monthly_stat_series = panda.Series(self.stats_by_month,index=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Oct","Sep","Nov","Dec"])


#Annual statistics of a developer
class AnnualDevStat(object):
    def __init__(self):
        self.annual_statistics = CsnsRepoStats()

#Statistics of CSNS repositories
class CsnsRepoStats(CsnsRepositoryList):
    def __init__(self):
        #Init repositories
        CsnsRepositoryList.__init__(self)

        #Setup a list of repo stats for all repositories that we have
        self.repo_stat_list = []
        for i in range(0,self.num_repos):
            self.repo_stat_list.append(RepoStats(self.list_of_repos[i]))

    def __str__(self):
        return

#List of repositories in the CSNS
class CsnsRepositoryList(object):
    def __init__(self):
        self.list_of_repos = ["SCL","OEL","HAL"]
        self.num_repos = len(self.list_of_repos)

def main():
    pass

if __name__ == '__main__':
    main()
