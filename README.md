#PyNavigate

PyNavigate is a python3 package with multiple methods for use in navigational problems.

Included in the package is a Navigation Utility GUI which demonstrates the 
calculation of (1) the bearing and distance between 2 geographical positions, (2) the final position based on an initial position, the course, speed and the running time, and (3) the final position based on the initial position the course and the distance traveled.

##Methods provided:
### Great Circle
> GreatCircle(startLatitude, startLongitude, course, distance)
	    
	    This procedure will calculate the new position of a given track as a result of the distance traveled.
        
        The great circle route is approximated by a series of rhumb lines as a function of latitude.  
        The rhumb line equations cannot be used at high latitudes, in which case, the actual great circle 
        computations must be made.  The use of either the rhumb line or great circle equations is determined 
        by a latitude tolerance.
        The rhumb line equations were taken from Dutton's Navigation and Piloting (Maloney).
        The great circle equations were derived from the American Practical Navigator (Bowditch).
        
### Great Circle Range
> GreatCircleRange(startPosition, endPosition)

	This method computes the distance (in Degrees) between two geographical positions along a great circle.
	The resulting distance may be converted to Nautical Miles by multiplying by 60.0
	
### Rhumb Line
> rhumb_line(startLatitude, startLongitude, course, distance)

	For mid-latitudes, the simple rhumb line equations are used to update the rhumb line route.  
	For high latitudes , the great circle equations are used without updating the course.  
	The use of either the rhumb line or great circle equations is determined by a latitude tolerance.

### Horizon
> horizon(eye_ht_ft)
	Computes the distance (NM) to the horizon from an observer at a height given in feet.
	
### Line of Sight Distance
> lineOfSightDistance(eye_ht_ft, obj_ht_ft)

	 Return line-of-sight distance(nm) from the eye to an object.  The heights of the eye and object are in feet.
	 
### Visibility
> isVisible(eye_ht_ft, obj_ht_ft, distance)

	Returns TRUE if the object is 'visible' from the eye when separated by a distance (NM); obj and eye heights are in feet
	
	 
### Calculate Bearing
> CalculateBearing(heading, startPosition, endPosition, BearingType)

	 Calculate the bearing from one geographic position to another one given the heading at the Start. The method also allows the use of Absolute or Relative Bearing (Bearing Type).  Absolute determines the bearing irregardless of the heading of the vessel at the initial position; Relative will determine the bearing from the heading of the vessel.
	 
### Calculate Absolute Bearing
> CalculateAbsBearing(startPosition, endPosition)

	A convenience method, which allows just a starting and ending positions as input
	
### Calculate Position XY
>	CalculatePositionXY(startPosition, theChangeInX, theChangeInY)

	Calculates the new position of a track using the starting position and changes in X and Y (nautical miles).
	
### Calculate XY
> CalculateXY(startPos, endPos):

	Compute the x and y distances (in Nautical Miles) of a geographic position 
            from an initial geographic position.
            
### Calculate Position using Course, Speed and running time
> CalculatePositionCS(startPosition, speed, course, timeInterval)

	Computes a new geographic position based on a heading, a speed, and a time interval (in hours) 
	from a starting location.
	
### Calculate Closest-Point-Of-Approach
> CalculateCPA(startPosition, startCourse, startSpeed, targetPosition, targetCourse, targetSpeed)

	Compute the closest point of approach between two objects.  
	Each has a given course (degrees) and speed (knots) and an initial geographic
    position.
    
### Calculate Perpendicular Distance
> CalculatePerpendicularDistance(targetPosition, theCircleStartPos, theCircleStopPos)

	Compute the perpendicular distance from a point to a great circle.
	The method does this by computing the CPA from the target to a dummy object 
	moving along the path.  
	Only the final range at CPA is valid.
	
### Find indices of Points (lat/lon) for the minimum distances between two routes.
> findMinimumDistanceIndices(startList, endList)

	Find the indices of the points with minimum distance between two routes.
	Input is 2 lists of Point representing the 2 routes.
	Rather brute force, could possibly be optimised.
	
### Find Points (lat/lon) for the minimum distances between two routes.
> findMinimumDistanceLocation(startList, endList)

	Find the Points with the minimum distance between two routes.
	Input is 2 lists of Point representing the 2 routes.
	Rather brute force, could possibly be optimised.
	
### Find new Latitude given a starting position, the heading and the distance to be traveled.
> NewPositionLatitude(start, bearing, distance)

	Given an initial Geographic Position, a bearing/course and a distance (in nm), compute the 
	latitude of the new position.

### Find new Longitude given a starting position, the heading and the distance to be traveled.
> NewPositionLongitude(start, bearing, distance)

	Given an initial Geographic Position, a bearing/course and a distance (in nm), compute the 
	longitude of the new position.

### Find position at a specificed fraction of the distance between two input positions.
> NewPositionFraction(startPos, endPos, fraction)

	Find the point at a given fraction of the path between two points.
	For example, if point 1 is at (0N, 1W) and point 2 is at (0N, 1E) a fraction of 0.5 will 
	result in a position (0N, 0W)