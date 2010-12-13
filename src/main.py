#!/usr/bin/env python
#coding: iso-8859-1

"""Documentation for main.py

The main thing, runs everything, 
well not really, just invokes run from world :).

project -- Rez: The Clone
author -- Edwood Grant
organization -- Binhex Tw. 
version -- 1.00
since -- 7/07/2007 19:30:33
"""

import world

if __name__ == '__main__': 
    wrld = world.World()
    wrld.run()
