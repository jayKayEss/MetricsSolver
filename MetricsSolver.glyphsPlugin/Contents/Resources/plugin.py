# encoding: utf-8

###########################################################################################################
#
#
#    General Plugin
#
#    Read the docs:
#    https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates/General%20Plugin
#
#
###########################################################################################################


from GlyphsApp.plugins import *
from processor import MetricsSolverProcessor

class MetricsSolver(GeneralPlugin):
    """Iteratively solves metrics keys and dependencies"""

    def settings(self):
        """Defines plugin settings"""
        self.name = Glyphs.localize({'en': u'Resolve All Metrics'})

    def start(self):
        """Starts the plugin"""
        try:
            # new API in Glyphs 2.3.1-910
            newMenuItem = NSMenuItem(self.name, self.showWindow)
            Glyphs.menu[EDIT_MENU].append(newMenuItem)
        except:
            mainMenu = Glyphs.mainMenu()
            s = objc.selector(self.invokePlugin, signature='v@:@')
            newMenuItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(self.name, s, "b")
            newMenuItem.setTarget_(self)
            mainMenu.itemWithTag_(5).submenu().addItem_(newMenuItem)

    def invokePlugin(self, sender):
        """Resolve all metrics"""
        processor = MetricsSolverProcessor()
        processor.run()

    def __file__(self):
        """Please leave this method unchanged"""
        return __file__
