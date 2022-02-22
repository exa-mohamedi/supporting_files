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
import argparse

class git_data:
    def __init__(self, hash : str, sub : str, user : str):
        self.hash = hash
        self.sub = sub
        self.user = user

def generate_commit_cmd(hash : list):
    print("=====================Git Commits to Cherry-Pick=====================")
    hash.reverse()
    for i in hash:
        print(f"git cherry-pick {i.hash} # {i.sub} | {i.user}")
    print("git push")

def default_values():
    val = dict()
    val['Merge_Branch_Commit_Msg'] = "Merge branch "
    val['Merge_Pull_Request'] = "Merge pull request #"
    val['Throw_Error_For_Specific_Msg'] = True
    return val

def main():
    default_values_dict = default_values()
    args = argumentParser()
    if not args.hashlogfile:
        print("[ERROR] Hash Log file not provided.")
        exit(1)
    if args.strictcheck:
        if args.strictcheck not in ['0', '1']:
            print("[ERROR] Invalid value for argument strictcheck is provided. Accepted values for 0 and 1")
            exit(1)
        elif args.strictcheck == '0':
            default_values_dict['Throw_Error_For_Specific_Msg'] = False
        elif args.strictcheck == '1':
            default_values_dict['Throw_Error_For_Specific_Msg'] = True

    Filename = args.hashlogfile

    # Print Configuration
    print(f"Git Hash Log file = {Filename}")
    print(f"Strict Hash Verification = {default_values_dict['Throw_Error_For_Specific_Msg']}")

    FileHandle = open(Filename, "r")
    Content = FileHandle.read()
    Lines = Content.splitlines()
    Lines = list(filter(None, Lines))
    Hashes = []
    for Line in Lines:
        try:
            Hash, Sub, Usr = re.search(r'HASH=\{(.+?)\},SUB=\{(.+?)\},USER=\{(.+?)\}', Line).groups()
            if default_values_dict['Merge_Branch_Commit_Msg'] in Sub or default_values_dict['Merge_Pull_Request'] in Sub:
                print(f"Hash = {Hash} Subject = {Sub} User = {Usr}")
                Msg = "Merge Branch commit found. Please remove the commit from the log."
                if default_values_dict['Throw_Error_For_Specific_Msg']:
                    print(f"[ERROR] {Msg}")
                    exit(1)
                else:
                    print(f"[WARNING] {Msg} The Commit is skipped. ")
                    continue
            Hashes.append(git_data(hash=Hash, sub=Sub, user=Usr))
        except AttributeError:
            pass
    generate_commit_cmd(Hashes)


"""
Parse the command line arguments
"""
def argumentParser():
    parser = argparse.ArgumentParser(description='Load the commit hash from git log file. And extract the hashes to '
                                                 'cherry-pick')
    parser.add_argument('--hashlogfile', '-l', help='Hash Log file')
    parser.add_argument('--strictcheck', '-s', help='Throw error for invalid hashes.\n'
                                                    'Accepted values are 0 (No) ot 1 (Yes)\n'
                                                    'Default value: 1 (Yes)')
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    main()
