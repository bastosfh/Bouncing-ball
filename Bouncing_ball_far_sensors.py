####################
# Bouncing ball task
# Click all squares close to the cursor and click the boucing ball
# When it enters a contact rectangle above the squares.

# For a list of modifications to this script
# Please see the log at the end of the file

# Before running the script, activate the virtual environment:
# source Environments/psychopy-py38/bin/activate
# I've written a script that does this and starts PsychoPy automatically.
# So, run it before running this task from inside PsychoPy Coder.


#########################
# Import needed libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
import os
import sys
import psychopy.visual
import psychopy.event
import psychopy.core
import psychopy.monitors


################
# Configurations

# Experimental group name 'between quotes'
group_name = 'Delete'

# Participant number
sj_num = 1

# Number of trials
n_trials = 5

# Practice organization - distribution of the sensors on the screen
file_with_the_practice_org = 'Seriada'

# Adjust the size of the sensors (the script was written to work with 5)
# Bigger number --> Smaller sensors
sensor_size_denominator = 5


# Organization of the sensors on the screen
# organization_of_sensors = 4

########################
# Folders and file names
# Folder to return after saving trial data
script_path = '/home/coleta/Bouncing ball task'

group_path = script_path + '/' + group_name
id_sj = group_name + '_sj' + str(sj_num)
file_sj_name = group_name + '_sj' + str(sj_num) + '.tsv'
file_sj_path = script_path + '/' + group_name + '/' + file_sj_name
practice_org_path = script_path + '/' + file_with_the_practice_org

practice_org = pd.read_csv(practice_org_path, delimiter = "\t", header = None)

# Create experimental group folder inside the script folder
os.chdir(script_path)

# Check if the group folder already exists and create one if it doesn't
group_folder_exists = os.path.exists(group_path)
if not group_folder_exists:
    os.mkdir(group_name)

#############
# Open window
# For better timing: fullscr = True, allowGUI = False
# units: important, since mouse displacement is determined in the units given here
# color: goes from -1 to 1 for each rbg channel
win = psychopy.visual.Window(monitor='testMonitor', screen=0, units='pix', color=(-1,-1,-1),
                    fullscr=True, size=(1366, 768), allowGUI=False, checkTiming=True)

# checkTiming
frame_period = win.monitorFramePeriod
frame_rate = win.getActualFrameRate(
    nIdentical=10, nMaxFrames=100, nWarmUpFrames=10, threshold=1)

# Screen edges
screen_left = -683
screen_right = 683
screen_top = 384
screen_bottom = -384


###################
# Animation objects

# Animation objects parameters
ball_x_ini = screen_left
ball_y_ini = screen_bottom/1.2 # For a ball_y_ini of screen_bottom/1.2, the ball kicks when y = -305 (so, I can draw a line there. floor_y)
# ball_size = 10 # Radius in pixels
drop_length = 48
drop_width = 7

# Draw a line (floor) accounting for the size of the ball
# Size of the ball in pixels (this is just for drawing the scene before the trial begins)
# The size of the ball is afterwards given by the practice org file
ball_size = 10

floor_y = -305 - ball_size

# Sensor1 is the base for the rest of the calculations
# And that is why it is out of the if clauses below and comes
# Before the for loop I use to control de trials
sensor1_width = screen_top/sensor_size_denominator # Divided by 5 is the default
sensor1_height = screen_top/sensor_size_denominator
sensor1_x = screen_right/3
sensor1_y = floor_y + (sensor1_height/2)
sensor1_color = 'blue'

# Cursor initial position
#cursor_x_ini = 0
cursor_x_ini = (sensor1_x + sensor1_width*2.5)
cursor_y_ini = sensor1_height/2




####################
# Keyboard and mouse
# So that I can stop the script with the scape key inside the infinite loop (while True)
keys = psychopy.event.BuilderKeyResponse()

# Create a mouse object so that I can track its position and clicks
my_mouse = psychopy.event.Mouse(visible = False, win = win, newPos = np.array([(cursor_x_ini), (cursor_y_ini)]))

###################
# For loop - trials
trial = 0
while trial < n_trials:
    
    # Trial counter
    trial += 1

    # The organization of the sensors is given by an
    # External file, which is specified by the experimenter in
    # The begining of the file (configs). Depending on the contents of the
    # File, practice organization can change each trial.
    organization_of_sensors = practice_org[0][trial-1]
    ball_size = practice_org[1][trial-1]


    # Organization of the sensors on the screen
    if organization_of_sensors == 1:
        sensor1_x = screen_right/3
        sensor1_y = floor_y + (sensor1_height/2)

        sensor2_x = sensor1_x + sensor1_width*2.5
        sensor2_y = floor_y + sensor1_height*2

        sensor3_x = sensor1_x + (sensor1_width*5)
        sensor3_y = floor_y + (sensor1_height/2)

    elif organization_of_sensors == 2:
        sensor1_x = screen_right/3
        sensor1_y = floor_y + sensor1_height*2

        sensor2_x = sensor1_x + sensor1_width*2.5
        sensor2_y = floor_y + (sensor1_height/2)

        sensor3_x = sensor1_x + (sensor1_width*5)
        sensor3_y = floor_y + sensor1_height*2

    elif organization_of_sensors == 3:
        sensor1_x = screen_right/3
        sensor1_y = floor_y + (sensor1_height/2)

        sensor2_x = sensor1_x + sensor1_width*2.5
        sensor2_y = floor_y + sensor1_height*2

        sensor3_x = sensor1_x + (sensor1_width*5)
        sensor3_y = floor_y + sensor1_height*3.5

    elif organization_of_sensors == 4:
        sensor1_x = screen_right/3
        sensor1_y = floor_y + sensor1_height*3.5

        sensor2_x = sensor1_x + sensor1_width*2.5
        sensor2_y = floor_y + sensor1_height*2

        sensor3_x = sensor1_x + (sensor1_width*5)
        sensor3_y = floor_y + (sensor1_height/2)




    ####################
    # Create the objects
    ball = psychopy.visual.Circle(win=win, name='ball', units='pix', radius=ball_size, edges=32,
                        ori=0, pos=np.array([ball_x_ini, ball_y_ini]), lineWidth=1, lineColor='red', lineColorSpace='rgb',
                        fillColor='red', fillColorSpace='rgb', opacity=1, interpolate=True)

    floor = psychopy.visual.Line(win = win, units = 'pix', start=(screen_left, (floor_y)), end=(screen_right, (floor_y)),
                        lineWidth=1, lineColor='white', lineColorSpace='rgb',
                        opacity=1, interpolate=True)

    contact_area = psychopy.visual.Rect(win=win, name='contact_area', units='pix', width=(sensor1_width*4), height= (screen_top), # 20% da máxima altura da bola
                        ori=0, pos=np.array([(sensor1_x + sensor1_width*2.5),(255)]), lineWidth=0, lineColor='grey', lineColorSpace='rgb', # lineWidth=0 makes it easier to calculate distances
                        fillColor='grey', fillColorSpace='rgb', opacity=0.2, interpolate=True)

    cursor = psychopy.visual.Circle(win=win, name='cursor', units='pix', radius=5, edges=32, 
                        ori=0, pos=np.array([(cursor_x_ini), (cursor_y_ini)]), lineWidth=1, lineColor='green', lineColorSpace='rgb',
                        fillColor='green', fillColorSpace='rgb', opacity=1, interpolate=True)

    sensor1 = psychopy.visual.Rect(win=win, name='sensor1', units='pix', width=sensor1_width, height=sensor1_height,
                        ori=0, pos=np.array([(sensor1_x),(sensor1_y)]), lineWidth=0, lineColor=sensor1_color, lineColorSpace='rgb', # lineWidth=0 makes it easier to calculate distances
                        fillColor=sensor1_color, fillColorSpace='rgb', opacity=1, interpolate=True)

    sensor2 = psychopy.visual.Rect(win=win, name='sensor2', units='pix', width=sensor1_width, height=sensor1_height,
                        ori=0, pos=np.array([(sensor2_x),(sensor2_y)]), lineWidth=0, lineColor=sensor1_color, lineColorSpace='rgb',
                        fillColor=sensor1_color, fillColorSpace='rgb', opacity=1, interpolate=True)

    sensor3 = psychopy.visual.Rect(win=win, name='sensor3', units='pix', width=sensor1_width, height=sensor1_height,
                        ori=0, pos=np.array([(sensor3_x),(sensor3_y)]), lineWidth=0, lineColor=sensor1_color, lineColorSpace='rgb',
                        fillColor=sensor1_color, fillColorSpace='rgb', opacity=1, interpolate=True)

    text_ini = psychopy.visual.TextStim(win=win, text='Clique com o mouse para iniciar', height=sensor1_height/3)
    #text_ini = psychopy.visual.TextBox(window=win, text='Clique com o mouse para iniciar', 
    #                    font_size=14, font_color=[1,1,1], color_space='rgb', pos=(0.0,0.0), 
    #                    textgrid_shape=[20,1]) # 32 cols (32 chars wide) by 1 rows (1 line of text))

    # The text argument will be added to text_feedback in the feeback section
    text_feedback = psychopy.visual.TextStim(win=win, height=sensor1_height/3)

    # Stuff I use to test the animation. 
    # Comment after the script is finished.
    ball_x_all = ball_x_ini
    ball_y_all = ball_y_ini

    cursor_x_all = 0
    cursor_y_all = 0

    ###############################################
    # Variables I'll need inside the animation loop
    sensor_order = np.array([(0)]) #0 # Will give the sequence of clicked sensors
    time_sq = np.array([(0)]) # Will give the ordered timestamp of clicked sensors
    time_mouse_move = None
    time_sensor1 = None
    time_sensor2 = None
    time_sensor3 = None
    contact_area_click_time = None
    contact_area_click_pos = None
    contact_area_ball_pos = None
    radial_error = None

    ##################################
    # Interaction with the participant

    # Draw text to tell participant to click the mouse to start the trial
    # And all animation objects, except the ball
    text_ini.draw()
    floor.draw() 
    sensor1.draw()
    sensor2.draw()
    sensor3.draw()
    contact_area.draw()
    cursor.draw()
    # Flip all objects to the screen
    win.flip()

    # Wait until the mouse click to start the animation
    psychopy.event.clearEvents()
    mouse1 = 0
    while (mouse1 == 0):
        mouse1, mouse2, mouse3 = my_mouse.getPressed() # Read mouse buttons
        my_mouse.setPos(newPos=(cursor_x_ini,cursor_y_ini)) # Fix mouse position in the initial position
    

    ###############################################
    # Reference time to clocks inside the animation
    time_ini = psychopy.clock.getTime()

    ###########
    # Animation
    for bounce in range(1, 6):
        for k in range(1, drop_length):
            if k < (drop_length/2):
                ball_x = ball_x_ini+drop_width*k+(drop_length*drop_width*(bounce-1))
                ball_y = -1*(ball_y_ini+k**2)
            else:
                ball_x = ball_x_ini+drop_width*k+(drop_length*drop_width*(bounce-1))
                ball_y = -1*(ball_y_ini+(drop_length+1-k)**2)

            # Update objects position
            ball.pos = (ball_x, ball_y)
            cursor.pos = my_mouse.getPos()

            # Draw updated objects
            floor.draw() 
            sensor1.draw()
            sensor2.draw()
            sensor3.draw()
            contact_area.draw()
            ball.draw()
            cursor.draw()

            # Get time when mouse is moved from initial position
            #time_inside_animation = psychopy.clock.getTime() - time_ini
            if not time_mouse_move and (round(cursor.pos[0]) != round(cursor_x_ini)) and (round(cursor.pos[1]) != round(cursor_y_ini)): #and time_inside_animation > 1
                time_mouse_move = psychopy.clock.getTime() - time_ini
                time_sq = np.append(time_sq, time_mouse_move)

            # Check if the mouse is clicked when the cursor is inside the each "sensor"
            if  not time_sensor1 and my_mouse.isPressedIn(shape = sensor1, buttons=[0]): # Prevent multiple clicks AND Left clicks only
                sensor1.fillColor = 'yellow'
                sensor1.lineColor = 'yellow'
                time_sensor1 = psychopy.clock.getTime() - time_ini
                time_sq = np.append(time_sq, time_sensor1)
                sensor_order = np.append(sensor_order, 1) # Indicate the order in which sensor1 was clicked

            if  not time_sensor2 and my_mouse.isPressedIn(shape = sensor2, buttons=[0]): # Prevent multiple clicks AND Left clicks only
                sensor2.fillColor = 'yellow'
                sensor2.lineColor = 'yellow'
                time_sensor2 = psychopy.clock.getTime() - time_ini
                time_sq = np.append(time_sq, time_sensor2)
                sensor_order = np.append(sensor_order, 2) # Indicate the order in which sensor2 was clicked

            if  not time_sensor3 and my_mouse.isPressedIn(shape = sensor3, buttons=[0]): # Prevent multiple clicks AND Left clicks only
                sensor3.fillColor = 'yellow'
                sensor3.lineColor = 'yellow'
                time_sensor3= psychopy.clock.getTime() - time_ini
                time_sq = np.append(time_sq, time_sensor3)
                sensor_order = np.append(sensor_order, 3) # Indicate the order in which sensor2 was clicked

            # Check if the mouse is clicked when the cursor is inside the contact_are and calculate the radial error
            # (considering click position and ball position)
            if  not radial_error and my_mouse.isPressedIn(shape = contact_area, buttons=[0]): # Prevent multiple clicks AND Left clicks only
                contact_area.fillColor = 'yellow'
                contact_area.lineColor = 'yellow'
                contact_area_click_time = psychopy.clock.getTime() - time_ini
                # Calculate the distance from the mouse click to the centre of the ball (a2 = b2 + c2)
                radial_error = math.sqrt(((ball.pos[0] - cursor.pos[0])**2) + ((ball.pos[1] - cursor.pos[1])**2))
                # Get the screen position (x,y) where the click occurred
                contact_area_click_pos = cursor.pos
                # Get the ball position (x,y) when the click occurred
                contact_area_ball_pos = ball.pos

            # Flip the screen
            win.flip()

            # Colect data so I can check what is going on
            # Comment after the script is finished
            ball_y_all = np.append(ball_y_all, ball_y)
            ball_x_all = np.append(ball_x_all, ball_x)

            cursor_x_all = np.append(cursor_x_all, cursor.pos[0])
            cursor_y_all = np.append(cursor_y_all, cursor.pos[1])

            if psychopy.event.getKeys(keyList=["escape"]):
                win.close()  # core.quit()

    # Assemble clicks in one numeric sequence - easier to write to disk and analyse
    # Check if all 3 sensors were clicked and input zeros to complete the array (in case some sensor was not clicked)
    

    if len(sensor_order) < 4:
        zeros_to_input_in_sensor_order = np.array([4 - len(sensor_order)]) # Created with np for compatibility with np.repeat used below
        sensor_order = np.append(sensor_order, np.repeat(0, zeros_to_input_in_sensor_order))
        # Zeros at the end of time_sq. Its 1 more measure in relation to sensor_order (time when cursor starts moving)
        time_sq = np.append(time_sq, np.repeat(0, zeros_to_input_in_sensor_order + 1))

    sensor_order_assembled = int(str(sensor_order[1]) + str(sensor_order[2]) + str(sensor_order[3]))

    ######################
    # Input missing values 
    # (in case there is no response inside the animation)
    if not time_mouse_move:
        time_mouse_move = 0
    if not time_sensor1:
        time_sensor1 = 0
    if not time_sensor2:
        time_sensor2 = 0
    if not time_sensor3:
        time_sensor3 = 0
    if not contact_area_click_time:
        contact_area_click_time = 9999
        contact_area_click_pos =  np.array([(9999), (9999)])
        contact_area_ball_pos =  np.array([(9999), (9999)])

    ############################
    # Draw feeback to the screen
    if not radial_error:
        text_feedback.text = 'Não houve clique na área'
        radial_error = 9999
    else:
        text_feedback.text=(str(round(radial_error)) + ' pixels')
    
    text_feedback.draw()
    win.flip()

    # Wait until the mouse click to dismiss the feedback message
    mouse1 = 0
    while (mouse1 == 0):
        mouse1, mouse2, mouse3 = my_mouse.getPressed() # Read mouse buttons
    # Wait 50 ms so the mouse is not pressed when the next trial begins
    psychopy.clock.wait(1, hogCPUperiod=0.95)



    ###################################################
    # Saving data for this trial using pandas to append 
    # To an existing file 

    # Change directory to group folder
    os.chdir(group_path)



    
#    if not 'data_frame' in globals():
#        # Create an empty dataframe with headers IF the participant has no file inside the group's folder
#        # ELSE data_frame will exist and I can combine it with data_frame_current using to_csv with mode='a'
#        data_frame = pd.DataFrame(columns=['id', 'sensor_order', 'cursor_starts_moving', 'time_sensor1', 'time_sensor2', 'time_sensor3', 'contact_area_click_time', 'radial_error', 'contact_area_click_xpos', 'contact_area_click_ypos', 'contact_area_ball_xpos', 'contact_area_ball_ypos', 'ball_size', 'organization_of_sensors'])
    
    
    

    # Create a dataframe with data from current trial
    data_frame = pd.DataFrame({'id': id_sj, 
    'sensor_order': sensor_order_assembled,
    'cursor_starts_moving': time_sq[1],
    'time_sensor1': time_sq[2], 
    'time_sensor2': time_sq[3],
    'time_sensor3': time_sq[4], 
    'contact_area_click_time': contact_area_click_time, 
    'radial_error': radial_error,
    'contact_area_click_xpos': contact_area_click_pos[0], 
    'contact_area_click_ypos': contact_area_click_pos[1], 
    'contact_area_ball_xpos': contact_area_ball_pos[0], 
    'contact_area_ball_ypos': contact_area_ball_pos[1],
    'ball_size': ball_size,
    'sensor_size': sensor1_width,
    'organization_of_sensors': organization_of_sensors},
    index=[trial - 1])
    
    # Combine dataframes (the one with last trials and the one with data from current trial)
#    data_frame = pd.concat([data_frame, data_frame_current], ignore_index = True)




    # Does this participant already have a file in the disk?
    data_path_exists = os.path.exists(file_sj_path)

    if not data_path_exists:
        # Write the data to disk using to_csv with headers (because it is a new file)
        data_frame.to_csv(file_sj_name, sep='\t', na_rep='', header=True, decimal='.', index=False)
    else:
        # Read the dataframe from disk using pd.read_tsv
        #data_frame = pd.read_csv(file_sj_path, sep='\t')

        # Write the appended data to disk using to_csv, without headers and appending to an existing file (mode='a')
        data_frame.to_csv(file_sj_name, sep='\t', na_rep='', header=False, decimal='.', index=False, mode='a')

    # Change directory back to script folder
    os.chdir(script_path)

    # Clean up
    psychopy.event.clearEvents()




# Close window
win.close()



# To execute the file from terminal:
# /usr/bin/python3 '/home/flavio/Documents/Drive/Insync/Scripts/Python - scripts/Bouncing ball task/Bouncing_ball.py'


##############################
# Plots to check acquired data
# plt.plot(ball_x_all, ball_y_all)
# plt.show()


# plt.plot(cursor_x_all, cursor_y_all)
# plt.show()


# # Kill python
# psychopy.core.quit()



 
# 15 Dec 2023
# Loading the organization of practice was not automated.
# Now, the script loads the file with the name specified in the configuration.
# Two configurations are now need in a practive organization config file -- position of the sensors and size of the ball (tab separated).
# This setting (change ball size from external file) was created so that this feature can also be manipulated to study practice organization.


# 23 Nov 2023
# The append function in pandas was deprecated, which cased the script to fail.
# The script was re-written using concat instead.
# All the appendig is now done using to_csv.

# It is now possible to modify the size of the sensors.abs
# Keep in mind, though, that all spaces between sensors and the size of the contact are changed proportionally.


# 03 Sep 2021
# Initial position of the cursor was shifted closer do the contact area and
# Aligned to it.

# 21 May 2019
# Script is registering the radial_error and the time_contact_area_click
# EVEN IF THE BALL IS OUTSIDE the contact area.
# This way, we always have a performance measure.
# The contact_area acts as a "constraint" so that the participant understand
# He / she is not suposed to get the ball before it enters the contact area