import asyncio
#import aiokwikset
from aiokwikset import API
import json
from gmailtest import *
import time
import requests
import urllib.parse

async def main() -> None:
    """Run!"""
    #initialize the API
    api = API("ljzimmerphone@gmail.com")

    #start auth
    #<CODE_TYPE> = [phone, email]
    pre_auth = await api.authenticate('Lisa1103!','email')
    time.sleep(15)
    the_code = get_code("ljzimmerphone@gmail.com", "from:kwikset-no-reply@goconcourse.com")
    print(the_code)
    #MFA verification
    await api.verify_user(pre_auth, the_code)

    # Get user account information:
    user_info = await api.user.get_info()

    # Get the homes
    homes = await api.user.get_homes()
    #print("homes are:  " + homes[0])
    print("id is:  " + homes[0]['homeid'])
   

    # Get the devices for the first home
    devices = await api.device.get_devices(homes[0]['homeid'])
    #print(devices)
    
    #delete_message(myserv, user, theid)
    y = json.dumps(devices)
    y = y.replace("'", "\"")
    y = y.replace("true", "\"TRUE\"")
    y = y.replace("false", "\"FALSE\"")
    z = json.loads(y)
    #print(z)
    print("posting json to HomeSeer")
    
    #headers = {'Content-type': 'application/json'}
    i = 0
    
    for x in z:
        #print(x)
        port = i + 8093
        print(port)
        w = json.dumps(x)
        u = json.loads(w)
        
        devname = u['devicename']
        convname = devname.replace(" ","%20")
        lstat = u['lockstatus']
        lbatt = u['batterypercentage']
        strbatt = str(lbatt)
        strport = str(port)
        bhalf = '?name=' + devname
        #url = 'http://192.168.17.59:8088/myjson.asp'
        #url = 'http://192.168.17.59:8088/myjson.asp?name=' + devname + '&status=' + lstat +'&batt='+ lbatt
        #url = 'http://192.168.17.59:8088/myjson.asp?name=' + devname + '&status=' + lstat
        #url = 'http://192.168.17.59:' + strport + '/myjson.asp?name=' + convname + '&status=' + lstat +'&batt='+ strbatt
        url = 'http://192.168.17.59:' + strport + '/myjson.asp?name=' + convname
        #myobj = {'name': devname, 'status': lstat ,'battlevel' : lbatt }
        #eurl = urllib.parse.quote_plus(bhalf)
        #nurl = url + eurl
        #print(url)
        #x = requests.post(url)
        x = requests.post(url, json=x)
        print(x.text)
        i = i + 1


    
    #r = requests.post('http://192.168.17.59:8088/myjson.asp', json=z) 
    #print(f"Status Code: {r.status_code}, Response: {r.json()}")
    
    

    # Get information for a specific device
    #device_info = await api.device.get_device_info(devices[0]['deviceid'])

    # Lock the specific device
    #lock = await api.device.lock_device(device_info, user_info)

    # Set led status
    #led = await api.device.set_ledstatus(device_info, "false")

    # Set audio status
    #audio = await api.device.set_audiostatus(device_info, "false")

    # Set secure screen status
    #screen = await api.device.set_securescreenstatus(device_info, "false")


asyncio.run(main())
