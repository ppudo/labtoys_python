#functions.py
#   Created on:	2020.11.19
#       Author: ppudo
#       e-mail:	ppudo@outlook.com
#
#   Project: 	labtoys
#   Description: 	functions that help writing scripts
#
#
#   Changelog:
#      	-2021.11.18		version: 0.1.0
#      		- Wait functions
#
#----------------------------------------------------------------------------------------------------------------------------------------------------
#       Idea and changes proposal:
#           
#       
#       Usefull information and links:
#

import time

#----------------------------------------------------------------------------------------------------------------------------------------------------
def Wait( info, sleepTime: int ):
    if( sleepTime > 0 ):
        for i in range( sleepTime ):
            print( info + "\t\t" + str( sleepTime-i ) + "          ", end="\r" )
            time.sleep( 1.0 )
    print( " "*len(info) + "\t\t" + " "*10, end="\r" )