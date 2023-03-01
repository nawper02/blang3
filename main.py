from blang import Blang


def main():
    blang = Blang()
    blang.run()


if __name__ == "__main__":
    main()


# TODO: Catch up to old version in misc features -- units
# TODO: function writer overhaul -- list view (delete, double click to edit, FOLDERS), control flow (hard),
# TODO: Add stats functionality -- distributions, etc
# TODO: Add units functionality using new strings functionality
# TODO: Make macro label a function browser where you can expand/open and edit functions
# TODO: Make var label display matrices correctly
# TODO: Fix growing spaces in list (.sq repeat on list make spaces grow)
# TODO: Make data load/save from a json
# TODO: Update reserved keywords
# TODO: Make matrw rows and cols scale to fit in window until a certain point at which scroll is enabled?
# TODO: make the docs
# TODO: Make log give basic useful information other than errors
# TODO: make quadrature work, implement secant root finding


# OLD TODOS:
"""
# ADD #
# TODO: add more functions in general
# TODO: remove stupid stuff from units?
# TODO: Make units tab with categories?
# TODO: conversions -- dtr(deg to rad), rtd(rad to deg), ctpd(cartesian to polar), ctsd(cartesian to spherical),
# TODO:                ctcd(cartesian to cylindrical) and other way for all as well as xxxr for radians.

# REFACTOR #
# TODO: make print_stack print abbreviated units ( inside print object method units elif)
# TODO: make transpose work on [1,2,3] pushes
# TODO: add displaytypes for all stack objects

# TEST #
# TODO: test trig functions, test units thuroughly
"""
