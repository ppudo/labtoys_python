#MSO5x.py
#   Created on:	2020.11.18
#       Author: ppudo
#       e-mail:	ppudo@outlook.com
#
#   Project: 	labtoys
#   Description: 	Class representing Tektronix MSO5 osciloscope series 
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
#           Programing manual:  https://download.tek.com/manual/5-Series-MSO54-MSO56-MSO58-MSO58L-Programmer-Manual_EN-US_077130501.pdf      (2021.11.18)
#

from ..scpi import SCPI_Socket
from enum import Enum

class MSO5x:

    def __init__( self, ip, port=4000 ):
        self.__device = SCPI_Socket( ip, port )
        self.__device.sendDalay = 0.001

    #------------------------------------------------------------------------------------------------------------------------------------------------
    # BASIC COMMANDS
    #------------------------------------------------------------------------------------------------------------------------------------------------
    def Clear( self ) -> bool:
        self.__device.SendCommand( "CLEAR" ) == 0                                                   #CLEAR

    #----------------------------------------------------------------------------------------------
    def Autoset( self ) -> bool:
        self.__device.SendCommand( "AUTO" ) == 0                                                    #AUTOset

    #------------------------------------------------------------------------------------------------------------------------------------------------
    # ACQUISITION COMMANDS
    #------------------------------------------------------------------------------------------------------------------------------------------------
    class ACQUIRE_STATE( Enum ):
        RUN     = 'RUN'
        STOP    = 'STOP'
        ERROR   = 'ERROR'                   #do not use, only for indication of results

    #--------------------------------------------
    def SetAcquireState( self, state: ACQUIRE_STATE=ACQUIRE_STATE.RUN ) -> bool:
        return self.__device.SendCommand( "ACQ:STATE " + state.value ) == 0                         #ACQuire:STATE

    #--------------------------------------------
    def GetAcquireState( self ) -> ACQUIRE_STATE:
        ans = self.__device.SendCommandGetAns( "TRIG:A:MOD?" )                                      #TRIGger:A:MODe?
        if( ans == "" ):    return self.ACQUIRE_STATE.ERROR
        if( ans == '1' ):
            return self.ACQUIRE_STATE.RUN
        elif( ans == '0' ):
            return self.ACQUIRE_STATE.STOP
        else:
            return self.ACQUIRE_STATE.ERROR

    #----------------------------------------------------------------------------------------------
    class ACQUIRE_STOP_AFTER( Enum ):
        RUN_STOP    = 'RUNSTOP'
        SEQUENCE    = 'SEQUENCE'
        ERROR       = 'ERROR'               #do not use, only for indication of results

    #--------------------------------------------
    def SetAcquireStopAfter( self, mode: ACQUIRE_STOP_AFTER=ACQUIRE_STOP_AFTER.RUN_STOP ) -> bool:
        return self.__device.SendCommand( "ACQ:STOPA " + mode.value ) == 0                          #ACQuire:STOPAfter

    #--------------------------------------------
    def GetAcquireStopAfter( self ) -> ACQUIRE_STOP_AFTER:
        ans = self.__device.SendCommandGetAns( "TRIG:A:MOD?" )                                      #TRIGger:A:MODe?
        if( ans == "" ):    return self.ACQUIRE_STOP_AFTER.ERROR
        try:
            return self.ACQUIRE_STOP_AFTER( ans )
        except ValueError:
            return self.ACQUIRE_STOP_AFTER.ERROR

    #----------------------------------------------------------------------------------------------
    def Single( self ):
        self.SetAcquireStopAfter( self.ACQUIRE_STOP_AFTER.SEQUENCE )
        self.SetAcquireState( self.ACQUIRE_STATE.RUN )

    #------------------------------------------------------------------------------------------------------------------------------------------------
    # TRIGGER COMMANDS
    #------------------------------------------------------------------------------------------------------------------------------------------------
    class TRIGGER_MODE( Enum ):
        AUTO    = 'AUTO'
        NORMAL  = 'NORMAL'
        ERROR   = 'ERROR'                   #do not use, only for indication of results

    #--------------------------------------------
    def SetTrigger_A_Mode( self, mode: TRIGGER_MODE=TRIGGER_MODE.AUTO ) -> bool:
        return self.__device.SendCommand( "TRIG:A:MOD " + mode.value ) == 0                         #TRIGger:A:MODe
    
    #--------------------------------------------
    def GetTrigger_A_Mode( self ) -> TRIGGER_MODE:
        ans = self.__device.SendCommandGetAns( "TRIG:A:MOD?" )                                      #TRIGger:A:MODe?
        if( ans == "" ):    return self.TRIGGER_MODE.ERROR
        try:
            return self.TRIGGER_MODE( ans )
        except ValueError:
            return self.TRIGGER_MODE.ERROR

    #----------------------------------------------------------------------------------------------
    class TRIGGER_STATE( Enum ):
        ARMED       = 'ARMED'
        AUTO        = 'AUTO'
        READY       = 'READY'
        SAVE        = 'SAVE'
        TRIGGER     = 'TRIGGER'
        ERROR       = 'ERROR'               #do not use, only for indication of results

    #--------------------------------------------
    def TriggerForce( self ) -> bool:
        return self.__device.SendCommand( "TRIG FORC" ) == 0                                        #TRIGger FORCe

    #--------------------------------------------
    def GetTriggerState( self ) -> TRIGGER_STATE:
        ans = self.__device.SendCommandGetAns( "TRIG:STATE?" )                                      #TRIGger:STATE?
        if( ans == "" ):    return self.TRIGGER_STATE.ERROR
        try:
            return self.TRIGGER_STATE( ans )
        except ValueError:
            return self.TRIGGER_STATE.ERROR

    #------------------------------------------------------------------------------------------------------------------------------------------------
    # General Instructions
    #------------------------------------------------------------------------------------------------------------------------------------------------
    def GetIDN( self ) -> list:
        ans = self.__device.SendCommandGetAns( "*IDN?" )
        if( len(ans) == 0 ): return []
        return ans.split( ',' )

    #------------------------------------------------------------------------------------------------------------------------------------------------
    # MEASUREMENTS
    #------------------------------------------------------------------------------------------------------------------------------------------------
    def __GetMeasurementsMax( self, id: int, connIdx: int ) -> float:
        command = "MEASU:MEAS" + str(id) + ":RESU:ALLA:MAX?"                                        #MEASUrement:MEAS<x>:RESUlts:ALLAcqs:MAXimum?
        meas = self.__device.SendCommandGetAns( command, connIdx=connIdx )
        if( len(meas) == 0 ): return float( 'nan' )
        return float( meas )

    def GetMeasurementsMax( self, id: int ) -> float:
        return self.__GetMeasurementsMax( id, 0 )

    #----------------------------------------------------------------------------------------------
    def __GetMeasurementsMean( self, id: int, connIdx: int ) -> float:
        command = "MEASU:MEAS" + str(id) + ":RESU:ALLA:MEAN?"                                       #MEASUrement:MEAS<x>:RESUlts:ALLAcqs:MEAN?
        meas = self.__device.SendCommandGetAns( command, connIdx=connIdx )
        if( len(meas) == 0 ): return float( 'nan' )
        return float( meas )

    def GetMeasurementsMean( self, id: int, connIdx=0 ) -> float:
        return self.__GetMeasurementsMean( id, 0 )

    #----------------------------------------------------------------------------------------------
    def __GetMeasurementsMin( self, id: int, connIdx: int ) -> float:
        command = "MEASU:MEAS" + str(id) + ":RESU:ALLA:MIN?"                                       #MEASUrement:MEAS<x>:RESUlts:ALLAcqs:MINimum?
        meas = self.__device.SendCommandGetAns( command, connIdx=connIdx )
        if( len(meas) == 0 ): return float( 'nan' )
        return float( meas )

    def GetMeasurementsMin( self, id: int, connIdx=0 ) -> float:
        return self.__GetMeasurementsMin( id, 0 )


    #----------------------------------------------------------------------------------------------
    def __GetMeasurementsPK2PK( self, id: int, connIdx: int ) -> float:
        command = "MEASU:MEAS" + str(id) + ":RESU:ALLA:PK2PK?"                                      #MEASUrement:MEAS<x>:RESUlts:ALLAcqs:PK2PK?
        meas = self.__device.SendCommandGetAns( command, connIdx=connIdx )
        if( len(meas) == 0 ): return float( 'nan' )
        return float( meas )

    def GetMeasurementsPK2PK( self, id: int ) -> float:
        return self.__GetMeasurementsPK2PK( id, 0 )

    #----------------------------------------------------------------------------------------------
    def __GetMeasurementsPopulation( self, id: int, connIdx: int ) -> float:
        command = "MEASU:MEAS" + str(id) + ":RESU:ALLA:POPU?"                                      #MEASUrement:MEAS<x>:RESUlts:ALLAcqs:POPUlation?
        meas = self.__device.SendCommandGetAns( command, connIdx=connIdx )
        if( len(meas) == 0 ): return float( 'nan' )
        return float( meas )

    def GetMeasurementsPopulation( self, id: int ) -> float:
        return self.__GetMeasurementsPopulation( id, 0 )

    #----------------------------------------------------------------------------------------------
    def __GetMeasurementsStdDev( self, id: int, connIdx: int ) -> float:
        command = "MEASU:MEAS" + str(id) + ":RESU:ALLA:STDD?"                                      #MEASUrement:MEAS<x>:RESUlts:ALLAcqs:STDDev?
        meas = self.__device.SendCommandGetAns( command, connIdx=connIdx )
        if( len(meas) == 0 ): return float( 'nan' )
        return float( meas )

    def GetMeasurementsStdDev( self, id: int ) -> float:
        return self.__GetMeasurementsStdDev( id, 0 )

    #------------------------------------------------------------------------------------------------------------------------------------------------
    class Measurements:

        def __init__( self, max: float, mean: float, min: float, pk2pk: float, pop: float, stdDev: float ):
            self.__maximum = max
            self.__mean = mean
            self.__minimum = min
            self.__peak2peak = pk2pk
            self.__population = pop
            self.__standardDeviation = stdDev

        #------------------------------------------------------------------------------------------
        @property
        def maximum( self ):
            return self.__maximum

        #-----------------------------------------------------------------
        @property
        def mean( self ):
            return self.__mean
            
        #-----------------------------------------------------------------
        @property
        def minimum( self ):
            return self.__minimum

        #-----------------------------------------------------------------
        @property
        def peak2peak( self ):
            return self.__peak2peak

        #-----------------------------------------------------------------
        @property
        def population( self ):
            return self.__population

        #-----------------------------------------------------------------
        @property
        def standardDeviation( self ):
            return self.__standardDeviation
    
    #----------------------------------------------------------------------------------------------
    def GetMeasurements( self, id: int ) -> Measurements:
        connIdx = self.__device.Connect()
        if( connIdx == -1 ): return None

        meas = MSO5x.Measurements( max = self.__GetMeasurementsMax( id, connIdx ),
                                    mean = self.__GetMeasurementsMean( id, connIdx ),
                                    min = self.__GetMeasurementsMin( id, connIdx ),
                                    pk2pk = self.__GetMeasurementsPK2PK( id, connIdx ),
                                    pop = self.__GetMeasurementsPopulation( id, connIdx ),
                                    stdDev = self.__GetMeasurementsStdDev( id, connIdx ) )
        self.__device.Close( connIdx )
        return meas

    #------------------------------------------------------------------------------------------------------------------------------------------------
    # SAVE FUNCTIONS
    #------------------------------------------------------------------------------------------------------------------------------------------------
    def SetCurrentWorkingDirectory( self, path: str ) -> bool:
        #path - with "/" as separator
        command = "FILES:CWD \"" + path + "\""                                                      #FILESystem:CWD
        return self.__device.SendCommand( command ) == 0

    #--------------------------------------------
    def GetCurrentWorkingDirectory( self ) -> str:
        directory = self.__device.SendCommandGetAns( "FILES:CWD?" )                                 #FILESystem:CWD?
        if( len(directory) == 0 ): return ""
        return directory

    #----------------------------------------------------------------------------------------------
    def SaveSession( self, path: str ) -> bool:
        #path - file with *.tss extension and with "/" as separator
        command = "SAVE:SESSION "                                                                   #SAVE:SESSION <path>
        command += "\"" + path + "\""
        return self.__device.SendCommand( command ) == 0
