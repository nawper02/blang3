from blang import Blang


def main():
    blang = Blang()
    blang.run()


if __name__ == "__main__":
    main()


# TODO: Replace stack label with a list view
# TODO: Catch up to old version in misc features -- units (no stupid stuff)
# TODO: fnwrtr control flow
# TODO: fnwrtr fix stupid combobox icon
# TODO: fnwrtr Stop everything from collapsing on update (its because of clear())
# TODO: Add stats functionality -- distributions, etc
# TODO: Add units functionality using new strings functionality
# TODO: Make macro label a function browser where you can expand/open and edit functions
# TODO: Make var label display matrices correctly
# TODO: Fix growing spaces in list (.sq repeat on list make spaces grow)
# TODO: Make data load/save from a json
# TODO: Update reserved keywords
# TODO: make a unit tab where you can click them and they get put on current items? similar structure to fnwrtr fns
# TODO: make transpose work on single row matrices
# TODO: work on pack and unpack so they work with matrices better
# TODO: conversions -- dtr(deg to rad), rtd(rad to deg), ctpd(cartesian to polar), ctsd(cartesian to spherical),
# TODO:                ctcd(cartesian to cylindrical) and other way for all as well as xxxr for radians.
# TODO: Make matrw rows and cols scale to fit in window until a certain point at which scroll is enabled?
# TODO: make the docs
# TODO: more stuff in general
# TODO: Make log give basic useful information other than errors
# TODO: make quadrature work, implement secant root finding
