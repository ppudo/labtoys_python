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
#       -2021.10.30     version: 0.2.1
#           - Fix bugs from GetAnd ('\n' on the end). Add close counter for auto refresh functions. - bugs from c# code version
#       -2021.11.08     version: 0.3.0
#           - Add connection idx's like in C# version
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
        self.sendDalay = 0.001
        self.timeout = 10
        self.lineEnding = "\n"
        self.__ignoreCloseCounter = 0
        self.__stayConnected = list()

        self.__idxConnectionCounter = 0
        self.__connectionList = list()
        self.__currentConnectionIdx = 0
        self.__freeConnectionList = list()
        self.__connectionWaitTime = 0.005

    #----------------------------------------------------------------------------------------------
    def __ConnectInternal( self, stayConnected=False, oldIdx=0 ) -> int:
        idx = 0
        #recall old socket idx if oldIdx is in use
        if( oldIdx != 0 ):
            if oldIdx in self.__freeConnectionList:
                idx = oldIdx
                self.__connectionList.append( idx )
                self.__freeConnectionList.remove( idx )
                print( "Get from free: " + str(idx) )

        #create new idx
        if( idx == 0 ):
            self.__idxConnectionCounter += 1
            #no checking as integers in python has no limits
            idx = self.__idxConnectionCounter
            self.__connectionList.append( idx )
            print( "Create new idx: " + str(idx) )

        #create socket if there is no socket
        if( self.__devSocket == None ):
            try:
                self.__devSocket = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
                self.__devSocket.connect( (self.hostIP, self.hostPort) )
                self.__devSocket.settimeout( self.timeout )
            except:
                #err = sys.exc_info()
                #print( "Error: ", err[0] )
                self.__connectionList.remove( idx )
                self.__devSocket = None
                return -1

        #save stay connected state
        if( stayConnected ):
            self.__stayConnected.append( idx )

        #check for currenct connection idx
        if( self.__currentConnectionIdx == 0 ):
            self.__currentConnectionIdx = idx

        return idx

    #----------------------------------------------------------------------------------------------
    def Connect( self, oldIdx=0 ) -> int:
        return self.__ConnectInternal( True, oldIdx )

    #----------------------------------------------------------------------------------------------
    def Close( self, connIdx: int ):
        status = True
        try:
            self.__connectionList.remove( connIdx )
        except ValueError:
            try:
                self.__freeConnectionList.remove( connIdx )
            except ValueError:
                status = False
        if( status
            and len(self.__connectionList) == 0
            and len(self.__freeConnectionList) == 0 ):
            if( self.__devSocket != None ):
                self.__devSocket.shutdown( socket.SHUT_RDWR )
                self.__devSocket.close()
                self.__devSocket = None
            print( "Dispose scoket" )

        #if this was current connection we need to change it to other if there is other avaiable
        if( self.__currentConnectionIdx == connIdx ):
            if( len(self.__connectionList) > 0 ):
                self.__currentConnectionIdx = self.__connectionList[0]
            else:
                self.__currentConnectionIdx = 0

        #remove this index from stay connected idx's
        try:
            self.__connectionList.remove( connIdx )
        except ValueError:
            pass
            
        print( "Close idx: " + str(connIdx) )
        return

    #----------------------------------------------------------------------------------------------
    def Free( self, connIdx: int):
        status = True
        try:
            self.__connectionList.remove( connIdx )
        except ValueError:
            status = False

        #connection is moved to free only when it can be properly removed from connection list
        if( status ):
            self.__freeConnectionList.append( connIdx )

        #if this was current connection we need to change it to other if there is other avaiable
        if( self.__currentConnectionIdx == connIdx ):
            if( len(self.__connectionList) > 0 ):
                self.__currentConnectionIdx = self.__connectionList[0]
            else:
                self.__currentConnectionIdx = 0

        print( "Free idx: " + str(connIdx) )

    #----------------------------------------------------------------------------------------------
    def SendRaw( self, data, stayConnected=False, connIdx=0 ) -> int:
        #check for connection
        if( self.__devSocket == None
            or connIdx == 0 ):
            connIdx = self.__ConnectInternal( oldIdx=connIdx )
            if( connIdx == -1 ): return -1

        #check that we are allowed to transmit
        while( connIdx != self.__currentConnectionIdx ):
            time.sleep( self.__connectionWaitTime )

        #try to send message
        try:
            self.__devSocket.sendall( data )
            time.sleep( self.sendDalay )
            if( stayConnected == False
                and not (connIdx in self.__stayConnected) ):
                self.Close( connIdx )
                connIdx = 0
        except:
            #err = sys.exc_info()
            #print( "Error: ", err[0] )
            self.Close( connIdx )
            return -1

        return connIdx

    #----------------------------------------------------------------------------------------------
    def SendCommand( self, command, stayConnected=False, connIdx=0 ) -> int:
        #format command
        command = command + self.lineEnding
        return self.SendRaw( data=command.encode( "UTF-8" ), stayConnected=stayConnected, connIdx=connIdx )

    #----------------------------------------------------------------------------------------------
    def GetRaw( self, respondLength=4096, stayConnected=False, connIdx=0 ):
        if( self.__devSocket == None
            and connIdx == 0 ):
            return []

        #try to receive message
        try:
            res = self.__devSocket.recv( respondLength )
            if( stayConnected == False
                and not (connIdx in self.__stayConnected) ):
                self.Close( connIdx )
                connIdx = 0
        except:
            #err = sys.exc_info()
            #print( "Error: ", err[0] )
            self.Close( connIdx )
            return []

        return res

    #----------------------------------------------------------------------------------------------
    def GetAns( self, respondLength=1024, stayConnected=False, connIdx=0 ) -> str:
        res = self.GetRaw( respondLength=respondLength, stayConnected=stayConnected, connIdx=connIdx )
        if( len(res) == 0 ):
            return ""

        res = res.decode( "UTF-8" ).rstrip()
        if( res.endswith( self.lineEnding ) ):
            res = res[:len(res)-len(self.lineEnding)]

        return res

    #----------------------------------------------------------------------------------------------
    def SendCommandGetAns( self, command, respondLength=1024, stayConnected=False, connIdx=0 ) -> str:
        connIdx = self.SendCommand( command, True, connIdx )
        if( connIdx == -1 ):
            return ""
        return self.GetAns( respondLength, stayConnected=stayConnected, connIdx=connIdx )
    
    #----------------------------------------------------------------------------------------------
    def SendCommandGetRaw( self, command, respondLength=4096, stayConnected=False, connIdx=0 ):
        connIdx = self.SendCommand( command, True, connIdx )
        if( connIdx == -1 ):
            return []
        return self.GetRaw( respondLength=respondLength, stayConnected=stayConnected, connIdx=0 )

    

    