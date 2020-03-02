# *** for unresolved

import time
from tkinter import *
import requests
import random
import math
import json
# *** use python json library, json.loads() function
# netstat -lnp | tcp, find port number of node application
# in janakj directory, ut, file api.mj explains format expectations of parameters etc


BANDWIDTH = 10 ** 5    # *** could just set to some number, and subtract quality from it every TIME_DIF?
                       # also have parameter link bit rate (bits/s), sets upper bound for bitrate
                       # (which opus changes depending on packet loss)
TIME_DIF = 2    # how often audio quality can be changed
START_QUALITY = 10    # starting quality
PROTOCOL_DOMAIN_PORT = "http://nist.ryngle.net:80"
CODEC = "opus"

"""
"codec":"opus", rfc: https://tools.ietf.org/html/rfc6716, wikipedia: https://en.wikipedia.org/wiki/Opus_(audio_format)
~ middle ground between wideband and phone-like
~ should yield good range of qualities
~ audio bandwidth : 6 kbit/s to 510 kbit/s, *** cannot change audio quality on application? 

Application:
    ~ "codec":"opus"
    ~ "packet_time":{10, 20, 30, 40, 50, 60}, will fix at 20
    ~ "mic_level":[0,100]
    ~ "speaker_level":[0,100]

    ~ "noise":null 
    ~ "noise_level":0

    ~ "tx_loss":[0,100], |101|, packet loss rate (%)
    ~ "tx_error":[0,100], |101|, packet corruption rate (%)

    # use one, tx_delay
    ~ "tx_delay":[0,2000] # transmit delay (ms)
    ~ "rx_delay":0 [0,2000] # receive delay (ms)
"""


"""
for "codec":"opus", which will be default
quality:[0,10], dictates quality of audio
dif:[True, False], indicates whether quality has been changed (and thus several parameters need to be altered) 
init:[True, False], indicates whether this is initialising call (set all parameters)
"""
def opus_json(quality, dif, init):

    json_data = "{"

    if init:
        # initialise all parameters which will not otherwise have a value set

        # codec
        json_data += "\"codec\":\"" + CODEC + "\","

        # packet_time
        json_data += "\"packet_time\":20,"

        # noise
        json_data += "\"noise\":null,"

        # noise_level
        json_data += "\"noise_level\":0,"

    if dif:
        # change all quality related parameters

        # tx_loss
        loss_and_corrupt = 5 * math.ceil((10-quality)/2)    # function mapping to values in excel # *** quality / 2 removed
        json_data += "\"tx_loss\":" + str(loss_and_corrupt) + ","

        # tx_error
        json_data += "\"tx_error\":" + str(loss_and_corrupt) + ","

        # tx_delay
        json_data += "\"tx_delay\":" + str((10 - quality) * 20) + "," # 300 ms -> stuttering # *** (10 - quality) * 30 changed to * 20

    # always alter mic_level and speaker_level
    u = random.random()    # sample random number from 0-1 uniform distribution
    p = quality * 0.1
    #"""
    if u <= p:
        json_data += "\"mic_level\":100,"
        json_data += "\"speaker_level\":100,"
    else:
        level = random.randint(quality * 10, 100)
        json_data += "\"mic_level\":" + str(level) + ","
        json_data += "\"speaker_level\":" + str(level) + ","
    #"""

    json_data = json_data[0:-1] + "}"    # removes last comma

    # POST desired settings
    headers = {"Content-Type": "application/json"}
    r1 = requests.post(url=PROTOCOL_DOMAIN_PORT+"/proxy/User-Terminal-[ut1-92cb01]._ut._tcp/api/settings",
                       data=json_data,
                       headers=headers)
    r2 = requests.post(url=PROTOCOL_DOMAIN_PORT+"/proxy/User-Terminal-[ut2-5dd34e]._ut._tcp/api/settings",
                       data=json_data,
                       headers=headers)

    # cause desired settings to be activated
    r1_activate = requests.post(url=PROTOCOL_DOMAIN_PORT+"/proxy/User-Terminal-[ut1-92cb01]._ut._tcp/api/settings/apply")
    r2_activate = requests.post(url=PROTOCOL_DOMAIN_PORT+"/proxy/User-Terminal-[ut2-5dd34e]._ut._tcp/api/settings/apply")

    if r1_activate.status_code == 200 and r2_activate.status_code == 200:
        print("Update to quality " + str(quality) + " successful.")
        print(json_data)
    else:
        print("Update to quality " + str(quality) + " unsuccessful." +
              "Request 1 status code: " + str(r1_activate.status_code) +
              ", Request 2 status code: " + str(r2_activate.status_code))


if __name__ == "__main__":

    # default set up
    opus_json(START_QUALITY, True, True)

    rem_bandwidth = BANDWIDTH

    # make scale
    root = Tk()
    var = IntVar(value=START_QUALITY)
    var_prev = var.get()
    scale = Scale(root, from_=10, to_=0, variable=var)
    scale.pack(anchor=CENTER)

    while rem_bandwidth > 0:
        #rem_bandwidth -= var.get()  # *** current: quality, want: bandwidth of quality
        t1 = time.time()
        t2 = t1

        while rem_bandwidth > 0 and t2 - t1 < TIME_DIF:
            root.update()
            t2 = time.time()

        root.update()
        if var_prev != var.get():
            # change quality
            opus_json(var.get(), True, False)
            print(str(var_prev) + " -> " + str(var.get()))
            var_prev = var.get()
        elif var.get() != 10:
            # change only mic_level and speaker_level since quality not perfect
            opus_json(var.get(), False, False)
