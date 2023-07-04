from re import TEMPLATE
import matplotlib.pyplot as plt
import array as arr
import numpy as np
from array import array
import os
import sys
import math
import argparse
import ROOT
from os import path
from ROOT import TGraphErrors, TCanvas, TF1, TFile, TPaveText, TMath, TH1F, TH2F, TString, TLegend, TRatioPlot, TGaxis, TLine, TLatex
from ROOT import gROOT, gBenchmark, gPad, gStyle, kTRUE, kFALSE, kBlack, kRed, kGray, kDashed
from plot_library import LoadStyle, SetLatex

def StoreHistogramsFromFile(fIn, histType):
    '''
    Method which returns all the histograms of a certain class from a given file
    '''
    histArray = []
    for key in fIn.GetListOfKeys():
        kname = key.GetName()
        if (fIn.Get(kname).ClassName() == histType):
            histArray.append(fIn.Get(kname))
    return histArray

def ComputeRMS(parValArray):
    '''
    Method to evaluate the RMS of a sample ()
    '''
    mean = 0
    for parVal in parValArray:
        mean += parVal
    mean = mean / len(parValArray)
    stdDev = 0
    for parVal in parValArray:
        stdDev += (parVal - mean) * (parVal - mean)
    stdDev = math.sqrt(stdDev / len(parValArray))
    return stdDev

def DoSystematics(path, varBin, parName):
    '''
    Method to evaluate the systematic errors from signal extraction
    '''
    LoadStyle()
    gStyle.SetOptStat(0)
    gStyle.SetOptFit(0)
    nameTrialArray = []
    trialIndexArray  = array( 'f', [] )
    parValArray  = array( 'f', [] )
    parErrArray = array( 'f', [] )

    fInNameAllList = os.listdir(path)
    fInNameSelList = [path + "/" + fInName for fInName in fInNameAllList if varBin in fInName]
    fInNameSelList = [fInName for fInName in fInNameSelList if ".root" in fInName]
    
    index = 0.5
    for fInName in fInNameSelList:
        fIn = TFile.Open(fInName)
        for key in fIn.GetListOfKeys():
            kname = key.GetName()
            if "fit_results" in fIn.Get(kname).GetName():
                trialIndexArray.append(index)
                nameTrialArray.append(fIn.Get(kname).GetName().replace("fit_results_", ""))
                parValArray.append(fIn.Get(kname).GetBinContent(fIn.Get(kname).GetXaxis().FindBin(parName)))
                parErrArray.append(fIn.Get(kname).GetBinError(fIn.Get(kname).GetXaxis().FindBin(parName)))
                index = index + 1

    graParVal = TGraphErrors(len(parValArray), trialIndexArray, parValArray, 0, parErrArray)
    graParVal.SetMarkerStyle(24)
    graParVal.SetMarkerSize(1.2)
    graParVal.SetMarkerColor(kBlack)
    graParVal.SetLineColor(kBlack)

    funcParVal = TF1("funcParVal", "[0]", 0, len(trialIndexArray))
    graParVal.Fit(funcParVal, "R0Q")
    funcParVal.SetLineColor(kRed)
    funcParVal.SetLineWidth(2)

    trialIndexWidthArray = array( 'f', [] )
    parValSystArray = array( 'f', [] )
    parErrSystArray = array( 'f', [] )
    for i in range(0, len(parValArray)):
        trialIndexWidthArray.append(0.5)
        parValSystArray.append(funcParVal.GetParameter(0))
        parErrSystArray.append(ComputeRMS(parValArray))

    graParSyst = TGraphErrors(len(parValArray), trialIndexArray, parValSystArray, trialIndexWidthArray, parErrSystArray)
    graParSyst.SetFillColorAlpha(kGray+1, 0.3)

    lineParStatUp = TLine(0, funcParVal.GetParameter(0) + funcParVal.GetParError(0), len(trialIndexArray), funcParVal.GetParameter(0) + funcParVal.GetParError(0))
    lineParStatUp.SetLineStyle(kDashed)
    lineParStatUp.SetLineColor(kGray+1)

    lineParStatDown = TLine(0, funcParVal.GetParameter(0) - funcParVal.GetParError(0), len(trialIndexArray), funcParVal.GetParameter(0) - funcParVal.GetParError(0))
    lineParStatDown.SetLineStyle(kDashed)
    lineParStatDown.SetLineColor(kGray+1)

    latexTitle = TLatex()
    SetLatex(latexTitle)

    canvasParVal = TCanvas("canvasParVal", "canvasParVal", 800, 600)
    #histGrid = TH2F("histGrid", "", len(parValArray), 0, len(parValArray), 100, 0.7 * max(parValArray), 1.3 * max(parValArray))
    histGrid = TH2F("histGrid", "", len(parValArray), 0, len(parValArray), 100, 0.7 * min(parValArray), 1.3 * max(parValArray))
    indexLabel = 1
    for nameTrial in nameTrialArray:
        histGrid.GetXaxis().SetBinLabel(indexLabel, nameTrial)
        indexLabel += 1
    histGrid.Draw("same")
    funcParVal.Draw("same")
    lineParStatUp.Draw("same")
    lineParStatDown.Draw("same")
    graParSyst.Draw("E2same")
    graParVal.Draw("EPsame")

    centralVal = funcParVal.GetParameter(0)
    statError = funcParVal.GetParError(0)
    systError = ComputeRMS(parValArray)
    latexTitle.DrawLatex(0.25, 0.85, "N_{J/#psi} = #bf{%3.2f} #pm #bf{%3.2f} (%3.2f %%) #pm #bf{%3.2f} (%3.2f %%)" % (centralVal, statError, (statError/centralVal)*100, systError, (systError/centralVal)*100))
    print("%s -> %3.2f +/- %3.2f (%3.2f %%) +/- %3.2f (%3.2f %%)" % (varBin, centralVal, statError, (statError/centralVal)*100, systError, (systError/centralVal)*100))

    canvasParVal.SaveAs("{}/systematics/{}_{}.pdf".format(path, varBin, parName))

def CheckVariables(fInNames, parNames, xMin, xMax, fOutName, obs):
    '''
    Method to chech the variable evolution vs file in the list
    '''
    LoadStyle()
    gStyle.SetOptStat(0)
    gStyle.SetOptFit(0)

    xBins  = array( 'f', [] )
    xCentr  = array( 'f', [] )
    xError = array( 'f', [] )

    for i in range(0, len(xMin)):
        xCentr.append((xMax[i] + xMin[i]) / 2.)
        xError.append((xMax[i] - xMin[i]) / 2.)
        xBins.append(xMin[i])
    xBins.append(xMax[len(xMin)-1])
    

    fOut = TFile("{}myAnalysis_{}.root".format(fOutName,obs), "RECREATE")

    for parName in parNames:
        parValArray  = array( 'f', [] )
        parErrArray = array( 'f', [] )
        for fInName in fInNames:
            fIn = TFile.Open(fInName)
            for key in fIn.GetListOfKeys():
                kname = key.GetName()
                if "fit_results" in fIn.Get(kname).GetName():
                    parValArray.append(fIn.Get(kname).GetBinContent(fIn.Get(kname).GetXaxis().FindBin(parName)))
                    parErrArray.append(fIn.Get(kname).GetBinError(fIn.Get(kname).GetXaxis().FindBin(parName)))
        
        histParVal = TH1F("hist_{}".format(parName), "", len(xMin), xBins)

        for i in range(0, len(xMin)):
            histParVal.SetBinContent(i+1, parValArray[i])
            histParVal.SetBinError(i+1, parErrArray[i])

        graParVal = TGraphErrors(len(parValArray), xCentr, parValArray, xError, parErrArray)
        graParVal.SetMarkerStyle(24)
        graParVal.SetMarkerSize(1.2)
        graParVal.SetMarkerColor(kBlack)
        graParVal.SetLineColor(kBlack)

        fOut.cd()
        histParVal.Write("hist_{}".format(parName))
        graParVal.Write("gra_{}".format(parName))

    

    #canvasParVal = TCanvas("canvasParVal", "canvasParVal", 800, 600)
    #histGrid = TH2F("histGrid", "", 100, xMin[0], xMax[len(xMax)-1], 100, 0.7 * min(parValArray), 1.3 * max(parValArray))
    #histGrid.Draw("same")
    #graParVal.Draw("EPsame")


    