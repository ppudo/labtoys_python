#DAQ_3497xA.py
#   Created on:	2020.11.18
#       Author: ppudo
#       e-mail:	ppudo@outlook.com
#
#   Project: 	labtoys
#   Description: 	Class representing Keysight 3497xA - Data Acquisition / Data Logger
#
#
#   Changelog:
#      	-2021.11.18		version: 0.1.0
#      		- Initial class
#
#----------------------------------------------------------------------------------------------------------------------------------------------------
#       Idea and changes proposal:
#           
#       
#       Usefull information and links:
#           Agilent 34970A/72A Commands:  https://documentation.help/Keysight-34970A-34972A/documentation.pdf     (2021.11.18)
#           User guide: https://www.keysight.com/zz/en/assets/9018-02644/user-manuals/9018-02644.pdf    (2021.11.18)
#           Agilent 34970A/72A user guide: https://testworld.com/wp-content/uploads/user-guide-keysight-agilent-34970a-34972a-daq.pdf   (2021.12.12)
# 

from ..scpi import SCPI_Socket
from enum import Enum

class DAQ_3497xA:

    def __init__( self, ip: str, port=5025 ):
        self.__device = SCPI_Socket( ip, port )
        self.__device.timeout = 3
        self.__device.sendDalay = 0.005

    #------------------------------------------------------------------------------------------------------------------------------------------------
    # General Instructions
    #------------------------------------------------------------------------------------------------------------------------------------------------
    def GetIDN( self ) -> list:
        ans = self.__device.SendCommandGetAns( "*IDN?" )
        if( len(ans) == 0 ): return []
        return ans.split( ',' )

    #----------------------------------------------------------------------------------------------
    class SYSTEM_CARD_IDX(Enum):
        CARD_1  = '100'
        CARD_2  = '200'
        CARD_3  = '300'

    #----------------------------------------------------------------------------------------------
    def GetSystemCardType( self, cardIdx: SYSTEM_CARD_IDX=SYSTEM_CARD_IDX.CARD_1 ) -> list:
        ans = self.__device.SendCommandGetAns( "SYST:CTYP? " + cardIdx.value )                      #SYSTem:CTYPe? {100|200|300}
        if( len(ans) == 0 ): return []
        return ans.split( ',' )

    #----------------------------------------------------------------------------------------------
    def DeviceReset( self ) -> bool:
        return self.__device.SendCommand( "*RST" ) == 0

    #------------------------------------------------------------------------------------------------------------------------------------------------
    class VOLT_RANGE(Enum):
        RANGE_100mV     = '0.1'
        RANGE_1V        = '1'
        RANGE_10V       = '10'
        RANGE_100V      = '100'
        RANGE_300V      = '300'
        RANGE_AUTO      = 'AUTO'

    #---------------------------------------------------------------------
    def ConfigureVoltageDC( self, card, channel, range: VOLT_RANGE = VOLT_RANGE.RANGE_AUTO ) -> bool:
        command = "CONF:VOLT:DC "
        command += range.value + ","
        command += self.__ConvertToChannelString( card, channel )
        return self.__device.SendCommand( command ) == 0

    #---------------------------------------------------------------------
    def ConfigureVoltageAC( self, card, channel, range: VOLT_RANGE = VOLT_RANGE.RANGE_AUTO ) -> bool:
        command = "CONF:VOLT:AC "
        command += range.value + ","
        command += self.__ConvertToChannelString( card, channel )
        return self.__device.SendCommand( command ) == 0

    #----------------------------------------------------------------------------------------------
    class THERMOCOUPLE_TYPE(Enum):
        TYPE_B  = 'B'
        TYPE_E  = 'E'
        TYPE_J  = 'J'
        TYPE_K  = 'K'
        TYPE_N  = 'N'
        TYPE_R  = 'R'
        TYPE_S  = 'S'
        TYPE_T  = 'T'

    #---------------------------------------------------------------------
    def ConfigureThermocouple( self, card: int, channel: int, type: THERMOCOUPLE_TYPE=THERMOCOUPLE_TYPE.TYPE_K ) -> bool:
        command = "CONF:TEMP TC,"
        command += type.value + ","
        command += self.__ConvertToChannelString( card, channel )
        return self.__device.SendCommand( command ) == 0

    #----------------------------------------------------------------------------------------------
    class TEMP_UNIT(Enum):
        CELSIUS     = 'C'
        FAHRENHEIT  = 'F'
        KELVIN      = 'K'

    #---------------------------------------------------------------------
    def SetTempeartureUnit( self, card: int, channel: int, unit: TEMP_UNIT=TEMP_UNIT.CELSIUS ) -> bool:
        command = "UNIT:TEMP "
        command += unit.value + ","
        command += self.__ConvertToChannelString( card, channel )
        return self.__device.SendCommand( command ) == 0

    #----------------------------------------------------------------------------------------------
    def ConfigureScanList( self, list: list ) -> bool:
        #list element '[ card: int, channel: int ]'
        command = "ROUT:SCAN (@"
        for i in range( len(list) ):
            if( i != 0 ):
                command += ","
            command += '{:01}'.format( list[i][0] ) + '{:02}'.format( list[i][1] )
        command += ")"
        return self.__device.SendCommand( command ) == 0

    #----------------------------------------------------------------------------------------------
    def Read( self ) -> list:
        command = "READ?"
        ans = self.__device.SendCommandGetAns( command )
        if( len(ans) == 0 ): return []

        result = ans.split( "," )
        for i in range( len( result ) ):
            result[i] = float( result[i] )
        return result

    #------------------------------------------------------------------------------------------------------------------------------------------------
    def __ConvertToChannelString( self, card: int, channel: int ) -> str:
        return "(@" + '{:01}'.format( card ) + '{:02}'.format( channel ) + ")"
