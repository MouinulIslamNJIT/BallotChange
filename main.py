# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import calculateMargin
import findBallotChange


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    from findBallotChange import *
    import numpy as np
    from calculateMargin import *

    inputArray = [
        ('Male', 'Junior', 'Married', 90),
        ('Male', 'Junior', 'Married', 80),
        ('Male', 'Mid', 'Unmarried', 85),
        ('Male', 'Senior', 'Married', 81),
        ('Male', 'Junior', 'Married', 89),
        ('Male', 'Junior', 'Unmarried', 88),
        ('Female', 'Junior', 'Married', 85),
        ('Female', 'Senior', 'Married', 85),
        ('Female', 'Senior', 'Married', 84),
        ('Female', 'Mid', 'Married', 84),
        ('Female', 'Mid', 'Unmarried', 80)
    ]
    inputArray.sort(reverse=True, key=lambda x: x[3])

    Lc = [i[0] for i in inputArray]
    Lv = [i[-1] for i in inputArray]
    for i in range(len(Lc)):
        if Lc[i] == "Male":
            Lc[i] = "B"
        else:
            Lc[i] = "A"

    k = 4
    a = int(np.ceil(k * (Lc.count("A") / len(inputArray))))
    b = int(np.floor(k * (Lc.count("B") / len(inputArray))))

    ia, aq, ib, bq = calculateIandQ(Lv, Lc, a, b)
    # print(findq(Lv,Lc,a,b))
    margin = calculateMargin(Lv, Lc, ia, ib, a, b, aq, bq)
    print(margin)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
