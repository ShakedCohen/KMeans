import matplotlib.pyplot as plt
#from scipy.misc import imread
import init_centroids
import numpy as np


class Centroid:

    _assigned_pixels = []
    _location = None

    def __init__(self, init_loc):
        self._assigned_pixels = []
        self._location = init_loc

    def get_location(self):
        return self._location

    def add_pixel(self, pixel):
        self._assigned_pixels.append(pixel)

    def remove_pixel(self, pixel):
        self._assigned_pixels.remove(pixel)

    def is_pixel_assigned(self, pixel):
        return self._assigned_pixels.__contains__(pixel)

    def update_location(self, k):
        pixel_sum = 0
        # sum all pixels
        for pixel in self._assigned_pixels:
            pixel_sum = pixel_sum + pixel

        # update new location
        _location = pixel_sum / k

    #def print_centroid(self):


def distance(x1, x2):
    return np.sqrt(pow((x1[0] - x2[0]), 2) + pow((x1[1] - x2[1]), 2) + pow((x1[2] - x2[2]), 2), 2)


def find_centroid_of_pixel(pixel, centroids):
    for cent in centroids:
        if cent.is_pixel_assigned(pixel):
            return cent
    return None


def print_centroids_locations(centroids, iteration):
    print("iter " + ""+iteration + ":")
    first = True
    for cent in centroids:
        if first:
            print(" ")
        else:
            print(", ")
        print(cent)

def main():
    path = 'dog.jpeg'
    A = imread(path)
    A_norm = A.astype(float) / 255.
    img_size = A_norm.shape
    X = A_norm.reshape(img_size[0] * img_size[1], img_size[2])

    for j in range(1, 5):

        # num of clusters
        k = pow(2, j)

        # centroid initialization
        init_locations = init_centroids.init_centroids(X, k)
        centroids = []
        for loc in init_locations:
            centroids.append(Centroid(loc))

        for i in range(0, 11):
            # one iteration
            for pixel in X:
                # holds the cent before new assignment
                prev_cent = find_centroid_of_pixel(pixel, centroids)
                # will hold the closest cent
                curr_min = (centroids[0], 100)
                # find closest cent
                for cent in centroids:
                    curr_dist = distance(cent.get_location(), pixel)
                    if curr_dist <= curr_dist[1]:
                        curr_min = (cent, curr_dist)
                # curr_min has the min cent and dist

                # remove pixel from old centroid
                prev_cent.remove_pixel(pixel)
                # add pixel to new centroid
                curr_min[0].add_pixel(pixel)
            # update centroids location
            for cent in centroids:
                cent.update_location(k)
        # finished learning

main()


