import pandas as pd
import preprocessing
import LSTM
datasetpath='Final_combined_datasets1.xlsx'
number_of_interations=500
#*******************Code to Preprocess Dataset***************************************
df=pd.read_excel(datasetpath)

print(df.head())

pre=preprocessing.Preprocessing(df)
df=pre.dataPreprocessing()


#*******************Code for LSTM***************************************

X=df[['Date','Temperature' ,'RelativeHumidity', 'WindSpeed','WindDirection','Precipitation', 
      'longitude','latitude','ndvi' ,'SLOPE', 'ELEVATION','FUEL_COVER','LAND_COVER']]


Y=df[['Fire_NonFire']]

l=LSTM.LSTMNeuralNetwork(X, Y,"LSTM",number_of_interations)
l.initLSTM()
    