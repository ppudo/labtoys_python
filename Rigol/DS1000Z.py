#DS1000Z.py
#   Created on:	2020.10.28
#       Author: ppudo
#       e-mail:	ppudo@outlook.com
#
#   Project: 	labtoys
#   Description: 	Class representing Rigol DS1000Z osciloscope series 
#
#
#   Changelog:
#      	-2020.10.28		version: 0.1.0
#      		- Initial class
#
#----------------------------------------------------------------------------------------------------------------------------------------------------
#       Idea and changes proposal:
#           
#       
#       Usefull information and links:
#           Programing manual:  https://rigol.com.pl/pl/p/file/4b4d1a97273d6a3ddc301181fa34fb11/MSO1000ZDS1000Z_ProgrammingGuide_EN.pdf      (2020.11.10)
#           Product page:       https://www.rigolna.com/products/digital-oscilloscopes/1000z/       (2020.11.10)
#

import scpi
from enum import Enum

class DS1000Z:
    def __init__( self, aIP="", aPort=5555 ):
        self.__device = scpi.SCPI_Socket( aIP, aPort )

    #--------------------------------------------
    def Connect( self, timeout=10 ):
        self.__device.Connect( timeout )

    #--------------------------------------------
    def Close( self ):
        self.__device.Close()

    #----------------------------------------------------------------------------------------------
    #Basic Commands - works as basic keys on scope
    #----------------------------------------------------------------------------------------------

    def Autoscale( self ):
        self.__device.SendCommand( "AUT" )                                                          #AUToscale

    #--------------------------------------------
    def Clear( self ):
        self.__device.SendCommand( "CLE" )                                                          #CLEar

    #--------------------------------------------
    def Run( self ):
        self.__device.SendCommand( "RUN" )                                                          #RUN

    #--------------------------------------------
    def Stop( self ):
        self.__device.SendCommand( "STOP" )                                                         #STOP

    #--------------------------------------------
    def Single( self ):
        self.__device.SendCommand( "SING" )                                                         #SINGLE

    #--------------------------------------------
    def TriggerForce( self ):
        self.__device.SendCommand( "TFOR" )                                                         #TFORce

    #----------------------------------------------------------------------------------------------
    #CHANNELS Commands
    #----------------------------------------------------------------------------------------------

    class CHANNEL_NUMBER(Enum):
        CH1     = '1'
        CH2     = '2'
        CH3     = '3'
        CH4     = '4'

    #---------------------------------------------------------------------
    class CHANNEL_BANDWIDTH(Enum):
        BAND_20M    = '20M'
        FULL        = 'OFF'

    #--------------------------------------------
    def SetChannelBandwidth( self, chanelNumber: CHANNEL_NUMBER, bandwidth: CHANNEL_BANDWIDTH=CHANNEL_BANDWIDTH.FULL ):
        self.__device.SendCommand( "CHAN" + chanelNumber.value + ":BWL " + bandwidth.value )

    #--------------------------------------------
    def GetChannelBandwidth( self, chanelNumber: CHANNEL_NUMBER ) -> CHANNEL_BANDWIDTH:
        ans = self.__device.SendCommandGetAns( "CHAN" + chanelNumber.value + ":BWL?" )
        try:
            return self.CHANNEL_BANDWIDTH( ans )
        except ValueError:
            return None

    #----------------------------------------------------------------------------------------------
    #DISPLAY Commands
    #----------------------------------------------------------------------------------------------

    def ClearDisplay( self ):
        self.__device.SendCommand( "DISP:CLE" )

    #---------------------------------------------------------------------
    def GetScreenDataBitmap( self ):
        self.__device.SendCommand( "DISP:DATA?" )
        header = self.__device.GetAns( 2 )                                                          #get begin of header #x - where x is length of rest of header
        header = int( header[1] )                                                                   #convert string to int
        length = int( self.__device.GetAns( header ) ) + 1                                          #get rest of heder info - this is length of bytes in stream with screen data + ending \n

        #get rest of stream data, loop reads data to end of stream in packet
        screen = b''
        while len(screen) < length:
            data = self.__device.GetRaw( length )
            screen = screen + data
        
        screen = screen[:len(screen)-1]                                                               #remove /n from end of stream
        return screen

    #--------------------------------------------
    def SaveScreenToBitmap( self, path ):
        screen = self.GetScreenDataBitmap()
        f = open( path, 'wb' )
        f.write( screen )
        f.close()

    #---------------------------------------------------------------------
    class DISPLAY_TYPE(Enum):
        VECTORS     = 'VECT'
        DOTS        = 'DOTS'

    #--------------------------------------------
    def SetDisplayType( self, type: DISPLAY_TYPE=DISPLAY_TYPE.VECTORS ):
        self.__device.SendCommand( "DISP:TYPE " + type.value )

    #--------------------------------------------
    def GetDisplayType( self ) -> DISPLAY_TYPE:
        ans = self.__device.SendCommandGetAns( "DISP:TYPE?" )
        try:
            return self.DISPLAY_TYPE( ans )
        except ValueError:
            return None

    #----------------------------------------------------------------------------------------------
    #IEEE488.2 Common Commands
    #----------------------------------------------------------------------------------------------

    def GetIDN( self ):
        ans = self.__device.SendCommandGetAns( "*IDN?" )
        idn = ans.split( ',' )
        return idn

    #---------------------------------------------------------------------
    def ClearStatus( self ):
        self.__device.SendCommand( "*CLS" )

    #---------------------------------------------------------------------
    def EnableOperationComplete( self ):
        self.__device.SendCommand( "*OPC" )

    #---------------------------------------------------------------------
    def IsOperationComplete( self ):
        ans = self.__device.SendCommandGetAns( "*OPC?" )
        if ans=="1":
            return True
        else: 
            return False

    #---------------------------------------------------------------------
    def RestoreToDefaultState( self ):
        self.__device.SendCommand( "*RST" )

    #---------------------------------------------------------------------
    def SelfTest( self ):
        ans = self.__device.SendCommandGetAns( "*TST?" )
        return int( ans )

    #----------------------------------------------------------------------------------------------
    #TRIGGER Commands
    #----------------------------------------------------------------------------------------------

    class TRIGGER_MODE(Enum):
        EDGE        = 'EDGE'
        PULSE       = 'PULSE'
        RUNT        = 'RUNT'
        WINDOW      = 'WIND'
        NTH         = 'NEDG'
        SLOPE       = 'SLOP'
        VIDEO       = 'VID'
        PATTERN     = 'PATT'
        DELAY       = 'DEL'
        TIMEOUT     = 'TIM'
        DURATION    = 'DUR'
        STPHOLD     = 'SHOL'
        RS232       = 'RS232'
        I2C         = 'IIC'
        SPI         = 'SPI'

    #--------------------------------------------
    def SetTriggerMode( self, mode: TRIGGER_MODE=TRIGGER_MODE.EDGE ):
        self.__device.SendCommand( "TRIG:MODE " + mode.value )

    #--------------------------------------------
    def GetTriggerMode( self ) -> TRIGGER_MODE:
        ans = self.__device.SendCommandGetAns( "TRIG:MODE?" )
        try:
            return self.TRIGGER_MODE( ans )
        except ValueError:
            return None

    #---------------------------------------------------------------------
    class TRIGGER_STATUS(Enum):
        TD      = 'TD'
        WAIT    = 'WAIT'
        RUN     = 'RUN'
        AUTO    = 'AUTO'
        STOP    = 'STOP'

    #--------------------------------------------
    def GetTriggerStatus( self ) -> TRIGGER_STATUS:
        ans = self.__device.SendCommandGetAns( "TRIG:STAT?" )
        try:
            return self.TRIGGER_STATUS( ans )
        except ValueError:
            return None

    #----------------------------------------------------------------------------------------------
    #WAVEFORMS Commands
    #----------------------------------------------------------------------------------------------

    class WAVEFORM_SOURCE(Enum):
        CH1     = 'CHAN1'
        CH2     = 'CHAN2'
        CH3     = 'CHAN3'
        CH4     = 'CHAN4'
        MATH    = 'MATH'
        D0      = 'D0'
        D1      = 'D1'
        D2      = 'D2'
        D3      = 'D3'
        D4      = 'D4'
        D5      = 'D5'
        D6      = 'D6'
        D7      = 'D7'
        D8      = 'D8'
        D9      = 'D9'
        D10     = 'D10'
        D11     = 'D11'
        D12     = 'D12'
        D13     = 'D13'
        D14     = 'D14'
        D15     = 'D15'

    #--------------------------------------------
    def SetWaveformSource( self, source: WAVEFORM_SOURCE=WAVEFORM_SOURCE.CH1 ):
        self.__device.SendCommand( "WAV:SOUR " + source.value )
        
    #--------------------------------------------
    def GetWaveformSource( self ) -> WAVEFORM_SOURCE:
        ans = self.__device.SendCommandGetAns( "WAV:SOUR?" )
        try:
            return self.WAVEFORM_SOURCE( ans )
        except ValueError:
            return None

    #---------------------------------------------------------------------
    class WAVEFORM_MODE(Enum):
        NORMAL  = 'NORM'
        MAXIMUM = 'MAX'
        RAW     = 'RAW'

    #--------------------------------------------
    def SetWaveformMode( self, mode: WAVEFORM_MODE=WAVEFORM_MODE.NORMAL ):
        self.__device.SendCommand( "WAV:MODE " + mode.value )
        
    #--------------------------------------------
    def GetWaveformMode( self ) -> WAVEFORM_MODE:
        ans = self.__device.SendCommandGetAns( "WAV:MODE?" )
        try:
            return self.WAVEFORM_MODE( ans )
        except ValueError:
            return None

    #---------------------------------------------------------------------
    class WAVEFORM_FORMAT(Enum):
        WORD    = 'WORD'
        BYTE    = 'BYTE'
        ASCII   = 'ASC'

    #--------------------------------------------
    def SetWaveformFormat( self, format: WAVEFORM_FORMAT=WAVEFORM_FORMAT.BYTE ):
        self.__device.SendCommand( "WAV:FORM " + format.value )
        
    #--------------------------------------------
    def GetWaveformFormat( self ) -> WAVEFORM_FORMAT:
        ans = self.__device.SendCommandGetAns( "WAV:FORM?" )
        try:
            return self.WAVEFORM_FORMAT( ans )
        except ValueError:
            return None

    #---------------------------------------------------------------------
    def GetWaveformXincrement( self ) -> float:
        ans = self.__device.SendCommandGetAns( "WAV:XINC?" )
        return float( ans )   

    #---------------------------------------------------------------------
    def GetWaveformXorigin( self ) -> float:
        ans = self.__device.SendCommandGetAns( "WAV:XOR?" )
        return float( ans )

    #---------------------------------------------------------------------
    def GetWaveformXreference( self ) -> float:
        ans = self.__device.SendCommandGetAns( "WAV:XREF?" )
        return float( ans )

    #---------------------------------------------------------------------
    def GetWaveformYincrement( self ) -> float:
        ans = self.__device.SendCommandGetAns( "WAV:YINC?" )
        return float( ans )

    #---------------------------------------------------------------------
    def GetWaveformYorigin( self ) -> float:
        ans = self.__device.SendCommandGetAns( "WAV:YOR?" )
        return float( ans )

    #---------------------------------------------------------------------
    def GetWaveformYreference( self ) -> float:
        ans = self.__device.SendCommandGetAns( "WAV:YREF?" )
        return float( ans )

    #---------------------------------------------------------------------
    def SetWaveformStart( self, start: int ):
        self.__device.SendCommand( "WAV:STAR " + str(start) )

    #--------------------------------------------
    def GetWaveformStart( self ) -> int:
        ans = self.__device.SendCommandGetAns( "WAV:STAR?" )
        return int( ans )

    #---------------------------------------------------------------------
    def SetWaveformStop( self, start: int ):
        self.__device.SendCommand( "WAV:STOP " + str(start) )

    #--------------------------------------------
    def GetWaveformStop( self ) -> int:
        ans = self.__device.SendCommandGetAns( "WAV:STOP?" )
        return int( ans )

    #---------------------------------------------------------------------
    class WAVFORM_PREAMBLE_IDX(Enum):
        FORMAT      = 0
        TYPE        = 1
        POINTS      = 2
        COUNT       = 3
        X_INCREMENT = 4
        X_ORIGIN    = 5
        X_REFERENCE = 6
        Y_INCREMENT = 7
        Y_ORIGIN    = 8
        Y_REFERENCE = 9

    #--------------------------------------------
    def GetWaveformPreamble( self ):
        ans = self.__device.SendCommandGetAns( "WAV:PRE?" )
        return ans.split( ',' )


    #---------------------------------------------------------------------
    def GetWaveformDataRaw( self, source: WAVEFORM_SOURCE=WAVEFORM_SOURCE.CH1 ):
        self.Stop()                                                                                 #data can be rady only when scope is stoped
        self.SetWaveformSource( source )                                                            #specify sourece of data
        self.SetWaveformMode( self.WAVEFORM_MODE.RAW )                                              #raw data type
        self.SetWaveformFormat( self.WAVEFORM_FORMAT.ASCII )                                        #data converted to ascii - no calculation needed

        #download information about waveform data
        preamble = self.GetWaveformPreamble()
        pointsCount = int( preamble[ self.WAVFORM_PREAMBLE_IDX.POINTS.value ] )

        currentStartIdx = 1
        points = b''
        while currentStartIdx <= pointsCount:
            #change range of data to read
            self.SetWaveformStart( currentStartIdx )
            restOfPoints = pointsCount-currentStartIdx
            if restOfPoints > 100000:                                                                 #max package is 131072 points of data, 100000 is round number
                self.SetWaveformStop( currentStartIdx+99999 )                                         #99999 couse with 1 is number of the last point
            else:
                self.SetWaveformStop( currentStartIdx + (pointsCount-currentStartIdx) )

            #start read data
            self.__device.SendCommand( "WAV:DATA?" )
            header = self.__device.GetAns( 2 )                                                      #get begin of header #x - where x is length of rest of header
            header = int( header[1] )                                                               #convert string to int
            length = int( self.__device.GetAns( header ) ) + 1                                      #get rest of heder info - this is length of bytes to read from stream + ending \n 
        
            #get rest of stream data, loop reads data to end of stream in packet
            data = b''
            while len(data) < length:
                newData = self.__device.GetRaw( length )
                data = data + newData

            points = points + data[:len(data)-1] + b','                                              #remove ending from data
            currentStartIdx = currentStartIdx + 100000

        points = points[:len(points)-1]
        points = points.decode( "UTF-8" ).rstrip().split( ',' )
        for i in range( len( points ) ):
            points[i] = float( points[i] )

        return points

    #---------------------------------------------------------------------
    def GetWaveformDataScreen( self, source: WAVEFORM_SOURCE=WAVEFORM_SOURCE.CH1 ):
        self.Stop()                                                                                 #data can be rady only when scope is stoped
        self.SetWaveformSource( source )                                                            #specify sourece of data
        self.SetWaveformMode( self.WAVEFORM_MODE.NORMAL )                                           #raw data type
        self.SetWaveformFormat( self.WAVEFORM_FORMAT.ASCII )                                        #data converted to ascii - no calculation needed

        self.SetWaveformStart( 1 )
        self.SetWaveformStop( 1200 )   

        #start read data
        self.__device.SendCommand( "WAV:DATA?" )
        header = self.__device.GetAns( 2 )                                                          #get begin of header #x - where x is length of rest of header
        header = int( header[1] )                                                                   #convert string to int
        length = int( self.__device.GetAns( header ) ) + 1                                          #get rest of heder info - this is length of bytes to read from stream + ending \n

        #get stream data
        data = b''
        while len(data) < length:
            newData = self.__device.GetRaw( length )
            data = data + newData

        data = data[:len(data)-1]                                                                   #remove ending from data
        data = data.decode( "UTF-8" ).rstrip().split( ',' )
        for i in range( len( data ) ):
            data[i] = float( data[i] )

        return data
    

    