from labtoys.DeltaElektronika.PSC_ETH import PSC_ETH
import time

delta = PSC_ETH()

delta.SetRemoteVoltage( delta.REMOTE_STATUS.REMOTE )
delta.SetRemoteCurrent( delta.REMOTE_STATUS.REMOTE )
delta.SetOutputVoltage( 0.0 )
delta.SetOutputCurrent( 10.0 )
delta.EnableOutput()

time.sleep( 10 )

for i in range( 5 ):
    for x in range( 13 ):
        delta.SetOutputVoltage( float(x) )
        time.sleep( 1 )
    for x in range( 13 ):
        delta.SetOutputVoltage( float(12-x) )
        time.sleep( 1 )

delta.DisableOutput()










