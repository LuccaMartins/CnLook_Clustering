import numpy as np

class Cluster:
    '''
    __init()__ Creates a new Cluster.
    Parameters
    label The cluster label, which should be globally unique
    parent The cluster which split to create this cluster
    birthLevel The MST edge level at which this cluster first appeared
    numPoints The initial number of points in this cluster
    '''
    
    def __init__(self, label, parent, birthLevel, numPoints):
        self.label = label
        self.birthLevel = birthLevel
        self.deathLevel = 0
        self.numPoints = numPoints
        
        # store unsupervised measures informatin
        self.stability = 0.0
        self.propagatedStability = 0
        self.propagatedLowestChildDeathLevel = np.Inf
        self.virtualChildCluster = []

        
        # Store objects ids information
        self.numberofLabeledInNode = 0
        self.objects = []
        
        self.parent = parent
        
        self.hasChildren = False
        
        if self.parent != None:
            self.parent.hasChildren = True
            
        
        self.propagatedDescendants = []
        self.children = []
    
    
    ''' --------------------- Public methods ---------------------'''
    ''' detachPoints
    Removes the specified number of points from this cluster at the given edge level, which will
    update the stability of this cluster and potentially cause cluster death.  If cluster death
    occurs, the number of constraints satisfied by the virtual child cluster will also be calculated.    
    numPoints The number of points to remove from the cluster
    level the dendrogram level removed from the dendrogram structure
     '''
    
    def detachPoints(self, numPoints, level):
        self.numPoints -= numPoints
        self.stability += (numPoints * (self.birthLevel-level))
        
        if self.numPoints == 0:
            self.deathLevel = level
        elif self.numPoints < 0:
            raise Exception("Cluster cannot have less than 0 points.")
    
    
    ''' propagate
    This cluster will propagate itself to its parent if its number of satisfied constraints is
    higher than the number of propagated constraints.  Otherwise, this cluster propagates its
    propagated descendants.  In the case of ties, stability is examined.
    Additionally, this cluster propagates the lowest death level of any of its descendants to its
    parent.
    '''
    
    def propagate(self):
                
        if self.parent != None:
            if self.propagatedLowestChildDeathLevel == np.Inf:
                self.propagatedLowestChildDeathLevel = self.deathLevel
            
            
            if self.propagatedLowestChildDeathLevel < self.parent.propagatedLowestChildDeathLevel:
                self.parent.propagatedLowestChildDeathLevel = self.propagatedLowestChildDeathLevel
            
            
            if not self.hasChildren:
                self.parent.propagatedStability += self.stability
                self.parent.propagatedDescendants.append(self)
            
            else:
                if self.stability >= self.propagatedStability:
                    self.parent.propagatedStability += self.stability
                    self.parent.propagatedDescendants.append(self)
                else:
                    self.parent.propagatedStability += self.propagatedStability
                    self.parent.propagatedDescendants = (self.parent.propagatedDescendants + self.propagatedDescendants)
    
    '''
    addPointsToVirtualChildCluster
    Updating cluster node after emerging a virtual child cluster
    '''
    
    def addPointsToVirtualChildCluster(self, points):
        self.virtualChildCluster = (self.virtualChildCluster + points).copy()
    
    
    '''
    virtualChildClusterContaintsPoint
    Check if a virtual child cluster contains a specific point
    '''
    def virtualChildClusterContaintsPoint(self, point):
        return (point in self.virtualChildCluster)
    
    '''
    addChild
    add constraint satisfaction for a cluster node
    '''
    def addChild(self, ch):
        self.children.append(ch)
    
    '''
    releaseVirtualChildCluster
    Sets the virtual child cluster to null, thereby saving memory.
    Only call this method after computing the number of constraints
    satisfied by the virtual child cluster.
     '''
    def releaseVirtualChildCluster(self):
        self.virtualChildCluster = []
    
    def releaseCluster(self):
        self.propagatedStability = 0
        self.propagatedLowestChildDeathLevel = np.Inf
        
        self.propagatedDescendants = []
    
    ''' ------------------ Getters and setters ------------------ '''
    
    def getLabel(self):
        return self.label
    
    def getParent(self):
        return self.parent
    
    def getBirthLevel(self):
        return self.birthLevel
    
    def getDeathLevel(self):
        return self.deathLevel
    
    def getStability(self):
        return self.stability
    
    def getPropagatedStability(self):
        return self.propagatedStability
    
    def getPropagatedLowestChildDeathLevel(self):
        return self.propagatedLowestChildDeathLevel
    
    def getPropagatedDescendants(self):
        return self.propagatedDescendants
    
    def _hasChildren(self):
        return self.hasChildren
    
    def getChildren(self):
        return self.children
    
    def getObjects(self):
        return self.objects
    
    def setObjects(self, objects):
        self.objects = objects.copy()
        
    def getClassDistribution(self):
        return self.classDistributionInNode
    
    
    def __str__(self):
        if self.parent != None:
            return "\nId: " + str(self.label) + " Parent: " + str(self.parent.label) + " Stability: " + "{:.4f}".format(self.stability) + " isLeaf? " + str(not self.hasChildren) + " Birth Level: " + "{:.4f}".format(self.birthLevel) + " Death Level: " + "{:.4f}".format(self.deathLevel) + " Num obj: " + str(len(self.objects))
        else:
            return "\nId: " + str(self.label) + " isLeaf? " + str(not self.hasChildren) + " Birth Level: Inf" + " Death Level: " + "{:.4f}".format(self.deathLevel) + " Num obj: " + str(len(self.objects))
        
    
    def __repr__(self):
        return str(self)
        