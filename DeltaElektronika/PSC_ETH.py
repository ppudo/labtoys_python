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

import scpi
from enum import Enum

class PSC_ETH:
    def __init__( self, aIP="10.1.0.101", aPort=8462 ):
        self.__device = scpi.SCPI_Socket( aIP, aPort )

    #--------------------------------------------
    def Connect( self, timeout=3 ):
        self.__device.Connect( timeout )

    #--------------------------------------------
    def Close( self ):
        self.__device.Close()

    #----------------------------------------------------------------------------------------------
    # General Instructions
    #----------------------------------------------------------------------------------------------

    def GetIDN( self ):
        ans = self.__device.SendCommandGetAns( "*IDN?" )
        idn = ans.split( ',' )
        return idn

    #--------------------------------------------
    def SetProtectedUserData( self, info: str ):
        if( len(info) > 72 ):
            info = info[:72]
        self.__device.SendCommand( "*PUD " + info )

    #--------------------------------------------
    def GetProtectedUserData( self ) -> str:
        ans = self.__device.SendCommandGetAns( "*PUD?" )
        return ans

    #--------------------------------------------
    def SaveSettings( self, password: str="" ):
        if( len(password) > 0 ):
            self.__device.SendCommand( "*SAV " + password )
        else:
            self.__device.SendCommand( "*SAV" )

    #--------------------------------------------
    def RestoreToDefaultState( self ):
        self.__device.SendCommand( "*RST" )

    #--------------------------------------------
    def RecallCalibration( self ):
        self.__device.SendCommand( "*RCL" )

    #----------------------------------------------------------------------------------------------
    # Source Subsystem
    #----------------------------------------------------------------------------------------------

    def SetOutputMaxVoltage( self, max: float ):
        self.__device.SendCommand( "SOUR:VOLT:MAX " + "{:.4f}".format( max ) )                      #SOURce:VOLTage:MAXimum

    #--------------------------------------------
    def GetOutputMaxVoltage( self ) -> float:
        ans = self.__device.SendCommandGetAns( "SOUR:VOLT:MAX?" )                                   #SOURce:VOLTage:MAXimum               
        return float( ans )
    
    #--------------------------------------------
    def SetOutputMaxCurrent( self, max: float ):
        self.__device.SendCommand( "SOUR:CURR:MAX " + "{:.4f}".format( max ) )                      #SOURce:CURRent:MAXimum

    #--------------------------------------------
    def GetOutputMaxCurrent( self ) -> float:
        ans = self.__device.SendCommandGetAns( "SOUR:CURR:MAX?" )                                   #SOURce:CURRent:MAXimum               
        return float( ans )

    #--------------------------------------------
    def SetOutputVoltage( self, voltage: float ):
        self.__device.SendCommand( "SOUR:VOLT " + "{:.4f}".format( voltage ) )                      #SOURce:VOLTage

    #--------------------------------------------
    def GetOutputVoltage( self ) -> float:
        ans = self.__device.SendCommandGetAns( "SOUR:VOLT?" )                                       #SOURce:VOLTage              
        return float( ans )

    #--------------------------------------------
    def SetOutputCurrent( self, current: float ):
        self.__device.SendCommand( "SOUR:CURRent " + "{:.4f}".format( current ) )                   #SOURce:CURRent

    #--------------------------------------------
    def GetOutputCurrent( self ) -> float:
        ans = self.__device.SendCommandGetAns( "SOUR:CURR?" )                                       #SOURce:CURRent           
        return float( ans )

    #----------------------------------------------------------------------------------------------
    # Measure Subsystem
    #----------------------------------------------------------------------------------------------

    def MeasureOutputVoltage( self ) -> float:
        ans = self.__device.SendCommandGetAns( "MEAS:VOLT?" )                                       #MEASure:VOLTage
        return float( ans )

    #--------------------------------------------
    def MeasureOutputCurrent( self ) -> float:
        ans = self.__device.SendCommandGetAns( "MEAS:CURR?" )                                       #MEASure:CURRent    
        return float( ans )

    #--------------------------------------------
    #commented as it's only avaibale in firmware version 3.4.0 - other on tested device
    #def MeasureOutputPower( self ) -> float:
    #    ans = self.__device.SendCommandGetAns( "MEAS:POW?" )                                       #MEASure:POWer
    #    return float( ans )

    #----------------------------------------------------------------------------------------------
    # Digital User In-/Outputs
    #----------------------------------------------------------------------------------------------

    def SetDigitalOutputs( self, outputs: int ):
        self.__device.SendCommand( "UOUT " + outputs )                                              #UOUTput

    #--------------------------------------------
    def GetDigitalOutputs( self ) -> int:
        ans = self.__device.SendCommandGetAns( "UOUT?" )                                            #UOUTput
        return int( ans )

    #--------------------------------------------
    def GetDigitalInputs( self ) -> int:
        ans = self.__device.SendCommandGetAns( "UINP:COND?" )                                       #UINPut:CONDition
        return int( ans )

    #----------------------------------------------------------------------------------------------
    # System Subsystem
    #----------------------------------------------------------------------------------------------

    def LockFrontPanel( self ):
        self.__device.SendCommand( "SYST:FRON 1" )                                                  #SYSTem:FRONtpanel[:STATus] 1 or ON

    def UnlockFrontPanel( self ):
        self.__device.SendCommand( "SYST:FRON 0" )                                                  #SYSTem:FRONtpanel[:STATus] 0 or OFF

    def GetFronPanelLockStatus( self ):
        ans = self.__device.SendCommandGetAns( "SYST:FRON?" )                                       #SYSTem:FRONtpanel[:STATus]?
        ans = int( ans )
        if( ans == 0 ):
            return False
        return True

    #---------------------------------------------------------------------
    class REMOTE_STATUS(Enum):
        REMOTE    = 'REM'
        LOCAL     = 'LOC'

    #--------------------------------------------
    def EnableRemoteMode( self ):
        self.__device.SendCommand( "SYST:REM " + self.REMOTE_STATUS.REMOTE.value )                  #SYSTem:REMote[:STATus] REMote

    #--------------------------------------------
    def DisableRemoteMode( self ):
        self.__device.SendCommand( "SYST:REM " + self.REMOTE_STATUS.LOCAL.value )                   #SYSTem:REMote[:STATus] LOCal

    #--------------------------------------------
    def GetRemoteModeStatus( self ):
        ans = self.__device.SendCommandGetAns( "SYST:REM?" )                                        #SYSTem:REMote[:STATus]?
        try:
            return self.REMOTE_STATUS( ans )
        except ValueError:
            return None

    #--------------------------------------------
    def EnableRemoteVoltage( self ):
        self.__device.SendCommand( "SYST:REM:CV " + self.REMOTE_STATUS.REMOTE.value )               #SYSTem:REMote:CV[:STATus] REMote

    #--------------------------------------------
    def DisableRemoteVoltage( self ):
        self.__device.SendCommand( "SYST:REM:CV " + self.REMOTE_STATUS.LOCAL.value )                #SYSTem:REMote:CV[:STATus] LOCal

    #--------------------------------------------
    def GetRemoteVoltageStatus( self ):
        ans = self.__device.SendCommandGetAns( "SYST:REM:CV?" )                                     #SYSTem:REMote:CV[:STATus]?
        try:
            return self.REMOTE_STATUS( ans )
        except ValueError:
            return None

    #--------------------------------------------
    def EnableRemoteCurrent( self ):
        self.__device.SendCommand( "SYST:REM:CC " + self.REMOTE_STATUS.REMOTE.value )               #SYSTem:REMote:CC[:STATus] REMote

    #--------------------------------------------
    def DisableRemoteCurrent( self ):
        self.__device.SendCommand( "SYST:REM:CC " + self.REMOTE_STATUS.LOCAL.value )                #SYSTem:REMote:CC[:STATus] LOCal

    #--------------------------------------------
    def GetRemoteCurrentStatus( self ):
        ans = self.__device.SendCommandGetAns( "SYST:REM:CC?" )                                     #SYSTem:REMote:CC[:STATus]?
        try:
            return self.REMOTE_STATUS( ans )
        except ValueError:
            return None

    #--------------------------------------------
    def GetSystemError( self ):
        ans = self.__device.SendCommandGetAns( "SYST:ERR?" )                                        #SYSTem:ERRor?
        pos = ans.find( ',' )
        errorCode = int( ans[:pos] )
        errorMsg = ans[pos+1:]
        return [errorCode, errorMsg]

    #--------------------------------------------
    def SetPassword( self, oldPassword="DEFAULT", newPassword="DEFAULT" ):
        if( (len(oldPassword) > 7 ) or (len(newPassword) > 7) ):
            return
        self.__device.SendCommand( "SYST:PASS " + oldPassword + "," + newPassword )                 #SYSTem:PASSword

    #--------------------------------------------
    def GetPasswordStatus( self ) -> bool:
        ans = self.__device.SendCommandGetAns( "SYST:PASS:STAT?" )                                  #SYSTem:PASSword:STATus?
        ans = int( ans )
        if( ans == 0 ):
            return False
        return True

    #----------------------------------------------------------------------------------------------
    # Output
    #----------------------------------------------------------------------------------------------

    def EnableOutput( self ):
        self.__device.SendCommand( "OUTP 1" )                                                       #OUTPut

    #--------------------------------------------
    def DisableOutput( self ):
        self.__device.SendCommand( "OUTP 0" )                                                       #OUTPut

    #--------------------------------------------
    def GetOutputStatus( self ):
        ans = self.__device.SendCommandGetAns( "OUTP?" )                                            #OUTPut
        ans = int( ans )
        if( ans == 0 ):
            return False
        return True

    #----------------------------------------------------------------------------------------------
    # Sequencer
    #----------------------------------------------------------------------------------------------

    def GetSequenceCatalog( self ):
        ans = self.__device.SendCommandGetAns( "PROG:CAT?" )                                        #PROGram:CATalog
        return ans.split( '\n' )

    #--------------------------------------------
    def SelectSequence( self, name: str ):
        if( len(name) > 16 ):
            name = name[:16]
        self.__device.SendCommand( "PROG:SEL:NAME " + name )                                        #PROGram:SELected:NAME

    #--------------------------------------------
    def GetSelectedSequenceName( self ) -> str:
        ans = self.__device.SendCommandGetAns( "PROG:SEL:NAME?" )                                   #PROGram:SELected:NAME
        return str( ans )

    #--------------------------------------------
    def SetSequenceStep( self, stepNo: int, command: str ):
        if( (stepNo <= 2000) and (stepNo >= 1) ):
            self.__device.SendCommand( "PROG:SEL:STEP " + str(stepNo) + " " + command )             #PROGram:SELected:STEP

    #--------------------------------------------
    def GetSequenceStep( self, stepNo: int ) -> str:
        if( (stepNo <= 2000) and (stepNo >= 1) ):
            ans = self.__device.SendCommandGetAns( "PROG:SEL:STEP " + str(stepNo) + "?" )           #PROGram:SELected:STEP
            if( ans == None ):
                return None
            pos = ans.find( ' ' )
            ans = ans[(pos+1):]
            return ans
        return None
        
    #--------------------------------------------
    def GetCompleteSequence( self ):
        #idea below do not work, return only first step - delta send only first step
        #ans = self.__device.SendCommandGetAns( "PROG:SEL:STEP ?" )                                 #PROGram:SELected:STEP
        #print( ans )
        #steps = ans.split( '\n' )
        #for i in range( len(steps) ):
        #    pos = steps[i].find( ' ' )
        #    steps[i] = steps[i][(pos+1):]
        #return steps
        idx = 1
        step = ""
        steps = []
        while( step != "END" ):
            step = self.GetSequenceStep( idx )
            if( step == None ):
                return steps
            steps.append( step )
            idx = idx + 1
        return steps

    #--------------------------------------------
    def DeleteSelectedSequence( self ):
        self.__device.SendCommand( "PROG:SEL:DEL" )                                                 #PROGram:SELected:DELete

    #--------------------------------------------
    #def DeleteAllSequences( self ):
    #    self._device.SendCommand( "PROG:CAT:DEL" )                                                  #PROGram:CATalog:DELete

    #--------------------------------------------
    def StartSequence( self ):
        self.__device.SendCommand( "PROG:SEL:STAT RUN" )                                            #PROGram:SELected:STATe RUN

    #--------------------------------------------
    def PauseSequence( self ):
        self.__device.SendCommand( "PROG:SEL:STAT PAUS" )                                           #PROGram:SELected:STATe PAUSe

    #--------------------------------------------
    def ContinueSequence( self ):
        self.__device.SendCommand( "PROG:SEL:STAT CONT" )                                           #PROGram:SELected:STATe CONTinue

    #--------------------------------------------
    def NextStep( self ):
        self.__device.SendCommand( "PROG:SEL:STAT NEXT" )                                           #PROGram:SELected:STATe NEXT

    #--------------------------------------------
    def StopSequence( self ):
        self.__device.SendCommand( "PROG:SEL:STAT STOP" )                                           #PROGram:SELected:STATe STOP

    #---------------------------------------------------------------------
    class SEQUENCE_STATE(Enum):
        STOP    = 'STOP'
        PAUSE   = 'PAUSE'
        RUN     = 'RUN'

    #--------------------------------------------
    def GetSequenceState( self ):
        ans = self.__device.SendCommandGetAns( "PROG:SEL:STAT?" )                                   #PROGram:SELected:STATe
        if( ans.find(self.SEQUENCE_STATE.STOP.value) != -1 ):
            return [ self.SEQUENCE_STATE.STOP, None ]
        elif( ans.find(self.SEQUENCE_STATE.PAUSE.value) != -1 ):
            step = int( ans[ len(self.SEQUENCE_STATE.PAUSE.value)+1: ] )
            return [ self.SEQUENCE_STATE.PAUSE, step ]
        elif( ans.find(self.SEQUENCE_STATE.RUN.value) != -1 ):
            step = int( ans[ len(self.SEQUENCE_STATE.RUN.value)+1: ] )
            return [ self.SEQUENCE_STATE.RUN, step ]
        return [None, None]

    #--------------------------------------------
    def TriggerStep( self ):
        self.__device.SendCommand( "TRIG:IMM" )                                                     #TRIGger:IMMediate
        


    
        