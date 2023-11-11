from GPS_Mapper import GPSVis
from PIL import Image,ImageDraw
import os
import numpy as np
import statistics 

from PIL import Image
import random
import numpy as np
import gridmarker

def remove(duplicate):
  final_list = []
  for num in duplicate:
    if num not in final_list:
        final_list.append(num)
  return final_list


def drawFirePattern(no_of_days,date,co_ordinates,pulled_image_path):
    resultpath="Results"
    if not os.path.exists(resultpath):
        os.makedirs(resultpath)         
    map_value=1
    if(map_value==1):
       
        st=co_ordinates.split(",")
        lat1=float(st[0])
        lang1=float(st[1])
        lat2=float(st[2])
        lang2=float(st[3])
        imageob = Image.open(pulled_image_path)
       # imageob = imageob.resize((1000,1000), Image.ANTIALIAS)
        imageob.save("Input_map.jpg") 
        
        vis = GPSVis(data_path='predicted_Cord.csv',
                     map_path='Input_map.jpg',  # Path to map downloaded from the OSM.
                     
                    points=(lat1,lang1, lat2, lang2)) # Two coordinates of the map (upper left, lower right)
        
        vis.create_image(color=(0, 0, 255), width=3)  # Set the color and the width of the GNSS tracks.
        img_points=vis.plot_map(output='save')
        
       # print("img_points ",img_points)
       
        finpath="Fire_Pattern_Predicted.png"
        gridmarker.getGriDImage()
        p1,p2=137,129  # LEFT Top corner
        p3,p4=800,800  # Right Bottom Corner
        newpoints=[]
        iqrdata=[]
        for points in img_points:
            x=points[0]
            y=points[1]
            if((x>p1 and x<p3) and (y>p2 and y<p4)):
                newrow=[]
                newrow.append(x)
                newrow.append(y)
                newpoints.append(newrow)
            else:
                if(x<p1):
                    x=p1+abs(p1-x)
                if(y<p2):
                    y=p2+abs(p2-y)
                if(x>p3):
                    x=x-abs(p3-x)
                if(y>p4):
                    y=y-abs(p4-y)
                    
                newrow=[]
                newrow.append(x)
                newrow.append(y)
                newpoints.append(newrow)   
        uniquepoints=[]            
        uniquepoints=remove(newpoints)
        
        sumlist=[]
        for row in uniquepoints:
            x1=row[0]
            y1=row[1]
            sum=x1+y1
            # sum1=abs(x1)+abs(y1)
            # iqrdata.append(sum1)
            newrow=[]
            newrow.append(x1)
            newrow.append(y1)
            newrow.append(sum)
            sumlist.append(newrow)
            
        sumlist.sort(key = lambda r: r[2]) 
            
            
                   
      #  print("\n\n\n\n\n\n")        
    #    print("sortedlist new  points are : ",sumlist)        
        k=0
        
        index=0
        sign=-1
        mx=0
        my=0
        finlist=[]
        for row in sumlist:
            if(k<no_of_days):
                
                testimgob = Image.open(finpath).convert('RGB')
                x1=row[0]
                y1=row[1]
                # sum=x1+y1
                # sum1=abs(x1)+abs(y1)
                # iqrdata.append(sum1)
                k=k+1
                if(k==1):
                                
                   
                   
                    mx=x1
                    my=y1
                    point1 = np.array((mx, my))
                    point2 = np.array((x1, y1))
                    dist = np.linalg.norm(point1 - point2)
                    temprow=[]
                    temprow.append(x1)
                    temprow.append(y1)
                    temprow.append(dist)
                    finlist.append(temprow)
                    
                    
                else:
                    val1=random.randint(0,100)
                    val2=random.randint(0,100)
                    x1=x1+val1
                    y1=y1+val2
                   
                    point1 = np.array((mx, my))
                    point2 = np.array((x1, y1))
                    dist = np.linalg.norm(point1 - point2)
                    temprow=[]
                    temprow.append(x1)
                    temprow.append(y1)
                    temprow.append(dist)
                    finlist.append(temprow)
               
            else:
                break
        finlist.sort(key = lambda r: r[2]) 
        
       # print(" finlist" ,finlist)
        tr=1
        for rowq in finlist:
            testimgob = Image.open(finpath).convert('RGB')
            x1=rowq[0]
            y1=rowq[1] 
            sum=x1+y1
            sum1=abs(x1)+abs(y1)
            iqrdata.append(sum1)
            x2=x1+25
            y2=y1+25
                
              
                
            bbox =  (x1, y1, x2, y2)
            draw = ImageDraw.Draw(testimgob)
            draw.ellipse(bbox, fill=(255, 0, 0))
            temp=str(tr)
            temppath=resultpath+"//"+temp+".jpg"
              #  print("temppath ",temppath)
            testimgob.save(temppath) 
            finpath=temppath
            tr=tr+1
            index=index+3
            sign=sign*-1
           
            
        
      #  print("iqrdata ",iqrdata)
       
        mid=int(len(iqrdata)/2)
        # First quartile (Q1)
        Q1 = np.median(iqrdata[:mid])
          
        # Third quartile (Q3)
        Q3 = np.median(iqrdata[mid:])
        # Interquartile range (IQR)
        IQR = Q3 - Q1
          
        print("Interquartile range (IQR) value  ",IQR)
        mean=statistics.mean(iqrdata)
        sd=statistics.stdev(iqrdata)
        range1=mean-sd
        range2=mean+sd
        print("MEAN  : ",mean)
        print("STANDARD DEVIATION  : ",sd)
        print("RANGES  : ",range1," TO ",range2)
    
    