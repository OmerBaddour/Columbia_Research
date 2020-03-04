import math

if __name__ == '__main__':

    config = open("config.txt", "w")

    for quality in range(0, 11):
        line = str(quality) + ": {\"codec\":\"opus\",\"packet_time\":20,\"noise\":null,\"noise_level\":0,\"mic_level\":100,\"speaker_level\":100,"
        loss_and_corrupt = 40 - (4 * quality)
        line += "\"tx_loss\":" + str(loss_and_corrupt) + ","
        line += "\"tx_error\":" + str(loss_and_corrupt) + ","
        line += "\"tx_delay\":" + str((10 - quality) * 30) + "}\n"
        config.write(line)