# Clare DuVal
# CPSC 4720, Spring 2021
# Productivity Project Part B

from tkinter import *
from tkinter import messagebox
import os, time, sys, threading
from pynput.keyboard import Key, Listener

root = Tk()
root.title("Pomodoro")
root.geometry("800x100")
  
time_str=StringVar()
words_str=StringVar()

#Timers in min
work_timer = 25 
break1_timer = 5 
break2_timer = 15 
s_num = 0
key_num = 0
tot_sec = 0

# Min and Sec labels
timeLabel= Label(root, width=45, font=("Monaco",18,"") ,
                   foreground="white",
                   background="black",
                   textvariable=time_str)
timeLabel.pack(side = TOP)
time_str.set("click 'clock in' to begin the application")
wordsLabel= Label(root, width=45, font=("Monaco",18,"") ,
                   foreground="white",
                   background="black",
                   textvariable=words_str)
wordsLabel.pack(side = TOP)
words_str.set("{0:2d} min".format(work_timer)+" "+"{0:2d} sec".format(0))

# Run a given timer 
def run_timer(mins, alarm, label):
    seconds = mins * 60
    global on
    time_str.set(label)
    while seconds >= 0 and on:
             
            # divmod(firstvalue = temp//60, secondvalue = temp%60)
            mins,secs = divmod(seconds,60) 
      
            # using format () method to store the value up to 
            # two decimal places
            words_str.set("{0:2d} min".format(mins)+" "+"{0:2d} sec".format(secs))
      
            # updating the GUI window after decrementing the
            # temp value every time
            root.update()
            time.sleep(1)
      
            # when temp value = 0; then a messagebox pop's up
            # with a message:"Time's up"
            if seconds == 0:
                os.system("""
                          osascript -e 'display notification "{}" with title "{}"'
                          """.format(alarm, "Pomodoro"))
                os.system('afplay /System/Library/Sounds/Sosumi.aiff')
            seconds -= 1
            global tot_sec
            tot_sec += 1
        
            
# Rotational timers
def timer():
    
    global btn
    btn.config(command=exit)
    btn.config(text="clock out")
    global tot_sec 
    tot_sec = 0
    while True:
        run_timer(work_timer, "Break time!", "Work time remaining:")
        run_timer(break1_timer, "Back to work!", "Break time remaining:")
        run_timer(work_timer, "Break time!", "Work time remaining:")
        run_timer(break1_timer, "Back to work!", "Break time remaining:")
        run_timer(work_timer, "Break time!", "Work time remaining:")
        run_timer(break2_timer, "Back to work!", "Break time remaining:")

def leave():
    os.execv(__file__, sys.argv)        
  
# Restart application on clock out          
def exit():
    
    global s_num
    mins,secs = divmod(tot_sec,60) 
    hours, mins = divmod(mins,60) 
    a = "Time elapsed: " + str(hours) + " hours, " + str(mins) + " minutes, " + str(secs) + " seconds"
    b = " \nWords typed: " + str(s_num+1)
    
    os.system("""
              osascript -e 'display notification "{}" with title "{}"'
              """.format(a + b, "Pomodoro"))
    os.system('afplay /System/Library/Sounds/Sosumi.aiff')
    
    #global btn
    #btn.destroy()
    
    
    time.sleep(10000)
    
    
    
    return False


def on_press(key):
    global s_num
    global key_num
    if str(key) == 'Key.space':
        s_num = s_num + 1
    elif str(key) == 'Key.backspace':
        key_num = key_num - 1
    elif (str(key)).isalnum: 
        key_num = key_num + 1
    
    
def on_release(key):
    if key == Key.esc:
        # Stop listener
        return False


def read_screen():
    ls =  Listener(on_press=on_press, on_release=on_release)
    ls.start()
        

def main_loop():
    root.mainloop()
    
def main():
    
    global on
    on = True
    
    # Button Widget
    global btn
    btn = Button(root, text="clock in", bd='5', 
                 highlightbackground = "black",
                 command= timer)
    btn.pack(side=BOTTOM)
  
    # Run Application
    root.configure(background='black')
    
    x = threading.Thread(target=main_loop, args=())
    y = threading.Thread(target=read_screen, args=())
    
    y.start()
    x.run()
    

if __name__ == '__main__':
    main()
    