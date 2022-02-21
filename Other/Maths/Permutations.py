
# Recursively create permuations of length cnt from the contents of arr
def generate_permutation(arr, cnt, result=None):

    if result is None:
        result = []

    if (cnt == 0):
        return [result]

    to_return = []

    for i, value in enumerate(arr):
        to_return.extend(generate_permutation(
            arr[i + 1:], cnt - 1, [*result, value]))

    return to_return


def main():
    pass


if __name__ == '__main__':
    main()
