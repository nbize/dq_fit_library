/*****************************************************************************
 * Project: RooFit                                                           *
 *                                                                           *
  * This code was autogenerated by RooClassFactory                            *
 *****************************************************************************/

#ifndef EXPPDF
#define EXPPDF

#include "RooAbsPdf.h"
#include "RooRealProxy.h"
#include "RooCategoryProxy.h"
#include "RooAbsReal.h"
#include "RooAbsCategory.h"

class ExpPdf : public RooAbsPdf {
public:
  ExpPdf() {} ;
  ExpPdf(const char *name, const char *title,
	      RooAbsReal& _x,
	      RooAbsReal& _A,
	      RooAbsReal& _B);
  ExpPdf(const ExpPdf& other, const char* name=0) ;
  virtual TObject* clone(const char* newname) const { return new ExpPdf(*this,newname); }
  inline virtual ~ExpPdf() { }

protected:

  RooRealProxy x ;
  RooRealProxy A ;
  RooRealProxy B ;

  Double_t evaluate() const ;

private:

  ClassDef(ExpPdf,1) // Your description goes here...
};

#endif