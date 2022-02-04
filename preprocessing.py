import re
import glob

files = glob.glob(
    r"C:\Users\owner\Desktop\python\practice poker\data\*")

for file in files:
    with open(file) as fi:
        game = []
        showdown = False
        data = []
        while True:
            line = fi.readline()

            if 'starts' in line:
                # ショーダウンまで行ったゲームのみ書き込み
                if showdown:
                    game.append('\n\n')
                    data.append(game)

                # 次のゲーム
                game = []
                showdown = False

            if not line == '\n':
                if 'shows' in line:
                    showdown = True

                game.append(line)
            if not line:
                break


class Preprocessing:
    def __init__(self, data):
        self.data = data
        self.add_ID_and_Stack()
        self.addPosition()
        self.replaceID()

    def add_ID_and_Stack(self):
        self.player_count = 0
        self.player_dict = {}
        self.player_num_list = []
        self.button = 0

        for text in self.data:
            if 'Seat' in text:
                if 'is the button' in text:
                    self.button = int(re.findall(r'\d+', text)[0])

                if self.player_count != 0:
                    info = {}
                    player_num = int(re.findall(r'\d+', text.split(' ')[1])[0])
                    info['id'] = text.split(' ')[2]
                    info['stack'] = text.split(' ')[4]
                    self.player_dict[player_num] = info

                    self.player_num_list.append(player_num)

            if 'Total number of players' in text:
                self.player_count = int(re.findall(r'\d+', text)[0])

            # 離席したプレイヤーを除く
            if 'left the table' in text:
                ID = text.split()[0]
                for i in self.player_dict:
                    if self.player_dict[i]['id'] == ID:
                        self.player_num_list.remove(i)
                        self.player_dict.pop(i)
                        self.player_count -= 1
                        break

        self.player_num_list.sort()

    def addPosition(self):
        # 各プレイヤーのポジション判定
        player_dict = self.player_dict
        player_num_list = self.player_num_list
        button = self.button
        idx = player_num_list.index(button)

        if self.player_count == 2:
            player_dict[button]['position'] = 'BTN'
            # [1, 2]  button = 2
            if idx == 1:
                player_dict[player_num_list[idx - 1]]['position'] = 'BB'
            # [1, 2]  button = 1
            else:
                player_dict[player_num_list[idx + 1]]['position'] = 'BB'

        elif self.player_count == 3:
            player_dict[button]['position'] = 'BTN'
            # [1, 2, 3]  button = 3
            if idx == 2:
                player_dict[player_num_list[idx - 2]]['position'] = 'SB'
                player_dict[player_num_list[idx - 1]]['position'] = 'BB'
            # [1, 2, 3]  button = 2
            elif idx == 1:
                player_dict[player_num_list[idx + 1]]['position'] = 'SB'
                player_dict[player_num_list[idx - 1]]['position'] = 'BB'
            # [1, 2, 3]  button = 1
            else:
                player_dict[player_num_list[idx + 1]]['position'] = 'SB'
                player_dict[player_num_list[idx + 2]]['position'] = 'BB'

        elif self.player_count == 4:
            player_dict[button]['position'] = 'BTN'
            # [1, 2, 3, 4]  button = 4
            if idx == 3:
                player_dict[player_num_list[idx - 3]]['position'] = 'SB'
                player_dict[player_num_list[idx - 2]]['position'] = 'BB'
                player_dict[player_num_list[idx - 1]]['position'] = 'CO'
            # [1, 2, 3, 4]  button = 3
            elif idx == 2:
                player_dict[player_num_list[idx + 1]]['position'] = 'SB'
                player_dict[player_num_list[idx - 2]]['position'] = 'BB'
                player_dict[player_num_list[idx - 1]]['position'] = 'CO'
            # [1, 2, 3, 4]  button = 2
            elif idx == 1:
                player_dict[player_num_list[idx + 1]]['position'] = 'SB'
                player_dict[player_num_list[idx + 2]]['position'] = 'BB'
                player_dict[player_num_list[idx - 1]]['position'] = 'CO'
            # [1, 2, 3, 4]  button = 1
            else:
                player_dict[player_num_list[idx + 1]]['position'] = 'SB'
                player_dict[player_num_list[idx + 2]]['position'] = 'BB'
                player_dict[player_num_list[idx + 3]]['position'] = 'CO'

        elif self.player_count == 5:
            player_dict[button]['position'] = 'BTN'
            # [1, 2, 3, 4, 5]  button = 5
            if idx == 4:
                player_dict[player_num_list[idx - 4]]['position'] = 'SB'
                player_dict[player_num_list[idx - 3]]['position'] = 'BB'
                player_dict[player_num_list[idx - 2]]['position'] = 'UTG'
                player_dict[player_num_list[idx - 1]]['position'] = 'CO'
            # [1, 2, 3, 4, 5]  button = 4
            elif idx == 3:
                player_dict[player_num_list[idx + 1]]['position'] = 'SB'
                player_dict[player_num_list[idx - 3]]['position'] = 'BB'
                player_dict[player_num_list[idx - 2]]['position'] = 'UTG'
                player_dict[player_num_list[idx - 1]]['position'] = 'CO'
            # [1, 2, 3, 4, 5]  button = 3
            elif idx == 2:
                player_dict[player_num_list[idx + 1]]['position'] = 'SB'
                player_dict[player_num_list[idx + 2]]['position'] = 'BB'
                player_dict[player_num_list[idx - 2]]['position'] = 'UTG'
                player_dict[player_num_list[idx - 1]]['position'] = 'CO'
            # [1, 2, 3, 4, 5]  button = 2
            elif idx == 1:
                player_dict[player_num_list[idx + 1]]['position'] = 'SB'
                player_dict[player_num_list[idx + 2]]['position'] = 'BB'
                player_dict[player_num_list[idx + 3]]['position'] = 'UTG'
                player_dict[player_num_list[idx - 1]]['position'] = 'CO'
            # [1, 2, 3, 4, 5]  button = 1
            else:
                player_dict[player_num_list[idx + 1]]['position'] = 'SB'
                player_dict[player_num_list[idx + 2]]['position'] = 'BB'
                player_dict[player_num_list[idx + 3]]['position'] = 'UTG'
                player_dict[player_num_list[idx + 4]]['position'] = 'CO'

        elif self.player_count == 6:
            player_dict[button]['position'] = 'BTN'
            # [1, 2, 3, 4, 5, 6]  button = 6
            if idx == 5:
                player_dict[player_num_list[idx - 5]]['position'] = 'SB'
                player_dict[player_num_list[idx - 4]]['position'] = 'BB'
                player_dict[player_num_list[idx - 3]]['position'] = 'UTG'
                player_dict[player_num_list[idx - 2]]['position'] = 'HJ'
                player_dict[player_num_list[idx - 1]]['position'] = 'CO'
            # [1, 2, 3, 4, 5, 6]  button = 5
            elif idx == 4:
                player_dict[player_num_list[idx + 1]]['position'] = 'SB'
                player_dict[player_num_list[idx - 4]]['position'] = 'BB'
                player_dict[player_num_list[idx - 3]]['position'] = 'UTG'
                player_dict[player_num_list[idx - 2]]['position'] = 'HJ'
                player_dict[player_num_list[idx - 1]]['position'] = 'CO'
            # [1, 2, 3, 4, 5, 6]  button = 4
            elif idx == 3:
                player_dict[player_num_list[idx + 1]]['position'] = 'SB'
                player_dict[player_num_list[idx + 2]]['position'] = 'BB'
                player_dict[player_num_list[idx - 3]]['position'] = 'UTG'
                player_dict[player_num_list[idx - 2]]['position'] = 'HJ'
                player_dict[player_num_list[idx - 1]]['position'] = 'CO'
            # [1, 2, 3, 4, 5, 6]  button = 3
            elif idx == 2:
                player_dict[player_num_list[idx + 1]]['position'] = 'SB'
                player_dict[player_num_list[idx + 2]]['position'] = 'BB'
                player_dict[player_num_list[idx + 3]]['position'] = 'UTG'
                player_dict[player_num_list[idx - 2]]['position'] = 'HJ'
                player_dict[player_num_list[idx - 1]]['position'] = 'CO'
            # [1, 2, 3, 4, 5, 6]  button = 2
            elif idx == 1:
                player_dict[player_num_list[idx + 1]]['position'] = 'SB'
                player_dict[player_num_list[idx + 2]]['position'] = 'BB'
                player_dict[player_num_list[idx + 3]]['position'] = 'UTG'
                player_dict[player_num_list[idx + 4]]['position'] = 'HJ'
                player_dict[player_num_list[idx - 1]]['position'] = 'CO'
            # [1, 2, 3, 4, 5, 6]  button = 1
            else:
                player_dict[player_num_list[idx + 1]]['position'] = 'SB'
                player_dict[player_num_list[idx + 2]]['position'] = 'BB'
                player_dict[player_num_list[idx + 3]]['position'] = 'UTG'
                player_dict[player_num_list[idx + 4]]['position'] = 'HJ'
                player_dict[player_num_list[idx + 5]]['position'] = 'CO'

        elif self.player_count == 7:
            player_dict[button]['position'] = 'BTN'
            # [1, 2, 3, 4, 5, 6, 7]  button = 7
            if idx == 6:
                player_dict[player_num_list[idx - 6]]['position'] = 'SB'
                player_dict[player_num_list[idx - 5]]['position'] = 'BB'
                player_dict[player_num_list[idx - 4]]['position'] = 'UTG'
                player_dict[player_num_list[idx - 3]]['position'] = 'LJ'
                player_dict[player_num_list[idx - 2]]['position'] = 'HJ'
                player_dict[player_num_list[idx - 1]]['position'] = 'CO'
            # [1, 2, 3, 4, 5, 6, 7]  button = 6
            elif idx == 5:
                player_dict[player_num_list[idx + 1]]['position'] = 'SB'
                player_dict[player_num_list[idx - 5]]['position'] = 'BB'
                player_dict[player_num_list[idx - 4]]['position'] = 'UTG'
                player_dict[player_num_list[idx - 3]]['position'] = 'LJ'
                player_dict[player_num_list[idx - 2]]['position'] = 'HJ'
                player_dict[player_num_list[idx - 1]]['position'] = 'CO'
            # [1, 2, 3, 4, 5, 6, 7]  button = 5
            elif idx == 4:
                player_dict[player_num_list[idx + 1]]['position'] = 'SB'
                player_dict[player_num_list[idx + 2]]['position'] = 'BB'
                player_dict[player_num_list[idx - 4]]['position'] = 'UTG'
                player_dict[player_num_list[idx - 3]]['position'] = 'LJ'
                player_dict[player_num_list[idx - 2]]['position'] = 'HJ'
                player_dict[player_num_list[idx - 1]]['position'] = 'CO'
            # [1, 2, 3, 4, 5, 6, 7]  button = 4
            elif idx == 3:
                player_dict[player_num_list[idx + 1]]['position'] = 'SB'
                player_dict[player_num_list[idx + 2]]['position'] = 'BB'
                player_dict[player_num_list[idx + 3]]['position'] = 'UTG'
                player_dict[player_num_list[idx - 3]]['position'] = 'LJ'
                player_dict[player_num_list[idx - 2]]['position'] = 'HJ'
                player_dict[player_num_list[idx - 1]]['position'] = 'CO'
            # [1, 2, 3, 4, 5, 6, 7]  button = 3
            elif idx == 2:
                player_dict[player_num_list[idx + 1]]['position'] = 'SB'
                player_dict[player_num_list[idx + 2]]['position'] = 'BB'
                player_dict[player_num_list[idx + 3]]['position'] = 'UTG'
                player_dict[player_num_list[idx + 4]]['position'] = 'LJ'
                player_dict[player_num_list[idx - 2]]['position'] = 'HJ'
                player_dict[player_num_list[idx - 1]]['position'] = 'CO'
            # [1, 2, 3, 4, 5, 6, 7]  button = 2
            elif idx == 1:
                player_dict[player_num_list[idx + 1]]['position'] = 'SB'
                player_dict[player_num_list[idx + 2]]['position'] = 'BB'
                player_dict[player_num_list[idx + 3]]['position'] = 'UTG'
                player_dict[player_num_list[idx + 4]]['position'] = 'LJ'
                player_dict[player_num_list[idx + 5]]['position'] = 'HJ'
                player_dict[player_num_list[idx - 1]]['position'] = 'CO'
            # [1, 2, 3, 4, 5, 6, 7]  button = 1
            else:
                player_dict[player_num_list[idx + 1]]['position'] = 'SB'
                player_dict[player_num_list[idx + 2]]['position'] = 'BB'
                player_dict[player_num_list[idx + 3]]['position'] = 'UTG'
                player_dict[player_num_list[idx + 4]]['position'] = 'LJ'
                player_dict[player_num_list[idx + 5]]['position'] = 'HJ'
                player_dict[player_num_list[idx + 6]]['position'] = 'CO'

        elif self.player_count == 8:
            player_dict[button]['position'] = 'BTN'
            # [1, 2, 3, 4, 5, 6, 7, 8]  button = 8
            if idx == 7:
                player_dict[player_num_list[idx - 7]]['position'] = 'SB'
                player_dict[player_num_list[idx - 6]]['position'] = 'BB'
                player_dict[player_num_list[idx - 5]]['position'] = 'UTG'
                player_dict[player_num_list[idx - 4]]['position'] = 'UTG+1'
                player_dict[player_num_list[idx - 3]]['position'] = 'LJ'
                player_dict[player_num_list[idx - 2]]['position'] = 'HJ'
                player_dict[player_num_list[idx - 1]]['position'] = 'CO'
            # [1, 2, 3, 4, 5, 6, 7, 8]  button = 7
            elif idx == 6:
                player_dict[player_num_list[idx + 1]]['position'] = 'SB'
                player_dict[player_num_list[idx - 6]]['position'] = 'BB'
                player_dict[player_num_list[idx - 5]]['position'] = 'UTG'
                player_dict[player_num_list[idx - 4]]['position'] = 'UTG+1'
                player_dict[player_num_list[idx - 3]]['position'] = 'LJ'
                player_dict[player_num_list[idx - 2]]['position'] = 'HJ'
                player_dict[player_num_list[idx - 1]]['position'] = 'CO'
            # [1, 2, 3, 4, 5, 6, 7, 8]  button = 6
            elif idx == 5:
                player_dict[player_num_list[idx + 1]]['position'] = 'SB'
                player_dict[player_num_list[idx + 2]]['position'] = 'BB'
                player_dict[player_num_list[idx - 5]]['position'] = 'UTG'
                player_dict[player_num_list[idx - 4]]['position'] = 'UTG+1'
                player_dict[player_num_list[idx - 3]]['position'] = 'LJ'
                player_dict[player_num_list[idx - 2]]['position'] = 'HJ'
                player_dict[player_num_list[idx - 1]]['position'] = 'CO'
            # [1, 2, 3, 4, 5, 6, 7, 8]  button = 5
            elif idx == 4:
                player_dict[player_num_list[idx + 1]]['position'] = 'SB'
                player_dict[player_num_list[idx + 2]]['position'] = 'BB'
                player_dict[player_num_list[idx + 3]]['position'] = 'UTG'
                player_dict[player_num_list[idx - 4]]['position'] = 'UTG+1'
                player_dict[player_num_list[idx - 3]]['position'] = 'LJ'
                player_dict[player_num_list[idx - 2]]['position'] = 'HJ'
                player_dict[player_num_list[idx - 1]]['position'] = 'CO'
            # [1, 2, 3, 4, 5, 6, 7, 8]  button = 4
            elif idx == 3:
                player_dict[player_num_list[idx + 1]]['position'] = 'SB'
                player_dict[player_num_list[idx + 2]]['position'] = 'BB'
                player_dict[player_num_list[idx + 3]]['position'] = 'UTG'
                player_dict[player_num_list[idx + 4]]['position'] = 'UTG+1'
                player_dict[player_num_list[idx - 3]]['position'] = 'LJ'
                player_dict[player_num_list[idx - 2]]['position'] = 'HJ'
                player_dict[player_num_list[idx - 1]]['position'] = 'CO'
            # [1, 2, 3, 4, 5, 6, 7, 8]  button = 3
            elif idx == 2:
                player_dict[player_num_list[idx + 1]]['position'] = 'SB'
                player_dict[player_num_list[idx + 2]]['position'] = 'BB'
                player_dict[player_num_list[idx + 3]]['position'] = 'UTG'
                player_dict[player_num_list[idx + 4]]['position'] = 'UTG+1'
                player_dict[player_num_list[idx + 5]]['position'] = 'LJ'
                player_dict[player_num_list[idx - 2]]['position'] = 'HJ'
                player_dict[player_num_list[idx - 1]]['position'] = 'CO'
            # [1, 2, 3, 4, 5, 6, 7, 8]  button = 2
            elif idx == 1:
                player_dict[player_num_list[idx + 1]]['position'] = 'SB'
                player_dict[player_num_list[idx + 2]]['position'] = 'BB'
                player_dict[player_num_list[idx + 3]]['position'] = 'UTG'
                player_dict[player_num_list[idx + 4]]['position'] = 'UTG+1'
                player_dict[player_num_list[idx + 5]]['position'] = 'LJ'
                player_dict[player_num_list[idx + 6]]['position'] = 'HJ'
                player_dict[player_num_list[idx - 1]]['position'] = 'CO'
            # [1, 2, 3, 4, 5, 6, 7, 8]  button = 1
            else:
                player_dict[player_num_list[idx + 1]]['position'] = 'SB'
                player_dict[player_num_list[idx + 2]]['position'] = 'BB'
                player_dict[player_num_list[idx + 3]]['position'] = 'UTG'
                player_dict[player_num_list[idx + 4]]['position'] = 'UTG+1'
                player_dict[player_num_list[idx + 5]]['position'] = 'LJ'
                player_dict[player_num_list[idx + 6]]['position'] = 'HJ'
                player_dict[player_num_list[idx + 7]]['position'] = 'CO'

        elif self.player_count == 9:
            player_dict[button]['position'] = 'BTN'
            if idx == 8:
                player_dict[player_num_list[idx - 8]]['position'] = 'SB'
                player_dict[player_num_list[idx - 7]]['position'] = 'BB'
                player_dict[player_num_list[idx - 6]]['position'] = 'UTG'
                player_dict[player_num_list[idx - 5]]['position'] = 'UTG+1'
                player_dict[player_num_list[idx - 4]]['position'] = 'UTG+2'
                player_dict[player_num_list[idx - 3]]['position'] = 'LJ'
                player_dict[player_num_list[idx - 2]]['position'] = 'HJ'
                player_dict[player_num_list[idx - 1]]['position'] = 'CO'
            elif idx == 7:
                player_dict[player_num_list[idx + 1]]['position'] = 'SB'
                player_dict[player_num_list[idx - 7]]['position'] = 'BB'
                player_dict[player_num_list[idx - 6]]['position'] = 'UTG'
                player_dict[player_num_list[idx - 5]]['position'] = 'UTG+1'
                player_dict[player_num_list[idx - 4]]['position'] = 'UTG+2'
                player_dict[player_num_list[idx - 3]]['position'] = 'LJ'
                player_dict[player_num_list[idx - 2]]['position'] = 'HJ'
                player_dict[player_num_list[idx - 1]]['position'] = 'CO'
            elif idx == 6:
                player_dict[player_num_list[idx + 1]]['position'] = 'SB'
                player_dict[player_num_list[idx + 2]]['position'] = 'BB'
                player_dict[player_num_list[idx - 6]]['position'] = 'UTG'
                player_dict[player_num_list[idx - 5]]['position'] = 'UTG+1'
                player_dict[player_num_list[idx - 4]]['position'] = 'UTG+2'
                player_dict[player_num_list[idx - 3]]['position'] = 'LJ'
                player_dict[player_num_list[idx - 2]]['position'] = 'HJ'
                player_dict[player_num_list[idx - 1]]['position'] = 'CO'
            elif idx == 5:
                player_dict[player_num_list[idx + 1]]['position'] = 'SB'
                player_dict[player_num_list[idx + 2]]['position'] = 'BB'
                player_dict[player_num_list[idx + 3]]['position'] = 'UTG'
                player_dict[player_num_list[idx - 5]]['position'] = 'UTG+1'
                player_dict[player_num_list[idx - 4]]['position'] = 'UTG+2'
                player_dict[player_num_list[idx - 3]]['position'] = 'LJ'
                player_dict[player_num_list[idx - 2]]['position'] = 'HJ'
                player_dict[player_num_list[idx - 1]]['position'] = 'CO'
            elif idx == 4:
                player_dict[player_num_list[idx + 1]]['position'] = 'SB'
                player_dict[player_num_list[idx + 2]]['position'] = 'BB'
                player_dict[player_num_list[idx + 3]]['position'] = 'UTG'
                player_dict[player_num_list[idx + 4]]['position'] = 'UTG+1'
                player_dict[player_num_list[idx - 4]]['position'] = 'UTG+2'
                player_dict[player_num_list[idx - 3]]['position'] = 'LJ'
                player_dict[player_num_list[idx - 2]]['position'] = 'HJ'
                player_dict[player_num_list[idx - 1]]['position'] = 'CO'
            elif idx == 3:
                player_dict[player_num_list[idx + 1]]['position'] = 'SB'
                player_dict[player_num_list[idx + 2]]['position'] = 'BB'
                player_dict[player_num_list[idx + 3]]['position'] = 'UTG'
                player_dict[player_num_list[idx + 4]]['position'] = 'UTG+1'
                player_dict[player_num_list[idx + 5]]['position'] = 'UTG+2'
                player_dict[player_num_list[idx - 3]]['position'] = 'LJ'
                player_dict[player_num_list[idx - 2]]['position'] = 'HJ'
                player_dict[player_num_list[idx - 1]]['position'] = 'CO'
            elif idx == 2:
                player_dict[player_num_list[idx + 1]]['position'] = 'SB'
                player_dict[player_num_list[idx + 2]]['position'] = 'BB'
                player_dict[player_num_list[idx + 3]]['position'] = 'UTG'
                player_dict[player_num_list[idx + 4]]['position'] = 'UTG+1'
                player_dict[player_num_list[idx + 5]]['position'] = 'UTG+2'
                player_dict[player_num_list[idx + 6]]['position'] = 'LJ'
                player_dict[player_num_list[idx - 2]]['position'] = 'HJ'
                player_dict[player_num_list[idx - 1]]['position'] = 'CO'
            elif idx == 1:
                player_dict[player_num_list[idx + 1]]['position'] = 'SB'
                player_dict[player_num_list[idx + 2]]['position'] = 'BB'
                player_dict[player_num_list[idx + 3]]['position'] = 'UTG'
                player_dict[player_num_list[idx + 4]]['position'] = 'UTG+1'
                player_dict[player_num_list[idx + 5]]['position'] = 'UTG+2'
                player_dict[player_num_list[idx + 6]]['position'] = 'LJ'
                player_dict[player_num_list[idx + 7]]['position'] = 'HJ'
                player_dict[player_num_list[idx - 1]]['position'] = 'CO'
            else:
                player_dict[player_num_list[idx + 1]]['position'] = 'SB'
                player_dict[player_num_list[idx + 2]]['position'] = 'BB'
                player_dict[player_num_list[idx + 3]]['position'] = 'UTG'
                player_dict[player_num_list[idx + 4]]['position'] = 'UTG+1'
                player_dict[player_num_list[idx + 5]]['position'] = 'UTG+2'
                player_dict[player_num_list[idx + 6]]['position'] = 'LJ'
                player_dict[player_num_list[idx + 7]]['position'] = 'HJ'
                player_dict[player_num_list[idx + 8]]['position'] = 'CO'

        self.player_dict = player_dict

    def replaceID(self):
        # id検索し、ポジション名に置換する
        copy = self.data
        for key in self.player_dict.keys():
            for text in copy:
                if self.player_dict[key]['id'] in text:
                    copy[copy.index(text)] = text.replace(
                        self.player_dict[key]['id'], self.player_dict[key]['position'])
        self.copy = copy


with open(r'C:\Users\owner\Desktop\python\practice poker\output\out.txt', mode='w') as fo:
    for game in data:
        p = Preprocessing(game)
        for line in game:
            fo.write(line)
