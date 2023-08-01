from sudokuClass import *


def getPossibleSwitches(amount_numbers_given, amount_numbers_variant):
    possible_switches = []
    if amount_numbers_given == amount_numbers_variant:
        possible_switches += [[]]
    for elm_given in range(3):
        for elm_variant in range(elm_given + 1, 3):
            if amount_numbers_given[elm_given] == amount_numbers_variant[elm_variant]:
                new_given = amount_numbers_given[:]
                new_given[elm_given], new_given[elm_variant] = new_given[elm_variant], new_given[elm_given]
                change = [elm_given, elm_variant]
                if new_given == amount_numbers_variant:
                    possible_switches += [[change]]
                third = [x for x in [0, 1, 2] if x not in change]
                for i in change:
                    if new_given[third[0]] == new_given[i] or new_given[third[0]] == amount_numbers_variant[i] and new_given[i] == amount_numbers_variant[third[0]]:
                        possible_switches += [[change, [third[0], i]]]
    return possible_switches


def getSolution(filename: str):
    # liest die angegebene Datei aus und transformiert sie in ein Sudoku Objekt
    sudokuInLines1, sudokuInLines2 = [], []
    with open(filename, 'r', encoding='utf-8-sig') as file:
        myLines = [line for line in file]
        for x in range(9):
            sudokuInLines1.append((myLines[x].split()))
        for x in range(10, 19):
            sudokuInLines2.append((myLines[x].split()))

    sudokuInLines1 = [[int(x) for x in y] for y in sudokuInLines1]
    sudokuInLines2 = [[int(x) for x in y] for y in sudokuInLines2]
    given_sudoku = Sudoku(sudokuInLines1)
    sudoku_variant = Sudoku(sudokuInLines2)
    # dreht das Sudoku um 90°, da andere Drehungen auch durch Zeilen-/Spaltenblock Tausche erreichbar sind
    my_sudokus = [given_sudoku, Sudoku(given_sudoku.turn_90_degree())]
    # prüft, wie das Umformen des Ursprungssudokus und 90° in die Variante möglich ist
    for sudoku_leaf in my_sudokus:
        ############################################################
        # Zeilenblock
        # possible Switches, wahrscheinlichste zuerst
        # findet anhand der Anzahl an vorgegebenen Zahlen pro Zeile heraus, velche Zeilenblöcke vertauscht werden können
        zeilenbloecke_amount_numbers_given = [sorted(get_amount_numbers_in_block(sudoku_leaf.get_zeilen_block(i))) for i in range(3)]
        zeilenbloecke_amount_numbers_variant = [sorted(get_amount_numbers_in_block(sudoku_variant.get_zeilen_block(i))) for i in range(3)]
        possible_zeilenblock_switches = getPossibleSwitches(zeilenbloecke_amount_numbers_given, zeilenbloecke_amount_numbers_variant)
        # führt einen möglichen Tausch durch und macht weiter
        # wenn der gewählte Tausch nicht funktioniert, macht mit dem nächsten in possible_zeilenblock_switches weiter
        for switches in possible_zeilenblock_switches:
            applied_switches = Sudoku(copy.deepcopy(sudoku_leaf.zeilen))
            for switch in switches:
                applied_switches = Sudoku(applied_switches.switch_zeilen_block(switch[0], switch[1]))
            # go on with applied_switches
            ############################################################
            # Spaltenblock
            # possible Switches, wahrscheinlichste zuerst
            # macht dasselbe für die möglichen Spaltenblock Tausche
            spaltenbloecke_amount_numbers_given = [sorted(get_amount_numbers_in_block(applied_switches.get_spalten_block(i))) for i in range(3)]
            spaltenbloecke_amount_numbers_variant = [sorted(get_amount_numbers_in_block(sudoku_variant.get_spalten_block(i))) for i in range(3)]
            possible_spaltenblock_switches = getPossibleSwitches(spaltenbloecke_amount_numbers_given, spaltenbloecke_amount_numbers_variant)
            for switches2 in possible_spaltenblock_switches:
                applied_switches2 = Sudoku(copy.deepcopy(applied_switches.zeilen))
                for switch in switches2:
                    applied_switches2 = Sudoku(applied_switches2.switch_spalten_block(switch[0], switch[1]))
                # go on with applied_switches2
                ############################################################
                # Zeilen
                # possible Switches, wahrscheinlichste zuerst
                # macht das selbe für alle möglichen Zeilen Tausche
                all_zeilen_switches = []
                for zeilen_block in range(3):
                    amount_numbers_in_part_line_given = [[] for x in range(3)]
                    amount_numbers_in_part_line_variant = [[] for x in range(3)]
                    for zeile in range(3):
                        zeile_given = applied_switches2.get_zeile(zeilen_block * 3 + zeile)
                        zeile_variant = sudoku_variant.get_zeile(zeilen_block * 3 + zeile)
                        for spalten_block in range(3):
                            amount_numbers_in_part_line_given[zeile] += [get_amount_numbers(zeile_given[spalten_block * 3: spalten_block * 3 + 3])]
                            amount_numbers_in_part_line_variant[zeile] += [get_amount_numbers(zeile_variant[spalten_block * 3: spalten_block * 3 + 3])]
                    possible_zeilen_switches = getPossibleSwitches(amount_numbers_in_part_line_given, amount_numbers_in_part_line_variant)
                    if (possible_zeilen_switches == []):  # if no switch is able to archieve the variant, dont go on with applied_switches2
                        break
                    all_zeilen_switches += [possible_zeilen_switches]
                else:
                    final_all_zeilen_switches = []
                    # [0, 0, 0], [1, 0, 0], [n, 0, 0]
                    for a in all_zeilen_switches[0]:
                        for b in all_zeilen_switches[1]:
                            for c in all_zeilen_switches[2]:
                                final_all_zeilen_switches += [[a, b, c]]
                    for switches3 in final_all_zeilen_switches:
                        applied_switches3 = Sudoku(copy.deepcopy(applied_switches2.zeilen))
                        for i, line in enumerate(switches3):
                            for switch in line:
                                applied_switches3 = Sudoku(applied_switches3.switch_zeilen(switch[0] + i * 3, switch[1] + i * 3))
                        # go on with applied_switches3
                        ############################################################
                        # Spalten
                        # possible Switches, wahrscheinlichste zuerst
                        # macht das selbe für alle möglichen Spalten Tausche
                        all_spalten_switches = []
                        for spalten_block in range(3):
                            amount_numbers_in_part_spalten_given = [[] for x in range(3)]
                            amount_numbers_in_part_spalten_variant = [[] for x in range(3)]
                            for spalte in range(3):
                                spalte_given = applied_switches2.get_spalte(spalten_block * 3 + spalte)
                                spalte_variant = sudoku_variant.get_spalte(spalten_block * 3 + spalte)
                                for zeilen_block in range(3):
                                    amount_numbers_in_part_spalten_given[spalte] += [get_amount_numbers(spalte_given[zeilen_block * 3: zeilen_block * 3 + 3])]
                                    amount_numbers_in_part_spalten_variant[spalte] += [get_amount_numbers(spalte_variant[zeilen_block * 3: zeilen_block * 3 + 3])]
                            possible_spalten_switches = getPossibleSwitches(amount_numbers_in_part_spalten_given, amount_numbers_in_part_spalten_variant)
                            if (possible_spalten_switches == []):  # if no switch is able to archieve the variant, dont go on with applied_switches2
                                break
                            all_spalten_switches += [possible_spalten_switches]
                        else:
                            final_all_spalten_switches = []
                            # [0, 0, 0], [1, 0, 0], [n, 0, 0]
                            for a in all_spalten_switches[0]:
                                for b in all_spalten_switches[1]:
                                    for c in all_spalten_switches[2]:
                                        final_all_spalten_switches += [[a, b, c]]
                            for switches4 in final_all_spalten_switches:
                                applied_switches4 = Sudoku(copy.deepcopy(applied_switches3.zeilen))
                                for i, spalten in enumerate(switches4):
                                    for switch in spalten:
                                        applied_switches4 = Sudoku(applied_switches4.switch_spalten(switch[0] + i * 3, switch[1] + i * 3))
                                # go on with applied_switches4
                                ############################################################
                                # Nummern
                                positions_given = []
                                positions_variant = []
                                # Prüft ob die Positionen der vorgegebenen Zahlen im geänderten Sudoku die selben wie in der Sudoku Variante sind
                                for i in range(9):
                                    positions_given += [[get_position_numbers(applied_switches4.get_zeile(i))]]
                                    positions_variant += [[get_position_numbers(sudoku_variant.get_zeile(i))]]
                                # Falls ja, werden die Nummern so vertauscht, dass sie der Sudoku Variante entsprechen
                                # Falls das nicht möglich ist, wird das mit den restlichen Spalten Tauschen, dann den restlichen
                                # Zeilen Tauschen, dann den restlichen Spaltenblock und dann den reastlichen Zeilenblock Tauschen ausprobiert.
                                # klappt das alles nicht, beginnt der Vorgang erneut mit dem um 90° gedrehten Sudoku
                                if (positions_given == positions_variant):
                                    print(f"Zeilenblock Tausch: {switches}")
                                    print(f"Spaltenblock Tausch: {switches2}")
                                    print(f"Zeilen Tausch: {switches3}")
                                    print(f"Spalten Tausch: {switches4}")
                                    final_Sudoku = copy.deepcopy(applied_switches4.zeilen)
                                    for n in range(1, 10):
                                        # switch numbers
                                        for i in range(9):
                                            for j in range(9):
                                                if applied_switches4.zeilen[i][j] == n:
                                                    replacement = sudoku_variant.zeilen[i][j]
                                                    if n != replacement:
                                                        print(f"{applied_switches4.zeilen[i][j]} -> {replacement}")
                                                        for h in range(0, 9):
                                                            for g in range(0, 9):
                                                                if applied_switches4.zeilen[h][g] == n:
                                                                    final_Sudoku[h][g] = replacement
                                                    break
                                            else:
                                                continue
                                            break
                                    if final_Sudoku == sudoku_variant.zeilen:
                                        print("\n")
                                        given_sudoku.print()
                                        sudoku_variant.print()
                                        return True
        print("turn 90 degree left")
    print("not possible")


if __name__ == "__main__":
    for i in range(5):
        print("________________________________")
        print(i)
        getSolution(f"sudoku{i}.txt")