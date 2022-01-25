import glob
import random

files = glob.glob(
    r"C:\Users\owner\Desktop\python\poker data preprocessing\output\out.txt")
# 前処理したゲームデータの読み取り
with open(files[0]) as fi:
    game = []
    showdown = True
    data = []
    while True:
        line = fi.readline()

        if 'starts' in line:
            if game:
                data.append(game)
            game = []

        if not line == '\n':
            game.append(line.strip())
        if not line:
            break

n = 1
for game in data:
    i = random.randint(0, len(data)-1)
    print("Game " + str(n) + ".")

    for line in data[i]:
        if 'wins' in line:
            position = line.split(' ')[0]

    print("You are " + position + ".")

    for line in data[i]:
        if position + " shows" in line:
            hand = line.split(' ')[3] + " " + line.split(' ')[4]

    print("Your hand is [" + hand + "].")

    act_dict = {1: "bets", 2: "checks", 3: "calls",
                4: "raises", 5: "all-In", 6: "folds"}

    start = False
    board = ""

    for line in data[i]:
        if "Hand History for Game" in line:
            start = True

        if start:
            if "Flop" in line:
                board = line.split(' ')[5] + " " + \
                    line.split(' ')[6] + " " + line.split(' ')[7]
            if ("Turn" in line) or ("River" in line):
                board = board + ", " + line.split(' ')[5]

            if position in line:
                if ("bets" in line) or ("checks" in line) or ("calls" in line) or ("raises" in line) or ("all-In" in line):
                    if board != "":
                        print("Your hand is [" + hand +
                              "]. Board is [" + board + "].")
                    act = eval(
                        input('Choose your action. 1: Bet 2:Check 3:Call 4:Raise 5:All-In 6:Fold=>'))
                    if act_dict[act] in line:
                        print("Collect!")
                    else:
                        print("Incollect...")
            print(line)

    input("Next:Enter. End:Ctrl+C.")
    n += 1
