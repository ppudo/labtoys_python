from labtoys.Keysight.DAQ_3497xA import DAQ_3497xA
from labtoys.functions import Wait

logger = DAQ_3497xA( "10.1.0.50" )

print( "IDN: " + str(logger.GetIDN()))
print( f"CARD 1: {logger.GetSystemCardType(logger.SYSTEM_CARD_IDX.CARD_1)}" )
print( f"CARD 2: {logger.GetSystemCardType(logger.SYSTEM_CARD_IDX.CARD_2)}"  )
print( f"CARD 3: {logger.GetSystemCardType(logger.SYSTEM_CARD_IDX.CARD_3)}"  )

'''
logger.ConfigureThermocouple( 1, 1, logger.THERMOCOUPLE_TYPE.TYPE_K )
logger.ConfigureVoltageDC( 1, 2, logger.VOLT_RANGE.RANGE_AUTO )
logger.ConfigureThermocouple( 1, 3, logger.THERMOCOUPLE_TYPE.TYPE_K )
'''

print( "Start configuration" )
scanList = []
for i in range( 20 ):
    logger.ConfigureVoltageDC( 1, i+1, logger.VOLT_RANGE.RANGE_AUTO )
    scanList.append( [1, i+1] )

for i in range( 20 ):
    logger.ConfigureThermocouple( 2, i+1, logger.THERMOCOUPLE_TYPE.TYPE_K )
    scanList.append( [2, i+1] )

'''
print( "Send scan list" )
logger.ConfigureScanList( scanList )
Wait( "wait after configuration", 10 )


for i in range( 10 ):
    value = logger.Read()
    print( f"{i}: {value}" )
    Wait( "next reading", 10 )

'''