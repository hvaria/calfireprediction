import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns




class Preprocessing:
    def __init__(self,dataframe):
        self.df=dataframe  
        
    def dataPreprocessing(self):
        print("\n")
        print('Shape of the file')#Number of Rows and Columns
        print('************************************************************************')
        print(self.df.shape)

        print("\n")
        print('Number of Missing Values per Column')
        print('************************************************************************')
        print("\n")
        print(self.df.isnull().sum())
        
        print("\n")
        print('Variable types')
        print('************************************************************************')
        print(self.df.dtypes)
        
        limitPer = len(self.df) * .94
        
        #print("limitPer: ",limitPer)
        self.df = self.df.dropna(thresh=limitPer, axis=1)
        
        print("\n")
        print('Number of Missing Values per Column After Data Cleaning')
        print('************************************************************************')
        print("\n")
        print(self.df.isnull().sum())
       
        # Converting date format
        self.df['Date'] = pd.to_datetime(self.df["Date"]).dt.strftime('%d%m%Y').astype(int)  
                          
        print("\n")
        print('Find Correlation Between Different Attributes')
        print('************************************************************************')
        print("\n")
        
        corrmatrix=self.df.corr(method='pearson')
        print("The correlation matrix: ")
        print("\n")
        print(corrmatrix)
        plt.subplots()
        sns.set(rc={'figure.figsize':(15,11)})
        sns.heatmap(corrmatrix, vmax=0.9, square=True)
        plt.show()
        
             
         
        return self.df
