# Grandstream Phonebook Converter

This script is intended to convert a directory of vCards to the XML phonebook
format understood by Grandstream VoIP phones. It is implemented as CGI script as
the Grandstream phones are able to fetch their phonebook from an HTTP server.

There are some workarounds for limitations of the XML format included. Family
names are replaced by the type of the number (Work, Home, Cell, ..) for contacts
with multiple numbers and some special characters are replaced by an
approximation.

The code is tested with vCards created by `kaddressbook` and a Grandstream
GXP2100. It depends on the Python 2.x and the module `vobject`.

