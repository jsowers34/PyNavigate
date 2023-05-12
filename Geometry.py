'''
 ***************************************************************************** 
 * PURPOSE
 *     Provide some convenient geometric methods.
 ***************************************************************************** 
 * MODIFICATIONS
 * @author JL Sowers Apr 28, 2023
 ***************************************************************************** 
 *  DESIGN NOTES:
 *  
 ***************************************************************************** 
'''
from com.rff.pynavigate.Stack import Stack
from com.rff.pynavigate.Point import Point
from com.rff.pynavigate.NavCommon import NavCommon
import math
from com.rff.pynavigate import Orientation

class Geometry(NavCommon):
    ORIENTATION = Orientation
   
    def selectFirstPoint(self, thePoints):
        """
         Select the point furthest to the West.  If more than 1 share the
         westward longitude, then select the southernmost point.
        """
        ix = 0
        count = 0
        numberPoints = len(thePoints)
        westIx = []
        p0 =  thePoints[0]
        westIx.append(0)
        for i in range(1, numberPoints-1):
            p = thePoints[i]
            if p0.getLongitude() > p.getLongitude():
                p0 = p
                ix = i
            elif p0.getLongitude() == p.getLongitude():
                count = count + 1
                westIx[count] = i
        if count > 0:
            p0 = thePoints[westIx[0]]
            
        for i in range(0, count):
            p = thePoints[westIx[i]]
            if p0.getLatitude() > p.getLatitude():
                ix = westIx[i]
                p0 = thePoints[ix]
        return ix;

    def isLeft(self, theStart, theEnd, thePoint):
        """ Tests if a point is Left of an infinite line. """
        test = (theEnd.getLongitude()-theStart.getLongitude())*(thePoint.getLatitude() - theStart.getLatitude())-(thePoint.getLongitude() - theStart.getLongitude())*(theEnd.getLatitude() - theStart.getLatitude())
        return test > 0.0
    
    def grahamScan(self, thePoints):
        stack = Stack();
        stack.push(thePoints[0])
        stack.push(thePoints[1])
        i = 2;
        while i < len(thePoints):
            # Get top 2 points on stack (pop'em & put'em back)
            pt1 = stack.pop();
            pt2 = stack.pop();
            stack.push(pt2);
            stack.push(pt1);
            if self.isLeft(pt1, pt2, thePoints[i]):
                stack.pop()
            stack.push(thePoints[i])
            i = i + 1
        # the Stack now has the convex hull
        hull = []
        while not stack.empty():
            hull.append(stack.pop());
        
        hull.reverse()
        return hull
    
    def orderByAngle(self, thePoints):
        """ Reorders the points so that they are in a counter-clockwise order. """
        temp = []
        ix0 = self.selectFirstPoint(thePoints);
        p0  = thePoints[ix0]
        
        # Put points in temp using an insertion sort such that the sort criterion
        # is the bearing angle from p0 (largest angle first)
        bearings = [None]*len(thePoints)
        for i in range(0, len(thePoints)):
            p1 = thePoints[i]
            if i == ix0:
                bearings[i] = +9999.9;  # insure this point is first
            else:
                bearings[i] = self.calculateHeading(p0, p1);
                
            if bearings[i] > 180.0:
                bearings[i] -= 360.0
                
        count = len(bearings)
        while count > 0:
            ix = 0;
            for i in range(0, len(bearings)):
                if bearings[ix] < bearings[i]:
                    ix = i

            # We are left with the index of the largest bearing.  Replace the value
            # with a -9999. and put the corresponding point in temp
            bearings[ix] = -9999.9
            temp.append(thePoints[ix])
            count = count - 1
        return temp;
    
    def angleSort(self, thePoints):
        """ 
            Sort by increasing angle using the orientation method avoiding computation of
            angles.
        """
        alist = thePoints
        #print(self.showPoints(alist)) # DEBUG
        ix0 = self.selectFirstPoint(alist);
        p0  = alist[ix0]    # Select westmost point
        del alist[ix0]      # Remove that point from list  
        p1 = alist[0]
        inside = 0
        temp = []
        for outside in range(1, len(alist)):
            p2 = alist[outside]
            #print(inside, outside, self.showPoint(p2))
            inside = outside
            #print(self.showOrientationPoints(p0, p1, p2), end = '') #debug
            orient = self.orientation(p0, p1, p2)
            # print(orient) #debug
            while (inside > 0) and (orient == Orientation.Orientation.CW):
                temp = alist[inside-1]
                del alist[inside]
                alist.insert(inside, temp)
                inside = inside - 1
            del alist[inside]
            alist.insert(inside, p1)
            p1 = p2
        alist.insert(0, p0)
        return alist;
   
    def calculateHeading(self, aStartPosition, anEndPosition):
        lat_error = 0.00005
        long_error = 0.000005
        ln_term = 0.0

        #  initialize bearings
        abs_bearing = 0.0
        source_lat = self.toRadians(aStartPosition.getLatitude())
        source_long = self.toRadians(aStartPosition.getLongitude())
        target_lat = self.toRadians(anEndPosition.getLatitude());
        target_long = self.toRadians(anEndPosition.getLongitude());
        
        # check if tracks are above 85 degrees latitude
        if (abs(source_lat) > self.RAD_85 or abs(target_lat) > self.RAD_85):
            raise Exception("Track above or below 85 degrees latitude.")
        else:
            # calc change in latitude and longitude
            del_lat = target_lat - source_lat;
            del_long = target_long - source_long;
            
        # Normalize
        if (del_long > self.RAD_180):
            del_long = del_long - self.RAD_360
        elif (del_long < -self.RAD_180):
            del_long = del_long + self.RAD_360;
            
        # check for headings of +/- pi_over_2
        if (abs(del_lat) < lat_error):
            if (del_long >= 0.0):
                abs_bearing = self.RAD_90
            else:
                abs_bearing = -self.RAD_90
        elif (abs(del_long) < long_error):
            if (target_lat >= source_lat):
                abs_bearing = 0.0
            else:
                abs_bearing = self.RAD_180
        else:
            # calculate the angle in radians
            t_term = math.tan(self.RAD_45 + target_lat / 2.0) / math.tan(self.RAD_45 + source_lat / 2.0)
            ln_term = math.log(t_term)
            abs_bearing = math.atan(del_long / ln_term);
        
        # convert to the proper quadrant
        if (ln_term < 0.0):
            if (del_long > 0.0):
                abs_bearing += self.RAD_180
            else:
                abs_bearing -= self.RAD_180;

        bearing = self.toDegrees(abs_bearing)
        return bearing;


    def orientation(self, the1st, the2nd, the3rd):
        det = the1st.getLongitude()*(the2nd.getLatitude()-the3rd.getLatitude()) \
            - the2nd.getLongitude()*(the1st.getLatitude() - the3rd.getLatitude()) \
            + the3rd.getLongitude() * (the1st.getLatitude() - the2nd.getLatitude())
        if det < 0.0:
            res = Orientation.Orientation.CW.name
        elif det > 0.0:
            res = Orientation.Orientation.CCW.name
        else: 
            res = Orientation.Orientation.COLL.name
        return res

    def showPoint(self, thePt):
        astr = "[" + str(thePt.getLatitude()) + ", " + str(thePt.getLongitude()) + "]" 
        return astr
    
    def showPoints(self, theList):
        astr= "["
        num = len(theList) - 1
        for i in range(0, num):
            value = self.showPoint(theList[i])
            astr += str(value) + ", "                 
        astr += str(self.showPoint(theList[num])) + "]"
        return astr
    
    def showOrientationPoints(self, p0, p1, p2):
        astr = "Orientation of " + self.showPoint(p0) + "--> "
        astr += self.showPoint(p1) + " --> " + self.showPoint(p2) + " is "
        return astr
    
    
    