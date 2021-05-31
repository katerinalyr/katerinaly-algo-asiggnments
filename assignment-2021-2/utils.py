import string
from itertools import chain, combinations

class Line:
    def __init__(self,a,b):
        self.x = a
        self.y = b
        self.points = set([a,b])
        return
    def addPoint(self,c):
    #    print("added point",c,self.points[0],self.points[1])
        self.points.add(c)
    def is_colinear(self,c):
        # To check if c is collinear we have to determine the following equation
        # a(n-y) + m(y-b) + x(b-n) = 0
        # Where (a,b), (m,n), (x,y) are the three points
        a = self.x[0]
        b = self.x[1]
        m = self.y[0]
        n = self.y[1]
        x = c[0]
        y = c[1]

        eq = a*(n-y) + m*(y-b) + x*(b-n)
        #print(eq)

        if eq == 0:
            return True
        else:
            return False

    # Returns true if point b is coaxial to x
    # Only when :
    # (x,y) = (x,y')
    # or (x,y) = (x',y)
    def is_coaxial(self,b):
        for p in self.points:
            if (p[0] == b[0]) or (p[1] == b[1]):
                continue
            else:
                return False
        return True
    def __str__(self):
        str = ""
        for p in self.points:
            str = str + "{} ".format(p)
        return str

def parseFile(points_file):
    with open(points_file) as f:
        lines = [line.rstrip() for line in f]
        points = []
        for line in lines:
            coords = line.split(' ')
            point = (int(coords[0]),int(coords[1]))
            points.append(point)
        #print(points)
    return points

# We solve greedily using only lines parallel to xx',yy'
def solveParallel(points):
    nrpoints = len(points)
    lines = []


    covered = set([])
    left = points
    all = set(points)

    while(len(covered) < nrpoints):
        max = -1
        maxLine = Line(0,0)
        for i in range(len(left)):
            line = Line(left[i],left[i])
            count = 0
            for p in left:
                if line.is_coaxial(p):
                    count += 1
                    line.addPoint(p)
            if count > max :
                maxLine = line
                max = count

        covered = covered.union(list(maxLine.points))
        left = list(all.difference(covered))
        lines.append(maxLine)
        #print(len(covered),nrpoints,left)

    return lines


def solve(points):
    nrpoints = len(points)
    lines = []


    covered = set([])
    left = points
    all = set(points)

    while(len(covered) < nrpoints):
        max = -1
        maxLine = Line(0,0)
        for i in range(len(left)):
            p1 = left[i]
            for j in range(i+1,len(left)):
                p2 = left[j]
                line = Line(p1,p2)
                count = 0
                for p in left:
                    if line.is_colinear(p):
                        count += 1
                        line.addPoint(p)
                if count > max :
                    maxLine = line
                    max = count

        covered = covered.union(list(maxLine.points))
        left = list(all.difference(covered))
        lines.append(maxLine)
        #print(len(covered),nrpoints,left)

    return lines

def covers_all(mset,points):
    all = set([])
    for line in mset:
        all = all.union(set(line.points))

    #print(len(all),len(points))
    if all == set(points):
        return True
    return False

def brute(points):
    # We calculate the powerset of the given set of
    # points to find all the possible combinations of lines
    # We have to check that all points of the selected line
    # are collinear
    pset = chain.from_iterable(combinations(points, r) for r in range(len(points)+1))

    # We keep only the sets that all points are collinear
    lines = []
    for s in pset:
        if len(s) < 2:
            continue
        l = Line(s[0],s[1])
        flag = True
        for p in s:
            if l.is_colinear(p):
                l.addPoint(p)
            else:
                flag = False
        if flag:
            lines.append(l)

    # We calculate the powerset of the set of lines
    pset2 = chain.from_iterable(combinations(lines, r) for r in range(len(lines)+1))

    minS = set()
    for s in pset2:
        if covers_all(s,points):
            minS = s
            break;


    return minS
