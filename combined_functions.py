
# DO NOT EDIT THIS FILE, IT IS A COMBINATION OF ALL THE FUNCTIONS IN THE functions/
# SUBDIRECTORY OF THIS REPOSITORY

from spike import PrimeHub, LightMatrix, Button, StatusLight, ForceSensor, MotionSensor, Speaker, ColorSensor, App, DistanceSensor, Motor, MotorPair
from spike.control import wait_for_seconds, wait_until, Timer
import math
import time
import hub


###
### BEGIN FUNCTION FROM FILE: control_attachments.py
###

# NOTE - default parameters are evaluated at compile time
# so we need to set ease to "None" by default
#and then if it is "None" set our actual default "LinearInOut"
def control_attachments(start_speed=40, end_speed=100, ease=None, degrees_wanted=720, also_end_if = None, motor_stop_mode='BRAKE', motor_letter='C', timeout_seconds = 0):
    print("=== Controlling attachment motor letter ", motor_letter, "degrees ", degrees_wanted)
    this_way = degrees_wanted>0
    t = Timer()
    t.reset()
    # if no ease, it sets the ease to linear
    if ease is None:
        ease = LinearInOut
    hub_motor = get_motor_by_letter( motor_letter )
    #it is presetting the count to 0
    hub_motor.preset( 0 )
    #set motor power to the start speed
    if (this_way):
        hub_motor.pwm( start_speed )
    else:
        hub_motor.pwm( -start_speed )

    keep_spinning = True

    while keep_spinning:
        speed, degrees_now, x, xx = hub_motor.get( )
        pct_to_degrees = abs(degrees_now) / abs(degrees_wanted)

        #math for fanding speed based on how far we are.
        speed = start_speed + ease(pct_to_degrees) * (end_speed - start_speed)
        if this_way:
            hub_motor.pwm(speed)
        else:
            hub_motor.pwm(-speed)

        #need to test multiple conditions
        #1 to the left
        #2 to the right
        #3 if ouur passed in functions is true (if touching black)
        if  ((degrees_now >= degrees_wanted and this_way) or
            (degrees_now<=degrees_wanted and not this_way) or
            also_end_if==True):
            print( degrees_now, 'all done' )
            keep_spinning = False
        ### at the start we start a timer and if that timer excedes timeout_seconds then it will stop.
        if timeout_seconds != 0 and t.now() > timeout_seconds:
            keep_spinning = False

        if keep_spinning == False:
            if motor_stop_mode == 'BRAKE':
                hub_motor.brake( )
            elif motor_stop_mode == 'FLOAT':
                hub_motor.float( )
            elif motor_stop_mode == 'HOLD':
                hub_motor.hold( )




###
### BEGIN FUNCTION FROM FILE: easing_functions.py
###

"""
Linear
"""
def LinearInOut(t):
	return t

"""
Quadratic easing functions
"""


def QuadEaseInOut(t):
	if t < 0.5:
	    return 2 * t * t
	return (-2 * t * t) + (4 * t) - 1


def QuadEaseIn(t):
    return t * t


def QuadEaseOut(t):
    return -(t * (t - 2))


"""
Cubic easing functions
"""


def CubicEaseIn(t):
    return t * t * t


def CubicEaseOut(t):
    return (t - 1) * (t - 1) * (t - 1) + 1


def CubicEaseInOut(t):
    if t < 0.5:
    	return 4 * t * t * t
    p = 2 * t - 2
    return 0.5 * p * p * p + 1


"""
Quartic easing functions
"""


def QuarticEaseIn(t):
    return t * t * t * t


def QuarticEaseOut(t):
    return (t - 1) * (t - 1) * (t - 1) * (1 - t) + 1


def QuarticEaseInOut(t):
    if t < 0.5:
        return 8 * t * t * t * t
    p = t - 1
    return -8 * p * p * p * p + 1


"""
Quintic easing functions
"""


def QuinticEaseIn(t):
    return t * t * t * t * t


def QuinticEaseOut(t):
    return (t - 1) * (t - 1) * (t - 1) * (t - 1) * (t - 1) + 1


def QuinticEaseInOut(t):
    if t < 0.5:
        return 16 * t * t * t * t * t
    p = (2 * t) - 2
    return 0.5 * p * p * p * p * p + 1


"""
Sine easing functions
"""


def SineEaseIn(t):
    return math.sin((t - 1) * math.pi / 2) + 1


def SineEaseOut(t):
    return math.sin(t * math.pi / 2)


def SineEaseInOut(t):
    return 0.5 * (1 - math.cos(t * math.pi))


"""
Circular easing functions
"""


def CircularEaseIn(t):
    return 1 - math.sqrt(1 - (t * t))


def CircularEaseOut(t):
    return math.sqrt((2 - t) * t)


def CircularEaseInOut(t):
    if t < 0.5:
        return 0.5 * (1 - math.sqrt(1 - 4 * (t * t)))
    return 0.5 * (math.sqrt(-((2 * t) - 3) * ((2 * t) - 1)) + 1)


"""
Exponential easing functions
"""


def ExponentialEaseIn(t):
    if t == 0:
        return 0
    return math.pow(2, 10 * (t - 1))


def ExponentialEaseOut(t):
    if t == 1:
        return 1
    return 1 - math.pow(2, -10 * t)


def ExponentialEaseInOut(t):
    if t == 0 or t == 1:
        return t

    if t < 0.5:
        return 0.5 * math.pow(2, (20 * t) - 10)
    return -0.5 * math.pow(2, (-20 * t) + 10) + 1


"""
Elastic Easing Functions
"""


def ElasticEaseIn(t):
	return math.sin(13 * math.pi / 2 * t) * math.pow(2, 10 * (t - 1))


def ElasticEaseOut(t):
    return math.sin(-13 * math.pi / 2 * (t + 1)) * math.pow(2, -10 * t) + 1


def ElasticEaseInOut(t):
    if t < 0.5:
        return (
            0.5
            * math.sin(13 * math.pi / 2 * (2 * t))
            * math.pow(2, 10 * ((2 * t) - 1))
        )
    return 0.5 * (
        math.sin(-13 * math.pi / 2 * ((2 * t - 1) + 1))
        * math.pow(2, -10 * (2 * t - 1))
        + 2
    )


"""
Back Easing Functions
"""


def BackEaseIn(t):
    return t * t * t - t * math.sin(t * math.pi)


def BackEaseOut(t):
    p = 1 - t
    return 1 - (p * p * p - p * math.sin(p * math.pi))


def BackEaseInOut(t):
    if t < 0.5:
        p = 2 * t
        return 0.5 * (p * p * p - p * math.sin(p * math.pi))

    p = 1 - (2 * t - 1)

    return 0.5 * (1 - (p * p * p - p * math.sin(p * math.pi))) + 0.5


"""
Bounce Easing Functions
"""


def BounceEaseIn(t):
    return 1 - BounceEaseOut(1 - t)


def BounceEaseOut(t):
    if t < 4 / 11:
        return 121 * t * t / 16
    elif t < 8 / 11:
        return (363 / 40.0 * t * t) - (99 / 10.0 * t) + 17 / 5.0
    elif t < 9 / 10:
        return (4356 / 361.0 * t * t) - (35442 / 1805.0 * t) + 16061 / 1805.0
    return (54 / 5.0 * t * t) - (513 / 25.0 * t) + 268 / 25.0


def BounceEaseInOut(t):
    if t < 0.5:
        return 0.5 * BounceEaseIn(t * 2)
    return 0.5 * BounceEaseOut(t * 2 - 1) + 0.5


###
### BEGIN FUNCTION FROM FILE: gyro_straight.py
###


def coast(motor_pair):
    motor_pair.set_stop_action('coast')
    motor_pair.stop()

def hold(motor_pair):
    motor_pair.set_stop_action('hold')
    motor_pair.stop()

def brake(motor_pair):
    motor_pair.set_stop_action('brake')
    motor_pair.stop()


def sensed_black(letter_one = 'C', letter_two = 'D'):
    color_sensor_one = ColorSensor(letter_one)
    color_sensor_two = ColorSensor(letter_two)
    color_one = color_sensor_one.get_color()
    color_two = color_sensor_two.get_color()
    if color_one == 'black' or color_two == 'black':
        return True
    else:
        return False

# NOTE - default parameters are evaluated at compile time so we need to set easing to "None" by default and then if it is "None" set our actual default "LinearInOut"
def gyro_straight( left_motor_letter='A', right_motor_letter='B', degrees=9000, start_power=100, end_power=50, easing = None, motor_stop_mode = brake, kp = 0.5, also_stop_if = lambda: False, timeout_seconds = 0 ):
    print("=== Gyro straighting ", degrees)
    # if the user did not specify what easing function they wanted to use then it will just do LinerInOut; a straight line
    if easing is None:
        easing = LinearInOut

    #swap letters if going backwards
    go_fwd = degrees > 0
    left_motor_fwd_letter = left_motor_letter
    right_motor_fwd_letter = right_motor_letter
    if not go_fwd:
        left_motor_fwd_letter = right_motor_letter
        right_motor_fwd_letter = left_motor_letter

    motor_pair = MotorPair(left_motor_fwd_letter, right_motor_fwd_letter)
    motor_left = get_motor_by_letter(left_motor_fwd_letter)
    motor_right = get_motor_by_letter(right_motor_fwd_letter)
    # motor_right.preset(0) will reset the relative degrees because otherwise the second time you run this function the relative degrees will start where it left off last time
    motor_right.preset(0)
    motor_left.preset(0)
    pct_degrees = 0
    t = Timer()
    t.reset()
    #resetting things, setting up hub
    my_hub = PrimeHub()
    my_hub.motion_sensor.reset_yaw_angle()
    #right here we start our motor
    motor_pair.start_tank(start_power, start_power)

    # while true is the same as a forever loop and we just say "return" when we want to exit
    while True:
        speed_right, relative_degrees_right, absolute_degrees_right, pwm_right = motor_right.get()
        speed_left, relative_degrees_left, absolute_degrees_left, pwm_left = motor_left.get()
        speed = (speed_right + speed_left) / 2
        relative_degrees = (abs(relative_degrees_right) + abs(relative_degrees_left)) / 2
        pct_degrees = relative_degrees / degrees
        pct_power = easing(pct_degrees)
        act_power = int(pct_power * (end_power - start_power) + start_power)
        # right now we are getting our yaw angle (our left and right) to see if we have veered off course then we correct our motors to turn.
        # we only turn slighty by kp (how much our robot reacts to being off course) of what we are of by as to not overshoot and then have to correct agian.
        yaw = my_hub.motion_sensor.get_yaw_angle()
        correction = int(yaw * kp)
        motor_pair.start_tank(act_power - correction, act_power + correction)
        # when we arive at our destination we need to stop and exit the loop.
        if timeout_seconds != 0 and t.now() > timeout_seconds:
            print(" timed out at degrees ", relative_degrees, " wanted ", degrees)
            motor_stop_mode(motor_pair)
            return relative_degrees - abs(degrees)
        if also_stop_if() == True or relative_degrees >= abs(degrees):
            motor_stop_mode(motor_pair)
            #return overshoot
            print(" completed degrees ", relative_degrees, " wanted ", degrees)
            return relative_degrees - abs(degrees)




###
### BEGIN FUNCTION FROM FILE: line_follow.py
###

def line_follow( Sspeed=40, Espeed=20, sensorLetter="D", stopIf=None, stopMode='brake', degrees=1000, motorLeftletter = 'A', motorRightletter='B', kp=0.4):

    motor_pair = MotorPair(motorLeftletter, motorRightletter)
    motor1 = Motor(motorLeftletter)
    motor2 = Motor(motorRightletter)

    color = ColorSensor(sensorLetter)
    stop = False
    integral = 0
    lastError = 0

    motor1.set_degrees_counted(0)
    motor2.set_degrees_counted(0)
    if stopMode is not None:
        motor_pair.set_stop_action(stopMode)
    while stop == False:
        mdeg1 = motor1.get_degrees_counted()
        mdeg2 = motor2.get_degrees_counted()
        motordeg = (abs(mdeg1) + abs(mdeg2))/ 2
        if motordeg >= degrees:
            stop = True

        pct = motordeg/degrees

        speedy = get_speed( Sspeed, Espeed, pct )
        # print('speedy', speedy )



        speed = speedy

        error = color.get_reflected_light() - 50
        P_fix = error * kp

        integral = integral + error

        I_fix = integral * 0.001

        derivative = error - lastError
        lastError = error
        D_fix = derivative * 1

        correction = P_fix+I_fix+D_fix

        motor_pair.start_tank_at_power(int(speed+correction), int(speed-correction))

        if stop == True and stopMode is not None:
            motor_pair.stop()


###
### BEGIN FUNCTION FROM FILE: line_square.py
###


def line_square ( speed=40, color_to_hit='black', sensorletterleft='D', sensorletterright='C', motorletterleft='A', motorletterright='B', overshoot_seconds = 0 ):
    print("=== line squaring")
    motors = MotorPair(motorletterleft, motorletterright)
    motors.set_stop_action('brake')
    sensorL = ColorSensor ( sensorletterleft )
    sensorR = ColorSensor ( sensorletterright )
    sensor_left_color = sensorL.get_color()
    sensor_right_color = sensorR.get_color()

    if sensor_right_color != color_to_hit and sensor_left_color != color_to_hit:
        print("neither sensor on color_to_hit, returning...")
        return

    if sensor_right_color == color_to_hit and sensor_left_color == color_to_hit:
        print("both sensors on color_to_hit, returning...")
        return

    if sensor_left_color == color_to_hit:
        leftfirst = True
    else:
        leftfirst = False

    def hit_colorL():
        # print( 'left', sensorL.get_color() )
        return sensorL.get_color() == color_to_hit

    def hit_colorR():
        # print( 'right', sensorR.get_color() )
        return sensorR.get_color() == color_to_hit

    if (leftfirst == True):
        if not hit_colorL ():
            motors.start_tank (speed, 0)
            wait_until (hit_colorL)
        if not hit_colorR ():
            motors.start_tank (0, speed)
            wait_until (hit_colorR)
    else:
        if not hit_colorR ():
            print('A')
            motors.start_tank (0, speed)
            wait_until (hit_colorR)
        if not hit_colorL ():
            print( 'B' )
            motors.start_tank (speed, 0)
            wait_until (hit_colorL)
    ### depending on what angle you hit a black line you have to overshoot with the second sensor to square it
    wait_for_seconds(overshoot_seconds)
    motors.stop()



###
### BEGIN FUNCTION FROM FILE: motor_rotation_functions.py
###

def motor_to_degrees(degrees=90, power=100, port='A'):
    hub_motor = get_motor_by_letter(port)
    hub_motor.preset(0)
    hub_motor.pwm(power)
    degrees_wanted = degrees

    keep_spinning = True
    while keep_spinning:
        speed, relative_degrees, absolute_degrees, pwm = hub_motor.get()
        if relative_degrees >= degrees_wanted:
            keep_spinning = False 
        if keep_spinning == False:
            hub_motor.brake()


###
### BEGIN FUNCTION FROM FILE: party_mode.py
###


def party_mode(color_sensor_one = 'C', color_sensor_two = 'D', party_length = 20):
    from random import random
    cs_one = ColorSensor(color_sensor_one)
    cs_two = ColorSensor(color_sensor_two)
    timer = Timer()
    timer.reset()

    # the first half of the party is random lights at random intensities
    while timer.now() < (party_length/2):
        intensity = int(100 * random())
        light_choice = 6 * random()
        if light_choice <= 1:
            cs_one.light_up(intensity, 0, 0)
        elif light_choice <= 2:
            cs_one.light_up(0, intensity, 0)
        elif light_choice <= 3:
            cs_one.light_up(0, 0, intensity)
        elif light_choice <= 4:
            cs_two.light_up(intensity, 0, 0)
        elif light_choice <= 5:
            cs_two.light_up(0, intensity, 0)
        elif light_choice <= 6:
            cs_two.light_up(0, 0, intensity)
        wait_for_seconds(0.05)
    cs_one.light_up_all(0)
    cs_two.light_up_all(0)
    wait_for_seconds(0.2)

    # the second half of the paty is bright blinking lights
    # at random intervals
    toggle = 1
    while timer.now() < party_length:
        wait_time = random() * 0.25
        cs_one.light_up_all(100 * toggle)
        cs_two.light_up_all(100 * toggle)
        wait_for_seconds(wait_time)
        if toggle == 1:
            toggle = 0
        else:
            toggle = 1

    # turn off the lights at the end of the party
    cs_one.light_up_all(0)
    cs_two.light_up_all(0)



###
### BEGIN FUNCTION FROM FILE: start_run.py
###

def start_run( color_sensor_letter = 'C', delay = 1):
    # color_sensor_letter = 'C' means that the active sensor is on the right side of the robot when it is facing the same direction as you
    color = ColorSensor(color_sensor_letter)
    status_light = StatusLight()
    speaker = Speaker()
    waiting_for_run = True
    while waiting_for_run:
        the_color = color.get_color()
        if the_color == 'red':
            print ( 'Detected:', the_color)
            status_light.on('red')
            speaker.beep(60, delay)
            zz_run_one()
            waiting_for_run = False
        elif the_color == 'green':
            print ( 'Detected:', the_color)
            status_light.on('green')
            speaker.beep(60, delay)
            zz_run_two()
            waiting_for_run = False
        elif the_color == 'blue':
            print ( 'Detected:', the_color)
            status_light.on('blue')
            speaker.beep(60, delay)
            zz_run_four()
            waiting_for_run = False
        elif the_color == 'violet':
            print ( 'Detected:', the_color)
            status_light.on('violet')
            speaker.beep(60, delay)
            zz_run_three()
            waiting_for_run = False
        elif the_color == 'cyan':
            print ( 'Detected:', the_color)
            status_light.on('cyan')
            speaker.beep(60, delay)
            zz_run_five()
            waiting_for_run = False
        else:
            print ('not a run color:', the_color)
            status_light.off()



###
### BEGIN FUNCTION FROM FILE: test_function.py
###

# this is a test function, don't actually use this one
def test_function():
    print("test function")


###
### BEGIN FUNCTION FROM FILE: turn_code.py
###

def get_speed(start, end, percent):
    return int ( start + (end - start)*percent )


def turn_function(degrees=90, easing=None, stoptype='brake',startspeed=40, endspeed=30, motorletterleft='A',also_end_if = None, motorletterright='B',turntype='both', timeout_seconds = 0):
    print("=== Turning ", degrees)

    neg = degrees<0

    hub = PrimeHub()


    hub.motion_sensor.reset_yaw_angle()
    motors = MotorPair(motorletterleft, motorletterright)
    t = Timer()
    t.reset()
    keep_spinning = True
    while keep_spinning == True:
        degrees_now= hub.motion_sensor.get_yaw_angle()
        if neg and degrees_now <= degrees :
            print("  completed turn at degree ", degrees_now)
            keep_spinning = False
        elif not neg and degrees_now >= degrees :
            print("  completed turn at degree ", degrees_now)
            keep_spinning = False
        if also_end_if is not None and also_end_if():
            print("  completed with end_if at degree ", degrees_now)
            keep_spinning=False

        if timeout_seconds != 0 and t.now() > timeout_seconds:
            keep_spinning = False
        if also_end_if is not None and also_end_if():
            keep_spinning=False
        if keep_spinning:
            pct_degrees = degrees_now/degrees
            pct_power = pct_degrees
            
            

            if easing is not None:
                pct_power = easing(pct_degrees)
            speed = get_speed (startspeed, endspeed, pct_power)

            if turntype is 'both':
                if neg:
                    motors.start_tank_at_power(-speed, speed)
                else:
                    motors.start_tank_at_power(speed, -speed)
            elif turntype is 'left':
                if neg:
                    motors.start_tank_at_power(-speed, 0)
                else:
                    motors.start_tank_at_power(speed, 0)
            elif turntype is 'right':
                if neg:
                    motors.start_tank_at_power(0,speed)
                else:
                    motors.start_tank_at_power(0,-speed)


    if stoptype is not None:
        motors.set_stop_action( stoptype )
        motors.stop()



###
### BEGIN FUNCTION FROM FILE: utillity_functions.py
###

def get_motor_by_letter(port):
    if port ==  'A':
        return hub.port.A.motor
    if port == 'B':
        return hub.port.B.motor
    if port == 'C':
        return hub.port.C.motor
    if port == 'D':
        return hub.port.D.motor
    if port == 'E':
        return hub.port.E.motor
    if port == 'F':
        return hub.port.F.motor


###
### BEGIN FUNCTION FROM FILE: zz_run_five.py
###

### this will put the mission model and energy into the middle and go to the right side of the board. This is the last run
def zz_run_five():
    gyro_straight( left_motor_letter='A', right_motor_letter='B', degrees=1640, start_power=100, end_power=40, easing = None, motor_stop_mode = brake, kp = 0.5, timeout_seconds = 0 )
    control_attachments(start_speed=50, end_speed=50, ease=None, degrees_wanted=580, also_end_if = None, motor_stop_mode='BRAKE', motor_letter='F', timeout_seconds = 0)
    gyro_straight( left_motor_letter='A', right_motor_letter='B', degrees=300, start_power=50, end_power=50, easing = None, motor_stop_mode = brake, kp = 0.5, timeout_seconds = 0 )
    turn_function(degrees=75, easing=None, stoptype='brake',startspeed=20, endspeed=20, motorletterleft='A',also_end_if = None, motorletterright='B',turntype='both', timeout_seconds = 0)
    gyro_straight( left_motor_letter='A', right_motor_letter='B', degrees=720, start_power=50, end_power=50, easing = None, motor_stop_mode = brake, kp = 0.5, timeout_seconds = 0 )
    turn_function(degrees=-45, easing=None, stoptype='brake',startspeed=20, endspeed=20, motorletterleft='A',also_end_if = None, motorletterright='B',turntype='both', timeout_seconds = 0)
    gyro_straight( left_motor_letter='A', right_motor_letter='B', degrees=1100, start_power=50, end_power=50, easing = None, motor_stop_mode = brake, kp = 0.5, timeout_seconds = 0 )


###
### BEGIN FUNCTION FROM FILE: zz_run_four.py
###

def zz_run_four():
    sensorL = ColorSensor ( 'D' )
    sensorR = ColorSensor ( 'C' )
    def see_black_left():
        return sensorL.get_color() is 'black'
    def see_black_right():
        return sensorR.get_color() is 'black'

    gyro_straight(degrees=1000, start_power=50, end_power=50, also_stop_if=see_black_left, kp=1)
    line_follow(degrees=750, stopIf=see_black_right)
    turn_function(degrees=-5, turntype='left', timeout_seconds=1, startspeed=40, endspeed=40)
    gyro_straight(degrees=400, start_power=100, end_power=100, timeout_seconds=3)
    control_attachments(degrees_wanted=-100, start_speed=100, end_speed=100, motor_letter='E', timeout_seconds=1)
    control_attachments(degrees_wanted=-150 ,start_speed=70, end_speed=70, motor_letter='F', timeout_seconds=1)
    gyro_straight(degrees=-400, start_power=40, end_power=40)
    turn_function(degrees=25, turntype='left', startspeed=40, endspeed=40)
    gyro_straight(degrees=-2000, start_power=100, end_power=100, kp=2)


###
### BEGIN FUNCTION FROM FILE: zz_run_one.py
###




def zz_run_one():
    sensorL = ColorSensor ( 'D' )
    sensorR = ColorSensor ( 'C' )
    #start fast, arrive slow -> expo-in-out!
    gyro_straight(degrees = 900, start_power = 70, end_power = 60, easing=ExponentialEaseInOut, motor_stop_mode = brake, kp=2,)
    #back up from tv
    gyro_straight(degrees = -160, start_power = 30, end_power = 25, kp=0)
    #orient the robot towards windmill T
    turn_function(degrees = -45, easing = ExponentialEaseInOut, stoptype = 'brake', startspeed = 30, endspeed = 30, turntype = 'right')
    #move toward front of windmill
    gyro_straight(degrees = 720, start_power = 100, end_power = 30, kp=0.5, easing = ExponentialEaseInOut)
    #spin to face windmill head on
    turn_function(degrees=65, easing=ExponentialEaseOut, stoptype='brake', startspeed=50, endspeed=40, turntype = 'both')
    #charge at the windmill! hope we funnel onto it
    gyro_straight(degrees = 320, start_power = 50, end_power = 50, kp=0.5)
    #snag the energies
    t = Timer()
    control_attachments(start_speed=80, end_speed=80, degrees_wanted=1150, motor_letter = 'E', timeout_seconds = 3)
    wait_for_seconds(.5)
    control_attachments(start_speed=80, end_speed=80, degrees_wanted= -1150, motor_letter = 'E', timeout_seconds = 3)
    wait_for_seconds(.5)
    control_attachments(start_speed=80, end_speed=80, degrees_wanted=1150, motor_letter = 'E', timeout_seconds = 3)
    wait_for_seconds(.5)
    control_attachments(start_speed=80, end_speed=80, degrees_wanted= -1150, motor_letter = 'E', timeout_seconds = 3)
    #back up from windmill
    gyro_straight(degrees=-255, start_power=20, end_power=20, easing=ExponentialEaseInOut, kp=0)
    # moves the arm to not hit the toy factory
    control_attachments(start_speed=80, end_speed=80, degrees_wanted=550, motor_letter = 'E',)
    gyro_straight(degrees=-355, start_power=20, end_power=20, easing=ExponentialEaseInOut, kp=0)
    #move back to the base so we can prepare it to do something else
    turn_function(degrees=90, easing=ExponentialEaseOut, stoptype='brake', startspeed=50, endspeed=40, turntype = 'both')
    gyro_straight(degrees = 1300, start_power = 60, end_power = 60, kp=0.5)
    control_attachments(start_speed=80, end_speed=80, degrees_wanted= -1150, motor_letter = 'E', timeout_seconds = 2)




###
### BEGIN FUNCTION FROM FILE: zz_run_three.py
###


def zz_run_three():
    sensorL = ColorSensor ( 'D' )
    sensorR = ColorSensor ( 'C' )
    def see_black_either():
        return sensorL.get_color() is 'black' or sensorR.get_color() is 'black'
    def see_black_left():
        return sensorL.get_color() is 'black'
    def see_black_right():
        return sensorR.get_color() is 'black'
    def see_white_left():
        return sensorL.get_color() is 'white'
    def see_white_either():
        return sensorR.get_color() is 'white'or sensorL.get_color() is 'white'
    def see_white_right():
        return sensorR.get_color() is 'white'

    #from start position, move to middle of field
    gyro_straight(degrees=1700, start_power=40, end_power=40, kp=0.5)
    wait_for_seconds(1)
    turn_function(degrees=30, startspeed=30, endspeed=30)
    wait_for_seconds(1)
    gyro_straight(degrees=500, timeout_seconds=2, start_power=60, end_power=60)
    wait_for_seconds(1)
    turn_function(degrees=25, startspeed=30, endspeed=30)
    wait_for_seconds(1)
    gyro_straight(degrees=700, start_power=70, end_power=40, kp=0.5, timeout_seconds=2)
    gyro_straight(degrees=-150, start_power=40, end_power=40)
    control_attachments(motor_letter="E", start_speed=100, end_speed=100, degrees_wanted=-2700)
    control_attachments(motor_letter="E", start_speed=100, end_speed=100, degrees_wanted=2700)
    gyro_straight(degrees=-100, start_power=40, end_power=40)
    # knock out water
    turn_function(degrees=-45, startspeed=30, endspeed=30)
    #line back up
    turn_function(degrees=45, startspeed=30, endspeed=30)
    # keep backin up
    gyro_straight(degrees=-50, start_power=40, end_power=40)
   
    turn_function(degrees=-45, startspeed=30, endspeed=30)
    gyro_straight(degrees=1000, start_power=40, end_power=40, also_stop_if=see_black_left)
    line_follow(degrees=600, stopIf=see_black_right)
    for i in range(3):
        gyro_straight(degrees=360, start_power=40, end_power=40, timeout_seconds=1)
        gyro_straight(degrees=-180, start_power=40, end_power=40, timeout_seconds=1)
    turn_function(degrees=-45, startspeed=30, endspeed=30)
    gyro_straight(degrees=1800, start_power=100, end_power=100)
    control_attachments(motor_letter="E", start_speed=100, end_speed=100, degrees_wanted=-2700)




###
### BEGIN FUNCTION FROM FILE: zz_run_two.py
###

def zz_run_two():
    ### dumps the energy into the toy factory
    gyro_straight( left_motor_letter='A', right_motor_letter='B', degrees=900, start_power=50, end_power=50, easing = None, motor_stop_mode = brake, kp = 0.5)
    gyro_straight( left_motor_letter='A', right_motor_letter='B', degrees=-1000, start_power=50, end_power=50, easing = None, motor_stop_mode = brake, kp = 0.5)

###
### FUNCTION DEFINITIONS
###
# (control_attachments.py) def control_attachments(start_speed=40, end_speed=100, ease=None, degrees_wanted=720, also_end_if = None, motor_stop_mode='BRAKE', motor_letter='C', timeout_seconds = 0):
# (gyro_straight.py) def coast(motor_pair):
# (gyro_straight.py) def hold(motor_pair):
# (gyro_straight.py) def brake(motor_pair):
# (gyro_straight.py) def sensed_black(letter_one = 'C', letter_two = 'D'):
# (gyro_straight.py) def gyro_straight( left_motor_letter='A', right_motor_letter='B', degrees=9000, start_power=100, end_power=50, easing = None, motor_stop_mode = brake, kp = 0.5, also_stop_if = lambda: False, timeout_seconds = 0 ):
# (line_follow.py) def line_follow( Sspeed=40, Espeed=20, sensorLetter="D", stopIf=None, stopMode='brake', degrees=1000, motorLeftletter = 'A', motorRightletter='B', kp=0.4):
# (line_square.py) def line_square ( speed=40, color_to_hit='black', sensorletterleft='D', sensorletterright='C', motorletterleft='A', motorletterright='B', overshoot_seconds = 0 ):
# (motor_rotation_functions.py) def motor_to_degrees(degrees=90, power=100, port='A'):
# (start_run.py) def start_run( color_sensor_letter = 'C', delay = 1):
# (turn_code.py) def get_speed(start, end, percent):
# (turn_code.py) def turn_function(degrees=90, easing=None, stoptype='brake',startspeed=40, endspeed=30, motorletterleft='A',also_end_if = None, motorletterright='B',turntype='both', timeout_seconds = 0):
# (utillity_functions.py) def get_motor_by_letter(port):
# (zz_run_five.py) def zz_run_five():
# (zz_run_four.py) def zz_run_four():
# (zz_run_one.py) def zz_run_one():
# (zz_run_three.py) def zz_run_three():
# (zz_run_two.py) def zz_run_two():


### Run 1: Red
### Run 2: Green
### Run 3: Violet (light pink-purple)
### Run 4: Blue
### Run 5: Cyan (light blue)

start_run()

