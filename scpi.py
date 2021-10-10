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
#
#----------------------------------------------------------------------------------------------------------------------------------------------------
#       Idea and changes proposal:
#           
#       
#       Usefull information and links:
#           socket library  https://docs.python.org/3/library/socket.html
#

import socket

#----------------------------------------------------------------------------------------------------------------------------------------------------
class SCPI_Socket:
    def __init__( self, aIP="localhost", aPort=5025 ):
        self.ip = aIP
        self.port = aPort

    def Connect( self, timeout=10 ):
        self.__devSocket = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        self.__devSocket.connect( (self.ip, self.port) )
        self.__devSocket.settimeout( timeout )

    def Close( self ):
        self.__devSocket.close()

    def SendCommand( self, command ):
        command = command + "\n"
        self.__devSocket.sendall( command.encode( "UTF-8" ) )
        
    def SendCommandGetAns( self, command ):
        self.SendCommand( command )
        try:
            return self.__devSocket.recv( 1024 ).decode( "UTF-8" ).rstrip()
        except socket.timeout as msg:
            return None
    
    def SendCommandGetRaw( self, command, repsondLength=4096 ):
        self.SendCommand( command )
        return self.__devSocket.recv( repsondLength )

    def GetRaw( self, respondLength ):
        return self.__devSocket.recv( respondLength )

    def GetAns( self, respondLength ):
        return self.__devSocket.recv( respondLength ).decode( "UTF-8" ).rstrip()