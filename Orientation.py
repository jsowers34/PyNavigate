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
 *  
 * @version 
 ***************************************************************************** 
'''
from enum import Enum

class Orientation(Enum):
        CCW = 1
        CW  = 2
        COLL = 3
        
if __name__ == '__main__':
    print(Orientation.CCW.value, Orientation.CCW.name)
    
        
        