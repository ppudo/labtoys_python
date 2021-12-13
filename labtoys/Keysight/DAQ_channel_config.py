#DAQ_channel_config.py
#   Created on:	2020.12.13
#       Author: ppudo
#       e-mail:	ppudo@outlook.com
#
#   Project: 	labtoys
#   Description: 	Class representing channel description for Keysight 3497xA - Data Acquisition / Data Logger
#
#
#   Changelog:
#      	-2021.12.13		version: 0.1.0
#      		- Initial class
#

class CHANNEL_TYPE:
    VOLT_DC             = 0
    VOLT_AC             = 1
    TEMP_THERMOCOUPLE   = 2

#--------------------------------------------------------------------------------------------------
class VOLT_RANGE:
    RANGE_100mV     = '0.1'
    RANGE_1V        = '1'
    RANGE_10V       = '10'
    RANGE_100V      = '100'
    RANGE_300V      = '300'
    RANGE_AUTO      = 'AUTO'

#--------------------------------------------------------------------------------------------------
class THERMOCOUPLE_TYPE:
    TYPE_B  = 'B'
    TYPE_E  = 'E'
    TYPE_J  = 'J'
    TYPE_K  = 'K'
    TYPE_N  = 'N'
    TYPE_R  = 'R'
    TYPE_S  = 'S'
    TYPE_T  = 'T'

#--------------------------------------------------------------------------------------------------
class TEMP_UNIT:
    CELSIUS     = 'C'
    FAHRENHEIT  = 'F'
    KELVIN      = 'K'

#--------------------------------------------------------------------------------------------------
class RESOLUTION:
    RES_4_HALF_DIGIT    = 1000
    RES_5_HALF_DIGIT    = 10000
    RES_6_HALF_DIGIT    = 100000

#----------------------------------------------------------------------------------------------------------------------------------------------------
class CHANNEL_CONFIG:

    def __init__( self, type: CHANNEL_TYPE=CHANNEL_TYPE.VOLT_DC, card: int=1, channel: int=1 ):
        self.channelType = type
        self.card = card
        self.channel = channel
        self.scan = True

        #Volt
        self.voltRange = VOLT_RANGE.RANGE_AUTO

        #Thermocouple
        self.thermocoupleType = THERMOCOUPLE_TYPE.TYPE_K
        self.tempUnit = TEMP_UNIT.CELSIUS

        #Mx+B scaling
        self.gain = 1.0
        self.offset = 0.0
        #self.unit = #TO DO

    #----------------------------------------------------------------------------------------------
    def ChannelString( self, withAt=False ) -> str:
        return ChannelString( self.card, self.channel, withAt )

    #----------------------------------------------------------------------------------------------
    def Scaling( self, value: float ) -> float:
        return value * self.gain + self.offset

#----------------------------------------------------------------------------------------------------------------------------------------------------
def ChannelString( card, channel, withAt=False ) -> str:
    res = '{:01}'.format( card ) + '{:02}'.format( channel )
    if( withAt ):
        res = "(@" + res + ")"
    return res