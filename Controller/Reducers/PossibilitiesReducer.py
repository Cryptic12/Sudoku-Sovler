class PossibilitiesReducer():

    _reducers = []

    def __init__(self, reducers):
        self._reducers = reducers

    # Add a reducer
    def add_reducer(self, reducer):
        self._reducers.append(reducer)

    # Returns a list of all reductions as determined by the reducers
    def reduce_possibilities(self, possibilities):

        reductions = []
        for reducer in self._reducers:
            reduction = reducer.reduce(possibilities)
            reductions.extend(reduction)

        return reductions


def main():
    pass


if __name__ == '__main__':
    main()
