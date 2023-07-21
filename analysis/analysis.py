import yaml
import json
import sys
import argparse
from array import array
import os
from os import path
import numpy as np
import pandas as pd
import uncertainties
from uncertainties import ufloat, unumpy
import ROOT
from ROOT import TCanvas, TH1F, TH2F, TGraphErrors, TLegend
sys.path.append('../utils')
from utils_library import LoadStyle, PropagateErrorsOnRatio
from plot_library import LoadStyle, SetGraStat, SetGraSyst, SetLegend


def main():
    parser = argparse.ArgumentParser(description='Arguments to pass')
    parser.add_argument("--plot_results", help="plot results", action="store_true")
    args = parser.parse_args()
    print(args)


    if args.plot_results:
        LoadStyle()
        ROOT.gStyle.SetOptStat(0)

        brJpsiToMuMu = 0.05961
        brPsi2sToMuMu = 0.008

        ###############
        # Load datasets
        ###############
        # y-dependence
        dfYieldJpsiY = pd.read_csv('/Users/lucamicheletti/GITHUB/dq_fit_library/analysis/output/analysis/LHC22o_full_stat_apass4_data_run3_tails/systematics/sig_Jpsi_vs_y.txt', sep=' ')
        yMin = dfYieldJpsiY["x_min"].to_numpy()
        yMax = dfYieldJpsiY["x_max"].to_numpy()
        yArr = np.append(yMin, yMax[len(yMin)-1],)
        yCentr = (yMin + yMax) / 2.
        yWidth = (yMax - yMin) / 2.
        yieldJpsiY = dfYieldJpsiY["val"].to_numpy()
        statYieldJpsiY = dfYieldJpsiY["stat"].to_numpy()
        systYieldJpsiY = dfYieldJpsiY["syst"].to_numpy()
        print("Sum J/psi vs y: ", sum(yieldJpsiY))

        dfYieldPsi2sY = pd.read_csv('/Users/lucamicheletti/GITHUB/dq_fit_library/analysis/output/analysis/LHC22o_full_stat_apass4_data_run3_tails/systematics/sig_Psi2s_vs_y.txt', sep=' ')
        yieldPsi2sY = dfYieldPsi2sY["val"].to_numpy()
        statYieldPsi2sY = dfYieldPsi2sY["stat"].to_numpy()
        systYieldPsi2sY = dfYieldPsi2sY["syst"].to_numpy()
        print("Sum Psi(2S) vs y: ", sum(yieldPsi2sY))

        dfYieldJpsiY = pd.read_csv('run2_results/sig_Jpsi_vs_y_run2.txt', sep=' ')
        yMinRun2 = dfYieldJpsiY["x_min"].to_numpy()
        yMaxRun2 = dfYieldJpsiY["x_max"].to_numpy()
        yArrRun2 = np.append(yMinRun2, yMaxRun2[len(yMinRun2)-1],)
        yCentrRun2 = (yMinRun2 + yMaxRun2) / 2.
        yWidthRun2 = (yMaxRun2 - yMinRun2) / 2.
        yieldJpsiYRun2 = dfYieldJpsiY["val"].to_numpy()
        statYieldJpsiYRun2 = dfYieldJpsiY["stat"].to_numpy()
        systYieldJpsiYRun2 = dfYieldJpsiY["syst"].to_numpy()

        dfYieldPsi2sY = pd.read_csv('run2_results/sig_Psi2s_vs_y_run2.txt', sep=' ')
        yieldPsi2sYRun2 = dfYieldPsi2sY["val"].to_numpy()
        statYieldPsi2sYRun2 = dfYieldPsi2sY["stat"].to_numpy()
        systYieldPsi2sYRun2 = dfYieldPsi2sY["syst"].to_numpy()

        dfCsRatioY = pd.read_csv('run2_results/cs_ratio_Psi2s_Jpsi_vs_y_run2.txt', sep=' ')
        csRatioYRun2 = dfCsRatioY["val"].to_numpy()
        statCsRatioYRun2 = dfCsRatioY["stat"].to_numpy()
        systCsRatioYRun2 = dfCsRatioY["syst"].to_numpy()

        dfAxeJpsiY = pd.read_csv('acceptance_efficiency/axe_Jpsi_vs_y.txt', sep=' ')
        axeJpsiY = dfAxeJpsiY["val"].to_numpy()
        statAxeJpsiY = dfAxeJpsiY["stat"].to_numpy()
        systAxeJpsiY = dfAxeJpsiY["syst"].to_numpy()

        dfAxePsi2sY = pd.read_csv('acceptance_efficiency/axe_Psi2s_vs_y.txt', sep=' ')
        axePsi2sY = dfAxePsi2sY["val"].to_numpy()
        statAxePsi2sY = dfAxePsi2sY["stat"].to_numpy()
        systAxePsi2sY = dfAxePsi2sY["syst"].to_numpy()

        # pt-dependence
        dfYieldJpsiPt = pd.read_csv('/Users/lucamicheletti/GITHUB/dq_fit_library/analysis/output/analysis/LHC22o_full_stat_apass4_data_run3_tails/systematics/sig_Jpsi_vs_pt.txt', sep=' ')
        ptMin = dfYieldJpsiPt["x_min"].to_numpy()
        ptMax = dfYieldJpsiPt["x_max"].to_numpy()
        ptArr = np.append(ptMin, ptMax[len(ptMin)-1],)
        ptCentr = (ptMin + ptMax) / 2.
        ptWidth = (ptMax - ptMin) / 2.
        yieldJpsiPt = dfYieldJpsiPt["val"].to_numpy()
        statYieldJpsiPt = dfYieldJpsiPt["stat"].to_numpy()
        systYieldJpsiPt = dfYieldJpsiPt["syst"].to_numpy()
        print("Sum J/psi vs pT: ", sum(yieldJpsiPt))

        dfYieldPsi2sPt = pd.read_csv('/Users/lucamicheletti/GITHUB/dq_fit_library/analysis/output/analysis/LHC22o_full_stat_apass4_data_run3_tails/systematics/sig_Psi2s_vs_pt.txt', sep=' ')
        yieldPsi2sPt = dfYieldPsi2sPt["val"].to_numpy()
        statYieldPsi2sPt = dfYieldPsi2sPt["stat"].to_numpy()
        systYieldPsi2sPt = dfYieldPsi2sPt["syst"].to_numpy()
        print("Sum J/psi vs pT: ", sum(yieldPsi2sPt))

        dfYieldJpsiPt = pd.read_csv('run2_results/sig_Jpsi_vs_pt_run2.txt', sep=' ')
        ptMinRun2 = dfYieldJpsiPt["x_min"].to_numpy()
        ptMaxRun2 = dfYieldJpsiPt["x_max"].to_numpy()
        ptArrRun2 = np.append(ptMinRun2, ptMaxRun2[len(ptMinRun2)-1],)
        ptCentrRun2 = (ptMinRun2 + ptMaxRun2) / 2.
        ptWidthRun2 = (ptMaxRun2 - ptMinRun2) / 2.
        yieldJpsiPtRun2 = dfYieldJpsiPt["val"].to_numpy()
        statYieldJpsiPtRun2 = dfYieldJpsiPt["stat"].to_numpy()
        systYieldJpsiPtRun2 = dfYieldJpsiPt["syst"].to_numpy()

        dfYieldPsi2sY = pd.read_csv('run2_results/sig_Psi2s_vs_pt_run2.txt', sep=' ')
        yieldPsi2sPtRun2 = dfYieldPsi2sY["val"].to_numpy()
        statYieldPsi2sPtRun2 = dfYieldPsi2sY["stat"].to_numpy()
        systYieldPsi2sPtRun2 = dfYieldPsi2sY["syst"].to_numpy()

        dfCsRatioPt = pd.read_csv('run2_results/cs_ratio_Psi2s_Jpsi_vs_pt_run2.txt', sep=' ')
        csRatioPtRun2 = dfCsRatioPt["val"].to_numpy()
        statCsRatioPtRun2 = dfCsRatioPt["stat"].to_numpy()
        systCsRatioPtRun2 = dfCsRatioPt["syst"].to_numpy()

        dfAxeJpsiPt = pd.read_csv('acceptance_efficiency/axe_Jpsi_vs_pt.txt', sep=' ')
        axeJpsiPt = dfAxeJpsiPt["val"].to_numpy()
        statAxeJpsiPt = dfAxeJpsiPt["stat"].to_numpy()
        systAxeJpsiPt = dfAxeJpsiPt["syst"].to_numpy()

        dfAxePsi2sPt = pd.read_csv('acceptance_efficiency/axe_Psi2s_vs_pt.txt', sep=' ')
        axePsi2sPt = dfAxePsi2sPt["val"].to_numpy()
        statAxePsi2sPt = dfAxePsi2sPt["stat"].to_numpy()
        systAxePsi2sPt = dfAxePsi2sPt["syst"].to_numpy()

        ############################
        # Create and fill histograms
        ############################
        # y-dependence
        histStatYieldJpsiY = TH1F("histStatYieldJpsiY", "", len(yArr)-1, yArr)
        for i in range(0, len(yArr)-1) : histStatYieldJpsiY.SetBinContent(i+1, yieldJpsiY[i]), histStatYieldJpsiY.SetBinError(i+1, statYieldJpsiY[i])
        SetGraStat(histStatYieldJpsiY, 20, ROOT.kRed+1)
        histStatYieldJpsiY.Scale(1, "WIDTH")

        histSystYieldJpsiY = TH1F("histSystYieldJpsiY", "", len(yArr)-1, yArr)
        for i in range(0, len(yArr)-1) : histSystYieldJpsiY.SetBinContent(i+1, yieldJpsiY[i]), histSystYieldJpsiY.SetBinError(i+1, systYieldJpsiY[i])
        SetGraSyst(histSystYieldJpsiY, 20, ROOT.kRed+1)
        histSystYieldJpsiY.Scale(1, "WIDTH")

        histStatYieldJpsiNormY = TH1F("histStatYieldJpsiNormY", "", len(yArr)-1, yArr)
        for i in range(0, len(yArr)-1) : histStatYieldJpsiNormY.SetBinContent(i+1, yieldJpsiY[i]), histStatYieldJpsiNormY.SetBinError(i+1, statYieldJpsiY[i])
        SetGraStat(histStatYieldJpsiNormY, 20, ROOT.kRed+1)
        histStatYieldJpsiNormY.Scale(1. / histStatYieldJpsiNormY.Integral())

        histSystYieldJpsiNormY = TH1F("histSystYieldJpsiNormY", "", len(yArr)-1, yArr)
        for i in range(0, len(yArr)-1) : histSystYieldJpsiNormY.SetBinContent(i+1, yieldJpsiY[i]), histSystYieldJpsiNormY.SetBinError(i+1, systYieldJpsiY[i])
        SetGraSyst(histSystYieldJpsiNormY, 20, ROOT.kRed+1)
        histSystYieldJpsiNormY.Scale(1. / histSystYieldJpsiNormY.Integral())

        histStatYieldPsi2sY = TH1F("histStatYieldPsi2sY", "", len(yArr)-1, yArr)
        for i in range(0, len(yArr)-1) : histStatYieldPsi2sY.SetBinContent(i+1, yieldPsi2sY[i]), histStatYieldPsi2sY.SetBinError(i+1, statYieldPsi2sY[i])
        SetGraStat(histStatYieldPsi2sY, 20, ROOT.kAzure+4)
        histStatYieldPsi2sY.Scale(1, "WIDTH")

        histSystYieldPsi2sY = TH1F("histSystYieldPsi2sY", "", len(yArr)-1, yArr)
        for i in range(0, len(yArr)-1) : histSystYieldPsi2sY.SetBinContent(i+1, yieldPsi2sY[i]), histSystYieldPsi2sY.SetBinError(i+1, systYieldPsi2sY[i])
        SetGraSyst(histSystYieldPsi2sY, 20, ROOT.kAzure+4)
        histSystYieldPsi2sY.Scale(1, "WIDTH")

        histStatYieldPsi2sNormY = TH1F("histStatYieldPsi2sNormY", "", len(yArr)-1, yArr)
        for i in range(0, len(yArr)-1) : histStatYieldPsi2sNormY.SetBinContent(i+1, yieldPsi2sY[i]), histStatYieldPsi2sNormY.SetBinError(i+1, statYieldPsi2sY[i])
        SetGraStat(histStatYieldPsi2sNormY, 20, ROOT.kAzure+4)
        histStatYieldPsi2sNormY.Scale(1. / histStatYieldPsi2sNormY.Integral())

        histSystYieldPsi2sNormY = TH1F("histSystYieldPsi2sNormY", "", len(yArr)-1, yArr)
        for i in range(0, len(yArr)-1) : histSystYieldPsi2sNormY.SetBinContent(i+1, yieldPsi2sY[i]), histSystYieldPsi2sNormY.SetBinError(i+1, systYieldPsi2sY[i])
        SetGraSyst(histSystYieldPsi2sNormY, 20, ROOT.kAzure+4)
        histSystYieldPsi2sNormY.Scale(1. / histSystYieldPsi2sNormY.Integral())

        # Run2
        histStatYieldJpsiNormYRun2 = TH1F("histStatYieldJpsiNormYRun2", "", len(yArrRun2)-1, yArrRun2)
        for i in range(0, len(yArrRun2)-1) : histStatYieldJpsiNormYRun2.SetBinContent(i+1, yieldJpsiYRun2[i]), histStatYieldJpsiNormYRun2.SetBinError(i+1, statYieldJpsiYRun2[i])
        SetGraStat(histStatYieldJpsiNormYRun2, 20, ROOT.kBlack)
        histStatYieldJpsiNormYRun2.Scale(1. / histStatYieldJpsiNormYRun2.Integral())

        histSystYieldJpsiNormYRun2 = TH1F("histSystYieldJpsiNormYRun2", "", len(yArrRun2)-1, yArrRun2)
        for i in range(0, len(yArrRun2)-1) : histSystYieldJpsiNormYRun2.SetBinContent(i+1, yieldJpsiYRun2[i]), histSystYieldJpsiNormYRun2.SetBinError(i+1, systYieldJpsiYRun2[i])
        SetGraSyst(histSystYieldJpsiNormYRun2, 20, ROOT.kBlack)
        histSystYieldJpsiNormYRun2.Scale(1. / histSystYieldJpsiNormYRun2.Integral())

        histStatYieldPsi2sNormYRun2 = TH1F("histStatYieldPsi2sNormYRun2", "", len(yArrRun2)-1, yArrRun2)
        for i in range(0, len(yArrRun2)-1) : histStatYieldPsi2sNormYRun2.SetBinContent(i+1, yieldPsi2sYRun2[i]), histStatYieldPsi2sNormYRun2.SetBinError(i+1, statYieldPsi2sYRun2[i])
        SetGraStat(histStatYieldPsi2sNormYRun2, 20, ROOT.kBlack)
        histStatYieldPsi2sNormYRun2.Scale(1. / histStatYieldPsi2sNormYRun2.Integral())

        histSystYieldPsi2sNormYRun2 = TH1F("histSystYieldPsi2sNormYRun2", "", len(yArrRun2)-1, yArrRun2)
        for i in range(0, len(yArrRun2)-1) : histSystYieldPsi2sNormYRun2.SetBinContent(i+1, yieldPsi2sYRun2[i]), histSystYieldPsi2sNormYRun2.SetBinError(i+1, systYieldPsi2sYRun2[i])
        SetGraSyst(histSystYieldPsi2sNormYRun2, 20, ROOT.kBlack)
        histSystYieldPsi2sNormYRun2.Scale(1. / histSystYieldPsi2sNormYRun2.Integral())

        # Acceptance-efficiency
        histAxeJpsiY = TH1F("histAxeJpsiY", "", len(yArr)-1, yArr)
        for i in range(0, len(yArr)-1) : histAxeJpsiY.SetBinContent(i+1, axeJpsiY[i]), histAxeJpsiY.SetBinError(i+1, statAxeJpsiY[i])
        SetGraStat(histAxeJpsiY, 20, ROOT.kRed+1)

        histAxePsi2sY = TH1F("histAxePsi2sY", "", len(yArr)-1, yArr)
        for i in range(0, len(yArr)-1) : histAxePsi2sY.SetBinContent(i+1, axePsi2sY[i]), histAxePsi2sY.SetBinError(i+1, statAxePsi2sY[i])
        SetGraStat(histAxePsi2sY, 20, ROOT.kAzure+4)

        # pt-dependence
        histStatYieldJpsiPt = TH1F("histStatYieldJpsiPt", "", len(ptArr)-1, ptArr)
        for i in range(0, len(ptArr)-1) : histStatYieldJpsiPt.SetBinContent(i+1, yieldJpsiPt[i]), histStatYieldJpsiPt.SetBinError(i+1, statYieldJpsiPt[i])
        SetGraStat(histStatYieldJpsiPt, 20, ROOT.kRed+1)
        histStatYieldJpsiPt.Scale(1, "WIDTH")

        histSystYieldJpsiPt = TH1F("histSystYieldJpsiPt", "", len(ptArr)-1, ptArr)
        for i in range(0, len(ptArr)-1) : histSystYieldJpsiPt.SetBinContent(i+1, yieldJpsiPt[i]), histSystYieldJpsiPt.SetBinError(i+1, systYieldJpsiPt[i])
        SetGraSyst(histSystYieldJpsiPt, 20, ROOT.kRed+1)
        histSystYieldJpsiPt.Scale(1, "WIDTH")

        histStatYieldJpsiNormPt = TH1F("histStatYieldJpsiNormPt", "", len(ptArr)-1, ptArr)
        for i in range(0, len(ptArr)-1) : histStatYieldJpsiNormPt.SetBinContent(i+1, yieldJpsiPt[i]), histStatYieldJpsiNormPt.SetBinError(i+1, statYieldJpsiPt[i])
        SetGraStat(histStatYieldJpsiNormPt, 20, ROOT.kRed+1)
        histStatYieldJpsiNormPt.Scale(1. / histStatYieldJpsiNormPt.Integral(), "WIDTH")

        histSystYieldJpsiNormPt = TH1F("histSystYieldJpsiNormPt", "", len(ptArr)-1, ptArr)
        for i in range(0, len(ptArr)-1) : histSystYieldJpsiNormPt.SetBinContent(i+1, yieldJpsiPt[i]), histSystYieldJpsiNormPt.SetBinError(i+1, systYieldJpsiPt[i])
        SetGraSyst(histSystYieldJpsiNormPt, 20, ROOT.kRed+1)
        histSystYieldJpsiNormPt.Scale(1. / histSystYieldJpsiNormPt.Integral(), "WIDTH")

        histStatYieldPsi2sPt = TH1F("histStatYieldPsi2sPt", "", len(ptArr)-1, ptArr)
        for i in range(0, len(ptArr)-1) : histStatYieldPsi2sPt.SetBinContent(i+1, yieldPsi2sPt[i]), histStatYieldPsi2sPt.SetBinError(i+1, statYieldPsi2sPt[i])
        SetGraStat(histStatYieldPsi2sPt, 20, ROOT.kAzure+4)
        histStatYieldPsi2sPt.Scale(1, "WIDTH")

        histSystYieldPsi2sPt = TH1F("histSystYieldPsi2sPt", "", len(ptArr)-1, ptArr)
        for i in range(0, len(ptArr)-1) : histSystYieldPsi2sPt.SetBinContent(i+1, yieldPsi2sPt[i]), histSystYieldPsi2sPt.SetBinError(i+1, systYieldPsi2sPt[i])
        SetGraSyst(histSystYieldPsi2sPt, 20, ROOT.kAzure+4)
        histSystYieldPsi2sPt.Scale(1, "WIDTH")

        histStatYieldPsi2sNormPt = TH1F("histStatYieldPsi2sNormPt", "", len(ptArr)-1, ptArr)
        for i in range(0, len(ptArr)-1) : histStatYieldPsi2sNormPt.SetBinContent(i+1, yieldPsi2sPt[i]), histStatYieldPsi2sNormPt.SetBinError(i+1, statYieldPsi2sPt[i])
        SetGraStat(histStatYieldPsi2sNormPt, 20, ROOT.kAzure+4)
        histStatYieldPsi2sNormPt.Scale(1. / histStatYieldPsi2sNormPt.Integral(), "WIDTH")

        histSystYieldPsi2sNormPt = TH1F("histSystYieldPsi2sNormPt", "", len(ptArr)-1, ptArr)
        for i in range(0, len(ptArr)-1) : histSystYieldPsi2sNormPt.SetBinContent(i+1, yieldPsi2sPt[i]), histSystYieldPsi2sNormPt.SetBinError(i+1, systYieldPsi2sPt[i])
        SetGraSyst(histSystYieldPsi2sNormPt, 20, ROOT.kAzure+4)
        histSystYieldPsi2sNormPt.Scale(1. / histSystYieldPsi2sNormPt.Integral(), "WIDTH")

        # Run2
        histStatYieldJpsiNormPtRun2 = TH1F("histStatYieldJpsiNormPtRun2", "", len(ptArrRun2)-1, ptArrRun2)
        for i in range(0, len(ptArrRun2)-1) : histStatYieldJpsiNormPtRun2.SetBinContent(i+1, yieldJpsiPtRun2[i]), histStatYieldJpsiNormPtRun2.SetBinError(i+1, statYieldJpsiPtRun2[i])
        SetGraStat(histStatYieldJpsiNormPtRun2, 20, ROOT.kBlack)
        histStatYieldJpsiNormPtRun2.Scale(1. / histStatYieldJpsiNormPtRun2.Integral(), "WIDTH")

        histSystYieldJpsiNormPtRun2 = TH1F("histSystYieldJpsiNormPtRun2", "", len(ptArrRun2)-1, ptArrRun2)
        for i in range(0, len(ptArrRun2)-1) : histSystYieldJpsiNormPtRun2.SetBinContent(i+1, yieldJpsiPtRun2[i]), histSystYieldJpsiNormPtRun2.SetBinError(i+1, systYieldJpsiPtRun2[i])
        SetGraSyst(histSystYieldJpsiNormPtRun2, 20, ROOT.kBlack)
        histSystYieldJpsiNormPtRun2.Scale(1. / histSystYieldJpsiNormPtRun2.Integral(), "WIDTH")

        histStatYieldPsi2sNormPtRun2 = TH1F("histStatYieldPsi2sNormPtRun2", "", len(ptArrRun2)-1, ptArrRun2)
        for i in range(0, len(ptArrRun2)-1) : histStatYieldPsi2sNormPtRun2.SetBinContent(i+1, yieldPsi2sPtRun2[i]), histStatYieldPsi2sNormPtRun2.SetBinError(i+1, statYieldPsi2sPtRun2[i])
        SetGraStat(histStatYieldPsi2sNormPtRun2, 20, ROOT.kBlack)
        histStatYieldPsi2sNormPtRun2.Scale(1. / histStatYieldPsi2sNormPtRun2.Integral(), "WIDTH")

        histSystYieldPsi2sNormPtRun2 = TH1F("histSystYieldPsi2sNormPtRun2", "", len(ptArrRun2)-1, ptArrRun2)
        for i in range(0, len(ptArrRun2)-1) : histSystYieldPsi2sNormPtRun2.SetBinContent(i+1, yieldPsi2sPtRun2[i]), histSystYieldPsi2sNormPtRun2.SetBinError(i+1, systYieldPsi2sPtRun2[i])
        SetGraSyst(histSystYieldPsi2sNormPtRun2, 20, ROOT.kBlack)
        histSystYieldPsi2sNormPtRun2.Scale(1. / histSystYieldPsi2sNormPtRun2.Integral(), "WIDTH")
        
        # Acceptance-efficiency
        histAxeJpsiPt = TH1F("histAxeJpsiPt", "", len(ptArr)-1, ptArr)
        for i in range(0, len(ptArr)-1) : histAxeJpsiPt.SetBinContent(i+1, axeJpsiPt[i]), histAxeJpsiPt.SetBinError(i+1, statAxeJpsiPt[i])
        SetGraStat(histAxeJpsiPt, 20, ROOT.kRed+1)

        histAxePsi2sPt = TH1F("histAxePsi2sPt", "", len(ptArr)-1, ptArr)
        for i in range(0, len(ptArr)-1) : histAxePsi2sPt.SetBinContent(i+1, axePsi2sPt[i]), histAxePsi2sPt.SetBinError(i+1, statAxePsi2sPt[i])
        SetGraStat(histAxePsi2sPt, 20, ROOT.kAzure+4)

        #############
        # Plot Yields 
        #############
        legendYieldJpsiVsPsi2sPt = TLegend(0.69, 0.69, 0.89, 0.89, " ", "brNDC")
        SetLegend(legendYieldJpsiVsPsi2sPt)
        legendYieldJpsiVsPsi2sPt.AddEntry(histSystYieldJpsiPt, "J/#psi", "FP")
        legendYieldJpsiVsPsi2sPt.AddEntry(histSystYieldPsi2sPt, "#psi(2S)", "FP")

        canvasYieldJpsiPt = TCanvas("canvasYieldJpsiPt", "canvasYieldJpsiPt", 800, 600)
        ROOT.gPad.SetLogy(1)
        histGridYieldJpsiPt  = TH2F("histGridYieldJpsiPt", "", 100, 0, 20, 100, 10, 5e5)
        histGridYieldJpsiPt.GetXaxis().SetTitle("#it{p}_{T} (Gev/#it{c})")
        histGridYieldJpsiPt.GetYaxis().SetTitle("Raw yield")
        histGridYieldJpsiPt.Draw()
        histSystYieldJpsiPt.Draw("E2 SAME")
        histStatYieldJpsiPt.Draw("EP SAME")
        histSystYieldPsi2sPt.Draw("E2 SAME")
        histStatYieldPsi2sPt.Draw("EP SAME")
        legendYieldJpsiVsPsi2sPt.Draw("SAME")
        canvasYieldJpsiPt.SaveAs("figures/jpsi_vs_psi2s_yield_vs_pt.pdf")

        legendYieldJpsiVsPsi2sY = TLegend(0.49, 0.29, 0.69, 0.49, " ", "brNDC")
        SetLegend(legendYieldJpsiVsPsi2sY)
        legendYieldJpsiVsPsi2sY.AddEntry(histSystYieldJpsiY, "J/#psi", "FP")
        legendYieldJpsiVsPsi2sY.AddEntry(histSystYieldPsi2sY, "#psi(2S)", "FP")

        canvasYieldJpsiY = TCanvas("canvasYieldJpsiY", "canvasYieldJpsiY", 800, 600)
        ROOT.gPad.SetLogy(1)
        histGridYieldJpsiY  = TH2F("histGridYieldJpsiY", "", 100, 2.5, 4, 100, 10, 5e6)
        histGridYieldJpsiY.GetXaxis().SetTitle("#it{y}")
        histGridYieldJpsiY.GetYaxis().SetTitle("Raw yield")
        histGridYieldJpsiY.Draw()
        histSystYieldJpsiY.Draw("E2 SAME")
        histStatYieldJpsiY.Draw("EP SAME")
        histSystYieldPsi2sY.Draw("E2 SAME")
        histStatYieldPsi2sY.Draw("EP SAME")
        legendYieldJpsiVsPsi2sY.Draw("SAME")
        canvasYieldJpsiY.SaveAs("figures/jpsi_vs_psi2s_yield_vs_y.pdf")

        ########################
        # Plot Yields normalized 
        ########################
        legendYieldJpsiPt = TLegend(0.69, 0.69, 0.89, 0.89, " ", "brNDC")
        SetLegend(legendYieldJpsiPt)
        legendYieldJpsiPt.AddEntry(histSystYieldJpsiNormPt, "Run3", "FP")
        legendYieldJpsiPt.AddEntry(histSystYieldJpsiNormPtRun2, "Run2", "FP")

        canvasYieldJpsiPt = TCanvas("canvasYieldJpsiPt", "canvasYieldJpsiPt", 800, 600)
        ROOT.gPad.SetLogy(1)
        histGridYieldJpsiPt  = TH2F("histGridYieldJpsiPt", "", 100, 0, 20, 100, 0.001, 1)
        histGridYieldJpsiPt.GetXaxis().SetTitle("#it{p}_{T} (Gev/#it{c})")
        histGridYieldJpsiPt.GetYaxis().SetTitle("Normalized yield")
        histGridYieldJpsiPt.Draw()
        histSystYieldJpsiNormPtRun2.Draw("E2 SAME")
        histStatYieldJpsiNormPtRun2.Draw("EP SAME")
        histSystYieldJpsiNormPt.Draw("E2 SAME")
        histStatYieldJpsiNormPt.Draw("EP SAME")
        legendYieldJpsiPt.Draw("SAME")
        canvasYieldJpsiPt.SaveAs("figures/jpsi_norm_yield_vs_pt.pdf")

        legendYieldPsi2sPt = TLegend(0.69, 0.69, 0.89, 0.89, " ", "brNDC")
        SetLegend(legendYieldPsi2sPt)
        legendYieldPsi2sPt.AddEntry(histSystYieldPsi2sNormPt, "Run3", "FP")
        legendYieldPsi2sPt.AddEntry(histSystYieldPsi2sNormPtRun2, "Run2", "FP")

        canvasYieldPsi2sPt = TCanvas("canvasYieldPsi2sPt", "canvasYieldPsi2sPt", 800, 600)
        ROOT.gPad.SetLogy(1)
        histGridYieldPsi2sPt  = TH2F("histGridYieldPsi2sPt", "", 100, 0, 20, 100, 0.001, 1)
        histGridYieldPsi2sPt.GetXaxis().SetTitle("#it{p}_{T} (Gev/#it{c})")
        histGridYieldPsi2sPt.GetYaxis().SetTitle("Normalized yield")
        histGridYieldPsi2sPt.Draw()
        histSystYieldPsi2sNormPtRun2.Draw("E2 SAME")
        histStatYieldPsi2sNormPtRun2.Draw("EP SAME")
        histSystYieldPsi2sNormPt.Draw("E2 SAME")
        histStatYieldPsi2sNormPt.Draw("EP SAME")
        legendYieldPsi2sPt.Draw("SAME")
        canvasYieldPsi2sPt.SaveAs("figures/psi2s_norm_yield_vs_pt.pdf")

        legendYieldJpsiY = TLegend(0.69, 0.69, 0.89, 0.89, " ", "brNDC")
        SetLegend(legendYieldJpsiY)
        legendYieldJpsiY.AddEntry(histSystYieldJpsiNormY, "Run3", "FP")
        legendYieldJpsiY.AddEntry(histSystYieldJpsiNormYRun2, "Run2", "FP")

        canvasYieldJpsiY = TCanvas("canvasYieldJpsiY", "canvasYieldJpsiY", 800, 600)
        ROOT.gPad.SetLogy(1)
        histGridYieldJpsiY  = TH2F("histGridYieldJpsiY", "", 100, 2.5, 4, 100, 0.03, 1)
        histGridYieldJpsiY.GetXaxis().SetTitle("#it{y}")
        histGridYieldJpsiY.GetYaxis().SetTitle("Normalized yield")
        histGridYieldJpsiY.Draw()
        histSystYieldJpsiNormYRun2.Draw("E2 SAME")
        histStatYieldJpsiNormYRun2.Draw("EP SAME")
        histSystYieldJpsiNormY.Draw("E2 SAME")
        histStatYieldJpsiNormY.Draw("EP SAME")
        legendYieldJpsiY.Draw("SAME")
        canvasYieldJpsiY.SaveAs("figures/jpsi_norm_yield_vs_y.pdf")

        legendYieldPsi2sY = TLegend(0.69, 0.69, 0.89, 0.89, " ", "brNDC")
        SetLegend(legendYieldPsi2sY)
        legendYieldPsi2sY.AddEntry(histSystYieldPsi2sNormY, "Run3", "FP")
        legendYieldPsi2sY.AddEntry(histSystYieldPsi2sNormYRun2, "Run2", "FP")

        canvasYieldPsi2sY = TCanvas("canvasYieldPsi2sY", "canvasYieldPsi2sY", 800, 600)
        ROOT.gPad.SetLogy(1)
        histGridYieldPsi2sY  = TH2F("histGridYieldPsi2sY", "", 100, 2.5, 4, 100, 0.03, 1)
        histGridYieldPsi2sY.GetXaxis().SetTitle("#it{y}")
        histGridYieldPsi2sY.GetYaxis().SetTitle("Normalized yield")
        histGridYieldPsi2sY.Draw()
        histSystYieldPsi2sNormYRun2.Draw("E2 SAME")
        histStatYieldPsi2sNormYRun2.Draw("EP SAME")
        histSystYieldPsi2sNormY.Draw("E2 SAME")
        histStatYieldPsi2sNormY.Draw("EP SAME")
        legendYieldPsi2sY.Draw("SAME")
        canvasYieldPsi2sY.SaveAs("figures/psi2s_norm_yield_vs_y.pdf")

        ################################
        # Plot the Ratio Psi(2S) / J/psi
        ################################
        measStatRatioY, statMeasStatRatioY = PropagateErrorsOnRatio(yieldJpsiY, statYieldJpsiY, yieldPsi2sY, statYieldPsi2sY)
        measSystRatioY, systMeasSystRatioY = PropagateErrorsOnRatio(yieldJpsiY, systYieldJpsiY, yieldPsi2sY, systYieldPsi2sY)

        measStatRatioPt, statMeasStatRatioPt = PropagateErrorsOnRatio(yieldJpsiPt, statYieldJpsiPt, yieldPsi2sPt, statYieldPsi2sPt)
        measSystRatioPt, systMeasSystRatioPt = PropagateErrorsOnRatio(yieldJpsiPt, systYieldJpsiPt, yieldPsi2sPt, systYieldPsi2sPt)

        graStatRatioY = TGraphErrors(len(yMin), yCentr, measStatRatioY, yWidth, statMeasStatRatioY)
        SetGraStat(graStatRatioY, 20, ROOT.kRed+1)

        graSystRatioY = TGraphErrors(len(yMin), yCentr, measSystRatioY, yWidth, systMeasSystRatioY)
        SetGraSyst(graSystRatioY, 20, ROOT.kRed+1)

        graStatRatioPt = TGraphErrors(len(ptMin), ptCentr, measStatRatioPt, ptWidth, statMeasStatRatioPt)
        SetGraStat(graStatRatioPt, 20, ROOT.kRed+1)

        graSystRatioPt = TGraphErrors(len(ptMin), ptCentr, measSystRatioPt, ptWidth, systMeasSystRatioPt)
        SetGraSyst(graSystRatioPt, 20, ROOT.kRed+1)

        measStatRatioYRun2, statMeasStatRatioYRun2 = PropagateErrorsOnRatio(yieldJpsiYRun2, statYieldJpsiYRun2, yieldPsi2sYRun2, statYieldPsi2sYRun2)
        measSystRatioYRun2, systMeasSystRatioYRun2 = PropagateErrorsOnRatio(yieldJpsiYRun2, systYieldJpsiYRun2, yieldPsi2sYRun2, systYieldPsi2sYRun2)

        measStatRatioPtRun2, statMeasStatRatioPtRun2 = PropagateErrorsOnRatio(yieldJpsiPtRun2, statYieldJpsiPtRun2, yieldPsi2sPtRun2, statYieldPsi2sPtRun2)
        measSystRatioPtRun2, systMeasSystRatioPtRun2 = PropagateErrorsOnRatio(yieldJpsiPtRun2, systYieldJpsiPtRun2, yieldPsi2sPtRun2, systYieldPsi2sPtRun2)

        graStatRatioYRun2 = TGraphErrors(len(yMinRun2), yCentrRun2, measStatRatioYRun2, yWidthRun2, statMeasStatRatioYRun2)
        SetGraStat(graStatRatioYRun2, 20, ROOT.kBlack)

        graSystRatioYRun2 = TGraphErrors(len(yMinRun2), yCentrRun2, measSystRatioYRun2, yWidthRun2, systMeasSystRatioYRun2)
        SetGraSyst(graSystRatioYRun2, 20, ROOT.kBlack)

        graStatRatioPtRun2 = TGraphErrors(len(ptMinRun2), ptCentrRun2, measStatRatioPtRun2, ptWidthRun2, statMeasStatRatioPtRun2)
        SetGraStat(graStatRatioPtRun2, 20, ROOT.kBlack)

        graSystRatioPtRun2 = TGraphErrors(len(ptMinRun2), ptCentrRun2, measSystRatioPtRun2, ptWidthRun2, systMeasSystRatioPtRun2)
        SetGraSyst(graSystRatioPtRun2, 20, ROOT.kBlack)

        legendRatioY = TLegend(0.19, 0.39, 0.39, 0.69, " ", "brNDC")
        SetLegend(legendRatioY)
        legendRatioY.AddEntry(graSystRatioY, "Run3", "FP")
        legendRatioY.AddEntry(graSystRatioYRun2, "Run2", "FP")
        
        canvasRatioY = TCanvas("canvasRatioY", "canvasRatioY", 800, 600)
        ROOT.gPad.SetLogy(1)
        histGridRatioY  = TH2F("histGridRatioY", "", 100, 2.5, 4, 100, 0, 0.10)
        histGridRatioY.GetXaxis().SetTitle("#it{y}")
        histGridRatioY.GetYaxis().SetTitle("#psi(2S) / J/#psi")
        histGridRatioY.Draw()
        graSystRatioYRun2.Draw("E2 SAME")
        graStatRatioYRun2.Draw("EP SAME")
        graSystRatioY.Draw("E2 SAME")
        graStatRatioY.Draw("EP SAME")
        legendRatioY.Draw("SAME")
        canvasRatioY.SaveAs("figures/psi2s_over_jpsi_vs_y.pdf")

        legendRatioPt = TLegend(0.69, 0.49, 0.89, 0.69, " ", "brNDC")
        SetLegend(legendRatioPt)
        legendRatioPt.AddEntry(graSystRatioPt, "Run3", "FP")
        legendRatioPt.AddEntry(graSystRatioPtRun2, "Run2", "FP")

        canvasRatioPt = TCanvas("canvasRatioPt", "canvasRatioPt", 800, 600)
        ROOT.gPad.SetLogy(1)
        histGridRatioPt  = TH2F("histGridRatioPt", "", 100, 0, 20, 100, 0, 0.10)
        histGridRatioPt.GetXaxis().SetTitle("#it{p}_{T} (GeV/#it{c}")
        histGridRatioPt.GetYaxis().SetTitle("#psi(2S) / J/#psi")
        histGridRatioPt.Draw()
        graSystRatioPtRun2.Draw("E2 SAME")
        graStatRatioPtRun2.Draw("EP SAME")
        graSystRatioPt.Draw("E2 SAME")
        graStatRatioPt.Draw("EP SAME")
        legendRatioPt.Draw("EP SAME")
        canvasRatioPt.SaveAs("figures/psi2s_over_jpsi_vs_pt.pdf")


        ######################################
        # Plot corrected Ratio Psi(2S) / J/psi
        ######################################
        canvasAxeY = TCanvas("canvasAxeY", "canvasAxeY", 800, 600)
        ROOT.gPad.SetLogy(1)
        histGridAxeY  = TH2F("histGridAxeY", "", 100, 2.5, 4, 100, 0.01, 1)
        histGridAxeY.GetXaxis().SetTitle("#it{y}")
        histGridAxeY.GetYaxis().SetTitle("A#times#varepsilon")
        histGridAxeY.Draw()
        histAxeJpsiY.Draw("HE SAME")
        histAxePsi2sY.Draw("HE SAME")
        canvasAxeY.SaveAs("figures/axe_jpsi_psi2s_vs_y.pdf")

        canvasAxePt = TCanvas("canvasAxePt", "canvasAxePt", 800, 600)
        ROOT.gPad.SetLogy(1)
        histGridAxePt  = TH2F("histGridAxePt", "", 100, 0, 20, 100, 0.1, 1)
        histGridAxePt.GetXaxis().SetTitle("#it{p}_{T} (GeV/#it{c}")
        histGridAxePt.GetYaxis().SetTitle("A#times#varepsilon")
        histGridAxePt.Draw()
        histAxeJpsiPt.Draw("HE SAME")
        histAxePsi2sPt.Draw("HE SAME")
        canvasAxePt.SaveAs("figures/axe_jpsi_psi2s_vs_pt.pdf")

        # Compute and plot the corrected yield
        corrYieldJpsiY, statCorrYieldJpsiY = PropagateErrorsOnRatio(axeJpsiY, statAxeJpsiY, yieldJpsiY, statYieldJpsiY)
        corrYieldJpsiY, systCorrYieldJpsiY = PropagateErrorsOnRatio(axeJpsiY, systAxeJpsiY, yieldJpsiY, systYieldJpsiY)
        corrYieldJpsiY = corrYieldJpsiY / brJpsiToMuMu
        statCorrYieldJpsiY = statCorrYieldJpsiY / brJpsiToMuMu
        systCorrYieldJpsiY = systCorrYieldJpsiY / brJpsiToMuMu

        corrYieldPsi2sY, statCorrYieldPsi2sY = PropagateErrorsOnRatio(axePsi2sY, statAxePsi2sY, yieldPsi2sY, statYieldPsi2sY)
        corrYieldPsi2sY, systCorrYieldPsi2sY = PropagateErrorsOnRatio(axePsi2sY, systAxePsi2sY, yieldPsi2sY, systYieldPsi2sY)
        corrYieldPsi2sY = corrYieldPsi2sY / brPsi2sToMuMu
        statCorrYieldPsi2sY = statCorrYieldPsi2sY / brPsi2sToMuMu
        systCorrYieldPsi2sY = systCorrYieldPsi2sY / brPsi2sToMuMu

        corrYieldJpsiPt, statCorrYieldJpsiPt = PropagateErrorsOnRatio(axeJpsiPt, statAxeJpsiPt, yieldJpsiPt, statYieldJpsiPt)
        corrYieldJpsiPt, systCorrYieldJpsiPt = PropagateErrorsOnRatio(axeJpsiPt, systAxeJpsiPt, yieldJpsiPt, systYieldJpsiPt)
        corrYieldJpsiPt = corrYieldJpsiPt / brJpsiToMuMu
        statCorrYieldJpsiPt = statCorrYieldJpsiPt / brJpsiToMuMu
        systCorrYieldJpsiPt = systCorrYieldJpsiPt / brJpsiToMuMu

        corrYieldPsi2sPt, statCorrYieldPsi2sPt = PropagateErrorsOnRatio(axePsi2sPt, statAxePsi2sPt, yieldPsi2sPt, statYieldPsi2sPt)
        corrYieldPsi2sPt, systCorrYieldPsi2sPt = PropagateErrorsOnRatio(axePsi2sPt, systAxePsi2sPt, yieldPsi2sPt, systYieldPsi2sPt)
        corrYieldPsi2sPt = corrYieldPsi2sPt / brPsi2sToMuMu
        statCorrYieldPsi2sPt = statCorrYieldPsi2sPt / brPsi2sToMuMu
        systCorrYieldPsi2sPt = systCorrYieldPsi2sPt / brPsi2sToMuMu

        histStatCorrYieldJpsiY = TH1F("histStatCorrYieldJpsiY", "", len(yArr)-1, yArr)
        for i in range(0, len(yArr)-1) : histStatCorrYieldJpsiY.SetBinContent(i+1, corrYieldJpsiY[i]), histStatCorrYieldJpsiY.SetBinError(i+1, statCorrYieldJpsiY[i])
        SetGraStat(histStatCorrYieldJpsiY, 20, ROOT.kRed+1)
        histStatCorrYieldJpsiY.Scale(1., "WIDTH")

        histSystCorrYieldJpsiY = TH1F("histSystCorrYieldJpsiY", "", len(yArr)-1, yArr)
        for i in range(0, len(yArr)-1) : histSystCorrYieldJpsiY.SetBinContent(i+1, corrYieldJpsiY[i]), histSystCorrYieldJpsiY.SetBinError(i+1, systCorrYieldJpsiY[i])
        SetGraSyst(histSystCorrYieldJpsiY, 20, ROOT.kRed+1)
        histSystCorrYieldJpsiY.Scale(1., "WIDTH")

        histStatCorrYieldPsi2sY = TH1F("histStatCorrYieldPsi2sY", "", len(yArr)-1, yArr)
        for i in range(0, len(yArr)-1) : histStatCorrYieldPsi2sY.SetBinContent(i+1, corrYieldPsi2sY[i]), histStatCorrYieldPsi2sY.SetBinError(i+1, statCorrYieldPsi2sY[i])
        SetGraStat(histStatCorrYieldPsi2sY, 20, ROOT.kAzure+4)
        histStatCorrYieldPsi2sY.Scale(1., "WIDTH")

        histSystCorrYieldPsi2sY = TH1F("histSystCorrYieldPsi2sY", "", len(yArr)-1, yArr)
        for i in range(0, len(yArr)-1) : histSystCorrYieldPsi2sY.SetBinContent(i+1, corrYieldPsi2sY[i]), histSystCorrYieldPsi2sY.SetBinError(i+1, systCorrYieldPsi2sY[i])
        SetGraSyst(histSystCorrYieldPsi2sY, 20, ROOT.kAzure+4)
        histSystCorrYieldPsi2sY.Scale(1., "WIDTH")

        histStatCorrYieldJpsiPt = TH1F("histStatCorrYieldJpsiPt", "", len(ptArr)-1, ptArr)
        for i in range(0, len(ptArr)-1) : histStatCorrYieldJpsiPt.SetBinContent(i+1, corrYieldJpsiPt[i]), histStatCorrYieldJpsiPt.SetBinError(i+1, statCorrYieldJpsiPt[i])
        SetGraStat(histStatCorrYieldJpsiPt, 20, ROOT.kRed+1)
        histStatCorrYieldJpsiPt.Scale(1., "WIDTH")

        histSystCorrYieldJpsiPt = TH1F("histSystCorrYieldJpsiPt", "", len(ptArr)-1, ptArr)
        for i in range(0, len(ptArr)-1) : histSystCorrYieldJpsiPt.SetBinContent(i+1, corrYieldJpsiPt[i]), histSystCorrYieldJpsiPt.SetBinError(i+1, systCorrYieldJpsiPt[i])
        SetGraSyst(histSystCorrYieldJpsiPt, 20, ROOT.kRed+1)
        histSystCorrYieldJpsiPt.Scale(1., "WIDTH")

        histStatCorrYieldPsi2sPt = TH1F("histStatCorrYieldPsi2sPt", "", len(ptArr)-1, ptArr)
        for i in range(0, len(ptArr)-1) : histStatCorrYieldPsi2sPt.SetBinContent(i+1, corrYieldPsi2sPt[i]), histStatCorrYieldPsi2sPt.SetBinError(i+1, statCorrYieldPsi2sPt[i])
        SetGraStat(histStatCorrYieldPsi2sPt, 20, ROOT.kAzure+4)
        histStatCorrYieldPsi2sPt.Scale(1., "WIDTH")

        histSystCorrYieldPsi2sPt = TH1F("histSystCorrYieldPsi2sPt", "", len(ptArr)-1, ptArr)
        for i in range(0, len(ptArr)-1) : histSystCorrYieldPsi2sPt.SetBinContent(i+1, corrYieldPsi2sPt[i]), histSystCorrYieldPsi2sPt.SetBinError(i+1, systCorrYieldPsi2sPt[i])
        SetGraSyst(histSystCorrYieldPsi2sPt, 20, ROOT.kAzure+4)
        histSystCorrYieldPsi2sPt.Scale(1., "WIDTH")

        canvasCorrYieldJpsiY = TCanvas("canvasCorrYieldJpsiY", "canvasCorrYieldJpsiY", 800, 600)
        ROOT.gPad.SetLogy(1)
        histGridCorrYieldJpsiY  = TH2F("histGridCorrYieldJpsiY", "", 100, 2.5, 4, 100, 1e3, 1e9)
        histGridCorrYieldJpsiY.GetXaxis().SetTitle("#it{y}")
        histGridCorrYieldJpsiY.GetYaxis().SetTitle("d#it{N} / (d#it{p}_{T} * A#times#varepsilon * BR)")
        histGridCorrYieldJpsiY.Draw()
        histSystCorrYieldJpsiY.Draw("E2 SAME")
        histStatCorrYieldJpsiY.Draw("EP SAME")
        histSystCorrYieldPsi2sY.Draw("E2 SAME")
        histStatCorrYieldPsi2sY.Draw("EP SAME")
        legendYieldJpsiVsPsi2sY.Draw("SAME")
        canvasCorrYieldJpsiY.SaveAs("figures/jpsi_vs_psi2s_corr_yield_vs_y.pdf")

        canvasCorrYieldJpsiPt = TCanvas("canvasCorrYieldJpsiPt", "canvasCorrYieldJpsiPt", 800, 600)
        ROOT.gPad.SetLogy(1)
        histGridCorrYieldJpsiPt  = TH2F("histGridCorrYieldJpsiPt", "", 100, 0, 20, 100, 1e3, 1e9)
        histGridCorrYieldJpsiPt.GetXaxis().SetTitle("#it{p}_{T} (Gev/#it{c})")
        histGridCorrYieldJpsiPt.GetYaxis().SetTitle("d#it{N} / (d#it{p}_{T} * A#times#varepsilon * BR)")
        histGridCorrYieldJpsiPt.Draw()
        histSystCorrYieldJpsiPt.Draw("E2 SAME")
        histStatCorrYieldJpsiPt.Draw("EP SAME")
        histSystCorrYieldPsi2sPt.Draw("E2 SAME")
        histStatCorrYieldPsi2sPt.Draw("EP SAME")
        legendYieldJpsiVsPsi2sPt.Draw("SAME")
        canvasCorrYieldJpsiPt.SaveAs("figures/jpsi_vs_psi2s_corr_yield_vs_pt.pdf")

        # Compute and plot the cross section ratio
        csRatioY, statCsRatioY = PropagateErrorsOnRatio(corrYieldJpsiY, statCorrYieldJpsiY, corrYieldPsi2sY, statCorrYieldPsi2sY)
        csRatioY, systCsRatioY = PropagateErrorsOnRatio(corrYieldJpsiY, systCorrYieldJpsiY, corrYieldPsi2sY, systCorrYieldPsi2sY)

        csRatioPt, statCsRatioPt = PropagateErrorsOnRatio(corrYieldJpsiPt, statCorrYieldJpsiPt, corrYieldPsi2sPt, statCorrYieldPsi2sPt)
        csRatioPt, systCsRatioPt = PropagateErrorsOnRatio(corrYieldJpsiPt, systCorrYieldJpsiPt, corrYieldPsi2sPt, systCorrYieldPsi2sPt)

        graStatCsRatioY = TGraphErrors(len(yMin), yCentr, csRatioY, yWidth, statCsRatioY)
        SetGraStat(graStatCsRatioY, 20, ROOT.kRed+1)

        graSystCsRatioY = TGraphErrors(len(yMin), yCentr, csRatioY, yWidth, systCsRatioY)
        SetGraSyst(graSystCsRatioY, 20, ROOT.kRed+1)

        graStatCsRatioPt = TGraphErrors(len(ptMin), ptCentr, csRatioPt, ptWidth, statCsRatioPt)
        SetGraStat(graStatCsRatioPt, 20, ROOT.kRed+1)

        graSystCsRatioPt = TGraphErrors(len(ptMin), ptCentr, csRatioPt, ptWidth, systCsRatioPt)
        SetGraSyst(graSystCsRatioPt, 20, ROOT.kRed+1)

        graStatCsRatioYRun2 = TGraphErrors(len(yMinRun2), yCentrRun2, csRatioYRun2, yWidthRun2, statCsRatioYRun2)
        SetGraStat(graStatCsRatioYRun2, 20, ROOT.kBlack)

        graSystCsRatioYRun2 = TGraphErrors(len(yMinRun2), yCentrRun2, csRatioYRun2, yWidthRun2, systCsRatioYRun2)
        SetGraSyst(graSystCsRatioYRun2, 20, ROOT.kBlack)

        graStatCsRatioPtRun2 = TGraphErrors(len(ptMinRun2), ptCentrRun2, csRatioPtRun2, ptWidthRun2, statCsRatioPtRun2)
        SetGraStat(graStatCsRatioPtRun2, 20, ROOT.kBlack)

        graSystCsRatioPtRun2 = TGraphErrors(len(ptMinRun2), ptCentrRun2, csRatioPtRun2, ptWidthRun2, systCsRatioPtRun2)
        SetGraSyst(graSystCsRatioPtRun2, 20, ROOT.kBlack)

        legendCsRatioY = TLegend(0.19, 0.39, 0.39, 0.69, " ", "brNDC")
        SetLegend(legendCsRatioY)
        legendCsRatioY.AddEntry(graSystRatioY, "Run3", "FP")
        legendCsRatioY.AddEntry(graSystRatioYRun2, "Run2", "FP")

        canvasCsRatioY = TCanvas("canvasCsRatioY", "canvasCsRatioY", 800, 600)
        histGridCsRatioY  = TH2F("histGridCsRatioY", "", 100, 2.5, 4, 100, 0, 0.35)
        histGridCsRatioY.GetXaxis().SetTitle("#it{p}_{T} (GeV/#it{c}")
        histGridCsRatioY.GetYaxis().SetTitle("d#sigma_{#psi(2S)}/d#it{y} / d#sigma_{J/#psi}/d#it{y}")
        histGridCsRatioY.Draw()
        graSystCsRatioYRun2.Draw("E2 SAME")
        graStatCsRatioYRun2.Draw("EP SAME")
        graSystCsRatioY.Draw("E2 SAME")
        graStatCsRatioY.Draw("EP SAME")
        legendCsRatioY.Draw("EP SAME")
        canvasCsRatioY.SaveAs("figures/cross_section_psi2s_over_jpsi_vs_y.pdf")

        legendCsRatioPt = TLegend(0.69, 0.69, 0.89, 0.89, " ", "brNDC")
        SetLegend(legendCsRatioPt)
        legendCsRatioPt.AddEntry(graSystRatioPt, "Run3", "FP")
        legendCsRatioPt.AddEntry(graSystRatioPtRun2, "Run2", "FP")

        canvasCsRatioPt = TCanvas("canvasCsRatioPt", "canvasCsRatioPt", 800, 600)
        histGridCsRatioPt  = TH2F("histGridCsRatioPt", "", 100, 0, 20, 100, 0, 0.7)
        histGridCsRatioPt.GetXaxis().SetTitle("#it{p}_{T} (GeV/#it{c}")
        histGridCsRatioPt.GetYaxis().SetTitle("d#sigma_{#psi(2S)}/d^{2}#it{p}_{T}d#it{y} / d#sigma_{J/#psi}/d^{2}#it{p}_{T}d#it{y}")
        histGridCsRatioPt.Draw()
        graSystCsRatioPtRun2.Draw("E2 SAME")
        graStatCsRatioPtRun2.Draw("EP SAME")
        graSystCsRatioPt.Draw("E2 SAME")
        graStatCsRatioPt.Draw("EP SAME")
        legendCsRatioPt.Draw("EP SAME")
        canvasCsRatioPt.SaveAs("figures/cross_section_psi2s_over_jpsi_vs_pt.pdf")



if __name__ == '__main__':
    main()