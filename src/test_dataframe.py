import pandas as pd

class RepoStats(object):
    def __init__(self,name):
        self.code_additions = 0
        self.code_deletions = 0
        self.code_changes = 0
        self.files_changed = 0
        self.repo_name = name
    def __str__(self):
        return 'Repository: ' + self.repo_name + ' Code changes: ' + self.code_changes.__str__()

    def updateRepoStats(self,code_additions,code_deletions,files_changed):
        self.code_additions += code_additions
        self.code_deletions += code_deletions
        self.files_changed += files_changed
        self.code_changes = self.code_additions + self.code_deletions


def main():
    month_list = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Oct","Sep","Nov","Dec"]
    devStat = pd.DataFrame(index=month_list,columns=['scl'],dtype=RepoStats)
    devStat.loc['Jan','scl']= RepoStats("scl")
    
    for index,row in devStat.iterrows():
        for series_index, value in row.iteritems():
            print(value)

    print ("******************")
    for index,column in devStat.iteritems():
        print(index,column)
    
    #print(devStat.loc[:])

if __name__ == "__main__":
    main()
