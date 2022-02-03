class PossibilitiesReducer():

    _reducers = []

    def __init__(self, reducers):
        self._reducers = reducers

    def add_reducer(self, reducer):
        self._reducers.append(reducer)

    def reduce_possibilities(self, possibilities):

        reductions = []
        for reducer in self._reducers:
            reduction = reducer.reduce(possibilities)
            reductions.extend(reduction)

        return reductions

    def _count_total_possibilities(self, possibilities):
        total = 0
        for row in possibilities:
            for position in row:
                total += len(position)
        return total


def main():
    pass


if __name__ == '__main__':
    main()
