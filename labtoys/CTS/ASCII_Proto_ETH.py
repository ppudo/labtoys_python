#ASCII_Proto_ETH.py
#   Created on:	2020.11.02
#       Author: ppudo
#       e-mail:	ppudo@outlook.com
#
#   Project: 	labtoys
#   Description: 	Class representing CTS T-40/50 climate chamber - ethernet protocol
#
#
#   Changelog:
#      	-2021.11.02		version: 0.1.0
#      		- Initial class
#       -2021.11.08     version: 0.1.1
#           - update functions to assign return type
#
#----------------------------------------------------------------------------------------------------------------------------------------------------
#       Idea and changes proposal:
#           
#       
#       Usefull information and links:
#           ASCII protocol desription:  https://www.cts-umweltsimulation.de/en/component/emdown/downloadfile/10565.html?id=10565&Itemid=358     (2021.11.06)
#           

from ..scpi import SCPI_Socket

class ASCII_Proto_ETH:
    def __init__( self, ip, port=1080 ):
        self.__device = SCPI_Socket( ip, port )
        self.__device.timeout = 3
        self.__device.lineEnding = ""

    #------------------------------------------------------------------------------------------------------------------------------------------------
    def GetMeasuredTemp( self ) -> float:
        respond = self.__device.SendCommandGetAns( "A0", respondLength=14 )
        if( len( respond ) == 0 ):  return float('nan')
        value = float( respond[3:8] )
        return value

    #----------------------------------------------------------------------------------------------
    def ReadSetTemp( self ) -> float:
        respond = self.__device.SendCommandGetAns( "A0", respondLength=14 )
        if( len( respond ) == 0  ):  return float('nan')
        value = float( respond[9:14] )
        return value

    #----------------------------------------------------------------------------------------------
    def SetTemp( self, temp: float ) -> bool:
        respond = self.__device.SendCommandGetAns( "a0 " + "{0:3.1f}".format(temp).zfill(5), respondLength=1 )
        if( len( respond ) == 0 
            and (respond != "A" and respond != "a") ):
            return False
        return True

    #------------------------------------------------------------------------------------------------------------------------------------------------
    def StartChamber( self ) -> bool:
        respond = self.__device.SendCommandGetAns( "s1 1", respondLength=2 )
        if( len( respond ) == 0 
            and (respond != "S1" and respond != "s1") ):
            return False
        return True

    #----------------------------------------------------------------------------------------------
    def StopChamber( self ) -> bool:
        respond = self.__device.SendCommandGetAns( "s1 0", respondLength=2 )
        if( len( respond ) == 0 
            and (respond != "S1" and respond != "s1") ):
            return False
        return True

    #------------------------------------------------------------------------------------------------------------------------------------------------
    def ReadGradientUp( self ) -> float:
        respond = self.__device.SendCommandGetAns( "U1", respondLength=14 )
        if( len( respond ) == 0  ):  return float('nan')
        value = float( respond[3:8] )
        return value

    #----------------------------------------------------------------------------------------------
    def ReadGradientDown( self ) -> float:
        respond = self.__device.SendCommandGetAns( "U1", respondLength=14 )
        if( len( respond ) == 0  ):  return float('nan')
        value = float( respond[9:14] )
        return value
    

