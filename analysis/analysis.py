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

        ###############
        # Load datasets
        ###############
        # y-dependence
        dfYieldJpsiY = pd.read_csv('/Users/lucamicheletti/GITHUB/dq_fit_library/analysis/output/analysis/LHC22o_medium_apass4_data_run3_tails/systematics/sig_Jpsi_vs_y.txt', sep=' ')
        yMin = dfYieldJpsiY["x_min"].to_numpy()
        yMax = dfYieldJpsiY["x_max"].to_numpy()
        yArr = np.append(yMin, yMax[len(yMin)-1],)
        yCentr = (yMin + yMax) / 2.
        yWidth = (yMax - yMin) / 2.
        yieldJpsiY = dfYieldJpsiY["val"].to_numpy()
        statYieldJpsiY = dfYieldJpsiY["stat"].to_numpy()
        systYieldJpsiY = dfYieldJpsiY["syst"].to_numpy()

        dfYieldPsi2sY = pd.read_csv('/Users/lucamicheletti/GITHUB/dq_fit_library/analysis/output/analysis/LHC22o_medium_apass4_data_run3_tails/systematics/sig_Psi2s_vs_y.txt', sep=' ')
        yieldPsi2sY = dfYieldPsi2sY["val"].to_numpy()
        statYieldPsi2sY = dfYieldPsi2sY["stat"].to_numpy()
        systYieldPsi2sY = dfYieldPsi2sY["syst"].to_numpy()

        dfYieldJpsiY = pd.read_csv('run2_results/sig_Jpsi_vs_y_run2.txt', sep=' ')
        yieldJpsiYRun2 = dfYieldJpsiY["val"].to_numpy()
        statYieldJpsiYRun2 = dfYieldJpsiY["stat"].to_numpy()
        systYieldJpsiYRun2 = dfYieldJpsiY["syst"].to_numpy()

        dfYieldPsi2sY = pd.read_csv('run2_results/sig_Psi2s_vs_y_run2.txt', sep=' ')
        yieldPsi2sYRun2 = dfYieldPsi2sY["val"].to_numpy()
        statYieldPsi2sYRun2 = dfYieldPsi2sY["stat"].to_numpy()
        systYieldPsi2sYRun2 = dfYieldPsi2sY["syst"].to_numpy()

        # pt-dependence
        dfYieldJpsiPt = pd.read_csv('/Users/lucamicheletti/GITHUB/dq_fit_library/analysis/output/analysis/LHC22o_medium_apass4_data_run3_tails/nicolas_results/systematics/sig_Jpsi_vs_pt.txt', sep=' ')
        ptMin = dfYieldJpsiPt["x_min"].to_numpy()
        ptMax = dfYieldJpsiPt["x_max"].to_numpy()
        ptArr = np.append(ptMin, ptMax[len(ptMin)-1],)
        ptCentr = (ptMin + ptMax) / 2.
        ptWidth = (ptMax - ptMin) / 2.
        yieldJpsiPt = dfYieldJpsiPt["val"].to_numpy()
        statYieldJpsiPt = dfYieldJpsiPt["stat"].to_numpy()
        systYieldJpsiPt = dfYieldJpsiPt["syst"].to_numpy()

        dfYieldPsi2sPt = pd.read_csv('/Users/lucamicheletti/GITHUB/dq_fit_library/analysis/output/analysis/LHC22o_medium_apass4_data_run3_tails/nicolas_results/systematics/sig_Psi2s_vs_pt.txt', sep=' ')
        yieldPsi2sPt = dfYieldPsi2sPt["val"].to_numpy()
        statYieldPsi2sPt = dfYieldPsi2sPt["stat"].to_numpy()
        systYieldPsi2sPt = dfYieldPsi2sPt["syst"].to_numpy()

        dfYieldJpsiPt = pd.read_csv('run2_results/sig_Jpsi_vs_pt_run2.txt', sep=' ')
        yieldJpsiPtRun2 = dfYieldJpsiPt["val"].to_numpy()
        statYieldJpsiPtRun2 = dfYieldJpsiPt["stat"].to_numpy()
        systYieldJpsiPtRun2 = dfYieldJpsiPt["syst"].to_numpy()

        dfYieldPsi2sY = pd.read_csv('run2_results/sig_Psi2s_vs_pt_run2.txt', sep=' ')
        yieldPsi2sPtRun2 = dfYieldPsi2sY["val"].to_numpy()
        statYieldPsi2sPtRun2 = dfYieldPsi2sY["stat"].to_numpy()
        systYieldPsi2sPtRun2 = dfYieldPsi2sY["syst"].to_numpy()

        ############################
        # Create and fill histograms
        ############################
        # y-dependence
        histStatYieldJpsiY = TH1F("histStatYieldJpsiY", "", len(yArr)-1, yArr)
        for i in range(0, len(yArr)-1) : histStatYieldJpsiY.SetBinContent(i+1, yieldJpsiY[i]), histStatYieldJpsiY.SetBinError(i+1, statYieldJpsiY[i])
        SetGraStat(histStatYieldJpsiY, 20, ROOT.kRed+1)
        histStatYieldJpsiY.Scale(1. / histStatYieldJpsiY.Integral())

        histSystYieldJpsiY = TH1F("histSystYieldJpsiY", "", len(yArr)-1, yArr)
        for i in range(0, len(yArr)-1) : histSystYieldJpsiY.SetBinContent(i+1, yieldJpsiY[i]), histSystYieldJpsiY.SetBinError(i+1, systYieldJpsiY[i])
        SetGraSyst(histSystYieldJpsiY, 20, ROOT.kRed+1)
        histSystYieldJpsiY.Scale(1. / histSystYieldJpsiY.Integral())

        histStatYieldPsi2sY = TH1F("histStatYieldPsi2sY", "", len(yArr)-1, yArr)
        for i in range(0, len(yArr)-1) : histStatYieldPsi2sY.SetBinContent(i+1, yieldPsi2sY[i]), histStatYieldPsi2sY.SetBinError(i+1, statYieldPsi2sY[i])
        SetGraStat(histStatYieldPsi2sY, 20, ROOT.kAzure+4)
        histStatYieldPsi2sY.Scale(1. / histStatYieldPsi2sY.Integral())

        histSystYieldPsi2sY = TH1F("histSystYieldPsi2sY", "", len(yArr)-1, yArr)
        for i in range(0, len(yArr)-1) : histSystYieldPsi2sY.SetBinContent(i+1, yieldPsi2sY[i]), histSystYieldPsi2sY.SetBinError(i+1, systYieldPsi2sY[i])
        SetGraSyst(histSystYieldPsi2sY, 20, ROOT.kAzure+4)
        histSystYieldPsi2sY.Scale(1. / histSystYieldPsi2sY.Integral())

        # Run2
        histStatYieldJpsiYRun2 = TH1F("histStatYieldJpsiYRun2", "", len(yArr)-1, yArr)
        for i in range(0, len(yArr)-1) : histStatYieldJpsiYRun2.SetBinContent(i+1, yieldJpsiYRun2[i]), histStatYieldJpsiYRun2.SetBinError(i+1, statYieldJpsiYRun2[i])
        SetGraStat(histStatYieldJpsiYRun2, 20, ROOT.kBlack)
        histStatYieldJpsiYRun2.Scale(1. / histStatYieldJpsiYRun2.Integral())

        histSystYieldJpsiYRun2 = TH1F("histSystYieldJpsiYRun2", "", len(yArr)-1, yArr)
        for i in range(0, len(yArr)-1) : histSystYieldJpsiYRun2.SetBinContent(i+1, yieldJpsiYRun2[i]), histSystYieldJpsiYRun2.SetBinError(i+1, systYieldJpsiYRun2[i])
        SetGraSyst(histSystYieldJpsiYRun2, 20, ROOT.kBlack)
        histSystYieldJpsiYRun2.Scale(1. / histSystYieldJpsiYRun2.Integral())

        histStatYieldPsi2sYRun2 = TH1F("histStatYieldPsi2sYRun2", "", len(yArr)-1, yArr)
        for i in range(0, len(yArr)-1) : histStatYieldPsi2sYRun2.SetBinContent(i+1, yieldPsi2sYRun2[i]), histStatYieldPsi2sYRun2.SetBinError(i+1, statYieldPsi2sYRun2[i])
        SetGraStat(histStatYieldPsi2sYRun2, 20, ROOT.kBlack)
        histStatYieldPsi2sYRun2.Scale(1. / histStatYieldPsi2sYRun2.Integral())

        histSystYieldPsi2sYRun2 = TH1F("histSystYieldPsi2sYRun2", "", len(yArr)-1, yArr)
        for i in range(0, len(yArr)-1) : histSystYieldPsi2sYRun2.SetBinContent(i+1, yieldPsi2sYRun2[i]), histSystYieldPsi2sYRun2.SetBinError(i+1, systYieldPsi2sYRun2[i])
        SetGraSyst(histSystYieldPsi2sYRun2, 20, ROOT.kBlack)
        histSystYieldPsi2sYRun2.Scale(1. / histSystYieldPsi2sYRun2.Integral())

        # pt-dependence
        histStatYieldJpsiPt = TH1F("histStatYieldJpsiPt", "", len(ptArr)-1, ptArr)
        for i in range(0, len(ptArr)-1) : histStatYieldJpsiPt.SetBinContent(i+1, yieldJpsiPt[i]), histStatYieldJpsiPt.SetBinError(i+1, statYieldJpsiPt[i])
        SetGraStat(histStatYieldJpsiPt, 20, ROOT.kRed+1)
        histStatYieldJpsiPt.Scale(1. / histStatYieldJpsiPt.Integral(), "WIDTH")

        histSystYieldJpsiPt = TH1F("histSystYieldJpsiPt", "", len(ptArr)-1, ptArr)
        for i in range(0, len(ptArr)-1) : histSystYieldJpsiPt.SetBinContent(i+1, yieldJpsiPt[i]), histSystYieldJpsiPt.SetBinError(i+1, systYieldJpsiPt[i])
        SetGraSyst(histSystYieldJpsiPt, 20, ROOT.kRed+1)
        histSystYieldJpsiPt.Scale(1. / histSystYieldJpsiPt.Integral(), "WIDTH")

        histStatYieldPsi2sPt = TH1F("histStatYieldPsi2sPt", "", len(ptArr)-1, ptArr)
        for i in range(0, len(ptArr)-1) : histStatYieldPsi2sPt.SetBinContent(i+1, yieldPsi2sPt[i]), histStatYieldPsi2sPt.SetBinError(i+1, statYieldPsi2sPt[i])
        SetGraStat(histStatYieldPsi2sPt, 20, ROOT.kAzure+4)
        histStatYieldPsi2sPt.Scale(1. / histStatYieldPsi2sPt.Integral(), "WIDTH")

        histSystYieldPsi2sPt = TH1F("histSystYieldPsi2sPt", "", len(ptArr)-1, ptArr)
        for i in range(0, len(ptArr)-1) : histSystYieldPsi2sPt.SetBinContent(i+1, yieldPsi2sPt[i]), histSystYieldPsi2sPt.SetBinError(i+1, systYieldPsi2sPt[i])
        SetGraSyst(histSystYieldPsi2sPt, 20, ROOT.kAzure+4)
        histSystYieldPsi2sPt.Scale(1. / histSystYieldPsi2sPt.Integral(), "WIDTH")

        # Run2
        histStatYieldJpsiPtRun2 = TH1F("histStatYieldJpsiPtRun2", "", len(ptArr)-1, ptArr)
        for i in range(0, len(ptArr)-1) : histStatYieldJpsiPtRun2.SetBinContent(i+1, yieldJpsiPtRun2[i]), histStatYieldJpsiPtRun2.SetBinError(i+1, statYieldJpsiPtRun2[i])
        SetGraStat(histStatYieldJpsiPtRun2, 20, ROOT.kBlack)
        histStatYieldJpsiPtRun2.Scale(1. / histStatYieldJpsiPtRun2.Integral(), "WIDTH")

        histSystYieldJpsiPtRun2 = TH1F("histSystYieldJpsiPtRun2", "", len(ptArr)-1, ptArr)
        for i in range(0, len(ptArr)-1) : histSystYieldJpsiPtRun2.SetBinContent(i+1, yieldJpsiPtRun2[i]), histSystYieldJpsiPtRun2.SetBinError(i+1, systYieldJpsiPtRun2[i])
        SetGraSyst(histSystYieldJpsiPtRun2, 20, ROOT.kBlack)
        histSystYieldJpsiPtRun2.Scale(1. / histSystYieldJpsiPtRun2.Integral(), "WIDTH")

        histStatYieldPsi2sPtRun2 = TH1F("histStatYieldPsi2sPtRun2", "", len(ptArr)-1, ptArr)
        for i in range(0, len(ptArr)-1) : histStatYieldPsi2sPtRun2.SetBinContent(i+1, yieldPsi2sPtRun2[i]), histStatYieldPsi2sPtRun2.SetBinError(i+1, statYieldPsi2sPtRun2[i])
        SetGraStat(histStatYieldPsi2sPtRun2, 20, ROOT.kBlack)
        histStatYieldPsi2sPtRun2.Scale(1. / histStatYieldPsi2sPtRun2.Integral(), "WIDTH")

        histSystYieldPsi2sPtRun2 = TH1F("histSystYieldPsi2sPtRun2", "", len(ptArr)-1, ptArr)
        for i in range(0, len(ptArr)-1) : histSystYieldPsi2sPtRun2.SetBinContent(i+1, yieldPsi2sPtRun2[i]), histSystYieldPsi2sPtRun2.SetBinError(i+1, systYieldPsi2sPtRun2[i])
        SetGraSyst(histSystYieldPsi2sPtRun2, 20, ROOT.kBlack)
        histSystYieldPsi2sPtRun2.Scale(1. / histSystYieldPsi2sPtRun2.Integral(), "WIDTH")

        ########################
        # Plot Yields normalized 
        ########################
        legendYieldJpsiPt = TLegend(0.69, 0.69, 0.89, 0.89, " ", "brNDC")
        SetLegend(legendYieldJpsiPt)
        legendYieldJpsiPt.AddEntry(histSystYieldJpsiPt, "Run3", "FP")
        legendYieldJpsiPt.AddEntry(histSystYieldJpsiPtRun2, "Run2", "FP")

        canvasYieldJpsiPt = TCanvas("canvasYieldJpsiPt", "canvasYieldJpsiPt", 800, 600)
        ROOT.gPad.SetLogy(1)
        histGridYieldJpsiPt  = TH2F("histGridYieldJpsiPt", "", 100, 0, 20, 100, 0.001, 1)
        histGridYieldJpsiPt.GetXaxis().SetTitle("#it{p}_{T} (Gev/#it{c})")
        histGridYieldJpsiPt.GetYaxis().SetTitle("Normalized yield")
        histGridYieldJpsiPt.Draw()
        histSystYieldJpsiPtRun2.Draw("E2 SAME")
        histStatYieldJpsiPtRun2.Draw("EP SAME")
        histSystYieldJpsiPt.Draw("E2 SAME")
        histStatYieldJpsiPt.Draw("EP SAME")
        legendYieldJpsiPt.Draw("SAME")
        canvasYieldJpsiPt.SaveAs("jpsi_norm_yield_vs_pt.pdf")

        legendYieldPsi2sPt = TLegend(0.69, 0.69, 0.89, 0.89, " ", "brNDC")
        SetLegend(legendYieldPsi2sPt)
        legendYieldPsi2sPt.AddEntry(histSystYieldPsi2sPt, "Run3", "FP")
        legendYieldPsi2sPt.AddEntry(histSystYieldPsi2sPtRun2, "Run2", "FP")

        canvasYieldPsi2sPt = TCanvas("canvasYieldPsi2sPt", "canvasYieldPsi2sPt", 800, 600)
        ROOT.gPad.SetLogy(1)
        histGridYieldPsi2sPt  = TH2F("histGridYieldPsi2sPt", "", 100, 0, 20, 100, 0.001, 1)
        histGridYieldPsi2sPt.GetXaxis().SetTitle("#it{y}")
        histGridYieldPsi2sPt.GetYaxis().SetTitle("Normalized yield")
        histGridYieldPsi2sPt.Draw()
        histSystYieldPsi2sPtRun2.Draw("E2 SAME")
        histStatYieldPsi2sPtRun2.Draw("EP SAME")
        histSystYieldPsi2sPt.Draw("E2 SAME")
        histStatYieldPsi2sPt.Draw("EP SAME")
        legendYieldPsi2sPt.Draw("SAME")
        canvasYieldPsi2sPt.SaveAs("psi2s_norm_yield_vs_pt.pdf")

        legendYieldJpsiY = TLegend(0.69, 0.69, 0.89, 0.89, " ", "brNDC")
        SetLegend(legendYieldJpsiY)
        legendYieldJpsiY.AddEntry(histSystYieldJpsiY, "Run3", "FP")
        legendYieldJpsiY.AddEntry(histSystYieldJpsiYRun2, "Run2", "FP")

        canvasYieldJpsiY = TCanvas("canvasYieldJpsiY", "canvasYieldJpsiY", 800, 600)
        ROOT.gPad.SetLogy(1)
        histGridYieldJpsiY  = TH2F("histGridYieldJpsiY", "", 100, 2.5, 4, 100, 0.03, 1)
        histGridYieldJpsiY.GetXaxis().SetTitle("#it{y}")
        histGridYieldJpsiY.GetYaxis().SetTitle("Normalized yield")
        histGridYieldJpsiY.Draw()
        histSystYieldJpsiYRun2.Draw("E2 SAME")
        histStatYieldJpsiYRun2.Draw("EP SAME")
        histSystYieldJpsiY.Draw("E2 SAME")
        histStatYieldJpsiY.Draw("EP SAME")
        legendYieldJpsiY.Draw("SAME")
        canvasYieldJpsiY.SaveAs("jpsi_norm_yield_vs_y.pdf")

        legendYieldPsi2sY = TLegend(0.69, 0.69, 0.89, 0.89, " ", "brNDC")
        SetLegend(legendYieldPsi2sY)
        legendYieldPsi2sY.AddEntry(histSystYieldPsi2sY, "Run3", "FP")
        legendYieldPsi2sY.AddEntry(histSystYieldPsi2sYRun2, "Run2", "FP")

        canvasYieldPsi2sY = TCanvas("canvasYieldPsi2sY", "canvasYieldPsi2sY", 800, 600)
        ROOT.gPad.SetLogy(1)
        histGridYieldPsi2sY  = TH2F("histGridYieldPsi2sY", "", 100, 2.5, 4, 100, 0.03, 1)
        histGridYieldPsi2sY.GetXaxis().SetTitle("#it{y}")
        histGridYieldPsi2sY.GetYaxis().SetTitle("Normalized yield")
        histGridYieldPsi2sY.Draw()
        histSystYieldPsi2sYRun2.Draw("E2 SAME")
        histStatYieldPsi2sYRun2.Draw("EP SAME")
        histSystYieldPsi2sY.Draw("E2 SAME")
        histStatYieldPsi2sY.Draw("EP SAME")
        legendYieldPsi2sY.Draw("SAME")
        canvasYieldPsi2sY.SaveAs("psi2s_norm_yield_vs_y.pdf")

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

        graStatRatioYRun2 = TGraphErrors(len(yMin), yCentr, measStatRatioYRun2, yWidth, statMeasStatRatioYRun2)
        SetGraStat(graStatRatioYRun2, 20, ROOT.kBlack)

        graSystRatioYRun2 = TGraphErrors(len(yMin), yCentr, measSystRatioYRun2, yWidth, systMeasSystRatioYRun2)
        SetGraSyst(graSystRatioYRun2, 20, ROOT.kBlack)

        graStatRatioPtRun2 = TGraphErrors(len(ptMin), ptCentr, measStatRatioPtRun2, ptWidth, statMeasStatRatioPtRun2)
        SetGraStat(graStatRatioPtRun2, 20, ROOT.kBlack)

        graSystRatioPtRun2 = TGraphErrors(len(ptMin), ptCentr, measSystRatioPtRun2, ptWidth, systMeasSystRatioPtRun2)
        SetGraSyst(graSystRatioPtRun2, 20, ROOT.kBlack)

        canvasRatioY = TCanvas("canvasRatioY", "canvasRatioY", 800, 600)
        histGridRatioY  = TH2F("histGridRatioY", "", 100, 2.5, 4, 100, 0, 0.05)
        histGridRatioY.Draw()
        graSystRatioYRun2.Draw("E2 SAME")
        graStatRatioYRun2.Draw("EP SAME")
        graSystRatioY.Draw("E2 SAME")
        graStatRatioY.Draw("EP SAME")
        canvasRatioY.SaveAs("psi2s_over_jpsi_vs_y.pdf")

        canvasRatioPt = TCanvas("canvasRatioPt", "canvasRatioPt", 800, 600)
        histGridRatioPt  = TH2F("histGridRatioPt", "", 100, 0, 20, 100, 0, 0.05)
        histGridRatioPt.Draw()
        graSystRatioPtRun2.Draw("E2 SAME")
        graStatRatioPtRun2.Draw("EP SAME")
        graSystRatioPt.Draw("E2 SAME")
        graStatRatioPt.Draw("EP SAME")
        canvasRatioPt.SaveAs("psi2s_over_jpsi_vs_pt.pdf")

if __name__ == '__main__':
    main()