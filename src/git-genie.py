#-------------------------------------------------------------------------------
# Name:        GitGenie Test application
# Purpose:
#
# Author:      chandp4
#
# Created:     23-12-2015
# Copyright:   (c) chandp4 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#Data structures
import pandas as panda
#Numerical algorithms
import numpy as numpy
#Import plotting library
import matplotlib.pyplot as pyplt
#Import os to ease directory manipulation
import os
#Import this to ease calling GIT commands
import subprocess as subproc

#General Statistics of a GIT repository
class RepoStats(object):
    def __init__(self,name):
        self.code_additions = 0
        self.code_deletions = 0
        self.code_changes = 0
        self.files_changed = 0
        self.num_of_commits = 0
        self.repo_name = name
    def __str__(self):
        return 'Repository: ' + self.repo_name + ' Code changes: ' + self.code_changes.__str__()

    def updateRepoStats(self,code_additions,code_deletions,files_changed):
        self.code_additions += code_additions
        self.code_deletions += code_deletions
        self.files_changed += files_changed
        self.num_of_commits += 1
        self.code_changes = self.code_additions + self.code_deletions

class GitStatEntry(object):
    def __init__(self):
        self.author= ""
        self.date = ""
        self.repo = ""
        self.insertions = 0
        self.deletions = 0
        self.files_changed = 0

    def storeDetails(self,author,insertions,deletions,files_changed,date,repo):
        self.author = author
        self.insertions = insertions
        self.deletions = deletions
        self.files_changed = files_changed
        self.date = date
        self.repo = repo

    def __del__(self):
        self.author= ""
        self.insertions = 0
        self.deletions = 0
        self.files_changed = 0
        self.date = ""
        self.repo = ""

    def __str__(self):
        print_str ="Author: " + self.author
        print_str +=" Repo: " + self.repo
        print_str +=" Date: " + self.date
        print_str += " Insertions: " + self.insertions.__str__()
        print_str += " Deletions: " + self.deletions.__str__()
        print_str += " Files Changed: " + self.files_changed.__str__()
        return print_str
#end GitStatEntry

#Developer Stats
class DeveloperStats(object):
    __month_list = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Oct","Sep","Nov","Dec"]
    __base_repo = 'scl'
    def __init__(self):
        self.num_of_commits = 0
        initial_table_data = self.__createRepoStatList(DeveloperStats.__base_repo)
        initial_series = panda.Series(initial_table_data,index=DeveloperStats.__month_list)
        initial_dict = {DeveloperStats.__base_repo: initial_series}
        self.monthly_stat_table = panda.DataFrame(initial_dict)
        self.__addRepoToMonthlyTable('scl')
        all_repo_series_data = self.__createRepoStatList("master repo")
        self.master_repo_stat_series = panda.Series(all_repo_series_data, index=DeveloperStats.__month_list,dtype=RepoStats)
        self.annual_stat = RepoStats("Annual Stats")

    def __createRepoStatList(self,repo_name):
        repo_stat_list = []
        for i in range(0,len(DeveloperStats.__month_list)):
            repo_stat_list.append(RepoStats(repo_name))
        return repo_stat_list

    def __addRepoToMonthlyTable(self,repo_name):
        monthly_data = []
        if repo_name not in self.monthly_stat_table.columns:
            monthly_data = self.__createRepoStatList(repo_name)
            self.monthly_stat_table[repo_name] = monthly_data

    def addRepo(self,repo_name):
        self.__addRepoToMonthlyTable(repo_name)

#End Developer stats

class Developer(DeveloperStats):
#Developer ID
    __developer_id = 0
    def __init__(self,name):
        DeveloperStats.__init__(self)
        self.name=name
        self.team = "Unassigned"
        self.repos_worked_on = []
        self.id = Developer.__developer_id
        Developer.__developer_id += 1

    def __del__(self):
        self.name= "NoName" + Developer.__developer_id.__str__()
        self.team = "Unassigned" + Developer.__developer_id.__str__()
        self.repos_worked_on = []

    def __updateMonthlyStat(self,git_stat_entry):
        month = git_stat_entry.date.split()[1]
        if month in self.monthly_stat_table.index:
            self.monthly_stat_table.loc[month,git_stat_entry.repo].updateRepoStats(git_stat_entry.insertions,git_stat_entry.deletions,git_stat_entry.files_changed)

    def __updateAllRepoMonthlyStat(self,git_stat_entry):
        month = git_stat_entry.date.split()[1]
        if month in self.master_repo_stat_series.index:
            self.master_repo_stat_series[month].updateRepoStats(git_stat_entry.insertions,git_stat_entry.deletions,git_stat_entry.files_changed)

    def updateDeveloperStat(self,git_stat_entry):
        if git_stat_entry.repo not in self.repos_worked_on:
            self.repos_worked_on.append(git_stat_entry.repo)
            self.addRepo(git_stat_entry.repo)
        self.num_of_commits += 1
        self.__updateMonthlyStat(git_stat_entry)
        self.__updateAllRepoMonthlyStat(git_stat_entry)

    def plotMonthlyStats(self,outpath):
        code_changes = []
        row_index = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Oct","Sep","Nov","Dec"]
        for i in range(0,self.master_repo_stat_series.count()):
            code_changes.append(self.master_repo_stat_series[i].code_changes)
        ind = numpy.arange(len(code_changes))
        fig,ax = pyplt.subplots()
        width = .35
        trend = ax.bar(ind,code_changes,width,color='y')
        ax.set_ylabel('Code Changes')
        ax.set_xlabel('Month')
        ax.set_xticks(ind+width)
        ax.set_xticklabels(row_index)
        ax.set_title('Code contributed per month by ' + self.name)
        file_name = outpath+'\\'+self.name+'__monthlyStats.png'
        pyplt.savefig(file_name,dpi=300)
        pyplt.close()


    def plotAnnualStats(self,outpath):
        self.calConsolidatedAnnualStats()
        fig,ax = pyplt.subplots()
        width = .25
        ind = numpy.arange(3)
        add_bar = ax.bar(0,self.annual_stat.code_additions,width,color='r')
        del_bar = ax.bar(1+width,self.annual_stat.code_deletions,width,color='g')
        files_bar = ax.bar(2+(2*width),self.annual_stat.files_changed,width,color='y')
        ax.set_xlabel(self.name)
        ax.set_ylabel('No. of changes')
        ax.set_xticks(ind+width)
        ax.set_xticklabels(('Code Additions','Code Deletions','Files Changed'))
        ax.set_title(self.name + ': Annual statistics')
        ax.legend((add_bar[0],del_bar[0],files_bar[0]),('Code Additions','Code Deletions','Files Changed'),fontsize=8)
        file_name = outpath+'\\'+self.name+'_annualStats.png'
        pyplt.savefig(file_name,dpi=300)
        pyplt.close()


    def plotStatsByRepo(self,outpath):
        stats_by_repo = self.calStatsByRepo()
        fig,ax = pyplt.subplots()
        ax.set_xlabel("Repository")
        ax.set_ylabel("Number of changes")
        ax.set_title(self.name + ': Stats by repository')
        ind = numpy.arange(len(self.repos_worked_on))
        width = 0.15
        i=0
        fig_list = []
        for stat in stats_by_repo:
            fig_list.append(ax.bar(i,stat.code_additions,width,color='r'))
            fig_list.append(ax.bar(i+width,stat.code_deletions,width,color='y'))
            fig_list.append(ax.bar(i+(2*width),stat.files_changed,width,color='g'))
            i+=1
        ax.set_xticks(ind+width)
        ax.set_xticklabels(self.repos_worked_on,fontsize=8)
        ax.legend((fig_list[0],fig_list[1],fig_list[2]),('Code Additions','Code Deletions','Files Changed'),fontsize=8)
        file_name = outpath+'\\'+self.name+'_statsByRepository.png'
        pyplt.savefig(file_name,dpi=300)
        pyplt.close()



    def calStatsByRepo(self):
        repo_stats = []
        for repo in self.repos_worked_on:
            repo_stats.append(RepoStats(repo))
            code_additions = 0
            code_deletions = 0
            files_changed = 0
            for month in self.monthly_stat_table.index:
                code_additions += self.monthly_stat_table.loc[month,repo].code_additions
                code_deletions += self.monthly_stat_table.loc[month,repo].code_deletions
                files_changed += self.monthly_stat_table.loc[month,repo].files_changed
            repo_stats[len(repo_stats)-1].updateRepoStats(code_additions,code_deletions,files_changed)
        return repo_stats

    def calStatsByMonth(self):
        month_stats = []
        for month in self.monthly_stat_table.index:
            month_stats.append(RepoStats(month))
            code_additions = 0
            code_deletions = 0
            files_changed = 0
            for repo in self.repos_worked_on:
                code_additions += self.monthly_stat_table.loc[month,repo].code_additions
                code_deletions += self.monthly_stat_table.loc[month,repo].code_deletions
                files_changed += self.monthly_stat_table.loc[month,repo].files_changed
            month_stats[len(month_stats)-1].updateRepoStats(code_additions,code_deletions,files_changed)
        return month_stats


    def calConsolidatedAnnualStats(self):
        self.annual_stat.code_additions = 0
        self.annual_stat.code_deletions = 0
        self.annual_stat.files_changed = 0
        self.annual_stat.code_changes = 0
        for index,value in self.master_repo_stat_series.iteritems():
            self.annual_stat.code_additions +=value.code_additions
            self.annual_stat.code_deletions += value.code_deletions
            self.annual_stat.files_changed += value.files_changed
        self.annual_stat.code_changes = self.annual_stat.code_additions + self.annual_stat.code_deletions

    def __str__(self):
        print_str = "Developer Name: " + self.name
        print_str += " Repos worked on: " + self.repos_worked_on.__str__()
        print_str += " Monthly Stat Table: " + self.monthly_stat_table.__str__()
        print_str += " Master Stat Series: " + self.master_repo_stat_series.__str__()
        print_str += " Annual Stats: " + self.annual_stat.__str__()
        return print_str

    def setTeam(self,team_name):
        self.team = team_name
#End Developer

class DeveloperList(object):
    def __init__(self):
        self.developer_list = []
        self.__num_developers = 0

    def __del__(self):
        self.developer_list = []
        self.__num_developers = 0


    def __doesDeveloperExist(self,name):
        developer_found = False
        index = 0
        for developer in self.developer_list:
            if developer.name == name:
                developer_found = True
                index = self.developer_list.index(developer)
        return developer_found, index

    def __addDeveloper(self,name):
        self.developer_list.append(Developer(name))
        self.__num_developers += 1

    def updateDeveloperList(self,git_stat_entry):
        flag = False
        name = git_stat_entry.author
        (flag,index) = self.__doesDeveloperExist(name)
        if (flag == True):
            self.developer_list[index].updateDeveloperStat(git_stat_entry)
        else:
            self.__addDeveloper(name)
            self.developer_list[self.__num_developers-1].updateDeveloperStat(git_stat_entry)

    def saveListStats(self,outpath):
        months_in_a_year = 12
        consolidated_monthly_stats = []
        for i in range(months_in_a_year):
            consolidated_monthly_stats.append(RepoStats('Month_'+i.__str__()))

        for developer in self.developer_list:
            monthly_stats = developer.calStatsByMonth()
            for i in range(months_in_a_year):
                consolidated_monthly_stats[i].updateRepoStats(monthly_stats[i].code_additions,monthly_stats[i].code_deletions,monthly_stats[i].files_changed)

        total_code_additions = []
        total_code_deletions = []
        total_files_changed = []
        for i in range(months_in_a_year):
            total_code_additions.append(consolidated_monthly_stats[i].code_additions)
            total_code_deletions.append(consolidated_monthly_stats[i].code_deletions)
            total_files_changed.append(consolidated_monthly_stats[i].files_changed)

        #Begin Plotting
        fig,ax = pyplt.subplots()
        ind = numpy.arange(months_in_a_year)
        month_names = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Oct","Sep","Nov","Dec"]
        width = 0.25
        cd_add_bar = ax.bar(ind,total_code_additions,width,color='y')
        cd_del_bar = ax.bar(ind+width,total_code_deletions,width,color='g')
        cd_changes_bar = ax.bar(ind+(2*width),total_files_changed,width,color='b')
        ax.set_xlabel('Months')
        ax.set_ylabel('Changes made')
        ax.set_title('Consolidated stats by month - For all developers')
        ax.set_xticks(ind+width)
        ax.set_xticklabels(month_names)
        ax.legend((cd_add_bar[0],cd_del_bar[0],cd_changes_bar[0]),('Code additions','Code deletions','Files changed'),fontsize=8)
        file_name = outpath+'\\'+'__consolidatedStats' +'__byMonth' +'.png'
        pyplt.savefig(file_name,dpi=300)


    def getMostActiveDeveloper(self):
        most_active_developer_idx = 0
        max_commits = 0
        for developer in self.developer_list:
            if developer.num_of_commits > max_commits:
                max_commits = developer.num_of_commits
                most_active_developer_idx = self.developer_list.index(developer)
        return self.developer_list[most_active_developer_idx]


class GitGenie(object):
    genie_id = 0
    def __init__(self,searchpath,outpath,developer_list):
        self.outpath = searchpath
        self.seedpath = outpath
        self.developer_list = developer_list

    def run(self):
        self.genieRecursiveSearch(self.seedpath)
        self.saveResults()

#Recursively find GIT directories in search path
    def genieRecursiveSearch(self,searchpath):
        os.chdir(searchpath)
        list_of_subdirs = os.listdir(searchpath)
        if len(list_of_subdirs) != 0:
            if ".git" not in list_of_subdirs:
                for directory in list_of_subdirs:
                    if os.path.isdir(directory):
                        new_path = os.path.join(searchpath,directory)
                        #Recursively search for GIT directories
                        self.genieRecursiveSearch(new_path)
                        parent_dir = os.path.split(new_path)[0]
                        os.chdir(parent_dir)
            else:
                print('Calculating statistics from ' + os.path.basename(searchpath))
                #Extract statistics from GIT repository
                self.extractStatsFromRepo(searchpath)

#Extracts statistics from a GIT repository and updates the Genies developer list
    def extractStatsFromRepo(self,path):
        ugly_stats = self.runGitLog(path)
        repo_name = os.path.basename(path)
        neat_stats = self.parseGitStats(ugly_stats,repo_name)
        for stat in neat_stats:
            self.developer_list.updateDeveloperList(stat)

#Run GIT log in the given path
    def runGitLog(self,path):
        os.chdir(path)
        git_proc = subproc.Popen(["git", "log",'--all',"--pretty=format:'--@--%cn---Commit:%h---%cd-#--","--shortstat" , "--since='12 month ago'", "--no-merges"],stdout=subproc.PIPE)
        stats = git_proc.stdout.read()
        return stats

#Parse the commit information obtained after running GIT Log
    def parseGitStats(self,gitstats,repo_name):
        git_stat_list = []
        files_changed = 0
        insertions = 0
        deletions = 0
        stat_str = gitstats.__str__()
        commit_history = stat_str.split("b",maxsplit=1)[1]
        commit_entries = commit_history.split("--@--")
        for entry in commit_entries:
            if (len(entry) > 2):
                commit_stat = GitStatEntry()
                (author,sep,left_over) = entry.partition("---")
                (sha_id,sep,left_over) = left_over.partition("---")
                (commit_date,sep,left_over) = left_over.partition('-#--')
                additional_stats = left_over.split(',')
                if(len(additional_stats)<2):
                    files_changed = 0
                    insertions = 0
                    deletions = 0
                else:
                    for i in range(0,len(additional_stats)):
                        if (i==0):
                            files_changed = int((additional_stats[0].split())[1])
                        elif(i==1):
                            insertions=int((additional_stats[1].split())[0])
                        else:
                            deletions=int((additional_stats[2].split())[0])
                commit_stat.storeDetails(author,insertions,deletions,files_changed,commit_date,repo_name)
                git_stat_list.append(commit_stat)
        return git_stat_list

#Creates charts in output directory
    def saveResults(self):
        for developer in self.developer_list.developer_list:
            print('Saving results for '+developer.name)
            developer.plotMonthlyStats(self.outpath)
            developer.plotAnnualStats(self.outpath)
            developer.plotStatsByRepo(self.outpath)
        best_developer = self.developer_list.getMostActiveDeveloper()
        print('Developer with maximum commits: '+best_developer.name)
        print('Number of commits: '+best_developer.num_of_commits.__str__())
        print('Saving consolidated statistics for all developers')
        self.developer_list.saveListStats(self.outpath)

#Destructor
    def __del__(self):
        self.outpath = ""
        self.seedpath = ""
        self.developer_list = []
#Printer
    def __str__(self):
        print_str = 'GIT Genie ' + GitGenie.genie_id.__str__() + '\n'
        print_str += 'Search Path: ' + self.seedpath + '\n'
        print_str += 'Output Path: ' + self.outpath
        return print_str

#Global developer list
global_developer_list = DeveloperList()

def main():
    genie = GitGenie("C:\\Prashanth\\CAT\\MyRepo\\git-genie","C:\\ivy\\ethernet_hal_platform_arch\\lib\\lib_csf",global_developer_list)
    print(genie)
    genie.run()

if __name__ == '__main__':
    main()
