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
#       -2021.09.29     version: 0.2.0
#           - Adapt to new scpi library
#
#----------------------------------------------------------------------------------------------------------------------------------------------------
#       Idea and changes proposal:
#           
#       
#       Usefull information and links:
#           Programing manual:  https://rigol.com.pl/pl/p/file/4b4d1a97273d6a3ddc301181fa34fb11/MSO1000ZDS1000Z_ProgrammingGuide_EN.pdf      (2020.11.10)
#           Product page:       https://www.rigolna.com/products/digital-oscilloscopes/1000z/       (2020.11.10)
#

from ..scpi import SCPI_Socket
from enum import Enum

class DS1000Z:
    def __init__( self, aIP, aPort=5555 ):
        self.__device = SCPI_Socket( aIP, aPort )
        self.__device.sendDalay = 0.001

    #----------------------------------------------------------------------------------------------
    #Basic Commands - works as basic keys on scope
    #----------------------------------------------------------------------------------------------

    def Autoscale( self ) -> bool:
        return self.__device.SendCommand( "AUT" ) == 0                                              #AUToscale                                                

    #--------------------------------------------
    def Clear( self ) -> bool:
        return self.__device.SendCommand( "CLE" ) == 0                                              #CLEar

    #--------------------------------------------
    def Run( self ) -> bool:
        return self.__device.SendCommand( "RUN" ) == 0                                              #RUN

    #--------------------------------------------
    def __Stop( self, connIdx: int ) -> bool:
        return self.__device.SendCommand( "STOP", connIdx=connIdx ) == connIdx                      #STOP

    def Stop( self ) -> bool:
        return self.__Stop( 0 )

    #--------------------------------------------
    def Single( self ) -> bool:
        return self.__device.SendCommand( "SING" ) == 0                                             #SINGLE

    #--------------------------------------------
    def TriggerForce( self ) -> bool:
        return self.__device.SendCommand( "TFOR" ) == 0                                             #TFORce

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
        ERROR       = 'ERROR'               #do not use, only for indication of results

    #--------------------------------------------
    def SetChannelBandwidth( self, chanelNumber: CHANNEL_NUMBER, bandwidth: CHANNEL_BANDWIDTH=CHANNEL_BANDWIDTH.FULL ) -> bool:
        return self.__device.SendCommand( "CHAN" + chanelNumber.value + ":BWL " + bandwidth.value ) == 0

    #--------------------------------------------
    def GetChannelBandwidth( self, chanelNumber: CHANNEL_NUMBER ) -> CHANNEL_BANDWIDTH:
        ans = self.__device.SendCommandGetAns( "CHAN" + chanelNumber.value + ":BWL?" )
        if( ans == "" ):    return self.CHANNEL_BANDWIDTH.ERROR

        try:
            return self.CHANNEL_BANDWIDTH( ans )
        except ValueError:
            return self.CHANNEL_BANDWIDTH.ERROR

    #----------------------------------------------------------------------------------------------
    #DISPLAY Commands
    #----------------------------------------------------------------------------------------------

    def ClearDisplay( self ) -> bool:
        return self.__device.SendCommand( "DISP:CLE" ) == 0

    #---------------------------------------------------------------------
    def GetScreenDataBitmap( self ) -> list:
        connIdx = self.__device.Connect()
        if( connIdx == -1 ): return []

        connIdx = self.__device.SendCommand( "DISP:DATA?", connIdx=connIdx )
        if( connIdx == -1 ):  return []

        header = self.__device.GetAns( 2, connIdx=connIdx )                                         #get begin of header #x - where x is length of rest of header
        if( len(header) == 0 ):   return []

        header = int( header[1] )                                                                   #convert string to int
        lengthInt = self.__device.GetAns( header, connIdx=connIdx )
        if( len( lengthInt) == 0 ): return []
        length = int( lengthInt ) + 1                                                               #get rest of heder info - this is length of bytes in stream with screen data + ending \n

        #get rest of stream data, loop reads data to end of stream in packet
        screen = b''
        while len(screen) < length:
            data = self.__device.GetRaw( length, connIdx=connIdx )
            if( len(data) == 0 ): return []
            screen = screen + data
        self.__device.Close( connIdx )
        
        screen = screen[:len(screen)-1]                                                               #remove /n from end of stream
        return screen

    #--------------------------------------------
    def SaveScreenToBitmap( self, path ) -> bool:
        screen = self.GetScreenDataBitmap()
        if( len(screen) == 0 ): return False

        try:
            f = open( path, 'wb' )
            f.write( screen )
            f.close()
        except:
            return False

        return True

    #---------------------------------------------------------------------
    class DISPLAY_TYPE(Enum):
        VECTORS     = 'VECT'
        DOTS        = 'DOTS'
        ERROR       = 'ERROR'           #do not use, only for indication of results

    #--------------------------------------------
    def SetDisplayType( self, type: DISPLAY_TYPE=DISPLAY_TYPE.VECTORS ) -> bool:
        return self.__device.SendCommand( "DISP:TYPE " + type.value ) == 0

    #--------------------------------------------
    def GetDisplayType( self ) -> DISPLAY_TYPE:
        ans = self.__device.SendCommandGetAns( "DISP:TYPE?" )
        if( len(ans) == 0 ):  self.DISPLAY_TYPE.ERROR

        try:
            return self.DISPLAY_TYPE( ans )
        except ValueError:
            return self.DISPLAY_TYPE.ERROR

    #----------------------------------------------------------------------------------------------
    #IEEE488.2 Common Commands
    #----------------------------------------------------------------------------------------------

    def GetIDN( self ) -> list:
        ans = self.__device.SendCommandGetAns( "*IDN?" )
        if( len(ans) == 0 ):  return []
        return ans.split( ',' )

    #---------------------------------------------------------------------
    def ClearStatus( self ) -> bool:
        return self.__device.SendCommand( "*CLS" ) == 0

    #---------------------------------------------------------------------
    def EnableOperationComplete( self ) -> bool:
        return self.__device.SendCommand( "*OPC" ) == 0

    #---------------------------------------------------------------------
    def IsOperationComplete( self ) -> bool:
        ans = self.__device.SendCommandGetAns( "*OPC?" )
        if( len(ans) == 0 ):  return False
        
        if ans=="1":
            return True
        else: 
            return False

    #---------------------------------------------------------------------
    def RestoreToDefaultState( self ) -> bool:
        return self.__device.SendCommand( "*RST" ) == 0

    #---------------------------------------------------------------------
    def SelfTest( self ) -> int:
        ans = self.__device.SendCommandGetAns( "*TST?" ) == 0
        if( ans == None ):  return None
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
        ERROR       = 'ERROR'       #do not use, only for indication of results

    #--------------------------------------------
    def SetTriggerMode( self, mode: TRIGGER_MODE=TRIGGER_MODE.EDGE ) -> bool:
        return self.__device.SendCommand( "TRIG:MODE " + mode.value ) == 0

    #--------------------------------------------
    def GetTriggerMode( self ) -> TRIGGER_MODE:
        ans = self.__device.SendCommandGetAns( "TRIG:MODE?" )
        if( len(ans) == 0 ):  return self.TRIGGER_MODE.ERROR

        try:
            return self.TRIGGER_MODE( ans )
        except ValueError:
            return self.TRIGGER_MODE.ERROR

    #---------------------------------------------------------------------
    class TRIGGER_STATUS(Enum):
        TD      = 'TD'
        WAIT    = 'WAIT'
        RUN     = 'RUN'
        AUTO    = 'AUTO'
        STOP    = 'STOP'
        ERROR   = 'ERROR'       #do not use, only for indication of results

    #--------------------------------------------
    def GetTriggerStatus( self ) -> TRIGGER_STATUS:
        ans = self.__device.SendCommandGetAns( "TRIG:STAT?" )
        if( len(ans) == 0 ):  return self.TRIGGER_STATUS.ERROR

        try:
            return self.TRIGGER_STATUS( ans )
        except ValueError:
            return self.TRIGGER_STATUS.ERROR

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
        ERROR   = 'ERROR'       #do not use, only for indication of results

    #--------------------------------------------
    def __SetWaveformSource( self, connIdx: int, source: WAVEFORM_SOURCE=WAVEFORM_SOURCE.CH1 ) -> bool:
        return self.__device.SendCommand( "WAV:SOUR " + source.value, connIdx=connIdx ) == connIdx

    def SetWaveformSource( self, source: WAVEFORM_SOURCE=WAVEFORM_SOURCE.CH1 ) -> bool:
        return self.__SetWaveformSource( 0, source )

    #--------------------------------------------
    def GetWaveformSource( self ) -> WAVEFORM_SOURCE:
        ans = self.__device.SendCommandGetAns( "WAV:SOUR?" )
        if( len( ans ) == 0 ): return self.WAVEFORM_SOURCE.ERROR

        try:
            return self.WAVEFORM_SOURCE( ans )
        except ValueError:
            return self.WAVEFORM_SOURCE.ERROR

    #---------------------------------------------------------------------
    class WAVEFORM_MODE(Enum):
        NORMAL  = 'NORM'
        MAXIMUM = 'MAX'
        RAW     = 'RAW'
        ERROR   = 'ERROR'       #do not use, only for indication of results

    #--------------------------------------------
    def __SetWaveformMode( self, connIdx: int, mode: WAVEFORM_MODE=WAVEFORM_MODE.NORMAL ) -> bool:
        return self.__device.SendCommand( "WAV:MODE " + mode.value, connIdx=connIdx ) == connIdx

    def SetWaveformMode( self, mode: WAVEFORM_MODE=WAVEFORM_MODE.NORMAL ) -> bool:
        return self.__SetWaveformMode( 0, mode=mode )   
    
    #--------------------------------------------
    def GetWaveformMode( self ) -> WAVEFORM_MODE:
        ans = self.__device.SendCommandGetAns( "WAV:MODE?" )
        if( len( ans ) == 0 ):  return self.WAVEFORM_MODE.ERROR

        try:
            return self.WAVEFORM_MODE( ans )
        except ValueError:
            return self.WAVEFORM_MODE.ERROR

    #---------------------------------------------------------------------
    class WAVEFORM_FORMAT(Enum):
        WORD    = 'WORD'
        BYTE    = 'BYTE'
        ASCII   = 'ASC'
        ERROR   = 'ERROR'

    #--------------------------------------------
    def __SetWaveformFormat( self, connIdx: int, format: WAVEFORM_FORMAT=WAVEFORM_FORMAT.BYTE ) -> bool:
        return self.__device.SendCommand( "WAV:FORM " + format.value, connIdx=connIdx ) == connIdx

    def SetWaveformFormat( self, format: WAVEFORM_FORMAT=WAVEFORM_FORMAT.BYTE ) -> bool:
        return self.__SetWaveformFormat( 0, format=format )
        
    #--------------------------------------------
    def GetWaveformFormat( self ) -> WAVEFORM_FORMAT:
        ans = self.__device.SendCommandGetAns( "WAV:FORM?" )
        if( len( ans ) == 0 ):  return self.WAVEFORM_FORMAT.ERROR

        try:
            return self.WAVEFORM_FORMAT( ans )
        except ValueError:
            return self.WAVEFORM_FORMAT.ERROR

    #---------------------------------------------------------------------
    def GetWaveformXincrement( self ) -> float:
        ans = self.__device.SendCommandGetAns( "WAV:XINC?" )
        if( len( ans ) == 0 ):  return float( 'nan' )
        return float( ans )   

    #---------------------------------------------------------------------
    def GetWaveformXorigin( self ) -> float:
        ans = self.__device.SendCommandGetAns( "WAV:XOR?" )
        if( len( ans ) == 0 ):  return float( 'nan' )
        return float( ans )

    #---------------------------------------------------------------------
    def GetWaveformXreference( self ) -> float:
        ans = self.__device.SendCommandGetAns( "WAV:XREF?" )
        if( len( ans ) == 0 ):  return float( 'nan' )
        return float( ans )

    #---------------------------------------------------------------------
    def GetWaveformYincrement( self ) -> float:
        ans = self.__device.SendCommandGetAns( "WAV:YINC?" )
        if( len( ans ) == 0 ):  return float( 'nan' )
        return float( ans )

    #---------------------------------------------------------------------
    def GetWaveformYorigin( self ) -> float:
        ans = self.__device.SendCommandGetAns( "WAV:YOR?" )
        if( len( ans ) == 0 ):  return float( 'nan' )
        return float( ans )

    #---------------------------------------------------------------------
    def GetWaveformYreference( self ) -> float:
        ans = self.__device.SendCommandGetAns( "WAV:YREF?" )
        if( len( ans ) == 0 ):  return float( 'nan' )
        return float( ans )

    #---------------------------------------------------------------------
    def __SetWaveformStart( self, connIdx: int, start: int ) -> bool:
        return self.__device.SendCommand( "WAV:STAR " + str(start), connIdx=connIdx ) == connIdx

    def SetWaveformStart( self, start: int ) -> bool:
        return self.__SetWaveformStart( 0, start=start )

    #--------------------------------------------
    def GetWaveformStart( self ) -> int:
        ans = self.__device.SendCommandGetAns( "WAV:STAR?" )
        if( len( ans ) == 0 ):  return -2147483648       #int32 min
        return int( ans )

    #---------------------------------------------------------------------
    def __SetWaveformStop( self, connIdx: int, start: int ) -> bool:
        return self.__device.SendCommand( "WAV:STOP " + str(start), connIdx=connIdx ) == connIdx

    def SetWaveformStop( self, start: int ) -> bool:
        return self.__SetWaveformStop( 0, start )

    #--------------------------------------------
    def GetWaveformStop( self ) -> int:
        ans = self.__device.SendCommandGetAns( "WAV:STOP?" )
        if( len( ans ) == 0 ):  return -2147483648       #int32 min
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
    def __GetWaveformPreamble( self, connIdx: int ) -> list:
        ans = self.__device.SendCommandGetAns( "WAV:PRE?", connIdx=connIdx )
        if( len(ans) == 0 ):  return []
        return ans.split( ',' )

    def GetWaveformPreamble( self ) -> list:
        return self.__GetWaveformPreamble( 0 )

    #---------------------------------------------------------------------
    def GetWaveformDataRaw( self, source: WAVEFORM_SOURCE=WAVEFORM_SOURCE.CH1 ) -> list:
        connIdx = self.__device.Connect()
        if( connIdx == -1 ): return []
        if( self.__Stop( connIdx ) == False ): return []                                            #data can be rady only when scope is stoped
        if( self.__SetWaveformSource( connIdx, source )  == False ): return []                      #specify sourece of data
        if( self.__SetWaveformMode( connIdx, self.WAVEFORM_MODE.RAW ) == False ): return []         #raw data type
        if( self.__SetWaveformFormat( connIdx, self.WAVEFORM_FORMAT.ASCII ) == False ): return []   #data converted to ascii - no calculation needed

        #download information about waveform data
        preamble = self.__GetWaveformPreamble( connIdx )
        if( len(preamble) == 0 ): return []
        pointsCount = int( preamble[ self.WAVFORM_PREAMBLE_IDX.POINTS.value ] )

        currentStartIdx = 1
        points = b''
        while currentStartIdx <= pointsCount:
            #change range of data to read
            if( self.__SetWaveformStart( connIdx, currentStartIdx ) == False ): return []
            restOfPoints = pointsCount-currentStartIdx
            if restOfPoints > 100000:                                                               #max package is 131072 points of data, 100000 is round number
                if( self.__SetWaveformStop( connIdx ,currentStartIdx+99999 ) == False ): return []  #99999 couse with 1 is number of the last point
            else:
                if( self.__SetWaveformStop( connIdx, currentStartIdx + (pointsCount-currentStartIdx) ) == False ): return []

            #start read data
            if( self.__device.SendCommand( "WAV:DATA?", connIdx=connIdx ) != connIdx ): return []
            header = self.__device.GetAns( 2, connIdx=connIdx )                                     #get begin of header #x - where x is length of rest of header
            if( len(header) == 0 ): return []
            header = int( header[1] )                                                               #convert string to int
            length = self.__device.GetAns( header, connIdx=connIdx )
            if( len(length) == 0 ): return []
            length = int( length ) + 1                                                              #get rest of heder info - this is length of bytes to read from stream + ending \n 
        
            #get rest of stream data, loop reads data to end of stream in packet
            data = b''
            while len(data) < length:
                newData = self.__device.GetRaw( length, connIdx=connIdx )
                if( len(newData)==0 ):  return []
                data = data + newData

            points = points + data[:len(data)-1] + b','                                              #remove ending from data
            currentStartIdx = currentStartIdx + 100000
        self.__device.Close( connIdx )

        points = points[:len(points)-1]
        points = points.decode( "UTF-8" ).rstrip().split( ',' )
        for i in range( len( points ) ):
            points[i] = float( points[i] )

        return points

    #---------------------------------------------------------------------
    def GetWaveformDataScreen( self, source: WAVEFORM_SOURCE=WAVEFORM_SOURCE.CH1 ) -> list:
        connIdx = self.__device.Connect()
        if( connIdx == -1 ): return []
        if( self.__Stop( connIdx ) == False ): return []                                            #data can be rady only when scope is stoped
        if( self.__SetWaveformSource( connIdx, source )  == False ): return []                      #specify sourece of data
        if( self.__SetWaveformMode( connIdx, self.WAVEFORM_MODE.NORMAL ) == False ): return []      #normal data type
        if( self.__SetWaveformFormat( connIdx, self.WAVEFORM_FORMAT.ASCII ) == False ): return []   #data converted to ascii - no calculation needed

        if( self.__SetWaveformStart( connIdx, 1 ) == False ): return []
        if( self.__SetWaveformStop( connIdx, 1200 ) == False ): return []

        #start read data
        if( self.__device.SendCommand( "WAV:DATA?", connIdx=connIdx ) != connIdx ): return []
        header = self.__device.GetAns( 2, connIdx=connIdx )                                     #get begin of header #x - where x is length of rest of header
        if( len(header) == 0 ): return []
        header = int( header[1] )                                                               #convert string to int
        length = self.__device.GetAns( header, connIdx=connIdx )
        if( len(length) == 0 ): return []
        length = int( length ) + 1                                                              #get rest of heder info - this is length of bytes to read from stream + ending \n 

        #get stream data
        data = b''
        while len(data) < length:
            newData = self.__device.GetRaw( length, connIdx=connIdx )
            if( len(newData)==0 ):  return []
            data = data + newData
        self.__device.Close( connIdx )

        data = data[:len(data)-1]                                                                   #remove ending from data
        data = data.decode( "UTF-8" ).rstrip().split( ',' )
        for i in range( len( data ) ):
            data[i] = float( data[i] )

        return data
    

    