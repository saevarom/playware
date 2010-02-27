def OpenRSCom(int baud, string port):
    try:
        m_ComIsOpen = BlindOpen(port, baud, 0);
        if m_ComIsOpen:
            this.m_rs232recbuff = new byte[0x400]  #Need to find out what this does...
            this.m_rs232sb = 0
            this.m_rs232eb = 0
			return m_ComIsOpen
    except:
        return false

def BlindOpen(port, baud, parity):
    return (checkSettings(port, baud, parity) and OpenPort(port, baud, parity))

def checkSettings:
	if (((len(port) > 0) and (baud > 0)) and ((parity >= 0) and (parity < 3))):
		return true
	else:
		return false

#OpenPort is next...

 


 

 

 
