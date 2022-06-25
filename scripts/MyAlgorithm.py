# !/usr/bin/python
#-*- coding: utf-8 -*-
import threading
import time
from datetime import datetime

import math
import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

time_cycle = 80

def canny_f(image):
    # converting to grey scale from rgb
    gray = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
    
    # removing image noise :- 
    blur = cv2.GaussianBlur(gray,(5,5),0)
    
    #finding gradient (this will highlight drastic change in derivative)
    canny = cv2.Canny(blur,50,150)    
    
    return canny

def display_lines(image, lines):
    line_image = np.zeros_like(image);
    if lines is not None:
        for line in lines:
            x1,y1,x2,y2=line.reshape(4);
            cv2.line(line_image,(x1,y1),(x2,y2),(255,0,0),10);
    return cv2.cvtColor(line_image,cv2.COLOR_RGB2GRAY)





class MyAlgorithm(threading.Thread):

    def __init__(self, camera, motors):
        self.final_coo = np.empty([0,2])
        self.camera = camera
        self.motors = motors
        self.threshold_image = np.zeros((640,360,3), np.uint8)
        self.color_image = np.zeros((640,360,3), np.uint8)
        self.stop_event = threading.Event()
        self.kill_event = threading.Event()
        self.lock = threading.Lock()
        self.threshold_image_lock = threading.Lock()
        self.color_image_lock = threading.Lock()
        threading.Thread.__init__(self, args=self.stop_event)
    def getcoordinates(self):
        return self.final_coo
    def getImage(self):
        self.lock.acquire()
        img = self.camera.getImage().data
        self.lock.release()
        return img

    def set_color_image (self, image):
        img  = np.copy(image)
        if len(img.shape) == 2:
          img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        self.color_image_lock.acquire()
        self.color_image = img
        self.color_image_lock.release()
        
    def get_color_image (self):
        self.color_image_lock.acquire()
        img = np.copy(self.color_image)
        self.color_image_lock.release()
        return img
        
    def set_threshold_image (self, image):
        img = np.copy(image)
        if len(img.shape) == 2:
          img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        self.threshold_image_lock.acquire()
        self.threshold_image = img
        self.threshold_image_lock.release()
        
    def get_threshold_image (self):
        self.threshold_image_lock.acquire()
        img  = np.copy(self.threshold_image)
        self.threshold_image_lock.release()
        return img

    def run (self):

        while (not self.kill_event.is_set()):
            start_time = datetime.now()
            if not self.stop_event.is_set():
                self.algorithm()
                self.img_detect()
            finish_Time = datetime.now()
            dt = finish_Time - start_time
            ms = (dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0
            #print (ms)
            if (ms < time_cycle):
                time.sleep((time_cycle - ms) / 1000.0)

    def stop (self):
        self.stop_event.set()

    def play (self):
        if self.is_alive():
            self.stop_event.clear()
        else:
            self.start()

    def kill (self):
        self.kill_event.set()

    def algorithm(self):
        #GETTING THE IMAGES
        image = self.getImage()
        print(image)
	
    def img_detect(self):
        image = self.getImage()
        lane_image = np.copy(image);
    	canny= canny_f(lane_image);

    	# 2nd,3rd arg bin size , 100 is the threshold , for bin acceptance
    	lines = cv2.HoughLinesP(canny,2,np.pi/180,20,np.array([]),minLineLength=5,maxLineGap=10)

    	# to display the lines
    	line_image = display_lines(lane_image,lines); 

    	# this will simply make the image pop up on our window

    	# print(canny.shape)

    	final_line_x = np.empty([0,1]);

    	final_line_y = np.array([]);

    	final_coordinates = np.empty([0,2]);

    	

    	for i in range(0,len(canny)):
    	    num=0;
    	    den=0;
    	    for j in range(len(canny[i])):
    		if(canny[i][j]>100):
    		    den=den+1;
    		    num=num+j;
    		
    	    if(den!=0):
    		new_ele= num/den
    		new_row=np.array([new_ele])
    		final_line_x = np.vstack ((final_line_x, new_row) )
    		final_line_y = np.append(final_line_y,i)
    		new_final_row = np.array([new_ele,i]);
    		final_coordinates = np.vstack ((final_coordinates, new_final_row) )
    		center_coordinates=(int(new_ele),int(i));
    	
    		canny = cv2.circle(canny, center_coordinates,1 , (255,0,0),2)

    		        
    	# print(final_line_x);
    	# print(final_line_y)




    	# reg = LinearRegression().fit(final_line_x,final_line_y)

    	# print(reg.coef_)

    	# print(reg.intercept_)

    	# print( image.shape[0])
    	# print( image.shape[1])



    	# canny = cv2.line(canny, (-232, 0), (0, 80), (255,0,0), 2)




    	# x1 = (0-reg.intercept_)/reg.coef_;
    	# y1=0;

    	# y2=len(canny);
    	# x2= (y2 - reg.intercept_)/reg.coef_;

    	# canny=cv2.line(canny, (int(x1), int(y1)), (int(x2), int(y2)), (255,0,0), 2);

    	cv2.imshow("result",canny)
    	cv2.waitKey(0)
        self.final_coo = final_coordinates
        

        # Add your code here
        print "Runing"

        #EXAMPLE OF HOW TO SEND INFORMATION TO THE ROBOT ACTUATORS
        #self.motors.sendV(10)
        #self.motors.sendW(5)

        #SHOW THE FILTERED IMAGE ON THE GUI
        self.set_threshold_image(image)
   
