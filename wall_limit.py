import matplotlib.image as mpimg
from matplotlib import pyplot as plt
from matplotlib import colors
import numpy as np
import numpy as np
import PIL
from PIL import Image
import cv2
import time




from mpl_toolkits.mplot3d import Axes3D  # noqa
from matplotlib.colors import hsv_to_rgb


def read_cv(path):
    img = cv2.imread(path)
    
    plt.imshow(img)
    plt.show()
    return img

def make_edge(img):

    img = cv2.imread(img,0)
    edges = cv2.Canny(img,10,18,4)

    plt.subplot(121),plt.imshow(img,cmap = 'gray')
    plt.title('Original Image'), plt.xticks([]), plt.yticks([])
    plt.subplot(122),plt.imshow(edges,cmap = 'gray')
    plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

    plt.show()
    return 


def pixel_average(path):
    img_data = PIL.Image.open(path)
    img = np.array(img_data) 
    moy=np.array([0,0,0])
    for i in range(3):
        for j in range(len(img)):
            for k in range(len(img[0])):
                moy[i]=moy[i]+img[j][k][i]
    moy=moy/(640*360)
    return moy


def close_to_wall(path):
    moy=np.array([82.83657986, 59.25006076, 35.67680556])
    img_moy=pixel_average(path)
    for i in range(len(moy)):
        if ((moy[i]-5<img_moy[i]) & (img_moy[i] < moy[i]+5)):
            return True
    return False


def segment_fish(image):
    """ Attempts to segment the clown fish out of the provided image. """
    image=cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    hsv_image = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    light_orange = (0,0,51)   
    dark_orange =  (255,85,60)
    mask = cv2.inRange(hsv_image, light_orange, dark_orange)
    # light_ground = (0, 0, 20)
    # dark_ground = (206, 12, 24)
    # mask_ground = cv2.inRange(hsv_image, light_ground, dark_ground)
    final_mask = mask# + mask_white
    result = cv2.bitwise_and(image, image, mask=final_mask)
    # result = cv2.GaussianBlur(result, (7, 7), 0)
    plt.imshow(result)
    return 

def detect_guy(image, number=None):
    """ Attempts to segment the clown fish out of the provided image. """
    
    hsv_image = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    light_jean = (6,49,40)
    dark_jean = (20, 255, 90)
    mask = cv2.inRange(hsv_image, light_jean, dark_jean)

    #finds all contours in the segmented image
    contours=[]
    contours, hierarchy= cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
   
    #finds the biggest one and saving the new image with the contour drawn
    max_area=0
    i_max=0
    biggest_cnt=[]
    [cy,cx]=[0,0]
    if len(contours)!=0:
        for i,cnt in enumerate(contours):
            area = cv2.contourArea(cnt)
            if area>=max_area:
                max_area=area
                i_max=i
                biggest_cnt=cnt

        img = cv2.drawContours(image, contours, i_max, (0,255,0), 3)
        im = Image.fromarray(img)
        im.save('../img/test'+str(number)+'detected_guy.png')  

        #finds its coordinates and area
        M = cv2.moments(biggest_cnt)
        #print(M)
        if M['m00']!=0:
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
   
    return [cy,cx],max_area#, contours, mask

def detect_wall(image, number=None):
    """ Attempts to segment the clown fish out of the provided image. """
    image=cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    hsv_image = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    light_orange = (0,50,5)
    dark_orange = (25, 255, 100)
    
    mask = cv2.inRange(hsv_image, light_orange, dark_orange)
    plt.imshow(mask)
    #finds all contours in the segmented image
    contours=[]
    contours, hierarchy= cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    #finds the biggest one and saving the new image with the contour drawn and check the extreme points
    max_area=0
    i_max=0
    result='RAS'
    [cy,cx]=[0,0]
    if len(contours)!=0:
        for i,cnt in enumerate(contours):
            area = cv2.contourArea(cnt)
            if area>=max_area:
                max_area=area
                i_max=i
        img = cv2.drawContours(image, contours, i_max, (0,255,0), 3)
        im = Image.fromarray(img)
        im.save('../img/test'+str(number)+'wall_detected.png')  
        cnt=contours[i_max]
        topmost = tuple(cnt[cnt[:,:,1].argmin()][0])
        print(topmost)
        bottommost = tuple(cnt[cnt[:,:,1].argmax()][0])
        print(bottommost)
        leftmost = tuple(cnt[cnt[:,:,0].argmin()][0])
        print(leftmost)
        rightmost = tuple(cnt[cnt[:,:,0].argmax()][0])
        print(rightmost)
        size_wall=bottommost[1]-topmost[1]
        print(size_wall)
        if size_wall>120:
            if bottommost[0]<320:
                result='left'
            else:
                result='right'
    print(result)
    #result = cv2.bitwise_and(image, image, mask=mask)
    #plt.imshow(cv2.bitwise_and(image, image, mask=mask))
    # result = cv2.GaussianBlur(result, (7, 7), 0)
    # im = Image.fromarray(cv2.bitwise_and(image, image, mask=mask))
    # im.save('../img/test'+str(number)+'.png')
    return result, size_wall



### TESTING ###

#Average colors

# moy=pixel_average('../wall_limit.png')
# print("Le calcul donne : " + str(moy))

# tab=[False for i in range(2)]
# for i in range(2):
#     img_data = PIL.Image.open('../img/edge'+str(i+1) + '.png' )
#     img = np.array(img_data) 
#     tab[i]=close_to_wall(img)

# print(tab)


#Edges

# t1=time.time()
# make_edge('../img/victim11.png')
# t2=time.time()
# print(t2-t1)

#Colors_segmentation

# light_ground = (0,0,51)
# dark_ground = (255,85,60)
# light_jean = (6,49,40)
# dark_jean = (20, 255, 90)


# img=read_cv("../img/test18.png")
# # segment_fish(img)
# result, size_wall=detect_wall(img)
#finds all contours in the segmented image
# xy, area,contours, mask=detect_guy(img)
# plt.imshow(mask)
# print(str(xy) + ' ' + str(area))
