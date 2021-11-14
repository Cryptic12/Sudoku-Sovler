class PossibilitiesReducer():

    _reducers = []

    def __init__(self, reducers):
        self._reducers = reducers

    def add_reducer(self, reducer):
        self._reducers.append(reducer)

    def reduce_possibilities(self, possibilities):
        count = self._count_total_possibilities(possibilities)
        continue_reducing = True
        for row in possibilities:
            print(row)

        while continue_reducing:
            for reducer in self._reducers:
                possibilities = reducer.reduce(possibilities)
                print(reducer)
                for row in possibilities:
                    print(row)
            count_after_reducers = self._count_total_possibilities(
                possibilities)
            if count_after_reducers >= count:
                continue_reducing = False
            count = count_after_reducers

        return possibilities

    def _count_total_possibilities(self, possibilities):
        total = 0
        for row in possibilities:
            for position in row:
                total += len(position)
        return total
