from telnetlib import DO
import os
import ROOT
from ROOT import TCanvas, TFile, TH1F, TPaveText, RooRealVar, RooDataSet, RooWorkspace, RooDataHist, RooArgSet
from ROOT import gPad, gROOT
from utils.plot_library import DoResidualPlot, DoPullPlot, DoCorrMatPlot, DoAlicePlot, LoadStyle
from utils.plot_library import DoPullPlot, DoCorrMatPlot, DoAlicePlot, LoadStyle

class DQFitter:
    def __init__(self, fInName, fInputName, fOutPath, minDatasetRange, maxDatasetRange):
        self.fPdfDict          = {}
        self.fOutPath          = fOutPath
        self.fFileOutName      = "{}{}__{}_{}.root".format(fOutPath, fInputName, minDatasetRange, maxDatasetRange)
        self.fFileOut          = TFile(self.fFileOutName, "RECREATE")
        self.fFileIn           = TFile.Open(fInName)
        self.fInputName        = fInputName
        self.fInput            = 0
        self.fRooWorkspace     = RooWorkspace('w','workspace')
        self.fParNames         = []
        self.fFitMethod        = "likelyhood"
        self.fFitRangeMin      = []
        self.fFitRangeMax      = []
        self.fTrialName        = ""
        self.fMinDatasetRange  = minDatasetRange
        self.fMaxDatasetRange  = maxDatasetRange
        self.fRooMass          = RooRealVar("m", "#it{M} (GeV/#it{c}^{2})", self.fMinDatasetRange, self.fMaxDatasetRange)
        self.fDoResidualPlot   = False
        self.fDoPullPlot       = False
        self.fDoCorrMatPlot    = False

    def SetFitConfig(self, pdfDict):
        '''
        Method set the configuration of the fit
        '''
        self.fPdfDict = pdfDict
        self.fInput = self.fFileIn.Get(self.fInputName)
        if not "TTree" in self.fInput.ClassName():
            self.fInput.Sumw2()
        self.fFitRangeMin = pdfDict["fitRangeMin"]
        self.fFitRangeMax = pdfDict["fitRangeMax"]
        self.fDoResidualPlot = pdfDict["doResidualPlot"]
        self.fDoPullPlot = pdfDict["doPullPlot"]
        self.fDoCorrMatPlot = pdfDict["doCorrMatPlot"]
        pdfList = []
        for pdf in self.fPdfDict["pdf"][:-1]:
            self.fTrialName = self.fTrialName + pdf + "_"
        
        for i in range(0, len(self.fPdfDict["pdf"])):
            if not self.fPdfDict["pdf"][i] == "SUM":
                gROOT.ProcessLineSync(".x ../fit_library/{}Pdf.cxx+".format(self.fPdfDict["pdf"][i]))
        
        for i in range(0, len(self.fPdfDict["pdf"])):
            parVal = self.fPdfDict["parVal"][i]
            parLimMin = self.fPdfDict["parLimMin"][i]
            parLimMax = self.fPdfDict["parLimMax"][i]
            parName = self.fPdfDict["parName"][i]

            if not len(parVal) == len(parLimMin) == len(parLimMax) == len(parName):
                print("WARNING! Different size if the input parameters in the configuration")
                print(parVal)
                print(parLimMin)
                print(parLimMax)
                print(parName)
                exit()

            if not self.fPdfDict["pdf"][i] == "SUM":
                # Filling parameter list
                for j in range(0, len(parVal)):
                    if ("sum" in parName[j]) or ("prod" in parName[j]):
                        self.fRooWorkspace.factory("{}".format(parName[j]))
                        # Replace the exression of the parameter with the name of the parameter
                        r1 = parName[j].find("::") + 2
                        r2 = parName[j].find("(", r1)
                        parName[j] = parName[j][r1:r2]
                        self.fRooWorkspace.factory("{}[{}]".format(parName[j], parVal[j]))
                    else:
                        if (parLimMin[j] == parLimMax[j]):
                            self.fRooWorkspace.factory("{}[{}]".format(parName[j], parVal[j]))
                        else:
                            self.fRooWorkspace.factory("{}[{},{},{}]".format(parName[j], parVal[j], parLimMin[j], parLimMax[j]))

                        self.fParNames.append(parName[j]) # only free parameters will be reported in the histogram of results

                # Define the pdf associating the parametes previously defined
                nameFunc = self.fPdfDict["pdf"][i]
                #nameFunc += "Pdf::{}Pdf(m[{},{}]".format(self.fPdfDict["pdfName"][i],self.fPdfDict["fitRangeMin"][0],self.fPdfDict["fitRangeMax"][0])
                nameFunc += "Pdf::{}Pdf(m[{},{}]".format(self.fPdfDict["pdfName"][i], self.fMinDatasetRange, self.fMaxDatasetRange)
                pdfList.append(self.fPdfDict["pdfName"][i])
                for j in range(0, len(parVal)):
                    nameFunc += ",{}".format(parName[j])
                nameFunc += ")"
                self.fRooWorkspace.factory(nameFunc)
            else:
                nameFunc = self.fPdfDict["pdf"][i]
                nameFunc += "::sum("
                for j in range(0, len(pdfList)):
                    nameFunc += "{}[{},{},{}]*{}Pdf".format(parName[j], parVal[j], parLimMin[j], parLimMax[j], pdfList[j])
                    self.fParNames.append(parName[j])
                    if not j == len(pdfList) - 1:
                        nameFunc += ","
                nameFunc += ")"
                self.fRooWorkspace.factory(nameFunc)

    def FitInvMassSpectrum(self, fitMethod, fitRangeMin, fitRangeMax):
        '''
        Method to perform the fit to the invariant mass spectrum
        '''
        LoadStyle()
        trialName = self.fTrialName + "_" + str(fitRangeMin) + "_" + str(fitRangeMax)
        self.fRooWorkspace.Print()
        pdf = self.fRooWorkspace.pdf("sum")
        self.fRooMass.setRange("range", fitRangeMin, fitRangeMax)
        fRooPlot = self.fRooMass.frame(ROOT.RooFit.Title(trialName), ROOT.RooFit.Range("range"))
        fRooPlotExtra = self.fRooMass.frame(ROOT.RooFit.Title(trialName), ROOT.RooFit.Range("range"))
        fRooPlotOff = self.fRooMass.frame(ROOT.RooFit.Title(trialName))
        if "TTree" in self.fInput.ClassName():
            print("########### Perform unbinned fit ###########")
            rooDs = RooDataSet("data", "data", RooArgSet(self.fRooMass), ROOT.RooFit.Import(self.fInput))
        else:
            print("########### Perform binned fit ###########")
            rooDs = RooDataHist("data", "data", RooArgSet(self.fRooMass), ROOT.RooFit.Import(self.fInput))

        # Select the fit method
        if fitMethod == "likelyhood":
            print("########### Perform likelyhood fit ###########")
            rooFitRes = ROOT.RooFitResult(pdf.fitTo(rooDs, ROOT.RooFit.Range(fitRangeMin,fitRangeMax),ROOT.RooFit.PrintLevel(-1), ROOT.RooFit.Save()))
        #if fitMethod == "chi2":
            #print("########### Perform X2 fit ###########")
            #rooFitRes = ROOT.RooFitResult(pdf.chi2FitTo(rooDs, ROOT.RooFit.Range(fitRangeMin,fitRangeMax),ROOT.RooFit.PrintLevel(-1), ROOT.RooFit.Save()))

        index = 1
        histResults = TH1F("fit_results_{}".format(trialName), "fit_results_{}".format(trialName), len(self.fParNames), 0., len(self.fParNames))
        # histResults = TH1F("fit_results_{}".format(trialName), "fit_results_{}".format(trialName), len(self.fParNames)+1, 0., len(self.fParNames)+1)
        # index = 2
        # ratio = self.fRooWorkspace.var("sig_Psi2s").getVal() / self.fRooWorkspace.var("sig_Jpsi").getVal()
        # histResults.GetXaxis().SetBinLabel(1,"ratio")
        # histResults.SetBinContent(1,ratio)
        for parName in self.fParNames:
            histResults.GetXaxis().SetBinLabel(index, parName)
            histResults.SetBinContent(index, self.fRooWorkspace.var(parName).getVal())
            histResults.SetBinError(index, self.fRooWorkspace.var(parName).getError())
            index += 1

      
        rooDs.plotOn(fRooPlot, ROOT.RooFit.MarkerStyle(20), ROOT.RooFit.MarkerSize(0.6), ROOT.RooFit.Range(fitRangeMin, fitRangeMax))
        pdf.plotOn(fRooPlot, ROOT.RooFit.LineColor(ROOT.kRed+1), ROOT.RooFit.LineWidth(2), ROOT.RooFit.Range(fitRangeMin, fitRangeMax))
        #pdf.plotOn(fRooPlot, ROOT.RooFit.VisualizeError(rooFitRes, 1), ROOT.RooFit.FillColor(ROOT.kRed-10), ROOT.RooFit.Range(fitRangeMin, fitRangeMax))
        rooDs.plotOn(fRooPlot, ROOT.RooFit.MarkerStyle(20), ROOT.RooFit.MarkerSize(0.6), ROOT.RooFit.Range(fitRangeMin, fitRangeMax))
        pdf.plotOn(fRooPlot, ROOT.RooFit.LineColor(ROOT.kRed+1), ROOT.RooFit.LineWidth(2), ROOT.RooFit.Range(fitRangeMin, fitRangeMax))
        for i in range(0, len(self.fPdfDict["pdf"])):
            if not self.fPdfDict["pdfName"][i] == "SUM":
                pdf.plotOn(fRooPlot, ROOT.RooFit.Components("{}Pdf".format(self.fPdfDict["pdfName"][i])), ROOT.RooFit.LineColor(self.fPdfDict["pdfColor"][i]), ROOT.RooFit.LineStyle(self.fPdfDict["pdfStyle"][i]), ROOT.RooFit.LineWidth(2), ROOT.RooFit.Range(fitRangeMin, fitRangeMax))
        
        extraText = [] # extra text for "propaganda" plots

        paveText = TPaveText(0.60, 0.45, 0.99, 0.94, "brNDC")
        paveText.SetTextFont(42)
        paveText.SetTextSize(0.025)
        paveText.SetFillColor(ROOT.kWhite)
        for parName in self.fParNames:
            paveText.AddText("{} = {:.4f} #pm {:.4f}".format(parName, self.fRooWorkspace.var(parName).getVal(), self.fRooWorkspace.var(parName).getError()))
            if self.fPdfDict["parForAlicePlot"].count(parName) > 0:
                text = self.fPdfDict["parNameForAlicePlot"][self.fPdfDict["parForAlicePlot"].index(parName)]
                if "sig" in parName:
                    extraText.append("{} = {:.0f} #pm {:.0f}".format(text, self.fRooWorkspace.var(parName).getVal(), self.fRooWorkspace.var(parName).getError()))
                else:
                    extraText.append("{} = {:.3f} #pm {:.3f}".format(text, self.fRooWorkspace.var(parName).getVal(), self.fRooWorkspace.var(parName).getError()))
            for i in range(0, len(self.fPdfDict["pdfName"])):
                if self.fPdfDict["pdfName"][i] in parName:
                    (paveText.GetListOfLines().Last()).SetTextColor(self.fPdfDict["pdfColor"][i])


        reduced_chi2 = 0
        if "TTree" in self.fInput.ClassName():
            #Fit with RooChi2Var
            # To Do : Find a way to get the number of bins differently. The following is a temparary solution.
            # WARNING : The largest fit range has to come first in the config file otherwise it does not work
            # Convert unbinned dataset into binned dataset
            rooDsBinned = RooDataHist("rooDsBinned","binned version of rooDs",RooArgSet(self.fRooMass),rooDs)
            nbinsperGev = rooDsBinned.numEntries() / (self.fPdfDict["fitRangeMax"][0] - self.fPdfDict["fitRangeMin"][0])
            nBins = (fitRangeMax - fitRangeMin) * nbinsperGev
        
            chi2 = ROOT.RooChi2Var("chi2", "chi2", pdf, rooDsBinned)
            nPars = rooFitRes.floatParsFinal().getSize()
            ndof = nBins - nPars
            reduced_chi2 = chi2.getVal() / ndof
        else:
            #Fit with RooChi2Var
            # To Do : Find a way to get the number of bins differently. The following is a temparary solution.
            # WARNING : The largest fit range has to come first in the config file otherwise it does not work
            nbinsperGev = rooDs.numEntries() / (self.fPdfDict["fitRangeMax"][0] - self.fPdfDict["fitRangeMin"][0])
            nBins = (fitRangeMax - fitRangeMin) * nbinsperGev
        
            chi2 = ROOT.RooChi2Var("chi2", "chi2", pdf, rooDs)
            nPars = rooFitRes.floatParsFinal().getSize()
            ndof = nBins - nPars
            reduced_chi2 = chi2.getVal() / ndof

        
        # Add the chiSquare value
        paveText.AddText("n Par = %3.2f" % (nPars)) 
        paveText.AddText("n Bins = %3.2f" % (nBins))
        paveText.AddText("#bf{#chi^{2}/dof = %3.2f}" % reduced_chi2)
      
        fRooPlot.addObject(paveText)
        extraText.append("#chi^{2}/dof = %3.2f" % reduced_chi2)
     
        # Fit plot
        canvasFit = TCanvas("fit_plot_{}".format(trialName), "fit_plot_{}".format(trialName), 800, 600)
        canvasFit.SetLeftMargin(0.15)
        gPad.SetLeftMargin(0.15)
        fRooPlot.GetYaxis().SetTitleOffset(1.4)
        fRooPlot.Draw()
        
        # Print the fit result
        rooFitRes.Print()
        
        # Official fit plot
        if self.fPdfDict["doAlicePlot"]:
            DoAlicePlot(rooDs, pdf, fRooPlotOff, self.fPdfDict, self.fInputName, trialName, self.fOutPath, extraText)

        # Save results
        self.fFileOut.cd()
        histResults.Write()
        canvasFit.Write()

        rooDs.plotOn(fRooPlotExtra, ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2), ROOT.RooFit.Range(fitRangeMin, fitRangeMax))
        pdf.plotOn(fRooPlotExtra, ROOT.RooFit.Range(fitRangeMin, fitRangeMax))

        # Residual plot
        if self.fDoResidualPlot:
            canvasResidual = DoResidualPlot(fRooPlotExtra, self.fRooMass, trialName)
            canvasResidual.Write()

        # Pull plot
        if self.fDoPullPlot:
            canvasPull = DoPullPlot(fRooPlotExtra, self.fRooMass, trialName)
            canvasPull.Write()

        # Correlation matrix plot
        if self.fDoCorrMatPlot:
            canvasCorrMat = DoCorrMatPlot(rooFitRes, trialName)
            canvasCorrMat.Write()

        rooFitRes.Write("info_fit_results_{}".format(trialName))
    
    def MultiTrial(self):
        '''
        WARNING! To be fixed, multiple fits do not work properly
        Method to perform a multi-trial fit
        '''
        for iRange in range(0, len(self.fFitRangeMin)):
            self.FitInvMassSpectrum(self.fFitMethod, self.fFitRangeMin[iRange], self.fFitRangeMax[iRange])
        self.fFileOut.Close()

        # Update file name
        trialName = self.fTrialName + "_" + str(self.fFitRangeMin[iRange]) + "_" + str(self.fFitRangeMax[iRange]) + ".root"
        oldFileOutName = self.fFileOutName
        newFileOutName = oldFileOutName.replace(str(self.fFitRangeMin[iRange]) + "_" + str(self.fFitRangeMax[iRange]) + ".root", trialName)
        os.rename(oldFileOutName, newFileOutName)

    def SingleFit(self, fitRangeMin, fitRangeMax):
        '''
        Method to perform a single fit (calling multi-trial from external script)
        '''
        self.FitInvMassSpectrum(self.fFitMethod, fitRangeMin, fitRangeMax)
        self.fFileOut.Close()

        # Update file name
        trialName = self.fTrialName + "_" + str(fitRangeMin) + "_" + str(fitRangeMax) + ".root"
        oldFileOutName = self.fFileOutName
        newFileOutName = oldFileOutName.replace(str(fitRangeMin) + "_" + str(fitRangeMax) + ".root", trialName)
        os.rename(oldFileOutName, newFileOutName)

