'''
 ***************************************************************************** 
 * PURPOSE
 *     Navigational Utilities
 *        Great Circle Computations
 *
 ***************************************************************************** 
 * MODIFICATIONS
 * @author JL Sowers Apr 30, 2023
 ***************************************************************************** 
 *  DESIGN NOTES:
 *      Translated from Java version (fortran -> c -> C++ -> Java -> Python3)
 ***************************************************************************** 
'''
import math
import sys
from enum import Enum
from NavCommon import NavCommon
from NavError import NavError
from CPA_Data import CPAData
from CPA_Data import CPA_State
from GeographicPosition import GeographicPosition

class BearingType(Enum):
    ABSOLUTE = 1
    RELATIVE = 2
    
class NavUtils(NavCommon):

    def GreatCircle(self, aLatitude, aLongitude, aCourse, aDistance):
        """
        This procedure will calculate the new position of a given track as
        a result of the distance traveled over the given distance.
        
        The great circle route is approximated by a series of rhumb lines as
        a function of latitude.  The rhumb line equations cannot be used at
        high latitudes, in which case, the actual great circle computations
        must be made.  The use of either the rhumb line or great circle
        equations is determined by a latitude tolerance.
        The rhumb line equations were taken from Dutton's Navigation and Piloting (Maloney).

        The great circle equations were derived from the American Practical Navigator (Bowditch).
        """
        eff_rad_0 = 0.000005
        
        sin_crs = math.sin(self.toRadians(aCourse))
        cos_crs = math.cos(self.toRadians(aCourse))

        sin_lat = math.sin(self.toRadians(aLatitude))
        cos_lat = math.cos(self.toRadians(aLatitude))

        cos_dist = math.cos(self.toRadians(aDistance / self.NM_PER_DEGREE))
        sin_dist = math.sin(self.toRadians(aDistance / self.NM_PER_DEGREE))

        new_lat = math.asin(cos_dist * sin_lat + cos_crs * sin_dist * cos_lat)

        delta_long = math.atan(sin_dist * sin_crs / (cos_dist * cos_lat - sin_dist *  cos_crs * sin_lat))

        # Perform course update
        sin_new_crs = sin_crs * cos_lat / math.cos(new_lat)
        
        if (abs(sin_new_crs) > 1.0):
            sin_new_crs = 1.0

        cos_new_crs = math.sqrt(1.0 - sin_new_crs * sin_new_crs)
        
        # Vertex of great circle check
        if ((math.sin(new_lat) * cos_dist - sin_lat) < 0.0):
            cos_new_crs = -(cos_new_crs)

        new_crs = math.acos(cos_new_crs)

        if (self.toRadians(aCourse) < 0.0):
            new_crs = -(new_crs)

        new_long = self.toRadians(aLongitude)
        
        # Check for polar crossing
        if (abs(self.toRadians(aCourse)) < eff_rad_0 or (abs(self.toRadians(aCourse) - self.RAD_180) < eff_rad_0)):
            if (abs(new_crs - self.toRadians(aCourse)) > self.RAD_90):
                if(self.toRadians(aLongitude) < 0.0):
                    adjustment = self.RAD_180
                else:
                    adjustment = -self.RAD_180
                new_long += adjustment
        
        # Normalize longitude
        new_long += delta_long;

        if (abs(new_long) >= self.RAD_180):
            new_long -= self.RAD_360 * self.signum(new_long)

        result = GeographicPosition(self.toDegrees(new_lat), self.toDegrees(new_long))
        return result;
    
    def NewPositionLatitude(self, start, bearing, distance):
        """ 
            Given an initial Geographic Position, a bearing/course and a distance (in nm),
            compute the latitude of the new position.
        """
        newPositionLat = 0.0
        if(bearing == 0.0 or bearing == 180.0 or bearing == 360.0):
            if(bearing == 180.0):
                newPositionLat = start.getLatitude() - distance/60.0
            else: 
                newPositionLat = start.getLatitude() + distance/60.0
        else:
            a = self.toRadians(90.0 - start.getLatitude())
            b = self.toRadians(distance/60.0)
            cAngle = self.toRadians(bearing)
            aPlusB = 2.0*math.atan(math.cos((a-b)/2.0) / (math.cos((a+b)/2.0)*math.tan(cAngle/2.0)))
            aMinusB = 2.0*math.atan(math.sin((a-b)/2.0) / (math.sin((a+b)/2.0)*math.tan(cAngle/2.0)))
            bAngle = (aPlusB - aMinusB)/2.0
            x = self.toDegrees(math.asin(self.truncate(math.sin(b)*math.sin(cAngle)/math.sin(bAngle),10))) - 90.0
            if(start.getLatitude() < 0.0):
                newPositionLat = x
            else: 
                newPositionLat = abs(x)
    
        if(newPositionLat > 90.0):
            newPositionLat -= 90.0
        elif(newPositionLat < - 90.0):
            newPositionLat = -(newPositionLat + 180.0)
        return newPositionLat;
    
    def NewPositionLongitude(self, start, bearing, distance):
        """ 
            Given an initial Geographic Position, a bearing/course and a distance (in nm),
            compute the longitude of the new position.
        """
        a = self.toRadians(90.0 - start.getLatitude())
        b = self.toRadians(distance/60.0)
        cAngle = self.toRadians(bearing)
        aPlusB = 2.0*math.atan(math.cos((a-b)/2.0) / (math.cos((a+b)/2.0)*math.tan(cAngle/2.0)))
        aMinusB = 2.0*math.atan(math.sin((a-b)/2.0) / (math.sin((a+b)/2.0)*math.tan(cAngle/2.0)))
        bAngle = (aPlusB - aMinusB)/2.0
    
        newPositionLon = start.getLongitude() + self.toDegrees(bAngle)
        if(newPositionLon > 180.0):
            newPositionLon -= 180.0
        elif(newPositionLon < -180.0):
            newPositionLon += 360.0
        return newPositionLon
    
    def GreatCircleRange(self, aStartPosition, anEndPosition):
        """ 
            Given starting and ending geographic positions, computes the distance (in degrees) between
            the two points.  Distance may be converted tp NM by multiplying by 60.0
        """
        source_lat = self.toRadians(aStartPosition.getLatitude())
        source_long = self.toRadians(aStartPosition.getLongitude())
        tgt_lat = self.toRadians(anEndPosition.getLatitude())
        tgt_long = self.toRadians(anEndPosition.getLongitude())

        #  compute delta lat and delta long
        delta_lat  = source_lat - tgt_lat
        delta_long = source_long - tgt_long

        #  normalize longitude
        if (delta_long > self.RAD_180):
            delta_long = delta_long - self.RAD_360
        elif (delta_long < -self.RAD_180):
            delta_long = delta_long + self.RAD_360
         
        #  compute great circle distance
        arange = math.cos(delta_lat) - (1.0 - math.cos(delta_long)) * math.cos(source_lat) * math.cos(tgt_lat)   
    
        if (abs(arange) >= 1.0):
            arange = 0.0
        else:
            arange = abs(math.acos(arange))
        
        #  check if distance is under five miles;  if so, use a linear approximation
        if (arange < self.RAD_FIVE_MILES):
            arange = math.sqrt(delta_lat * delta_lat + delta_long * delta_long * math.cos(source_lat) * math.cos(tgt_lat))
    
        return arange * self.RAD_TO_DEGREE
    
    def rhumb_line(self, aLatitude, aLongitude, theCourse, aDistance):
        """
            For mid-latitudes, the simple rhumb line equations are used to update
            the rhumb line route.  For high latitudes , the great circle
            equations are used without updating the course.  The use of either
            the rhumb line or great circle equations is determined by a latitude tolerance.
        """
        def_denom = 0.00000001   # Default denominator so it is not 0 
        init_lat = self.toRadians(aLatitude)
        init_long = self.toRadians(aLongitude)
        distance = self.toRadians(aDistance / self.NM_PER_DEGREE)
        init_course = self.toRadians(theCourse)

        # get sin/cos of course 
        sin_crs = math.sin(init_course)
        cos_crs = math.cos(init_course)
        
        if (abs(init_lat) > self.LAT_TOLERANCE):
            # perform polar update using great circle equations */
            cos_dist = math.cos(distance)
            sin_dist = math.sin(distance)

            # get sin/cos of latitude */
            sin_lat = math.sin(init_lat)
            cos_lat = math.cos(init_lat)
            
            # compute new position along a great circle
            new_lat = math.asin(cos_dist * sin_lat + cos_crs * sin_dist * cos_lat)
            delta_lat = new_lat - init_lat
            denom = cos_dist * cos_lat - sin_dist * cos_crs * sin_lat
            
            if (denom == 0.0):
                denom = def_denom
                
            delta_long = math.atan(sin_dist * sin_crs / denom)
    
        else:
            # perform mid-latitude update
            delta_lat = distance * cos_crs
            new_lat = init_lat + delta_lat
            delta_long = distance * sin_crs / math.cos(init_lat + self.RAD_90 * delta_lat)

        # check latitude tolerance */
        new_long = init_long + delta_long;

        if (abs(new_long) >= self.RAD_180):
            new_long -= self.RAD_360 * self.signum(new_long)

        return GeographicPosition(self.toDegrees(new_lat), self.toDegrees(new_long))
    
    def horizon(self, eye_ht_ft):
        """
            Compute the distance (NM) to the horizon from an observer at a height given in feet.
        """
        return self.lineOfSightDistance(eye_ht_ft, 0.0)

    def isVisible(self, eye_ht_ft, obj_ht_ft, distance):
        """
            Returns TRUE if the object is 'visible' from the eye when separated by a distance (NM); obj and eye are in feet
        """
        arange = self.lineOfSightDistance(eye_ht_ft, obj_ht_ft)
        return (distance <= arange)

    def lineOfSightDistance(self, eye_ht_ft, obj_ht_ft):
        """
        Return line-of-sight distance(nm) from the eye to an object.  The heights of the eye and object are in feet.
        """
        return 1.144 * (math.sqrt(eye_ht_ft) + math.sqrt(obj_ht_ft))
    
    def CalculateBearing(self, theHeading, aStartPosition, anEndPosition, theBearingType):
        """
            Calculate the bearing from one geographic position to another one given the heading at the Start.
        """
        bearing = 0.0
        lat_error = 0.00005
        long_error = 0.000005
        ln_term = 0.0

        #  initialize bearings 
        abs_bearing = theHeading
        rel_bearing = theHeading
        source_lat = self.toRadians(aStartPosition.getLatitude())
        source_long = self.toRadians(aStartPosition.getLongitude())
        target_lat = self.toRadians(anEndPosition.getLatitude())
        target_long = self.toRadians(anEndPosition.getLongitude())
        source_heading = self.toRadians(theHeading)
        
        #  check if tracks are above 85 degrees latitude
        if (abs(source_lat) > self.RAD_85 or abs(target_lat) > self.RAD_85):
            NavError("Track above or below 85 degrees latitude.")
            
        else:
            #  calc change in latitude and longitude
            del_lat = target_lat - source_lat
            del_long = target_long - source_long
      
            #  normalize
            if (del_long > self.RAD_180):
                del_long = del_long - self.RAD_360
            elif (del_long < -self.RAD_180):
                del_long = del_long + self.RAD_360

            # check for headings of +/- pi_over_2
            if (abs(del_lat) < lat_error):
                if (del_long >= 0):
                    abs_bearing = self.RAD_90
                else:
                    abs_bearing = -self.RAD_90
            else:
                if (abs(del_long) < long_error):
                    if (target_lat >= source_lat):
                        abs_bearing = 0.0
                    else:
                        abs_bearing = self.RAD_180
                else:
                    #  calculate the angle in radians
                    t_term = math.tan(self.RAD_45 + target_lat / 2.0) / math.tan(self.RAD_45 + source_lat / 2.0)
                    ln_term = math.log(t_term)
                    abs_bearing = math.atan(del_long / ln_term)
                    
            #  convert to the proper quadrant */
            if (ln_term < 0.0):
                if (del_long > 0.0):
                    abs_bearing += self.RAD_180
                else:
                    abs_bearing -= self.RAD_180
                    
            bearing = self.toDegrees(abs_bearing)
            
            if (theBearingType == BearingType.RELATIVE):
                #  calculate relative bearing
                rel_bearing = abs_bearing - source_heading

                #  normalize
                if (rel_bearing > self.RAD_180):
                    rel_bearing -= self.RAD_360
                elif (rel_bearing < -self.RAD_180):
                    rel_bearing += self.RAD_360 
                bearing = self.toDegrees(rel_bearing);
                
        return bearing;
    
    def CalculateAbsBearing(self, aStartPosition, anEndPosition):
        """ Calculate Absolute bearing irregardless of heading. """
        return self.CalculateBearing(0.0, aStartPosition, anEndPosition, BearingType.ABSOLUTE)
            
    def CalculatePositionXY(self, aStartPosition, theChangeInX, theChangeInY):
        """
        This entry point calculates the new position of a track using the 
        starting position and changes in X and Y (nautical miles).
        """
        latitude = self.toRadians(aStartPosition.getLatitude())
        out_lat = aStartPosition.getLatitude() + theChangeInY / 60.0

        if (abs(abs(latitude) - self.PI ) > 0.00001):
            out_long = aStartPosition.getLongitude() + theChangeInX / (60.0 * math.cos(latitude))
        else:
            out_long = 0.0; # North or South Pole, any longitude will do
            
        return GeographicPosition(out_lat, out_long)
    
    
    def CalculateXY(self, theStartP, theEndP):
        """
            Compute the x and y distances (in Nautical Miles) of position lat1, lon1  
            from an initial location of lat0, lon0.
        """
        bearing = self.CalculateBearing(0.0, theStartP, theEndP, BearingType.RELATIVE)
        arange = self.GreatCircleRange(theStartP, theEndP) * self.NM_PER_DEGREE
        bearing = self.toRadians(bearing);

        xy = [arange * math.sin(bearing), arange * math.cos(bearing)]

        return xy;
    
    def CalculatePositionCS(self, aStartPosition, theSpeed, theHeading, theTimeInterval):
        """
            Computes a new geographic position based on a heading, a speed, and a time interval 
            from a starting location.
        """
        l_lat = aStartPosition.getLatitude()
        l_long = aStartPosition.getLongitude()

        if (theSpeed > 0.0):
            l_distance = theSpeed * theTimeInterval
            newPosition = self.GreatCircle(l_lat, l_long, theHeading, l_distance)
        else:
            newPosition = aStartPosition
            
        return newPosition
    

    def CalculateCPA(self, theApproachPosition, theApproachCourse, theApproachSpeed, \
                           theTargetPosition, theTargetCourse, theTargetSpeed):
        """
            Compute the closest point of approach between two objects.  Each
            has a give course (degrees) and speed (knots) and an initial
            location (lat & long in degrees).
        """

        epsilon = 0.000001 
        code = CPA_State.VALID;

        approach_course = self.PI_OVER_2 - self.toRadians(theApproachCourse)
        approach_speed = theApproachSpeed
        target_course = self.PI_OVER_2 - self.toRadians(theTargetCourse)
        target_speed = theTargetSpeed
        
        # Get the relative bearing (target_rb) from the approach to the target
        approach_sin = math.sin(approach_course)
        approach_cos = math.cos(approach_course)

        approach_speed_x = approach_speed * approach_cos
        approach_speed_y = approach_speed * approach_sin

        target_sin = math.sin(target_course)
        target_cos = math.cos(target_course)

        range_to_target = self. GreatCircleRange(theApproachPosition, theTargetPosition) * self.NM_PER_DEGREE
        approach_speed_x_rel = approach_speed_x * target_cos + approach_speed_y * target_sin - target_speed
        approach_speed_y_rel =  approach_speed_y * target_cos - approach_speed_x * target_sin
        
        # Get the relative velocity squared
        rel_velocity = approach_speed_x_rel * approach_speed_x_rel + approach_speed_y_rel * approach_speed_y_rel
        rel_velocity = math.sqrt(rel_velocity)
        
        approach_course_rel = 0.0
        
        if (rel_velocity < epsilon):
            code = CPA_State.NO_RELATIVE_MOTION
        else:
            # Get approach heading in target's frame of reference  */
            if (abs(approach_speed_x_rel) <= epsilon):
                if (abs(approach_speed_y_rel) <= epsilon):
                    approach_course_rel = 0.0
                else:
                    approach_course_rel = self.PI
            else:
                approach_course_rel = math.atan(approach_speed_y_rel / approach_speed_x_rel)

            # Adjust for quadrant */
            if (approach_speed_x_rel < 0.0 or abs(approach_speed_x_rel) <= epsilon):
                if (approach_speed_y_rel > 0.0 or abs(approach_speed_y_rel) <= epsilon):
                    approach_course_rel = self.PI + approach_course_rel
                else:
                    approach_course_rel = approach_course_rel - self.PI
        
        approach_rb =  self.CalculateBearing(theTargetCourse - self.toDegrees(approach_course_rel), \
                                             theApproachPosition, theTargetPosition, \
                                             BearingType.RELATIVE)
        approach_rb = self.toRadians(approach_rb)

        if (abs(approach_rb) >= self.PI_OVER_2):
            code = CPA_State.RECEDING
            
        # Load Output record
        output = CPAData()
        if (code == CPA_State.VALID):
            rb_sin = abs(math.sin(approach_rb));
            rb_cos = abs(math.cos(approach_rb))
            dist = range_to_target * rb_cos;
            output.setRangeAtCPA(range_to_target * rb_sin)
            output.setCode(code);

            output.setElapsedTime(dist / rel_velocity); # Hours

            # Now recompute distance from 'approach' starting point
            output.setDistToCPA(output.getElapsedTime() * approach_speed);
            time_interval = output.getElapsedTime() # Need in hours

            output.setElapsedTime(3600.0 * output.getElapsedTime()); # Seconds

            approach = self.CalculatePositionCS(theApproachPosition, theApproachSpeed, theApproachCourse, time_interval)
            output.setCpaPosition(approach)
        else:
            dist = range_to_target
            output.setRangeAtCPA(dist)
            output.setDistToCPA(dist)
            output.setElapsedTime(0.0)
            output.setCode(code)
            output.setCpaPosition(theApproachPosition)

        return output
    
    def CalculatePerpendicularDistance(self, theTargetPosition, theCircleStartP, theCircleStopP):
        """
            Compute the perpendicular distance from a point to a great circle.
            The method does this by computing the CPA from the target to a
            dummy object moving along the path.  Only the final rangeAtCPA
            is valid.
        """
        # From the starting point, we need the absolute bearing to the stop point
        # Any speed is OK, so choose 60 knots to make checking easy.
        course = self.CalculateBearing(0.0, theCircleStartP, theCircleStopP, BearingType.ABSOLUTE)
        cpa = self.CalculateCPA(theCircleStartP, course, 60.0, theTargetPosition, 0.0, 0.0)
        return cpa.getRangeAtCPA()
    
    def findMinimumDistanceIndices(self, startList, endList):
        """
            Find the indices of the points with minimum distance between two routes.
            Input is 2 lists of Point representing the 2 routes.
            Rather brute force, could possibly be optimised.
        """
        indices = [-1, -1]
        minDistance = sys.float_info.max
        for i in range(0, len(startList)):
            cosLatS = math.cos(self.toRadians(startList[i].getLatitude()))
            for j in range(0, len(endList)):
                cosLatE = math.cos(self.toRadians(endList[j].getLatitude()))
                deltaL  = math.cos(self.toRadians(startList[i].getLatitude() - endList[j].getLatitude()))
                deltal  = math.cos(self.toRadians(startList[i].getLongitude() - endList[j].getLongitude()))
                distance = math.acos(deltaL - (1.0 - deltal)*cosLatS*cosLatE)
                if(distance < minDistance):
                    indices[0] = i
                    indices[1] = j
                    minDistance = distance
        return indices
    
    def findMinimumDistanceLocation(self, startList, endList):
        """
        Find the two Points having the minimum distance between two routes.
        Input is 2 lists of Point representing the 2 routes.
        """
        ixes = self.findMinimumDistanceIndices(startList, endList)
        positions = []
        positions[0] = startList[ixes[0]]
        positions[1] = endList[ixes[1]]
        return positions
    
    def NewPositionFraction(self, start, end, fraction):
        """
            Find the point at a given fraction of the path between two points.
            For example, if point 1 is at (0N, 1W) and point 2 is at (0N, 1E) a fraction of 0.5
            will result in a position (0N, 0W)
        """
        distance = self.toRadians(self.GreatCircleRange(start, end))
        a = math.sin(distance*(1.0 - fraction))/math.sin(distance)
        b = math.sin(distance * fraction)/math.sin(distance)
        x = a*math.cos(self.toRadians(start.getLatitude())) * math.cos(self.toRadians(start.getLongitude())) \
                      + b * math.cos(self.toRadians(end.getLatitude())) * math.cos(self.toRadians(end.getLongitude()))
        y = a*math.cos(self.toRadians(start.getLatitude())) * math.sin(self.toRadians(start.getLongitude())) \
                      + b * math.cos(self.toRadians(end.getLatitude())) * math.sin(self.toRadians(end.getLongitude()));
        z = a*math.sin(self.toRadians(start.getLatitude())) + b * math.sin(self.toRadians(end.getLatitude()))
        latF = self.toDegrees(math.atan2(z, math.sqrt(x*x + y*y)))
        lonF = self.toDegrees(math.atan2(y,x))
        return GeographicPosition(latF, lonF)
    
    
