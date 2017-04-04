'''
Created on Mar 27, 2017

Record a set number of samples when triggered 

@author: quangvu
'''

import time
import dwf

#constants
N_TRACES  = 2          # Total number of traces to record
N_AVG     = 2          # Number of traces to average

HZ_ACQ    = 1000000    # 1MHz
N_SAMPLES = 2000       # 2000 / 1MHz = 2msec

#set up acquisition
dwf_ai = dwf.DwfAnalogIn()
dwf_ai.channelEnableSet(0, True)
dwf_ai.channelRangeSet(0, 3.3)
dwf_ai.acquisitionModeSet(dwf_ai.ACQMODE.RECORD)
dwf_ai.frequencySet(HZ_ACQ)
dwf_ai.recordLengthSet(N_SAMPLES / HZ_ACQ)

#set up trigger
dwf_ai.triggerAutoTimeoutSet() #disable auto trigger
dwf_ai.triggerSourceSet(dwf_ai.TRIGSRC.DETECTOR_ANALOG_IN)
dwf_ai.triggerTypeSet(dwf_ai.TRIGTYPE.EDGE)
dwf_ai.triggerChannelSet(1)  # Trigger on Channel 2
dwf_ai.triggerLevelSet(1)    # 1V
dwf_ai.triggerConditionSet(dwf_ai.TRIGCOND.FALLING_NEGATIVE)

#wait at least 2 seconds for the offset to stabilize
time.sleep(2)

traces = []
print("Start recording traces...")
for iTrigger in range(N_TRACES):
    for iAvg in range(N_AVG):
        cSamples   = 0
        rgdSamples = []
        fLost      = False
        fCorrupted = False
    
        #begin acquisition
        dwf_ai.configure(False, True)
        while cSamples < N_SAMPLES:
            sts = dwf_ai.status(True)
            if cSamples == 0 and sts in (dwf_ai.STATE.CONFIG,
                                         dwf_ai.STATE.PREFILL,
                                         dwf_ai.STATE.ARMED):
                # Acquisition not yet started.
                continue
    
            cAvailable, cLost, cCorrupted = dwf_ai.statusRecord()
            cSamples += cLost
    
            if cAvailable == 0:
                continue
            if cSamples + cAvailable > N_SAMPLES:
                cAvailable = N_SAMPLES - cSamples
                
            # get samples
            rgdSamples.extend(dwf_ai.statusData(0, cAvailable))
            cSamples += cAvailable

        # Record finished
        traces.append(rgdSamples)

dwf_ai.close()
print("Finished!")

# Average traces to reduce noise
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
    
# Write traces to file
traces_filename = 'avg_traces.txt'
with open(traces_filename, 'w+') as file_out:
    for trace in avg_traces:
        file_out.write(" ".join([str(f) for f in trace]) + "\n")

     
        
