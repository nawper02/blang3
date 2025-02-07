from blang import Blang

# pyinstaller BLANG3.spec --noconfirm


def main():
    blang = Blang()
    blang.run()


if __name__ == "__main__":
    main()


# TODO: UNITS
# TODO: make variable list have folders maybe
# TODO: add delete button to fnwrtr or make right click delete
# TODO: add imaginary number type and operations, quadratic formula
# TODO: fnwrtr control flow -- loops -- more prefixes? maybe prefixes for loops? prefix entire lines (just put char on each token automatically)
# TODO: add grapher function and popup window
# TODO: make ui paths automatic so it doesnt only work for me
# TODO: refactor interpreter.interpret_tokens, refactor parser is_value and get_value
# TODO: fnwrtr fix stupid combobox icon
# TODO: fnwrtr Stop everything from collapsing on update (its because of clear())
# TODO: Add stats functionality -- distributions, etc, regressions for sure (lists)
# TODO: Add units functionality using new strings functionality
# TODO: Make var label display matrices correctly
# TODO: Fix growing spaces in list (.sq repeat on list make spaces grow)
# TODO: Make data load/save from a file (and save on close) -- https://pyinstaller.org/en/stable/spec-files.html#using-spec-files - pickle
# TODO: Update reserved keywords
# TODO: make a unit tab where you can click them and they get put on current items? similar structure to fnwrtr fns
# TODO: make transpose work on single row matrices
# TODO: work on pack and unpack so they work with matrices better
# TODO: conversions -- dtr(deg to rad), rtd(rad to deg), ctpd(cartesian to polar), ctsd(cartesian to spherical),
# TODO:                ctcd(cartesian to cylindrical) and other way for all as well as xxxr for radians.
# TODO: Make matrw rows and cols scale to fit in window until a certain point at which scroll is enabled?
# TODO: make the docs - note: no spaces in lists if list is arg to fn
# TODO: more stuff in general
# TODO: Make log give basic useful information other than errors
# TODO: make quadrature work, implement secant root finding
