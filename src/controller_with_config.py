import time
from tkinter import *
import requests
import math

TOTAL_MAX_QUALITY = 50    # total and max quality
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


def kill_audio():

    json_data = "{\"mic_level\":0,\"speaker_level\":0}"
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
        print("Killing audio successful.")
        print(json_data)
    else:
        print("Killing audio unsuccessful." +
              "Request 1 status code: " + str(r1_activate.status_code) +
              ", Request 2 status code: " + str(r2_activate.status_code))


if __name__ == "__main__":

    # default set up
    opus_json(START_QUALITY)

    rem_quality = TOTAL_MAX_QUALITY

    # make scale
    root = Tk()
    var = IntVar(value=START_QUALITY)
    var_prev = var.get()
    scale = Scale(root, from_=10, to_=0, variable=var)
    scale.pack(anchor=CENTER)

    while True:

        while rem_quality > 0:
            print(rem_quality)

            # augment remaining quality
            change = (math.floor(len(data_list)/2) - var.get()) * TIME_DIF
            if rem_quality + change > TOTAL_MAX_QUALITY:
                rem_quality = TOTAL_MAX_QUALITY
            else:
                rem_quality += change

            t1 = time.time()
            t2 = t1

            while rem_quality > 0 and t2 - t1 < TIME_DIF:
                root.update()
                t2 = time.time()

            root.update()
            if var_prev != var.get():
                # change quality
                opus_json(var.get())
                print(str(var_prev) + " -> " + str(var.get()))
                var_prev = var.get()

        print(rem_quality)
        kill_audio()
        time.sleep(TIME_DIF)
        rem_quality += math.floor(len(data_list)/2)
