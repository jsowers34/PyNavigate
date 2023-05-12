'''
 ***************************************************************************** 
 * PURPOSE
 *          Error Display Dialog
 ***************************************************************************** 
 * MODIFICATIONS
 * @author JL Sowers 08 MAY 2023
 ***************************************************************************** 
 *  DESIGN NOTES:
 *      Uses GTK Message Dialog
 ***************************************************************************** 
'''
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk

class NavError(object):
    
    def __init__(self, message, more = None):
        self.gladefile = "NavError.glade"
        builder = gtk.Builder()
        builder.add_from_file(self.gladefile)
        self.topLevel = builder.get_object('toplevel')
        self.topLevel.set_property("text",message)
        if(more is not None):
            self.topLevel.set_property("secondary_text",more)
    
        # Let'r rip!
        self.topLevel.show_all()
        
        response = self.topLevel.run()
        if response == gtk.ResponseType.CLOSE:
            self.topLevel.destroy()
