from traceback import print_tb
import yaml
import json
import sys
import argparse
from array import array
import os
from os import path
import ROOT
from ROOT import TGraphErrors
from ROOT import kRed
sys.path.append('../')
from DQFitter import DQFitter
sys.path.append('../utils')
from utils_library import DoSystematics, CheckVariables

def main():
    print('start')
    parser = argparse.ArgumentParser(description='Arguments to pass')
    parser.add_argument('cfgFileName', metavar='text', default='config.yml', help='config file name')
    parser.add_argument("--gen_tutorial", help="generate tutorial sample", action="store_true")
    parser.add_argument("--do_fit", help="run the multi trial", action="store_true")
    parser.add_argument("--do_systematics", help="do systematic on signal extraction", action="store_true")
    parser.add_argument("--check_variables", help="check variables for the fit file", action="store_true")
    args = parser.parse_args()
    print(args)
    print('Loading task configuration: ...', end='\r')

    with open(args.cfgFileName, 'r') as jsonCfgFile:
        #inputCfg = json.load(jsonCfgFile)
        inputCfg = yaml.load(jsonCfgFile, yaml.FullLoader)
    print('Loading task configuration: Done!')
    
    if args.do_fit:
        if not path.isdir(inputCfg["output"]["output_file_name"]):
            os.system("mkdir -p %s" % (inputCfg["output"]["output_file_name"]))
        for histName in inputCfg["input"]["input_name"]:
            minFitRanges = inputCfg["input"]["pdf_dictionary"]["fitRangeMin"]
            maxFitRanges = inputCfg["input"]["pdf_dictionary"]["fitRangeMax"]
            for iRange in range(0, len(minFitRanges)):
                dqFitter = DQFitter(inputCfg["input"]["input_file_name"], histName, inputCfg["output"]["output_file_name"], minFitRanges[iRange], maxFitRanges[iRange])
                dqFitter.SetFitConfig(inputCfg["input"]["pdf_dictionary"])
                dqFitter.SingleFit(minFitRanges[iRange], maxFitRanges[iRange])
            #dqFitter.MultiTrial() # TO BE FIXED

    if args.do_systematics:
        # pt bin systematics
        ptMin = inputCfg["input"]["analysis_dictionary"]["ptMin"]
        ptMax = inputCfg["input"]["analysis_dictionary"]["ptMax"]
        with open("{}/systematics/{}_vs_pt.txt".format(inputCfg["output"]["output_file_name"], "sig_Jpsi"), 'w') as fOut:
            fOut.write("x_min x_max val stat syst \n")
            for iRange in range(0, len(ptMin)):
                DoSystematics(inputCfg["output"]["output_file_name"], "pt_%i_%i" % (ptMin[iRange], ptMax[iRange]), "sig_Jpsi", fOut)

        # y bin systematics
        yMin = inputCfg["input"]["analysis_dictionary"]["yMin"]
        yMax = inputCfg["input"]["analysis_dictionary"]["yMax"]
        with open("{}/systematics/{}_vs_y.txt".format(inputCfg["output"]["output_file_name"], "sig_Jpsi"), 'w') as fOut:
            fOut.write("x_min x_max val stat syst \n")
            for iRange in range(0, len(yMin)):
                DoSystematics(inputCfg["output"]["output_file_name"], "y_%3.2f_%3.2f" % (yMin[iRange], yMax[iRange]), "sig_Jpsi", fOut)
            fOut.close()

    if args.check_variables:
        fInNames = inputCfg["input"]["analysis_dictionary"]["input_name_pt"]
        ptMin = inputCfg["input"]["analysis_dictionary"]["ptMin"]
        ptMax = inputCfg["input"]["analysis_dictionary"]["ptMax"]
        parNames = inputCfg["input"]["analysis_dictionary"]["parName"]
        fOutName = inputCfg["output"]["output_file_name"]
        CheckVariables(fInNames, parNames, ptMin, ptMax, fOutName, "pt")

        fInNames = inputCfg["input"]["analysis_dictionary"]["input_name_y"]
        yMin = inputCfg["input"]["analysis_dictionary"]["yMin"]
        yMax = inputCfg["input"]["analysis_dictionary"]["yMax"]
        parNames = inputCfg["input"]["analysis_dictionary"]["parName"]
        fOutName = inputCfg["output"]["output_file_name"]
        print(fInNames)
        print(yMin)
        print(yMax)
        print(parNames)
        print(fOutName)
        CheckVariables(fInNames, parNames, yMin, yMax, fOutName, "y")



if __name__ == '__main__':
    main()
