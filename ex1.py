import matplotlib.pyplot as plt
from scipy.misc import imread
import math
import init_centroids
import numpy as np


class Centroid:

    _assigned_pixels = []
    _location = None

    def __init__(self, init_loc):
        self._assigned_pixels = []
        self._location = init_loc

    def init_assigned_pixels(self):
        self._assigned_pixels = []

    def get_location(self):
        return self._location

    def add_pixel(self, pixel):
        self._assigned_pixels.append(pixel)

    def remove_pixel(self, pixel):
        self._assigned_pixels.remove(pixel)

    def is_pixel_assigned(self, pixel):
        for curr_pixel in self._assigned_pixels:
            if curr_pixel is pixel:
                return True
        return False

    def update_location(self):
        pixel_sum = 0
        # sum all pixels
        for pixel in self._assigned_pixels:
            pixel_sum = pixel_sum + pixel

        # update new location
        self._location = pixel_sum / self._assigned_pixels.__len__()

    def print_cent(self):
        cent = self.get_location()
        if type(cent) == list:
            cent = np.asarray(cent)
        if len(cent.shape) == 1:
            return ' '.join(str(np.floor(100 * cent) / 100).split()).replace('[ ', '[').replace('\n', ' ').replace(' ]',
                                                                                                                   ']').replace(
                ' ', ', ')
        else:
            return ' '.join(str(np.floor(100 * cent) / 100).split()).replace('[ ', '[').replace('\n', ' ').replace(' ]',
                                                                                                                   ']').replace(
                ' ', ', ')[1:-1]


def distance(x1, x2):
    return math.sqrt(pow((x1[0] - x2[0]), 2) + pow((x1[1] - x2[1]), 2) + pow((x1[2] - x2[2]), 2))


def find_centroid_of_pixel(pixel, centroids):
    for cent in centroids:
        if cent.is_pixel_assigned(pixel):
            return cent
    return None


def print_centroids_locations(centroids):
    first = True
    for cent in centroids:
        if first:
            print(" ", end='')
            first = False
        else:
            print(", ", end='')
        location_to_print = cent.print_cent()
        print(location_to_print, end='')
    print(flush=True)


def main():
    path = 'dog.jpeg'
    A = imread(path)
    A_norm = A.astype(float) / 255.
    img_size = A_norm.shape
    X = A_norm.reshape(img_size[0] * img_size[1], img_size[2])

    for j in range(1, 5):
        # num of clusters
        k = pow(2, j)
        print("k=" + k.__str__() + ":")
        #k = 2
        # centroid initialization
        init_locations = init_centroids.init_centroids(X, k)
        centroids = []
        for loc in init_locations:
            centroids.append(Centroid(loc))

        print("iter 0:", end='')
        print_centroids_locations(centroids)

        for i in range(1, 11):
            print("iter " + "" + i.__str__() + ":", end='')
            # one iteration
            for cent in centroids:
                cent.init_assigned_pixels()
            for pixel in X:
                # will hold the closest cent
                curr_min = (centroids[0], 100)
                # find closest cent
                for cent in centroids:
                    curr_dist = distance(cent.get_location(), pixel)
                    if curr_dist <= curr_min[1]:
                        curr_min = (cent, curr_dist)
                # curr_min has the min cent and dist

                # add pixel to new centroid
                curr_min[0].add_pixel(pixel)
            # update centroids location
            for cent in centroids:
                cent.update_location()
            print_centroids_locations(centroids)

        # displays photo at the end of iteration
        display_image(X, centroids, img_size)

    # finished learning


def display_image(X, centroids, img_size):
    def calcDistance(p1, p2):
        return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2 + (p1[2] - p2[2]) ** 2)

    array = [c.get_location() for c in centroids]
    B = []
    # create the new picture array
    for pixel in X:
        smallestDist = calcDistance(pixel, array[0])
        smallestIndex = 0
        index = 0
        # check witch centroid is the closest to the current pixel
        for centroid in array:
            dist = calcDistance(pixel, centroid)
            if smallestDist > dist:
                smallestDist = dist
                smallestIndex = index
            index += 1
        B.append(array[smallestIndex])
    B = np.array(B)
    # plot the image
    B = B * 255
    B = B.astype(int)
    Y = B.reshape(img_size[0], img_size[1], img_size[2])
    plt.imshow(Y)
    plt.grid(False)
    plt.show()


main()


