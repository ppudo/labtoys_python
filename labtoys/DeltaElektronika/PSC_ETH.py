#PSC_ETH.py
#   Created on:	2020.11.10
#       Author: ppudo
#       e-mail:	ppudo@outlook.com
#
#   Project: 	labtoys
#   Description: 	Class representing Delta Elektronika PSC-ETH interface adapter for power supply
#
#
#   Changelog:
#      	-2020.11.10		version: 0.1.0
#      		- Initial class
#       -2021.09.29     version: 0.2.0
#           - Adapt to new scpi librar
#       -2021.10.30     version: 0.2.1
#           - Add functions to upload sequence to delta
#       -2021.10.30     version: 0.2.2
#           - Modify functions to set remote status
#
#----------------------------------------------------------------------------------------------------------------------------------------------------
#       Idea and changes proposal:
#           
#       
#       Usefull information and links:
#           Product page:       https://www.delta-elektronika.nl/en/products/interfaces/ethernet-interface.html     (2020.11.10)
#           Programing manual:  https://www.delta-elektronika.nl/upload/MANUAL_ETHERNET_CARD_AND_MODULE.pdf     (2020.11.10)
#           Testing device:     http://www.delta-elektronika.nl/en/products/dc-power-supplies-800w-sm800-series.html    (2020.11.10) - manual taken from attached software
#

from ..scpi import SCPI_Socket
from enum import Enum

class PSC_ETH:
    def __init__( self, aIP="10.1.0.101", aPort=8462 ):
        self.__device = SCPI_Socket( aIP, aPort )
        self.__device.timeout = 3
        self.__device.sendDalay = 0.005

    #----------------------------------------------------------------------------------------------
    # General Instructions
    #----------------------------------------------------------------------------------------------

    def GetIDN( self ) -> list:
        ans = self.__device.SendCommandGetAns( "*IDN?" )
        if( len(ans) == 0 ): return []
        return ans.split( ',' )

    #--------------------------------------------
    def SetProtectedUserData( self, info: str ) -> bool:
        if( len(info) > 72 ):
            info = info[:72]
        return self.__device.SendCommand( "*PUD " + info ) == 0

    #--------------------------------------------
    def GetProtectedUserData( self ) -> str:
        ans = self.__device.SendCommandGetAns( "*PUD?" )
        if( len(ans) == 0 ):  return ""
        return ans

    #--------------------------------------------
    def SaveSettings( self, password: str="" ) -> bool:
        if( len(password) > 0 ):
            return self.__device.SendCommand( "*SAV " + password ) == 0
        else:
            return self.__device.SendCommand( "*SAV" ) == 0

    #--------------------------------------------
    def RestoreToDefaultState( self ) -> bool:
        return self.__device.SendCommand( "*RST" ) == 0

    #--------------------------------------------
    def RecallCalibration( self ) -> bool:
        return self.__device.SendCommand( "*RCL" ) == 0

    #----------------------------------------------------------------------------------------------
    # Source Subsystem
    #----------------------------------------------------------------------------------------------

    def SetOutputMaxVoltage( self, max: float ) -> bool:
        return self.__device.SendCommand( "SOUR:VOLT:MAX " + "{:.4f}".format( max ) ) == 0          #SOURce:VOLTage:MAXimum

    #--------------------------------------------
    def GetOutputMaxVoltage( self ) -> float:
        ans = self.__device.SendCommandGetAns( "SOUR:VOLT:MAX?" )                                   #SOURce:VOLTage:MAXimum
        if( len(ans) == 0 ): return float( 'nan' )              
        return float( ans )
    
    #--------------------------------------------
    def SetOutputMaxCurrent( self, max: float ) -> bool:
        return self.__device.SendCommand( "SOUR:CURR:MAX " + "{:.4f}".format( max ) ) == 0          #SOURce:CURRent:MAXimum

    #--------------------------------------------
    def GetOutputMaxCurrent( self ) -> float:
        ans = self.__device.SendCommandGetAns( "SOUR:CURR:MAX?" )                                   #SOURce:CURRent:MAXimum
        if( len( ans ) == 0 ): return float( 'nan' )              
        return float( ans )

    #--------------------------------------------
    def SetOutputVoltage( self, voltage: float ) -> bool:
        return self.__device.SendCommand( "SOUR:VOLT " + "{:.4f}".format( voltage ) ) == 0          #SOURce:VOLTage

    #--------------------------------------------
    def GetOutputVoltage( self ) -> float:
        ans = self.__device.SendCommandGetAns( "SOUR:VOLT?" )                                       #SOURce:VOLTage
        if( len( ans ) == 0 ): return float( 'nan' )           
        return float( ans )

    #--------------------------------------------
    def SetOutputCurrent( self, current: float ) -> bool:
        return self.__device.SendCommand( "SOUR:CURRent " + "{:.4f}".format( current ) ) == 0       #SOURce:CURRent

    #--------------------------------------------
    def GetOutputCurrent( self ) -> float:
        ans = self.__device.SendCommandGetAns( "SOUR:CURR?" )                                       #SOURce:CURRent
        if( len( ans ) == 0 ):  return float( 'nan' )      
        return float( ans )

    #----------------------------------------------------------------------------------------------
    # Measure Subsystem
    #----------------------------------------------------------------------------------------------

    def MeasureOutputVoltage( self ) -> float:
        ans = self.__device.SendCommandGetAns( "MEAS:VOLT?" )                                       #MEASure:VOLTage
        if( len( ans ) == 0 ): return float( 'nan' )
        return float( ans )

    #--------------------------------------------
    def MeasureOutputCurrent( self ) -> float:
        ans = self.__device.SendCommandGetAns( "MEAS:CURR?" )                                       #MEASure:CURRent
        if( len( ans ) == 0 ): return float( 'nan' )
        return float( ans )

    #--------------------------------------------
    #commented as it's only avaibale in firmware version 3.4.0 - other on tested device
    #def MeasureOutputPower( self ) -> float:
    #    ans = self.__device.SendCommandGetAns( "MEAS:POW?" )                                       #MEASure:POWer
    #    if( len( ans ) ): return float( 'nan' )
    #    return float( ans )

    #----------------------------------------------------------------------------------------------
    # Digital User In-/Outputs
    #----------------------------------------------------------------------------------------------

    def SetDigitalOutputs( self, outputs: int ) -> bool:
        outputs = outputs & 0x3F
        return self.__device.SendCommand( "UOUT " + outputs ) == 0                                  #UOUTput

    #--------------------------------------------
    def GetDigitalOutputs( self ) -> int:
        ans = self.__device.SendCommandGetAns( "UOUT?" )                                            #UOUTput
        if( len( ans ) == 0 ):  return -2147483648       #int32 min
        return int( ans )

    #--------------------------------------------
    def GetDigitalInputs( self ) -> int:
        ans = self.__device.SendCommandGetAns( "UINP:COND?" )                                       #UINPut:CONDition
        if( len( ans ) == 0 ):  return -2147483648       #int32 min
        return int( ans )

    #----------------------------------------------------------------------------------------------
    # System Subsystem
    #----------------------------------------------------------------------------------------------

    def LockFrontPanel( self ) -> bool:
        return self.__device.SendCommand( "SYST:FRON 1" ) == 0                                      #SYSTem:FRONtpanel[:STATus] 1 or ON

    def UnlockFrontPanel( self ) -> bool:
        return self.__device.SendCommand( "SYST:FRON 0" ) == 0                                      #SYSTem:FRONtpanel[:STATus] 0 or OFF

    def GetFronPanelLockStatus( self ) -> bool:
        ans = self.__device.SendCommandGetAns( "SYST:FRON?" )                                       #SYSTem:FRONtpanel[:STATus]?
        if( len( ans ) == 0 ): return False
        ans = int( ans )
        if( ans == 0 ):
            return False
        return True

    #---------------------------------------------------------------------
    class REMOTE_STATUS(Enum):
        REMOTE    = 'REM'
        LOCAL     = 'LOC'
        ERROR     = 'ERROR'         #do not use, only for indication of results

    #--------------------------------------------
    def SetRemoteMode( self, mode: REMOTE_STATUS ) -> bool:
        if( mode == self.REMOTE_STATUS.REMOTE ):
            return self.__device.SendCommand( "SYST:REM " + self.REMOTE_STATUS.REMOTE.value ) == 0  #SYSTem:REMote[:STATus] REMote
        else:
            return self.__device.SendCommand( "SYST:REM " + self.REMOTE_STATUS.LOCAL.value ) == 0   #SYSTem:REMote[:STATus] LOCal        

    #--------------------------------------------
    def GetRemoteModeStatus( self ) -> REMOTE_STATUS:
        ans = self.__device.SendCommandGetAns( "SYST:REM?" )                                        #SYSTem:REMote[:STATus]?
        if( len( ans ) == 0 ): return self.REMOTE_STATUS.ERROR
        try:
            return self.REMOTE_STATUS( ans )
        except ValueError:
            return None

    #--------------------------------------------
    def SetRemoteVoltage( self, mode: REMOTE_STATUS ) -> bool:
        if( mode == self.REMOTE_STATUS.REMOTE ):
            return self.__device.SendCommand( "SYST:REM:CV " + self.REMOTE_STATUS.REMOTE.value ) == 0   #SYSTem:REMote:CV[:STATus] REMote
        else:
            return self.__device.SendCommand( "SYST:REM:CV " + self.REMOTE_STATUS.LOCAL.value ) == 0    #SYSTem:REMote:CV[:STATus] LOCal

    #--------------------------------------------
    def GetRemoteVoltageStatus( self ) -> REMOTE_STATUS:
        ans = self.__device.SendCommandGetAns( "SYST:REM:CV?" )                                     #SYSTem:REMote:CV[:STATus]?
        if( len( ans ) == 0 ): return self.REMOTE_STATUS.ERROR
        try:
            return self.REMOTE_STATUS( ans )
        except ValueError:
            return None

    #--------------------------------------------
    def SetRemoteCurrent( self, mode: REMOTE_STATUS ) -> bool:
        if( mode == self.REMOTE_STATUS.REMOTE ):
            return self.__device.SendCommand( "SYST:REM:CC " + self.REMOTE_STATUS.REMOTE.value ) == 0   #SYSTem:REMote:CC[:STATus] REMote
        else:
            return self.__device.SendCommand( "SYST:REM:CC " + self.REMOTE_STATUS.LOCAL.value ) == 0    #SYSTem:REMote:CC[:STATus] LOCal

    #--------------------------------------------
    def GetRemoteCurrentStatus( self ) -> REMOTE_STATUS:
        ans = self.__device.SendCommandGetAns( "SYST:REM:CC?" )                                     #SYSTem:REMote:CC[:STATus]?
        if( len( ans ) == 0 ): return self.REMOTE_STATUS.ERROR
        try:
            return self.REMOTE_STATUS( ans )
        except ValueError:
            return None

    #--------------------------------------------
    def GetSystemError( self ) -> list:
        ans = self.__device.SendCommandGetAns( "SYST:ERR?" )                                        #SYSTem:ERRor?
        if( len( ans ) == 0 ):  return []
        pos = ans.find( ',' )
        errorCode = int( ans[:pos] )
        errorMsg = ans[pos+1:]
        return [errorCode, errorMsg]

    #--------------------------------------------
    def SetPassword( self, oldPassword="DEFAULT", newPassword="DEFAULT" ) -> bool:
        if( (len(oldPassword) > 7 ) or (len(newPassword) > 7) ):
            return False
        return self.__device.SendCommand( "SYST:PASS " + oldPassword + "," + newPassword ) == 0     #SYSTem:PASSword

    #--------------------------------------------
    def GetPasswordStatus( self ) -> bool:
        ans = self.__device.SendCommandGetAns( "SYST:PASS:STAT?" )                                  #SYSTem:PASSword:STATus?
        if( len( ans ) == 0 ): return False
        ans = int( ans )
        if( ans == 0 ):
            return False
        return True

    #----------------------------------------------------------------------------------------------
    # Output
    #----------------------------------------------------------------------------------------------

    def EnableOutput( self ) -> bool:
        return self.__device.SendCommand( "OUTP 1" ) == 0                                           #OUTPut

    #--------------------------------------------
    def DisableOutput( self ) -> bool:
        return self.__device.SendCommand( "OUTP 0" ) == 0                                           #OUTPut

    #--------------------------------------------
    def GetOutputStatus( self ) -> bool:
        ans = self.__device.SendCommandGetAns( "OUTP?" )                                            #OUTPut
        if( len( ans ) == 0 ): return False
        ans = int( ans )
        if( ans == 0 ):
            return False
        return True

    #----------------------------------------------------------------------------------------------
    # Sequencer
    #----------------------------------------------------------------------------------------------

    def GetSequenceCatalog( self ) -> list:
        ans = self.__device.SendCommandGetAns( "PROG:CAT?" )                                        #PROGram:CATalog
        if( len( ans ) == 0 ): return []
        return ans.split( '\n' )

    #--------------------------------------------
    def __SelectSequence( self, name: str, connIdx: int ) -> bool:
        if( len(name) > 16 ):
            name = name[:16]
        return self.__device.SendCommand( "PROG:SEL:NAME " + name, connIdx=connIdx ) == connIdx     #PROGram:SELected:NAME

    def SelectSequence( self, name: str ) -> bool:
        return self.__SelectSequence( name, 0 )

    #--------------------------------------------
    def GetSelectedSequenceName( self ) -> str:
        ans = self.__device.SendCommandGetAns( "PROG:SEL:NAME?" )                                   #PROGram:SELected:NAME
        if( len( ans ) == 0 ): return ""
        return str( ans )

    #--------------------------------------------
    def __SetSequenceStep( self, stepNo: int, command: str, connIdx: str ) -> bool:
        if( (stepNo <= 2000) and (stepNo >= 1) ):
            return self.__device.SendCommand( "PROG:SEL:STEP " + str(stepNo) + " " + command ) == connIdx   #PROGram:SELected:STEP
        else:
            return False

    def SetSequenceStep( self, stepNo: int, command: str ) -> bool:
        return self.__SetSequenceStep( stepNo, command, 0)

    #--------------------------------------------
    def __GetSequenceStep( self, stepNo: int, connIdx: int ) -> str:
        if( (stepNo <= 2000) and (stepNo >= 1) ):
            ans = self.__device.SendCommandGetAns( "PROG:SEL:STEP " + str(stepNo) + "?", connIdx=connIdx )  #PROGram:SELected:STEP
            if( len( ans ) == 0 ): return ""
            pos = ans.find( ' ' )
            ans = ans[(pos+1):]
            return ans
        return ""

    def GetSequenceStep( self, stepNo: int ) -> str:
        return self.__GetSequenceStep( self, stepNo, 0 )
        
    #--------------------------------------------
    def GetCompleteSequence( self ) -> list:
        #ans = self.__device.SendCommandGetAns( "PROG:SEL:STEP ?" )                                 #PROGram:SELected:STEP          <- this is not working, return only first step
        idx = 1
        step = ""
        steps = []
        connIdx = self.__device.Connect()
        if( connIdx == -1 ): return []
        while( step != "END" ):
            step = self.__GetSequenceStep( idx, connIdx )
            if( len( step ) == 0 ):
                break
            steps.append( step )
            idx = idx + 1
        self.__device.Close( connIdx )
        return steps

    #--------------------------------------------
    def __DeleteSelectedSequence( self, connIdx: int ) -> bool:
        return self.__device.SendCommand( "PROG:SEL:DEL", connIdx=connIdx ) == connIdx              #PROGram:SELected:DELete

    def DeleteSelectedSequence( self ) -> bool:
        return self.__DeleteSelectedSequence( 0 )

    #--------------------------------------------
    #def DeleteAllSequences( self ) -> bool:
    #    return self._device.SendCommand( "PROG:CAT:DEL" )                                          #PROGram:CATalog:DELete

    #--------------------------------------------
    def StartSequence( self ) -> bool:
        return self.__device.SendCommand( "PROG:SEL:STAT RUN" ) == 0                                #PROGram:SELected:STATe RUN

    #--------------------------------------------
    def PauseSequence( self ) -> bool:
        return self.__device.SendCommand( "PROG:SEL:STAT PAUS" ) == 0                               #PROGram:SELected:STATe PAUSe

    #--------------------------------------------
    def ContinueSequence( self ) -> bool:
        return self.__device.SendCommand( "PROG:SEL:STAT CONT" ) == 0                               #PROGram:SELected:STATe CONTinue

    #--------------------------------------------
    def NextStep( self ) -> bool:
        return self.__device.SendCommand( "PROG:SEL:STAT NEXT" ) == 0                               #PROGram:SELected:STATe NEXT

    #--------------------------------------------
    def StopSequence( self ) -> bool:
        return self.__device.SendCommand( "PROG:SEL:STAT STOP" ) == 0                               #PROGram:SELected:STATe STOP

    #---------------------------------------------------------------------
    class SEQUENCE_STATE(Enum):
        STOP    = 'STOP'
        PAUSE   = 'PAUSE'
        RUN     = 'RUN'
        ERROR   = 'ERROR'

    #--------------------------------------------
    def GetSequenceState( self ) -> list:
        ans = self.__device.SendCommandGetAns( "PROG:SEL:STAT?" )                                   #PROGram:SELected:STATe
        if( len( ans ) ):  return [self.SEQUENCE_STATE.ERROR, -1]
        if( ans.find(self.SEQUENCE_STATE.STOP.value) != -1 ):
            return [ self.SEQUENCE_STATE.STOP, 0 ]
        elif( ans.find(self.SEQUENCE_STATE.PAUSE.value) != -1 ):
            step = int( ans[ len(self.SEQUENCE_STATE.PAUSE.value)+1: ] )
            return [ self.SEQUENCE_STATE.PAUSE, step ]
        elif( ans.find(self.SEQUENCE_STATE.RUN.value) != -1 ):
            step = int( ans[ len(self.SEQUENCE_STATE.RUN.value)+1: ] )
            return [ self.SEQUENCE_STATE.RUN, step ]
        return [self.SEQUENCE_STATE.ERROR, -1]

    #--------------------------------------------
    def TriggerStep( self ) -> bool:
        return self.__device.SendCommand( "TRIG:IMM" ) == 0                                         #TRIGger:IMMediate
        
    #--------------------------------------------
    def SendSequence( self, name : str, steps : list ) -> bool:
        connIdx = self.__device.Connect()
        if( connIdx == -1 ): return False

        #delete current sequence with the same name
        if( self.__SelectSequence( name, connIdx ) == False ): return False
        if( self.__DeleteSelectedSequence( connIdx ) == False ): return False

        #select sequence again and upload new sequence
        if( self.__SelectSequence( name, connIdx ) == False ): return False
        for i in range( len(steps) ):
            if( self.__SetSequenceStep(i+1, steps[i], connIdx) == False ): return False

        self.__device.Close( connIdx )
        return True

        