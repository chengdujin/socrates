#!/usr/bin/python
# -*- coding: utf-8 -*-

##
# this script serves to use the k-means
# to cluster articles within a category
#
# @author Yuan JIN
# @contact chengdujin@gmail.com
# @since 2012.03.15
# @latest 2012.03.16
#

# reload the script encoding
import sys 
reload(sys)
sys.setdefaultencoding('UTF-8')


class Cluster(object):
    'class to model a cluster'
    def __init__(self):
        self.centroid = None
        self.points = []
        self.word_map = {}

class KMeans(object):
    'a simple implementation of k-means algorithm'
    def __init__(self, points, k=None):
        self.k = k
        self.points = points
        self.centroids = self.init_centroids(points, k)
        self.clusters = []

    def init_centroids(self, points, limit):
        'pick the inital centroids among the data points'
        'the candidates should be stored in self.centroids'
        import random
        centroids = []
        weighted_points = {}
        for point in points:
            weight = random.random() * 10000
            weighted_points[point] = weight

        # sort out limit number of candidate centroids
        weighted_points = sorted(weighted_points.items(), key=lambda d: -d[1])
        for i in range(limit):
            centroids.append(weighted_points.keys()[i])
        return centroids

    def distance(self, centroid, point):
        'calculate the distance between the two points'
        intersect = set(centroid.labels) & set(point.labels)
        return float(len(intersect) / len(point))

    def find_closest_centroid(self, point):
        'find the closest centroid by distance'
        minimum = float(1)
        closest = None
        for centroid in self.centroids:
            dist = self.distance(centroid, point) 
            if dist < minimum:
                minimum = dist
                closest = centroid
        return closest    

    def find_centroid(self, cluster):
        'find the centroid within a cluster'
        minimum_total_dist = len(cluster) - 1
        centroid_candidate = None
        for point in cluster.points:
            total_dist = 0
            a = len(point.labels)
            # compare with other points
            for other in cluster:
                if point <> other:
                    b = len(other.labels)
                    intersect = set(a) & set(b)
                    total_dist += (float(len(intersect)) / float(len(other.labels)))
            if total_dist < minimum_total_dist:
                minimum_total_dist = total_dist
                centroid_candidate = point
        return centroid_candidate
    
    def cluster(self):
        ''
        # array of Cluster instances
        clusters = []
        centroids_changed = True
        while centroids_changed:
            for point in self.points:
                # the closest centroid to point
                closest = self.find_closest_centroid(point)
                # gotch is an instance of Cluster
                gotcha = None
                for cluster in clusters:
                    # a cluster is an instance of Cluster
                    # a cluster contains a centroid and several points
                    if closest == cluster.centroid:
                        gotcha = cluster
                        break
                if not gotcha:
                    gotcha = Cluster()
                    gotcha.centroid = closest
                    clusters.append(gotcha)
                gotcha.points.append(point)

            # calculate new centroids from current ones
            centroid_changed = False
            old_clusters = clusters
            clusters = []
            for old_cluster in old_clusters:
                if len(old_cluster):
                    # old_cluster is an instance of Cluster
                    new_centroid = find_centroid(old_cluster)
                    if new_centroid <> old_cluster.centroid:
                        centroid_changed = True
                        new_cluster = Cluster()
                        new_cluster.centroid = new_centroid
                        clusters.append(new_cluster)
                    else:
                        clusters.append(old_cluster)
        self.clusters = clusters

if __name__ == '__main__':
    'test ground'
    kmeans = KMeans(4, None) 
