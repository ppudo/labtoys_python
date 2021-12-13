from labtoys.Keysight.DAQ_3497xA import DAQ_3497xA
import labtoys.Keysight.DAQ_channel_config as DAQ_CFG
from labtoys.functions import Wait

daq = DAQ_3497xA( "10.1.0.106" )

daq.DeviceReset()
Wait( "wait for reset", 3 )

print( "IDN: " + str(daq.GetIDN()))
print( f"CARD 1: {daq.GetSystemCardType(daq.SYSTEM_CARD_IDX.CARD_1)}" )
print( f"CARD 2: {daq.GetSystemCardType(daq.SYSTEM_CARD_IDX.CARD_2)}" )
print( f"CARD 3: {daq.GetSystemCardType(daq.SYSTEM_CARD_IDX.CARD_3)}" )

print( "Start configuration" )
scanList = []
for i in range( 20 ):
    ch = DAQ_CFG.CHANNEL_CONFIG( DAQ_CFG.CHANNEL_TYPE.VOLT_DC, 1, i+1 )
    ch.voltRange = DAQ_CFG.VOLT_RANGE.RANGE_AUTO
    ch.scan = True
    scanList.append( ch )
for i in range( 20 ):
    ch = DAQ_CFG.CHANNEL_CONFIG( DAQ_CFG.CHANNEL_TYPE.VOLT_DC, 2, i+1 )
    ch.voltRange = DAQ_CFG.VOLT_RANGE.RANGE_AUTO
    ch.scan = True
    scanList.append( ch )
for i in range( 20 ):
    ch = DAQ_CFG.CHANNEL_CONFIG( DAQ_CFG.CHANNEL_TYPE.TEMP_THERMOCOUPLE, 3, i+1 )
    ch.thermocoupleType = DAQ_CFG.THERMOCOUPLE_TYPE.TYPE_K
    ch.tempUnit = DAQ_CFG.TEMP_UNIT.CELSIUS
    scanList.append( ch )
    
print( daq.ConfigureChannels(scanList) )
Wait( "wait after configuration", 10 )

for i in range( 10 ):
    value = daq.Read()
    print( f"{i}: {value}" )
    Wait( "next reading", 10 )
