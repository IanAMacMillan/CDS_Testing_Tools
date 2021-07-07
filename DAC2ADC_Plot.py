import matplotlib.pyplot as plt
import numpy as np
import os

fileNameList = ['results_C1-BHD_0_16_0_0_-30000_30000_5000.txt', 'results_C1-BHD_0_16_16_0_-30000_30000_5000.txt', 'results_C1-SU2_0_16_0_0_-30000_30000_5000.txt', 'results_C1-SU2_16_16_32_0_-30000_30000_5000.txt', 'results_C1-SU2_32_16_16_0_-30000_30000_5000.txt', 'results_C1-SU2_32_16_48_0_-30000_30000_5000.txt']

for fileName in fileNameList:
    #get metadata
    parts = fileName.split('_')

    FEroot=parts[1]
    DACstart=parts[2]
    DACnum=parts[3]
    ADCstart=parts[4]
    driveADC=parts[5]
    offsetStart=parts[6]
    offsetStop=parts[7]
    offsetStep=parts[8].split('.')[0]

    plotfolder = 'Plots/' + FEroot +'/'

    #+ '_'.join([str(v) for v in [FEroot, DACstart, DACnum, ADCstart, driveADC]]) + '/'
    if not os.path.exists(plotfolder):
        os.makedirs(plotfolder)

    rawDataSum = np.loadtxt(fileName)
    rawData = np.loadtxt(fileName).T
    numChan = len(rawData) - 1 #the number of channels

    offsetVal=rawData[0]/10
    #data = np.delete(rawData, 0)

    plt.figure(figsize=(10,6.5))
    for set in reversed(range(len(rawDataSum))):
        xchan=range(int(DACstart),numChan+int(DACstart), 1)
        ydata=list(np.delete((rawDataSum[set]/10), 0, axis=None))
        plt.plot(xchan, ydata, linestyle='None', markersize = 7.0, marker='.', label=str(offsetVal[set]))
    #plt.plot(np.full((1, len(rawData[set+1])), set+1)[0], rawData[set+1]/10, linestyle='None', markersize = 7.0,marker='.')

    plt.xticks(np.arange(int(DACstart), numChan+int(DACstart)+1, 1.0))
    plt.yticks(np.arange(-1500, 1500, 250))
    plt.xlabel('DAC Channel')
    plt.ylabel('Response')
    plt.title(FEroot + ', DAC Channels ' + DACstart + '-' + str(int(DACstart)+int(DACnum)-1) + ' Connected to Respective ADC Channels ' + ADCstart + '-' + str(int(ADCstart)+int(DACnum)-1))
    plt.grid(True)
    #plt.legend()
    plt.legend(title='Offsets', bbox_to_anchor=(1.0, 1), loc='upper left')
    plt.savefig(plotfolder + 'ChRespSummary_' + '_'.join([str(v) for v in [FEroot, DACstart, DACnum, ADCstart, driveADC, offsetStart, offsetStop, offsetStep]]) + '.pdf', bbox_inches = 'tight', pad_inches = 0.2)
    #plt.show()
    plt.close()


    for k in range(numChan):
        fig, (ax1, rem, ax12) = plt.subplots(3, sharex=True,figsize=(10,6.5), gridspec_kw={'height_ratios':[2,0.1,0.75]})
        
        
        ax1.title.set_text(FEroot + ', DAC Channel ' + str(int(DACstart)+k) + ' Connected to ADC Channel ' + str(int(ADCstart)+k))
        # make expected data
        t = np.arange(-3000, 4000, 1000)
        s = t/2
        ax1.plot(t, s, linewidth = 1, color='xkcd:azure', label='Expected Response (0.5 Gain)')
        ax1.plot(offsetVal, rawData[k+1]/10, color='r', markersize = 7.0,marker='.', label='Measured Response')
        
        ax1.legend()
        ax1.grid(which='minor',axis='both')
        ax1.grid(which='major',axis='both')
        
        ax1.set(ylabel='Channel Response')
        
        rem.remove()
        
        
        
        # plot channel response diffrence
        diffrence=(rawData[k+1]/10)-((offsetVal)/2)
        
        ax12.title.set_text('Diffrence Between Expected Response and Measured Response' )
        ax12.plot([-3000,3000], [0,0], color='xkcd:azure', linewidth = 1, label='Ideal response')
        ax12.plot(offsetVal, diffrence, color='g', markersize = 7.0,marker='.', label='Measured - Expected Response')
        
        secondMax=np.partition(diffrence.flatten(), -2)[-2]
        secondMin=np.partition(diffrence.flatten(), -2)[2]
        ax12.set_ylim(min([-0.5,secondMin-(abs(secondMin)*0.2)]), secondMax*1.2)
        ax12.set(ylabel='Diffrence', xlabel='Offest')
        ax12.grid(which='minor',axis='both')
        ax12.grid(which='major',axis='both')
        #ax12.legend()
            
        plt.subplots_adjust(top=None,bottom=None, hspace=0.075)
        
        plt.savefig(plotfolder + 'ChResp_' + '_'.join([str(v) for v in [FEroot, 'DAC',str(int(DACstart)+k), 'ADC',str(int(ADCstart)+k)]]) + '.pdf', bbox_inches = 'tight', pad_inches = 0.2)
        plt.close
        #plt.show()

    '''
        
        for k in range(numChan):
        plt.figure(figsize=(8,5))
        
        #make expected data
        t = np.arange(-3000, 4000, 1000)
        s = t/2
        plt.plot(t, s, linewidth = 1, color='xkcd:azure', label='expected response (0.5 Gain)')
        
        plt.plot(offsetVal, rawData[k+1]/10, color='r', markersize = 7.0,marker='.', label='Measured Response')
        
        plt.xlabel('Offset')
        plt.ylabel('Channel Response')
        plt.title(FEroot + ', DAC Channel ' + str(int(DACstart)+k) + ', ADC Channel ' + str(int(ADCstart)+k))
        plt.grid(True)
        plt.legend()
        plt.savefig(plotfolder + 'ChResp_' + '_'.join([str(v) for v in [FEroot, 'DAC',str(int(DACstart)+k), 'ADC',str(int(ADCstart)+k)]]) + '.pdf')
        #plt.show()
        plt.close()
        
        
        
        #plot channel response diffrence
        diffrence=(rawData[k+1]/10)-((offsetVal)/2)
        plt.figure(figsize=(8,5))
        plt.plot([-3000,3000], [0,0], color='xkcd:azure', label='expected response')
        plt.plot(offsetVal, diffrence, color='r', markersize = 7.0,marker='.', label='Channel Response Diffrence')
        #plt.yscale('log')
        secondMax=np.partition(diffrence.flatten(), -2)[-2]
        secondMin=np.partition(diffrence.flatten(), 2)[2]
        plt.ylim(min([-0.5,secondMin-(abs(secondMin)*0.5)]), secondMax*1.2)
        plt.xlabel('Offset')
        plt.ylabel('Channel Response - Expected Response')
        plt.title( 'Diffrence: ' + FEroot + ', DAC Channel ' + str(int(DACstart)+k) + ', ADC Channel ' + str(int(ADCstart)+k))
        plt.grid(True)
        plt.legend()
        plt.savefig(plotfolder + 'ChRespDiff_' + '_'.join([str(v) for v in [FEroot, 'DAC',str(int(DACstart)+k), 'ADC',str(int(ADCstart)+k)]]) + '.pdf')
        #plt.show()
        plt.close()
        '''
