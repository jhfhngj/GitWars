import os
import json
import subprocess
import random
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
def battle(youbytes:int,thembytes:int):
    leftyou = youbytes
    leftthem = thembytes
    exhaustedyou = 0
    exhaustedthem = 0
    while not exhaustedyou > youbytes:
        used = random.randint(10000,500000)
        exhaustedyou += used
        leftthem -= used
        print("You land a blow worth",used,"bytes.")
    print("Now it's their turn!")
    while not exhaustedthem > thembytes:
        used = random.randint(10000,500000)
        exhaustedthem += used
        leftyou -= used
        print("BLAM! They ate",used,"bytes of yours.")
    print("Time to tally!")
    print("You have",leftyou,"bytes left. Don't worry if it's in the negatives! You'll just see the opponent's soon.")
    print("And they have",leftthem,"bytes left!")
    print("Let's see who wins...")
    cur["battlecount"] += 1
    if not leftyou == leftthem:
        if leftthem>leftyou:
            print("You lose...")
        else:
            print("HOORAY! You WIN!")
            cur["won"] += 1
    else:
        print("It's a tie...")

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
            print("Here are your battles:"," ".join(cur["battles"]))
        else:
            print("Welcome to Battle Mode.")
            print("Here you can battle all your opponents.")
            print("Who of all the GitHub land would you like to battle?")
            out = 3.14159265358
            while out != 0:
                tobattle = input()
                out = os.system(f"gh api users/{tobattle} --jq '.login'")
            print("Fetching bytes...")
            bytesa = sum(map(int,api(f"/users/{tobattle}/repos --jq '.[].size'").splitlines()))
            print(tobattle,"has",bytesa,"bytes. Proceed? (Y/n)")
            if input().lower() == "y":
                print("Battling start!")
            else:
                print("Battle denied.")
                break
            battle(sum(map(int,api(f"/users/{uname}/repos --jq '.[].size'").splitlines())),bytesa)
            cur["battles"].append("You vs "+tobattle+"!")
            with open("game.json","w") as f:
                json.dump(cur,f)
            
except (EOFError, KeyboardInterrupt):
    with open("game.json","w") as f:
        json.dump(cur,f)
    print("Goodbye!")
except Exception as e:
    print("A fatal exception in GitWars has occurred:",e)
    with open("game.json","w") as f:
        json.dump(cur,f)
