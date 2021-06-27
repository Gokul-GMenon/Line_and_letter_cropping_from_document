import cv2 as cv
import os

name=0
source=0
img=0
img1=0
img2=0
line_height=0
line_start=0

def input_file():

    name = input('\tPlease input the name of the file with extension - ')
    source = os.path.join('Input\\',name)
    if os.path.isfile(source) == True:
        img = cv.imread(source, cv.IMREAD_GRAYSCALE)
        img1 = img.copy()
        img2 = cv.imread(source)
        line_height = img.shape[0]
        line_start = 1
        return 1,img,img1,img2,line_start,line_height
    else:
        return 0,0,0,0,0,0
        

# This function is called to obtain the starting margins for the line. ie; the upper
# corner of the crop. This is done only for cropping the lines
def gettingmargins(line_height, line_start,):

    x_loc = 0
    pos = img.shape[0]
    
    noline = True
    
    state =-1
    info = 0
    state_line = -1
    i = line_start + 6
    for j in range (0, img1.shape[1]):
        while i < (line_start + line_height-1):

            if img1[i,j] < 127:

                noline = False
                info += 1          
                if i < pos:
                    pos = i

            i+=1
        
                    
        if noline == False:
            line_start = pos-1 
            x_loc = j
            j+=2
            state = -1
            break
        i = line_start -1
        # To show end of file
        noline = True

    if noline == True:
        
        return x_loc,line_start, 1
    else:
        return x_loc,line_start, 0


# This function is used to understand the height of each line. This is used for cropping
# the lines.
def lineheight(line_start):
    
    flag = -1
    itr = 0

    for i in range(line_start , img.shape[0]):
        flag = 0
        for j in range(0, img.shape[1]):
            
            if img1[i,j] < 145:    
                itr += 1
                if itr != 1:
                    flag = 1
                    break
                else:
                    flag = 0
            else:
                flag = 0
        if flag == 0 and itr > 1:
            break
        
        
    line_height = i - line_start
    
    return line_height

# This function is used for finding the lower corners of the crop when drawing 
# the rectangle.
def getting_horizontal(line_height, line_start, x_loc, i):

    flag = -1
    hold = 0

    while i < line_height+line_start:
        
        pt1 = line_start - 2
        pt2 = x_loc - 2
        j = img1.shape[1]-1
        pos = i

        while pos  <= i + line_height-3:    

            while j > x_loc:

                if img1[pos,j] < 145:
                    flag = 0
                    break
                j -= 1
            if j > hold and flag == 0:
                
                hold = j
            flag = -1
            j = img1.shape[1] - 1
            pos += 1    
        
        i += line_height
        
    return hold,pt1,pt2


# This function is used for cropping the individual letters in each line. The line itself
# is passed as a numpy array and cropping is done on it.
def lettergap(line_start, img, save):

    pos1 = pos2 = pos4 = pos3 =0
    # line_start = 0
    img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    
    state =-1
    # shape = img.shape
    state_line = -1
    for j in range (0, img_gray.shape[1]):
        for i in range (0, img_gray.shape[0]):

            if img_gray[i,j] < 127:

                # To note that there was atleast one dark 
                # pixel this round
                state_line = 0
    
                # To mark the starting position
                if state == -1:  
                    state = 0                  
                    pos1 = i-1
                    pos2 = j -1
                    
                    
                    break
                else:
                    break
                    
        if state_line == -1 and state == 0:# and i != img.shape[0]-1:
            pos3 = i +1
            pos4 = j +1
            # line_start = pos3
            
            
            state = -1
            img_letter = img[pos1:pos3,pos2:pos4].copy()
            name = 'letter_'+ str(save) +'.png'
    
            
            path = os.path.join('Letters\\',name)
            cv.imwrite(path, img_letter)
            save+=1
            
        state_line = -1
    
    return save

# This is the primary function called for cropping lines. It calls the above mentioned
# functions during execution. It also calls the function for cropping the letters
# after each line has been cropped and saved.
def cropLines(line_start, line_height, save =0, save_letter = 1, save_word = 1):
    k=0
    start = 0
    while True:
        x_loc = 0
        
        if line_start+line_height>img.shape[0]+1:
            break
        x_loc, start, p = gettingmargins(line_height, start)
        
        if start>line_start:
            line_start = start


        line_height = lineheight(line_start)

    
        
        pt1=pt2=pt3=pt4=0
        
        i = line_start

        hold, pt1,pt2 = getting_horizontal(line_height, line_start, x_loc,i)
    
        
        pt3 = pt1 + line_height + 4 
        pt4 = hold + 2 
        
    
        if pt4 > x_loc:
            cv.rectangle(img, (pt2, pt1), (pt4, pt3), color = 0)
            save +=1
            img3 = img2[pt1:pt3,pt2:pt4].copy()
            name = 'line_'+ str(save) +'.png'
        
            path = os.path.join('Lines\\',name)
            cv.imwrite(path, img3)
            save_letter = lettergap(line_start, img3, save_letter)
        
        
        if k<line_start:
            k = line_start + line_height
        else:
            k += line_height
        line_start+=line_height
    
    
    return

exist, img, img1, img2, line_start, line_height = input_file()
if exist==0:
    print("\n\tFILE DOES NOT EXIST!!!")
else:
    cropLines(line_start, line_height)
    cv.waitKey(0)