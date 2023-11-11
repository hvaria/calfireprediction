import pandas as pd
import preprocessing
import Test_Processing


def predict(co_ordinates, date):
	datasetpath='Final_combined_datasets1.xlsx'


	no_of_days=5
	# date='2020-08-20'
	#co_ordinates='39.705062,-121.241684,40.579076,-120.327158'
	# co_ordinates='39.705062,-121.241684,41.579076,-120.327158'
	pulled_image_path="temp_image.jpg"
	print(co_ordinates, date )

	#*******************Code to Preprocess Dataset***************************************
	df=pd.read_excel(datasetpath)

	print(df.head())

	pre=preprocessing.Preprocessing(df)
	df=pre.dataPreprocessing()


	#*******************Code for LSTM***************************************

	X=df[['Date','Temperature' ,'RelativeHumidity', 'WindSpeed','WindDirection','Precipitation', 
	      'longitude','latitude','ndvi' ,'SLOPE', 'ELEVATION','FUEL_COVER','LAND_COVER']]


	Y=df[['Fire_NonFire']]

	l=Test_Processing.LSTMNeuralNetwork(X, Y,"LSTM",no_of_days,date,co_ordinates,df,pulled_image_path)
	l.initLSTM()
    
 