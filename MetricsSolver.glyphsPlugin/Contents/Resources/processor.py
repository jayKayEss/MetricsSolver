from __future__ import division, print_function, unicode_literals
import re
from GlyphsApp.plugins import *
from matcher import MetricsSolverMatcher

class MetricsSolverProcessor(object):
    def __init__(self):
        self.font = Glyphs.font
        self.masters = self.font.masters
        self.glyphs = self.font.glyphs
        self.has_problems = False

    def get_glyph(self, name):
        glyph = self.font.glyphs[name]
        return glyph

    def get_layer(self, glyph, master):
        return glyph.layers[master.id]

    def warn_on_circular_dependency(self, chain):
        chain.reverse()
        print("WARNING: Circular dependency found: %s" % ' -> '.join(chain))
        self.has_problems = True

    def warn_on_bad_key(self, glyph_name, dep):
        print("WARNING: Bad metrics key %s found in glyph %s" % (dep, glyph_name))
        self.has_problems = True

    def get_left_dependency(self, glyph, layer):
        dep = layer.leftMetricsKey or glyph.leftMetricsKey
        if dep:
            return MetricsSolverMatcher.match(dep)
        return None

    def get_right_dependency(self, glyph, layer):
        dep = layer.rightMetricsKey or glyph.rightMetricsKey
        if dep:
            return MetricsSolverMatcher.match(dep)
        return None

    def get_dependency_chain(self, glyph, master, dependency_func):
        chain = [glyph.name]
        current = glyph

        while True:
            layer = self.get_layer(current, master)
            dep = dependency_func(current, layer)
            if dep:
                if dep in chain:
                    self.warn_on_circular_dependency([dep] + chain)
                    break
                glyph = self.get_glyph(dep)
                if glyph is None:
                    self.warn_on_bad_key(current.name, dep)
                    break
                else:
                    current = glyph
                    chain = [dep] + chain
            else:
                break
        return chain

    def update_chain(self, chain, master, cache):
        for glyph_name in chain:
            if glyph_name in cache:
                continue
            glyph = self.get_glyph(glyph_name)
            layer = self.get_layer(glyph, master)
            layer.syncMetrics()
            cache.add(glyph_name)
        return cache

    def run(self):
        try:
            Glyphs.clearLog()
            self.font.disableUpdateInterface()
            for master in self.masters:
                for func in [self.get_left_dependency, self.get_right_dependency]:
                    cache = set()
                    for glyph in self.glyphs:
                        lchain = self.get_dependency_chain(glyph, master, func)
                        cache = self.update_chain(lchain, master, cache)
            self.font.enableUpdateInterface()
            Glyphs.redraw()

            if self.has_problems:
                Glyphs.showNotification("Resolve Metrics", "Some problems were found with metrics keys. Check the log for details.")
                Glyphs.showMacroWindow()
            else:
                Glyphs.showNotification("Resolve Metrics", "All metrics resolved successfully")
        except:
            import traceback
            print(traceback.format_exc())
            Glyphs.showNotification("Resolve Metrics", "An error occurred! Check the log for details.")
            Glyphs.showMacroWindow()
