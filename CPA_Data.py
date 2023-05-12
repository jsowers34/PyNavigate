'''
 ***************************************************************************** 
 * PURPOSE
 *     Provide a class to hold data for Closest Point of Approach (CPA)
 ***************************************************************************** 
 * MODIFICATIONS
 * @author JL Sowers May 1, 2023
 ***************************************************************************** 
 *  DESIGN NOTES:
 *  
 ***************************************************************************** 
'''
from enum import Enum
from com.rff.pynavigate.GeographicPosition import GeographicPosition

class CPA_State(Enum):
    VALID = 1               # Vessels are approaching each other
    RECEDING = 2            #             moving away from each other
    NO_RELATIVE_MOTION = 3  #             moving parallel to each other or are at rest.


class CPAData():

    def __init__(self):
        self.cpaPosition = GeographicPosition()
        self.distToCPA = 0.0
        self.elapsedTime = 0.0
        self.rangeAtCPA = 0.0
        self.code = CPA_State.VALID
        
    def __equals__(self, other):
        result = self.cpaPosition == other.cpaPosition
        result = result and self.distToCPA == other.distToCPA
        result = result and self.rangeAtCPA == other.rangeAtCPA and self.code == other.code
        return result
        
    def setCpaPosition(self, *args):
        if (len(args) == 1):
            self.cpaPosition = args[0]
        else:
            self.cpaPosition.setLatitude(args[0])
            self.cpaPosition.setLongitude(args[1])
    
    def getCpaPosition(self):
        return self.cpaPosition

    def setDistToCPA(self, theDistToCPA):
        self.distToCPA = theDistToCPA

    def getDistToCPA(self):
        return self.distToCPA

    def setElapsedTime(self, theElapsedTime):
        self.elapsedTime = theElapsedTime

    def getElapsedTime(self):
        return self.elapsedTime 

    def setRangeAtCPA(self, theRangeAtCPA):
        self.rangeAtCPA = theRangeAtCPA

    def getRangeAtCPA(self):
        return self.rangeAtCPA

    def setCode(self, theCode):
        self.code = theCode

    def getCode(self):
        return self.code
    
    def getStatus(self):
        return self.code.name
    
    def toString(self):
        astr = self.cpaPosition.toString() + "\n"
        astr += "Distance to CPA = " + str(self.distToCPA) + "\n"
        astr += "Range to CPA = " + str(self.rangeAtCPA) + "\n"
        astr += "Elapsed Time = " + str(self.elapsedTime) + "\n"
        astr += "CPA Status = " + self.code.name + "\n"
        return astr

