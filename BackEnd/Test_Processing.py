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
import MapInit
import csv
import glob
from PIL import Image




class LSTMNeuralNetwork:
    
    def __init__(self, X,Y,name,no_of_days,date,co_ordinates,dataframe,pulled_image_path):
        self.X=X
        self.Y=Y
        self.name=name
     
        self.no_of_days=no_of_days
        self.date=date
        self.co_ordinates=co_ordinates
        self.df=dataframe
        self.pulled_image_path=pulled_image_path
        
        
    def initLSTM(self):
        
        # Code to split dataset into testing and training
        X_train, X_test, Y_train, Y_test= train_test_split(self.X, self.Y, test_size=0.25,random_state=52,shuffle=True)

        print(X_train.shape)
    
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
        model.load_weights('LSTMModelData.h5')
        
        predicted_fire_status = model.predict(test_X1)
        df= pd.DataFrame(X_test['Date'])
        df= pd.to_datetime(df['Date'], format='%d%m%Y').dt.date
        #print(df.head())
        inputdate=pd.Series(df.unique()).tolist()
        testresult=[]    
        datalist=self.df.values.tolist()
        cordinates=[]
        for val in datalist:
            
            
            drow=[]
            drow.append(val[7])
            drow.append(val[6])
            cordinates.append(drow)
        with open('predicted_Cord.csv', 'w') as f:
            write = csv.writer(f)
            write.writerows(cordinates)    
        
       
      
        
        i=0
        
        for row in inputdate:
            value=predicted_fire_status[i]
            value1=str(row)
            #print(value1)
            
            if value<=0.04:
                value=0
            else:
                value=1
                
            result=[value1,value]
            testresult.append(result)
            i+=1
            
                
      
      #  for row in testresult:
           # print(row)
        
     
  
       

        
        
      
        #calculate root mean squared error
        MapInit.drawFirePattern(self.no_of_days,self.date,self.co_ordinates,self.pulled_image_path)
        print("\n")
        print("*****************Root Mean Square Error Using LSTM********************")
        print("\n")
        lstmtestScore = math.sqrt(mean_squared_error(test_Y, predicted_fire_status))
        print('Root Mean Square Error for LSTM', lstmtestScore)
        frame_folder="Results"
        frames = [Image.open(image) for image in glob.glob(f"{frame_folder}/*.JPG")]
        frame_one = frames[0]
        frame_one.save('LSTM_output.gif', format="GIF", append_images=frames,save_all=True, duration=300, loop=0)
        