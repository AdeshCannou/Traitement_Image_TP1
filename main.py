import cv2 as cv
import os
import numpy as np

path = "frag_eroded/frag_eroded/"

# Charger les données des fragments et des fragments à ignorer
fragment_data = [line.strip().split() for line in open("fragments.txt", "r")]
fragment_skip = [line.strip().split() for line in open("fragments_s.txt", "r")]

img_width, img_height = 2000, 1500

# Créer une image vide de la taille de l'image de sortie
image = np.zeros((img_height, img_width, 3), np.uint8)  # Utilisez 3 canaux pour RGB

# Placer les fragments dans l'image de sortie avec une marge à partir de (200, 200)
margin_x, margin_y = 200, 200

for i in fragment_data:
    index, center_x, center_y, angle = i  # Convertir en virgule flottante

    fragment_filename = os.path.join(path, f"frag_eroded_{int(index)}.png")

    # Charger les fragments
    fragment = cv.imread(fragment_filename)

    fragment_height, fragment_width, _ = fragment.shape

    M = cv.getRotationMatrix2D(
        (fragment_width / 2, fragment_height / 2),
        float(angle),
        1,
    )
    fragment = cv.warpAffine(fragment, M, (fragment_width, fragment_height))

    # Calculer les coins du fragment avec la marge
    x1 = int(center_x) - fragment_width // 2 + margin_x
    y1 = int(center_y) - fragment_height // 2 + margin_y
    x2 = x1 + fragment_width
    y2 = y1 + fragment_height

    image[y1:y2, x1:x2] += fragment

# crop l'image 1775x775
crop_img = image[200:975, 200:1907]

# Afficher l'image de sortie
cv.imwrite("output.png", crop_img)
cv.imshow("Image Finale", crop_img)
cv.waitKey(0)
cv.destroyAllWindows()