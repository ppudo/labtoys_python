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
from . import DAQ_channel_config as CFG

class DAQ_3497xA:

    def __init__( self, ip: str, port=5025 ):
        self.__device = SCPI_Socket( ip, port )
        self.__device.timeout = 15
        self.__device.sendDalay = 0.005

    #------------------------------------------------------------------------------------------------------------------------------------------------
    # General Instructions
    #------------------------------------------------------------------------------------------------------------------------------------------------
    def GetIDN( self ) -> list:
        ans = self.__device.SendCommandGetAns( "*IDN?" )
        if( len(ans) == 0 ): return []
        return ans.split( ',' )

    #----------------------------------------------------------------------------------------------
    class SYSTEM_CARD_IDX:
        CARD_1  = '100'
        CARD_2  = '200'
        CARD_3  = '300'

    #----------------------------------------------------------------------------------------------
    def GetSystemCardType( self, cardIdx: SYSTEM_CARD_IDX=SYSTEM_CARD_IDX.CARD_1 ) -> list:
        ans = self.__device.SendCommandGetAns( "SYST:CTYP? " + cardIdx )                      #SYSTem:CTYPe? {100|200|300}
        if( len(ans) == 0 ): return []
        return ans.split( ',' )

    #----------------------------------------------------------------------------------------------
    def DeviceReset( self ) -> bool:
        return self.__device.SendCommand( "*RST" ) == 0

    #------------------------------------------------------------------------------------------------------------------------------------------------
    # Channel Configurator
    #------------------------------------------------------------------------------------------------------------------------------------------------
    def ConfigVoltageDC( self, card: int, channel: int, range: CFG.VOLT_RANGE=CFG.VOLT_RANGE.RANGE_AUTO ) -> CFG.CHANNEL_CONFIG:
        channelCfg = CFG.CHANNEL_CONFIG( CFG.CHANNEL_TYPE.VOLT_DC, card, channel )
        channelCfg.voltRange = range
        channelCfg.scan = True
        if( self.__ConfigVoltageDC( channelCfg ) ):
            return channelCfg
        else:
            return None

    #----------------------------------------------------------------------------------------------
    def __ConfigVoltageDC( self, channel: CFG.CHANNEL_CONFIG, connIdx=0 ) -> bool:
        if( channel.channelType == CFG.CHANNEL_TYPE.VOLT_DC ):
            command = "CONF:VOLT:DC "
            command += f"{channel.voltRange},{channel.ChannelString(True)}"
            return self.__device.SendCommand( command, connIdx=connIdx ) == connIdx
        else:
            return False

    #----------------------------------------------------------------------------------------------
    def ConfigVoltageAC( self, card: int, channel: int, range: CFG.VOLT_RANGE=CFG.VOLT_RANGE.RANGE_AUTO ) -> CFG.CHANNEL_CONFIG:
        channelCfg = CFG.CHANNEL_CONFIG( CFG.CHANNEL_TYPE.VOLT_AC, card, channel )
        channelCfg.voltRange = range
        channelCfg.scan = True
        if( self.__ConfigVoltageAC( channelCfg ) ):
            return channelCfg
        else:
            return None

    #----------------------------------------------------------------------------------------------
    def __ConfigVoltageAC( self, channel: CFG.CHANNEL_CONFIG, connIdx=0 ) -> bool:
        if( channel.channelType == CFG.CHANNEL_TYPE.VOLT_AC ):
            command = "CONF:VOLT:AC "
            command += f"{channel.voltRange},{channel.ChannelString(True)}"
            return self.__device.SendCommand( command, connIdx=connIdx ) == connIdx
        else:
            return False

    #----------------------------------------------------------------------------------------------
    def ConfigTempThermocuple( self, card: int, channel: int, type: CFG.THERMOCOUPLE_TYPE=CFG.THERMOCOUPLE_TYPE.TYPE_K ) -> bool:
        channelCfg = CFG.CHANNEL_CONFIG( CFG.CHANNEL_TYPE.TEMP_THERMOCOUPLE, card, channel )
        channelCfg.thermocoupleType = type
        channelCfg.scan = True
        if( self.__ConfigTempThermocuple( channelCfg ) ):
            return channelCfg
        else:
            return None

    #----------------------------------------------------------------------------------------------
    def __ConfigTempThermocuple( self, channel: CFG.CHANNEL_CONFIG, connIdx=0 ) -> bool:
        if( channel.channelType == CFG.CHANNEL_TYPE.TEMP_THERMOCOUPLE ):
            command = "CONF:TEMP TC,"
            command += f"{channel.thermocoupleType},{channel.ChannelString(True)}"
            return self.__device.SendCommand( command, connIdx=connIdx ) == connIdx
        else:
            return False

    #------------------------------------------------------------------------------------------------------------------------------------------------
    def __SendScanList( self, channels: list, connIdx=0 ) -> bool:
        command = "ROUT:SCAN (@"
        count = 0
        for ch in channels:
            if( ch.scan ):
                if( count != 0 ):
                    command += ","
                command += ch.ChannelString()
                count += 1
        command += ")"
        if( count == 0 ):
            return False
        return self.__device.SendCommand( command, connIdx=connIdx ) == connIdx

    #----------------------------------------------------------------------------------------------
    def SendScanList( self, channels: list ) -> bool:
        return self.__SendScanList( channels )    

    #----------------------------------------------------------------------------------------------
    def ConfigureChannel( self, channel: CFG.CHANNEL_CONFIG, connIdx=0 ) -> bool:
        if( channel.channelType == CFG.CHANNEL_TYPE.VOLT_DC ):
            return self.__ConfigVoltageDC( channel, connIdx )
        elif( channel.channelType == CFG.CHANNEL_TYPE.VOLT_AC ):
            return self.__ConfigVoltageAC( channel, connIdx )
        elif( channel.channelType == CFG.CHANNEL_TYPE.TEMP_THERMOCOUPLE ):
            return self.__ConfigTempThermocuple( channel, connIdx )
        else:
            return False

    #----------------------------------------------------------------------------------------------
    def ConfigureChannels( self, channels: list ) -> bool:
        connIdx = self.__device.Connect()
        if( connIdx == -1 ):    return False

        #configure channels
        status = True
        for i, ch, in enumerate( channels ):
            status &= self.ConfigureChannel( ch, connIdx )
            if( status == False ): break
        
        #send scan list
        if( status ):
            status &= self.__SendScanList( channels, connIdx )

        self.__device.Close( connIdx )
        return status

    #----------------------------------------------------------------------------------------------
    def Read( self ) -> list:
        command = "READ?"
        ans = self.__device.SendCommandGetAns( command )
        if( len(ans) == 0 ): return []

        result = ans.split( "," )
        for i in range( len( result ) ):
            result[i] = float( result[i] )
        return result
