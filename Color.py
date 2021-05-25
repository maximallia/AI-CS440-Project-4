from PIL import Image
import numpy as np
from random import randint
import copy

'''
    Kyle VanWageninge kjv48
    Daniel Ying dty16
    AI Project 4 Colorization
'''


# runs the k means clustering algorithm
def kmeans(cluster_centers, clusters, arr):
    # print(clusters)
    print(cluster_centers)
    clusters = [[] for _ in range(5)]
    run = 0
    # will look for new centers 29 times
    while run < 30:
        imagecopy2 = [[[] for _ in range(int(len(arr[0]) / 2))] for _ in range(int(len(arr)))]
        distance = 0
        for i in range(int(len(arr))):
            for k in range(int(len(arr[i]) / 2)):
                final_cluster = -1
                all_distances = []
                for x in range(5):
                    old_distance = copy.deepcopy(distance)
                    if x == 0:
                        final_cluster = 0
                        old_distance = -1
                    reds = (2 * (cluster_centers[x][0] - int(arr[i][k][0])) ** 2)
                    greens = (4 * (cluster_centers[x][1] - int(arr[i][k][1])) ** 2)
                    blues = (3 * (cluster_centers[x][2] - int(arr[i][k][2])) ** 2)
                    distance = (reds + blues + greens) ** .5
                    # print(distance)
                    # print('old ', old_distance)
                    all_distances.append(distance)

                holder = min(all_distances)
                for y in range(len(all_distances)):
                    if all_distances[y] == holder:
                        final_cluster = y

                # on the final run fill the new image with rgb values of the cluster centers
                if run == 29:
                    imagecopy2[i][k] = copy.deepcopy(cluster_centers[final_cluster])
                clusters[final_cluster].append(list(arr[i][k]))
        # print(clusters)
        if run != 29:
            # calculate the average of each cluster to get the center
            for k in range(5):
                red_avg = 0
                green_avg = 0
                blue_avg = 0
                for i in range(len(clusters[k])):
                    red_avg = red_avg + int(clusters[k][i][0])
                    green_avg = green_avg + int(clusters[k][i][1])
                    blue_avg = blue_avg + int(clusters[k][i][2])

                if len(clusters[k]) != 0:
                    red_avg = red_avg / len(clusters[k])
                    cluster_centers[k][0] = int(red_avg)

                    green_avg = green_avg / len(clusters[k])
                    cluster_centers[k][1] = int(green_avg)

                    blue_avg = blue_avg / len(clusters[k])
                    cluster_centers[k][2] = int(blue_avg)

        # print(clusters)
        print(cluster_centers)

        run += 1
    print(imagecopy2)

    array = np.array(imagecopy2, dtype=np.uint8)
    new_image = Image.fromarray(array)
    # new_image.save('new.png')
    new_image.show()
    return cluster_centers, imagecopy2


# get the 6 most similar patches and re color the right side of the image
def findSix(bw_image, recolored_image, centers):
    offset = int(len(bw_image) / 2)
    imagecopy2 = [[[] for _ in range(int(len(bw_image[0]) / 2))] for _ in range(int(len(bw_image)))]
    if offset >= len(bw_image):
        offset -= 1
    right_image = []
    for i in range(len(bw_image)):
        for k in range(int(len(bw_image[i]) / 2)):
            print(i, k)
            # take the pixel in the test data, get the surrounding pixels and map it to the cluster center majority
            if i != 0 and k < int(((len(bw_image[i])) / 2) - 1) and k != 0 and i < int((len(bw_image)) - 1):
                all_pixels = SurroundingSquares(i, k + offset, len(bw_image), len(bw_image[i]), bw_image)
                top = TopSix(all_pixels, bw_image)
                rep_colors = []
                for s in range(len(top)):
                    rep_colors.append(recolored_image[top[s][1]][top[s][2]])
                # print(rep_colors)
                final_color = getColor(rep_colors, centers)
                imagecopy2[i][k] = copy.deepcopy(final_color)
            else:
                imagecopy2[i][k] = [255, 255, 255]
    print(imagecopy2)
    array = np.array(imagecopy2, dtype=np.uint8)
    new_image = Image.fromarray(array)
    # new_image.save('new.png')
    new_image.show()


# get the majority color from the 6 closest centers to the test patch, return an rgb value
def getColor(middle_color, centers):
    c1 = 0
    c2 = 0
    c3 = 0
    c4 = 0
    c5 = 0
    for i in range(len(middle_color)):
        if middle_color[i] == centers[0]:
            c1 += 1
        elif middle_color[i] == centers[1]:
            c2 += 1
        elif middle_color[i] == centers[2]:
            c3 += 1
        elif middle_color[i] == centers[3]:
            c4 += 1
        elif middle_color[i] == centers[4]:
            c5 += 1

    final = [c1, c2, c3, c4, c5]
    # print(middle_color)
    # print(centers)
    # print(final)
    ma = final[0]
    x = 1
    while x < len(final):
        if ma < final[x]:
            ma = final[x]
        x += 1

    found = 0
    f = []
    for t in range(len(final)):
        if final[t] == ma:
            found += 1
            f.append(t)
    # print(f)

    for i in range(len(middle_color)):
        for s in range(len(f)):
            if centers[f[s]] == middle_color[i]:
                # print(centers[f[s]])
                # x = input()
                return centers[f[s]]


# find the top 6 similar patches
def TopSix(pixels, bw_image):
    distances = []
    for i in range(int(len(bw_image))):
        for k in range(int(len(bw_image[i]) / 2)):
            if i != 0 and k < (len(bw_image[i]) - 1) and k != 0 and i < len(bw_image) - 1:
                train_pixels = SurroundingSquares(i, k, len(bw_image), len(bw_image[i]), bw_image)
                # print(train_pixels)
                # print(pixels)
                total = 0
                for x in range(len(pixels)):
                    total += ((pixels[x] - train_pixels[x]) ** 2)
                distances.append([total ** .5, i, k])

    # take all the distances and pop off the 6 closest to the original
    topSix = []
    for k in range(6):
        lowest = distances[0][0]
        spot = 0
        for i in range(len(distances)):
            if distances[i][0] < lowest:
                lowest = distances[i][0]
                spot = i
        topSix.append(distances.pop(spot))
    # print(topSix)

    return topSix


# find the surrounding pixels
def SurroundingSquares(x, y, image_sizex, image_sizey, image):
    all_pixels = [image[x][y]]

    all_pixels.append(int(image[x + 1][y]))

    all_pixels.append(int(image[x][y + 1]))

    all_pixels.append(int(image[x - 1][y]))

    all_pixels.append(int(image[x - 1][y]))

    all_pixels.append(int(image[x + 1][y + 1]))

    all_pixels.append(int(image[x - 1][y - 1]))

    all_pixels.append(int(image[x + 1][y - 1]))

    all_pixels.append(int(image[x - 1][y + 1]))
    return all_pixels


def main():
    img = Image.open('f12.jpg')
    newsize = (250, 250)
    img = img.resize(newsize)
    img.show()
    arr = np.array(img)  # 640x480x4 array
    print(arr)
    print(len(arr))
    print(len(arr[0]))
    imagecopy = [[0 for _ in range(len(arr[0]))] for _ in range(len(arr))]
    print(arr[0][0][0])
    # print(imagecopy[0][0][0])
    # create a new black and white image based on the original image
    for i in range(len(arr)):
        # print(i)
        for k in range(len(arr[i])):
            # print(k)
            imagecopy[i][k] = int((int(arr[i][k][0]) + int(arr[i][k][1]) + int(arr[i][k][2])) / 3)

    array = np.array(imagecopy, dtype=np.uint8)
    new_image = Image.fromarray(array)
    # new_image.save('new.png')
    new_image.show()

    clusters = [[] for _ in range(5)]

    # give the base starting centers for the clusters
    cluster_center = [[221, 0, 0], [254, 246, 1], [0, 187, 0], [0, 126, 254], [70, 1, 155]]
    # print(imagecopy)

    # run k-means, then find the six similar patches and color the test data
    c, imagecopy2 = kmeans(cluster_center, clusters, arr)
    findSix(imagecopy, imagecopy2, cluster_center)


main()
