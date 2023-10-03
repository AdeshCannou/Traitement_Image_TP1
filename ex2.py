import cv2 as cv
import os
import numpy as np

path = "frag_eroded/frag_eroded/"


dx = float(input("Choose dx "))
dy = float(input("Choose dy "))
da = float(input("Choose da "))

delta = np.array([dx, dy, da])

def is_solution(sol, test):
    return abs(sol - test) < delta

fragment_data = { el[0]:np.array([el[1], el[2], el[3]], dtype=float) for el in [line.strip().split() for line in open("fragments.txt", "r")]}
compared = {  el[0]:np.array([el[1], el[2], el[3]], dtype=float) for el in [line.strip().split() for line in open("solution.txt", "r")]}
fragment_skip = [line.strip().split() for line in open("fragments_s.txt", "r")]

total = 0
div = 0

for i in fragment_data:
    if i in fragment_skip:
        continue

    fragment_filename = os.path.join(path, f"frag_eroded_{int(i)}.png")

    # Charger les fragments
    fragment = cv.imread(fragment_filename)

    fragment_height, fragment_width, _ = fragment.shape

    if i not in compared.keys():
        total -= fragment_height * fragment_width
    else:
        div += fragment_width * fragment_height
        if all(is_solution(fragment_data[i], compared[i])):
            total += fragment_height * fragment_width


result = round(total/div * 100, 2)
print("précision : " + str(result) + "%")