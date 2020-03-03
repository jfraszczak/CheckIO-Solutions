class Unit:
    def __init__(self, row, column, wins, losses):
        self.row = row
        self.column = column
        self.wins = wins
        self.losses = losses
        self.district = None

class Map:
    def __init__(self, rows, columns, map):
        self.grid = []
        self.rows = rows
        self.columns = columns
        self.nextDistrict = 'A'
        for row in range(rows):
            tmpRow = []
            for column in range(columns):
                unit = Unit(row, column, map[row][column][0], map[row][column][1])
                tmpRow.append(unit)
            self.grid.append(tmpRow)

    def nextFreeUnit(self):
        for row in range(self.rows):
            for column in range(self.columns):
                if self.grid[row][column].district is None:
                    return self.grid[row][column]
        return -1

    def unitInArray(self, unit, array):
        for arrayUnit in array:
            if arrayUnit.row == unit.row and arrayUnit.column == unit.column:
                return True
        return False

    def findAdjacent(self, units):
        adjacentUnits = []
        for unit in units:
            topRow = unit.row - 1
            bottomRow = unit.row + 1
            leftCol = unit.column - 1
            rightCol = unit.column + 1
            if leftCol >= 0:
                if not self.unitInArray(self.grid[unit.row][leftCol], units) and self.grid[unit.row][leftCol].district is None:
                    adjacentUnits.append(self.grid[unit.row][leftCol])
            if rightCol < self.columns:
                if not self.unitInArray(self.grid[unit.row][rightCol], units) and self.grid[unit.row][rightCol].district is None:
                    adjacentUnits.append(self.grid[unit.row][rightCol])
            if topRow >= 0:
                if not self.unitInArray(self.grid[topRow][unit.column], units) and self.grid[topRow][unit.column].district is None:
                    adjacentUnits.append(self.grid[topRow][unit.column])
            if bottomRow < self.rows:
                if not self.unitInArray(self.grid[bottomRow][unit.column], units) and self.grid[bottomRow][unit.column].district is None:
                    adjacentUnits.append(self.grid[bottomRow][unit.column])
        return adjacentUnits

    def sumOfCitizens(self, district):
        sum = 0
        for unit in district:
            sum += unit.wins + unit.losses
        return sum

    def printDistrict(self, district):
        for unit in district:
            print(unit.row, unit.column)
        print(self.sumOfCitizens(district))

    def showMap(self):
        for row in range(self.rows):
            line = ""
            for column in range(self.columns):
                if self.grid[row][column].district is not None:
                    line += self.grid[row][column].district
                else:
                    line += 'X'
            print(line)
        print("\n")

    def setDistrict(self, units):
        for unit in units:
            self.grid[unit.row][unit.column].district = self.nextDistrict
        self.nextDistrict = chr(ord(self.nextDistrict) + 1)

    def deleteDistrict(self, units):
        for unit in units:
            self.grid[unit.row][unit.column].district = None
        self.nextDistrict = chr(ord(self.nextDistrict) - 1)

    def checkWin(self):
        district = 'A'
        wonDistricts = 0
        lostDistricts = 0
        while ord(district) < ord(self.nextDistrict):
            wins = 0
            losses = 0
            for row in range(self.rows):
                for column in range(self.columns):
                    if self.grid[row][column].district == district:
                        wins += self.grid[row][column].wins
                        losses += self.grid[row][column].losses
            if wins > losses:
                wonDistricts += 1
            elif wins < losses:
                lostDistricts += 1
            district = chr(ord(district) + 1)
        #print("WINS:", wonDistricts, "LOSSES", lostDistricts)
        if wonDistricts > lostDistricts:
            return True
        return False

    def resultInCorrectFormat(self):
        result = []
        for row in range(self.rows):
            line = ''
            for column in range(self.columns):
                line += self.grid[row][column].district
            result.append(line)
        return result

    def backTracking(self, district, limit, result):
        if result != []:
            return result
        adjacentUnits = self.findAdjacent(district)
        adjacentUnits = reversed(adjacentUnits)
        if self.sumOfCitizens(district) == limit:
            self.setDistrict(district)
            start = self.nextFreeUnit()
            if start == -1:
                if self.checkWin():
                    self.showMap()
                    result = self.resultInCorrectFormat()
                    self.deleteDistrict(district)
                    return result
            else:
                result = self.backTracking([start], limit, result)
            self.deleteDistrict(district)
        else:
            for unit in adjacentUnits:
                district.append(unit)
                if self.sumOfCitizens(district) <= limit:
                    result = self.backTracking(district, limit, result)
                district.pop()
        return result

def unfair_districts(amount_of_people, grid):
    map = Map(len(grid), len(grid[0]), grid)
    district = [map.nextFreeUnit()]
    result = []
    result = map.backTracking(district, amount_of_people, result)
    print("RESULT", result)

    return result


if __name__ == '__main__':

    from itertools import chain
    from collections import defaultdict


    def checker(solution, amount_of_people, grid, win_flg=True):

        w, h = len(grid[0]), len(grid)
        size = w * h
        cell_dic = {}

        # make cell_dic
        def adj_cells(cell):
            result = []
            if cell % w != 1 and cell - 1 > 0:
                result.append(cell - 1)
            if cell % w and cell + 1 <= size:
                result.append(cell + 1)
            if (cell - 1) // w:
                result.append(cell - w)
            if (cell - 1) // w < h - 1:
                result.append(cell + w)
            return set(result)

        for i, v in enumerate(chain(*grid)):
            cell_dic[i + 1] = {'vote': v, 'adj': adj_cells(i + 1)}

        answer = solution(amount_of_people, grid)

        if answer == [] and not win_flg:
            return True

        if not isinstance(answer, list):
            print('wrong data type :', answer)
            return False
        else:
            if len(answer) != h:
                print('wrong data length', answer)
                return False
            for an in answer:
                if len(an) != w:
                    print('wrong data length', an)
                    return False

        ds_dic = defaultdict(list)
        for i, r in enumerate(''.join(answer), start=1):
            ds_dic[r].append(i)

        # answer check
        def district_check(d):
            all_cells = set(d[1:])
            next_cells = cell_dic[d[0]]['adj'] & set(d)
            for _ in range(len(d)):
                all_cells -= next_cells
                next_cells = set(chain(*[list(cell_dic[nc]['adj']) for nc in next_cells])) & set(d)
            return not all_cells

        for ch, cells in ds_dic.items():
            dist_people = sum(sum(cell_dic[c]['vote']) for c in cells)
            if not district_check(cells):
                print('wrong district: ', ch)
                return False
            if dist_people != amount_of_people:
                print('wrong people:', ch)
                return False

        # win check
        win, lose = 0, 0
        for part in ds_dic.values():
            vote_a, vote_b = 0, 0
            for p in part:
                a, b = cell_dic[p]['vote']
                vote_a += a
                vote_b += b
            win += vote_a > vote_b
            lose += vote_a < vote_b

        return win > lose

    assert checker(unfair_districts, 5, [
        [[2, 1], [1, 1], [1, 2]],
        [[2, 1], [1, 1], [0, 2]]]), '3x2grid'

    assert checker(unfair_districts, 9, [
        [[0, 3], [3, 3], [1, 1]],
        [[1, 2], [1, 0], [1, 1]],
        [[0, 3], [2, 1], [2, 2]]]), '3x3gid'

    assert checker(unfair_districts, 8, [
        [[1, 1], [2, 0], [2, 0], [3, 3]],
        [[1, 1], [1, 2], [1, 1], [0, 3]],
        [[1, 1], [1, 1], [1, 2], [0, 3]],
        [[1, 1], [1, 1], [1, 1], [2, 0]]]), '4x4gid'

    assert checker(unfair_districts, 3, [
        [[3, 0], [0, 3]],
        [[2, 0], [0, 1]]]), 'Fail'

    assert checker(unfair_districts, 6, [
        [[2, 0], [1, 1], [1, 1], [1, 1], [1, 1], [0, 2]],
        [[2, 0], [1, 1], [0, 2], [2, 0], [0, 2], [1, 1]]]), 'Fail'

    assert checker(unfair_districts, 15,[[[1,0],[0,5],[0,1],[5,0],[1,0]],
                                         [[0,2],[0,3],[0,2],[0,4],[2,0]],
                                         [[3,0],[4,0],[1,0],[0,5],[0,4]],
                                         [[0,5],[0,3],[2,0],[5,0],[0,3]],
                                         [[0,4],[0,1],[0,2],[0,3],[0,4]]])

    print('check done')

