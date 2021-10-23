class PossibilitiesReducer():

    _reducers = []

    def __init__(self, reducers):
        self._reducers = reducers

    def addReducer(self, reducer):
        self._reducers.append(reducer)

    def reducePossibilities(self, possibilities):
        count = self._countTotalPossibilities(possibilities)
        continueReducing = True
        for row in possibilities:
            print(row)

        while continueReducing:
            for reducer in self._reducers:
                possibilities = reducer.reduce(possibilities)
                print(reducer)
                for row in possibilities:
                    print(row)
            countAfterReducers = self._countTotalPossibilities(possibilities)
            if countAfterReducers >= count:
                continueReducing = False
            count = countAfterReducers

        return possibilities

    def _countTotalPossibilities(self, possibilities):
        total = 0
        for row in possibilities:
            for position in row:
                total += len(position)
        return total
