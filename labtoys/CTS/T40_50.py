#T40_50.py
#   Created on:	2020.11.02
#       Author: ppudo
#       e-mail:	ppudo@outlook.com
#
#   Project: 	labtoys
#   Description: 	Class representing CTS T-40/50 climate chamber
#
#
#   Changelog:
#      	-2021.11.02		version: 0.1.0
#      		- Initial class
#
#----------------------------------------------------------------------------------------------------------------------------------------------------
#       Idea and changes proposal:
#           
#       
#       Usefull information and links:
#           

from ..scpi import SCPI_Socket

class T40_50:
    def __init__( self, ip, port=1080 ):
        self.__device = SCPI_Socket( ip, port )
        self.__device.timeout = 3
        self.__device.lineEnding = ""

    #------------------------------------------------------------------------------------------------------------------------------------------------
    def GetMeasuredTemp( self ) -> float:
        respond = self.__device.SendCommandGetAns( "A0", respondLength=14 )
        if( respond == None ):  return float('nan')
        value = float( respond[3:8] )
        return value

    #----------------------------------------------------------------------------------------------
    def ReadSetTemp( self ) -> float:
        respond = self.__device.SendCommandGetAns( "A0", respondLength=14 )
        if( respond == None ):  return float('nan')
        value = float( respond[9:14] )
        return value

    #----------------------------------------------------------------------------------------------
    def SetTemp( self, temp: float ) -> bool:
        respond = self.__device.SendCommandGetAns( "a0 " + "{0:3.1f}".format(temp).zfill(5) )
        if( respond == None
            and (respond != "A" and respond != "a") ):
            return False
        return True

    #------------------------------------------------------------------------------------------------------------------------------------------------
    def StartChamber( self ):
        respond = self.__device.SendCommandGetAns( "s1 1" )
        if( respond == None
            and (respond != "S1" and respond != "s1") ):
            return False
        return True

    #----------------------------------------------------------------------------------------------
    def StopChamber( self ):
        respond = self.__device.SendCommandGetAns( "s1 0" )
        if( respond == None
            and (respond != "S1" and respond != "s1") ):
            return False
        return True

    #------------------------------------------------------------------------------------------------------------------------------------------------
    def ReadGradientUp( self ):
        respond = self.__device.SendCommandGetAns( "U1", respondLength=14 )
        if( respond == None ):  return float('nan')
        value = float( respond[3:8] )
        return value

    #----------------------------------------------------------------------------------------------
    def ReadGradientDown( self ):
        respond = self.__device.SendCommandGetAns( "U1", respondLength=14 )
        if( respond == None ):  return float('nan')
        value = float( respond[9:14] )
        return value
    

