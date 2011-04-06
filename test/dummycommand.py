#!/usr/bin/env python
import sys
if sys.argv[1] == "status":
    print "el servicio esta...   running"
elif sys.argv[1] == "start":
    print "ejecutando bla bla... done"
else:
    print "ejecutando bla bla... eror"