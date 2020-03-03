def counting(array, number):
    k = 0
    for i in array:
        if i < number:
            k += 2
        if i == number:
            k += 1
    return k

def winning_die(enemy_die):
    Array_of_objects = []
    array = list(set(enemy_die))
    for i in array:
        value1 = counting(enemy_die, i) - len(enemy_die) ** 2
        size1 = i - 1
        value2 = counting(enemy_die, i + 1) - len(enemy_die) ** 2
        size2 = i
        pom1 = [value1, size1]
        pom2 = [value2, size2]
        Array_of_objects.append(pom1)
        Array_of_objects.append(pom2)
    Capacity = sum(enemy_die) - len(enemy_die)
    Amount = len(enemy_die)

    V = []
    Q = []
    pom = []
    for i in range(len(Array_of_objects) + 1):
        row = []
        for j in range(Capacity + 1):
            row.append(-len(enemy_die) ** 2)
        pom.append(row)
    V.append(pom)
    for i in range(Amount):
        pom = [[-len(enemy_die) ** 2] * (Capacity + 1)]
        V.append(pom)

    for i in range(1, Amount + 1):
        SQ = []
        for j in range(1, len(Array_of_objects) + 1):
            rowV = []
            rowQ = []
            for e in range(Capacity + 1):
                if Array_of_objects[j - 1][1] <= e:
                    pomV = max(V[i][j - 1][e],
                               V[i - 1][j][e - Array_of_objects[j - 1][1]] + Array_of_objects[j - 1][0] + len(
                                   enemy_die) ** 2)
                    if pomV == V[i - 1][j][e - Array_of_objects[j - 1][1]] + Array_of_objects[j - 1][0] + len(
                            enemy_die) ** 2:
                        pomQ = 1
                    else:
                        pomQ = 0
                else:
                    pomV = V[i][j - 1][e]
                    pomQ = 0
                rowV.append(pomV)
                rowQ.append(pomQ)
            V[i].append(rowV)
            SQ.append(rowQ)
        Q.append(SQ)

    dice = []
    if V[Amount][len(Array_of_objects)][Capacity] > 0:
        dice = []
        i = Amount - 1
        j = len(Array_of_objects) - 1
        e = Capacity
        while i >= 0 and j >= 0 and e >= 0:
            if Q[i][j][e] == 1:
                dice.append(Array_of_objects[j][1] + 1)
                i -= 1
                e -= Array_of_objects[j][1]
            else:
                j -= 1
        for i in range(len(enemy_die) - len(dice)):
            dice.append(1)
        p = sum(enemy_die) - sum(dice)
        dice[0] += p
        dice.sort()
    print(dice)
    return dice


if __name__ == '__main__':
    # These are only used for self-checking and not necessary for auto-testing
    def check_solution(func, enemy):
        player = func(enemy)
        total = 0
        for p in player:
            for e in enemy:
                if p > e:
                    total += 1
                elif p < e:
                    total -= 1
        return total > 0


    assert check_solution(winning_die, [3, 3, 3, 3, 6, 6]), "Threes and Sixes"
    assert check_solution(winning_die, [4, 4, 4, 4, 4, 4]), "All Fours"
    assert check_solution(winning_die, [1, 1, 1, 4]), "Unities and Four"
    assert winning_die([1, 2, 3, 4, 5, 6]) == [], "All in row -- No die"