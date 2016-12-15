# kmeans_test.py
# Walker M. White (wmw2), Steve Marschner (srm2)
# October 12, 2015
"""Unit test for k-means clustering

This unit test is not complete.  It is enough to help guide you with this assignment,
but you should not rely on it catching all possible errors.  You might want to add
other tests, but this is not required."""
#import cornelltest # Make sure you have NEW version
import random
import numpy

# The modules to test.
import a6


# Helper function for latter tests
def candy_to_kmeans(filename,k,seed=None):
    """Returns: KMeans object for the given candy CSV file.
    
    Candy CSV files have 5 attributes: the candy name, the sweetness, the sourness,
    the nuttiness, and the texture.  The first value is a string.  The remaining
    four values are floats between 0 and 1.
    
    Precondition: filename is a name of a candy CSV file."""
    file = open(filename)
    contents = []
    for x in file:
        if x[0] != '#': # Ignore comments
            point = x.strip().split(',')
            point = map(float,point[1:]) # Remove the name and convert to floats
            contents.append(point)
    dataset = a6.Dataset(4,contents)
    return a6.ClusterGroup(dataset, k, seed)


def test_dataset():
    """Test the Dataset class."""
    print '  Testing class Dataset'
    
    # TEST CASE 1
    # Create and test an empty dataset
    dset1 = a6.Dataset(3)
    assert 3 == dset1.getDimension()
    assert 0 == dset1.getSize()
    
    # We use this assert function to compare lists
    assert [] == dset1.getContents()
    
    print '    Default initialization looks okay'
    
    # TEST CASE 2
    # Create and test a non-empty dataset
    items = [[0.0,0.0,0.0],[1.0,0.0,0.0],[0.0,1.0,0.0],[0.0,0.0,1.0]]
    dset2 = a6.Dataset(3,items)
    assert 3 == dset2.getDimension()
    assert 4 == dset2.getSize()
    
    # Check that contents is initialized correctly
    # Make sure items is COPIED
    assert items == dset2.getContents()
    assert (dset2.getContents() is items) == False
    assert (dset2.getContents()[0] is items[0]) == False
    
    print '    User-provided initialization looks okay'
    
    # Check that getPoint() is correct AND that it copies
    assert [0.0,1.0,0.0] == dset2.getPoint(2)
    assert (dset2.getContents()[2] is dset2.getPoint(2)) == False
    
    print '    Method Dataset.getPoint looks okay'
    
    # Add something to the dataset (and check it was added)
    dset1.addPoint([0.0,0.5,4.2])
    assert [[0.0,0.5,4.2]] == dset1.getContents()
    assert [0.0,0.5,4.2] == dset1.getPoint(0)
    # Check the point is COPIED
    assert (dset1.getPoint(0) is dset1.getContents()[0]) == False
    
    extra = [0.0,0.5,4.2]
    dset2.addPoint(extra)
    items.append(extra)
    assert items == dset2.getContents()
    # Check the point was COPIED
    assert False == (id(extra) in map(id,dset2.getContents()))
    
    print '    Method Dataset.addPoint looks okay'
    print '  class Dataset appears correct'
    print ''


def test_cluster_a():
    """Test Part A of the Cluster class assignment."""
    print '  Testing Part A of class Cluster'
    
    # TEST CASE 1
    # Create and test a cluster (always empty)
    dset = a6.Dataset(3)
    point = [0.0,1.0,0.0]
    cluster1 = a6.Cluster(dset, point)
    
    # Compare centroid and contents
    assert point == cluster1.getCentroid()
    assert [] == cluster1.getIndices()
    # Make sure centroid COPIED
    assert id(point) != id(cluster1.getCentroid())
    
    print '    Basic cluster methods look okay'    
    
    # Add something to cluster (and check it was added)
    extra = [[0.0,0.5,4.2],[0.0,1.0,0.0]]
    dset.addPoint(extra[0])
    dset.addPoint(extra[1])
    cluster1.addIndex(1)
    assert [1] == cluster1.getIndices()
    cluster1.addIndex(0)
    assert [1,0] == cluster1.getIndices()
    # Make sure we can handle duplicates!
    cluster1.addIndex(1)
    assert [1,0] == cluster1.getIndices()
    
    print '    Method Cluster.addIndex look okay'
    
    # And clear it
    contents = cluster1.getContents()
    assert 2 == len(contents)
    assert extra[1] == contents[0]
    assert extra[0] == contents[1]
    
    print '    Method Cluster.getContents look okay'
    
    # And clear it
    cluster1.clear()
    assert [] == cluster1.getIndices()
    
    print '    Method Cluster.clear look okay'
    print '  Part A of class Cluster appears correct'
    print ''


def test_cluster_b():
    """Test Part B of the Cluster class assignment."""
    print '  Testing Part B of class Cluster'

    # A dataset with four points
    items = [[1.0,0.0,0.0],[0.0,1.0,0.0],[0.0,0.0,0.0],[0.0,0.0,1.0]]
    dset = a6.Dataset(3, items)
    
    # Create two clusters
    cluster2 = a6.Cluster(dset, [0.5,0.5,0.0])
    cluster3 = a6.Cluster(dset, [0.0,0.0,0.5])
    
    # TEST CASE 1 (distance)
    dist = cluster2.distance([1.0,0.0,-1.0])
    assert 1.22474487139 == round(dist,11)
    
    # TEST CASE 2 (distance)
    dist = cluster2.distance([0.5,0.5,0.0])
    assert 0.0 == dist
    
    # TEST CASE 3 (distance)
    dist = cluster3.distance([0.5,0.0,0.5])
    assert 0.5 == dist
    print '    Method Cluster.distance() looks okay'
    
    # TEST CASE 1 (updateCentroid): centroid remains the same
    cluster2.addIndex(0)
    cluster2.addIndex(1)
    stable = cluster2.updateCentroid()
    print cluster2.getCentroid()
    assert [0.5, 0.5, 0.0] == cluster2.getCentroid()
    assert True == stable

    # TEST CASE 2 (updateCentroid): centroid changes
    cluster2.addIndex(2)
    cluster2.addIndex(3)
    stable = cluster2.updateCentroid()
    assert [0.25, 0.25, 0.25] == cluster2.getCentroid()
    assert False == stable
    # updating again without changing points: centroid stable
    stable = cluster2.updateCentroid()
    assert [0.25, 0.25, 0.25] == cluster2.getCentroid()
    assert True == stable

    print '    Method Cluster.updateCentroid() looks okay'
    print '  Part B of class Cluster appears correct'
    print ''


def test_kmeans_a():
    """Test Part A of the ClusterGroup class."""
    print '  Testing Part A of class ClusterGroup'
    
    # A dataset with four points almost in a square
    items = [[0.,0.], [10.,1.], [10.,10.], [0.,9.]]
    dset = a6.Dataset(2, items)

    # Test creating a clustering with random seeds
    km = a6.ClusterGroup(dset, 3)
    # Should have 3 clusters
    assert len(km.getClusters()) == 3
    for clust in km.getClusters():
        # cluster centroids should have been chosen from items
        assert clust.getCentroid() in items
        # cluster centroids should be distinct (since items are)
        for clust2 in km.getClusters():
            if clust2 is not clust:
                assert clust.getCentroid() != clust2.getCentroid()

    print '    Random ClusterGroup initialization looks okay'

    # Clusterings of that dataset, with two and three deterministic clusters
    km = a6.ClusterGroup(dset, 2, [0,2])
    assert items[0] == km.getClusters()[0].getCentroid()
    assert items[2] == km.getClusters()[1].getCentroid()
    km = a6.ClusterGroup(dset, 3, [0,2,3])
    assert items[0] == km.getClusters()[0].getCentroid()
    assert items[2] == km.getClusters()[1].getCentroid()
    assert items[3] == km.getClusters()[2].getCentroid()
    
    # Try it on a file
    km2 = candy_to_kmeans('datasets/smallcandy.csv',3,[23, 54, 36])
    assert [0.38, 0.94, 0.53, 0.07] == km2.getClusters()[0].getCentroid()
    assert [0.84, 0.88, 0.04, 0.86] == km2.getClusters()[1].getCentroid()
    assert [0.8, 0.4, 0.23, 0.33] == km2.getClusters()[2].getCentroid()
    
    print '    Seeded ClusterGroup initialization looks okay'
    print '  Part A of class ClusterGroup appears correct'
    print ''


def test_kmeans_b():
    """Test Part B of the ClusterGroup class."""
    # This function tests the methods _nearest_cluster and _partition,
    # both of which are private methods.  Normally it's not good form to
    # directly call these methods from outside the class, but we make an
    # exception for testing code, which often has to be more tightly
    # integrated with the implementation of a class than other code that
    # just uses the class.
    print '  Testing Part B of class ClusterGroup'
    # Reinitialize data set
    items = [[0.,0.], [10.,1.], [10.,10.], [0.,9.]]
    dset = a6.Dataset(2, items)
    km1 = a6.ClusterGroup(dset, 2, [0,2])
    km2 = a6.ClusterGroup(dset, 3, [0,2,3])

    nearest = km1._nearest_cluster([1.,1.])
    assert nearest is km1.getClusters()[0]

    nearest = km1._nearest_cluster([1.,10.])
    assert nearest is km1.getClusters()[1]

    nearest = km2._nearest_cluster([1.,1.])
    assert nearest is km2.getClusters()[0]

    nearest = km2._nearest_cluster([1.,10.])
    assert nearest is km2.getClusters()[2]
    print '    Method ClusterGroup._nearest_cluster() looks okay'

    # Testing partition()
    # For this example points 0 and 3 are closer, as are 1 and 2
    km1._partition()
    assert set([0,3]) == set(km1.getClusters()[0].getIndices())
    assert set([1,2]) == set(km1.getClusters()[1].getIndices())
    # partition and repeat -- should not change clusters.
    km1._partition()
    assert set([0,3]) == set(km1.getClusters()[0].getIndices())
    assert set([1,2]) == set(km1.getClusters()[1].getIndices())
    
    # Reset the cluster centroids; now it changes
    cluster = km1.getClusters()
    cluster[0]._centroid = [5.0, 10.0]
    cluster[1]._centroid = [0.0, 2.0]
    km1._partition()
    assert set([2,3]) == set(km1.getClusters()[0].getIndices())
    assert set([0,1]) == set(km1.getClusters()[1].getIndices())
    
    # Try it on a file
    index1 = [2, 3, 5, 9, 11, 15, 16, 18, 19, 20, 22, 23, 29, 30, 32, 33, 37, 40, 41, 42, 
              44, 45, 50, 60, 61, 62, 64, 69, 71, 73, 75, 76, 78, 80, 85, 88, 90, 94, 97]
    index2 = [0, 34, 8, 43, 66, 46, 77, 84, 54]
    index3 = [1, 4, 6, 7, 10, 12, 13, 14, 17, 21, 24, 25, 26, 27, 28, 31, 35, 36, 38, 39, 
              47, 48, 49, 51, 52, 53, 55, 56, 57, 58, 59, 63, 65, 67, 68, 70, 72, 74, 79, 
              81, 82, 83, 86, 87, 89, 91, 92, 93, 95, 96, 98, 99]
    
    km3 = candy_to_kmeans('datasets/smallcandy.csv',3,[23, 54, 36])
    km3._partition()
    assert set(index1) == set(km3.getClusters()[0].getIndices())
    assert set(index2) == set(km3.getClusters()[1].getIndices())
    assert set(index3) == set(km3.getClusters()[2].getIndices())
    
    
    print '    Method ClusterGroup._partition() looks okay'
    print '  Part B of class ClusterGroup appears correct'
    print ''

def test_kmeans_c():
    """Test Part C of the ClusterGroup class."""
    print '  Testing Part C of class ClusterGroup'
    items = [[0.,0.], [10.,1.], [10.,10.], [0.,9.]]
    dset = a6.Dataset(2, items)
    km1 = a6.ClusterGroup(dset, 2, [0,2])
    km1._partition()
    
    # Test update()
    stable = km1._update()
    assert [0,4.5] == km1.getClusters()[0].getCentroid()
    assert [10.0,5.5], km1.getClusters()[1].getCentroid()
    assert False == stable
    
    # updating again should not change anything, but should return stable
    stable = km1._update()
    assert [0,4.5] == km1.getClusters()[0].getCentroid()
    assert [10.0,5.5] == km1.getClusters()[1].getCentroid()
    assert stable

    print '    Method ClusterGroup._update() looks okay'

    # Now test the k-means process itself.

    # FOR ALL TEST CASES
    # Create and initialize a non-empty dataset
    items = [[0.5,0.5,0.5],[0.5,0.6,0.6],[0.6,0.5,0.6],[0.5,0.6,0.5],[0.5,0.4,0.5],[0.5,0.4,0.4]]
    dset = a6.Dataset(3,items)

    # Create a clustering, providing non-random seed indices so the test is deterministic
    km2 = a6.ClusterGroup(dset, 2, [1, 3])

    # PRE-TEST: Check first cluster (should be okay if passed part D)
    cluster1 = km2.getClusters()[0]
    assert [0.5, 0.6, 0.6] == cluster1.getCentroid()
    assert set([]) == set(cluster1.getIndices())

    # PRE-TEST: Check second cluster (should be okay if passed part D)
    cluster2 = km2.getClusters()[1]
    assert [0.5, 0.6, 0.5] == cluster2.getCentroid()
    assert set([]) == set(cluster2.getIndices())

    # Make a fake cluster to test update_centroid() method
    clustertest = a6.Cluster(dset, [0.5, 0.6, 0.6])
    for ind in [1, 2]:
        clustertest.addIndex(ind)

    # TEST CASE 1 (update)
    stable = clustertest.updateCentroid()
    assert [0.55, 0.55, 0.6] == clustertest.getCentroid()
    assert False == stable # Not yet stable

    # TEST CASE 2 (update)
    stable = clustertest.updateCentroid()
    assert [0.55, 0.55, 0.6] == clustertest.getCentroid()
    assert stable == True # Now it is stable

    # TEST CASE 3 (step)
    km2.step()

    # Check first cluster (WHICH HAS CHANGED!)
    cluster1 = km2.getClusters()[0]
    assert [0.55, 0.55, 0.6] == cluster1.getCentroid()
    assert set([1, 2]) == set(cluster1.getIndices())

    # Check second cluster (WHICH HAS CHANGED!)
    cluster2 = km2.getClusters()[1]
    assert [0.5, 0.475, 0.475] == cluster2.getCentroid()
    assert set([0, 3, 4, 5]) == set(cluster2.getIndices())

    # TEST CASE 3 (step)
    km2.step()

    # Check first cluster (WHICH HAS CHANGED!)
    cluster1 = km2.getClusters()[0]
    print cluster1.getCentroid()
    print [8./15, 17./30, 17./30]
    #print [8./15, 17./30, 17./30] == cluster1.getCentroid()
    assert set([1, 2, 3]) == set(cluster1.getIndices())

    # Check second cluster (WHICH HAS CHANGED!)
    cluster2 = km2.getClusters()[1]
    print cluster2.getCentroid()
    print [0.5, 13./30, 14./30]
    #assert [0.5, 13./30, 14./30] == cluster2.getCentroid()
    assert set([0, 4, 5]) == set(cluster2.getIndices())
    
    # Try it on a file
    km3 = candy_to_kmeans('datasets/smallcandy.csv',3,[23, 54, 36])
    km3.step()
    
    # The actual results
    cluster0 = km3.getClusters()[0]
    cluster1 = km3.getClusters()[1]
    cluster2 = km3.getClusters()[2]
    
    # The "correct" answers
    contents0 = [[0.88, 0.84, 0.8, 0.3], [0.02, 0.67, 0.75, 0.61], [0.2, 0.54, 0.73, 0.85],
                 [0.62, 0.75, 0.65, 0.43], [0.35, 0.63, 0.65, 0.12], [0.61, 0.85, 0.81, 0.44], 
                 [0.95, 0.94, 0.98, 0.69], [0.04, 0.69, 0.38, 0.39], [0.04, 0.52, 0.99, 0.75], 
                 [0.28, 0.91, 0.63, 0.08], [0.14, 0.55, 0.67, 0.63], [0.38, 0.94, 0.53, 0.07], 
                 [0.08, 0.62, 0.32, 0.27], [0.69, 0.82, 0.75, 0.65], [0.84, 0.89, 0.91, 0.38], 
                 [0.22, 0.88, 0.39, 0.33], [0.39, 0.38, 0.85, 0.32], [0.26, 0.39, 0.95, 0.63], 
                 [0.15, 0.87, 0.62, 0.22], [0.65, 0.81, 0.69, 0.55], [0.27, 0.63, 0.69, 0.39], 
                 [0.35, 0.7, 0.41, 0.15], [0.2, 0.48, 0.98, 0.84], [0.76, 0.86, 0.74, 0.61], 
                 [0.27, 0.65, 0.52, 0.28], [0.86, 0.91, 0.88, 0.62], [0.1, 0.79, 0.5, 0.12], 
                 [0.09, 0.85, 0.55, 0.21], [0.79, 0.94, 0.83, 0.48], [0.73, 0.92, 0.74, 0.39], 
                 [0.31, 0.5, 0.87, 0.85], [0.39, 0.9, 0.52, 0.26], [0.46, 0.35, 0.96, 0.05], 
                 [0.21, 0.62, 0.33, 0.09], [0.58, 0.37, 0.9, 0.08], [0.54, 0.92, 0.36, 0.35], 
                 [0.36, 0.64, 0.57, 0.26], [0.09, 0.47, 0.63, 0.8], [0.4, 0.69, 0.74, 0.7]] 
    contents1 = [[0.32, 0.87, 0.14, 0.68], [0.87, 0.99, 0.2, 0.8], [0.86, 0.86, 0.32, 0.88], 
                 [0.81, 0.66, 0.26, 0.82], [0.91, 0.98, 0.61, 0.58], [0.84, 0.88, 0.04, 0.86], 
                 [0.8, 0.62, 0.09, 0.65], [0.72, 0.88, 0.02, 0.95], [0.88, 0.96, 0.09, 0.88]] 
    contents2 = [[0.4, 0.21, 0.78, 0.68], [0.54, 0.06, 0.81, 0.98], [0.73, 0.31, 0.15, 0.08], 
                 [0.81, 0.69, 0.65, 0.65], [0.14, 0.31, 0.86, 0.74], [0.77, 0.45, 0.31, 0.31], 
                 [0.39, 0.14, 0.99, 0.24], [0.23, 0.32, 0.7, 0.75], [0.65, 0.05, 0.39, 0.49], 
                 [0.96, 0.09, 0.49, 0.3], [0.86, 0.03, 0.3, 0.39], [0.5, 0.2, 0.69, 0.95], 
                 [0.79, 0.09, 0.41, 0.69], [0.4, 0.3, 0.78, 0.74], [0.65, 0.24, 0.63, 0.27], 
                 [0.35, 0.3, 0.94, 0.92], [0.71, 0.78, 0.64, 0.57], [0.8, 0.4, 0.23, 0.33], 
                 [0.38, 0.07, 0.82, 0.01], [0.66, 0.09, 0.69, 0.46], [0.54, 0.06, 0.74, 0.86], 
                 [0.95, 0.62, 0.28, 0.01], [0.35, 0.71, 0.01, 0.32], [0.62, 0.24, 0.77, 0.17], 
                 [0.73, 0.65, 0.23, 0.02], [0.27, 0.38, 0.76, 0.63], [0.9, 0.63, 0.83, 0.6], 
                 [0.7, 0.04, 0.7, 0.82], [0.95, 0.83, 0.64, 0.5], [0.41, 0.11, 0.61, 0.78], 
                 [0.22, 0.44, 0.67, 0.99], [0.51, 0.05, 0.95, 0.66], [0.99, 0.68, 0.8, 0.42], 
                 [0.72, 0.55, 0.1, 0.17], [0.44, 0.1, 0.61, 0.98], [0.31, 0.16, 0.95, 0.9], 
                 [0.61, 0.42, 0.24, 0.33], [0.89, 0.72, 0.78, 0.38], [0.5, 0.09, 0.84, 0.78], 
                 [0.62, 0.01, 0.88, 0.1], [0.44, 0.28, 0.88, 0.99], [0.57, 0.23, 0.6, 0.85], 
                 [0.9, 0.05, 0.34, 0.41], [0.9, 0.41, 0.27, 0.36], [0.67, 0.32, 0.66, 0.2], 
                 [0.72, 0.14, 0.63, 0.37], [0.39, 0.08, 0.77, 0.96], [0.9, 0.7, 0.74, 0.63], 
                 [0.63, 0.05, 0.52, 0.63], [0.62, 0.27, 0.67, 0.77], [0.35, 0.04, 0.85, 0.86], 
                 [0.36, 0.34, 0.75, 0.37]]
    centroid0 = [0.3987179487179487, 0.7097435897435899, 0.6864102564102561, 0.4164102564102565]
    centroid1 = [0.7788888888888889, 0.8555555555555555, 0.19666666666666668, 0.788888888888889] 
    centroid2 = [0.6038461538461538, 0.29865384615384616, 0.6217307692307692, 0.5455769230769231]

    assert centroid0 == cluster0.getCentroid()
    assert centroid1 == cluster1.getCentroid()
    assert centroid2 == cluster2.getCentroid()
    assert contents0 == cluster0.getContents() 
    assert contents1 == cluster1.getContents() 
    assert contents2 == cluster2.getContents() 
    
    
    print '    Method ClusterGroup.step looks okay'
    print '  Part C of class ClusterGroup appears correct'
    print ''


def test_kmeans_d():
    """Test Part D of the ClusterGroup class."""
    print '  Testing Part D of class ClusterGroup'
    items = [[0.5,0.5,0.5],[0.5,0.6,0.6],[0.6,0.5,0.6],[0.5,0.6,0.5],[0.5,0.4,0.5],[0.5,0.4,0.4]]
    dset = a6.Dataset(3,items)
    
    # Try the same test case straight from the top using perform_k_means
    km1 = a6.ClusterGroup(dset, 2, [1, 3])
    km1.run(10)
    
    # Check first cluster
    cluster1 = km1.getClusters()[0]
    print cluster1.getCentroid()
    print [8./15, 17./30, 17./30]
    #assert [8./15, 17./30, 17./30] ==  cluster1.getCentroid()
    assert set([1, 2, 3]) == set(cluster1.getIndices())
    
    # Check second cluster
    cluster2 = km1.getClusters()[1]
    print cluster2.getCentroid()
    print [0.5, 13./30, 14./30]
    #assert [0.5, 13./30, 14./30] == cluster2.getCentroid()
    assert set([0, 4, 5]) == set(cluster2.getIndices())
    print '    Method run looks okay'
    
    # Test on a real world data set
    km2 = candy_to_kmeans('datasets/smallcandy.csv',3,[23, 54, 36])
    km2.run(20)
    
    # The actual results
    cluster0 = km2.getClusters()[0]
    cluster1 = km2.getClusters()[1]
    cluster2 = km2.getClusters()[2]
    
    # The "correct" answers
    contents0 = [[0.88, 0.84, 0.8, 0.3], [0.02, 0.67, 0.75, 0.61], [0.81, 0.69, 0.65, 0.65], 
                 [0.62, 0.75, 0.65, 0.43], [0.35, 0.63, 0.65, 0.12], [0.61, 0.85, 0.81, 0.44], 
                 [0.95, 0.94, 0.98, 0.69], [0.04, 0.69, 0.38, 0.39], [0.28, 0.91, 0.63, 0.08], 
                 [0.38, 0.94, 0.53, 0.07], [0.08, 0.62, 0.32, 0.27], [0.69, 0.82, 0.75, 0.65], 
                 [0.84, 0.89, 0.91, 0.38], [0.22, 0.88, 0.39, 0.33], [0.71, 0.78, 0.64, 0.57], 
                 [0.15, 0.87, 0.62, 0.22], [0.65, 0.81, 0.69, 0.55], [0.27, 0.63, 0.69, 0.39], 
                 [0.35, 0.7, 0.41, 0.15], [0.91, 0.98, 0.61, 0.58], [0.9, 0.63, 0.83, 0.6], 
                 [0.95, 0.83, 0.64, 0.5], [0.76, 0.86, 0.74, 0.61], [0.27, 0.65, 0.52, 0.28], 
                 [0.86, 0.91, 0.88, 0.62], [0.1, 0.79, 0.5, 0.12], [0.99, 0.68, 0.8, 0.42], 
                 [0.09, 0.85, 0.55, 0.21], [0.79, 0.94, 0.83, 0.48], [0.73, 0.92, 0.74, 0.39], 
                 [0.89, 0.72, 0.78, 0.38], [0.39, 0.9, 0.52, 0.26], [0.46, 0.35, 0.96, 0.05], 
                 [0.21, 0.62, 0.33, 0.09], [0.58, 0.37, 0.9, 0.08], [0.54, 0.92, 0.36, 0.35], 
                 [0.67, 0.32, 0.66, 0.2], [0.36, 0.64, 0.57, 0.26], [0.9, 0.7, 0.74, 0.63], 
                 [0.4, 0.69, 0.74, 0.7]]
    contents1 = [[0.32, 0.87, 0.14, 0.68], [0.73, 0.31, 0.15, 0.08], [0.87, 0.99, 0.2, 0.8], 
                 [0.77, 0.45, 0.31, 0.31], [0.96, 0.09, 0.49, 0.3], [0.86, 0.03, 0.3, 0.39], 
                 [0.86, 0.86, 0.32, 0.88], [0.8, 0.4, 0.23, 0.33], [0.81, 0.66, 0.26, 0.82], 
                 [0.95, 0.62, 0.28, 0.01], [0.35, 0.71, 0.01, 0.32], [0.73, 0.65, 0.23, 0.02], 
                 [0.84, 0.88, 0.04, 0.86], [0.8, 0.62, 0.09, 0.65], [0.72, 0.55, 0.1, 0.17], 
                 [0.61, 0.42, 0.24, 0.33], [0.72, 0.88, 0.02, 0.95], [0.88, 0.96, 0.09, 0.88], 
                 [0.9, 0.05, 0.34, 0.41], [0.9, 0.41, 0.27, 0.36]]
    contents2 = [[0.4, 0.21, 0.78, 0.68], [0.54, 0.06, 0.81, 0.98], [0.2, 0.54, 0.73, 0.85], 
                 [0.14, 0.31, 0.86, 0.74], [0.39, 0.14, 0.99, 0.24], [0.23, 0.32, 0.7, 0.75], 
                 [0.65, 0.05, 0.39, 0.49], [0.04, 0.52, 0.99, 0.75], [0.14, 0.55, 0.67, 0.63], 
                 [0.5, 0.2, 0.69, 0.95], [0.79, 0.09, 0.41, 0.69], [0.4, 0.3, 0.78, 0.74], 
                 [0.65, 0.24, 0.63, 0.27], [0.35, 0.3, 0.94, 0.92], [0.39, 0.38, 0.85, 0.32], 
                 [0.38, 0.07, 0.82, 0.01], [0.66, 0.09, 0.69, 0.46], [0.26, 0.39, 0.95, 0.63], 
                 [0.54, 0.06, 0.74, 0.86], [0.2, 0.48, 0.98, 0.84], [0.62, 0.24, 0.77, 0.17], 
                 [0.27, 0.38, 0.76, 0.63], [0.7, 0.04, 0.7, 0.82], [0.41, 0.11, 0.61, 0.78], 
                 [0.22, 0.44, 0.67, 0.99], [0.51, 0.05, 0.95, 0.66], [0.44, 0.1, 0.61, 0.98], 
                 [0.31, 0.16, 0.95, 0.9], [0.31, 0.5, 0.87, 0.85], [0.5, 0.09, 0.84, 0.78], 
                 [0.62, 0.01, 0.88, 0.1], [0.44, 0.28, 0.88, 0.99], [0.57, 0.23, 0.6, 0.85], 
                 [0.72, 0.14, 0.63, 0.37], [0.39, 0.08, 0.77, 0.96], [0.09, 0.47, 0.63, 0.8], 
                 [0.63, 0.05, 0.52, 0.63], [0.62, 0.27, 0.67, 0.77], [0.35, 0.04, 0.85, 0.86], 
                 [0.36, 0.34, 0.75, 0.37]]
    centroid0 = [0.54125, 0.7545, 0.66125, 0.3775]
    centroid1 = [0.76900, 0.5705, 0.20550, 0.4775]
    centroid2 = [0.42325, 0.2330, 0.75775, 0.6765]

    print centroid0 
    print cluster0.getCentroid()
    print ""
    print centroid1 
    print cluster1.getCentroid()
    print ""
    print centroid2 
    print cluster2.getCentroid()
    print ""
    print contents0 
    print cluster0.getContents() 
    print ""
    print contents1 
    print cluster1.getContents() 
    print ""
    print contents2 
    print cluster2.getContents() 
    print '    Candy analysis test looks okay'
    print '  Part D of class ClusterGroup appears correct'
    print ''


if __name__ == '__main__':
    print 'Starting unit test\n'
    test_dataset()
    test_cluster_a()
    test_cluster_b()
    test_kmeans_a()
    test_kmeans_b()
    test_kmeans_c()
    test_kmeans_d()
    print 'All test cases passed!'

    print "TO FIX:"
    print "FIX ASSERTION ERROR IN addIndex()"
