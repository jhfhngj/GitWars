import os
import json
import subprocess
if not os.path.exists("game.json"):
    with open("game.json","a") as f:
        json.dump({"battlecount":0,"battles":[],"won":0},f)
    cur = {"battlecount":0,"battles":[],"won":0}
else:
    with open("game.json") as f:
        cur = json.loads(f.read())
if os.system("gh") != 0:
    print("Install GitHub CLI and log in for this game to work.")
    exit( 1 )
def api(do):
    return command(f"gh api --cache 1h {do}")
def command(do):
    return subprocess.run(do.split(),capture_output=True,text=True,check=True).stdout

print("GitWars by jhfhngj")
print("Welcome to GitWars!")
uname = api("user --jq .login")
print("Your username is",uname)
print("Ctrl-C or (Ctrl-D for *nix, Ctrl-Z+Enter for Windows) to exit.")
try:
    while True:
        print("Would you like to")
        print("1. Battle")
        print("or")
        print("2. Fetch your stats")
        print("?")
        do = int(input()[0])
        if do == 2:
            print("Your stats:")
            repocount = command("gh repo list").splitlines()[1].strip().replace("Showing ","").replace("of ","").replace("repositories in ","").replace(" ","").split()[0]
            won = cur["won"]
            print("You have",repocount,"repos.")
            print("Whilst battling, you won",won,"times!")
            print("You currently have",sum(map(int,api(f"/users/{uname}/repos --jq '.[].size'").splitlines())),"bytes.")
        else:
            print("Welcome to Battle Mode.")
            print("Here you can battle all your opponents.")
            print("Who of all the GitHub land would you like to battle?")
            out = 0
            while out != 0:
                tobattle = input()
                out = os.system(f"gh api users/{tobattle} --jq '.login'")
            
except (EOFError, KeyboardInterrupt):
    print("Goodbye!")
except Exception as e:
    print("A fatal exception in GitWars has occurred:",e)
