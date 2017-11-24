# coding: utf-8

debug = False

import sys
import os

def silent(function):
    """ fonction wraper qui empeche les functions avec @silent de print si la variable global debug est à False, si debug est à True les fonctions s'affichent normalement """
    def stop_print(*args):
        """ prevent a function to print """
        global debug
        if debug == True:
            if not args:
                res = function()
            else:
                res = function(*args)
            return res
        else:
            sys.stdout = open(os.devnull, "w")
            if not args:
                res = function()
            else:
                res = function(*args)
            sys.stdout = sys.__stdout__
            return res
    return stop_print
