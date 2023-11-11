from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense
from sklearn.metrics import mean_squared_error
from plot_keras_history import show_history, plot_history
import math
from matplotlib import pyplot as plt 
import pandas as pd
from keras.layers import Dropout

import csv

class LSTMNeuralNetwork:
    
    def __init__(self, X,Y,name,number_of_interations):
        self.X=X
        self.Y=Y
        self.name=name
        self.number_of_interations=number_of_interations
       
        
        
    def initLSTM(self):
        
        # Code to split dataset into testing and training
        X_train, X_test, Y_train, Y_test= train_test_split(self.X, self.Y, test_size=0.25,random_state=52,shuffle=True)

        print(X_train.shape)
        print(Y_train.shape)
        print(X_test.shape)
        print(Y_test.shape)



        # #define min max scaler and transfor data
        scaler = MinMaxScaler()
        train_X=scaler.fit_transform(X_train)
        test_X=scaler.transform(X_test)
        train_Y=scaler.fit_transform(Y_train)
        test_Y=scaler.transform(Y_test)


        # reshape input to be 3D for LSTM [samples, timesteps, features]
        train_X1 = train_X.reshape((train_X.shape[0],1,train_X.shape[1]))
        train_Y1 = train_Y.reshape((train_Y.shape[0],1,train_Y.shape[1]))
        test_X1= test_X.reshape((test_X.shape[0],1,test_X.shape[1]))
        test_Y1= test_Y.reshape((test_Y.shape[0],1,test_Y.shape[1]))




        print(train_X1.shape, train_Y1.shape, test_X1.shape)


        # Create LSTM network
        model = Sequential()
        model.add(LSTM(units=20,return_sequences=True,input_shape=(train_X1.shape[1], train_X1.shape[2])))
        model.add(Dropout(0.2))
        model.add(LSTM(units=40,return_sequences=True))
        model.add(Dropout(0.2))
        model.add(LSTM(units=80,return_sequences=True))
        model.add(Dropout(0.2))
        model.add(LSTM(units=80))
        model.add(Dropout(0.2))
        model.add(Dense(units=40,activation='tanh'))
        model.add(Dense(units=1, activation='tanh'))
        model.compile( optimizer='adam',loss='mean_squared_error', metrics=['accuracy'])
        history=model.fit(train_X1, train_Y1, epochs=self.number_of_interations, batch_size=10,validation_data=(test_X1, test_Y1), shuffle=False)
        model.save("LSTMModelData.h5")
        show_history(history)
        plot_history(history, path="Loss_Accuracy.png")
        plt.close()


        
        
        
        
        
        
