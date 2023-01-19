import pymem, time

#noclip value               ::   0.0003051850945 
#noclip overwritten value   ::  -1

byte_sig = b"\\x40\\x01\\xA0\\x39\\x40\\x01\\xA0\\x39\\x40\\x01\\xA0\\x39\\x40\\x01\\xA0\\x39\\xCD\\xCC\\x4C\\x3D\\xCD\\xCC\\x4C\\x3D\\xCD\\xCC\\x4C\\x3D\\xCD\\xCC\\x4C\\x3D"

speed_x = 0x80
speed_y = 0x84
speed_w = 0x88
gamespeed = 0x8C

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

try:
    pm = pymem.Pymem("RainbowSix.exe") 
    print(f"[+] Game Found, PID:", pm.process_id)
except:
    print("[-] Open Rainbow Six, Failed to find game.")

def getNoclipValue(addr) -> int:
    return pm.read_float(addr)



def doNoclip(): 

    try:
        print("[~] Pattern Scanning...")
        noclip_addrs = pattern_scan_all(pm.process_handle, byte_sig, return_multiple=True)
    except:
        print("[-] Scan Failed.")
        
         
    if noclip_addrs:
        for addr in noclip_addrs:
            print(f"->", hex(addr))
            print(f"Addr 1 (Pre) - ", getNoclipValue(addr))
            pm.write_float(addr, (float)(-1))
            print(f"Addr 1 (Post) - ", getNoclipValue(addr))
        
    time.sleep(15)
    doNoclip()
    
def doSpeed():
    try:
        print("[~] Pattern Scanning...")
        speed_addrs = pattern_scan_all(pm.process_handle, byte_sig, return_multiple=True)
    except:
        print("[-] Scan Failed.")
        
         
    if speed_addrs:
        for addr in speed_addrs:
            speed_x1 = addr + speed_x
            print(f"->", hex(addr))
            print("nigga", hex(speed_x1))
        

doSpeed()