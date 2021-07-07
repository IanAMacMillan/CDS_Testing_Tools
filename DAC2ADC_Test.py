import os
import time
import numpy as np
import subprocess
from traceback import print_exc
import argparse


def grabInputArgs():
    parser = argparse.ArgumentParser(
        description='This script tets newly made FE machine ADCs and DACs'
        )
    parser.add_argument('-d', '--DACstart', type=int,
                        help='Starting index of connected DAC ouput. Default 0.',
                        default=0)
    parser.add_argument('-n', '--DACnum', type=int,
                        help='Number of connected DAC ouput. Default 16.',
                        default=16)
    parser.add_argument('-a', '--ADCstart', type=int,
                        help='Starting index of connected ADC ouput. Default 0.',
                        default=0)
    parser.add_argument('-r', '--driveADC', type=int,
                        help='Index of driving ADC. Default 16.',
                        default=16)
    parser.add_argument('-s', '--offsetStart', type=int,
                        help='Start offset value. Default -3000.',
                        default=-3000)
    parser.add_argument('-p', '--offsetStop', type=int,
                        help='Stop offset value. Default 3000.',
                        default=3000)
    parser.add_argument('-t', '--offsetStep', type=int,
                        help='Stop offset value. Default 1000.',
                        default=1000)
    parser.add_argument('-f', '--fileRoot', type=str,
                        default='results')
    parser.add_argument('-e', '--FEroot', type=str,
                        default='C1:SU2')
    parser.add_argument('-m', '--MMroot', type=str,
                        default='MM')
    return parser.parse_args()


def DAC2ADC_Test(DACstart, DACnum, ADCstart, driveADC,
                 offsetStart, offsetStop, offsetStep, fileRoot, FEroot):
    try:
        DAC_con = list(range(DACstart, DACstart + DACnum))
        ADC_con = list(range(ADCstart, ADCstart + DACnum))
        # DAC_con=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] # list of DAC outputs
        # ADC_con=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] # list of conected ADC inputs
        # driveADC = 16

        # Offset=300 # the value of the offset sent to the DAC
        offsetVals = list(range(offsetStart, offsetStop + 1, offsetStep))
    
    	  # f=open("results.txt", "a+")

    	  # set matrix elements
    	for dac in DAC_con:
          os.system('caput ' + FEroot + '-MM_'+ str(dac + 1) + '_' + str(driveADC) + ' 1')
        toWrite = np.zeros((len(offsetVals), DACnum + 1))
        for kk, offset in enumerate(offsetVals):
            os.system('caput ' + FEroot + '-FM' + str(driveADC) + '_OFFSET ' + str(offset)) # set OFFSET to desired value
            toWrite[kk, 0] = offset
            for ii, adc in enumerate(ADC_con):
                output = subprocess.check_output('caget ' + FEroot + '-FM' + str(adc) + '_INMON', shell=True) # record recieved value

                # TURN OUTPUT INTO NUMBER
                toWrite[kk, ii+1] = float(output.split(' ')[-1].replace('\n', ''))
        filename = fileRoot + '_' + '_'.join([str(v) for v in [FEroot, DACstart, DACnum, ADCstart, driveADC, offsetStart, offsetStop, offsetStep]]) + '.txt'
    	np.savetxt(filename, toWrite)

    except BaseException:
        print_exc()
    finally:
        os.system('caput ' + FEroot + '-FM' + str(driveADC) + '_OFFSET 0') # set OFFSET to zero
        # os.system('cdsutils switch C1:SU2-FM' + str(driveADC) + ' OFFSET OFF') # turn DAC OFFSET off
        # reset matrix elements
        for dac in DAC_con:
            os.system('caput ' + FEroot + '-MM_'+ str(dac + 1) + '_' + str(driveADC) + ' 0')


if __name__ == "__main__":
    args = grabInputArgs()
    DAC2ADC_Test(args.DACstart, args.DACnum, args.ADCstart, args.driveADC,
                 args.offsetStart, args.offsetStop, args.offsetStep,
                 args.fileRoot, args.FEroot)
