#!/usr/bin/python
import sys
import re
import usb.core
import usb.util
# decimal vendor and product values
dev = usb.core.find(idVendor=0x0477, idProduct=0x5620)
# first endpoint
interface = 0
endpoint = dev[0][(0,0)][0]
# if the OS kernel already claimed the device, which is most likely true
# thanks to http://stackoverflow.com/questions/8218683/pyusb-cannot-set-configuration
if dev.is_kernel_driver_active(interface) is True:
  # tell the kernel to detach
  dev.detach_kernel_driver(interface)
  # claim the device
  usb.util.claim_interface(dev, interface)
stopflag = 1
collected = 0
dev.write(1, sys.argv[1], 0) #, 100)
strout = ''
while stopflag:
    try:
        data = dev.read(endpoint.bEndpointAddress,endpoint.wMaxPacketSize)
        collected += 1
        #print data
	sret = ''.join([chr(x) for x in data])
	#print sret
	if sret == '|1|2|':
		stopflag = 0
	else:
		if collected > 1:
			strout += ', ' + sret
		else:
			strout += sret

    except usb.core.USBError as e:
        data = None
        if e.args == ('Operation timed out',):
            continue
print strout
# release the device
usb.util.release_interface(dev, interface)
# reattach the device to the OS kernel
dev.attach_kernel_driver(interface)
