import random as r
import os

_Exit  = False
_Turn  = r.choice((True, False))
_Table = [0 for _ in range(9)]
cls    = lambda: os.system("cls || clear")

gry = "\033[1;30m"
red = "\033[1;31m"
grn = "\033[1;32m"
end = "\033[0m"


# --- Table edits --- #

def DrawTable(style=None):
    # 0 = win  1 = lose  2 = draw
    cls()
    readableTable = [f"{grn}x{end}" if n == 1 else f"{red}o{end}" if n == 4 else f"{gry}{i}{end}" for i, n in enumerate(_Table)]
    print(f"""
  {readableTable[0]} {grn if style == 0 else red if style == 1 else gry if style == 2 else ''}│{end} {readableTable[1]} {grn if style == 0 else red if style == 1 else gry if style == 2 else ''}│{end} {readableTable[2]}
 {grn if style == 0 else red if style == 1 else gry if style == 2 else ''}───┼───┼───{end}
  {readableTable[3]} {grn if style == 0 else red if style == 1 else gry if style == 2 else ''}│{end} {readableTable[4]} {grn if style == 0 else red if style == 1 else gry if style == 2 else ''}│{end} {readableTable[5]}
 {grn if style == 0 else red if style == 1 else gry if style == 2 else ''}───┼───┼───{end}
  {readableTable[6]} {grn if style == 0 else red if style == 1 else gry if style == 2 else ''}│{end} {readableTable[7]} {grn if style == 0 else red if style == 1 else gry if style == 2 else ''}│{end} {readableTable[8]}
    """)

def PutOnTable(side, place):
    if _Table[place] == 0:
        _Table[place] = side
        return True
    return False


# --- Inside table --- #

def ParseTable():
    return (([_Table[0], _Table[3], _Table[6]], [_Table[1], _Table[4], _Table[7]], [_Table[2], _Table[5], _Table[8]], [_Table[0], _Table[1], _Table[2]], [_Table[3], _Table[4], _Table[5]], [_Table[6], _Table[7], _Table[8]], [_Table[0], _Table[4], _Table[8]], [_Table[2], _Table[4], _Table[6]]), ([0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 4, 8], [2, 4, 6]))

def CheckResult():
    parsedTable = ParseTable()[0]

    # Check for draw.
    try:
        _Table.index(0)

    except:
        DrawTable(2)
        return False

    for part in parsedTable:
        partSum = sum(part)

        # Bot win.
        if partSum == 12:
            DrawTable(1)
            return False

        # Player win.
        elif partSum == 3:
            DrawTable(0)
            return False

    return True


# --- Bot control --- #

def BotHandleTable():
    parsedTable = ParseTable()

    for idx, part in enumerate(parsedTable[0]):
        if sum(part) == 8:
            PutOnTable(4, parsedTable[1][idx][part.index(0)])
            return

    for idx, part in enumerate(parsedTable[0]):
        if sum(part) == 2:
            PutOnTable(4, parsedTable[1][idx][part.index(0)])
            return

    if sum(part) == 1:
        PutOnTable(4, parsedTable[1][idx][part.index(0)])
        return

    else:
        for i in range(0, 9, 2):
            if _Table[i] == 0:
                PutOnTable(4, i)
                return

        else:
            PutOnTable(4, r.choice([idx for idx, e in enumerate(_Table) if e == 0]))
            return


#==== MAIN GAME LOOP ====#
while True:
    if _Exit:
        exit()

    DrawTable()
    _Turn = not _Turn

    # Player turn.
    if _Turn == True:
        while True:
            PlayerChoose = input("Index: ")

            try:
                PlayerChoose = int(PlayerChoose)

                if PlayerChoose in range(0, 10):

                    PlayerPutStatus = PutOnTable(1, PlayerChoose)
                    if PlayerPutStatus == True:
                        if not CheckResult():
                            _Exit = True
                        break

                    else:
                        print(f"{red}[!] This place is holded.\n{end}")
                        continue

                else:
                    print(f"{red}[!] Out of range.\n{end}")
                    continue

            except Exception as e:
                print(f"{red}[!] Not a number.\n{end}")
                continue

    # Bot turn
    if _Turn == False:
        BotHandleTable()
        if not CheckResult():
            _Exit = True

