from labtoys.logger import Logger
import time
from random import random

log = Logger( "test\\test.csv" )
log.includeIdx = True
log.includeTimeFromStart = True

log.MakeHeaders( ["i", "Test1", "Test2", "Test3"] )

for i in range(100):
    log.Log( [i, random(), int( random() * 100 ), "test_" + str(i) ] )
    time.sleep( 5 )
    print( "Log: " + str(i) )

log.CloseFile()