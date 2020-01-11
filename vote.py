### Import libraries
from datetime import datetime
import json
import iota
import sys
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from time import sleep

#Select GPIO mode
GPIO.setmode(GPIO.BCM)

#Set buzzer - pin 23 as output
buzzer=23 
GPIO.setup(buzzer,GPIO.OUT)

### IOTA address
IOTAAddr = b"QBSETYBUTTJCI9SDVQNHWGPXTRN9HPHXCQUFETVHJ9EAMK9TISAJOAVMKSYOJILCDLBZHMGQTXZVWFIGCYHWZYFEAY"

### IOTA full node
api = iota.Iota("https://nodes.thetangle.org:443")

project = "Voting via RFID"
reader = SimpleMFRC522()

try:
    while True:
        print("\nIOTA Project Voting")
        
### only yes or no allowed
        while True:
           casted_vote = input("\nCast your vote (YES/NO) and hit Enter: ").lower()
           if casted_vote == "yes":
               print("You voted YES")
               break
           elif casted_vote == "no":
               print("You voted NO")
               break   
        
        print("\nThank you, now hold your ID card near the reader")       
        id, text = reader.read()
        data = {'tagID': str(id), 'tagText':str(text), 'project': project, 'casted_vote': casted_vote}
        
        pt = iota.ProposedTransaction(address = iota.Address(IOTAAddr),
                                      message = iota.TryteString.from_unicode(json.dumps(data)),
                                      tag     = iota.Tag(b'IOTA999RFID999VOTE'),
                                      value   = 0)
        GPIO.output(buzzer,GPIO.HIGH)
        sleep(0.1) # Delay in seconds
        GPIO.output(buzzer,GPIO.LOW)
        sleep(0.1)
        print("\nID card detected...Sending transaction...Please wait...")

        FinalBundle = api.send_transfer(depth=3, transfers=[pt], min_weight_magnitude=14)['bundle']
   
        print("\nTransaction sucessfully recorded")
        
	#bundle is broadcasted, let's print it
        print("\nBundle hash: %s" % (FinalBundle.hash))
        break
                
finally:
     GPIO.cleanup()

