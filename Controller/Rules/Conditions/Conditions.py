from typing import List

# No duplication allowed


class UniqueCondition():

    def check(self, positions, value):
        for position in positions:
            if value in position:
                return False

        return True


def main():
    pass


if __name__ == '__main__':
    main()
