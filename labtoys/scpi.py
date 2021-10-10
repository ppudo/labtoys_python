#scpi.py
#   Created on:	2020.10.29
#       Author: ppudo
#       e-mail:	ppudo@outlook.com
#
#   Project: 	labtoys
#   Description: 	Class is responsible for comunication between phisical device over transmition medium and class representing this device in system
#
#
#   Changelog:
#      	-2020.10.29		version: 0.1.0
#      		- Initial class
#       -2020.11.10     version: 0.1.1
#           - Return None when timeout occurs on receive - for test only on SendCommandGetAns
#       -2021.09.17     version: 0.2.0
#           - Change the way of sending messages. Now connecting is not requirred before sending message
#
#----------------------------------------------------------------------------------------------------------------------------------------------------
#       Idea and changes proposal:
#           
#       
#       Usefull information and links:
#           socket library  https://docs.python.org/3/library/socket.html
#

import socket
import time

#----------------------------------------------------------------------------------------------------------------------------------------------------
class SCPI_Socket:
    def __init__( self, ip, port ):
        self.hostIP = ip
        self.hostPort = port

        self.__devSocket = None
        self.__stayConnected = False
        self.sendDalay = 0.001
        self.timeout = 10
        

    #----------------------------------------------------------------------------------------------
    def __ConnectInternal( self, stayConnected=False ) -> bool:
        try:
            self.__devSocket = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
            self.__devSocket.connect( (self.ip, self.port) )
            self.__devSocket.settimeout( self.timeout )
            self.__stayConnected = stayConnected
        except:
            #err = sys.exc_info()
            #print( "Error: ", err[0] )
            self.__devSocket = None
            return False

        return True

    #----------------------------------------------------------------------------------------------
    def Connect( self ) -> bool:
        return self.__ConnectInternal( stayConnected=True )

    #----------------------------------------------------------------------------------------------
    def Close( self ):
        if( self.__devSocket != None ):
            self.__devSocket.shutdown( socket.SHUT_RDWR )
            self.__devSocket.close()
            self.__devSocket = None

    #----------------------------------------------------------------------------------------------
    def SendRaw( self, data, stayConnected=False ) -> bool:
        #connect to device
        if( self.__devSocket == None ):
            if( self.__ConnectInternal() == False ):
                return False

        #try to send message
        try:
            self.__devSocket.sendall( data )
            time.sleep( 0.001 )
            if( stayConnected == False
                and self.__stayConnected == False ):
                self.Close()
        except:
            #err = sys.exc_info()
            #print( "Error: ", err[0] )
            self.Close()
            return False

        return True

    #----------------------------------------------------------------------------------------------
    def SendCommand( self, command, stayConnected=False ) -> bool:
        #format command
        command = command + "\n"

        return self.SendRaw( data=command.encode( "UTF-8" ), stayConnected=stayConnected )

    #----------------------------------------------------------------------------------------------
    def GetRaw( self, respondLength=4096, stayConnected=False ):
        res = None
        if( self.__devSocket == None ):
            return res

        #try to receive message
        try:
            res = self.__devSocket.recv( respondLength )
            if( stayConnected == False
                and self.__stayConnected == False ):
                self.Close()
        except:
            #err = sys.exc_info()
            #print( "Error: ", err[0] )
            self.Close()
            return None

        return res

    #----------------------------------------------------------------------------------------------
    def GetAns( self, respondLength=1024, stayConnected=False ) -> str:
        res = self.GetRaw( respondLength=respondLength, stayConnected=stayConnected )
        if( res != None ):
            res = res.decode( "UTF-8" ).rstrip()

        return res

    #----------------------------------------------------------------------------------------------
    def SendCommandGetAns( self, command, stayConnected=False ) -> str:
        if( self.SendCommand( command, True ) == False ):
            return None
        return self.GetAns( respondLength=1024, stayConnected=stayConnected )
    
    #----------------------------------------------------------------------------------------------
    def SendCommandGetRaw( self, command, respondLength=4096, stayConnected=False ):
        if( self.SendCommand( command, True ) == False ):
            return None
        return self.GetRaw( respondLength=respondLength, stayConnected=stayConnected )

    

    