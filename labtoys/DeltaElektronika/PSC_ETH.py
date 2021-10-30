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
        self.__device.sendDalay = 0.001

    #----------------------------------------------------------------------------------------------
    # General Instructions
    #----------------------------------------------------------------------------------------------

    def GetIDN( self ) -> list:
        ans = self.__device.SendCommandGetAns( "*IDN?" )
        if( ans == None ):  return None
        return ans.split( ',' )

    #--------------------------------------------
    def SetProtectedUserData( self, info: str ) -> bool:
        if( len(info) > 72 ):
            info = info[:72]
        return self.__device.SendCommand( "*PUD " + info )

    #--------------------------------------------
    def GetProtectedUserData( self ) -> str:
        ans = self.__device.SendCommandGetAns( "*PUD?" )
        if( ans == None ):  return None
        return ans

    #--------------------------------------------
    def SaveSettings( self, password: str="" ) -> bool:
        if( len(password) > 0 ):
            return self.__device.SendCommand( "*SAV " + password )
        else:
            return self.__device.SendCommand( "*SAV" )

    #--------------------------------------------
    def RestoreToDefaultState( self ) -> bool:
        return self.__device.SendCommand( "*RST" )

    #--------------------------------------------
    def RecallCalibration( self ) -> bool:
        return self.__device.SendCommand( "*RCL" )

    #----------------------------------------------------------------------------------------------
    # Source Subsystem
    #----------------------------------------------------------------------------------------------

    def SetOutputMaxVoltage( self, max: float ) -> bool:
        return self.__device.SendCommand( "SOUR:VOLT:MAX " + "{:.4f}".format( max ) )               #SOURce:VOLTage:MAXimum

    #--------------------------------------------
    def GetOutputMaxVoltage( self ) -> float:
        ans = self.__device.SendCommandGetAns( "SOUR:VOLT:MAX?" )                                   #SOURce:VOLTage:MAXimum
        if( ans == None ):  return None               
        return float( ans )
    
    #--------------------------------------------
    def SetOutputMaxCurrent( self, max: float ) -> bool:
        return self.__device.SendCommand( "SOUR:CURR:MAX " + "{:.4f}".format( max ) )               #SOURce:CURRent:MAXimum

    #--------------------------------------------
    def GetOutputMaxCurrent( self ) -> float:
        ans = self.__device.SendCommandGetAns( "SOUR:CURR:MAX?" )                                   #SOURce:CURRent:MAXimum
        if( ans == None ):  return None               
        return float( ans )

    #--------------------------------------------
    def SetOutputVoltage( self, voltage: float ) -> bool:
        return self.__device.SendCommand( "SOUR:VOLT " + "{:.4f}".format( voltage ) )               #SOURce:VOLTage

    #--------------------------------------------
    def GetOutputVoltage( self ) -> float:
        ans = self.__device.SendCommandGetAns( "SOUR:VOLT?" )                                       #SOURce:VOLTage
        if( ans == None ):  return None           
        return float( ans )

    #--------------------------------------------
    def SetOutputCurrent( self, current: float ) -> bool:
        return self.__device.SendCommand( "SOUR:CURRent " + "{:.4f}".format( current ) )            #SOURce:CURRent

    #--------------------------------------------
    def GetOutputCurrent( self ) -> float:
        ans = self.__device.SendCommandGetAns( "SOUR:CURR?" )                                       #SOURce:CURRent
        if( ans == None ):  return None      
        return float( ans )

    #----------------------------------------------------------------------------------------------
    # Measure Subsystem
    #----------------------------------------------------------------------------------------------

    def MeasureOutputVoltage( self ) -> float:
        ans = self.__device.SendCommandGetAns( "MEAS:VOLT?" )                                       #MEASure:VOLTage
        if( ans == None ):  return None
        return float( ans )

    #--------------------------------------------
    def MeasureOutputCurrent( self ) -> float:
        ans = self.__device.SendCommandGetAns( "MEAS:CURR?" )                                       #MEASure:CURRent
        if( ans == None ):  return None
        return float( ans )

    #--------------------------------------------
    #commented as it's only avaibale in firmware version 3.4.0 - other on tested device
    #def MeasureOutputPower( self ) -> float:
    #    ans = self.__device.SendCommandGetAns( "MEAS:POW?" )                                       #MEASure:POWer
    #    if( ans == None ):  return None
    #    return float( ans )

    #----------------------------------------------------------------------------------------------
    # Digital User In-/Outputs
    #----------------------------------------------------------------------------------------------

    def SetDigitalOutputs( self, outputs: int ) -> bool:
        outputs = outputs & 0x3F
        return self.__device.SendCommand( "UOUT " + outputs )                                       #UOUTput

    #--------------------------------------------
    def GetDigitalOutputs( self ) -> int:
        ans = self.__device.SendCommandGetAns( "UOUT?" )                                            #UOUTput
        if( ans == None ):  return None
        return int( ans )

    #--------------------------------------------
    def GetDigitalInputs( self ) -> int:
        ans = self.__device.SendCommandGetAns( "UINP:COND?" )                                       #UINPut:CONDition
        if( ans == None ):  return None
        return int( ans )

    #----------------------------------------------------------------------------------------------
    # System Subsystem
    #----------------------------------------------------------------------------------------------

    def LockFrontPanel( self ) -> bool:
        return self.__device.SendCommand( "SYST:FRON 1" )                                           #SYSTem:FRONtpanel[:STATus] 1 or ON

    def UnlockFrontPanel( self ) -> bool:
        return self.__device.SendCommand( "SYST:FRON 0" )                                           #SYSTem:FRONtpanel[:STATus] 0 or OFF

    def GetFronPanelLockStatus( self ) -> bool:
        ans = self.__device.SendCommandGetAns( "SYST:FRON?" )                                       #SYSTem:FRONtpanel[:STATus]?
        if( ans == None ):  return None
        ans = int( ans )
        if( ans == 0 ):
            return False
        return True

    #---------------------------------------------------------------------
    class REMOTE_STATUS(Enum):
        REMOTE    = 'REM'
        LOCAL     = 'LOC'

    #--------------------------------------------
    def SetRemoteMode( self, mode: REMOTE_STATUS ) -> bool:
        if( mode == self.REMOTE_STATUS.REMOTE ):
            return self.__device.SendCommand( "SYST:REM " + self.REMOTE_STATUS.REMOTE.value )       #SYSTem:REMote[:STATus] REMote
        else:
            return self.__device.SendCommand( "SYST:REM " + self.REMOTE_STATUS.LOCAL.value )        #SYSTem:REMote[:STATus] LOCal        

    #--------------------------------------------
    def GetRemoteModeStatus( self ) -> REMOTE_STATUS:
        ans = self.__device.SendCommandGetAns( "SYST:REM?" )                                        #SYSTem:REMote[:STATus]?
        if( ans == None ):  return None
        try:
            return self.REMOTE_STATUS( ans )
        except ValueError:
            return None

    #--------------------------------------------
    def SetRemoteVoltage( self, mode: REMOTE_STATUS ) -> bool:
        if( mode == self.REMOTE_STATUS.REMOTE ):
            return self.__device.SendCommand( "SYST:REM:CV " + self.REMOTE_STATUS.REMOTE.value )    #SYSTem:REMote:CV[:STATus] REMote
        else:
            return self.__device.SendCommand( "SYST:REM:CV " + self.REMOTE_STATUS.LOCAL.value )     #SYSTem:REMote:CV[:STATus] LOCal

    #--------------------------------------------
    def GetRemoteVoltageStatus( self ) -> REMOTE_STATUS:
        ans = self.__device.SendCommandGetAns( "SYST:REM:CV?" )                                     #SYSTem:REMote:CV[:STATus]?
        if( ans == None ):  return None
        try:
            return self.REMOTE_STATUS( ans )
        except ValueError:
            return None

    #--------------------------------------------
    def SetRemoteCurrent( self, mode: REMOTE_STATUS ) -> bool:
        if( mode == self.REMOTE_STATUS.REMOTE ):
            return self.__device.SendCommand( "SYST:REM:CC " + self.REMOTE_STATUS.REMOTE.value )    #SYSTem:REMote:CC[:STATus] REMote
        else:
            return self.__device.SendCommand( "SYST:REM:CC " + self.REMOTE_STATUS.LOCAL.value )     #SYSTem:REMote:CC[:STATus] LOCal

    #--------------------------------------------
    def GetRemoteCurrentStatus( self ) -> REMOTE_STATUS:
        ans = self.__device.SendCommandGetAns( "SYST:REM:CC?" )                                     #SYSTem:REMote:CC[:STATus]?
        if( ans == None ):  return None
        try:
            return self.REMOTE_STATUS( ans )
        except ValueError:
            return None

    #--------------------------------------------
    def GetSystemError( self ) -> list:
        ans = self.__device.SendCommandGetAns( "SYST:ERR?" )                                        #SYSTem:ERRor?
        if( ans == None ):  return None
        pos = ans.find( ',' )
        errorCode = int( ans[:pos] )
        errorMsg = ans[pos+1:]
        return [errorCode, errorMsg]

    #--------------------------------------------
    def SetPassword( self, oldPassword="DEFAULT", newPassword="DEFAULT" ) -> bool:
        if( (len(oldPassword) > 7 ) or (len(newPassword) > 7) ):
            return False
        return self.__device.SendCommand( "SYST:PASS " + oldPassword + "," + newPassword )          #SYSTem:PASSword

    #--------------------------------------------
    def GetPasswordStatus( self ) -> bool:
        ans = self.__device.SendCommandGetAns( "SYST:PASS:STAT?" )                                  #SYSTem:PASSword:STATus?
        if( ans == None ):  return None
        ans = int( ans )
        if( ans == 0 ):
            return False
        return True

    #----------------------------------------------------------------------------------------------
    # Output
    #----------------------------------------------------------------------------------------------

    def EnableOutput( self ) -> bool:
        return self.__device.SendCommand( "OUTP 1" )                                                #OUTPut

    #--------------------------------------------
    def DisableOutput( self ) -> bool:
        return self.__device.SendCommand( "OUTP 0" )                                                #OUTPut

    #--------------------------------------------
    def GetOutputStatus( self ) -> bool:
        ans = self.__device.SendCommandGetAns( "OUTP?" )                                            #OUTPut
        if( ans == None ):  return None
        ans = int( ans )
        if( ans == 0 ):
            return False
        return True

    #----------------------------------------------------------------------------------------------
    # Sequencer
    #----------------------------------------------------------------------------------------------

    def GetSequenceCatalog( self ) -> list:
        ans = self.__device.SendCommandGetAns( "PROG:CAT?" )                                        #PROGram:CATalog
        if( ans == None ):  return None
        return ans.split( '\n' )

    #--------------------------------------------
    def SelectSequence( self, name: str ) -> bool:
        if( len(name) > 16 ):
            name = name[:16]
        return self.__device.SendCommand( "PROG:SEL:NAME " + name )                                 #PROGram:SELected:NAME

    #--------------------------------------------
    def GetSelectedSequenceName( self ) -> str:
        ans = self.__device.SendCommandGetAns( "PROG:SEL:NAME?" )                                   #PROGram:SELected:NAME
        if( ans == None ):  return None
        return str( ans )

    #--------------------------------------------
    def SetSequenceStep( self, stepNo: int, command: str ) -> bool:
        if( (stepNo <= 2000) and (stepNo >= 1) ):
            return self.__device.SendCommand( "PROG:SEL:STEP " + str(stepNo) + " " + command )      #PROGram:SELected:STEP
        else:
            return False

    #--------------------------------------------
    def GetSequenceStep( self, stepNo: int ) -> str:
        if( (stepNo <= 2000) and (stepNo >= 1) ):
            ans = self.__device.SendCommandGetAns( "PROG:SEL:STEP " + str(stepNo) + "?" )           #PROGram:SELected:STEP
            if( ans == None ):  return None
            pos = ans.find( ' ' )
            ans = ans[(pos+1):]
            return ans
        return None
        
    #--------------------------------------------
    def GetCompleteSequence( self ) -> list:
        #ans = self.__device.SendCommandGetAns( "PROG:SEL:STEP ?" )                                 #PROGram:SELected:STEP          <- this is not working, return only first step
        idx = 1
        step = ""
        steps = []
        if( self.__device.Connect() == False ): return None
        while( step != "END" ):
            step = self.GetSequenceStep( idx )
            if( step == None ):
                if( len(steps) == 0 ):  
                    return None
                else:
                    return steps
            steps.append( step )
            idx = idx + 1
        self.__device.Close()
        return steps

    #--------------------------------------------
    def DeleteSelectedSequence( self ) -> bool:
        return self.__device.SendCommand( "PROG:SEL:DEL" )                                          #PROGram:SELected:DELete

    #--------------------------------------------
    #def DeleteAllSequences( self ) -> bool:
    #    return self._device.SendCommand( "PROG:CAT:DEL" )                                          #PROGram:CATalog:DELete

    #--------------------------------------------
    def StartSequence( self ) -> bool:
        return self.__device.SendCommand( "PROG:SEL:STAT RUN" )                                     #PROGram:SELected:STATe RUN

    #--------------------------------------------
    def PauseSequence( self ) -> bool:
        return self.__device.SendCommand( "PROG:SEL:STAT PAUS" )                                    #PROGram:SELected:STATe PAUSe

    #--------------------------------------------
    def ContinueSequence( self ) -> bool:
        return self.__device.SendCommand( "PROG:SEL:STAT CONT" )                                    #PROGram:SELected:STATe CONTinue

    #--------------------------------------------
    def NextStep( self ) -> bool:
        return self.__device.SendCommand( "PROG:SEL:STAT NEXT" )                                    #PROGram:SELected:STATe NEXT

    #--------------------------------------------
    def StopSequence( self ) -> bool:
        return self.__device.SendCommand( "PROG:SEL:STAT STOP" )                                    #PROGram:SELected:STATe STOP

    #---------------------------------------------------------------------
    class SEQUENCE_STATE(Enum):
        STOP    = 'STOP'
        PAUSE   = 'PAUSE'
        RUN     = 'RUN'

    #--------------------------------------------
    def GetSequenceState( self ) -> list:
        ans = self.__device.SendCommandGetAns( "PROG:SEL:STAT?" )                                   #PROGram:SELected:STATe
        if( ans == None ):  return None
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
    def TriggerStep( self ) -> bool:
        return self.__device.SendCommand( "TRIG:IMM" )                                              #TRIGger:IMMediate
        
    #--------------------------------------------
    def SendSequence( self, name : str, steps : list ) -> bool:
        if( self.__device.Connect() == False ): return False

        #delete current sequence with the same name
        if( self.SelectSequence( name ) == False ): return False
        if( self.DeleteSelectedSequence() == False ): return False

        #select sequence again and upload new sequence
        if( self.SelectSequence( name ) == False ): return False
        for i in range( len(steps) ):
            if( self.SetSequenceStep(i+1, steps[i]) == False ): return False

        self.__device.Close()
        return True

        