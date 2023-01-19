from tkinter import *
import pymem, time

from threading import Thread

def pattern_scan_all(handle, pattern, *, return_multiple=False):
    next_region = 0
    found = []
    while next_region < 0x7FFFFFFF0000:
        next_region, page_found = pymem.pattern.scan_pattern_page(
            handle,
            next_region,
            pattern,
            return_multiple=return_multiple
        )
        if not return_multiple and page_found:
            return page_found
        if page_found:
            found += page_found
    if not return_multiple:
        return None
    return found

byte_sig = b"\\x40\\x01\\xA0\\x39\\x40\\x01\\xA0\\x39\\x40\\x01\\xA0\\x39\\x40\\x01\\xA0\\x39\\xCD\\xCC\\x4C\\x3D\\xCD\\xCC\\x4C\\x3D\\xCD\\xCC\\x4C\\x3D\\xCD\\xCC\\x4C\\x3D"


### OFFSET DEFINITION

speed_x = 0x80 # speed x
speed_y = 0x84 # speed y
speed_w = 0x88 # levitation [-1]

speed_float = 0.6000000238418579


class Memory:
    memoryhandle = pymem.Pymem("RainbowSix.exe") 
    print(memoryhandle.process_id)
    address = pattern_scan_all(memoryhandle.process_handle, byte_sig, return_multiple=True)
    for addr in address:
        print("Address: ", hex(addr))
    
    
    def updateMemory(self):
        try:
            print("Updating Memory...")
            self.memoryhandle = pymem.Pymem("RainbowSix.exe") 
            self.address = pattern_scan_all(self.memoryhandle.process_handle, byte_sig, return_multiple=True)
            print("Updated Memory")
            for addr in self.address:
                print("Address: ", hex(addr))
        except:
            print("Failed to update memory..")
            
    def updateThread(self):
        while True:
            self.updateMemory()
            time.sleep(15)
        
Mem = Memory()

 ## WINDOW SETUP

window = Tk()
window.title("cp lover")
window.geometry('1000x1000')
window.maxsize(1000, 1000)



#---------------------------



## FUNCTION DEFINITION



def doNoclip():  
    try:
        if Mem.address:
            for addr in Mem.address:
                print(f"Noclip (Pre) - ", Mem.memoryhandle.read_float(addr))
                Mem.memoryhandle.write_float(addr, (float)(-1))
                print(f"Noclip (Post) - ", Mem.memoryhandle.read_float(addr))
    except:
        print("error trying to write float")
        
def doNograv():
    try:
        if Mem.address:
            for addr in Mem.address:
                print(f"FloatW (Pre) - ", Mem.memoryhandle.read_float(addr+speed_w))
                Mem.memoryhandle.write_float(addr+speed_w, (float)(-1))
                print(f"FloatW (Post) - ", Mem.memoryhandle.read_float(addr+speed_w))
    except:
        print("error trying to write float")     

def doGrav():
    if Mem.address:
        for addr in Mem.address:
            print(f"FloatW (Pre) - ", Mem.memoryhandle.read_float(addr+speed_w))
            Mem.memoryhandle.write_float(addr+speed_w, (float)(0.6000000238418579))
            print(f"FloatW (Post) - ", Mem.memoryhandle.read_float(addr+speed_w))

def setSpeed():
    print(speed_float)
#------------------------------

def setupWindow():
    btn = Button(window, text="Noclip", command=doNoclip)
    btn.grid(column=0, row=0)

    btn1 = Button(window, text="Disable Gravity", command=doNograv)
    btn1.grid(column=0, row=3)

    btn2 = Button(window, text="Enable Gravity", command=doGrav)
    btn2.grid(column=0, row=4)

    refreshbtn = Button(window, text="Refresh Sig", command=Mem.updateMemory)
    refreshbtn.grid(column=0, row=5)
    
    slider = Scale(window, from_=0.55, to=50.0, resolution=0.05, orient=HORIZONTAL, length=300)
    slider.grid(column=0, row=1)
    
    def getSpeed() -> float:
        return slider.get()
    
    def setSpeed():
        try:
            if Mem.address:
                for addr in Mem.address:
                    print(f"SpeedX (Pre) - ", Mem.memoryhandle.read_float(addr+speed_x))
                    print(f"SpeedY (Pre) - ", Mem.memoryhandle.read_float(addr+speed_y))
                    Mem.memoryhandle.write_float(addr+speed_x, (float)(getSpeed()))
                    Mem.memoryhandle.write_float(addr+speed_y, (float)(getSpeed()))
                    print(f"SpeedX (Post) - ", Mem.memoryhandle.read_float(addr+speed_x))
                    print(f"SpeedY (Post) - ", Mem.memoryhandle.read_float(addr+speed_y))
        except:
            print("error trying to write float")  
    
    setspeed = Button(window, text="Set Speed", command=setSpeed)
    setspeed.grid(column=0, row=2)



## MAIN LOOP ( DONT CHANGE )

setupWindow()

window.mainloop()
