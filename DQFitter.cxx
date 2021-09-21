// \author Luca Micheletti <luca.micheletti@cern.ch>

// STL includes
#include <Riostream.h>
#include <stdio.h>
#include <string>
#include <vector>
#include <sstream>

// ROOT includes
#include <TROOT.h>
#include <TObjArray.h>
#include <TMinuit.h>
#include <TCanvas.h>
#include <TFile.h>
#include <TH1.h>
#include <TH2.h>
#include <TH3.h>
#include <TF1.h>
#include <TStyle.h>
#include <TLatex.h>
#include <TLegend.h>
#include <TLine.h>
#include <TMath.h>
#include <TPad.h>
#include <TSystem.h>
#include <TGraphErrors.h>
#include <TFile.h>
#include <TTree.h>
#include <TChain.h>
#include <TFitResult.h>
#include <TMatrixDSym.h>
#include <TPaveText.h>
#include <TCollection.h>
#include <TKey.h>
#include <TGaxis.h>

// RooFit includes
#include "RooRealVar.h"
#include "RooDataSet.h"
#include "RooWorkspace.h"
#include "RooAddPdf.h"
#include "RooExtendPdf.h"
#include "RooPlot.h"
#include "RooDataHist.h"
using namespace RooFit;

// My includes
#include "FunctionLibrary.C"
#include "DQFitter.h"

ClassImp(DQFitter)

//______________________________________________________________________________
DQFitter::DQFitter(): TObject() {
  // default constructor
  fPathToFile       = "AnalysisResults.root";
  fNParBkg          = 2;
  fNParSig          = 3;
  fMaxFitIterations = 100;
  fMinFitRange      = 0.;
  fMaxFitRange      = 100;
  fFitMethod        = "SRL";
}
//______________________________________________________________________________
DQFitter::DQFitter(TString pathToFile): TObject() {
  // standard constructor
  fPathToFile       = pathToFile;
  fNParBkg          = 2;
  fNParSig          = 3;
  fMaxFitIterations = 100;
  fMinFitRange      = 0.;
  fMaxFitRange      = 100;
  fFitMethod        = "SRL";
  OpenOutputFile(fPathToFile);
}
//______________________________________________________________________________
DQFitter::~DQFitter() {
  // destructor
}
//______________________________________________________________________________
void DQFitter::OpenOutputFile(TString pathToFile) {
  fPathToFile=pathToFile;
  printf("\n************ Create output file %s ************\n", fPathToFile.Data());
  fFile = new TFile(fPathToFile, "RECREATE");
}
//______________________________________________________________________________
void DQFitter::CloseOutputFile() {
  if (fFile) {
    fFile->Close();
  } else {
    printf("\n************ WARNING: no output file inizialized ************\n");
  }
}
//______________________________________________________________________________
void DQFitter::SetHistogram(TH1F *hist) {
  fHist = hist;
  fHist->GetYaxis()->SetRangeUser(0., 2.*fHist->GetMaximum());
}
//______________________________________________________________________________
void DQFitter::SetFunction(FitFunctionsList func) {
  switch (func) {
    case kFuncPol0 :
      fFuncTot = new TF1("funcPol0", FuncPol0, -100., 100., nParameters[kFuncPol0]);
      break;
    case kFuncExp :
      fFuncTot = new TF1("funcExp", FuncExp, -100., 100., nParameters[kFuncExp]);
      break;
    case kFuncGaus :
      fFuncTot = new TF1("funcGaus", FuncGaus, -100., 100., nParameters[kFuncGaus]);
      break;
    case kFuncPol0Gaus :
      fFuncTot = new TF1("funcPol0Gaus", FuncPol0Gaus, -100., 100., nParameters[kFuncPol0Gaus]);
      fFuncBkg = new TF1("funcPol0",     FuncPol0,     -100., 100., nParameters[kFuncPol0]);
      fNParBkg = nParameters[kFuncPol0];
      fFuncSig = new TF1("funcGaus",     FuncGaus,     -100., 100., nParameters[kFuncGaus]);
      fNParSig = nParameters[kFuncGaus];
      break;
    case kFuncExpGaus :
      fFuncTot = new TF1("funcExpGaus", FuncExpGaus, -100., 100., nParameters[kFuncExpGaus]);
      fFuncBkg = new TF1("funcExp",     FuncExp,     -100., 100., nParameters[kFuncExp]);
      fNParBkg = nParameters[kFuncExp];
      fFuncSig = new TF1("funcGaus",    FuncGaus,    -100., 100., nParameters[kFuncGaus]);
      fNParSig = nParameters[kFuncGaus];
      break;
    case kNFunctions :
      break;
  }
}
//______________________________________________________________________________
void DQFitter::SetFitRange(Double_t minFitRange, Double_t maxFitRange) {
  fMinFitRange = minFitRange;
  fMaxFitRange = maxFitRange;
}
//______________________________________________________________________________
void DQFitter::SetFitMethod(TString fitMethod) {
  fFitMethod = fitMethod;
}
//______________________________________________________________________________
void DQFitter::InitParameters(Int_t nParams, Double_t *params, TString *fixParams, TString *nameParams) {
  fNParams = nParams;

  for (int iPar = 0;iPar < fNParams;iPar++) {
    if (fixParams[iPar] == "free") {
      fFuncTot->SetParameter(iPar, params[iPar]);
    } else {
      fFuncTot->FixParameter(iPar, params[iPar]);
    }
    if (!nameParams) {
      fFuncTot->SetParName(iPar, Form("p%i", iPar));
    } else {
      fFuncTot->SetParName(iPar, nameParams[iPar].Data());
    }
  }

  // Init the histogram with the fit results
  fHistResults = new TH1F("histResults", "", fNParams+2, 0., fNParams+2);
  fHistResults->GetXaxis()->SetBinLabel(1, "#chi^{2} / NDF");
  fHistResults->GetXaxis()->SetBinLabel(2, "Signal");
  for (int iPar = 2;iPar < fNParams+2;iPar++) {
    fHistResults->GetXaxis()->SetBinLabel(iPar+1, fFuncTot->GetParName(iPar-2));
  }
}
//______________________________________________________________________________
void DQFitter::BinnedFitInvMassSpectrum(TString trialName) {
  fTrialName = trialName;

  // Fit the histogram
  TFitResultPtr ptrFit;
  ptrFit = (TFitResultPtr) fHist->Fit(fFuncTot, fFitMethod, "", fMinFitRange, fMaxFitRange);
  TMatrixDSym covSig  = ptrFit->GetCovarianceMatrix().GetSub(fNParBkg, fNParBkg+fNParSig-1, fNParBkg, fNParBkg+fNParSig-1);

  // Set Background prameters
  for (Int_t iParBkg = 0;iParBkg < fNParBkg;iParBkg++) {
    fFuncBkg->SetParameter(iParBkg, fFuncTot->GetParameter(iParBkg));
  }
  // Set Signal parameters
  for (Int_t iParSig = 0;iParSig < fNParSig;iParSig++) {
    fFuncSig->SetParameter(iParSig, fFuncTot->GetParameter(fNParBkg + iParSig));
  }

  fChiSquareNDF      = fFuncTot->GetChisquare() / fFuncTot->GetNDF();
  fErrorChiSquareNDF = 0.;
  fSignal            = fFuncSig->Integral(fMinFitRange, fMaxFitRange) / fHist->GetBinWidth(1);
  fErrorSignal       = fFuncSig->IntegralError(fMinFitRange, fMaxFitRange, fFuncSig->GetParameters(), covSig.GetMatrixArray()) / fHist->GetBinWidth(1);

  // Default entries of the results histogram
  fHistResults->SetBinContent(fHistResults->GetXaxis()->FindBin("#chi^{2} / NDF"), fChiSquareNDF);
  fHistResults->SetBinError(fHistResults->GetXaxis()->FindBin("#chi^{2} / NDF"), fErrorChiSquareNDF);
  fHistResults->SetBinContent(fHistResults->GetXaxis()->FindBin("Signal"), fSignal);
  fHistResults->SetBinError(fHistResults->GetXaxis()->FindBin("Signal"), fErrorSignal);

  // User entries of the results histogram
  for (int iPar = 0;iPar < fNParams;iPar++) {
    fHistResults->SetBinContent(iPar+3, fFuncTot->GetParameter(iPar));
    fHistResults->SetBinError(iPar+3, fFuncTot->GetParError(iPar));
  }
  if (!fFile) {
    printf("\n************ WARNING: no output file! ************\n");
  } else {
    SaveResults();
  }
}
//______________________________________________________________________________
void DQFitter::SaveResults() {
  // Create the directory where the output will be saved
  TDirectory *trialDir = fFile->mkdir(fTrialName);

  // Some settings for plotting...
  gStyle->SetOptStat(0);

  fHist->SetTitle("");
  fHist->GetXaxis()->SetTitle("#it{M}_{#it{l^{+}}#it{l^{-}}} GeV/#it{c^{2}}");
  fHist->GetYaxis()->SetTitle("Entries");
  fHist->SetMarkerStyle(20);
  fHist->SetMarkerColor(kBlack);
  fHist->SetLineColor(kBlack);

  fFuncTot->SetRange(fMinFitRange, fMaxFitRange);
  fFuncTot->SetLineColor(kRed);
  fFuncTot->SetLineStyle(kSolid);

  fFuncBkg->SetRange(fMinFitRange, fMaxFitRange);
  fFuncBkg->SetLineColor(kGray+1);
  fFuncBkg->SetLineStyle(kDotted);

  fFuncSig->SetRange(fMinFitRange, fMaxFitRange);
  fFuncSig->SetLineColor(kBlue);
  fFuncSig->SetLineStyle(kDashed);

  fHistRatio = (TH1F*) fHist->Clone("histRatio");
  fHistRatio->SetTitle("");
  fHistRatio->GetXaxis()->SetTitle("#it{M}_{#it{l^{+}}#it{l^{-}}} GeV/#it{c^{2}}");
  fHistRatio->GetYaxis()->SetTitle("Data / Fit");
  fHistRatio->Sumw2();
  fHistRatio->Divide(fFuncTot);
  fHistRatio->GetYaxis()->SetRangeUser(0., 2.);

  // Draw fit results
  TPaveText *paveText = new TPaveText(0.6,0.6,0.95,0.95,"brNDC");
  paveText->SetTextSize(0.03);
  paveText->AddText(Form("#chi^{2}/NDF = %3.2f", fChiSquareNDF));
  paveText->AddText(Form("S = %1.0f #pm %1.0f", fSignal, fErrorSignal));
  for (int iPar = 0;iPar < fNParams;iPar++) {
    paveText->AddText(Form("%s = %4.3f #pm %4.3f", fFuncTot->GetParName(iPar), fFuncTot->GetParameter(iPar), fFuncTot->GetParError(iPar)));
  }

  TCanvas *canvasFit = new TCanvas(Form("canvasFit_%s", fTrialName.Data()), Form("canvasFit_%s", fTrialName.Data()), 600, 600);
  canvasFit->SetLeftMargin(0.15);
  fHist->Draw("EP");
  fFuncBkg->Draw("same");
  fFuncSig->Draw("same");
  fFuncTot->Draw("same");
  paveText->Draw();

  // Draw Ratio Data / Fit
  TLine *lineUnity = new TLine(fMinFitRange, 1.,fMaxFitRange, 1.);
  lineUnity->SetLineStyle(kDashed);
  lineUnity->SetLineWidth(2);
  lineUnity->SetLineColorAlpha(kRed, 0.4);

  TCanvas *canvasRatio = new TCanvas(Form("canvasRatio_%s", fTrialName.Data()), Form("canvasRatio_%s", fTrialName.Data()), 600, 600);
  fHistRatio->Draw("E0");
  lineUnity->Draw("saem");

  // Save fHistResults and canvas into the output file
  trialDir->cd();
  canvasFit->Write();
  canvasRatio->Write();
  fHistResults->Write();
  delete canvasFit;
  delete canvasRatio;
}
//______________________________________________________________________________
void DQFitter::SetPDF(FitFunctionsList func) {
  gROOT->ProcessLineSync(".x GausPdf.cxx+");
  gROOT->ProcessLineSync(".x ExpPdf.cxx+");

  fRooMass = RooRealVar("m", "#it{M} (GeV/#it{c}^{2})", 0, 5);
  switch (func) {
    case kFuncPol0 :
      break;
    case kFuncExp :
      break;
    case kFuncGaus :
      break;
    case kFuncPol0Gaus :
      break;
    case kFuncExpGaus :
      fRooWorkspace.factory("GausPdf::myGaus(m[0,5], mean[3,2,4], width[0.1,0,0.2])");
      fRooWorkspace.factory("ExpPdf::myExp(m[0,5], a[1,0.7,1.3], b[0.5,-10,10])");
      fRooWorkspace.factory("SUM::sum(nsig[10000,5000,20000]*myGaus,nbkg[100000,50000,200000]*myExp)");
      break;
    case kNFunctions :
      break;
  }
}
//______________________________________________________________________________
void DQFitter::InitRooParameters(Int_t nParams, RooRealVar *rooParameters[]) {
  fNParams = nParams;
  for (int iPar = 0;iPar < fNParams;iPar++) {
    fRooParameters[iPar] = rooParameters[iPar];
  }
}
//______________________________________________________________________________
void DQFitter::UnbinnedFitInvMassSpectrum(TString trialName) {
  fTrialName = trialName;
  fRooWorkspace.Print();
  auto pdf = fRooWorkspace.pdf("sum");

  // Generate toy data from pdf and plot data and pdf on frame
  RooPlot *frame1 = fRooMass.frame(Title("Fit Example"));

  /*
  RooDataSet *data = pdf->generate(fRooMass, 1000);
  pdf->fitTo(*data);
  data->plotOn(frame1);
  pdf->plotOn(frame1);

  TCanvas *c = new TCanvas("rf104_classfactory", "rf104_classfactory", 800, 400);
  c->cd(1);
  gPad->SetLeftMargin(0.15);
  frame1->GetYaxis()->SetTitleOffset(1.4);
  frame1->Draw();
  */



  RooDataHist data("data","data",fRooMass,Import(*fHist)) ;
  pdf->fitTo(data);
  data.plotOn(frame1);
  pdf->plotOn(frame1);
  pdf->paramOn(frame1, Layout(0.55));

  TCanvas *canvasFit = new TCanvas(Form("canvasFit_%s", fTrialName.Data()), Form("canvasFit_%s", fTrialName.Data()), 600, 600);
  canvasFit->SetLeftMargin(0.15);
  gPad->SetLeftMargin(0.15);
  frame1->GetYaxis()->SetTitleOffset(1.4);
  frame1->Draw();
}
