Are you plagued by little yellow triangles in your [Glyphs.app](https://glyphsapp.com) project?

![screenshot](https://github.com/jayKayEss/MetricsSolver/raw/master/Extras/screenshot.png)

Glyphs gives us a powerful language for specifying sidebearings by referencing the values of dependent glyphs. This is useful, but can lead to some problems. For instance, you might set the left sidebearing of `Dcaron` to be equal to `D`, which in turn is equal to `H`. But, if you edit `H`, the derived sidebearings will no longer be correct. This requires tedious manual upating to fix.

MetricsSolver is a plugin for Glyphs.app that attempts to resolve all metrics for all glyphs in your font, across all masters. It does this by building a simple dependency graph for each glyph, and resolving the metrics on the referenced glyphs first. It'll also warn you about metrics keys that can't be resolved (either because you mistyped the name of a glyph, or set up a circular dependency, e.g. A depends on B which depends on A.)

To use it, just select "Resolve All Metrics" from the "Edit" menu.

Caveats:
* The font view tab won't automatically update; to get rid of the little yellow triangles just scroll the view.
* Some metrics may have rounding errors(?) and won't resolve completely no matter what. I'm not sure what the cause or fix is for this.
* This plugin has only been tested against my own work; feedback and (especially) pull requests are welcome!
