import matplotlib.pyplot as plt
import matplotlib.ticker as plticker

def getGriDImage():
        
    try:
        from PIL import Image
    except ImportError:
        import Image
    
    # Open image file
    image = Image.open('Fire_Pattern_Predicted.png')
    
    # Set up figure
    gridLineWidth=5
    fig=plt.figure(figsize=(float(image.size[0])/gridLineWidth, float(image.size[1])/gridLineWidth), dpi=gridLineWidth)
    axes=fig.add_subplot(111)
    
    # Remove whitespace from around the image
   # fig.subplots_adjust(left=0,right=1,bottom=0,top=1)
    
    # Set the gridding interval: here we use the major tick interval
    gridInterval=127.
    location = plticker.MultipleLocator(base=gridInterval)
    axes.xaxis.set_major_locator(location)
    axes.yaxis.set_major_locator(location)
    
    
    
    
    # Add the grid
    axes.grid(which='major', axis='both', linestyle='-', linewidth=10,color='#000000')
    
    # Add the image
   # axes.imshow(image)
    
    ##The below lines can be skipped if labelling of grids is not required
    # Find number of gridsquares in x and y direction
    nx=abs(int(float(axes.get_xlim()[1]-axes.get_xlim()[0])/float(gridInterval)))
    ny=abs(int(float(axes.get_ylim()[1]-axes.get_ylim()[0])/float(gridInterval)))
    
    # Add some labels to the gridsquares
    for j in range(ny):
        y=gridInterval/2+j*gridInterval
        for i in range(nx):
            x=gridInterval/2.+float(i)*gridInterval
            axes.text(x,y,'{:d}'.format(i+j*nx), color='#000000', fontsize='25',  ha='center', va='center')
    ##Can be skipped until here
    
    
    # Save the figure
   # fig.savefig("Fire_Pattern_Predicted.png", dpi=gridLineWidth)
    
#getGriDImage() 