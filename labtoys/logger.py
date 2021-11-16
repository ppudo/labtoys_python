#scpi.py
#   Created on:	2021.10.25
#       Author: ppudo
#       e-mail:	ppudo@outlook.com
#
#   Project: 	labtoys
#   Description: 	Class is responsible for creating and writing log data created during test
#
#
#   Changelog:
#      	-2020.10.25		version: 0.1.0
#      		- Initial class
#       -2021.11.15     version: 0.2.0
#           - Changes for more options
#
#----------------------------------------------------------------------------------------------------------------------------------------------------
#       Idea and changes proposal:         
#       
#       Usefull information and links:
#

from datetime import datetime
from genericpath import exists
import os

class Logger:

    def __init__( self, filePath: str ):
        self.__fileFullPath = filePath 
        if( not os.path.isabs(filePath) ):
            self.__fileFullPath = os.path.abspath(filePath)

        pathElements = self.__fileFullPath.split( '\\' )
        self.__fileName = pathElements[ len(pathElements)-1 ]
        self.__path = self.__fileFullPath.replace( self.__fileName, "" )
        
        print( "full path: " + self.__fileFullPath )
        print( "fileName: " + self.__fileName )
        print( "path: " + self.__path )

        testPath = pathElements[0] + '\\'
        pathElements.remove( pathElements[0] )
        for i in range( len(pathElements)-1 ):
            testPath = os.path.join( testPath, pathElements[i] )
            if( not os.path.exists( testPath) ):
                os.mkdir( testPath )
                print( "create dir: " + testPath )

        self.__file = None
        self.__OpenFile()

        #init variables
        self.maxUnsaved = 10
        self.maxLines = 10000
        self.__unsaved = 0
        self.__linesInFile = 0
        self.__allLines = 0
        self.__fileIdx = 0

        self.__headers = []
        self.lineEnding = "\n"
        self.columnSeparator = ";"

        self.__startTime = datetime.now()
        self.__idx = 0

        self.includeDate = True
        self.includeTime = True
        self.includeIdx = False
        self.includeTimeFromStart = False

    #------------------------------------------------------------------------------------------------------------------------------------------------
    @property
    def path( self ):
        return self.__path

    @property
    def fileName( self ):
        return self.__fileName

    @property
    def allLines( self ):
        return self.__allLines

    #---------------------------------------------------------------------
    @property
    def headers( self ):
        return self.__headers

    #------------------------------------------------------------------------------------------------------------------------------------------------
    def __WriteLine( self, line: str, reOpen: bool = False ) -> bool:
        line = line + self.lineEnding
        self.__unsaved += 1
        try:
            self.__file.write( line )
        except:
            return False

        self.__allLines += 1
        self.__linesInFile += 1
        if( self.__unsaved >= self.maxUnsaved
            or reOpen ):
            self.__unsaved = 0
            return self.__ReOpen()
        return True

    #----------------------------------------------------------------------------------------------
    def __OpenFile( self ) -> bool:
        try:
            self.__file = open( self.__fileFullPath, 'a' )
        except Exception as e:
            print( e.args )
            self.__file = None
            return False
        return True  

    #----------------------------------------------------------------------------------------------
    def __ReOpen( self ) -> bool:
        print( "Re open" )
        self.CloseFile
        return self.__OpenFile()

    #----------------------------------------------------------------------------------------------
    def CloseFile( self ):
        self.__file.close()
        self.__file = None

    #----------------------------------------------------------------------------------------------
    def MakeHeaders( self, columnsNames: list ) -> bool:
        if( len( columnsNames ) == 0 
            and len( self.__headers ) != 0 ):
            return False

        header = ""

        #predefined columns
        if( self.includeDate ):
            header += "Date" + self.columnSeparator
            self.__headers.append( "Date" )

        if( self.includeTime ):
            header += "Time" + self.columnSeparator
            self.__headers.append( "Time" )

        if( self.includeIdx ):
            header += "Idx" + self.columnSeparator
            self.__headers.append( "Idx" )

        if( self.includeTimeFromStart ):
            header += "Time_from_start" + self.columnSeparator
            self.__headers.append( "Time_from_start" )

        #user columns
        for i in range( len(columnsNames) ):
            header += columnsNames[i] + self.columnSeparator
            self.__headers.append( columnsNames[i] )
        
        header = header[:-len(self.columnSeparator)]
        return self.__WriteLine(header, True)

    #----------------------------------------------------------------------------------------------
    def Log( self, data: list ) -> bool:
        line = ""
        time = datetime.now()

        #predefined columns
        if( self.includeDate ):
            line += time.strftime( "%Y.%m.%d" ) + self.columnSeparator

        if( self.includeTime ):
            line += time.strftime( "%H:%M:%S" ) + self.columnSeparator

        if( self.includeIdx ):
            self.__idx += 1
            line += str( self.__idx ) + self.columnSeparator
        
        if( self.includeTimeFromStart ):
            line += "{:.3f}".format( (time - self.__startTime).total_seconds() ) + self.columnSeparator
        
        #user data
        for i in range( len(data) ):
            line += str( data[i] ) + self.columnSeparator

        line = line[:-len(self.columnSeparator)]
        return self.__WriteLine( line )
