#!/usr/bin/python
# -*- coding: utf-8 -*-

##
# this script serves to use the k-means
# to cluster articles within a category
#
# @author Yuan JIN
# @contact chengdujin@gmail.com
# @since 2012.03.15
# @latest 2012.03.21
#

import redis
REDIS_SERVER = 'localhost'
r = redis.StrictRedis(REDIS_SERVER)

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
    def __init__(self, docs, k=None):
        self.k = k
        self.docs = docs
        self.points, self.centroids = self.init_centroids(docs, k)
        self.clusters = []

    def init_centroids(self, docs, limit):
        'pick the inital centroids among the data points'
        'the candidates should be stored in self.centroids'
        # merge all the points
        points = []
        for doc in docs:
            points.extend(doc)
        
        import random
        from ordereddict import OrderedDict
        centroids = []
        weighted_points = {}
        for point in points:
            weight = random.random() * 10000
            weighted_points[point] = weight

        # sort out limit number of candidate centroids
        weighted_points = OrderedDict(sorted(weighted_points.items(), key=lambda d: -d[1]))
        for i in range(limit):
            centroids.append(weighted_points.keys()[i])
        return points, centroids

    def distance(self, centroid, point):
        'calculate the distance between the two points'
        if not centroid or not point: 
            return 0

        # a point (incl. centroid) is an instance of media.Segment
        if r.exists(u'@%s' % centroid.word) or r.exists(u'@%s' % point.word):
            if centroid.word <> point.word:
                first = r.get(u'%s:%s' % (centroid.word, point.word))
                first = first if first else 0
                second = r.get(u'%s:%s' % (point.word, centroid.word))
                second = second if second else 0
                if first or second:
                    return first if first > second else second
                else: # if one word does not really exists, which is highly possible
                    # compute the average value
                    compounds = r.keys(u'%s:*' % (centroid.word if first else point.word))
                    total = 0
                    for v in compounds:
                        total += float(r.get(v))
                    return total / float(len(compounds))
            else: # if two words are the same, they should have the closest distance
                return 1e30000
        else: # no words actually exists
            return 1 / float(len(r.keys('@*')))
            
    def find_closest_centroid(self, point):
        'find the closest centroid by distance'
        maximum = float(0)
        closest = None
        for centroid in self.centroids:
            dist = self.distance(centroid, point) 
            if dist > maximum:
                maximum = dist
                closest = centroid
        return closest    

    def find_centroid(self, cluster):
        'find the centroid within a cluster by finding out the smallest average value from a node to others'
        all_points = []
        all_points.extend(cluster.points)
        all_points.append(cluster.centroid)
        new_centroid = None
        max_dist = 0

        for point in all_points:
            dists = [self.distance(point, p) if point <> p else 0 for p in all_points]
            total_dist = 0
            for dist in dists:
                total_dist += dist
            average_dist = float(total_dist) / float(len(all_points) - 1)
            if average_dist > max_dist:
                max_dist = average_dist
                new_centroid = point
        return new_centroid
    
    def cluster(self):
        ''
        # array of Cluster instances
        clusters = []
        centroids_changed = True
        counter = 1
        while centroids_changed:
            print counter, 'round'
            if counter > 1:
                break
            counter += 1
            for point in self.points:
                # point is an instance of media.Segment
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
                if len(old_cluster.points):
                    new_centroid = self.find_centroid(old_cluster)
                    if new_centroid <> old_cluster.centroid:
                        centroid_changed = True
                        new_cluster = Cluster()
                        new_cluster.centroid = new_centroid
                        clusters.append(new_cluster)
                    else:
                        clusters.append(old_cluster)
        self.clusters = clusters

    def publish(self):
        words = []
        for cluster in self.clusters:
            terms = []
            # first one is the center node of the cluster
            terms.append(cluster.centroid)
            terms.extend(cluster.points)
            if terms:
                print cluster.centroid.word;
                print ','.join([p.word for p in cluster.points])
                print
                words.append(terms)
        if words:
            return words

if __name__ == '__main__':
    'test ground'
    kmeans = KMeans(4, None) 
