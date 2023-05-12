'''
 ***************************************************************************** 
 * PURPOSE
 *     A set of Common Constants and methods
 ***************************************************************************** 
 * MODIFICATIONS
 * @author JL Sowers May 1, 2023
 ***************************************************************************** 
 *  DESIGN NOTES:
 *  
 ***************************************************************************** 
'''
import math
import com.rff.pynavigate.NavError as NavError

class NavCommon(object):   
    C_MS_PER_NM = 6.177606
    HR_PER_SEC = 2.777777778e-4
    INDEX_REF_SEA = 1.000338
    LAT_TOLERANCE = 1.483529864
    NM_PER_RADIAN = 3437.74677078
    NM_PER_DEGREE = 60.0
    FT_PER_NM = 6076.1
    PI = math.pi
    PI_OVER_2 = 1.570796327
    PI_OVER_180 = PI / 180.0
    RAD_TO_DEGREE = 180.0 / PI
    DEGREE_TO_RAD = PI_OVER_180
    PI2 = 6.283185307
    RADIANS_PER_NM = 0.00029080
    RAD_45 = 0.785398163
    RAD_85 = 1.483529864
    RAD_90 = PI_OVER_2
    RAD_180 = PI
    RAD_270 = 4.712389
    RAD_360 = PI2;
    EARTH_RADIUS_NM = 3444.0
    RAD_FIVE_MILES = 0.001455825
    
    def toRadians(self, deg):
        return self.PI_OVER_180 * deg 
    
    def toDegrees(self, rad):
        return rad / self.PI_OVER_180
    
    def signum(self, x):
        return (x > 0) - (x < 0)
    
    def truncate(self, f, n):
        return math.floor(f * 10 ** n) / 10 ** n
    
    def dms2dec(self, dms):
        """ Deg-Min-Sec (list) to Decimal Degree """
        deg,xmin,sec = dms
        result = deg + xmin/60.0 + sec/3600.0
        return result
    
    def dec2dms(self,dec):
        """ Decimal Degree to Deg-Min-Sec (list) """
        decdeg = abs(dec)
        ideg = int(decdeg)
        d = (decdeg - ideg)
        imin = int(d * 60.0)
        sec = self.truncate((d * 60.0 - imin)*60.0 + 5.0E-8, 7)
        result = [ideg, imin, sec]
        return result
    
    def hrs2hms(self,hrs):
        """ Decimal Hours to Hour-Min-Sec (list) """
        ihr, imn, isc = self.dms2dec(hrs)
        if(ihr >= 24):
                NavError("Hours is greater than 24")
        return [ihr, imn, isc]
    
    def hms2hrs(self, hms):
        """ Hrs-Min-Sec (list) to Decimal Hours """
        return self.dms2dec(hms)
    
    def normalizeDMS(self, dms):
        ideg, imin, sec = dms
        sgn = self.signum(ideg)
        isec = int(sec)
        if(isec >= 60):
            a = isec/60
            imin = imin + a
            sec = sec - 60*a
            
        if(imin >= 60):
            a = int(imin/60)
            ideg = abs(ideg) + a

        ideg = ideg * sgn
        result = [ideg, imin, sec]
        return result
    
    def normalizeHMS(self, hms):
        return self.normalizeDMS(hms)
        
    
if __name__ == '__main__':
    nav = NavCommon()
    test1 = [75, 30, 0]
    test2 = [74, 1, 0]
    test3 = [74, 0, 60]
    test4 = [-74, 30, 0]
    print("DMS to Decimal Degree:")
    decdeg1 = nav.dms2dec(test1)
    print(str(test1) + " --> " + str(decdeg1))
    decdeg2 = nav.dms2dec(test2)
    print(str(test2) + " --> " + str(decdeg2))
    decdeg3 = nav.dms2dec(test3)
    print(str(test3) + " --> " + str(decdeg3))
    decdeg4 = nav.dms2dec(test4)
    print(str(test4) + " --> " + str(decdeg4))
    # Now reverse
    print("Decimal Degree to DMS:")
    print(str(decdeg1) + " --> " + str(nav.dec2dms(decdeg1)))
    print(str(decdeg2) + " --> " + str(nav.dec2dms(decdeg2)))
    print(str(decdeg3) + " --> " + str(nav.dec2dms(decdeg3)))
    print(str(decdeg4) + " --> " + str(nav.dec2dms(decdeg4)))