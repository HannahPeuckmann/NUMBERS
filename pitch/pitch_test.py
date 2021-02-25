#pitch_test.py

import logging
import crepe
from scipy.io.wavfile import read, write
import amfm_decompy.basic_tools as basic
import amfm_decompy.pYAAPT as pYAAPT
import matplotlib.pyplot as plt
import numpy as np
import webrtcvad



def pitch():
    signal = basic.SignalObj('record.wav')
    seperator = '\t'
    text_file = open("pitch.txt", mode="w")
    rate, np_audio, = read('record.wav')
    time, frequency, confidence, activation = crepe.predict(np_audio, rate)
    for i in range(len(time)):
        text_file.write(str(time[i]) + seperator
                            + str(frequency[i]) + seperator \
                            + str(confidence[i]) + seperator \
                            + '\n')
    pitchY = pYAAPT.yaapt(signal,\
            frame_length=10,\
            tda_frame_length=30,\
            f0_min=40, f0_max=1000)

    #plot
    fig, (ax1,ax2,ax3) = plt.subplots(3, 1, sharex=True, sharey=True, figsize=(12, 8))
    ax1.plot(np.asarray(frequency), label='crepe', color='green')
    ax1.legend(loc="upper right")
    ax2.plot(pitchY.samp_values, label='YAAPT', color='blue')
    ax2.legend(loc="upper right")
    plt.show()

def plot_from_txt(txt):
    f = open(txt, mode="r")
    freq = []
    for line in f:
        line = line.split()
        freq.append(line[1])

    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True, sharey=True, figsize=(12, 8))
    ax1.plot(np.asarray(freq), label='crepe', color='green')
    ax1.legend(loc="upper right")
    plt.show()

def fft_freq():
    rate, data = read('silence.wav')
    duration = len(data)/rate
    time = np.arange(0,duration,1/rate)
    # Plotting the Graph using Matplotlib
    print(len(data))
    counter = 0
    for i in data:
        if i > 2000:
            counter += 1
    print(counter)
    plt.plot(time,data)
    plt.xlabel('Time [s]')
    plt.ylabel('Amplitude')
    plt.title('6TU5302374.wav')
    plt.show()






if __name__ == "__main__":
    logging.basicConfig(filename='NUMBERS.log',
                    level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s: %(message)s')
    fft_freq()