import os
if os.system("gh") != 0:
    print("Install GitHub CLI and log in for this game to work.")
    exit( 1 )

print("GitHub Wars")
