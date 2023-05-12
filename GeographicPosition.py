'''
 ***************************************************************************** 
 * PURPOSE
 * 
 ***************************************************************************** 
 * MODIFICATIONS
 * @author JL Sowers Apr 28, 2023
 ***************************************************************************** 
 *  DESIGN NOTES:
 *  
 ***************************************************************************** 
'''
class GeographicPosition():
    
    def __init__(self, *args):
        if(len(args) > 0):
            self.latitude = args[0]
            self.longitude = args[1]
        else:
            self.latitude = 0.0
            self.longitude = 0.0
            
    def setLatitude(self, newlat):
        self.latitude = newlat
        
    def setLongitude(self, newlon):
        self.longitude = newlon
        
    def getLatitude(self):
        return self.latitude
    
    def getLongitude(self):
        return self.longitude
    
    def toString(self):
        astr = "Latitude: " + str(self.latitude) +  ";  Longitude: " + str(self.longitude)
        return astr

    def __eq__(self, other):
        """
            Compares this location to another location.  If this location's lat and lon are the
            same as the other location's lat and long, then they are equal.  An exception
            is made if both latitudes are equal to 90 or -90.
        """
        if isinstance(other, GeographicPosition):
            res = ((self.latitude == other.latitude) and (self.longitude == other.longitude)) or (self.latitude == 90.0 and other.latitude == 90.0) or (self.latitude == -90.0 and other.latitude == -90.0)
            return res
        return NotImplemented