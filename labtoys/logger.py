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
#
#----------------------------------------------------------------------------------------------------------------------------------------------------
#       Idea and changes proposal:         
#       
#       Usefull information and links:
#

import datetime

class Logger:

    def __init__( self, path, maxUnsaved=10, maxLines=10000, lineEnd="\n" ):
        self.__path = path
        self.__file = open( self.__path, 'a' )
        #self.__fileName = ""                                                                        #get file name
        self.__maxUnsaved = maxUnsaved                                                              #evry how many lines should I do repoen the file
        self.__unsaved = 0                                                                          #current lines counter to reopen
        self.__maxLines = maxLines                                                                  #how many lines can be in one file
        self.__linesInFile = 0                                                                      #how many lines is currently in file
        self.__allLines = 0                                                                         #summary of all lines
        self.__fileIdx = 0                                                                          #file inedtyficator - when excene linesInFile excede maxLines, new file is created
        self.__headers = None
        self.__lineEnd = lineEnd

    #----------------------------------------------------------------------------------------------
    def __WriteLine( self, line ) -> bool:
        line = line + self.__lineEnd
        try:
            self.__file.write( line )
        except:
            return False

        self.__allLines += 1
        self.__linesInFile += 1
        self.__unsaved += 1
        if( self.__unsaved >= self.__maxUnsaved ):
            self.__unsaved = 0
            return self.__ReOpen()
        return True

    #----------------------------------------------------------------------------------------------
    def __ReOpen( self ) -> bool:
        try:
            self.__file.close()
            self.__file.open( self.__path, 'a' )
        except:
            return False
        
        return True

    #----------------------------------------------------------------------------------------------
    def CloseFile( self ):
        self.__file.close()

    #----------------------------------------------------------------------------------------------
    def MakeHeaders( self, columnsNames ) -> bool:
        if( self.__headers != None ):
            return False

        header = ""
        self.__headers = [ "Date", "Time" ]
        for i in range( len(self.__headers) ):
            header = header + self.__headers[i] + ";"
        header = header[:-1]

        for i in range( len(columnsNames) ):
            header = header + ";" + columnsNames[i]
            self.__headers.append( columnsNames[i] ) 
        return self.__WriteLine(header)

    #----------------------------------------------------------------------------------------------
    def Log( self, data ) -> bool:
        now = datetime.datetime.now()
        line = str(now.year) + "." + str(now.month) + "." + str(now.day) + ";"
        line = line + str(now.hour) + ":" + str(now.minute) + ":" + str(now.second)

        for i in range( len(data) ):
            line = line + ";" + str( data[i] )

        return self.__WriteLine( line )

#if __name__ == "__main__":
#    log = Logger( "Test2.csv" )
#    log.MakeHeaders(["idx", "1", "2"])
#    for i in range( 30 ):
#        log.Log( [i, i*43563, i*65672/(32*(i+1)/3)] )
#    log.CloseFile()