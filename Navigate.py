'''
 ***************************************************************************** 
 * PURPOSE
 *     A Navigation Utility GUI
 *     Demonstrates the use of the PyNavigate package
 ***************************************************************************** 
 * MODIFICATIONS
 * @author JL Sowers May 2, 2023    Initial Code
 *
 *         JL Sowers May 26, 2023   Added background color to indicate Result fields
 ***************************************************************************** 
 *  DESIGN NOTES:
 *     Overiding the color without CSS caused a deprecate warning which
 *     we tell the system to ignore.
 ***************************************************************************** 
'''
from GeographicPosition import GeographicPosition
from NavUtils import NavUtils
from NavCommon import NavCommon
from NavError import NavError
import warnings

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk
from gi.repository import Gdk as gdk

class Navigate(object):
    def __init__(self):
        # Overriding the color without CSS gives a deprecated warning
        warnings.filterwarnings("ignore", category=DeprecationWarning) 
        
        self.NC = NavCommon()
        self.navu = NavUtils()
        self.gladefile = "Navigate.glade"  
        builder = gtk.Builder()
        builder.add_from_file(self.gladefile)
        self.topLevel = builder.get_object('toplevel')
        
        # Use a light blue to indicate results areas  
        self.color = gdk.RGBA()
        self.color.parse("#b0e2ff")  # light sky blue 1
        self.color.to_string()

        # a flag to see if we are in DecDec or DMS mode
        self.dms_f = True
        self.currentPage = 'Bearing'
        
        self.switcher = builder.get_object('switchSTK')
        self.switcher.connect("event", self.selectPage)
        
        self.decdeg = builder.get_object('decRB')
        self.dms = builder.get_object('dmsRB')
        self.decdeg.connect('toggled', self.checkRButtons, "decdeg")
        self.dms.connect('toggled', self.checkRButtons, "dms")
                 
        self.setupBearingPage(builder)
        self.setupCourseSpeedPage(builder)
        self.setupCourseDistancePage(builder)
        self.setupCPAPage(builder)
        
        # Set up the Buttons
        self.executeBtn = builder.get_object("executeBtn")
        self.executeBtn.connect('clicked', lambda w: self.process())
        self.clearBtn = builder.get_object("clearBtn")
        self.clearBtn.connect('clicked', lambda w: self.clear())
        self.quitBtn = builder.get_object("quitBtn")
        self.quitBtn.connect('clicked', lambda w: self.bye_bye())     
        self.topLevel.show_all()
        
    def setupBearingPage(self, builder):
        """Get TextViewBuffers for all of the Bearing Page. """
        # Initial Position Latitude, Longitude
        self.initLatDeg = builder.get_object('initLatDeg')
        self.initLatMin = builder.get_object('initLatMin')
        self.initLatSec = builder.get_object('initLatSec')
        self.initLatDegBUF = builder.get_object('initLatDegBUF')
        self.initLatMinBUF = builder.get_object('initLatMinBUF')
        self.initLatSecBUF = builder.get_object('initLatSecBUF')
        
        self.initLonDeg = builder.get_object('initLonDeg')
        self.initLonMin = builder.get_object('initLonMin')
        self.initLonSec = builder.get_object('initLonSec')
        self.initLonDegBUF = builder.get_object('initLonDegBUF')
        self.initLonMinBUF = builder.get_object('initLonMinBUF')
        self.initLonSecBUF = builder.get_object('initLonSecBUF')
        
        # Final Position Latitude, Longitude
        self.finalLatDeg = builder.get_object('finalLatDeg')
        self.finalLatMin = builder.get_object('finalLatMin')
        self.finalLatSec = builder.get_object('finalLatSec')
        self.finalLatDegBUF = builder.get_object('finalLatDegBUF')
        self.finalLatMinBUF = builder.get_object('finalLatMinBUF')
        self.finalLatSecBUF = builder.get_object('finalLatSecBUF')
        
        self.finalLonDeg = builder.get_object('finalLonDeg')
        self.finalLonMin = builder.get_object('finalLonMin')
        self.finalLonSec = builder.get_object('finalLonSec')
        self.finalLonDegBUF = builder.get_object('finalLonDegBUF')
        self.finalLonMinBUF = builder.get_object('finalLonMinBUF')
        self.finalLonSecBUF = builder.get_object('finalLonSecBUF')
        
        # Bearing
        self.bearingDeg = builder.get_object('bearingDeg')
        self.setBackground(self.bearingDeg)
        self.bearingMin = builder.get_object('bearingMin')
        self.setBackground(self.bearingMin)
        self.bearingSec = builder.get_object('bearingSec')
        self.setBackground(self.bearingSec)
        self.bearingDegBUF = builder.get_object('bearingDegBUF')
        self.bearingMinBUF = builder.get_object('bearingMinBUF')
        self.bearingSecBUF = builder.get_object('bearingSecBUF')
        
        # Distance
        self.gcrange = builder.get_object('gcRange')
        self.setBackground(self.gcrange)
        self.gcrangeBUF = builder.get_object('gcRangeBUF')
        
    def setupCourseSpeedPage(self, builder):
        """Get TextViewBuffers for all of the Course-Speed Page. """
        # Initial Position Latitude, Longitude
        self.initLatDeg1 = builder.get_object('initLatDeg1')
        self.initLatMin1 = builder.get_object('initLatMin1')
        self.initLatSec1 = builder.get_object('initLatSec1')
        self.initLatDegBUF = builder.get_object('initLatDegBUF')
        self.initLatMinBUF = builder.get_object('initLatMinBUF')
        self.initLatSecBUF = builder.get_object('initLatSecBUF')
        self.initLonDeg1 = builder.get_object('initLonDeg1')
        self.initLonMin1 = builder.get_object('initLonMin1')
        self.initLonSec1 = builder.get_object('initLonSec1')
        self.initLonDegBUF = builder.get_object('initLonDegBUF')
        self.initLonMinBUF = builder.get_object('initLonMinBUF')
        self.initLonSecBUF = builder.get_object('initLonSecBUF')
        
        # Final Position Latitude, Longitude
        self.finalLatDeg1 = builder.get_object('finalLatDeg1')
        self.setBackground(self.finalLatDeg1)
        self.finalLatMin1 = builder.get_object('finalLatMin1')
        self.setBackground(self.finalLatMin1)
        self.finalLatSec1 = builder.get_object('finalLatSec1')
        self.setBackground(self.finalLatSec1)
        self.finalLatDegBUF = builder.get_object('finalLatDegBUF')
        self.finalLatMinBUF = builder.get_object('finalLatMinBUF')
        self.finalLatSecBUF = builder.get_object('finalLatSecBUF')
        
        self.finalLonDeg1 = builder.get_object('finalLonDeg1')
        self.setBackground(self.finalLonDeg1)
        self.finalLonMin1 = builder.get_object('finalLonMin1')
        self.setBackground(self.finalLonMin1)
        self.finalLonSec1 = builder.get_object('finalLonSec1')
        self.setBackground(self.finalLonSec1)
        self.finalLonDegBUF = builder.get_object('finalLonDegBUF')
        self.finalLonMinBUF = builder.get_object('finalLonMinBUF')
        self.finalLonSecBUF = builder.get_object('finalLonSecBUF')
        
        self.crsDeg = builder.get_object('crsDeg')
        self.crsMin = builder.get_object('crsMin')
        self.crsSec = builder.get_object('crsSec')
        self.crsDegBUF = builder.get_object('crsDegBUF')
        self.crsMinBUF = builder.get_object('crsMinBUF')
        self.crsSecBUF = builder.get_object('crsSecBUF')
        
        self.durHour = builder.get_object('durHour')
        self.durMin = builder.get_object('durMin')
        self.durSec = builder.get_object('durSec')
        self.durHourBUF = builder.get_object('durHourBUF')
        self.durMinBUF = builder.get_object('durMinBUF')
        self.durSecBUF = builder.get_object('durSecBUF')
        
        self.speed = builder.get_object('speed')
        self.speedBUF = builder.get_object('speedBUF')
        
    def setupCourseDistancePage(self, builder):
        """Get TextViewBuffers for all of the Course-Distance Page. """
        # Initial Position Latitude, Longitude
        self.initLatDeg2 = builder.get_object('initLatDeg2')
        self.initLatMin2 = builder.get_object('initLatMin2')
        self.initLatSec2 = builder.get_object('initLatSec2')
        self.initLatDegBUF = builder.get_object('initLatDegBUF')
        self.initLatMinBUF = builder.get_object('initLatMinBUF')
        self.initLatSecBUF = builder.get_object('initLatSecBUF')
        self.initLonDeg2 = builder.get_object('initLonDeg2')
        self.initLonMin2 = builder.get_object('initLonMin2')
        self.initLonSec2 = builder.get_object('initLonSec2')
        self.initLonDegBUF = builder.get_object('initLonDegBUF')
        self.initLonMinBUF = builder.get_object('initLonMinBUF')
        self.initLonSecBUF = builder.get_object('initLonSecBUF')
        
        # Final Position Latitude, Longitude
        self.finalLatDeg2 = builder.get_object('finalLatDeg2')
        self.setBackground(self.finalLatDeg2)
        self.finalLatMin2 = builder.get_object('finalLatMin2')
        self.setBackground(self.finalLatMin2)
        self.finalLatSec2 = builder.get_object('finalLatSec2')
        self.setBackground(self.finalLatSec2)
        self.finalLatDegBUF = builder.get_object('finalLatDegBUF')
        self.finalLatMinBUF = builder.get_object('finalLatMinBUF')
        self.finalLatSecBUF = builder.get_object('finalLatSecBUF')
        
        self.finalLonDeg2 = builder.get_object('finalLonDeg2')
        self.setBackground(self.finalLonDeg2)
        self.finalLonMin2 = builder.get_object('finalLonMin2')
        self.setBackground(self.finalLonMin2)
        self.finalLonSec2 = builder.get_object('finalLonSec2')
        self.setBackground(self.finalLonSec2)
        self.finalLonDegBUF = builder.get_object('finalLonDegBUF')
        self.finalLonMinBUF = builder.get_object('finalLonMinBUF')
        self.finalLonSecBUF = builder.get_object('finalLonSecBUF')
        
        self.crsDeg2 = builder.get_object('crsDeg2')
        self.crsMin2 = builder.get_object('crsMin2')
        self.crsSec2 = builder.get_object('crsSec2')
        self.crsDegBUF = builder.get_object('crsDegBUF')
        self.crsMinBUF = builder.get_object('crsMinBUF')
        self.crsSecBUF = builder.get_object('crsSecBUF')
        
        self.distance = builder.get_object('distance')
        self.distanceBUF = builder.get_object('distanceBUF')
        
    def setupCPAPage(self, builder):
        """Get TextViewBuffers for all of the Closest-Point-of-Approach Page. """
        # Vessel 1 Latitude, Longitude, Course
        self.cpaLatDeg1 = builder.get_object('cpaLatDeg1')
        self.cpaLatMin1 = builder.get_object('cpaLatMin1')
        self.cpaLatSec1 = builder.get_object('cpaLatSec1')
        self.cpaLatDeg1BUF = builder.get_object('initLatDegBUF')
        self.cpaLatMin1BUF = builder.get_object('initLatMinBUF')
        self.cpaLatSec1BUF = builder.get_object('initLatSecBUF')
        self.cpaLonDeg1 = builder.get_object('cpaLonDeg1')
        self.cpaLonMin1 = builder.get_object('cpaLonMin1')
        self.cpaLonSec1 = builder.get_object('cpaLonSec1')
        self.cpaLonDeg1BUF = builder.get_object('initLonDegBUF')
        self.cpaLonMin1BUF = builder.get_object('initLonMinBUF')
        self.cpaLonSec1BUF = builder.get_object('initLonSecBUF')
        self.cpaCrsDeg1 = builder.get_object('cpaCrsDeg1')
        self.cpaCrsMin1 = builder.get_object('cpaCrsMin1')
        self.cpaCrsSec1 = builder.get_object('cpaCrsSec1')
        self.cpaCrsDeg1BUF = builder.get_object('crsDegBUF')
        self.cpaCrsMin1BUF = builder.get_object('crsMinBUF')
        self.cpaCrsSec1BUF = builder.get_object('crsSecBUF')
        self.cpaSpeed1 = builder.get_object('cpaSpeed1')
        self.cpaSpeed1BUF = builder.get_object('speedBUF')
        
        # Vessel 2 Latitude, Longitude, Course
        self.cpaLatDeg2 = builder.get_object('cpaLatDeg2')
        self.cpaLatMin2 = builder.get_object('cpaLatMin2')
        self.cpaLatSec2 = builder.get_object('cpaLatSec2')
        self.cpaLatDeg2BUF = builder.get_object('cpaLatDeg2BUF')
        self.cpaLatMin2BUF = builder.get_object('cpaLatMin2BUF')
        self.cpaLatSec2BUF = builder.get_object('cpaLatSec2BUF')
        self.cpaLonDeg2 = builder.get_object('cpaLonDeg2')
        self.cpaLonMin2 = builder.get_object('cpaLonMin2')
        self.cpaLonSec2 = builder.get_object('cpaLonSec2')
        self.cpaLonDeg2BUF = builder.get_object('cpaLonDeg2BUF')
        self.cpaLonMin2BUF = builder.get_object('cpaLonMin2BUF')
        self.cpaLonSec2BUF = builder.get_object('cpaLonSec2BUF')
        self.cpaCrsDeg2BUF = builder.get_object('cpaCrsDeg2BUF')
        self.cpaCrsMin2BUF = builder.get_object('cpaCrsMin2BUF')
        self.cpaCrsSec2BUF = builder.get_object('cpaCrsSec2BUF')
        self.cpaSpeed2 = builder.get_object('cpaSpeed2')
        self.cpaSpeed2BUF = builder.get_object('speed2BUF')
        
        # CPA Data
        self.cpaFinalLatDeg = builder.get_object('cpaFinalLatDeg')
        self.setBackground(self.cpaFinalLatDeg)
        self.cpaFinalLatMin = builder.get_object('cpaFinalLatMin')
        self.setBackground(self.cpaFinalLatMin)
        self.cpaFinalLatSec = builder.get_object('cpaFinalLatSec')
        self.setBackground(self.cpaFinalLatSec)
        self.cpaFinalLatDegBUF = builder.get_object('finalLatDegBUF')
        self.cpaFinalLatMinBUF = builder.get_object('finalLatMinBUF')
        self.cpaFinalLatSecBUF = builder.get_object('finalLatSecBUF')
        self.cpaFinalLonDeg = builder.get_object('cpaFinalLonDeg')
        self.setBackground(self.cpaFinalLonDeg)
        self.cpaFinalLonMin = builder.get_object('cpaFinalLonMin')
        self.setBackground(self.cpaFinalLonMin)
        self.cpaFinalLonMin = builder.get_object('cpaFinalLonSec')
        self.setBackground(self.cpaFinalLonMin)
        self.cpaFinalLonDegBUF = builder.get_object('finalLonDegBUF')
        self.cpaFinalLonMinBUF = builder.get_object('finalLonMinBUF')
        self.cpaFinalLonSecBUF = builder.get_object('finalLonSecBUF')
        self.distCPA = builder.get_object('distCPA')
        self.setBackground(self.distCPA)
        self.distCPABUF = builder.get_object('distCPABUF')
        self.rangeCPA = builder.get_object('rangeCPA')
        self.setBackground(self.rangeCPA)
        self.rangeCPABUF = builder.get_object('rangeCPABUF')
        self.elapsedTime = builder.get_object('elapsedTime')
        self.setBackground(self.elapsedTime)
        self.elapsedTimeBUF = builder.get_object('elapsedTimeBUF')
        self.statusCPA = builder.get_object('statusCPA')
        self.setBackground(self.statusCPA)
        self.statusCPABUF = builder.get_object('statusCPABUF')
        
    def setBackground(self, field):
        field.override_background_color(gtk.StateFlags.NORMAL, self.color)

    def checkRButtons(self, button, bname):
        if button.get_active():
            if bname == 'decdeg':
                self.dms_f = False
                if(self.currentPage == 'Bearing'):
                    self.initLatMin.set_visible(False)
                    self.initLatSec.set_visible(False)
                    self.initLonMin.set_visible(False)
                    self.initLonSec.set_visible(False)
                    self.finalLatMin.set_visible(False)
                    self.finalLatSec.set_visible(False)
                    self.finalLonMin.set_visible(False)
                    self.finalLonSec.set_visible(False)
                    self.bearingMin.set_visible(False)
                    self.bearingSec.set_visible(False)
                elif self.currentPage == 'CourseSpeed':
                    self.initLatMin1.set_visible(False)
                    self.initLatSec1.set_visible(False)
                    self.initLonMin1.set_visible(False)
                    self.initLonSec1.set_visible(False)
                    self.finalLatMin1.set_visible(False)
                    self.finalLatSec1.set_visible(False)
                    self.finalLonMin1.set_visible(False)
                    self.finalLonSec1.set_visible(False)
                    self.crsMin.set_visible(False)
                    self.crsSec.set_visible(False)
                elif self.currentPage == 'CourseDistance':
                    self.initLatMin2.set_visible(False)
                    self.initLatSec2.set_visible(False)
                    self.initLonMin2.set_visible(False)
                    self.initLonSec2.set_visible(False)
                    self.finalLatMin2.set_visible(False)
                    self.finalLatSec2.set_visible(False)
                    self.finalLonMin2.set_visible(False)
                    self.finalLonSec2.set_visible(False)
                    self.crsMin2.set_visible(False)
                    self.crsSec2.set_visible(False)
                self.toDecimal() 
            elif bname == 'dms':
                self.dms_f = True
                if(self.currentPage == 'Bearing'):
                    self.initLatMin.set_visible(True)
                    self.initLatSec.set_visible(True)
                    self.initLonMin.set_visible(True)
                    self.initLonSec.set_visible(True)
                    self.finalLatMin.set_visible(True)
                    self.finalLatSec.set_visible(True)
                    self.finalLonMin.set_visible(True)
                    self.finalLonSec.set_visible(True)
                    self.bearingMin.set_visible(True)
                    self.bearingSec.set_visible(True)
                elif self.currentPage == 'CourseSpeed':
                    self.initLatMin1.set_visible(True)
                    self.initLatSec1.set_visible(True)
                    self.initLonMin1.set_visible(True)
                    self.initLonSec1.set_visible(True)
                    self.finalLatMin1.set_visible(True)
                    self.finalLatSec1.set_visible(True)
                    self.finalLonMin1.set_visible(True)
                    self.finalLonSec1.set_visible(True)
                    self.crsMin.set_visible(True)
                    self.crsSec.set_visible(True)
                elif self.currentPage == 'CourseDistance':
                    self.initLatMin2.set_visible(True)
                    self.initLatSec2.set_visible(True)
                    self.initLonMin2.set_visible(True)
                    self.initLonSec2.set_visible(True)
                    self.finalLatMin2.set_visible(True)
                    self.finalLatSec2.set_visible(True)
                    self.finalLonMin2.set_visible(True)
                    self.finalLonSec2.set_visible(True)
                    self.crsMin2.set_visible(True)
                    self.crsSec2.set_visible(True)
                    
                self.toDMS() 
                          
    def selectPage(self, widget, data=None):
        name = self.switcher.get_stack().get_visible_child_name()
        self.currentPage = name
        
    def process(self):       
        if(self.currentPage == 'Bearing'):
            self.processBearing()
        elif (self.currentPage == 'CourseSpeed'):
            self.processCourseSpeed()
        elif (self.currentPage == 'CourseDistance'):
            self.processCourseDistance()
        elif (self.currentPage == 'CPA'):
            self.processCPA()
        
    def toDecimal(self):
        """
            Used when switching from Degree-Min-Sec to DecimalDegrees. Reads the fields and
            rewrites the buffers after conversion to Decimal.
        """
        # Initial Position
        latStr  = [self.processField(self.initLatDegBUF), self.processField(self.initLatMinBUF),self.processField(self.initLatSecBUF)]
        lonStr = [self.processField(self.initLonDegBUF), self.processField(self.initLonMinBUF),self.processField(self.initLonSecBUF)]
        i = 0
        for x in latStr:
            if x == '':
                x = '0.0'
                latStr[i] = x
            i = i + 1
        i = 0
        for x in lonStr:
            if x == '':
                x = '0.0'
                lonStr[i] = x
            i = i + 1
        latitude = [float(x) for x in latStr]
        longitude = [float(x) for x in lonStr]
        lat = self.NC.dms2dec(latitude)
        lon = self.NC.dms2dec(longitude)  
        self.setBuffer(self.initLatDegBUF, str(lat))
        self.setBuffer(self.initLatMinBUF, '')
        self.setBuffer(self.initLatSecBUF, '')
        self.setBuffer(self.initLonDegBUF, str(lon))
        self.setBuffer(self.initLonMinBUF, '')
        self.setBuffer(self.initLonSecBUF, '')
        # Final Position
        latStr  = [self.processField(self.finalLatDegBUF), self.processField(self.finalLatMinBUF),self.processField(self.finalLatSecBUF)]
        lonStr = [self.processField(self.finalLonDegBUF), self.processField(self.finalLonMinBUF),self.processField(self.finalLonSecBUF)]
        i = 0
        for x in latStr:
            if x == '':
                x = '0.0'
                latStr[i] = x
            i = i + 1
        i = 0
        for x in lonStr:
            if x == '':
                x = '0.0'
                lonStr[i] = x
            i = i + 1
        latitude = [float(x) for x in latStr]
        longitude = [float(x) for x in lonStr]
        lat = self.NC.dms2dec(latitude)
        lon = self.NC.dms2dec(longitude)  
        self.setBuffer(self.finalLatDegBUF, str(lat))
        self.setBuffer(self.finalLatMinBUF, '')
        self.setBuffer(self.finalLatSecBUF, '')
        self.setBuffer(self.finalLonDegBUF, str(lon))
        self.setBuffer(self.finalLonMinBUF, '')
        self.setBuffer(self.finalLonSecBUF, '')
        
        # Course
        crsStr  = [self.processField(self.crsDegBUF), self.processField(self.crsMinBUF),self.processField(self.crsSecBUF)]
        i = 0
        for x in crsStr:
            if x == '':
                x = '0.0'
                crsStr[i] = x
            i = i + 1
        course = [float(x) for x in crsStr]
        crs = self.NC.dms2dec(course)
        self.setBuffer(self.crsDegBUF, str(crs))

    def toDMS(self):
        """
            Used when switching from DecimalDegrees to Degree-Min-Sec. Reads the Deg fields and
            rewrites the buffers after conversion to DMS.
        """
        # Initial Position 
        degrS = self.initLatDegBUF.get_text()
        if degrS == '':
            degr = 0.0
        else:
            degr = float(degrS)
        latitude = self.NC.dec2dms(degr)
        latitudeS = [str(x) for x in latitude]
        self.setBuffer(self.initLatDegBUF, latitudeS[0])
        self.setBuffer(self.initLatMinBUF, latitudeS[1])
        self.setBuffer(self.initLatSecBUF, latitudeS[2])
        degrS = self.initLonDegBUF.get_text()
        if degrS == '':
            degr = 0.0
        else:
            degr = float(degrS)
        degr = float(degrS)
        longitude = self.NC.dec2dms(degr)
        longitudeS = [str(x) for x in longitude]
        self.setBuffer(self.initLonDegBUF, longitudeS[0])
        self.setBuffer(self.initLonMinBUF, longitudeS[1])
        self.setBuffer(self.initLonSecBUF, longitudeS[2])
        # Final Position
        degrS = self.finalLatDegBUF.get_text()
        if degrS == '':
            degr = 0.0
        else:
            degr = float(degrS)
        latitude = self.NC.dec2dms(degr)
        latitudeS = [str(x) for x in latitude]
        self.setBuffer(self.finalLatDegBUF, latitudeS[0])
        self.setBuffer(self.finalLatMinBUF, latitudeS[1])
        self.setBuffer(self.finalLatSecBUF, latitudeS[2])
        degrS = self.finalLonDegBUF.get_text()
        degr = float(degrS)
        longitude = self.NC.dec2dms(degr)
        longitudeS = [str(x) for x in longitude]
        self.setBuffer(self.finalLonDegBUF, longitudeS[0])
        self.setBuffer(self.finalLonMinBUF, longitudeS[1])
        self.setBuffer(self.finalLonSecBUF, longitudeS[2])
        # Course
        degrS = self.crsDegBUF.get_text()
        if degrS == '':
            degr = 0.0
        else:
            degr = float(degrS)
        course = self.NC.dec2dms(degr)
        courseS = [str(x) for x in course]
        self.setBuffer(self.crsDegBUF, courseS[0])
        self.setBuffer(self.crsMinBUF, courseS[1])
        self.setBuffer(self.crsSecBUF, courseS[2])      
        self.setBuffer(self.finalLatSecBUF, '')
        
    def processBearing(self):
        latitudeS  = [self.processField(self.initLatDegBUF), self.processField(self.initLatMinBUF),self.processField(self.initLatSecBUF)]
        longitudeS = [self.processField(self.initLonDegBUF), self.processField(self.initLonMinBUF),self.processField(self.initLonSecBUF)]
        latitude, longitude = self.checkInput(latitudeS, longitudeS)  
        if self.dms_f:
            decLat = self.NC.dms2dec(latitude)
            decLon = self.NC.dms2dec(longitude)
        else:
            decLat = latitude[0]
            decLon = longitude[0]
        initPos = GeographicPosition(decLat, decLon)
        
        latitudeS  = [self.processField(self.finalLatDegBUF), self.processField(self.finalLatMinBUF),self.processField(self.finalLatSecBUF)]
        longitudeS = [self.processField(self.finalLonDegBUF), self.processField(self.finalLonMinBUF),self.processField(self.finalLonSecBUF)]
        latitude, longitude = self.checkInput(latitudeS, longitudeS)  
        if self.dms_f:
            decLat = self.NC.dms2dec(latitude)
            decLon = self.NC.dms2dec(longitude)
        else:
            decLat = latitude[0]
            decLon = longitude[0]
        finalPos = GeographicPosition(decLat, decLon)
        
        # Compute and display the results
        bearingdec = NavUtils.CalculateAbsBearing(self.navu, initPos, finalPos)
        bearing = self.NC.dec2dms(bearingdec)
        bdeg = str(bearing[0])
        bmin = str(bearing[1])
        bsec = str(bearing[2])
        self.bearingDegBUF.set_text(bdeg, len(bdeg))
        self.bearingMinBUF.set_text(bmin, len(bmin))
        self.bearingSecBUF.set_text(bsec, len(bsec))
        distance = 60.0 * NavUtils.GreatCircleRange(self.navu, initPos, finalPos)
        distance = self.NC.truncate(distance + 0.5E-8, 7)
        distanceS = str(distance)
        self.gcrangeBUF.set_text(distanceS, len(distanceS))
        
    def processCourseSpeed(self):
        latitudeS  = [self.processField(self.initLatDegBUF), self.processField(self.initLatMinBUF),self.processField(self.initLatSecBUF)]
        longitudeS = [self.processField(self.initLonDegBUF), self.processField(self.initLonMinBUF),self.processField(self.initLonSecBUF)]
        latitude, longitude = self.checkInput(latitudeS, longitudeS)  
        if self.dms_f:
            decLat = self.NC.dms2dec(latitude)
            decLon = self.NC.dms2dec(longitude)
        else:
            decLat = latitude[0]
            decLon = longitude[0]
        initPos = GeographicPosition(decLat, decLon)
        
        courseS = [self.processField(self.crsDegBUF), self.processField(self.crsMinBUF),self.processField(self.crsSecBUF)]
        dummy, course = self.checkInput(['0','0','0'], courseS)
        durationS =[self.processField(self.durHourBUF), self.processField(self.durMinBUF),self.processField(self.durSecBUF)]
        runningHours = self.checkInputTime(durationS)
        if self.dms_f:
            decCourse = self.NC.dms2dec(course)
            decHours = self.NC.hms2hrs(runningHours)
        else:
            decCourse = course[0]
            decHours = runningHours[0]
            
        speedS = self.processField(self.speedBUF)
        if speedS == '':
            speed = 0.0
        else:
            speed = float(speedS)
        
        # Calculate and display the final position
        finalPos = NavUtils.CalculatePositionCS(self.navu, initPos, speed, decCourse, decHours)
        lat= finalPos.getLatitude()
        lon = finalPos.getLongitude()
        if self.dms_f:
            latitude = self.NC.dec2dms(lat)
            longitude = self.NC.dec2dms(lon)
            latitude = [str(x) for x in latitude]
            longitude = [str(x) for x in longitude]
        else:
            lat = str(lat)
            lon = str(lon)
            latitude  = [lat, '0.0', '0.0']
            longitude = [lon, '0.0', '0.0']
        self.setBuffer(self.finalLatDegBUF,latitude[0])
        self.setBuffer(self.finalLatMinBUF,latitude[1])
        self.setBuffer(self.finalLatSecBUF,latitude[2])
        self.setBuffer(self.finalLonDegBUF,longitude[0])
        self.setBuffer(self.finalLonMinBUF,longitude[1])
        self.setBuffer(self.finalLonSecBUF,longitude[2])
            
    def setBuffer(self, field, astr):
        field.set_text(astr, len(astr))    

    def processCourseDistance(self):
        latitudeS  = [self.processField(self.initLatDegBUF), self.processField(self.initLatMinBUF),self.processField(self.initLatSecBUF)]
        longitudeS = [self.processField(self.initLonDegBUF), self.processField(self.initLonMinBUF),self.processField(self.initLonSecBUF)]
        latitude, longitude = self.checkInput(latitudeS, longitudeS)  
        if self.dms_f:
            decLat = self.NC.dms2dec(latitude)
            decLon = self.NC.dms2dec(longitude)
        else:
            decLat = latitude[0]
            decLon = longitude[0]
        courseS = [self.processField(self.crsDegBUF), self.processField(self.crsMinBUF),self.processField(self.crsSecBUF)]
        dummy, course = self.checkInput(['0','0','0'], courseS)
        if self.dms_f:
            decCourse = self.NC.dms2dec(course)
        else:
            decCourse = course[0]
        distS = self.processField(self.distance)
        if distS == '':
            distS = '0.0'
        distance = float(distS)
        
        # Calculate and display the final position
        finalPos = NavUtils.GreatCircle(self.navu, decLat, decLon, decCourse, distance)
        lat= finalPos.getLatitude()
        lon = finalPos.getLongitude()
        if self.dms_f:
            latitude = self.NC.dec2dms(lat)
            longitude = self.NC.dec2dms(lon)
            latitude = [str(x) for x in latitude]
            longitude = [str(x) for x in longitude]
        else:
            lat = str(lat)
            lon = str(lon)
            latitude  = [lat, '0.0', '0.0']
            longitude = [lon, '0.0', '0.0']
        self.setBuffer(self.finalLatDegBUF,latitude[0])
        self.setBuffer(self.finalLatMinBUF,latitude[1])
        self.setBuffer(self.finalLatSecBUF,latitude[2])
        self.setBuffer(self.finalLonDegBUF,longitude[0])
        self.setBuffer(self.finalLonMinBUF,longitude[1])
        self.setBuffer(self.finalLonSecBUF,longitude[2])
        
    def processCPA(self):
        # Vessel 1
        latitudeS  = [self.processField(self.initLatDegBUF), self.processField(self.initLatMinBUF),self.processField(self.initLatSecBUF)]
        longitudeS = [self.processField(self.initLonDegBUF), self.processField(self.initLonMinBUF),self.processField(self.initLonSecBUF)]
        latitude, longitude = self.checkInput(latitudeS, longitudeS)  
        if self.dms_f:
            decLat = self.NC.dms2dec(latitude)
            decLon = self.NC.dms2dec(longitude)
        else:
            decLat = latitude[0]
            decLon = longitude[0]
        initPos1 = GeographicPosition(decLat, decLon)
        courseS = [self.processField(self.crsDegBUF), self.processField(self.crsMinBUF),self.processField(self.crsSecBUF)]
        dummy, course1 = self.checkInput(['0','0','0'], courseS)
        course1 = self.NC.dms2dec(course1)
        speedS = self.processField(self.speedBUF)
        if speedS == '':
            speed1 = 0.0
        else:
            speed1 = float(speedS)
        
        
        # Vessel 2
        latitudeS  = [self.processField(self.cpaLatDeg2BUF), self.processField(self.cpaLatMin2BUF),self.processField(self.cpaLatSec2BUF)]
        longitudeS = [self.processField(self.cpaLonDeg2BUF), self.processField(self.cpaLonMin2BUF),self.processField(self.cpaLonSec2BUF)]
        latitude, longitude = self.checkInput(latitudeS, longitudeS)  
        if self.dms_f:
            decLat = self.NC.dms2dec(latitude)
            decLon = self.NC.dms2dec(longitude)
        else:
            decLat = latitude[0]
            decLon = longitude[0]
        initPos2 = GeographicPosition(decLat, decLon)
        courseS = [self.processField(self.cpaCrsDeg2BUF), self.processField(self.cpaCrsMin2BUF),self.processField(self.cpaCrsSec2BUF)]
        dummy, course2 = self.checkInput(['0','0','0'], courseS)
        course2 = self.NC.dms2dec(course2)
        speedS = self.processField(self.cpaSpeed2BUF)
        if speedS == '':
            speed2 = 0.0
        else:
            speed2 = float(speedS)
        
        # Calculate and display the CPA Results   
        cpaData = NavUtils.CalculateCPA(self.navu,initPos1, course1, speed1, initPos2, course2, speed2)
        lat = cpaData.getCpaPosition().getLatitude()
        lon = cpaData.getCpaPosition().getLongitude()
        if self.dms_f:
            latitude = self.NC.dec2dms(lat)
            longitude = self.NC.dec2dms(lon)
            latitude = [str(x) for x in latitude]
            longitude = [str(x) for x in longitude]
        else:
            lat = str(lat)
            lon = str(lon)
            latitude  = [lat, '0.0', '0.0']
            longitude = [lon, '0.0', '0.0']
        
        dist   = self.round3(cpaData.getDistToCPA())
        rnge   = self.round3(cpaData.getRangeAtCPA())
        etime  = self.round3(cpaData.getElapsedTime())
        status = cpaData.getStatus()
        
        
        self.setBuffer(self.cpaFinalLatDegBUF,latitude[0])
        self.setBuffer(self.cpaFinalLatMinBUF,latitude[1])
        self.setBuffer(self.cpaFinalLatSecBUF,latitude[2])
        self.setBuffer(self.cpaFinalLonDegBUF,longitude[0])
        self.setBuffer(self.cpaFinalLonMinBUF,longitude[1])
        self.setBuffer(self.cpaFinalLonSecBUF,longitude[2])
        self.setBuffer(self.distCPABUF, str(dist))
        self.setBuffer(self.rangeCPABUF, str(rnge))
        self.setBuffer(self.elapsedTimeBUF, str(etime/3600.0)) # Make it hours
        self.setBuffer(self.statusCPABUF, str(status))
        
    def round3(self, value):
        return round(value, 3)

    def checkInput(self, latStr, lonStr):
        if(self.dms_f == False):
            if latStr[0] == '':
                latStr[0] = '0.0'
            if lonStr[0] == '':
                lonStr[0] = '0.0'
            latStr[1:] = ['0.0', '0.0']
            lonStr[1:] = ['0.0', '0.0']
        else:
            i = 0
            for x in latStr:
                if x == '':
                    x = '0.0'
                    latStr[i] = x
                i = i + 1
            i = 0
            for x in lonStr:
                if x == '':
                    x = '0.0'
                    lonStr[i] = x
                i = i + 1
        latitude = [float(x) for x in latStr]
        longitude = [float(x) for x in lonStr]
        self.checkLatitudeRange(latitude)
        self.checkLongitudeRange(longitude)
        return [latitude, longitude]
    
    def checkInputTime(self, timeS):
        i = 0
        for x in timeS:
            if x == '':
                x = '0.0'
                timeS[i] = x
            i = i + 1
        hours = [float(x) for x in timeS]
        self.checkTimeRange(hours)
        return hours
    
    def checkLatitudeRange(self, lat):
        if(abs(lat[0]) > 90.0):
            NavError("Latitude out of range")
        if(lat[1] < 0.0 or lat[1] >= 60.0):
            NavError("Latitude Minutes out of range")
        if(lat[2] < 0.0 or lat[2] >= 60.0):
            NavError("Latitude Seconds out of range")
    
    def checkLongitudeRange(self, lon):
        if(abs(lon[0]) >= 360.0):
            NavError("Longitude out of range")
        if(lon[1] < 0.0 or lon[1] >= 60.0):
            NavError("Longitude Minutes out of range")
        if(lon[2] < 0.0 or lon[2] >= 60.0):
            NavError("Longitude Seconds out of range")
        
    def checkTimeRange(self, hours):
        if(hours[0] < 0.0):
            NavError("Time cannot be negative")
        if(hours[1] < 0.0 or hours[1] >= 60.0):
            NavError("Running Time Minutes out of range")
        if(hours[2] < 0.0 or hours[2] >= 60.0):
            NavError("Running Time Seconds out of range")

    def processField(self, field):
        value = field.get_text()
        return value
        
    def clear(self):
        self.initLatDegBUF.set_text("", 0)
        self.initLatMinBUF.set_text("", 0)
        self.initLatSecBUF.set_text("", 0)
        self.initLonDegBUF.set_text("", 0)
        self.initLonMinBUF.set_text("", 0)
        self.initLonSecBUF.set_text("", 0)
        self.finalLatDegBUF.set_text("", 0)
        self.finalLatMinBUF.set_text("", 0)
        self.finalLatSecBUF.set_text("", 0)
        self.finalLonDegBUF.set_text("", 0)
        self.finalLonMinBUF.set_text("", 0)
        self.finalLonSecBUF.set_text("", 0)
        self.bearingDegBUF.set_text("", 0)
        self.bearingMinBUF.set_text("", 0)
        self.bearingSecBUF.set_text("", 0)
        self.crsDegBUF.set_text("", 0)
        self.crsMinBUF.set_text("", 0)
        self.crsSecBUF.set_text("", 0)
        self.cpaCrsDeg2BUF.set_text("", 0)
        self.cpaCrsMin2BUF.set_text("", 0)
        self.cpaCrsSec2BUF.set_text("", 0)
        self.speedBUF.set_text("", 0)
        self.durHourBUF.set_text("", 0)
        self.durMinBUF.set_text("", 0)
        self.durSecBUF.set_text("", 0)
        self.gcrangeBUF.set_text("", 0)
        self.distanceBUF.set_text("", 0)
        self.elapsedTimeBUF.set_text("", 0)
        self.statusCPABUF.set_text("", 0)
        self.rangeCPABUF.set_text("", 0)
        self.distCPABUF.set_text("", 0)
        self.cpaLatDeg2BUF.set_text("", 0)
        self.cpaLatMin2BUF.set_text("", 0)
        self.cpaLatSec2BUF.set_text("", 0)
        self.cpaLonDeg2BUF.set_text("", 0)
        self.cpaLonMin2BUF.set_text("", 0)
        self.cpaLonSec2BUF.set_text("", 0)
        self.cpaSpeed2BUF.set_text("", 0)
        
    def bye_bye(self):
        gtk.main_quit()        
    
if __name__ == '__main__':
    Navigate()
    gtk.main()   