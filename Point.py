'''
 ***************************************************************************** 
 * PURPOSE
 *     Provide a point in lat/long
 ***************************************************************************** 
 * MODIFICATIONS
 * @author JL Sowers Apr 28, 2023
 ***************************************************************************** 
 *  DESIGN NOTES:
 *  
 ***************************************************************************** 
'''
import math

class Point():
    
    def __init__(self, *args):
        self.RADIUS = 10.0       
        if len(args) == 2:
            self.lat = args[0]
            self.lon = args[1]

            self.x = self.RADIUS
            self.x *= math.cos(self.toRadians(self.lon)) * math.cos(self.toRadians(self.lat))
            self.y = self.RADIUS
            self.y *= math.sin(self.toRadians(self.lon)) * math.cos(self.toRadians(self.lat))
            self.z = self.RADIUS * math.sin(self.toRadians(self.lat))
        elif len(args) == 3:
            self.x = args[0]
            self.y = args[1]
            self.z = args[2]
            self.lat = self.toDegrees(math.asin(self.z / self.RADIUS))
            self.lon = self.toDegrees(math.atan2(self.y, self.x));
        
    def toRadians(self, deg):
        return math.pi * deg / 180.0
    
    def toDegrees(self,rad):
        return 180.0 * rad / math.pi
    
    def normalize(self,  aLon):
        while (aLon < -180.0):
            aLon += 360.0;
        while (aLon > 180.0):
            aLon -= 360.0;
        return aLon;

    def toString(self):
        slat = str(self.lat)
        slon = str(self.lon)
        sx = str(self.x)
        sy = str(self.y)
        sz = str(self.z)
        astr = "lat=" + slat + ", lon=" + slon + ", x=" + sx + ", y=" + sy + ", z=" + sz
        return astr

    def __eq__(self, other):
        """
            Compares this point to another point.  If this point's lat and lon are the
            same as the other point's lat and long, then they are equal.  An exception
            is made if both lats are equal to 90 or -90.
        """
        if isinstance(other, Point):
            res = ((self.lat == other.lat) and (self.lon == other.lon)) or (self.lat == 90.0 and other.lat == 90.0) or (self.lat == -90.0 and other.lat == -90.0)
            return res
        return NotImplemented
    
    def getLatitude(self):
        return self.lat
    
    def getLongitude(self):
        return self.lon
    
    def setLatitude(self, alat):
        self.lat= alat
    
    def setLongitude(self, alon):
        self.lon = alon


    