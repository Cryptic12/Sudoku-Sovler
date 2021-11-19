from typing import List


class UniqueCondition():

    def check(self, positions, value):
        for position in positions:
            if value in position:
                return False

        return True
