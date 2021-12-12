#D:\2021\11\29\python_test
from labtoys.Tektronix.MSO5x import MSO5x

mso = MSO5x( "10.1.0.10" )

#print( mso.SetCurrentWorkingDirectory("E:/2021/11/29/python_test") )
print( mso.GetCurrentWorkingDirectory() )

mso.SaveSession( "test_sesion.tss" )

print( mso.GetMeasurementsMean( 1 ) )

meas2 = mso.GetMeasurements( 2 )
print(  meas2.mean )

meas3 = mso.GetMeasurements( 3 )
print( meas3.minimum )

print( mso.GetTriggerState() )

meas1 = mso.GetMeasurements(1)
print( meas1 )