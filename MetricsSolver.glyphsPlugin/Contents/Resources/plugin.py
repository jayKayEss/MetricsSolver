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


from __future__ import division, print_function, unicode_literals
import objc
from GlyphsApp.plugins import *
from GlyphsApp import EDIT_MENU
from AppKit import NSMenuItem
from processor import MetricsSolverProcessor

class MetricsSolver(GeneralPlugin):
    """Iteratively solves metrics keys and dependencies"""

    @objc.python_method
    def settings(self):
        """Defines plugin settings"""
        self.name = Glyphs.localize({'en': 'Resolve All Metrics'})

    @objc.python_method
    def start(self):
        """Starts the plugin"""
        try:
            # new API in Glyphs 2.3.1-910
            newMenuItem = NSMenuItem(self.name, self.invokePlugin_)
            Glyphs.menu[EDIT_MENU].append(newMenuItem)
        except:
            mainMenu = Glyphs.mainMenu()
            s = objc.selector(self.invokePlugin_, signature='v@:@')
            newMenuItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(self.name, s, '\\')
            newMenuItem.setTarget_(self)
            mainMenu.itemWithTag_(5).submenu().addItem_(newMenuItem)

    def invokePlugin_(self, sender):
        """Resolve all metrics"""
        processor = MetricsSolverProcessor()
        processor.run()

    @objc.python_method
    def __file__(self):
        """Please leave this method unchanged"""
        return __file__
