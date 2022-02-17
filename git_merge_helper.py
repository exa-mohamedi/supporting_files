"""
To pick the changes from one merge commit to another.

1. Use to load all commits of a merge commit (962f08418c7e4631d6fd77bf165c5fba40de0f61):
git config --global alias.log-merge '!f() { git log --stat "$1^..$1" --pretty=format:HASH={%H},SUB={%s}; }; f' && git log-merge 962f08418c7e4631d6fd77bf165c5fba40de0f61 | tee Commits

2. Check the commits log and delete the commits not needed manually (Ex: Branch Merges).

3. Load the updated commit file in the python script.

4. Python Script will generate the cherry-pick command and push command.

5. Run those commands manually on the terminal.

Note: Please be careful about the commits.
"""
import re

Merge_Branch_Commit_Msg = "Merge branch "
class git_data:
    def __init__(self, hash : str, sub : str):
        self.hash = hash
        self.sub = sub

def generate_commit_cmd(hash : list):
    hash.reverse()
    for i in hash:
        print(f"git cherry-pick {i.hash} # {i.sub}")
    print("git push")

def main():
    Filename = "/home/mom/nosync/2022_02_17/git.db+master.interfaces-1a22b214-64o/Commits"
    FileHandle = open(Filename, "r")
    Content = FileHandle.read()
    Lines = Content.splitlines()
    Lines = list(filter(None, Lines))
    Hashes = []
    for Line in Lines:
        try:
            Hash, Sub = re.search(r'HASH=\{(.+?)\},SUB=\{(.+?)\}', Line).groups()
            if Merge_Branch_Commit_Msg in Sub:
                print("[ERROR] Merge Branch commit found. Please remove the commit from the log.")
                print(f"Hash = {Hash} Subject = {Sub}")
                exit(1)
            Hashes.append(git_data(hash=Hash, sub=Sub))
        except AttributeError:
            pass
    generate_commit_cmd(Hashes)




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
