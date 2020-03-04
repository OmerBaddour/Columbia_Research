import math

if __name__ == '__main__':

    for quality in range(0, 11):
        line = str(quality) + ": {\"codec\":\"opus\",\"packet_time\":20,\"noise\":null,\"noise_level\":0,"
        loss_and_corrupt = 5 * math.ceil((10 - quality) / 2)
        line += "\"tx_loss\":" + str(loss_and_corrupt) + ","
        line += "\"tx_error\":" + str(loss_and_corrupt) + ","
        line += "\"tx_delay\":" + str((10 - quality) * 30) + "}"
        print(line)