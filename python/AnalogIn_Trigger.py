#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
   DWF Python Example 5

   Modified by: MURAMATSU Atsushi <amura@tomato.sakura.ne.jp>   
   Revised: 2016-04-21
   Original Author:  Digilent, Inc.
   Original Revision: 10/17/2013

   Requires:                       
       Python 2.7, 3.3 or later
"""

from adc import dwf
import time

import matplotlib.pyplot as plt

#print DWF version
print("DWF Version: " + dwf.FDwfGetVersion())

#open device
print("Opening first device")
dwf_ai = dwf.DwfAnalogIn()

print("Preparing to read sample...")

FREQ      = 8e6
N_SAMPLES = 8192

N_TRACES  = 1
N_AVG     = 600

#set up acquisition
dwf_ai.frequencySet(FREQ)
dwf_ai.bufferSizeSet(N_SAMPLES)
dwf_ai.channelEnableSet(0, True)
dwf_ai.channelRangeSet(0, 5.0)

#set up trigger
dwf_ai.triggerAutoTimeoutSet() #disable auto trigger
dwf_ai.triggerSourceSet(dwf_ai.TRIGSRC.DETECTOR_ANALOG_IN)
dwf_ai.triggerTypeSet(dwf_ai.TRIGTYPE.EDGE)
dwf_ai.triggerChannelSet(1)
dwf_ai.triggerLevelSet(2.0) # 1.5V
dwf_ai.triggerConditionSet(dwf_ai.TRIGCOND.FALLING_NEGATIVE)

# wait at least 2 seconds with Analog Discovery for the offset to stabilize,
# before the first reading after device open or offset/range change
time.sleep(2)

traces = []
print("   starting repeated acquisitions")
for iTrigger in range(N_TRACES):
    for iavg in range(N_AVG):
        #begin acquisition
        dwf_ai.configure(False, True)

        while True:
            if dwf_ai.status(True) == dwf_ai.STATE.DONE:
                break
            time.sleep(0.001)

        rgdSamples = dwf_ai.statusData(0, N_SAMPLES)
        traces.append(rgdSamples)
dwf_ai.close()

# Average traces to reduce noise
if N_AVG > 1:
    n          = N_TRACES * N_AVG
    avg_traces = []
    for i in range(0, n, N_AVG):
        avg   = [0.0] * N_SAMPLES
        chunk = traces[i:i+N_AVG]
        for c in chunk:
            for iSamples in range(0, N_SAMPLES):
                avg[iSamples] += c[iSamples]
        for iAvg in range(0, N_SAMPLES):
            avg[iAvg] = avg[iAvg] / N_AVG
        avg_traces.append(avg)
else:
    avg_traces = traces

filename = 'traces//traces.txt'
with open(filename, 'w+') as file_out:
    for trace in avg_traces:
        file_out.write(" ".join([str(f) for f in trace]) + "\n")