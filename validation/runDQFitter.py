from traceback import print_tb
import yaml
import json
import sys
import argparse
from array import array
import os
from os import path
import ROOT
from ROOT import TFile
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
            dqFitter = DQFitter(inputCfg["input"]["input_file_name"], histName, inputCfg["output"]["output_file_name"], 2, 5)
            #dqFitter = DQFitter(inputCfg["input"]["input_file_name"], inputCfg["input"]["input_name"], inputCfg["output"]["output_file_name"])
            dqFitter.SetFitConfig(inputCfg["input"]["pdf_dictionary"])
            dqFitter.MultiTrial()

    if args.do_systematics:
        fIn = TFile.Open("1")
        DoSystematics(fIn, "sig_Jpsi")

    if args.check_variables:
        fInNames = inputCfg["input"]["analysis_dictionary"]["input_name"]
        xMin = inputCfg["input"]["analysis_dictionary"]["xMin"]
        xMax = inputCfg["input"]["analysis_dictionary"]["xMax"]
        parNames = inputCfg["input"]["analysis_dictionary"]["parName"]
        fOutName = inputCfg["output"]["output_file_name"]
        CheckVariables(fInNames, parNames, xMin, xMax, fOutName)



if __name__ == '__main__':
    main()
