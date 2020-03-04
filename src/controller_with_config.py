import time
from tkinter import *
import requests
import random
import math

BANDWIDTH = 10 ** 5    # *** redundant right now, may just do as a function of total quality
TIME_DIF = 2    # how often audio quality can be changed
START_QUALITY = 10    # starting quality
PROTOCOL_DOMAIN_PORT = "http://nist.ryngle.net:80"
CODEC = "opus"

f = open("C:\\Users\\Omer Baddour\\PycharmProjects\\ResearchV3\\config.txt", "r")
data_list = []
lines = f.readlines()
for line in lines:
    data_list.append(line.split())


def opus_json(quality):

    # fetch json_data from data_list, from config.txt
    json_data = data_list[quality][1]
    headers = {"Content-Type": "application/json"}
    r1 = requests.post(url=PROTOCOL_DOMAIN_PORT + "/proxy/User-Terminal-[ut1-92cb01]._ut._tcp/api/settings",
                       data=json_data,
                       headers=headers)
    r2 = requests.post(url=PROTOCOL_DOMAIN_PORT + "/proxy/User-Terminal-[ut2-5dd34e]._ut._tcp/api/settings",
                       data=json_data,
                       headers=headers)

    # cause desired settings to be activated
    r1_activate = requests.post(
        url=PROTOCOL_DOMAIN_PORT + "/proxy/User-Terminal-[ut1-92cb01]._ut._tcp/api/settings/apply")
    r2_activate = requests.post(
        url=PROTOCOL_DOMAIN_PORT + "/proxy/User-Terminal-[ut2-5dd34e]._ut._tcp/api/settings/apply")

    if r1_activate.status_code == 200 and r2_activate.status_code == 200:
        print("Update to quality " + str(quality) + " successful.")
        print(json_data)
    else:
        print("Update to quality " + str(quality) + " unsuccessful." +
              "Request 1 status code: " + str(r1_activate.status_code) +
              ", Request 2 status code: " + str(r2_activate.status_code))


if __name__ == "__main__":

    # default set up
    opus_json(START_QUALITY)

    rem_bandwidth = BANDWIDTH

    # make scale
    root = Tk()
    var = IntVar(value=START_QUALITY)
    var_prev = var.get()
    scale = Scale(root, from_=10, to_=0, variable=var)
    scale.pack(anchor=CENTER)

    while rem_bandwidth > 0:
        # rem_bandwidth -= var.get()  # *** current: quality, want: bandwidth of quality
        t1 = time.time()
        t2 = t1

        while rem_bandwidth > 0 and t2 - t1 < TIME_DIF:
            root.update()
            t2 = time.time()

        root.update()
        if var_prev != var.get():
            # change quality
            opus_json(var.get())
            print(str(var_prev) + " -> " + str(var.get()))
            var_prev = var.get()
        """
        # for mic_level and speaker_level fluctuations
        elif var.get() != 10:
            # change only mic_level and speaker_level since quality not perfect
            opus_json(var.get())
        """
