# -*- coding: utf-8 -*-

# Type definiton for (type, data) tuples representing a value
# See http://androidxref.com/9.0.0_r3/xref/frameworks/base/libs/androidfw/include/androidfw/ResourceTypes.h#262

# The 'data' is either 0 or 1, specifying this resource is either
# undefined or empty, respectively.
TYPE_NULL = 0x00
# The 'data' holds a ResTable_ref, a reference to another resource
# table entry.
TYPE_REFERENCE = 0x01
# The 'data' holds an attribute resource identifier.
TYPE_ATTRIBUTE = 0x02
# The 'data' holds an index into the containing resource table's
# global value string pool.
TYPE_STRING = 0x03
# The 'data' holds a single-precision floating point number.
TYPE_FLOAT = 0x04
# The 'data' holds a complex number encoding a dimension value
# such as "100in".
TYPE_DIMENSION = 0x05
# The 'data' holds a complex number encoding a fraction of a
# container.
TYPE_FRACTION = 0x06
# The 'data' holds a dynamic ResTable_ref, which needs to be
# resolved before it can be used like a TYPE_REFERENCE.
TYPE_DYNAMIC_REFERENCE = 0x07
# The 'data' holds an attribute resource identifier, which needs to be resolved
# before it can be used like a TYPE_ATTRIBUTE.
TYPE_DYNAMIC_ATTRIBUTE = 0x08
# Beginning of integer flavors...
TYPE_FIRST_INT = 0x10
# The 'data' is a raw integer value of the form n..n.
TYPE_INT_DEC = 0x10
# The 'data' is a raw integer value of the form 0xn..n.
TYPE_INT_HEX = 0x11
# The 'data' is either 0 or 1, for input "false" or "true" respectively.
TYPE_INT_BOOLEAN = 0x12
# Beginning of color integer flavors...
TYPE_FIRST_COLOR_INT = 0x1C
# The 'data' is a raw integer value of the form #aarrggbb.
TYPE_INT_COLOR_ARGB8 = 0x1C
# The 'data' is a raw integer value of the form #rrggbb.
TYPE_INT_COLOR_RGB8 = 0x1D
# The 'data' is a raw integer value of the form #argb.
TYPE_INT_COLOR_ARGB4 = 0x1E
# The 'data' is a raw integer value of the form #rgb.
TYPE_INT_COLOR_RGB4 = 0x1F
# ...end of integer flavors.
TYPE_LAST_COLOR_INT = 0x1F
# ...end of integer flavors.
TYPE_LAST_INT = 0x1F

# Constants for ARSC Files
# see http://androidxref.com/9.0.0_r3/xref/frameworks/base/libs/androidfw/include/androidfw/ResourceTypes.h#215
RES_NULL_TYPE = 0x0000
RES_STRING_POOL_TYPE = 0x0001
RES_TABLE_TYPE = 0x0002
RES_XML_TYPE = 0x0003

RES_XML_FIRST_CHUNK_TYPE = 0x0100
RES_XML_START_NAMESPACE_TYPE = 0x0100
RES_XML_END_NAMESPACE_TYPE = 0x0101
RES_XML_START_ELEMENT_TYPE = 0x0102
RES_XML_END_ELEMENT_TYPE = 0x0103
RES_XML_CDATA_TYPE = 0x0104
RES_XML_LAST_CHUNK_TYPE = 0x017F

RES_XML_RESOURCE_MAP_TYPE = 0x0180

RES_TABLE_PACKAGE_TYPE = 0x0200
RES_TABLE_TYPE_TYPE = 0x0201
RES_TABLE_TYPE_SPEC_TYPE = 0x0202
RES_TABLE_LIBRARY_TYPE = 0x0203

# Flags in the STRING Section
UTF8_FLAG = 1 << 8

# Position of the fields inside an attribute
ATTRIBUTE_IX_NAMESPACE_URI = 0
ATTRIBUTE_IX_NAME = 1
ATTRIBUTE_IX_VALUE_STRING = 2
ATTRIBUTE_IX_VALUE_TYPE = 3
ATTRIBUTE_IX_VALUE_DATA = 4
ATTRIBUTE_LENGHT = 5

# Internally used state variables for AXMLParser
START_DOCUMENT = 0
END_DOCUMENT = 1
START_TAG = 2
END_TAG = 3
TEXT = 4

# Table used to lookup functions to determine the value representation in ARSCParser
TYPE_TABLE = {
    TYPE_ATTRIBUTE: "attribute",
    TYPE_DIMENSION: "dimension",
    TYPE_FLOAT: "float",
    TYPE_FRACTION: "fraction",
    TYPE_INT_BOOLEAN: "int_boolean",
    TYPE_INT_COLOR_ARGB4: "int_color_argb4",
    TYPE_INT_COLOR_ARGB8: "int_color_argb8",
    TYPE_INT_COLOR_RGB4: "int_color_rgb4",
    TYPE_INT_COLOR_RGB8: "int_color_rgb8",
    TYPE_INT_DEC: "int_dec",
    TYPE_INT_HEX: "int_hex",
    TYPE_NULL: "null",
    TYPE_REFERENCE: "reference",
    TYPE_STRING: "string",
}

RADIX_MULTS = [0.00390625, 3.051758e-005, 1.192093e-007, 4.656613e-010]
DIMENSION_UNITS = ["px", "dip", "sp", "pt", "in", "mm"]
FRACTION_UNITS = ["%", "%p"]

COMPLEX_UNIT_MASK = 0x0F

ACONFIGURATION_MCC = 0x0001
ACONFIGURATION_MNC = 0x0002
ACONFIGURATION_LOCALE = 0x0004
ACONFIGURATION_TOUCHSCREEN = 0x0008
ACONFIGURATION_KEYBOARD = 0x0010
ACONFIGURATION_KEYBOARD_HIDDEN = 0x0020
ACONFIGURATION_NAVIGATION = 0x0040
ACONFIGURATION_ORIENTATION = 0x0080
ACONFIGURATION_DENSITY = 0x0100
ACONFIGURATION_SCREEN_SIZE = 0x0200
ACONFIGURATION_VERSION = 0x0400
ACONFIGURATION_SCREEN_LAYOUT = 0x0800
ACONFIGURATION_UI_MODE = 0x1000
ACONFIGURATION_LAYOUTDIR_ANY = 0x00
ACONFIGURATION_LAYOUTDIR_LTR = 0x01
ACONFIGURATION_LAYOUTDIR_RTL = 0x02
ACONFIGURATION_SCREENSIZE_ANY = 0x00
ACONFIGURATION_SCREENSIZE_SMALL = 0x01
ACONFIGURATION_SCREENSIZE_NORMAL = 0x02
ACONFIGURATION_SCREENSIZE_LARGE = 0x03
ACONFIGURATION_SCREENSIZE_XLARGE = 0x04
ACONFIGURATION_SCREENLONG_ANY = 0x00
ACONFIGURATION_SCREENLONG_NO = 0x1
ACONFIGURATION_SCREENLONG_YES = 0x2
ACONFIGURATION_TOUCHSCREEN_ANY = 0x0000
ACONFIGURATION_TOUCHSCREEN_NOTOUCH = 0x0001
ACONFIGURATION_TOUCHSCREEN_STYLUS = 0x0002
ACONFIGURATION_TOUCHSCREEN_FINGER = 0x0003
ACONFIGURATION_DENSITY_DEFAULT = 0
ACONFIGURATION_DENSITY_LOW = 120
ACONFIGURATION_DENSITY_MEDIUM = 160
ACONFIGURATION_DENSITY_TV = 213
ACONFIGURATION_DENSITY_HIGH = 240
ACONFIGURATION_DENSITY_XHIGH = 320
ACONFIGURATION_DENSITY_XXHIGH = 480
ACONFIGURATION_DENSITY_XXXHIGH = 640
ACONFIGURATION_DENSITY_ANY = 0xFFFE
ACONFIGURATION_DENSITY_NONE = 0xFFFF
MASK_LAYOUTDIR = 0xC0
MASK_SCREENSIZE = 0x0F
MASK_SCREENLONG = 0x30
SHIFT_LAYOUTDIR = 6
SHIFT_SCREENLONG = 4
LAYOUTDIR_ANY = ACONFIGURATION_LAYOUTDIR_ANY << SHIFT_LAYOUTDIR
LAYOUTDIR_LTR = ACONFIGURATION_LAYOUTDIR_LTR << SHIFT_LAYOUTDIR
LAYOUTDIR_RTL = ACONFIGURATION_LAYOUTDIR_RTL << SHIFT_LAYOUTDIR
SCREENSIZE_ANY = ACONFIGURATION_SCREENSIZE_ANY
SCREENSIZE_SMALL = ACONFIGURATION_SCREENSIZE_SMALL
SCREENSIZE_NORMAL = ACONFIGURATION_SCREENSIZE_NORMAL
SCREENSIZE_LARGE = ACONFIGURATION_SCREENSIZE_LARGE
SCREENSIZE_XLARGE = ACONFIGURATION_SCREENSIZE_XLARGE
SCREENLONG_ANY = ACONFIGURATION_SCREENLONG_ANY << SHIFT_SCREENLONG
SCREENLONG_NO = ACONFIGURATION_SCREENLONG_NO << SHIFT_SCREENLONG
SCREENLONG_YES = ACONFIGURATION_SCREENLONG_YES << SHIFT_SCREENLONG
DENSITY_DEFAULT = ACONFIGURATION_DENSITY_DEFAULT
DENSITY_LOW = ACONFIGURATION_DENSITY_LOW
DENSITY_MEDIUM = ACONFIGURATION_DENSITY_MEDIUM
DENSITY_TV = ACONFIGURATION_DENSITY_TV
DENSITY_HIGH = ACONFIGURATION_DENSITY_HIGH
DENSITY_XHIGH = ACONFIGURATION_DENSITY_XHIGH
DENSITY_XXHIGH = ACONFIGURATION_DENSITY_XXHIGH
DENSITY_XXXHIGH = ACONFIGURATION_DENSITY_XXXHIGH
DENSITY_ANY = ACONFIGURATION_DENSITY_ANY
DENSITY_NONE = ACONFIGURATION_DENSITY_NONE
TOUCHSCREEN_ANY = ACONFIGURATION_TOUCHSCREEN_ANY
TOUCHSCREEN_NOTOUCH = ACONFIGURATION_TOUCHSCREEN_NOTOUCH
TOUCHSCREEN_STYLUS = ACONFIGURATION_TOUCHSCREEN_STYLUS
TOUCHSCREEN_FINGER = ACONFIGURATION_TOUCHSCREEN_FINGER
