# -*- coding: mbcs -*-
# Created by makepy.py version 0.5.01
# By python version 2.7.11 |Continuum Analytics, Inc.| (default, Dec  7 2015, 14:10:42) [MSC v.1500 64 bit (AMD64)]
# On Wed Jan 27 18:52:33 2016
'ClearImage COM Server'
makepy_version = '0.5.01'
python_version = 0x2070bf0

import win32com.client.CLSIDToClass, pythoncom, pywintypes
import win32com.client.util
from pywintypes import IID
from win32com.client import Dispatch

# The following 3 lines may need tweaking for the particular server
# Candidates are pythoncom.Missing, .Empty and .ArgNotFound
defaultNamedOptArg=pythoncom.Empty
defaultNamedNotOptArg=pythoncom.Empty
defaultUnnamedArg=pythoncom.Empty

CLSID = IID('{F2BCF178-0B27-11D4-B5F5-9CC767000000}')
MajorVersion = 1
MinorVersion = 0
LibraryFlags = 8
LCID = 0x0

class constants:
	cibBestRecognition            =2          # from enum EBarcodeAlgorithm
	cibBestSpeed                  =1          # from enum EBarcodeAlgorithm
	ebeCompressionA1              =2          # from enum EBarcodeEncoding
	ebeCompressionV1              =1          # from enum EBarcodeEncoding
	ebeNone                       =0          # from enum EBarcodeEncoding
	cibRotDiag                    =5          # from enum EBarcodeRotation
	cibRotLeft                    =3          # from enum EBarcodeRotation
	cibRotNone                    =1          # from enum EBarcodeRotation
	cibRotRight                   =4          # from enum EBarcodeRotation
	cibRotUpsideDown              =2          # from enum EBarcodeRotation
	cib4State                     =32         # from enum EBarcodeType
	cibAddon2                     =10         # from enum EBarcodeType
	cibAddon5                     =11         # from enum EBarcodeType
	cibAirline2of5                =16         # from enum EBarcodeType
	cibAustralianPost             =35         # from enum EBarcodeType
	cibBpoPostcode                =34         # from enum EBarcodeType
	cibCodabar                    =4          # from enum EBarcodeType
	cibCode128                    =3          # from enum EBarcodeType
	cibCode32                     =12         # from enum EBarcodeType
	cibCode39                     =2          # from enum EBarcodeType
	cibCode93                     =7          # from enum EBarcodeType
	cibDataMatrix                 =30         # from enum EBarcodeType
	cibDatalogic2of5              =14         # from enum EBarcodeType
	cibEan13                      =9          # from enum EBarcodeType
	cibEan8                       =6          # from enum EBarcodeType
	cibIndustrial2of5             =13         # from enum EBarcodeType
	cibInterleaved2of5            =1          # from enum EBarcodeType
	cibMatrix2of5                 =15         # from enum EBarcodeType
	cibPatch                      =18         # from enum EBarcodeType
	cibPdf417                     =31         # from enum EBarcodeType
	cibPlanet                     =20         # from enum EBarcodeType
	cibPostnet                    =19         # from enum EBarcodeType
	cibQR                         =36         # from enum EBarcodeType
	cibSingaporePost              =37         # from enum EBarcodeType
	cibUcc128                     =17         # from enum EBarcodeType
	cibUpca                       =5          # from enum EBarcodeType
	cibUpce                       =8          # from enum EBarcodeType
	cibUspsIntelligentMail        =33         # from enum EBarcodeType
	ciBtcBwOnly                   =3          # from enum EBiTonalConversion
	ciBtcEdge1H                   =220        # from enum EBiTonalConversion
	ciBtcEdge1V                   =221        # from enum EBiTonalConversion
	ciBtcEdge3                    =222        # from enum EBiTonalConversion
	ciBtcEdge4                    =223        # from enum EBiTonalConversion
	ciBtcEdgeOne                  =4          # from enum EBiTonalConversion
	ciBtcLocalThr                 =5          # from enum EBiTonalConversion
	ciBtcNone                     =1          # from enum EBiTonalConversion
	ciBtcStandard                 =2          # from enum EBiTonalConversion
	ciBtcUnknown                  =0          # from enum EBiTonalConversion
	ciFalse                       =0          # from enum EBoolean
	ciTrue                        =65535      # from enum EBoolean
	ciBeaCleaner                  =2          # from enum EBorderExtractAlgorithm
	ciBeaFaster                   =1          # from enum EBorderExtractAlgorithm
	ciBexBorder                   =1          # from enum EBorderExtractFlags
	ciBexBorderDeskew             =2          # from enum EBorderExtractFlags
	ciBexBorderDeskewCrop         =3          # from enum EBorderExtractFlags
	ciBexDeskewCrop               =4          # from enum EBorderExtractFlags
	ciCnxBlackNoise               =1          # from enum ECleanNoiseFlags
	ciCnxMarginsNoise             =8          # from enum ECleanNoiseFlags
	ciCnxWhiteNoise               =2          # from enum ECleanNoiseFlags
	citbAUTO                      =0          # from enum EComprBitonal
	citbCCITTFAX3                 =3          # from enum EComprBitonal
	citbCCITTFAX4                 =4          # from enum EComprBitonal
	citbNONE                      =1          # from enum EComprBitonal
	citbORIGINAL                  =500        # from enum EComprBitonal
	citcAUTO                      =0          # from enum EComprColor
	citcJPEG                      =7          # from enum EComprColor
	citcLZW                       =5          # from enum EComprColor
	citcNONE                      =1          # from enum EComprColor
	ciBMP                         =3          # from enum EFileFormat
	ciEXT                         =1          # from enum EFileFormat
	ciGIF                         =102        # from enum EFileFormat
	ciICO                         =106        # from enum EFileFormat
	ciJBG                         =113        # from enum EFileFormat
	ciJP2                         =114        # from enum EFileFormat
	ciJPC                         =115        # from enum EFileFormat
	ciJPG                         =103        # from enum EFileFormat
	ciPCX                         =4          # from enum EFileFormat
	ciPGX                         =116        # from enum EFileFormat
	ciPNG                         =104        # from enum EFileFormat
	ciPNM                         =117        # from enum EFileFormat
	ciTGA                         =108        # from enum EFileFormat
	ciTIFF                        =5          # from enum EFileFormat
	ciTIFF_G3_1D                  =6          # from enum EFileFormat
	ciTIFF_G4                     =7          # from enum EFileFormat
	ciTIFF_JPEG                   =20         # from enum EFileFormat
	ciTIFF_LZW                    =21         # from enum EFileFormat
	ciTIFF_NEOL                   =8          # from enum EFileFormat
	ciWBMP                        =110        # from enum EFileFormat
	cifICL                        =23         # from enum EFileFormat
	cifPDF                        =22         # from enum EFileFormat
	ciGscEqual                    =3          # from enum EGrayscaleConversion
	ciGscNTSC                     =4          # from enum EGrayscaleConversion
	ciGscSoften                   =5          # from enum EGrayscaleConversion
	ciGscStandard                 =2          # from enum EGrayscaleConversion
	epiaBestFit                   =20         # from enum EImageAlignment
	epiaBottomCenter              =6          # from enum EImageAlignment
	epiaBottomLeft                =3          # from enum EImageAlignment
	epiaBottomRight               =4          # from enum EImageAlignment
	epiaCenter                    =0          # from enum EImageAlignment
	epiaLeftCenter                =7          # from enum EImageAlignment
	epiaRightCenter               =8          # from enum EImageAlignment
	epiaStretch                   =21         # from enum EImageAlignment
	epiaTopCenter                 =5          # from enum EImageAlignment
	epiaTopLeft                   =1          # from enum EImageAlignment
	epiaTopRight                  =2          # from enum EImageAlignment
	ciErrorText                   =3          # from enum EInfoType
	ciModulesList                 =1          # from enum EInfoType
	ciModulesXml                  =2          # from enum EInfoType
	ciCurvHigh                    =5          # from enum ELineCurvature
	ciCurvLow                     =3          # from enum ELineCurvature
	ciCurvMedium                  =4          # from enum ELineCurvature
	ciCurvStraight                =1          # from enum ELineCurvature
	ciCurvVeryLow                 =2          # from enum ELineCurvature
	ciLineHorz                    =2          # from enum ELineDirection
	ciLineUnknown                 =0          # from enum ELineDirection
	ciLineVert                    =1          # from enum ELineDirection
	ciLineVertAndHorz             =3          # from enum ELineDirection
	ciLogActions                  =1          # from enum ELogType
	ciLogMeasurements             =2          # from enum ELogType
	ciLogResults                  =3          # from enum ELogType
	ciMorphAllNeighbours          =7          # from enum EMorphDirections
	ciMorphDiag                   =4          # from enum EMorphDirections
	ciMorphHorz                   =1          # from enum EMorphDirections
	ciMorphHorzAndVert            =3          # from enum EMorphDirections
	ciMorphVert                   =2          # from enum EMorphDirections
	epgoAuto                      =0          # from enum EPageOrientation
	epgoLandscape                 =2          # from enum EPageOrientation
	epgoPortrait                  =1          # from enum EPageOrientation
	ciRotLeft                     =4          # from enum EPageRotation
	ciRotLeftOrRight              =12         # from enum EPageRotation
	ciRotNone                     =1          # from enum EPageRotation
	ciRotPortrait                 =3          # from enum EPageRotation
	ciRotRight                    =8          # from enum EPageRotation
	ciRotUnknown                  =0          # from enum EPageRotation
	ciRotUpsideDown               =2          # from enum EPageRotation
	epgsA4                        =20         # from enum EPageSize
	epgsCustom                    =4          # from enum EPageSize
	epgsImage                     =40         # from enum EPageSize
	epgsLedger                    =12         # from enum EPageSize
	epgsLegal                     =11         # from enum EPageSize
	epgsLetter                    =10         # from enum EPageSize
	epgsNearest                   =41         # from enum EPageSize
	epgsNearestMetric             =43         # from enum EPageSize
	epgsNearestStd                =42         # from enum EPageSize
	epgsOriginal                  =5          # from enum EPageSize
	eprmAuto                      =0          # from enum EPdfRasterColorMode
	eprmBw                        =1          # from enum EPdfRasterColorMode
	eprmGs                        =2          # from enum EPdfRasterColorMode
	eprmRgb                       =3          # from enum EPdfRasterColorMode
	epemAuto                      =0          # from enum EPdfReadMode
	epemImage                     =1          # from enum EPdfReadMode
	epemRaster                    =2          # from enum EPdfReadMode
	ciScaleBestQuality            =1          # from enum EScaleBmpType
	ciScaleBestSpeed              =2          # from enum EScaleBmpType
	ciScaleMergeLineGaps          =1          # from enum EScaleType
	ciScaleMergeLinePixels        =2          # from enum EScaleType
	ciScaleSkipLines              =3          # from enum EScaleType
	ciScaleThreshold              =101        # from enum EScaleType
	esuCentimeter                 =3          # from enum ESizeUnit
	esuInch                       =1          # from enum ESizeUnit
	esuPixel                      =0          # from enum ESizeUnit
	ciSmoothDarkenEdges           =1          # from enum ESmoothType
	ciSmoothLightenEdges          =2          # from enum ESmoothType
	cibNoValidation               =512        # from enum FBarcodeDiag
	cibRawData                    =64         # from enum FBarcodeDiag
	cibSymbologyIdentifier        =8192       # from enum FBarcodeDiag
	cibDiag                       =4          # from enum FBarcodeDirections
	cibHorz                       =1          # from enum FBarcodeDirections
	cibVert                       =2          # from enum FBarcodeDirections
	cibBadChecksum                =2          # from enum FBarcodeErrors
	cibBadData                    =16         # from enum FBarcodeErrors
	cibBadStartChar               =4          # from enum FBarcodeErrors
	cibBadStopChar                =8          # from enum FBarcodeErrors
	cibDecoding                   =1          # from enum FBarcodeErrors
	cibf4State                    =33554432   # from enum FBarcodeType
	cibfAddon2                    =512        # from enum FBarcodeType
	cibfAddon5                    =1024       # from enum FBarcodeType
	cibfAirline2of5               =524288     # from enum FBarcodeType
	cibfCodabar                   =8          # from enum FBarcodeType
	cibfCode128                   =4          # from enum FBarcodeType
	cibfCode32                    =8388608    # from enum FBarcodeType
	cibfCode39                    =2          # from enum FBarcodeType
	cibfCode93                    =64         # from enum FBarcodeType
	cibfDatalogic2of5             =131072     # from enum FBarcodeType
	cibfEan13                     =256        # from enum FBarcodeType
	cibfEan8                      =32         # from enum FBarcodeType
	cibfIndustrial2of5            =65536      # from enum FBarcodeType
	cibfInterleaved2of5           =1          # from enum FBarcodeType
	cibfMatrix2of5                =262144     # from enum FBarcodeType
	cibfPatch                     =2097152    # from enum FBarcodeType
	cibfPostnet                   =16777216   # from enum FBarcodeType
	cibfUcc128                    =1048576    # from enum FBarcodeType
	cibfUpca                      =16         # from enum FBarcodeType
	cibfUpce                      =128        # from enum FBarcodeType
	ciLogEnable                   =1          # from enum FLogFlags
	ciLogFileName                 =2          # from enum FLogFlags
	ciLogSignature                =4          # from enum FLogFlags
	ciLogTime                     =8          # from enum FLogFlags
	ciLogTimeStamp                =16         # from enum FLogFlags

from win32com.client import DispatchBaseClass
class ICiAdvColor(DispatchBaseClass):
	'ICiAdvColor Interface'
	CLSID = IID('{8CBBAECA-9716-40CA-B8F6-0E9FF213522A}')
	coclass_clsid = IID('{3022D35D-0127-4C24-B1F0-1C66A831807E}')

	def ConvertToBitonal(self, mode=2, Par0=0, par1=0, par2=0):
		'Convert image to bitonal'
		return self._oleobj_.InvokeTypes(2, LCID, 1, (24, 0), ((3, 49), (3, 49), (3, 49), (3, 49)),mode
			, Par0, par1, par2)

	def ConvertToGrayscale(self, mode=2, Par0=0, par1=0, par2=0):
		'Convert image to grayscale'
		return self._oleobj_.InvokeTypes(3, LCID, 1, (24, 0), ((3, 49), (3, 49), (3, 49), (3, 49)),mode
			, Par0, par1, par2)

	def ScaleToDpi(self, mode=1, Par0=0):
		return self._oleobj_.InvokeTypes(4, LCID, 1, (24, 0), ((3, 49), (3, 49)),mode
			, Par0)

	# The method Setcx2l is actually a property, but must be used as a method to correctly pass the arguments
	def Setcx2l(self, i=defaultNamedNotOptArg, arg1=defaultUnnamedArg):
		'property cx2l'
		return self._oleobj_.InvokeTypes(5, LCID, 4, (24, 0), ((3, 1), (3, 1)),i
			, arg1)

	# The method Setcx3d is actually a property, but must be used as a method to correctly pass the arguments
	def Setcx3d(self, i=defaultNamedNotOptArg, arg1=defaultUnnamedArg):
		'property cx3d'
		return self._oleobj_.InvokeTypes(6, LCID, 4, (24, 0), ((3, 1), (5, 1)),i
			, arg1)

	# The method cx2l is actually a property, but must be used as a method to correctly pass the arguments
	def cx2l(self, i=defaultNamedNotOptArg):
		'property cx2l'
		return self._oleobj_.InvokeTypes(5, LCID, 2, (3, 0), ((3, 1),),i
			)

	# The method cx3d is actually a property, but must be used as a method to correctly pass the arguments
	def cx3d(self, i=defaultNamedNotOptArg):
		'property cx3d'
		return self._oleobj_.InvokeTypes(6, LCID, 2, (5, 0), ((3, 1),),i
			)

	_prop_map_get_ = {
		# Method 'Image' returns object of type 'ICiImage'
		"Image": (1, 2, (9, 0), (), "Image", '{F2BCF189-0B27-11D4-B5F5-9CC767000000}'),
		"o": (7, 2, (20, 0), (), "o", None),
	}
	_prop_map_put_ = {
		"Image": ((1, LCID, 4, 0),()),
		"o": ((7, LCID, 4, 0),()),
	}
	def __iter__(self):
		"Return a Python iterator for this object"
		try:
			ob = self._oleobj_.InvokeTypes(-4,LCID,3,(13, 10),())
		except pythoncom.error:
			raise TypeError("This object does not support enumeration")
		return win32com.client.util.Iterator(ob, None)

class ICiBarcode(DispatchBaseClass):
	'ICiBarcode Interface'
	CLSID = IID('{4ED88240-0BE1-11D4-B5F6-009FC6000000}')
	coclass_clsid = IID('{4ED88241-0BE1-11D4-B5F6-009FC6000000}')

	# The method Info is actually a property, but must be used as a method to correctly pass the arguments
	def Info(self, Type=defaultNamedNotOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(18, LCID, 2, (8, 0), ((8, 1),),Type
			)

	# The method SetInfo is actually a property, but must be used as a method to correctly pass the arguments
	def SetInfo(self, Type=defaultNamedNotOptArg, arg1=defaultUnnamedArg):
		return self._oleobj_.InvokeTypes(18, LCID, 4, (24, 0), ((8, 1), (8, 1)),Type
			, arg1)

	_prop_map_get_ = {
		"Confidence": (9, 2, (3, 0), (), "Confidence", None),
		"Data": (6, 2, (12, 0), (), "Data", None),
		"Encoding": (20, 2, (3, 0), (), "Encoding", None),
		"ErrorFlags": (8, 2, (3, 0), (), "ErrorFlags", None),
		"IsBinary": (15, 2, (3, 0), (), "IsBinary", None),
		"IsChecksumVerified": (16, 2, (3, 0), (), "IsChecksumVerified", None),
		"Length": (4, 2, (3, 0), (), "Length", None),
		"ModuleSize": (12, 2, (5, 0), (), "ModuleSize", None),
		"Quality": (17, 2, (5, 0), (), "Quality", None),
		# Method 'Rect' returns object of type 'ICiRect'
		"Rect": (1, 2, (9, 0), (), "Rect", '{4ED88244-0BE1-11D4-B5F6-009FC6000000}'),
		"Rotation": (3, 2, (3, 0), (), "Rotation", None),
		"Skew": (19, 2, (5, 0), (), "Skew", None),
		"Text": (5, 2, (8, 0), (), "Text", None),
		"Type": (2, 2, (3, 0), (), "Type", None),
		"o": (21, 2, (20, 0), (), "o", None),
	}
	_prop_map_put_ = {
		"Confidence": ((9, LCID, 4, 0),()),
		"Data": ((6, LCID, 4, 0),()),
		"Encoding": ((20, LCID, 4, 0),()),
		"ErrorFlags": ((8, LCID, 4, 0),()),
		"IsBinary": ((15, LCID, 4, 0),()),
		"IsChecksumVerified": ((16, LCID, 4, 0),()),
		"ModuleSize": ((12, LCID, 4, 0),()),
		"Quality": ((17, LCID, 4, 0),()),
		"Rotation": ((3, LCID, 4, 0),()),
		"Skew": ((19, LCID, 4, 0),()),
		"Text": ((5, LCID, 4, 0),()),
		"Type": ((2, LCID, 4, 0),()),
		"o": ((21, LCID, 4, 0),()),
	}
	def __iter__(self):
		"Return a Python iterator for this object"
		try:
			ob = self._oleobj_.InvokeTypes(-4,LCID,3,(13, 10),())
		except pythoncom.error:
			raise TypeError("This object does not support enumeration")
		return win32com.client.util.Iterator(ob, None)

class ICiBarcodeBasic(DispatchBaseClass):
	'ICiBarcodeBasic Interface'
	CLSID = IID('{21DA65F1-9E63-45E3-B081-F78096F9D6C3}')
	coclass_clsid = IID('{12806B0A-7754-4297-AE05-631C2A1E928D}')

	def Find(self, MaxBarcodes=0):
		'Find multiple barcodes'
		return self._oleobj_.InvokeTypes(11, LCID, 1, (3, 0), ((3, 49),),MaxBarcodes
			)

	# Result is of type ICiBarcode
	def FirstBarcode(self):
		'Find first barcode'
		ret = self._oleobj_.InvokeTypes(2, LCID, 1, (9, 0), (),)
		if ret is not None:
			ret = Dispatch(ret, u'FirstBarcode', '{4ED88240-0BE1-11D4-B5F6-009FC6000000}')
		return ret

	# Result is of type ICiBarcode
	def NextBarcode(self):
		'Find another barcode'
		ret = self._oleobj_.InvokeTypes(3, LCID, 1, (9, 0), (),)
		if ret is not None:
			ret = Dispatch(ret, u'NextBarcode', '{4ED88240-0BE1-11D4-B5F6-009FC6000000}')
		return ret

	_prop_map_get_ = {
		"AutoDetect1D": (8, 2, (3, 0), (), "AutoDetect1D", None),
		# Method 'Barcodes' returns object of type 'ICiBarcodes'
		"Barcodes": (10, 2, (9, 0), (), "Barcodes", '{41F7F4D4-9FC1-46C6-92E5-2A3457CE3D5E}'),
		# Method 'Image' returns object of type 'ICiImage'
		"Image": (5, 2, (9, 0), (), "Image", '{F2BCF189-0B27-11D4-B5F5-9CC767000000}'),
		"Type": (7, 2, (3, 0), (), "Type", None),
		"ValidateOptChecksum": (9, 2, (3, 0), (), "ValidateOptChecksum", None),
		"o": (12, 2, (20, 0), (), "o", None),
	}
	_prop_map_put_ = {
		"AutoDetect1D": ((8, LCID, 4, 0),()),
		"Image": ((5, LCID, 4, 0),()),
		"Type": ((7, LCID, 4, 0),()),
		"ValidateOptChecksum": ((9, LCID, 4, 0),()),
		"o": ((12, LCID, 4, 0),()),
	}
	def __iter__(self):
		"Return a Python iterator for this object"
		try:
			ob = self._oleobj_.InvokeTypes(-4,LCID,3,(13, 10),())
		except pythoncom.error:
			raise TypeError("This object does not support enumeration")
		return win32com.client.util.Iterator(ob, None)

class ICiBarcodePro(DispatchBaseClass):
	'ICiBarcodePro Interface'
	CLSID = IID('{BDDB0244-0CFD-11D4-B5F8-B89D57000000}')
	coclass_clsid = IID('{BDDB0245-0CFD-11D4-B5F8-B89D57000000}')

	def Find(self, MaxBarcodes=0):
		'Find multiple barcodes'
		return self._oleobj_.InvokeTypes(13, LCID, 1, (3, 0), ((3, 49),),MaxBarcodes
			)

	# Result is of type ICiBarcode
	def FirstBarcode(self):
		'Find first barcode'
		ret = self._oleobj_.InvokeTypes(8, LCID, 1, (9, 0), (),)
		if ret is not None:
			ret = Dispatch(ret, u'FirstBarcode', '{4ED88240-0BE1-11D4-B5F6-009FC6000000}')
		return ret

	def Fx1(self, par1=0, par2=0):
		ret = self._oleobj_.InvokeTypes(14, LCID, 1, (13, 0), ((3, 49), (3, 49)),par1
			, par2)
		if ret is not None:
			# See if this IUnknown is really an IDispatch
			try:
				ret = ret.QueryInterface(pythoncom.IID_IDispatch)
			except pythoncom.error:
				return ret
			ret = Dispatch(ret, u'Fx1', None)
		return ret

	# Result is of type ICiBarcode
	def NextBarcode(self):
		'Find another barcode'
		ret = self._oleobj_.InvokeTypes(9, LCID, 1, (9, 0), (),)
		if ret is not None:
			ret = Dispatch(ret, u'NextBarcode', '{4ED88240-0BE1-11D4-B5F6-009FC6000000}')
		return ret

	# The method Setcx2l is actually a property, but must be used as a method to correctly pass the arguments
	def Setcx2l(self, i=defaultNamedNotOptArg, arg1=defaultUnnamedArg):
		'property cx2l'
		return self._oleobj_.InvokeTypes(15, LCID, 4, (24, 0), ((3, 1), (3, 1)),i
			, arg1)

	# The method cx2l is actually a property, but must be used as a method to correctly pass the arguments
	def cx2l(self, i=defaultNamedNotOptArg):
		'property cx2l'
		return self._oleobj_.InvokeTypes(15, LCID, 2, (3, 0), ((3, 1),),i
			)

	_prop_map_get_ = {
		"Algorithm": (4, 2, (3, 0), (), "Algorithm", None),
		"AutoDetect1D": (10, 2, (3, 0), (), "AutoDetect1D", None),
		# Method 'Barcodes' returns object of type 'ICiBarcodes'
		"Barcodes": (12, 2, (9, 0), (), "Barcodes", '{41F7F4D4-9FC1-46C6-92E5-2A3457CE3D5E}'),
		"DiagFlags": (5, 2, (3, 0), (), "DiagFlags", None),
		"Directions": (2, 2, (3, 0), (), "Directions", None),
		"Encodings": (16, 2, (3, 0), (), "Encodings", None),
		# Method 'Image' returns object of type 'ICiImage'
		"Image": (6, 2, (9, 0), (), "Image", '{F2BCF189-0B27-11D4-B5F5-9CC767000000}'),
		"Type": (1, 2, (3, 0), (), "Type", None),
		"ValidateOptChecksum": (11, 2, (3, 0), (), "ValidateOptChecksum", None),
		"o": (17, 2, (20, 0), (), "o", None),
	}
	_prop_map_put_ = {
		"Algorithm": ((4, LCID, 4, 0),()),
		"AutoDetect1D": ((10, LCID, 4, 0),()),
		"DiagFlags": ((5, LCID, 4, 0),()),
		"Directions": ((2, LCID, 4, 0),()),
		"Encodings": ((16, LCID, 4, 0),()),
		"Image": ((6, LCID, 4, 0),()),
		"Type": ((1, LCID, 4, 0),()),
		"ValidateOptChecksum": ((11, LCID, 4, 0),()),
		"o": ((17, LCID, 4, 0),()),
	}
	def __iter__(self):
		"Return a Python iterator for this object"
		try:
			ob = self._oleobj_.InvokeTypes(-4,LCID,3,(13, 10),())
		except pythoncom.error:
			raise TypeError("This object does not support enumeration")
		return win32com.client.util.Iterator(ob, None)

class ICiBarcodes(DispatchBaseClass):
	'ICiBarcodes Interface'
	CLSID = IID('{41F7F4D4-9FC1-46C6-92E5-2A3457CE3D5E}')
	coclass_clsid = IID('{DAB01618-F817-4662-ADBA-46EE1C94921A}')

	def Add(self, pVal=defaultNamedNotOptArg):
		'method Add'
		return self._oleobj_.InvokeTypes(1, LCID, 1, (24, 0), ((9, 1),),pVal
			)

	def AddLocal(self, pVal=defaultNamedNotOptArg):
		'method AddLocal'
		return self._oleobj_.InvokeTypes(5, LCID, 1, (24, 0), ((9, 1),),pVal
			)

	# Result is of type ICiBarcode
	# The method Item is actually a property, but must be used as a method to correctly pass the arguments
	def Item(self, n=defaultNamedNotOptArg):
		'Barcode Item (1-based)'
		ret = self._oleobj_.InvokeTypes(0, LCID, 2, (9, 0), ((3, 1),),n
			)
		if ret is not None:
			ret = Dispatch(ret, u'Item', '{4ED88240-0BE1-11D4-B5F6-009FC6000000}')
		return ret

	# Result is of type ICiBarcode
	def Remove(self, n=defaultNamedNotOptArg):
		'method Remove'
		ret = self._oleobj_.InvokeTypes(2, LCID, 1, (9, 0), ((3, 1),),n
			)
		if ret is not None:
			ret = Dispatch(ret, u'Remove', '{4ED88240-0BE1-11D4-B5F6-009FC6000000}')
		return ret

	_prop_map_get_ = {
		"Count": (3, 2, (3, 0), (), "Count", None),
		"o": (4, 2, (20, 0), (), "o", None),
	}
	_prop_map_put_ = {
		"o": ((4, LCID, 4, 0),()),
	}
	# Default method for this class is 'Item'
	def __call__(self, n=defaultNamedNotOptArg):
		'Barcode Item (1-based)'
		ret = self._oleobj_.InvokeTypes(0, LCID, 2, (9, 0), ((3, 1),),n
			)
		if ret is not None:
			ret = Dispatch(ret, '__call__', '{4ED88240-0BE1-11D4-B5F6-009FC6000000}')
		return ret

	def __unicode__(self, *args):
		try:
			return unicode(self.__call__(*args))
		except pythoncom.com_error:
			return repr(self)
	def __str__(self, *args):
		return str(self.__unicode__(*args))
	def __int__(self, *args):
		return int(self.__call__(*args))
	def __iter__(self):
		"Return a Python iterator for this object"
		try:
			ob = self._oleobj_.InvokeTypes(-4,LCID,2,(13, 10),())
		except pythoncom.error:
			raise TypeError("This object does not support enumeration")
		return win32com.client.util.Iterator(ob, '{4ED88240-0BE1-11D4-B5F6-009FC6000000}')
	#This class has Count() property - allow len(ob) to provide this
	def __len__(self):
		return self._ApplyTypes_(*(3, 2, (3, 0), (), "Count", None))
	#This class has a __len__ - this is needed so 'if object:' always returns TRUE.
	def __nonzero__(self):
		return True

class ICiDataMatrix(DispatchBaseClass):
	'ICiDataMatrix Interface'
	CLSID = IID('{8B79E556-FAD7-4339-8A8F-2C35D5C42C6F}')
	coclass_clsid = IID('{90E9D617-A4B1-4DDE-B842-60BECC114254}')

	def Find(self, MaxBarcodes=0):
		'Find multiple barcodes'
		return self._oleobj_.InvokeTypes(10, LCID, 1, (3, 0), ((3, 49),),MaxBarcodes
			)

	# Result is of type ICiBarcode
	def FirstBarcode(self):
		'Find first barcode'
		ret = self._oleobj_.InvokeTypes(2, LCID, 1, (9, 0), (),)
		if ret is not None:
			ret = Dispatch(ret, u'FirstBarcode', '{4ED88240-0BE1-11D4-B5F6-009FC6000000}')
		return ret

	def Fx1(self, par1=0, par2=0):
		ret = self._oleobj_.InvokeTypes(11, LCID, 1, (13, 0), ((3, 49), (3, 49)),par1
			, par2)
		if ret is not None:
			# See if this IUnknown is really an IDispatch
			try:
				ret = ret.QueryInterface(pythoncom.IID_IDispatch)
			except pythoncom.error:
				return ret
			ret = Dispatch(ret, u'Fx1', None)
		return ret

	# Result is of type ICiBarcode
	def NextBarcode(self):
		'Find another barcode'
		ret = self._oleobj_.InvokeTypes(3, LCID, 1, (9, 0), (),)
		if ret is not None:
			ret = Dispatch(ret, u'NextBarcode', '{4ED88240-0BE1-11D4-B5F6-009FC6000000}')
		return ret

	# The method Setcx2l is actually a property, but must be used as a method to correctly pass the arguments
	def Setcx2l(self, i=defaultNamedNotOptArg, arg1=defaultUnnamedArg):
		'property cx2l'
		return self._oleobj_.InvokeTypes(12, LCID, 4, (24, 0), ((3, 1), (3, 1)),i
			, arg1)

	# The method cx2l is actually a property, but must be used as a method to correctly pass the arguments
	def cx2l(self, i=defaultNamedNotOptArg):
		'property cx2l'
		return self._oleobj_.InvokeTypes(12, LCID, 2, (3, 0), ((3, 1),),i
			)

	_prop_map_get_ = {
		"Algorithm": (4, 2, (3, 0), (), "Algorithm", None),
		# Method 'Barcodes' returns object of type 'ICiBarcodes'
		"Barcodes": (9, 2, (9, 0), (), "Barcodes", '{41F7F4D4-9FC1-46C6-92E5-2A3457CE3D5E}'),
		"DiagFlags": (7, 2, (3, 0), (), "DiagFlags", None),
		"Directions": (8, 2, (3, 0), (), "Directions", None),
		"Encodings": (13, 2, (3, 0), (), "Encodings", None),
		# Method 'Image' returns object of type 'ICiImage'
		"Image": (5, 2, (9, 0), (), "Image", '{F2BCF189-0B27-11D4-B5F5-9CC767000000}'),
		"o": (14, 2, (20, 0), (), "o", None),
	}
	_prop_map_put_ = {
		"Algorithm": ((4, LCID, 4, 0),()),
		"DiagFlags": ((7, LCID, 4, 0),()),
		"Directions": ((8, LCID, 4, 0),()),
		"Encodings": ((13, LCID, 4, 0),()),
		"Image": ((5, LCID, 4, 0),()),
		"o": ((14, LCID, 4, 0),()),
	}
	def __iter__(self):
		"Return a Python iterator for this object"
		try:
			ob = self._oleobj_.InvokeTypes(-4,LCID,3,(13, 10),())
		except pythoncom.error:
			raise TypeError("This object does not support enumeration")
		return win32com.client.util.Iterator(ob, None)

class ICiImage(DispatchBaseClass):
	'ICiImage Interface'
	CLSID = IID('{F2BCF189-0B27-11D4-B5F5-9CC767000000}')
	coclass_clsid = IID('{F2BCF18A-0B27-11D4-B5F5-9CC767000000}')

	def Append(self, FileName=defaultNamedNotOptArg, Format=7):
		'Append image to file'
		return self._oleobj_.InvokeTypes(14, LCID, 1, (24, 0), ((8, 1), (3, 49)),FileName
			, Format)

	def Clear(self):
		'Set all pixels to white'
		return self._oleobj_.InvokeTypes(8, LCID, 1, (24, 0), (),)

	def Close(self):
		'Close image'
		return self._oleobj_.InvokeTypes(2, LCID, 1, (24, 0), (),)

	def Copy(self, ImageFrom=defaultNamedNotOptArg):
		'Copy image to another image'
		return self._oleobj_.InvokeTypes(20, LCID, 1, (24, 0), ((9, 0),),ImageFrom
			)

	def CopyToClipboard(self):
		'Copy image to clipboard'
		return self._oleobj_.InvokeTypes(29, LCID, 1, (24, 0), (),)

	def Create(self, Width=defaultNamedNotOptArg, Height=defaultNamedNotOptArg):
		'Create a Bitonal image'
		return self._oleobj_.InvokeTypes(1, LCID, 1, (24, 0), ((3, 1), (3, 1)),Width
			, Height)

	def CreateBpp(self, Width=defaultNamedNotOptArg, Height=defaultNamedNotOptArg, BitsPerPixel=defaultNamedNotOptArg):
		'Create an image (bpp = 1, 8, 24)'
		return self._oleobj_.InvokeTypes(54, LCID, 1, (24, 0), ((3, 1), (3, 1), (3, 1)),Width
			, Height, BitsPerPixel)

	# Result is of type ICiImage
	def CreateZone(self, left=0, top=0, right=0, bottom=0):
		'Create new Zone within image'
		ret = self._oleobj_.InvokeTypes(45, LCID, 1, (9, 0), ((3, 49), (3, 49), (3, 49), (3, 49)),left
			, top, right, bottom)
		if ret is not None:
			ret = Dispatch(ret, u'CreateZone', '{F2BCF189-0B27-11D4-B5F5-9CC767000000}')
		return ret

	# Result is of type ICiImage
	def CreateZoneRect(self, Rect=defaultNamedNotOptArg):
		'Create new Zone within image'
		ret = self._oleobj_.InvokeTypes(43, LCID, 1, (9, 0), ((9, 1),),Rect
			)
		if ret is not None:
			ret = Dispatch(ret, u'CreateZoneRect', '{F2BCF189-0B27-11D4-B5F5-9CC767000000}')
		return ret

	def Crop(self, left=defaultNamedNotOptArg, top=defaultNamedNotOptArg, right=defaultNamedNotOptArg, bottom=defaultNamedNotOptArg):
		'Crop rectangle'
		return self._oleobj_.InvokeTypes(51, LCID, 1, (24, 0), ((3, 1), (3, 1), (3, 1), (3, 1)),left
			, top, right, bottom)

	# Result is of type ICiImage
	def Duplicate(self):
		'Create a duplicate of this CiImage object'
		ret = self._oleobj_.InvokeTypes(47, LCID, 1, (9, 0), (),)
		if ret is not None:
			ret = Dispatch(ret, u'Duplicate', '{F2BCF189-0B27-11D4-B5F5-9CC767000000}')
		return ret

	def Flip(self):
		'Rotate image upside down'
		return self._oleobj_.InvokeTypes(13, LCID, 1, (24, 0), (),)

	def FlipHorz(self):
		'Flip image around horizontal axis'
		return self._oleobj_.InvokeTypes(10, LCID, 1, (24, 0), (),)

	def FlipVert(self):
		'Flip image around vertical axis'
		return self._oleobj_.InvokeTypes(9, LCID, 1, (24, 0), (),)

	# The method Info is actually a property, but must be used as a method to correctly pass the arguments
	def Info(self, Type=defaultNamedNotOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(68, LCID, 2, (8, 0), ((8, 1),),Type
			)

	def Invert(self):
		'Invert image pixels'
		return self._oleobj_.InvokeTypes(6, LCID, 1, (24, 0), (),)

	def IsBitonal(self):
		'Is image bitonal'
		return self._oleobj_.InvokeTypes(57, LCID, 1, (3, 0), (),)

	def LoadFromMemory(self, pData=defaultNamedNotOptArg):
		'Load image bits from image memory'
		return self._oleobj_.InvokeTypes(28, LCID, 1, (24, 0), ((12, 1),),pData
			)

	# The method LogFlags is actually a property, but must be used as a method to correctly pass the arguments
	def LogFlags(self, LogType=defaultNamedNotOptArg):
		'Logging control flags'
		return self._oleobj_.InvokeTypes(49, LCID, 2, (3, 0), ((3, 1),),LogType
			)

	def Open(self, FileName=defaultNamedNotOptArg, PageNumber=1):
		'Create image from image file'
		return self._oleobj_.InvokeTypes(3, LCID, 1, (24, 0), ((8, 1), (3, 49)),FileName
			, PageNumber)

	def OpenFromBitmap(self, hBitmap=defaultNamedNotOptArg):
		'Create image from Windows Bitmap'
		return self._oleobj_.InvokeTypes(27, LCID, 1, (24, 0), ((20, 1),),hBitmap
			)

	def OpenFromClipboard(self):
		'Create image from Clipboard'
		return self._oleobj_.InvokeTypes(26, LCID, 1, (24, 0), (),)

	def RotateLeft(self):
		'Rotate image to the left'
		return self._oleobj_.InvokeTypes(12, LCID, 1, (24, 0), (),)

	def RotateRight(self):
		'Rotate image to the right'
		return self._oleobj_.InvokeTypes(11, LCID, 1, (24, 0), (),)

	def Save(self):
		'Save image into its image file'
		return self._oleobj_.InvokeTypes(25, LCID, 1, (24, 0), (),)

	def SaveAs(self, FileName=defaultNamedNotOptArg, Format=1):
		'Save image in new file'
		return self._oleobj_.InvokeTypes(5, LCID, 1, (24, 0), ((8, 1), (3, 49)),FileName
			, Format)

	def SaveToBitmap(self):
		'Copy image to new Windows Bitmap'
		return self._oleobj_.InvokeTypes(30, LCID, 1, (20, 0), (),)

	def SaveToDIB(self):
		'Copy image to new Windows DIB'
		return self._oleobj_.InvokeTypes(31, LCID, 1, (20, 0), (),)

	def SaveToMemory(self):
		'Copy image bits to image memory'
		return self._ApplyTypes_(32, 1, (12, 0), (), u'SaveToMemory', None,)

	def ScaleToDIB(self, ScaleX=defaultNamedNotOptArg, ScaleY=defaultNamedNotOptArg):
		'Moved to Tools'
		return self._oleobj_.InvokeTypes(40, LCID, 1, (20, 0), ((5, 1), (5, 1)),ScaleX
			, ScaleY)

	# The method SetInfo is actually a property, but must be used as a method to correctly pass the arguments
	def SetInfo(self, Type=defaultNamedNotOptArg, arg1=defaultUnnamedArg):
		return self._oleobj_.InvokeTypes(68, LCID, 4, (24, 0), ((8, 1), (8, 1)),Type
			, arg1)

	# The method SetLogFlags is actually a property, but must be used as a method to correctly pass the arguments
	def SetLogFlags(self, LogType=defaultNamedNotOptArg, arg1=defaultUnnamedArg):
		'Logging control flags'
		return self._oleobj_.InvokeTypes(49, LCID, 4, (24, 0), ((3, 1), (3, 1)),LogType
			, arg1)

	# The method Setcx2l is actually a property, but must be used as a method to correctly pass the arguments
	def Setcx2l(self, i=defaultNamedNotOptArg, arg1=defaultUnnamedArg):
		'property cx2l'
		return self._oleobj_.InvokeTypes(62, LCID, 4, (24, 0), ((3, 1), (3, 1)),i
			, arg1)

	def ToBitonal(self):
		'method ToBitonal'
		return self._oleobj_.InvokeTypes(64, LCID, 1, (24, 0), (),)

	def ToGrayscale(self):
		'method ToGrayscale'
		return self._oleobj_.InvokeTypes(65, LCID, 1, (24, 0), (),)

	# The method cx2l is actually a property, but must be used as a method to correctly pass the arguments
	def cx2l(self, i=defaultNamedNotOptArg):
		'property cx2l'
		return self._oleobj_.InvokeTypes(62, LCID, 2, (3, 0), ((3, 1),),i
			)

	_prop_map_get_ = {
		"BitsPerPixel": (53, 2, (3, 0), (), "BitsPerPixel", None),
		"Buffer": (55, 2, (20, 0), (), "Buffer", None),
		"CiCx": (58, 2, (9, 0), (), "CiCx", None),
		"FileName": (22, 2, (8, 0), (), "FileName", None),
		"FileSize": (59, 2, (5, 0), (), "FileSize", None),
		"Format": (41, 2, (3, 0), (), "Format", None),
		"Handle": (42, 2, (3, 0), (), "Handle", None),
		"Height": (17, 2, (3, 0), (), "Height", None),
		"HorzDpi": (18, 2, (3, 0), (), "HorzDpi", None),
		"IsModified": (21, 2, (3, 0), (), "IsModified", None),
		"IsValid": (61, 2, (3, 0), (), "IsValid", None),
		"IsZone": (44, 2, (3, 0), (), "IsZone", None),
		"JpegQuality": (60, 2, (3, 0), (), "JpegQuality", None),
		"LineBytes": (52, 2, (3, 0), (), "LineBytes", None),
		"LogSignature": (50, 2, (8, 0), (), "LogSignature", None),
		"PageCount": (24, 2, (3, 0), (), "PageCount", None),
		"PageNumber": (23, 2, (3, 0), (), "PageNumber", None),
		# Method 'Parent' returns object of type 'ICiImage'
		"Parent": (46, 2, (9, 0), (), "Parent", '{F2BCF189-0B27-11D4-B5F5-9CC767000000}'),
		# Method 'Pdf' returns object of type 'ICiPdf'
		"Pdf": (63, 2, (9, 0), (), "Pdf", '{70A6F899-6298-447E-951C-07430C0FF812}'),
		"VertDpi": (19, 2, (3, 0), (), "VertDpi", None),
		"Width": (16, 2, (3, 0), (), "Width", None),
		# Method 'Zone' returns object of type 'ICiRect'
		"Zone": (4, 2, (9, 0), (), "Zone", '{4ED88244-0BE1-11D4-B5F6-009FC6000000}'),
		"o": (69, 2, (20, 0), (), "o", None),
		"pComprBitonal": (67, 2, (3, 0), (), "pComprBitonal", None),
		"pComprColor": (66, 2, (3, 0), (), "pComprColor", None),
		"pScaleBmpBrightness": (37, 2, (3, 0), (), "pScaleBmpBrightness", None),
		"pScaleBmpContrast": (38, 2, (3, 0), (), "pScaleBmpContrast", None),
		"pScaleBmpType": (36, 2, (3, 0), (), "pScaleBmpType", None),
		"pScaleThreshold": (34, 2, (3, 0), (), "pScaleThreshold", None),
		"pScaleType": (33, 2, (3, 0), (), "pScaleType", None),
	}
	_prop_map_put_ = {
		"HorzDpi": ((18, LCID, 4, 0),()),
		"JpegQuality": ((60, LCID, 4, 0),()),
		"LogSignature": ((50, LCID, 4, 0),()),
		"VertDpi": ((19, LCID, 4, 0),()),
		"o": ((69, LCID, 4, 0),()),
		"pComprBitonal": ((67, LCID, 4, 0),()),
		"pComprColor": ((66, LCID, 4, 0),()),
		"pScaleBmpBrightness": ((37, LCID, 4, 0),()),
		"pScaleBmpContrast": ((38, LCID, 4, 0),()),
		"pScaleBmpType": ((36, LCID, 4, 0),()),
		"pScaleThreshold": ((34, LCID, 4, 0),()),
		"pScaleType": ((33, LCID, 4, 0),()),
	}
	def __iter__(self):
		"Return a Python iterator for this object"
		try:
			ob = self._oleobj_.InvokeTypes(-4,LCID,3,(13, 10),())
		except pythoncom.error:
			raise TypeError("This object does not support enumeration")
		return win32com.client.util.Iterator(ob, None)

class ICiLine(DispatchBaseClass):
	'ICiLine Interface'
	CLSID = IID('{B8E5EE38-BB0D-4561-B8D3-26C18C8817EE}')
	coclass_clsid = IID('{A7A8BF7F-8CB8-49DC-8A76-D0A1A145189C}')

	_prop_map_get_ = {
		"Angle": (37, 2, (5, 0), (), "Angle", None),
		"Direction": (35, 2, (3, 0), (), "Direction", None),
		# Method 'End' returns object of type 'ICiPoint'
		"End": (40, 2, (9, 0), (), "End", '{8C531E23-84B0-431E-B39E-849AB24613AF}'),
		# Method 'Rect' returns object of type 'ICiRect'
		"Rect": (38, 2, (9, 0), (), "Rect", '{4ED88244-0BE1-11D4-B5F6-009FC6000000}'),
		# Method 'Start' returns object of type 'ICiPoint'
		"Start": (39, 2, (9, 0), (), "Start", '{8C531E23-84B0-431E-B39E-849AB24613AF}'),
		"Thickness": (36, 2, (5, 0), (), "Thickness", None),
		"o": (41, 2, (20, 0), (), "o", None),
	}
	_prop_map_put_ = {
		"o": ((41, LCID, 4, 0),()),
	}
	def __iter__(self):
		"Return a Python iterator for this object"
		try:
			ob = self._oleobj_.InvokeTypes(-4,LCID,3,(13, 10),())
		except pythoncom.error:
			raise TypeError("This object does not support enumeration")
		return win32com.client.util.Iterator(ob, None)

class ICiObject(DispatchBaseClass):
	'ICiObject Interface'
	CLSID = IID('{59A0E32D-5050-47F5-A21B-F00397A21FCC}')
	coclass_clsid = IID('{4BBE294D-3C2A-4698-8B5F-84B1D3A6F621}')

	# The method Setcx2l is actually a property, but must be used as a method to correctly pass the arguments
	def Setcx2l(self, i=defaultNamedNotOptArg, arg1=defaultUnnamedArg):
		'property cx2l'
		return self._oleobj_.InvokeTypes(7, LCID, 4, (24, 0), ((3, 1), (3, 1)),i
			, arg1)

	# The method Setcx3d is actually a property, but must be used as a method to correctly pass the arguments
	def Setcx3d(self, i=defaultNamedNotOptArg, arg1=defaultUnnamedArg):
		'property cx3d'
		return self._oleobj_.InvokeTypes(6, LCID, 4, (24, 0), ((3, 1), (5, 1)),i
			, arg1)

	# The method cx2l is actually a property, but must be used as a method to correctly pass the arguments
	def cx2l(self, i=defaultNamedNotOptArg):
		'property cx2l'
		return self._oleobj_.InvokeTypes(7, LCID, 2, (3, 0), ((3, 1),),i
			)

	# The method cx3d is actually a property, but must be used as a method to correctly pass the arguments
	def cx3d(self, i=defaultNamedNotOptArg):
		'property cx3d'
		return self._oleobj_.InvokeTypes(6, LCID, 2, (5, 0), ((3, 1),),i
			)

	_prop_map_get_ = {
		"Intervals": (4, 2, (3, 0), (), "Intervals", None),
		"Pixels": (3, 2, (3, 0), (), "Pixels", None),
		# Method 'Rect' returns object of type 'ICiRect'
		"Rect": (5, 2, (9, 0), (), "Rect", '{4ED88244-0BE1-11D4-B5F6-009FC6000000}'),
		"o": (8, 2, (20, 0), (), "o", None),
	}
	_prop_map_put_ = {
		"o": ((8, LCID, 4, 0),()),
	}
	def __iter__(self):
		"Return a Python iterator for this object"
		try:
			ob = self._oleobj_.InvokeTypes(-4,LCID,3,(13, 10),())
		except pythoncom.error:
			raise TypeError("This object does not support enumeration")
		return win32com.client.util.Iterator(ob, None)

class ICiPdf(DispatchBaseClass):
	'ICiPdf Interface'
	CLSID = IID('{70A6F899-6298-447E-951C-07430C0FF812}')
	coclass_clsid = IID('{FB2E2C05-DB40-4A6F-8E52-0243621D7734}')

	_prop_map_get_ = {
		"Author": (13, 2, (8, 0), (), "Author", None),
		"CreationDate": (12, 2, (8, 0), (), "CreationDate", None),
		"Creator": (11, 2, (8, 0), (), "Creator", None),
		"ImageAlignment": (22, 2, (3, 0), (), "ImageAlignment", None),
		"Keywords": (17, 2, (8, 0), (), "Keywords", None),
		"ModDate": (18, 2, (8, 0), (), "ModDate", None),
		"PageOrientation": (21, 2, (3, 0), (), "PageOrientation", None),
		"PageSize": (20, 2, (3, 0), (), "PageSize", None),
		"Producer": (14, 2, (8, 0), (), "Producer", None),
		"Ptr": (19, 2, (16408, 0), (), "Ptr", None),
		"Subject": (16, 2, (8, 0), (), "Subject", None),
		"Title": (15, 2, (8, 0), (), "Title", None),
		"dpiRasterBw": (3, 2, (3, 0), (), "dpiRasterBw", None),
		"dpiRasterGs": (4, 2, (3, 0), (), "dpiRasterGs", None),
		"dpiRasterRgb": (5, 2, (3, 0), (), "dpiRasterRgb", None),
		"minImageHeight": (9, 2, (5, 0), (), "minImageHeight", None),
		"minImageWidth": (8, 2, (5, 0), (), "minImageWidth", None),
		"o": (23, 2, (20, 0), (), "o", None),
		"rasterColorMode": (7, 2, (3, 0), (), "rasterColorMode", None),
		"readEnabled": (1, 2, (3, 0), (), "readEnabled", None),
		"readMode": (6, 2, (3, 0), (), "readMode", None),
		"useMinImageColors": (10, 2, (3, 0), (), "useMinImageColors", None),
		"writeEnabled": (2, 2, (3, 0), (), "writeEnabled", None),
	}
	_prop_map_put_ = {
		"Author": ((13, LCID, 4, 0),()),
		"CreationDate": ((12, LCID, 4, 0),()),
		"Creator": ((11, LCID, 4, 0),()),
		"ImageAlignment": ((22, LCID, 4, 0),()),
		"Keywords": ((17, LCID, 4, 0),()),
		"ModDate": ((18, LCID, 4, 0),()),
		"PageOrientation": ((21, LCID, 4, 0),()),
		"PageSize": ((20, LCID, 4, 0),()),
		"Producer": ((14, LCID, 4, 0),()),
		"Subject": ((16, LCID, 4, 0),()),
		"Title": ((15, LCID, 4, 0),()),
		"dpiRasterBw": ((3, LCID, 4, 0),()),
		"dpiRasterGs": ((4, LCID, 4, 0),()),
		"dpiRasterRgb": ((5, LCID, 4, 0),()),
		"minImageHeight": ((9, LCID, 4, 0),()),
		"minImageWidth": ((8, LCID, 4, 0),()),
		"o": ((23, LCID, 4, 0),()),
		"rasterColorMode": ((7, LCID, 4, 0),()),
		"readMode": ((6, LCID, 4, 0),()),
		"useMinImageColors": ((10, LCID, 4, 0),()),
	}
	def __iter__(self):
		"Return a Python iterator for this object"
		try:
			ob = self._oleobj_.InvokeTypes(-4,LCID,3,(13, 10),())
		except pythoncom.error:
			raise TypeError("This object does not support enumeration")
		return win32com.client.util.Iterator(ob, None)

class ICiPdf417(DispatchBaseClass):
	'ICiPdf417 Interface'
	CLSID = IID('{8B79E556-FAD7-4339-8A8F-2C35D5C42C6E}')
	coclass_clsid = IID('{90E9D617-A4B1-4DDE-B842-60BECC114253}')

	def Find(self, MaxBarcodes=0):
		'Find multiple barcodes'
		return self._oleobj_.InvokeTypes(10, LCID, 1, (3, 0), ((3, 49),),MaxBarcodes
			)

	# Result is of type ICiBarcode
	def FirstBarcode(self):
		'Find first barcode'
		ret = self._oleobj_.InvokeTypes(2, LCID, 1, (9, 0), (),)
		if ret is not None:
			ret = Dispatch(ret, u'FirstBarcode', '{4ED88240-0BE1-11D4-B5F6-009FC6000000}')
		return ret

	def Fx1(self, par1=0, par2=0):
		ret = self._oleobj_.InvokeTypes(11, LCID, 1, (13, 0), ((3, 49), (3, 49)),par1
			, par2)
		if ret is not None:
			# See if this IUnknown is really an IDispatch
			try:
				ret = ret.QueryInterface(pythoncom.IID_IDispatch)
			except pythoncom.error:
				return ret
			ret = Dispatch(ret, u'Fx1', None)
		return ret

	# Result is of type ICiBarcode
	def NextBarcode(self):
		'Find another barcode'
		ret = self._oleobj_.InvokeTypes(3, LCID, 1, (9, 0), (),)
		if ret is not None:
			ret = Dispatch(ret, u'NextBarcode', '{4ED88240-0BE1-11D4-B5F6-009FC6000000}')
		return ret

	# The method Setcx2l is actually a property, but must be used as a method to correctly pass the arguments
	def Setcx2l(self, i=defaultNamedNotOptArg, arg1=defaultUnnamedArg):
		'property cx2l'
		return self._oleobj_.InvokeTypes(12, LCID, 4, (24, 0), ((3, 1), (3, 1)),i
			, arg1)

	# The method cx2l is actually a property, but must be used as a method to correctly pass the arguments
	def cx2l(self, i=defaultNamedNotOptArg):
		'property cx2l'
		return self._oleobj_.InvokeTypes(12, LCID, 2, (3, 0), ((3, 1),),i
			)

	_prop_map_get_ = {
		"Algorithm": (4, 2, (3, 0), (), "Algorithm", None),
		# Method 'Barcodes' returns object of type 'ICiBarcodes'
		"Barcodes": (9, 2, (9, 0), (), "Barcodes", '{41F7F4D4-9FC1-46C6-92E5-2A3457CE3D5E}'),
		"DiagFlags": (7, 2, (3, 0), (), "DiagFlags", None),
		"Directions": (8, 2, (3, 0), (), "Directions", None),
		"Encodings": (13, 2, (3, 0), (), "Encodings", None),
		# Method 'Image' returns object of type 'ICiImage'
		"Image": (5, 2, (9, 0), (), "Image", '{F2BCF189-0B27-11D4-B5F5-9CC767000000}'),
		"o": (14, 2, (20, 0), (), "o", None),
	}
	_prop_map_put_ = {
		"Algorithm": ((4, LCID, 4, 0),()),
		"DiagFlags": ((7, LCID, 4, 0),()),
		"Directions": ((8, LCID, 4, 0),()),
		"Encodings": ((13, LCID, 4, 0),()),
		"Image": ((5, LCID, 4, 0),()),
		"o": ((14, LCID, 4, 0),()),
	}
	def __iter__(self):
		"Return a Python iterator for this object"
		try:
			ob = self._oleobj_.InvokeTypes(-4,LCID,3,(13, 10),())
		except pythoncom.error:
			raise TypeError("This object does not support enumeration")
		return win32com.client.util.Iterator(ob, None)

class ICiPoint(DispatchBaseClass):
	'ICiPoint Interface'
	CLSID = IID('{8C531E23-84B0-431E-B39E-849AB24613AF}')
	coclass_clsid = IID('{A7E1D34A-24DA-4D97-AF2E-CE7E4481E1E2}')

	_prop_map_get_ = {
		"o": (3, 2, (20, 0), (), "o", None),
		"x": (1, 2, (3, 0), (), "x", None),
		"y": (2, 2, (3, 0), (), "y", None),
	}
	_prop_map_put_ = {
		"o": ((3, LCID, 4, 0),()),
		"x": ((1, LCID, 4, 0),()),
		"y": ((2, LCID, 4, 0),()),
	}
	def __iter__(self):
		"Return a Python iterator for this object"
		try:
			ob = self._oleobj_.InvokeTypes(-4,LCID,3,(13, 10),())
		except pythoncom.error:
			raise TypeError("This object does not support enumeration")
		return win32com.client.util.Iterator(ob, None)

class ICiQR(DispatchBaseClass):
	'ICiQR Interface'
	CLSID = IID('{8B79E556-FAD7-4339-8A8F-2C35D5C42C70}')
	coclass_clsid = IID('{90E9D617-A4B1-4DDE-B842-60BECC114255}')

	def Find(self, MaxBarcodes=0):
		'Find multiple barcodes'
		return self._oleobj_.InvokeTypes(10, LCID, 1, (3, 0), ((3, 49),),MaxBarcodes
			)

	# Result is of type ICiBarcode
	def FirstBarcode(self):
		'Find first barcode'
		ret = self._oleobj_.InvokeTypes(2, LCID, 1, (9, 0), (),)
		if ret is not None:
			ret = Dispatch(ret, u'FirstBarcode', '{4ED88240-0BE1-11D4-B5F6-009FC6000000}')
		return ret

	def Fx1(self, par1=0, par2=0):
		ret = self._oleobj_.InvokeTypes(11, LCID, 1, (13, 0), ((3, 49), (3, 49)),par1
			, par2)
		if ret is not None:
			# See if this IUnknown is really an IDispatch
			try:
				ret = ret.QueryInterface(pythoncom.IID_IDispatch)
			except pythoncom.error:
				return ret
			ret = Dispatch(ret, u'Fx1', None)
		return ret

	# Result is of type ICiBarcode
	def NextBarcode(self):
		'Find another barcode'
		ret = self._oleobj_.InvokeTypes(3, LCID, 1, (9, 0), (),)
		if ret is not None:
			ret = Dispatch(ret, u'NextBarcode', '{4ED88240-0BE1-11D4-B5F6-009FC6000000}')
		return ret

	# The method Setcx2l is actually a property, but must be used as a method to correctly pass the arguments
	def Setcx2l(self, i=defaultNamedNotOptArg, arg1=defaultUnnamedArg):
		'property cx2l'
		return self._oleobj_.InvokeTypes(12, LCID, 4, (24, 0), ((3, 1), (3, 1)),i
			, arg1)

	# The method cx2l is actually a property, but must be used as a method to correctly pass the arguments
	def cx2l(self, i=defaultNamedNotOptArg):
		'property cx2l'
		return self._oleobj_.InvokeTypes(12, LCID, 2, (3, 0), ((3, 1),),i
			)

	_prop_map_get_ = {
		"Algorithm": (4, 2, (3, 0), (), "Algorithm", None),
		# Method 'Barcodes' returns object of type 'ICiBarcodes'
		"Barcodes": (9, 2, (9, 0), (), "Barcodes", '{41F7F4D4-9FC1-46C6-92E5-2A3457CE3D5E}'),
		"DiagFlags": (7, 2, (3, 0), (), "DiagFlags", None),
		"Directions": (8, 2, (3, 0), (), "Directions", None),
		"Encodings": (13, 2, (3, 0), (), "Encodings", None),
		# Method 'Image' returns object of type 'ICiImage'
		"Image": (5, 2, (9, 0), (), "Image", '{F2BCF189-0B27-11D4-B5F5-9CC767000000}'),
		"o": (14, 2, (20, 0), (), "o", None),
	}
	_prop_map_put_ = {
		"Algorithm": ((4, LCID, 4, 0),()),
		"DiagFlags": ((7, LCID, 4, 0),()),
		"Directions": ((8, LCID, 4, 0),()),
		"Encodings": ((13, LCID, 4, 0),()),
		"Image": ((5, LCID, 4, 0),()),
		"o": ((14, LCID, 4, 0),()),
	}
	def __iter__(self):
		"Return a Python iterator for this object"
		try:
			ob = self._oleobj_.InvokeTypes(-4,LCID,3,(13, 10),())
		except pythoncom.error:
			raise TypeError("This object does not support enumeration")
		return win32com.client.util.Iterator(ob, None)

class ICiRect(DispatchBaseClass):
	'ICiRect Interface'
	CLSID = IID('{4ED88244-0BE1-11D4-B5F6-009FC6000000}')
	coclass_clsid = IID('{4ED88245-0BE1-11D4-B5F6-009FC6000000}')

	def Empty(self):
		'Set rectangle coordinates to zero'
		return self._oleobj_.InvokeTypes(5, LCID, 1, (24, 0), (),)

	_prop_map_get_ = {
		"IsEmpty": (6, 2, (3, 0), (), "IsEmpty", None),
		"bottom": (2, 2, (3, 0), (), "bottom", None),
		"left": (3, 2, (3, 0), (), "left", None),
		"o": (7, 2, (20, 0), (), "o", None),
		"right": (4, 2, (3, 0), (), "right", None),
		"top": (1, 2, (3, 0), (), "top", None),
	}
	_prop_map_put_ = {
		"bottom": ((2, LCID, 4, 0),()),
		"left": ((3, LCID, 4, 0),()),
		"o": ((7, LCID, 4, 0),()),
		"right": ((4, LCID, 4, 0),()),
		"top": ((1, LCID, 4, 0),()),
	}
	def __iter__(self):
		"Return a Python iterator for this object"
		try:
			ob = self._oleobj_.InvokeTypes(-4,LCID,3,(13, 10),())
		except pythoncom.error:
			raise TypeError("This object does not support enumeration")
		return win32com.client.util.Iterator(ob, None)

class ICiRepair(DispatchBaseClass):
	'ICiRepair Interface'
	CLSID = IID('{63F6480C-997E-4FDE-AD63-A24E5F0FFDC7}')
	coclass_clsid = IID('{CB149079-A739-4178-A4DA-BACA546C3728}')

	def AdvancedBinarize(self, targetDpi=0, reserved1=0.0, reserved2=0.0):
		'Advanced Binarize'
		return self._oleobj_.InvokeTypes(47, LCID, 1, (24, 0), ((3, 49), (5, 49), (5, 49)),targetDpi
			, reserved1, reserved2)

	def AutoCrop(self, NewLeftMargin=defaultNamedNotOptArg, NewTopMargin=defaultNamedNotOptArg, NewRightMargin=defaultNamedNotOptArg, NewBottomMargin=defaultNamedNotOptArg):
		'Set image margins'
		return self._oleobj_.InvokeTypes(30, LCID, 1, (24, 0), ((3, 1), (3, 1), (3, 1), (3, 1)),NewLeftMargin
			, NewTopMargin, NewRightMargin, NewBottomMargin)

	def AutoDeskew(self):
		'Automatically deskew image'
		return self._oleobj_.InvokeTypes(36, LCID, 1, (5, 0), (),)

	def AutoInvertBlocks(self, MinWidth=defaultNamedNotOptArg, MinHeight=defaultNamedNotOptArg):
		'Find and invert white-on-black objects'
		return self._oleobj_.InvokeTypes(26, LCID, 1, (24, 0), ((3, 1), (3, 1)),MinWidth
			, MinHeight)

	def AutoInvertImage(self, Threshold=defaultNamedNotOptArg):
		'Negative to Positive'
		return self._oleobj_.InvokeTypes(25, LCID, 1, (24, 0), ((3, 1),),Threshold
			)

	def AutoRegister(self, NewLeftMargin=defaultNamedNotOptArg, NewTopMargin=defaultNamedNotOptArg):
		'Set top and left margins'
		return self._oleobj_.InvokeTypes(31, LCID, 1, (24, 0), ((3, 1), (3, 1)),NewLeftMargin
			, NewTopMargin)

	def AutoRotate(self):
		'Automatically rotate image'
		return self._oleobj_.InvokeTypes(37, LCID, 1, (3, 0), (),)

	def BorderExtract(self, Flags=3, Algorithm=2):
		'Extract document image using borders'
		return self._oleobj_.InvokeTypes(41, LCID, 1, (24, 0), ((3, 49), (3, 49)),Flags
			, Algorithm)

	def CleanBorders(self):
		'Clean image borders'
		return self._oleobj_.InvokeTypes(20, LCID, 1, (24, 0), (),)

	def CleanNoise(self, NoiseSize=defaultNamedNotOptArg):
		'Remove noise objects'
		return self._oleobj_.InvokeTypes(24, LCID, 1, (24, 0), ((3, 1),),NoiseSize
			)

	def CleanNoiseExt(self, Flags=defaultNamedNotOptArg, maxNoiseSizeHorz=defaultNamedNotOptArg, maxNoiseSizeVert=defaultNamedNotOptArg, minObjectDistance=defaultNamedNotOptArg
			, reserved0=defaultNamedNotOptArg):
		'Remove noise objects (extended)'
		return self._oleobj_.InvokeTypes(50, LCID, 1, (24, 0), ((3, 1), (3, 1), (3, 1), (3, 1), (3, 1)),Flags
			, maxNoiseSizeHorz, maxNoiseSizeVert, minObjectDistance, reserved0)

	def ClearBackground(self, ThrLevel=30.0):
		'Set background to white'
		return self._oleobj_.InvokeTypes(42, LCID, 1, (24, 0), ((5, 49),),ThrLevel
			)

	def DeleteLines(self, Direction=defaultNamedNotOptArg, bRepair=65535):
		'Delete lines and reconnect intersected objects'
		return self._oleobj_.InvokeTypes(40, LCID, 1, (24, 0), ((3, 1), (3, 49)),Direction
			, bRepair)

	def FaxRemoveBlankLines(self):
		'Remove blank lines from faxed image'
		return self._oleobj_.InvokeTypes(2, LCID, 1, (24, 0), (),)

	def FaxRemoveHeader(self):
		'Remove header from faxed image'
		return self._oleobj_.InvokeTypes(3, LCID, 1, (24, 0), (),)

	def FaxStandardToFine(self):
		'Convert standard resolution fax image to fine resolution'
		return self._oleobj_.InvokeTypes(1, LCID, 1, (24, 0), (),)

	def IsBlankImage(self, reserved0=0, reserved1=0.0, reserved2=0.0):
		'Is image blank'
		return self._oleobj_.InvokeTypes(44, LCID, 1, (3, 0), ((3, 49), (5, 49), (5, 49)),reserved0
			, reserved1, reserved2)

	def MinimizeBitsPerPixel(self, reserved1=0.0, reserved2=0.0):
		'Minimize Bits per Pixel'
		return self._oleobj_.InvokeTypes(48, LCID, 1, (24, 0), ((5, 49), (5, 49)),reserved1
			, reserved2)

	def ReconstructLines(self, Direction=defaultNamedNotOptArg):
		'Find and straighten image lines'
		return self._oleobj_.InvokeTypes(29, LCID, 1, (24, 0), ((3, 1),),Direction
			)

	def RemoveHalftone(self):
		'Remove halftone from image background'
		return self._oleobj_.InvokeTypes(22, LCID, 1, (24, 0), (),)

	def RemovePunchHoles(self):
		'Remove punch holes form image'
		return self._oleobj_.InvokeTypes(21, LCID, 1, (24, 0), (),)

	def Resize(self, PageSize=defaultNamedNotOptArg, PageOrientation=0, ImageAlignment=0, Width=8.5
			, Height=11.0, Unit=1):
		'Resize image to page'
		return self._oleobj_.InvokeTypes(43, LCID, 1, (24, 0), ((3, 1), (3, 49), (3, 49), (5, 49), (5, 49), (3, 49)),PageSize
			, PageOrientation, ImageAlignment, Width, Height, Unit
			)

	# The method Setcx2l is actually a property, but must be used as a method to correctly pass the arguments
	def Setcx2l(self, i=defaultNamedNotOptArg, arg1=defaultUnnamedArg):
		'property cx2l'
		return self._oleobj_.InvokeTypes(45, LCID, 4, (24, 0), ((3, 1), (3, 1)),i
			, arg1)

	# The method Setcx3d is actually a property, but must be used as a method to correctly pass the arguments
	def Setcx3d(self, i=defaultNamedNotOptArg, arg1=defaultUnnamedArg):
		'property cx3d'
		return self._oleobj_.InvokeTypes(46, LCID, 4, (24, 0), ((3, 1), (5, 1)),i
			, arg1)

	def SmoothCharacters(self, Type=defaultNamedNotOptArg):
		'Smoothen character edges'
		return self._oleobj_.InvokeTypes(23, LCID, 1, (24, 0), ((3, 1),),Type
			)

	# The method cx2l is actually a property, but must be used as a method to correctly pass the arguments
	def cx2l(self, i=defaultNamedNotOptArg):
		'property cx2l'
		return self._oleobj_.InvokeTypes(45, LCID, 2, (3, 0), ((3, 1),),i
			)

	# The method cx3d is actually a property, but must be used as a method to correctly pass the arguments
	def cx3d(self, i=defaultNamedNotOptArg):
		'property cx3d'
		return self._oleobj_.InvokeTypes(46, LCID, 2, (5, 0), ((3, 1),),i
			)

	_prop_map_get_ = {
		# Method 'Image' returns object of type 'ICiImage'
		"Image": (39, 2, (9, 0), (), "Image", '{F2BCF189-0B27-11D4-B5F5-9CC767000000}'),
		"o": (51, 2, (20, 0), (), "o", None),
		"pLineCurvature": (19, 2, (3, 0), (), "pLineCurvature", None),
		"pMaxLineAngle": (18, 2, (5, 0), (), "pMaxLineAngle", None),
		"pMaxLineGap": (17, 2, (3, 0), (), "pMaxLineGap", None),
		"pMinLineLength": (16, 2, (3, 0), (), "pMinLineLength", None),
	}
	_prop_map_put_ = {
		"Image": ((39, LCID, 4, 0),()),
		"o": ((51, LCID, 4, 0),()),
		"pLineCurvature": ((19, LCID, 4, 0),()),
		"pMaxLineAngle": ((18, LCID, 4, 0),()),
		"pMaxLineGap": ((17, LCID, 4, 0),()),
		"pMinLineLength": ((16, LCID, 4, 0),()),
	}
	def __iter__(self):
		"Return a Python iterator for this object"
		try:
			ob = self._oleobj_.InvokeTypes(-4,LCID,3,(13, 10),())
		except pythoncom.error:
			raise TypeError("This object does not support enumeration")
		return win32com.client.util.Iterator(ob, None)

class ICiServer(DispatchBaseClass):
	'ICiServer Interface'
	CLSID = IID('{A34FC1A7-C73F-4706-886E-C4A33E37C6E5}')
	coclass_clsid = IID('{D836E300-A317-4C7E-BE61-D650CE242589}')

	# Result is of type ICiAdvColor
	def CreateAdvColor(self):
		'Create new CiAdvColor object'
		ret = self._oleobj_.InvokeTypes(17, LCID, 1, (9, 0), (),)
		if ret is not None:
			ret = Dispatch(ret, u'CreateAdvColor', '{8CBBAECA-9716-40CA-B8F6-0E9FF213522A}')
		return ret

	# Result is of type ICiBarcode
	def CreateBarcode(self):
		ret = self._oleobj_.InvokeTypes(18, LCID, 1, (9, 0), (),)
		if ret is not None:
			ret = Dispatch(ret, u'CreateBarcode', '{4ED88240-0BE1-11D4-B5F6-009FC6000000}')
		return ret

	# Result is of type ICiBarcodeBasic
	def CreateBarcodeBasic(self):
		'Create new CiBarcodeBasic object'
		ret = self._oleobj_.InvokeTypes(8, LCID, 1, (9, 0), (),)
		if ret is not None:
			ret = Dispatch(ret, u'CreateBarcodeBasic', '{21DA65F1-9E63-45E3-B081-F78096F9D6C3}')
		return ret

	# Result is of type ICiBarcodePro
	def CreateBarcodePro(self):
		'Create new CiBarcodePro object'
		ret = self._oleobj_.InvokeTypes(2, LCID, 1, (9, 0), (),)
		if ret is not None:
			ret = Dispatch(ret, u'CreateBarcodePro', '{BDDB0244-0CFD-11D4-B5F8-B89D57000000}')
		return ret

	# Result is of type ICiBarcodes
	def CreateBarcodes(self):
		ret = self._oleobj_.InvokeTypes(19, LCID, 1, (9, 0), (),)
		if ret is not None:
			ret = Dispatch(ret, u'CreateBarcodes', '{41F7F4D4-9FC1-46C6-92E5-2A3457CE3D5E}')
		return ret

	# Result is of type ICiDataMatrix
	def CreateDataMatrix(self):
		'Create new CiDataMatrix object'
		ret = self._oleobj_.InvokeTypes(15, LCID, 1, (9, 0), (),)
		if ret is not None:
			ret = Dispatch(ret, u'CreateDataMatrix', '{8B79E556-FAD7-4339-8A8F-2C35D5C42C6F}')
		return ret

	# Result is of type ICiImage
	def CreateImage(self):
		'Create new CiImage object'
		ret = self._oleobj_.InvokeTypes(1, LCID, 1, (9, 0), (),)
		if ret is not None:
			ret = Dispatch(ret, u'CreateImage', '{F2BCF189-0B27-11D4-B5F5-9CC767000000}')
		return ret

	# Result is of type ICiPdf417
	def CreatePdf417(self):
		'Create new CiPdf417 object'
		ret = self._oleobj_.InvokeTypes(9, LCID, 1, (9, 0), (),)
		if ret is not None:
			ret = Dispatch(ret, u'CreatePdf417', '{8B79E556-FAD7-4339-8A8F-2C35D5C42C6E}')
		return ret

	# Result is of type ICiQR
	def CreateQR(self):
		'Create new CiQR object'
		ret = self._oleobj_.InvokeTypes(23, LCID, 1, (9, 0), (),)
		if ret is not None:
			ret = Dispatch(ret, u'CreateQR', '{8B79E556-FAD7-4339-8A8F-2C35D5C42C70}')
		return ret

	# Result is of type ICiRect
	def CreateRect(self, left=0, top=0, right=0, bottom=0):
		'Create new CiRect object'
		ret = self._oleobj_.InvokeTypes(11, LCID, 1, (9, 0), ((3, 49), (3, 49), (3, 49), (3, 49)),left
			, top, right, bottom)
		if ret is not None:
			ret = Dispatch(ret, u'CreateRect', '{4ED88244-0BE1-11D4-B5F6-009FC6000000}')
		return ret

	# Result is of type ICiRepair
	def CreateRepair(self):
		'Create new CiRepair object'
		ret = self._oleobj_.InvokeTypes(5, LCID, 1, (9, 0), (),)
		if ret is not None:
			ret = Dispatch(ret, u'CreateRepair', '{63F6480C-997E-4FDE-AD63-A24E5F0FFDC7}')
		return ret

	# Result is of type ICiTools
	def CreateTools(self):
		'Create new CiTools object'
		ret = self._oleobj_.InvokeTypes(6, LCID, 1, (9, 0), (),)
		if ret is not None:
			ret = Dispatch(ret, u'CreateTools', '{316BC128-8995-471D-985D-B3E68E87C084}')
		return ret

	# The method GetDevMode is actually a property, but must be used as a method to correctly pass the arguments
	def GetDevMode(self, bGlobalDevMode=0):
		'Get DevMode'
		return self._oleobj_.InvokeTypes(20, LCID, 2, (3, 0), ((3, 49),),bGlobalDevMode
			)

	# The method Info is actually a property, but must be used as a method to correctly pass the arguments
	def Info(self, Type=defaultNamedNotOptArg, nParam=0):
		'Server Information'
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(16, LCID, 2, (8, 0), ((3, 1), (3, 49)),Type
			, nParam)

	def OpenExt(self, hModule=defaultNamedNotOptArg, MasterId=defaultNamedNotOptArg, pParam=defaultNamedNotOptArg):
		'Open ClearImage COM License'
		return self._oleobj_.InvokeTypes(10, LCID, 1, (24, 0), ((20, 1), (3, 1), (20, 1)),hModule
			, MasterId, pParam)

	def OpenUser(self, User=defaultNamedNotOptArg, key=defaultNamedNotOptArg, reserved=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(24, LCID, 1, (24, 0), ((8, 1), (8, 1), (8, 1)),User
			, key, reserved)

	# The method SetDevMode is actually a property, but must be used as a method to correctly pass the arguments
	def SetDevMode(self, bGlobalDevMode=0, arg1=defaultUnnamedArg):
		'Get DevMode'
		return self._oleobj_.InvokeTypes(20, LCID, 4, (24, 0), ((3, 49), (3, 1)),bGlobalDevMode
			, arg1)

	# The method SetVar is actually a property, but must be used as a method to correctly pass the arguments
	def SetVar(self, Name=defaultNamedNotOptArg, arg1=defaultUnnamedArg):
		return self._oleobj_.InvokeTypes(21, LCID, 4, (24, 0), ((8, 1), (8, 1)),Name
			, arg1)

	# The method Var is actually a property, but must be used as a method to correctly pass the arguments
	def Var(self, Name=defaultNamedNotOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(21, LCID, 2, (8, 0), ((8, 1),),Name
			)

	def uncompress(self, DataIn=defaultNamedNotOptArg, Encoding=defaultNamedNotOptArg, DataOut=pythoncom.Missing):
		'Uncompress Data'
		return self._ApplyTypes_(22, 1, (3, 0), ((12, 1), (16387, 3), (16396, 2)), u'uncompress', None,DataIn
			, Encoding, DataOut)

	_prop_map_get_ = {
		"DevMode": (20, 2, (3, 0), ((3, 49),), "DevMode", None),
		"VerMajor": (12, 2, (3, 0), (), "VerMajor", None),
		"VerMinor": (13, 2, (3, 0), (), "VerMinor", None),
		"VerRelease": (14, 2, (3, 0), (), "VerRelease", None),
		"o": (25, 2, (20, 0), (), "o", None),
	}
	_prop_map_put_ = {
		"DevMode": ((20, LCID, 4, 0),()),
		"o": ((25, LCID, 4, 0),()),
	}
	def __iter__(self):
		"Return a Python iterator for this object"
		try:
			ob = self._oleobj_.InvokeTypes(-4,LCID,3,(13, 10),())
		except pythoncom.error:
			raise TypeError("This object does not support enumeration")
		return win32com.client.util.Iterator(ob, None)

class ICiTools(DispatchBaseClass):
	'ICiTools Interface'
	CLSID = IID('{316BC128-8995-471D-985D-B3E68E87C084}')
	coclass_clsid = IID('{286F56E6-7A78-4541-9D66-92DD901C7DE1}')

	def AndImage(self, ImgSrc=defaultNamedNotOptArg, left=0, top=0):
		'Logical AND with another image'
		return self._oleobj_.InvokeTypes(58, LCID, 1, (24, 0), ((9, 1), (3, 49), (3, 49)),ImgSrc
			, left, top)

	def CountPixels(self):
		'Count image pixels'
		return self._oleobj_.InvokeTypes(23, LCID, 1, (3, 0), (),)

	# Result is of type ICiImage
	def ExtractObject(self, Object=defaultNamedNotOptArg):
		'Extract an object into new image'
		ret = self._oleobj_.InvokeTypes(6, LCID, 1, (9, 0), ((9, 1),),Object
			)
		if ret is not None:
			ret = Dispatch(ret, u'ExtractObject', '{F2BCF189-0B27-11D4-B5F5-9CC767000000}')
		return ret

	def Fatten(self, Pixels=defaultNamedNotOptArg, Direction=defaultNamedNotOptArg):
		'Fatten image'
		return self._oleobj_.InvokeTypes(54, LCID, 1, (24, 0), ((3, 1), (3, 1)),Pixels
			, Direction)

	# Result is of type ICiLine
	def FirstLine(self):
		'Find first line'
		ret = self._oleobj_.InvokeTypes(12, LCID, 1, (9, 0), (),)
		if ret is not None:
			ret = Dispatch(ret, u'FirstLine', '{B8E5EE38-BB0D-4561-B8D3-26C18C8817EE}')
		return ret

	# Result is of type ICiObject
	def FirstObject(self):
		'Find first object'
		ret = self._oleobj_.InvokeTypes(1, LCID, 1, (9, 0), (),)
		if ret is not None:
			ret = Dispatch(ret, u'FirstObject', '{59A0E32D-5050-47F5-A21B-F00397A21FCC}')
		return ret

	def MeasureContrast(self, nArea=1):
		'Measure contrast'
		return self._oleobj_.InvokeTypes(80, LCID, 1, (5, 0), ((3, 49),),nArea
			)

	def MeasureHorzHistogram(self):
		'Measure horizontal histogram'
		return self._ApplyTypes_(25, 1, (12, 0), (), u'MeasureHorzHistogram', None,)

	# Result is of type ICiRect
	def MeasureMargins(self):
		'Measure image margins'
		ret = self._oleobj_.InvokeTypes(14, LCID, 1, (9, 0), (),)
		if ret is not None:
			ret = Dispatch(ret, u'MeasureMargins', '{4ED88244-0BE1-11D4-B5F6-009FC6000000}')
		return ret

	def MeasureRotation(self):
		'Measure image rotation'
		return self._oleobj_.InvokeTypes(42, LCID, 1, (3, 0), (),)

	def MeasureSkew(self):
		'Measure image skew'
		return self._oleobj_.InvokeTypes(19, LCID, 1, (5, 0), (),)

	def MeasureVertHistogram(self):
		'Measure vertical histogram'
		return self._ApplyTypes_(24, 1, (12, 0), (), u'MeasureVertHistogram', None,)

	# Result is of type ICiLine
	def NextLine(self):
		'Find another line'
		ret = self._oleobj_.InvokeTypes(13, LCID, 1, (9, 0), (),)
		if ret is not None:
			ret = Dispatch(ret, u'NextLine', '{B8E5EE38-BB0D-4561-B8D3-26C18C8817EE}')
		return ret

	# Result is of type ICiObject
	def NextObject(self):
		'Find another object'
		ret = self._oleobj_.InvokeTypes(2, LCID, 1, (9, 0), (),)
		if ret is not None:
			ret = Dispatch(ret, u'NextObject', '{59A0E32D-5050-47F5-A21B-F00397A21FCC}')
		return ret

	def OrImage(self, ImgSrc=defaultNamedNotOptArg, left=0, top=0):
		'Logical OR with another image'
		return self._oleobj_.InvokeTypes(59, LCID, 1, (24, 0), ((9, 1), (3, 49), (3, 49)),ImgSrc
			, left, top)

	def Outline(self):
		'Outline objects on image'
		return self._oleobj_.InvokeTypes(56, LCID, 1, (24, 0), (),)

	def PasteImage(self, ImgSrc=defaultNamedNotOptArg, left=0, top=0):
		'Paste another image'
		return self._oleobj_.InvokeTypes(61, LCID, 1, (24, 0), ((9, 1), (3, 49), (3, 49)),ImgSrc
			, left, top)

	def ScaleImage(self, ScaleX=defaultNamedNotOptArg, ScaleY=defaultNamedNotOptArg):
		'Scale image'
		return self._oleobj_.InvokeTypes(75, LCID, 1, (24, 0), ((5, 1), (5, 1)),ScaleX
			, ScaleY)

	def ScaleToDIB(self, ScaleX=defaultNamedNotOptArg, ScaleY=defaultNamedNotOptArg):
		'Scale image to Windows DIB'
		return self._oleobj_.InvokeTypes(79, LCID, 1, (20, 0), ((5, 1), (5, 1)),ScaleX
			, ScaleY)

	# The method Setcx2l is actually a property, but must be used as a method to correctly pass the arguments
	def Setcx2l(self, i=defaultNamedNotOptArg, arg1=defaultUnnamedArg):
		'property cx2l'
		return self._oleobj_.InvokeTypes(63, LCID, 4, (24, 0), ((3, 1), (3, 1)),i
			, arg1)

	# The method Setcx3d is actually a property, but must be used as a method to correctly pass the arguments
	def Setcx3d(self, i=defaultNamedNotOptArg, arg1=defaultUnnamedArg):
		'property cx3d'
		return self._oleobj_.InvokeTypes(62, LCID, 4, (24, 0), ((3, 1), (5, 1)),i
			, arg1)

	def Skeleton(self):
		'Skeleton objects on image'
		return self._oleobj_.InvokeTypes(57, LCID, 1, (24, 0), (),)

	def Skew(self, Angle=defaultNamedNotOptArg):
		'Skew image'
		return self._oleobj_.InvokeTypes(38, LCID, 1, (24, 0), ((5, 1),),Angle
			)

	def Trim(self, Pixels=defaultNamedNotOptArg, Direction=defaultNamedNotOptArg):
		'Trim image'
		return self._oleobj_.InvokeTypes(55, LCID, 1, (24, 0), ((3, 1), (3, 1)),Pixels
			, Direction)

	def XorImage(self, ImgSrc=defaultNamedNotOptArg, left=0, top=0):
		'Logical XOR with another image'
		return self._oleobj_.InvokeTypes(60, LCID, 1, (24, 0), ((9, 1), (3, 49), (3, 49)),ImgSrc
			, left, top)

	# The method cx2l is actually a property, but must be used as a method to correctly pass the arguments
	def cx2l(self, i=defaultNamedNotOptArg):
		'property cx2l'
		return self._oleobj_.InvokeTypes(63, LCID, 2, (3, 0), ((3, 1),),i
			)

	# The method cx3d is actually a property, but must be used as a method to correctly pass the arguments
	def cx3d(self, i=defaultNamedNotOptArg):
		'property cx3d'
		return self._oleobj_.InvokeTypes(62, LCID, 2, (5, 0), ((3, 1),),i
			)

	_prop_map_get_ = {
		# Method 'Image' returns object of type 'ICiImage'
		"Image": (26, 2, (9, 0), (), "Image", '{F2BCF189-0B27-11D4-B5F5-9CC767000000}'),
		"o": (81, 2, (20, 0), (), "o", None),
		"pLineCurvature": (11, 2, (3, 0), (), "pLineCurvature", None),
		"pLineDirection": (41, 2, (3, 0), (), "pLineDirection", None),
		"pMaxLineAngle": (10, 2, (5, 0), (), "pMaxLineAngle", None),
		"pMaxLineGap": (9, 2, (3, 0), (), "pMaxLineGap", None),
		"pMinLineLength": (8, 2, (3, 0), (), "pMinLineLength", None),
		"pScaleBmpBrightness": (77, 2, (3, 0), (), "pScaleBmpBrightness", None),
		"pScaleBmpContrast": (78, 2, (3, 0), (), "pScaleBmpContrast", None),
		"pScaleBmpType": (76, 2, (3, 0), (), "pScaleBmpType", None),
		"pScaleThreshold": (74, 2, (3, 0), (), "pScaleThreshold", None),
		"pScaleType": (73, 2, (3, 0), (), "pScaleType", None),
		"rConfidence": (22, 2, (3, 0), (), "rConfidence", None),
	}
	_prop_map_put_ = {
		"Image": ((26, LCID, 4, 0),()),
		"o": ((81, LCID, 4, 0),()),
		"pLineCurvature": ((11, LCID, 4, 0),()),
		"pLineDirection": ((41, LCID, 4, 0),()),
		"pMaxLineAngle": ((10, LCID, 4, 0),()),
		"pMaxLineGap": ((9, LCID, 4, 0),()),
		"pMinLineLength": ((8, LCID, 4, 0),()),
		"pScaleBmpBrightness": ((77, LCID, 4, 0),()),
		"pScaleBmpContrast": ((78, LCID, 4, 0),()),
		"pScaleBmpType": ((76, LCID, 4, 0),()),
		"pScaleThreshold": ((74, LCID, 4, 0),()),
		"pScaleType": ((73, LCID, 4, 0),()),
	}
	def __iter__(self):
		"Return a Python iterator for this object"
		try:
			ob = self._oleobj_.InvokeTypes(-4,LCID,3,(13, 10),())
		except pythoncom.error:
			raise TypeError("This object does not support enumeration")
		return win32com.client.util.Iterator(ob, None)

class ICiView(DispatchBaseClass):
	'ICiView Interface'
	CLSID = IID('{98AFD5D0-A728-498D-B1DE-0D811D719793}')
	coclass_clsid = IID('{BCE12DAC-09D5-4E64-AC70-9C7994B5832C}')

	_prop_map_get_ = {
		"o": (1, 2, (20, 0), (), "o", None),
	}
	_prop_map_put_ = {
		"o": ((1, LCID, 4, 0),()),
	}
	def __iter__(self):
		"Return a Python iterator for this object"
		try:
			ob = self._oleobj_.InvokeTypes(-4,LCID,3,(13, 10),())
		except pythoncom.error:
			raise TypeError("This object does not support enumeration")
		return win32com.client.util.Iterator(ob, None)

class _ICiImageEvents:
	'_ICiImageEvents Interface'
	CLSID = CLSID_Sink = IID('{F2BCF18B-0B27-11D4-B5F5-9CC767000000}')
	coclass_clsid = IID('{F2BCF18A-0B27-11D4-B5F5-9CC767000000}')
	_public_methods_ = [] # For COM Server support
	_dispid_to_func_ = {
		        1 : "OnLog",
		}

	def __init__(self, oobj = None):
		if oobj is None:
			self._olecp = None
		else:
			import win32com.server.util
			from win32com.server.policy import EventHandlerPolicy
			cpc=oobj._oleobj_.QueryInterface(pythoncom.IID_IConnectionPointContainer)
			cp=cpc.FindConnectionPoint(self.CLSID_Sink)
			cookie=cp.Advise(win32com.server.util.wrap(self, usePolicy=EventHandlerPolicy))
			self._olecp,self._olecp_cookie = cp,cookie
	def __del__(self):
		try:
			self.close()
		except pythoncom.com_error:
			pass
	def close(self):
		if self._olecp is not None:
			cp,cookie,self._olecp,self._olecp_cookie = self._olecp,self._olecp_cookie,None,None
			cp.Unadvise(cookie)
	def _query_interface_(self, iid):
		import win32com.server.util
		if iid==self.CLSID_Sink: return win32com.server.util.wrap(self)

	# Event Handlers
	# If you create handlers, they should have the following prototypes:
#	def OnLog(self, LogSignature=defaultNamedNotOptArg, LogRecord=defaultNamedNotOptArg, RsltRecord=defaultNamedNotOptArg):
#		'Log event'


from win32com.client import CoClassBaseClass
class CiAdvColor(CoClassBaseClass): # A CoClass
	# Color Image processing object
	CLSID = IID('{3022D35D-0127-4C24-B1F0-1C66A831807E}')
	coclass_sources = [
	]
	coclass_interfaces = [
		ICiAdvColor,
	]
	default_interface = ICiAdvColor

class CiBarcode(CoClassBaseClass): # A CoClass
	# Barcode information object
	CLSID = IID('{4ED88241-0BE1-11D4-B5F6-009FC6000000}')
	coclass_sources = [
	]
	coclass_interfaces = [
		ICiBarcode,
	]
	default_interface = ICiBarcode

class CiBarcodeBasic(CoClassBaseClass): # A CoClass
	# 1D barcodes recognition object (Basic)
	CLSID = IID('{12806B0A-7754-4297-AE05-631C2A1E928D}')
	coclass_sources = [
	]
	coclass_interfaces = [
		ICiBarcodeBasic,
	]
	default_interface = ICiBarcodeBasic

class CiBarcodePro(CoClassBaseClass): # A CoClass
	# 1D barcodes recognition object (Pro)
	CLSID = IID('{BDDB0245-0CFD-11D4-B5F8-B89D57000000}')
	coclass_sources = [
	]
	coclass_interfaces = [
		ICiBarcodePro,
	]
	default_interface = ICiBarcodePro

class CiBarcodes(CoClassBaseClass): # A CoClass
	# Barcodes Class
	CLSID = IID('{DAB01618-F817-4662-ADBA-46EE1C94921A}')
	coclass_sources = [
	]
	coclass_interfaces = [
		ICiBarcodes,
	]
	default_interface = ICiBarcodes

class CiDataMatrix(CoClassBaseClass): # A CoClass
	# DataMatrix barcodes recognition object
	CLSID = IID('{90E9D617-A4B1-4DDE-B842-60BECC114254}')
	coclass_sources = [
	]
	coclass_interfaces = [
		ICiDataMatrix,
	]
	default_interface = ICiDataMatrix

class CiImage(CoClassBaseClass): # A CoClass
	# Image object
	CLSID = IID('{F2BCF18A-0B27-11D4-B5F5-9CC767000000}')
	coclass_sources = [
		_ICiImageEvents,
	]
	default_source = _ICiImageEvents
	coclass_interfaces = [
		ICiImage,
	]
	default_interface = ICiImage

class CiLine(CoClassBaseClass): # A CoClass
	# Line information object
	CLSID = IID('{A7A8BF7F-8CB8-49DC-8A76-D0A1A145189C}')
	coclass_sources = [
	]
	coclass_interfaces = [
		ICiLine,
	]
	default_interface = ICiLine

class CiObject(CoClassBaseClass): # A CoClass
	# Object information object
	CLSID = IID('{4BBE294D-3C2A-4698-8B5F-84B1D3A6F621}')
	coclass_sources = [
	]
	coclass_interfaces = [
		ICiObject,
	]
	default_interface = ICiObject

class CiPdf(CoClassBaseClass): # A CoClass
	# Pdf Read/Write configuration Class
	CLSID = IID('{FB2E2C05-DB40-4A6F-8E52-0243621D7734}')
	coclass_sources = [
	]
	coclass_interfaces = [
		ICiPdf,
	]
	default_interface = ICiPdf

class CiPdf417(CoClassBaseClass): # A CoClass
	# PDF417 barcodes recognition object
	CLSID = IID('{90E9D617-A4B1-4DDE-B842-60BECC114253}')
	coclass_sources = [
	]
	coclass_interfaces = [
		ICiPdf417,
	]
	default_interface = ICiPdf417

class CiPoint(CoClassBaseClass): # A CoClass
	# Point-on-image object
	CLSID = IID('{A7E1D34A-24DA-4D97-AF2E-CE7E4481E1E2}')
	coclass_sources = [
	]
	coclass_interfaces = [
		ICiPoint,
	]
	default_interface = ICiPoint

class CiQR(CoClassBaseClass): # A CoClass
	# QR barcodes recognition object
	CLSID = IID('{90E9D617-A4B1-4DDE-B842-60BECC114255}')
	coclass_sources = [
	]
	coclass_interfaces = [
		ICiQR,
	]
	default_interface = ICiQR

class CiRect(CoClassBaseClass): # A CoClass
	# Rectangle on image object
	CLSID = IID('{4ED88245-0BE1-11D4-B5F6-009FC6000000}')
	coclass_sources = [
	]
	coclass_interfaces = [
		ICiRect,
	]
	default_interface = ICiRect

class CiRepair(CoClassBaseClass): # A CoClass
	# Image repair object
	CLSID = IID('{CB149079-A739-4178-A4DA-BACA546C3728}')
	coclass_sources = [
	]
	coclass_interfaces = [
		ICiRepair,
	]
	default_interface = ICiRepair

# This CoClass is known by the name 'ClearImage.ClearImage.1'
class CiServer(CoClassBaseClass): # A CoClass
	# ClearImage COM root object
	CLSID = IID('{D836E300-A317-4C7E-BE61-D650CE242589}')
	coclass_sources = [
	]
	coclass_interfaces = [
		ICiServer,
	]
	default_interface = ICiServer

class CiTools(CoClassBaseClass): # A CoClass
	# Image tools object
	CLSID = IID('{286F56E6-7A78-4541-9D66-92DD901C7DE1}')
	coclass_sources = [
	]
	coclass_interfaces = [
		ICiTools,
	]
	default_interface = ICiTools

class CiView(CoClassBaseClass): # A CoClass
	# Image viewer object
	CLSID = IID('{BCE12DAC-09D5-4E64-AC70-9C7994B5832C}')
	coclass_sources = [
	]
	coclass_interfaces = [
		ICiView,
	]
	default_interface = ICiView

ICiAdvColor_vtables_dispatch_ = 1
ICiAdvColor_vtables_ = [
	(( u'Image' , u'pVal' , ), 1, (1, (), [ (16393, 10, None, "IID('{F2BCF189-0B27-11D4-B5F5-9CC767000000}')") , ], 1 , 2 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( u'Image' , u'pVal' , ), 1, (1, (), [ (9, 1, None, "IID('{F2BCF189-0B27-11D4-B5F5-9CC767000000}')") , ], 1 , 4 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( u'ConvertToBitonal' , u'mode' , u'Par0' , u'par1' , u'par2' , 
			), 2, (2, (), [ (3, 49, '2', None) , (3, 49, '0', None) , (3, 49, '0', None) , (3, 49, '0', None) , ], 1 , 1 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( u'ConvertToGrayscale' , u'mode' , u'Par0' , u'par1' , u'par2' , 
			), 3, (3, (), [ (3, 49, '2', None) , (3, 49, '0', None) , (3, 49, '0', None) , (3, 49, '0', None) , ], 1 , 1 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( u'ScaleToDpi' , u'mode' , u'Par0' , ), 4, (4, (), [ (3, 49, '1', None) , 
			(3, 49, '0', None) , ], 1 , 1 , 4 , 0 , 88 , (3, 0, None, None) , 1088 , )),
	(( u'cx2l' , u'i' , u'pVal' , ), 5, (5, (), [ (3, 1, None, None) , 
			(16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 96 , (3, 0, None, None) , 1088 , )),
	(( u'cx2l' , u'i' , u'pVal' , ), 5, (5, (), [ (3, 1, None, None) , 
			(3, 1, None, None) , ], 1 , 4 , 4 , 0 , 104 , (3, 0, None, None) , 1088 , )),
	(( u'cx3d' , u'i' , u'pVal' , ), 6, (6, (), [ (3, 1, None, None) , 
			(16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 112 , (3, 0, None, None) , 1088 , )),
	(( u'cx3d' , u'i' , u'pVal' , ), 6, (6, (), [ (3, 1, None, None) , 
			(5, 1, None, None) , ], 1 , 4 , 4 , 0 , 120 , (3, 0, None, None) , 1088 , )),
	(( u'o' , u'pVal' , ), 7, (7, (), [ (16404, 10, None, None) , ], 1 , 2 , 4 , 0 , 128 , (3, 0, None, None) , 1088 , )),
	(( u'o' , u'pVal' , ), 7, (7, (), [ (20, 1, None, None) , ], 1 , 4 , 4 , 0 , 136 , (3, 0, None, None) , 1088 , )),
]

ICiBarcode_vtables_dispatch_ = 1
ICiBarcode_vtables_ = [
	(( u'Rect' , u'pVal' , ), 1, (1, (), [ (16393, 10, None, "IID('{4ED88244-0BE1-11D4-B5F6-009FC6000000}')") , ], 1 , 2 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( u'Type' , u'pVal' , ), 2, (2, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( u'Rotation' , u'pVal' , ), 3, (3, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( u'Length' , u'pVal' , ), 4, (4, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( u'Text' , u'pVal' , ), 5, (5, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( u'Data' , u'pVal' , ), 6, (6, (), [ (16396, 10, None, None) , ], 1 , 2 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
	(( u'ErrorFlags' , u'pVal' , ), 8, (8, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 104 , (3, 0, None, None) , 0 , )),
	(( u'Confidence' , u'pVal' , ), 9, (9, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 112 , (3, 0, None, None) , 0 , )),
	(( u'ModuleSize' , u'pVal' , ), 12, (12, (), [ (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 120 , (3, 0, None, None) , 0 , )),
	(( u'IsBinary' , u'pVal' , ), 15, (15, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 128 , (3, 0, None, None) , 0 , )),
	(( u'IsChecksumVerified' , u'pVal' , ), 16, (16, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 136 , (3, 0, None, None) , 0 , )),
	(( u'Quality' , u'pVal' , ), 17, (17, (), [ (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 144 , (3, 0, None, None) , 1088 , )),
	(( u'Type' , u'pVal' , ), 2, (2, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 152 , (3, 0, None, None) , 1024 , )),
	(( u'Rotation' , u'pVal' , ), 3, (3, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 160 , (3, 0, None, None) , 1024 , )),
	(( u'Text' , u'pVal' , ), 5, (5, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 168 , (3, 0, None, None) , 1024 , )),
	(( u'Data' , u'pVal' , ), 6, (6, (), [ (12, 1, None, None) , ], 1 , 4 , 4 , 0 , 176 , (3, 0, None, None) , 1024 , )),
	(( u'ErrorFlags' , u'pVal' , ), 8, (8, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 184 , (3, 0, None, None) , 1024 , )),
	(( u'Confidence' , u'pVal' , ), 9, (9, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 192 , (3, 0, None, None) , 1024 , )),
	(( u'ModuleSize' , u'pVal' , ), 12, (12, (), [ (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 200 , (3, 0, None, None) , 1024 , )),
	(( u'IsBinary' , u'pVal' , ), 15, (15, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 208 , (3, 0, None, None) , 1024 , )),
	(( u'IsChecksumVerified' , u'pVal' , ), 16, (16, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 216 , (3, 0, None, None) , 1024 , )),
	(( u'Quality' , u'pVal' , ), 17, (17, (), [ (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 224 , (3, 0, None, None) , 1088 , )),
	(( u'Info' , u'Type' , u'pVal' , ), 18, (18, (), [ (8, 1, None, None) , 
			(16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 232 , (3, 0, None, None) , 1088 , )),
	(( u'Info' , u'Type' , u'pVal' , ), 18, (18, (), [ (8, 1, None, None) , 
			(8, 1, None, None) , ], 1 , 4 , 4 , 0 , 240 , (3, 0, None, None) , 1088 , )),
	(( u'Skew' , u'pVal' , ), 19, (19, (), [ (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 248 , (3, 0, None, None) , 1088 , )),
	(( u'Skew' , u'pVal' , ), 19, (19, (), [ (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 256 , (3, 0, None, None) , 1088 , )),
	(( u'Encoding' , u'pVal' , ), 20, (20, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 264 , (3, 0, None, None) , 0 , )),
	(( u'Encoding' , u'pVal' , ), 20, (20, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 272 , (3, 0, None, None) , 1024 , )),
	(( u'o' , u'pVal' , ), 21, (21, (), [ (16404, 10, None, None) , ], 1 , 2 , 4 , 0 , 280 , (3, 0, None, None) , 1088 , )),
	(( u'o' , u'pVal' , ), 21, (21, (), [ (20, 1, None, None) , ], 1 , 4 , 4 , 0 , 288 , (3, 0, None, None) , 1088 , )),
]

ICiBarcodeBasic_vtables_dispatch_ = 1
ICiBarcodeBasic_vtables_ = [
	(( u'FirstBarcode' , u'pVal' , ), 2, (2, (), [ (16393, 10, None, "IID('{4ED88240-0BE1-11D4-B5F6-009FC6000000}')") , ], 1 , 1 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( u'NextBarcode' , u'pVal' , ), 3, (3, (), [ (16393, 10, None, "IID('{4ED88240-0BE1-11D4-B5F6-009FC6000000}')") , ], 1 , 1 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( u'Image' , u'pVal' , ), 5, (5, (), [ (16393, 10, None, "IID('{F2BCF189-0B27-11D4-B5F5-9CC767000000}')") , ], 1 , 2 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( u'Image' , u'pVal' , ), 5, (5, (), [ (9, 1, None, "IID('{F2BCF189-0B27-11D4-B5F5-9CC767000000}')") , ], 1 , 4 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( u'Type' , u'pVal' , ), 7, (7, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( u'Type' , u'pVal' , ), 7, (7, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
	(( u'AutoDetect1D' , u'pVal' , ), 8, (8, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 104 , (3, 0, None, None) , 0 , )),
	(( u'AutoDetect1D' , u'pVal' , ), 8, (8, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 112 , (3, 0, None, None) , 0 , )),
	(( u'ValidateOptChecksum' , u'pVal' , ), 9, (9, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 120 , (3, 0, None, None) , 0 , )),
	(( u'ValidateOptChecksum' , u'pVal' , ), 9, (9, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 128 , (3, 0, None, None) , 0 , )),
	(( u'Barcodes' , u'pVal' , ), 10, (10, (), [ (16393, 10, None, "IID('{41F7F4D4-9FC1-46C6-92E5-2A3457CE3D5E}')") , ], 1 , 2 , 4 , 0 , 136 , (3, 0, None, None) , 0 , )),
	(( u'Find' , u'MaxBarcodes' , u'pVal' , ), 11, (11, (), [ (3, 49, '0', None) , 
			(16387, 10, None, None) , ], 1 , 1 , 4 , 0 , 144 , (3, 0, None, None) , 0 , )),
	(( u'o' , u'pVal' , ), 12, (12, (), [ (16404, 10, None, None) , ], 1 , 2 , 4 , 0 , 152 , (3, 0, None, None) , 1088 , )),
	(( u'o' , u'pVal' , ), 12, (12, (), [ (20, 1, None, None) , ], 1 , 4 , 4 , 0 , 160 , (3, 0, None, None) , 1088 , )),
]

ICiBarcodePro_vtables_dispatch_ = 1
ICiBarcodePro_vtables_ = [
	(( u'Type' , u'pVal' , ), 1, (1, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( u'Type' , u'pVal' , ), 1, (1, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( u'Directions' , u'pVal' , ), 2, (2, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( u'Directions' , u'pVal' , ), 2, (2, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( u'AutoDetect1D' , u'pVal' , ), 10, (10, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( u'AutoDetect1D' , u'pVal' , ), 10, (10, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
	(( u'ValidateOptChecksum' , u'pVal' , ), 11, (11, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 104 , (3, 0, None, None) , 0 , )),
	(( u'ValidateOptChecksum' , u'pVal' , ), 11, (11, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 112 , (3, 0, None, None) , 0 , )),
	(( u'Barcodes' , u'pVal' , ), 12, (12, (), [ (16393, 10, None, "IID('{41F7F4D4-9FC1-46C6-92E5-2A3457CE3D5E}')") , ], 1 , 2 , 4 , 0 , 120 , (3, 0, None, None) , 0 , )),
	(( u'Algorithm' , u'pVal' , ), 4, (4, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 128 , (3, 0, None, None) , 0 , )),
	(( u'Algorithm' , u'pVal' , ), 4, (4, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 136 , (3, 0, None, None) , 0 , )),
	(( u'DiagFlags' , u'pVal' , ), 5, (5, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 144 , (3, 0, None, None) , 0 , )),
	(( u'DiagFlags' , u'pVal' , ), 5, (5, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 152 , (3, 0, None, None) , 0 , )),
	(( u'Image' , u'pVal' , ), 6, (6, (), [ (16393, 10, None, "IID('{F2BCF189-0B27-11D4-B5F5-9CC767000000}')") , ], 1 , 2 , 4 , 0 , 160 , (3, 0, None, None) , 0 , )),
	(( u'Image' , u'pVal' , ), 6, (6, (), [ (9, 1, None, "IID('{F2BCF189-0B27-11D4-B5F5-9CC767000000}')") , ], 1 , 4 , 4 , 0 , 168 , (3, 0, None, None) , 0 , )),
	(( u'FirstBarcode' , u'pVal' , ), 8, (8, (), [ (16393, 10, None, "IID('{4ED88240-0BE1-11D4-B5F6-009FC6000000}')") , ], 1 , 1 , 4 , 0 , 176 , (3, 0, None, None) , 0 , )),
	(( u'NextBarcode' , u'pVal' , ), 9, (9, (), [ (16393, 10, None, "IID('{4ED88240-0BE1-11D4-B5F6-009FC6000000}')") , ], 1 , 1 , 4 , 0 , 184 , (3, 0, None, None) , 0 , )),
	(( u'Find' , u'MaxBarcodes' , u'pVal' , ), 13, (13, (), [ (3, 49, '0', None) , 
			(16387, 10, None, None) , ], 1 , 1 , 4 , 0 , 192 , (3, 0, None, None) , 0 , )),
	(( u'Fx1' , u'par1' , u'par2' , u'ppRet' , ), 14, (14, (), [ 
			(3, 49, '0', None) , (3, 49, '0', None) , (16397, 10, None, None) , ], 1 , 1 , 4 , 0 , 200 , (3, 0, None, None) , 1088 , )),
	(( u'cx2l' , u'i' , u'pVal' , ), 15, (15, (), [ (3, 1, None, None) , 
			(16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 208 , (3, 0, None, None) , 1088 , )),
	(( u'cx2l' , u'i' , u'pVal' , ), 15, (15, (), [ (3, 1, None, None) , 
			(3, 1, None, None) , ], 1 , 4 , 4 , 0 , 216 , (3, 0, None, None) , 1088 , )),
	(( u'Encodings' , u'pVal' , ), 16, (16, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 224 , (3, 0, None, None) , 0 , )),
	(( u'Encodings' , u'pVal' , ), 16, (16, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 232 , (3, 0, None, None) , 0 , )),
	(( u'o' , u'pVal' , ), 17, (17, (), [ (16404, 10, None, None) , ], 1 , 2 , 4 , 0 , 240 , (3, 0, None, None) , 1088 , )),
	(( u'o' , u'pVal' , ), 17, (17, (), [ (20, 1, None, None) , ], 1 , 4 , 4 , 0 , 248 , (3, 0, None, None) , 1088 , )),
]

ICiBarcodes_vtables_dispatch_ = 1
ICiBarcodes_vtables_ = [
	(( u'Add' , u'pVal' , ), 1, (1, (), [ (9, 1, None, "IID('{4ED88240-0BE1-11D4-B5F6-009FC6000000}')") , ], 1 , 1 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( u'Remove' , u'n' , u'ppVal' , ), 2, (2, (), [ (3, 1, None, None) , 
			(16393, 10, None, "IID('{4ED88240-0BE1-11D4-B5F6-009FC6000000}')") , ], 1 , 1 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( u'Count' , u'pnCount' , ), 3, (3, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( u'Item' , u'n' , u'ppItem' , ), 0, (0, (), [ (3, 1, None, None) , 
			(16393, 10, None, "IID('{4ED88240-0BE1-11D4-B5F6-009FC6000000}')") , ], 1 , 2 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( u'_NewEnum' , u'ppEnum' , ), -4, (-4, (), [ (16397, 10, None, None) , ], 1 , 2 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( u'o' , u'pVal' , ), 4, (4, (), [ (16404, 10, None, None) , ], 1 , 2 , 4 , 0 , 96 , (3, 0, None, None) , 1088 , )),
	(( u'o' , u'pVal' , ), 4, (4, (), [ (20, 1, None, None) , ], 1 , 4 , 4 , 0 , 104 , (3, 0, None, None) , 1088 , )),
	(( u'AddLocal' , u'pVal' , ), 5, (5, (), [ (9, 1, None, "IID('{4ED88240-0BE1-11D4-B5F6-009FC6000000}')") , ], 1 , 1 , 4 , 0 , 112 , (3, 0, None, None) , 1088 , )),
]

ICiDataMatrix_vtables_dispatch_ = 1
ICiDataMatrix_vtables_ = [
	(( u'FirstBarcode' , u'pVal' , ), 2, (2, (), [ (16393, 10, None, "IID('{4ED88240-0BE1-11D4-B5F6-009FC6000000}')") , ], 1 , 1 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( u'NextBarcode' , u'pVal' , ), 3, (3, (), [ (16393, 10, None, "IID('{4ED88240-0BE1-11D4-B5F6-009FC6000000}')") , ], 1 , 1 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( u'Image' , u'pVal' , ), 5, (5, (), [ (16393, 10, None, "IID('{F2BCF189-0B27-11D4-B5F5-9CC767000000}')") , ], 1 , 2 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( u'Image' , u'pVal' , ), 5, (5, (), [ (9, 1, None, "IID('{F2BCF189-0B27-11D4-B5F5-9CC767000000}')") , ], 1 , 4 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( u'Algorithm' , u'pVal' , ), 4, (4, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( u'Algorithm' , u'pVal' , ), 4, (4, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
	(( u'DiagFlags' , u'pVal' , ), 7, (7, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 104 , (3, 0, None, None) , 0 , )),
	(( u'DiagFlags' , u'pVal' , ), 7, (7, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 112 , (3, 0, None, None) , 0 , )),
	(( u'Barcodes' , u'pVal' , ), 9, (9, (), [ (16393, 10, None, "IID('{41F7F4D4-9FC1-46C6-92E5-2A3457CE3D5E}')") , ], 1 , 2 , 4 , 0 , 120 , (3, 0, None, None) , 0 , )),
	(( u'Directions' , u'pVal' , ), 8, (8, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 128 , (3, 0, None, None) , 0 , )),
	(( u'Directions' , u'pVal' , ), 8, (8, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 136 , (3, 0, None, None) , 0 , )),
	(( u'Find' , u'MaxBarcodes' , u'pVal' , ), 10, (10, (), [ (3, 49, '0', None) , 
			(16387, 10, None, None) , ], 1 , 1 , 4 , 0 , 144 , (3, 0, None, None) , 0 , )),
	(( u'Fx1' , u'par1' , u'par2' , u'ppRet' , ), 11, (11, (), [ 
			(3, 49, '0', None) , (3, 49, '0', None) , (16397, 10, None, None) , ], 1 , 1 , 4 , 0 , 152 , (3, 0, None, None) , 1088 , )),
	(( u'cx2l' , u'i' , u'pVal' , ), 12, (12, (), [ (3, 1, None, None) , 
			(16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 160 , (3, 0, None, None) , 1088 , )),
	(( u'cx2l' , u'i' , u'pVal' , ), 12, (12, (), [ (3, 1, None, None) , 
			(3, 1, None, None) , ], 1 , 4 , 4 , 0 , 168 , (3, 0, None, None) , 1088 , )),
	(( u'Encodings' , u'pVal' , ), 13, (13, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 176 , (3, 0, None, None) , 0 , )),
	(( u'Encodings' , u'pVal' , ), 13, (13, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 184 , (3, 0, None, None) , 0 , )),
	(( u'o' , u'pVal' , ), 14, (14, (), [ (16404, 10, None, None) , ], 1 , 2 , 4 , 0 , 192 , (3, 0, None, None) , 1088 , )),
	(( u'o' , u'pVal' , ), 14, (14, (), [ (20, 1, None, None) , ], 1 , 4 , 4 , 0 , 200 , (3, 0, None, None) , 1088 , )),
]

ICiImage_vtables_dispatch_ = 1
ICiImage_vtables_ = [
	(( u'Create' , u'Width' , u'Height' , ), 1, (1, (), [ (3, 1, None, None) , 
			(3, 1, None, None) , ], 1 , 1 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( u'Close' , ), 2, (2, (), [ ], 1 , 1 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( u'Open' , u'FileName' , u'PageNumber' , ), 3, (3, (), [ (8, 1, None, None) , 
			(3, 49, '1', None) , ], 1 , 1 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( u'Zone' , u'pVal' , ), 4, (4, (), [ (16393, 10, None, "IID('{4ED88244-0BE1-11D4-B5F6-009FC6000000}')") , ], 1 , 2 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( u'SaveAs' , u'FileName' , u'Format' , ), 5, (5, (), [ (8, 1, None, None) , 
			(3, 49, '1', None) , ], 1 , 1 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( u'Invert' , ), 6, (6, (), [ ], 1 , 1 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
	(( u'Clear' , ), 8, (8, (), [ ], 1 , 1 , 4 , 0 , 104 , (3, 0, None, None) , 0 , )),
	(( u'FlipVert' , ), 9, (9, (), [ ], 1 , 1 , 4 , 0 , 112 , (3, 0, None, None) , 0 , )),
	(( u'FlipHorz' , ), 10, (10, (), [ ], 1 , 1 , 4 , 0 , 120 , (3, 0, None, None) , 0 , )),
	(( u'RotateRight' , ), 11, (11, (), [ ], 1 , 1 , 4 , 0 , 128 , (3, 0, None, None) , 0 , )),
	(( u'RotateLeft' , ), 12, (12, (), [ ], 1 , 1 , 4 , 0 , 136 , (3, 0, None, None) , 0 , )),
	(( u'Flip' , ), 13, (13, (), [ ], 1 , 1 , 4 , 0 , 144 , (3, 0, None, None) , 0 , )),
	(( u'Append' , u'FileName' , u'Format' , ), 14, (14, (), [ (8, 1, None, None) , 
			(3, 49, '7', None) , ], 1 , 1 , 4 , 0 , 152 , (3, 0, None, None) , 0 , )),
	(( u'Width' , u'pVal' , ), 16, (16, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 160 , (3, 0, None, None) , 0 , )),
	(( u'Height' , u'pVal' , ), 17, (17, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 168 , (3, 0, None, None) , 0 , )),
	(( u'pScaleType' , u'pVal' , ), 33, (33, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 176 , (3, 0, None, None) , 1089 , )),
	(( u'pScaleType' , u'pVal' , ), 33, (33, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 184 , (3, 0, None, None) , 1089 , )),
	(( u'pScaleThreshold' , u'pVal' , ), 34, (34, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 192 , (3, 0, None, None) , 1089 , )),
	(( u'pScaleThreshold' , u'pVal' , ), 34, (34, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 200 , (3, 0, None, None) , 1089 , )),
	(( u'ScaleImage' , u'ScaleX' , u'ScaleY' , ), 35, (35, (), [ (5, 1, None, None) , 
			(5, 1, None, None) , ], 1 , 1 , 4 , 0 , 208 , (3, 0, None, None) , 1089 , )),
	(( u'HorzDpi' , u'pVal' , ), 18, (18, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 216 , (3, 0, None, None) , 0 , )),
	(( u'HorzDpi' , u'pVal' , ), 18, (18, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 224 , (3, 0, None, None) , 0 , )),
	(( u'VertDpi' , u'pVal' , ), 19, (19, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 232 , (3, 0, None, None) , 0 , )),
	(( u'VertDpi' , u'pVal' , ), 19, (19, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 240 , (3, 0, None, None) , 0 , )),
	(( u'Copy' , u'ImageFrom' , ), 20, (20, (), [ (9, 0, None, "IID('{F2BCF189-0B27-11D4-B5F5-9CC767000000}')") , ], 1 , 1 , 4 , 0 , 248 , (3, 0, None, None) , 0 , )),
	(( u'IsModified' , u'pVal' , ), 21, (21, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 256 , (3, 0, None, None) , 0 , )),
	(( u'FileName' , u'pVal' , ), 22, (22, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 264 , (3, 0, None, None) , 0 , )),
	(( u'PageNumber' , u'pVal' , ), 23, (23, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 272 , (3, 0, None, None) , 0 , )),
	(( u'PageCount' , u'pVal' , ), 24, (24, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 280 , (3, 0, None, None) , 0 , )),
	(( u'Save' , ), 25, (25, (), [ ], 1 , 1 , 4 , 0 , 288 , (3, 0, None, None) , 0 , )),
	(( u'CopyToClipboard' , ), 29, (29, (), [ ], 1 , 1 , 4 , 0 , 296 , (3, 0, None, None) , 0 , )),
	(( u'SaveToBitmap' , u'hBitmap' , ), 30, (30, (), [ (16404, 10, None, None) , ], 1 , 1 , 4 , 0 , 304 , (3, 0, None, None) , 0 , )),
	(( u'SaveToDIB' , u'hDib' , ), 31, (31, (), [ (16404, 10, None, None) , ], 1 , 1 , 4 , 0 , 312 , (3, 0, None, None) , 0 , )),
	(( u'SaveToMemory' , u'pData' , ), 32, (32, (), [ (16396, 10, None, None) , ], 1 , 1 , 4 , 0 , 320 , (3, 0, None, None) , 0 , )),
	(( u'OpenFromClipboard' , ), 26, (26, (), [ ], 1 , 1 , 4 , 0 , 328 , (3, 0, None, None) , 0 , )),
	(( u'OpenFromBitmap' , u'hBitmap' , ), 27, (27, (), [ (20, 1, None, None) , ], 1 , 1 , 4 , 0 , 336 , (3, 0, None, None) , 0 , )),
	(( u'LoadFromMemory' , u'pData' , ), 28, (28, (), [ (12, 1, None, None) , ], 1 , 1 , 4 , 0 , 344 , (3, 0, None, None) , 0 , )),
	(( u'pScaleBmpBrightness' , u'pVal' , ), 37, (37, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 352 , (3, 0, None, None) , 1089 , )),
	(( u'pScaleBmpBrightness' , u'pVal' , ), 37, (37, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 360 , (3, 0, None, None) , 1089 , )),
	(( u'pScaleBmpContrast' , u'pVal' , ), 38, (38, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 368 , (3, 0, None, None) , 1089 , )),
	(( u'pScaleBmpContrast' , u'pVal' , ), 38, (38, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 376 , (3, 0, None, None) , 1089 , )),
	(( u'pScaleBmpType' , u'pVal' , ), 36, (36, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 384 , (3, 0, None, None) , 1088 , )),
	(( u'pScaleBmpType' , u'pVal' , ), 36, (36, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 392 , (3, 0, None, None) , 1088 , )),
	(( u'ScaleToDIB' , u'ScaleX' , u'ScaleY' , u'hBitmap' , ), 40, (40, (), [ 
			(5, 1, None, None) , (5, 1, None, None) , (16404, 10, None, None) , ], 1 , 1 , 4 , 0 , 400 , (3, 0, None, None) , 1088 , )),
	(( u'Format' , u'pVal' , ), 41, (41, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 408 , (3, 0, None, None) , 0 , )),
	(( u'Handle' , u'pVal' , ), 42, (42, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 416 , (3, 0, None, None) , 1088 , )),
	(( u'CreateZoneRect' , u'Rect' , u'ppInt' , ), 43, (43, (), [ (9, 1, None, "IID('{4ED88244-0BE1-11D4-B5F6-009FC6000000}')") , 
			(16393, 10, None, "IID('{F2BCF189-0B27-11D4-B5F5-9CC767000000}')") , ], 1 , 1 , 4 , 0 , 424 , (3, 0, None, None) , 0 , )),
	(( u'CreateZone' , u'left' , u'top' , u'right' , u'bottom' , 
			u'ppInt' , ), 45, (45, (), [ (3, 49, '0', None) , (3, 49, '0', None) , (3, 49, '0', None) , 
			(3, 49, '0', None) , (16393, 10, None, "IID('{F2BCF189-0B27-11D4-B5F5-9CC767000000}')") , ], 1 , 1 , 4 , 0 , 432 , (3, 0, None, None) , 0 , )),
	(( u'IsZone' , u'pVal' , ), 44, (44, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 440 , (3, 0, None, None) , 0 , )),
	(( u'Parent' , u'pVal' , ), 46, (46, (), [ (16393, 10, None, "IID('{F2BCF189-0B27-11D4-B5F5-9CC767000000}')") , ], 1 , 2 , 4 , 0 , 448 , (3, 0, None, None) , 0 , )),
	(( u'Duplicate' , u'ppInt' , ), 47, (47, (), [ (16393, 10, None, "IID('{F2BCF189-0B27-11D4-B5F5-9CC767000000}')") , ], 1 , 1 , 4 , 0 , 456 , (3, 0, None, None) , 0 , )),
	(( u'LogFlags' , u'LogType' , u'pVal' , ), 49, (49, (), [ (3, 1, None, None) , 
			(16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 464 , (3, 0, None, None) , 1088 , )),
	(( u'LogFlags' , u'LogType' , u'pVal' , ), 49, (49, (), [ (3, 1, None, None) , 
			(3, 1, None, None) , ], 1 , 4 , 4 , 0 , 472 , (3, 0, None, None) , 1088 , )),
	(( u'LogSignature' , u'pVal' , ), 50, (50, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 480 , (3, 0, None, None) , 1088 , )),
	(( u'LogSignature' , u'pVal' , ), 50, (50, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 488 , (3, 0, None, None) , 1088 , )),
	(( u'Crop' , u'left' , u'top' , u'right' , u'bottom' , 
			), 51, (51, (), [ (3, 1, None, None) , (3, 1, None, None) , (3, 1, None, None) , (3, 1, None, None) , ], 1 , 1 , 4 , 0 , 496 , (3, 0, None, None) , 0 , )),
	(( u'LineBytes' , u'pVal' , ), 52, (52, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 504 , (3, 0, None, None) , 0 , )),
	(( u'BitsPerPixel' , u'pVal' , ), 53, (53, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 512 , (3, 0, None, None) , 0 , )),
	(( u'CreateBpp' , u'Width' , u'Height' , u'BitsPerPixel' , ), 54, (54, (), [ 
			(3, 1, None, None) , (3, 1, None, None) , (3, 1, None, None) , ], 1 , 1 , 4 , 0 , 520 , (3, 0, None, None) , 0 , )),
	(( u'Buffer' , u'pVal' , ), 55, (55, (), [ (16404, 10, None, None) , ], 1 , 2 , 4 , 0 , 528 , (3, 0, None, None) , 1088 , )),
	(( u'IsBitonal' , u'pVal' , ), 57, (57, (), [ (16387, 10, None, None) , ], 1 , 1 , 4 , 0 , 536 , (3, 0, None, None) , 1088 , )),
	(( u'CiCx' , u'pVal' , ), 58, (58, (), [ (16393, 10, None, None) , ], 1 , 2 , 4 , 0 , 544 , (3, 0, None, None) , 1088 , )),
	(( u'FileSize' , u'pVal' , ), 59, (59, (), [ (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 552 , (3, 0, None, None) , 1088 , )),
	(( u'JpegQuality' , u'pVal' , ), 60, (60, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 560 , (3, 0, None, None) , 0 , )),
	(( u'JpegQuality' , u'pVal' , ), 60, (60, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 568 , (3, 0, None, None) , 0 , )),
	(( u'IsValid' , u'pVal' , ), 61, (61, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 576 , (3, 0, None, None) , 0 , )),
	(( u'cx2l' , u'i' , u'pVal' , ), 62, (62, (), [ (3, 1, None, None) , 
			(16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 584 , (3, 0, None, None) , 1088 , )),
	(( u'cx2l' , u'i' , u'pVal' , ), 62, (62, (), [ (3, 1, None, None) , 
			(3, 1, None, None) , ], 1 , 4 , 4 , 0 , 592 , (3, 0, None, None) , 1088 , )),
	(( u'Pdf' , u'pVal' , ), 63, (63, (), [ (16393, 10, None, "IID('{70A6F899-6298-447E-951C-07430C0FF812}')") , ], 1 , 2 , 4 , 0 , 600 , (3, 0, None, None) , 0 , )),
	(( u'ToBitonal' , ), 64, (64, (), [ ], 1 , 1 , 4 , 0 , 608 , (3, 0, None, None) , 0 , )),
	(( u'ToGrayscale' , ), 65, (65, (), [ ], 1 , 1 , 4 , 0 , 616 , (3, 0, None, None) , 0 , )),
	(( u'pComprColor' , u'pVal' , ), 66, (66, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 624 , (3, 0, None, None) , 0 , )),
	(( u'pComprColor' , u'pVal' , ), 66, (66, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 632 , (3, 0, None, None) , 0 , )),
	(( u'pComprBitonal' , u'pVal' , ), 67, (67, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 640 , (3, 0, None, None) , 0 , )),
	(( u'pComprBitonal' , u'pVal' , ), 67, (67, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 648 , (3, 0, None, None) , 0 , )),
	(( u'Info' , u'Type' , u'pVal' , ), 68, (68, (), [ (8, 1, None, None) , 
			(16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 656 , (3, 0, None, None) , 1088 , )),
	(( u'Info' , u'Type' , u'pVal' , ), 68, (68, (), [ (8, 1, None, None) , 
			(8, 1, None, None) , ], 1 , 4 , 4 , 0 , 664 , (3, 0, None, None) , 1088 , )),
	(( u'o' , u'pVal' , ), 69, (69, (), [ (16404, 10, None, None) , ], 1 , 2 , 4 , 0 , 672 , (3, 0, None, None) , 1088 , )),
	(( u'o' , u'pVal' , ), 69, (69, (), [ (20, 1, None, None) , ], 1 , 4 , 4 , 0 , 680 , (3, 0, None, None) , 1088 , )),
]

ICiLine_vtables_dispatch_ = 1
ICiLine_vtables_ = [
	(( u'Direction' , u'pVal' , ), 35, (35, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( u'Thickness' , u'pVal' , ), 36, (36, (), [ (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( u'Angle' , u'pVal' , ), 37, (37, (), [ (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( u'Rect' , u'pVal' , ), 38, (38, (), [ (16393, 10, None, "IID('{4ED88244-0BE1-11D4-B5F6-009FC6000000}')") , ], 1 , 2 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( u'Start' , u'pVal' , ), 39, (39, (), [ (16393, 10, None, "IID('{8C531E23-84B0-431E-B39E-849AB24613AF}')") , ], 1 , 2 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( u'End' , u'pVal' , ), 40, (40, (), [ (16393, 10, None, "IID('{8C531E23-84B0-431E-B39E-849AB24613AF}')") , ], 1 , 2 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
	(( u'o' , u'pVal' , ), 41, (41, (), [ (16404, 10, None, None) , ], 1 , 2 , 4 , 0 , 104 , (3, 0, None, None) , 1088 , )),
	(( u'o' , u'pVal' , ), 41, (41, (), [ (20, 1, None, None) , ], 1 , 4 , 4 , 0 , 112 , (3, 0, None, None) , 1088 , )),
]

ICiObject_vtables_dispatch_ = 1
ICiObject_vtables_ = [
	(( u'Pixels' , u'pVal' , ), 3, (3, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( u'Intervals' , u'pVal' , ), 4, (4, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( u'Rect' , u'pVal' , ), 5, (5, (), [ (16393, 10, None, "IID('{4ED88244-0BE1-11D4-B5F6-009FC6000000}')") , ], 1 , 2 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( u'cx3d' , u'i' , u'pVal' , ), 6, (6, (), [ (3, 1, None, None) , 
			(16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 80 , (3, 0, None, None) , 1088 , )),
	(( u'cx3d' , u'i' , u'pVal' , ), 6, (6, (), [ (3, 1, None, None) , 
			(5, 1, None, None) , ], 1 , 4 , 4 , 0 , 88 , (3, 0, None, None) , 1088 , )),
	(( u'cx2l' , u'i' , u'pVal' , ), 7, (7, (), [ (3, 1, None, None) , 
			(16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 96 , (3, 0, None, None) , 1088 , )),
	(( u'cx2l' , u'i' , u'pVal' , ), 7, (7, (), [ (3, 1, None, None) , 
			(3, 1, None, None) , ], 1 , 4 , 4 , 0 , 104 , (3, 0, None, None) , 1088 , )),
	(( u'o' , u'pVal' , ), 8, (8, (), [ (16404, 10, None, None) , ], 1 , 2 , 4 , 0 , 112 , (3, 0, None, None) , 1088 , )),
	(( u'o' , u'pVal' , ), 8, (8, (), [ (20, 1, None, None) , ], 1 , 4 , 4 , 0 , 120 , (3, 0, None, None) , 1088 , )),
]

ICiPdf_vtables_dispatch_ = 1
ICiPdf_vtables_ = [
	(( u'readEnabled' , u'pVal' , ), 1, (1, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 56 , (3, 0, None, None) , 1089 , )),
	(( u'writeEnabled' , u'pVal' , ), 2, (2, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 64 , (3, 0, None, None) , 1089 , )),
	(( u'dpiRasterBw' , u'pVal' , ), 3, (3, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( u'dpiRasterBw' , u'pVal' , ), 3, (3, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( u'dpiRasterGs' , u'pVal' , ), 4, (4, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( u'dpiRasterGs' , u'pVal' , ), 4, (4, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
	(( u'dpiRasterRgb' , u'pVal' , ), 5, (5, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 104 , (3, 0, None, None) , 0 , )),
	(( u'dpiRasterRgb' , u'pVal' , ), 5, (5, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 112 , (3, 0, None, None) , 0 , )),
	(( u'readMode' , u'pVal' , ), 6, (6, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 120 , (3, 0, None, None) , 0 , )),
	(( u'readMode' , u'pVal' , ), 6, (6, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 128 , (3, 0, None, None) , 0 , )),
	(( u'rasterColorMode' , u'pVal' , ), 7, (7, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 136 , (3, 0, None, None) , 0 , )),
	(( u'rasterColorMode' , u'pVal' , ), 7, (7, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 144 , (3, 0, None, None) , 0 , )),
	(( u'minImageWidth' , u'pVal' , ), 8, (8, (), [ (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 152 , (3, 0, None, None) , 0 , )),
	(( u'minImageWidth' , u'pVal' , ), 8, (8, (), [ (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 160 , (3, 0, None, None) , 0 , )),
	(( u'minImageHeight' , u'pVal' , ), 9, (9, (), [ (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 168 , (3, 0, None, None) , 0 , )),
	(( u'minImageHeight' , u'pVal' , ), 9, (9, (), [ (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 176 , (3, 0, None, None) , 0 , )),
	(( u'useMinImageColors' , u'pVal' , ), 10, (10, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 184 , (3, 0, None, None) , 0 , )),
	(( u'useMinImageColors' , u'pVal' , ), 10, (10, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 192 , (3, 0, None, None) , 0 , )),
	(( u'Creator' , u'pVal' , ), 11, (11, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 200 , (3, 0, None, None) , 0 , )),
	(( u'Creator' , u'pVal' , ), 11, (11, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 208 , (3, 0, None, None) , 0 , )),
	(( u'CreationDate' , u'pVal' , ), 12, (12, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 216 , (3, 0, None, None) , 0 , )),
	(( u'CreationDate' , u'pVal' , ), 12, (12, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 224 , (3, 0, None, None) , 0 , )),
	(( u'Author' , u'pVal' , ), 13, (13, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 232 , (3, 0, None, None) , 0 , )),
	(( u'Author' , u'pVal' , ), 13, (13, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 240 , (3, 0, None, None) , 0 , )),
	(( u'Producer' , u'pVal' , ), 14, (14, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 248 , (3, 0, None, None) , 0 , )),
	(( u'Producer' , u'pVal' , ), 14, (14, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 256 , (3, 0, None, None) , 0 , )),
	(( u'Title' , u'pVal' , ), 15, (15, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 264 , (3, 0, None, None) , 0 , )),
	(( u'Title' , u'pVal' , ), 15, (15, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 272 , (3, 0, None, None) , 0 , )),
	(( u'Subject' , u'pVal' , ), 16, (16, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 280 , (3, 0, None, None) , 0 , )),
	(( u'Subject' , u'pVal' , ), 16, (16, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 288 , (3, 0, None, None) , 0 , )),
	(( u'Keywords' , u'pVal' , ), 17, (17, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 296 , (3, 0, None, None) , 0 , )),
	(( u'Keywords' , u'pVal' , ), 17, (17, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 304 , (3, 0, None, None) , 0 , )),
	(( u'ModDate' , u'pVal' , ), 18, (18, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 312 , (3, 0, None, None) , 0 , )),
	(( u'ModDate' , u'pVal' , ), 18, (18, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 320 , (3, 0, None, None) , 0 , )),
	(( u'Ptr' , u'pVal' , ), 19, (19, (), [ (16408, 10, None, None) , ], 1 , 2 , 4 , 0 , 328 , (3, 0, None, None) , 1089 , )),
	(( u'PageSize' , u'pVal' , ), 20, (20, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 336 , (3, 0, None, None) , 1089 , )),
	(( u'PageSize' , u'pVal' , ), 20, (20, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 344 , (3, 0, None, None) , 1089 , )),
	(( u'PageOrientation' , u'pVal' , ), 21, (21, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 352 , (3, 0, None, None) , 1089 , )),
	(( u'PageOrientation' , u'pVal' , ), 21, (21, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 360 , (3, 0, None, None) , 1089 , )),
	(( u'ImageAlignment' , u'pVal' , ), 22, (22, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 368 , (3, 0, None, None) , 1089 , )),
	(( u'ImageAlignment' , u'pVal' , ), 22, (22, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 376 , (3, 0, None, None) , 1089 , )),
	(( u'o' , u'pVal' , ), 23, (23, (), [ (16404, 10, None, None) , ], 1 , 2 , 4 , 0 , 384 , (3, 0, None, None) , 1088 , )),
	(( u'o' , u'pVal' , ), 23, (23, (), [ (20, 1, None, None) , ], 1 , 4 , 4 , 0 , 392 , (3, 0, None, None) , 1088 , )),
]

ICiPdf417_vtables_dispatch_ = 1
ICiPdf417_vtables_ = [
	(( u'FirstBarcode' , u'pVal' , ), 2, (2, (), [ (16393, 10, None, "IID('{4ED88240-0BE1-11D4-B5F6-009FC6000000}')") , ], 1 , 1 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( u'NextBarcode' , u'pVal' , ), 3, (3, (), [ (16393, 10, None, "IID('{4ED88240-0BE1-11D4-B5F6-009FC6000000}')") , ], 1 , 1 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( u'Image' , u'pVal' , ), 5, (5, (), [ (16393, 10, None, "IID('{F2BCF189-0B27-11D4-B5F5-9CC767000000}')") , ], 1 , 2 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( u'Image' , u'pVal' , ), 5, (5, (), [ (9, 1, None, "IID('{F2BCF189-0B27-11D4-B5F5-9CC767000000}')") , ], 1 , 4 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( u'Algorithm' , u'pVal' , ), 4, (4, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( u'Algorithm' , u'pVal' , ), 4, (4, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
	(( u'DiagFlags' , u'pVal' , ), 7, (7, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 104 , (3, 0, None, None) , 0 , )),
	(( u'DiagFlags' , u'pVal' , ), 7, (7, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 112 , (3, 0, None, None) , 0 , )),
	(( u'Barcodes' , u'pVal' , ), 9, (9, (), [ (16393, 10, None, "IID('{41F7F4D4-9FC1-46C6-92E5-2A3457CE3D5E}')") , ], 1 , 2 , 4 , 0 , 120 , (3, 0, None, None) , 0 , )),
	(( u'Directions' , u'pVal' , ), 8, (8, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 128 , (3, 0, None, None) , 0 , )),
	(( u'Directions' , u'pVal' , ), 8, (8, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 136 , (3, 0, None, None) , 0 , )),
	(( u'Find' , u'MaxBarcodes' , u'pVal' , ), 10, (10, (), [ (3, 49, '0', None) , 
			(16387, 10, None, None) , ], 1 , 1 , 4 , 0 , 144 , (3, 0, None, None) , 0 , )),
	(( u'Fx1' , u'par1' , u'par2' , u'ppRet' , ), 11, (11, (), [ 
			(3, 49, '0', None) , (3, 49, '0', None) , (16397, 10, None, None) , ], 1 , 1 , 4 , 0 , 152 , (3, 0, None, None) , 1088 , )),
	(( u'cx2l' , u'i' , u'pVal' , ), 12, (12, (), [ (3, 1, None, None) , 
			(16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 160 , (3, 0, None, None) , 1088 , )),
	(( u'cx2l' , u'i' , u'pVal' , ), 12, (12, (), [ (3, 1, None, None) , 
			(3, 1, None, None) , ], 1 , 4 , 4 , 0 , 168 , (3, 0, None, None) , 1088 , )),
	(( u'Encodings' , u'pVal' , ), 13, (13, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 176 , (3, 0, None, None) , 0 , )),
	(( u'Encodings' , u'pVal' , ), 13, (13, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 184 , (3, 0, None, None) , 0 , )),
	(( u'o' , u'pVal' , ), 14, (14, (), [ (16404, 10, None, None) , ], 1 , 2 , 4 , 0 , 192 , (3, 0, None, None) , 1088 , )),
	(( u'o' , u'pVal' , ), 14, (14, (), [ (20, 1, None, None) , ], 1 , 4 , 4 , 0 , 200 , (3, 0, None, None) , 1088 , )),
]

ICiPoint_vtables_dispatch_ = 1
ICiPoint_vtables_ = [
	(( u'x' , u'pVal' , ), 1, (1, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( u'x' , u'pVal' , ), 1, (1, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( u'y' , u'pVal' , ), 2, (2, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( u'y' , u'pVal' , ), 2, (2, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( u'o' , u'pVal' , ), 3, (3, (), [ (16404, 10, None, None) , ], 1 , 2 , 4 , 0 , 88 , (3, 0, None, None) , 1088 , )),
	(( u'o' , u'pVal' , ), 3, (3, (), [ (20, 1, None, None) , ], 1 , 4 , 4 , 0 , 96 , (3, 0, None, None) , 1088 , )),
]

ICiQR_vtables_dispatch_ = 1
ICiQR_vtables_ = [
	(( u'FirstBarcode' , u'pVal' , ), 2, (2, (), [ (16393, 10, None, "IID('{4ED88240-0BE1-11D4-B5F6-009FC6000000}')") , ], 1 , 1 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( u'NextBarcode' , u'pVal' , ), 3, (3, (), [ (16393, 10, None, "IID('{4ED88240-0BE1-11D4-B5F6-009FC6000000}')") , ], 1 , 1 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( u'Image' , u'pVal' , ), 5, (5, (), [ (16393, 10, None, "IID('{F2BCF189-0B27-11D4-B5F5-9CC767000000}')") , ], 1 , 2 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( u'Image' , u'pVal' , ), 5, (5, (), [ (9, 1, None, "IID('{F2BCF189-0B27-11D4-B5F5-9CC767000000}')") , ], 1 , 4 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( u'Algorithm' , u'pVal' , ), 4, (4, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( u'Algorithm' , u'pVal' , ), 4, (4, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
	(( u'DiagFlags' , u'pVal' , ), 7, (7, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 104 , (3, 0, None, None) , 0 , )),
	(( u'DiagFlags' , u'pVal' , ), 7, (7, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 112 , (3, 0, None, None) , 0 , )),
	(( u'Barcodes' , u'pVal' , ), 9, (9, (), [ (16393, 10, None, "IID('{41F7F4D4-9FC1-46C6-92E5-2A3457CE3D5E}')") , ], 1 , 2 , 4 , 0 , 120 , (3, 0, None, None) , 0 , )),
	(( u'Directions' , u'pVal' , ), 8, (8, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 128 , (3, 0, None, None) , 1088 , )),
	(( u'Directions' , u'pVal' , ), 8, (8, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 136 , (3, 0, None, None) , 1088 , )),
	(( u'Find' , u'MaxBarcodes' , u'pVal' , ), 10, (10, (), [ (3, 49, '0', None) , 
			(16387, 10, None, None) , ], 1 , 1 , 4 , 0 , 144 , (3, 0, None, None) , 0 , )),
	(( u'Fx1' , u'par1' , u'par2' , u'ppRet' , ), 11, (11, (), [ 
			(3, 49, '0', None) , (3, 49, '0', None) , (16397, 10, None, None) , ], 1 , 1 , 4 , 0 , 152 , (3, 0, None, None) , 1088 , )),
	(( u'cx2l' , u'i' , u'pVal' , ), 12, (12, (), [ (3, 1, None, None) , 
			(16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 160 , (3, 0, None, None) , 1088 , )),
	(( u'cx2l' , u'i' , u'pVal' , ), 12, (12, (), [ (3, 1, None, None) , 
			(3, 1, None, None) , ], 1 , 4 , 4 , 0 , 168 , (3, 0, None, None) , 1088 , )),
	(( u'Encodings' , u'pVal' , ), 13, (13, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 176 , (3, 0, None, None) , 0 , )),
	(( u'Encodings' , u'pVal' , ), 13, (13, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 184 , (3, 0, None, None) , 0 , )),
	(( u'o' , u'pVal' , ), 14, (14, (), [ (16404, 10, None, None) , ], 1 , 2 , 4 , 0 , 192 , (3, 0, None, None) , 1088 , )),
	(( u'o' , u'pVal' , ), 14, (14, (), [ (20, 1, None, None) , ], 1 , 4 , 4 , 0 , 200 , (3, 0, None, None) , 1088 , )),
]

ICiRect_vtables_dispatch_ = 1
ICiRect_vtables_ = [
	(( u'top' , u'pVal' , ), 1, (1, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( u'top' , u'pVal' , ), 1, (1, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( u'bottom' , u'pVal' , ), 2, (2, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( u'bottom' , u'pVal' , ), 2, (2, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( u'left' , u'pVal' , ), 3, (3, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( u'left' , u'pVal' , ), 3, (3, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
	(( u'right' , u'pVal' , ), 4, (4, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 104 , (3, 0, None, None) , 0 , )),
	(( u'right' , u'pVal' , ), 4, (4, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 112 , (3, 0, None, None) , 0 , )),
	(( u'Empty' , ), 5, (5, (), [ ], 1 , 1 , 4 , 0 , 120 , (3, 0, None, None) , 0 , )),
	(( u'IsEmpty' , u'pVal' , ), 6, (6, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 128 , (3, 0, None, None) , 0 , )),
	(( u'o' , u'pVal' , ), 7, (7, (), [ (16404, 10, None, None) , ], 1 , 2 , 4 , 0 , 136 , (3, 0, None, None) , 1088 , )),
	(( u'o' , u'pVal' , ), 7, (7, (), [ (20, 1, None, None) , ], 1 , 4 , 4 , 0 , 144 , (3, 0, None, None) , 1088 , )),
]

ICiRepair_vtables_dispatch_ = 1
ICiRepair_vtables_ = [
	(( u'FaxStandardToFine' , ), 1, (1, (), [ ], 1 , 1 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( u'FaxRemoveBlankLines' , ), 2, (2, (), [ ], 1 , 1 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( u'FaxRemoveHeader' , ), 3, (3, (), [ ], 1 , 1 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( u'AutoDeskew' , u'pVal' , ), 36, (36, (), [ (16389, 10, None, None) , ], 1 , 1 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( u'AutoRotate' , u'pVal' , ), 37, (37, (), [ (16387, 10, None, None) , ], 1 , 1 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( u'Image' , u'pVal' , ), 39, (39, (), [ (16393, 10, None, "IID('{F2BCF189-0B27-11D4-B5F5-9CC767000000}')") , ], 1 , 2 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
	(( u'Image' , u'pVal' , ), 39, (39, (), [ (9, 1, None, "IID('{F2BCF189-0B27-11D4-B5F5-9CC767000000}')") , ], 1 , 4 , 4 , 0 , 104 , (3, 0, None, None) , 0 , )),
	(( u'pMinLineLength' , u'pVal' , ), 16, (16, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 112 , (3, 0, None, None) , 0 , )),
	(( u'pMinLineLength' , u'pVal' , ), 16, (16, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 120 , (3, 0, None, None) , 0 , )),
	(( u'pMaxLineGap' , u'pVal' , ), 17, (17, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 128 , (3, 0, None, None) , 0 , )),
	(( u'pMaxLineGap' , u'pVal' , ), 17, (17, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 136 , (3, 0, None, None) , 0 , )),
	(( u'pMaxLineAngle' , u'pVal' , ), 18, (18, (), [ (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 144 , (3, 0, None, None) , 0 , )),
	(( u'pMaxLineAngle' , u'pVal' , ), 18, (18, (), [ (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 152 , (3, 0, None, None) , 0 , )),
	(( u'pLineCurvature' , u'pVal' , ), 19, (19, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 160 , (3, 0, None, None) , 0 , )),
	(( u'pLineCurvature' , u'pVal' , ), 19, (19, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 168 , (3, 0, None, None) , 0 , )),
	(( u'CleanBorders' , ), 20, (20, (), [ ], 1 , 1 , 4 , 0 , 176 , (3, 0, None, None) , 1088 , )),
	(( u'RemovePunchHoles' , ), 21, (21, (), [ ], 1 , 1 , 4 , 0 , 184 , (3, 0, None, None) , 0 , )),
	(( u'RemoveHalftone' , ), 22, (22, (), [ ], 1 , 1 , 4 , 0 , 192 , (3, 0, None, None) , 0 , )),
	(( u'SmoothCharacters' , u'Type' , ), 23, (23, (), [ (3, 1, None, None) , ], 1 , 1 , 4 , 0 , 200 , (3, 0, None, None) , 0 , )),
	(( u'CleanNoise' , u'NoiseSize' , ), 24, (24, (), [ (3, 1, None, None) , ], 1 , 1 , 4 , 0 , 208 , (3, 0, None, None) , 0 , )),
	(( u'AutoInvertImage' , u'Threshold' , ), 25, (25, (), [ (3, 1, None, None) , ], 1 , 1 , 4 , 0 , 216 , (3, 0, None, None) , 0 , )),
	(( u'AutoInvertBlocks' , u'MinWidth' , u'MinHeight' , ), 26, (26, (), [ (3, 1, None, None) , 
			(3, 1, None, None) , ], 1 , 1 , 4 , 0 , 224 , (3, 0, None, None) , 1088 , )),
	(( u'ReconstructLines' , u'Direction' , ), 29, (29, (), [ (3, 1, None, None) , ], 1 , 1 , 4 , 0 , 232 , (3, 0, None, None) , 0 , )),
	(( u'AutoCrop' , u'NewLeftMargin' , u'NewTopMargin' , u'NewRightMargin' , u'NewBottomMargin' , 
			), 30, (30, (), [ (3, 1, None, None) , (3, 1, None, None) , (3, 1, None, None) , (3, 1, None, None) , ], 1 , 1 , 4 , 0 , 240 , (3, 0, None, None) , 0 , )),
	(( u'AutoRegister' , u'NewLeftMargin' , u'NewTopMargin' , ), 31, (31, (), [ (3, 1, None, None) , 
			(3, 1, None, None) , ], 1 , 1 , 4 , 0 , 248 , (3, 0, None, None) , 0 , )),
	(( u'DeleteLines' , u'Direction' , u'bRepair' , ), 40, (40, (), [ (3, 1, None, None) , 
			(3, 49, '65535', None) , ], 1 , 1 , 4 , 0 , 256 , (3, 0, None, None) , 0 , )),
	(( u'BorderExtract' , u'Flags' , u'Algorithm' , ), 41, (41, (), [ (3, 49, '3', None) , 
			(3, 49, '2', None) , ], 1 , 1 , 4 , 0 , 264 , (3, 0, None, None) , 0 , )),
	(( u'ClearBackground' , u'ThrLevel' , ), 42, (42, (), [ (5, 49, '30.0', None) , ], 1 , 1 , 4 , 0 , 272 , (3, 0, None, None) , 0 , )),
	(( u'Resize' , u'PageSize' , u'PageOrientation' , u'ImageAlignment' , u'Width' , 
			u'Height' , u'Unit' , ), 43, (43, (), [ (3, 1, None, None) , (3, 49, '0', None) , 
			(3, 49, '0', None) , (5, 49, '8.5', None) , (5, 49, '11.0', None) , (3, 49, '1', None) , ], 1 , 1 , 4 , 0 , 280 , (3, 0, None, None) , 0 , )),
	(( u'IsBlankImage' , u'reserved0' , u'reserved1' , u'reserved2' , u'pVal' , 
			), 44, (44, (), [ (3, 49, '0', None) , (5, 49, '0.0', None) , (5, 49, '0.0', None) , (16387, 10, None, None) , ], 1 , 1 , 4 , 0 , 288 , (3, 0, None, None) , 0 , )),
	(( u'cx2l' , u'i' , u'pVal' , ), 45, (45, (), [ (3, 1, None, None) , 
			(16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 296 , (3, 0, None, None) , 1088 , )),
	(( u'cx2l' , u'i' , u'pVal' , ), 45, (45, (), [ (3, 1, None, None) , 
			(3, 1, None, None) , ], 1 , 4 , 4 , 0 , 304 , (3, 0, None, None) , 1088 , )),
	(( u'cx3d' , u'i' , u'pVal' , ), 46, (46, (), [ (3, 1, None, None) , 
			(16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 312 , (3, 0, None, None) , 1088 , )),
	(( u'cx3d' , u'i' , u'pVal' , ), 46, (46, (), [ (3, 1, None, None) , 
			(5, 1, None, None) , ], 1 , 4 , 4 , 0 , 320 , (3, 0, None, None) , 1088 , )),
	(( u'AdvancedBinarize' , u'targetDpi' , u'reserved1' , u'reserved2' , ), 47, (47, (), [ 
			(3, 49, '0', None) , (5, 49, '0.0', None) , (5, 49, '0.0', None) , ], 1 , 1 , 4 , 0 , 328 , (3, 0, None, None) , 0 , )),
	(( u'MinimizeBitsPerPixel' , u'reserved1' , u'reserved2' , ), 48, (48, (), [ (5, 49, '0.0', None) , 
			(5, 49, '0.0', None) , ], 1 , 1 , 4 , 0 , 336 , (3, 0, None, None) , 1088 , )),
	(( u'CleanNoiseExt' , u'Flags' , u'maxNoiseSizeHorz' , u'maxNoiseSizeVert' , u'minObjectDistance' , 
			u'reserved0' , ), 50, (50, (), [ (3, 1, None, None) , (3, 1, None, None) , (3, 1, None, None) , 
			(3, 1, None, None) , (3, 1, None, None) , ], 1 , 1 , 4 , 0 , 344 , (3, 0, None, None) , 0 , )),
	(( u'o' , u'pVal' , ), 51, (51, (), [ (16404, 10, None, None) , ], 1 , 2 , 4 , 0 , 352 , (3, 0, None, None) , 1088 , )),
	(( u'o' , u'pVal' , ), 51, (51, (), [ (20, 1, None, None) , ], 1 , 4 , 4 , 0 , 360 , (3, 0, None, None) , 1088 , )),
]

ICiServer_vtables_dispatch_ = 1
ICiServer_vtables_ = [
	(( u'CreateImage' , u'ppInt' , ), 1, (1, (), [ (16393, 10, None, "IID('{F2BCF189-0B27-11D4-B5F5-9CC767000000}')") , ], 1 , 1 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( u'CreateBarcodePro' , u'ppInt' , ), 2, (2, (), [ (16393, 10, None, "IID('{BDDB0244-0CFD-11D4-B5F8-B89D57000000}')") , ], 1 , 1 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( u'OpenExt' , u'hModule' , u'MasterId' , u'pParam' , ), 10, (10, (), [ 
			(20, 1, None, None) , (3, 1, None, None) , (20, 1, None, None) , ], 1 , 1 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( u'CreateRect' , u'left' , u'top' , u'right' , u'bottom' , 
			u'ppInt' , ), 11, (11, (), [ (3, 49, '0', None) , (3, 49, '0', None) , (3, 49, '0', None) , 
			(3, 49, '0', None) , (16393, 10, None, "IID('{4ED88244-0BE1-11D4-B5F6-009FC6000000}')") , ], 1 , 1 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( u'VerMajor' , u'pVal' , ), 12, (12, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( u'VerMinor' , u'pVal' , ), 13, (13, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
	(( u'VerRelease' , u'pVal' , ), 14, (14, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 104 , (3, 0, None, None) , 0 , )),
	(( u'CreateRepair' , u'ppInt' , ), 5, (5, (), [ (16393, 10, None, "IID('{63F6480C-997E-4FDE-AD63-A24E5F0FFDC7}')") , ], 1 , 1 , 4 , 0 , 112 , (3, 0, None, None) , 0 , )),
	(( u'CreateTools' , u'ppInt' , ), 6, (6, (), [ (16393, 10, None, "IID('{316BC128-8995-471D-985D-B3E68E87C084}')") , ], 1 , 1 , 4 , 0 , 120 , (3, 0, None, None) , 0 , )),
	(( u'CreateBarcodeBasic' , u'ppInt' , ), 8, (8, (), [ (16393, 10, None, "IID('{21DA65F1-9E63-45E3-B081-F78096F9D6C3}')") , ], 1 , 1 , 4 , 0 , 128 , (3, 0, None, None) , 0 , )),
	(( u'CreatePdf417' , u'ppInt' , ), 9, (9, (), [ (16393, 10, None, "IID('{8B79E556-FAD7-4339-8A8F-2C35D5C42C6E}')") , ], 1 , 1 , 4 , 0 , 136 , (3, 0, None, None) , 0 , )),
	(( u'CreateDataMatrix' , u'ppInt' , ), 15, (15, (), [ (16393, 10, None, "IID('{8B79E556-FAD7-4339-8A8F-2C35D5C42C6F}')") , ], 1 , 1 , 4 , 0 , 144 , (3, 0, None, None) , 0 , )),
	(( u'Info' , u'Type' , u'nParam' , u'pVal' , ), 16, (16, (), [ 
			(3, 1, None, None) , (3, 49, '0', None) , (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 152 , (3, 0, None, None) , 0 , )),
	(( u'CreateAdvColor' , u'ppInt' , ), 17, (17, (), [ (16393, 10, None, "IID('{8CBBAECA-9716-40CA-B8F6-0E9FF213522A}')") , ], 1 , 1 , 4 , 0 , 160 , (3, 0, None, None) , 0 , )),
	(( u'CreateBarcode' , u'ppInt' , ), 18, (18, (), [ (16393, 10, None, "IID('{4ED88240-0BE1-11D4-B5F6-009FC6000000}')") , ], 1 , 1 , 4 , 0 , 168 , (3, 0, None, None) , 1088 , )),
	(( u'CreateBarcodes' , u'ppInt' , ), 19, (19, (), [ (16393, 10, None, "IID('{41F7F4D4-9FC1-46C6-92E5-2A3457CE3D5E}')") , ], 1 , 1 , 4 , 0 , 176 , (3, 0, None, None) , 1088 , )),
	(( u'DevMode' , u'bGlobalDevMode' , u'pVal' , ), 20, (20, (), [ (3, 49, '0', None) , 
			(16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 184 , (3, 0, None, None) , 0 , )),
	(( u'DevMode' , u'bGlobalDevMode' , u'pVal' , ), 20, (20, (), [ (3, 49, '0', None) , 
			(16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 184 , (3, 0, None, None) , 0 , )),
	(( u'DevMode' , u'bGlobalDevMode' , u'pVal' , ), 20, (20, (), [ (3, 49, '0', None) , 
			(3, 1, None, None) , ], 1 , 4 , 4 , 0 , 192 , (3, 0, None, None) , 0 , )),
	(( u'DevMode' , u'bGlobalDevMode' , u'pVal' , ), 20, (20, (), [ (3, 49, '0', None) , 
			(3, 1, None, None) , ], 1 , 4 , 4 , 0 , 192 , (3, 0, None, None) , 0 , )),
	(( u'Var' , u'Name' , u'pVal' , ), 21, (21, (), [ (8, 1, None, None) , 
			(16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 200 , (3, 0, None, None) , 1088 , )),
	(( u'Var' , u'Name' , u'pVal' , ), 21, (21, (), [ (8, 1, None, None) , 
			(8, 1, None, None) , ], 1 , 4 , 4 , 0 , 208 , (3, 0, None, None) , 1088 , )),
	(( u'uncompress' , u'DataIn' , u'Encoding' , u'DataOut' , u'RetCodeLng' , 
			), 22, (22, (), [ (12, 1, None, None) , (16387, 3, None, None) , (16396, 2, None, None) , (16387, 10, None, None) , ], 1 , 1 , 4 , 0 , 216 , (3, 0, None, None) , 1088 , )),
	(( u'CreateQR' , u'ppInt' , ), 23, (23, (), [ (16393, 10, None, "IID('{8B79E556-FAD7-4339-8A8F-2C35D5C42C70}')") , ], 1 , 1 , 4 , 0 , 224 , (3, 0, None, None) , 0 , )),
	(( u'OpenUser' , u'User' , u'key' , u'reserved' , ), 24, (24, (), [ 
			(8, 1, None, None) , (8, 1, None, None) , (8, 1, None, None) , ], 1 , 1 , 4 , 0 , 232 , (3, 0, None, None) , 1088 , )),
	(( u'o' , u'pVal' , ), 25, (25, (), [ (16404, 10, None, None) , ], 1 , 2 , 4 , 0 , 240 , (3, 0, None, None) , 1088 , )),
	(( u'o' , u'pVal' , ), 25, (25, (), [ (20, 1, None, None) , ], 1 , 4 , 4 , 0 , 248 , (3, 0, None, None) , 1088 , )),
]

ICiTools_vtables_dispatch_ = 1
ICiTools_vtables_ = [
	(( u'FirstObject' , u'pVal' , ), 1, (1, (), [ (16393, 10, None, "IID('{59A0E32D-5050-47F5-A21B-F00397A21FCC}')") , ], 1 , 1 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( u'NextObject' , u'pVal' , ), 2, (2, (), [ (16393, 10, None, "IID('{59A0E32D-5050-47F5-A21B-F00397A21FCC}')") , ], 1 , 1 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( u'ExtractObject' , u'Object' , u'ppInt' , ), 6, (6, (), [ (9, 1, None, "IID('{59A0E32D-5050-47F5-A21B-F00397A21FCC}')") , 
			(16393, 10, None, "IID('{F2BCF189-0B27-11D4-B5F5-9CC767000000}')") , ], 1 , 1 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( u'pMinLineLength' , u'pVal' , ), 8, (8, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( u'pMinLineLength' , u'pVal' , ), 8, (8, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( u'pMaxLineGap' , u'pVal' , ), 9, (9, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
	(( u'pMaxLineGap' , u'pVal' , ), 9, (9, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 104 , (3, 0, None, None) , 0 , )),
	(( u'pMaxLineAngle' , u'pVal' , ), 10, (10, (), [ (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 112 , (3, 0, None, None) , 0 , )),
	(( u'pMaxLineAngle' , u'pVal' , ), 10, (10, (), [ (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 120 , (3, 0, None, None) , 0 , )),
	(( u'pLineCurvature' , u'pVal' , ), 11, (11, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 128 , (3, 0, None, None) , 0 , )),
	(( u'pLineCurvature' , u'pVal' , ), 11, (11, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 136 , (3, 0, None, None) , 0 , )),
	(( u'FirstLine' , u'pVal' , ), 12, (12, (), [ (16393, 10, None, "IID('{B8E5EE38-BB0D-4561-B8D3-26C18C8817EE}')") , ], 1 , 1 , 4 , 0 , 144 , (3, 0, None, None) , 0 , )),
	(( u'NextLine' , u'pVal' , ), 13, (13, (), [ (16393, 10, None, "IID('{B8E5EE38-BB0D-4561-B8D3-26C18C8817EE}')") , ], 1 , 1 , 4 , 0 , 152 , (3, 0, None, None) , 0 , )),
	(( u'MeasureMargins' , u'pVal' , ), 14, (14, (), [ (16393, 10, None, "IID('{4ED88244-0BE1-11D4-B5F6-009FC6000000}')") , ], 1 , 1 , 4 , 0 , 160 , (3, 0, None, None) , 0 , )),
	(( u'MeasureSkew' , u'pVal' , ), 19, (19, (), [ (16389, 10, None, None) , ], 1 , 1 , 4 , 0 , 168 , (3, 0, None, None) , 0 , )),
	(( u'MeasureRotation' , u'pVal' , ), 42, (42, (), [ (16387, 10, None, None) , ], 1 , 1 , 4 , 0 , 176 , (3, 0, None, None) , 0 , )),
	(( u'CountPixels' , u'Pixels' , ), 23, (23, (), [ (16387, 10, None, None) , ], 1 , 1 , 4 , 0 , 184 , (3, 0, None, None) , 0 , )),
	(( u'MeasureVertHistogram' , u'pData' , ), 24, (24, (), [ (16396, 10, None, None) , ], 1 , 1 , 4 , 0 , 192 , (3, 0, None, None) , 0 , )),
	(( u'MeasureHorzHistogram' , u'pData' , ), 25, (25, (), [ (16396, 10, None, None) , ], 1 , 1 , 4 , 0 , 200 , (3, 0, None, None) , 0 , )),
	(( u'Image' , u'pVal' , ), 26, (26, (), [ (16393, 10, None, "IID('{F2BCF189-0B27-11D4-B5F5-9CC767000000}')") , ], 1 , 2 , 4 , 0 , 208 , (3, 0, None, None) , 0 , )),
	(( u'Image' , u'pVal' , ), 26, (26, (), [ (9, 1, None, "IID('{F2BCF189-0B27-11D4-B5F5-9CC767000000}')") , ], 1 , 4 , 4 , 0 , 216 , (3, 0, None, None) , 0 , )),
	(( u'rConfidence' , u'pVal' , ), 22, (22, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 224 , (3, 0, None, None) , 0 , )),
	(( u'pLineDirection' , u'pVal' , ), 41, (41, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 232 , (3, 0, None, None) , 0 , )),
	(( u'pLineDirection' , u'pVal' , ), 41, (41, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 240 , (3, 0, None, None) , 0 , )),
	(( u'Skew' , u'Angle' , ), 38, (38, (), [ (5, 1, None, None) , ], 1 , 1 , 4 , 0 , 248 , (3, 0, None, None) , 0 , )),
	(( u'Fatten' , u'Pixels' , u'Direction' , ), 54, (54, (), [ (3, 1, None, None) , 
			(3, 1, None, None) , ], 1 , 1 , 4 , 0 , 256 , (3, 0, None, None) , 0 , )),
	(( u'Trim' , u'Pixels' , u'Direction' , ), 55, (55, (), [ (3, 1, None, None) , 
			(3, 1, None, None) , ], 1 , 1 , 4 , 0 , 264 , (3, 0, None, None) , 0 , )),
	(( u'Outline' , ), 56, (56, (), [ ], 1 , 1 , 4 , 0 , 272 , (3, 0, None, None) , 1088 , )),
	(( u'Skeleton' , ), 57, (57, (), [ ], 1 , 1 , 4 , 0 , 280 , (3, 0, None, None) , 1088 , )),
	(( u'AndImage' , u'ImgSrc' , u'left' , u'top' , ), 58, (58, (), [ 
			(9, 1, None, "IID('{F2BCF189-0B27-11D4-B5F5-9CC767000000}')") , (3, 49, '0', None) , (3, 49, '0', None) , ], 1 , 1 , 4 , 0 , 288 , (3, 0, None, None) , 0 , )),
	(( u'OrImage' , u'ImgSrc' , u'left' , u'top' , ), 59, (59, (), [ 
			(9, 1, None, "IID('{F2BCF189-0B27-11D4-B5F5-9CC767000000}')") , (3, 49, '0', None) , (3, 49, '0', None) , ], 1 , 1 , 4 , 0 , 296 , (3, 0, None, None) , 0 , )),
	(( u'XorImage' , u'ImgSrc' , u'left' , u'top' , ), 60, (60, (), [ 
			(9, 1, None, "IID('{F2BCF189-0B27-11D4-B5F5-9CC767000000}')") , (3, 49, '0', None) , (3, 49, '0', None) , ], 1 , 1 , 4 , 0 , 304 , (3, 0, None, None) , 0 , )),
	(( u'PasteImage' , u'ImgSrc' , u'left' , u'top' , ), 61, (61, (), [ 
			(9, 1, None, "IID('{F2BCF189-0B27-11D4-B5F5-9CC767000000}')") , (3, 49, '0', None) , (3, 49, '0', None) , ], 1 , 1 , 4 , 0 , 312 , (3, 0, None, None) , 0 , )),
	(( u'cx3d' , u'i' , u'pVal' , ), 62, (62, (), [ (3, 1, None, None) , 
			(16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 320 , (3, 0, None, None) , 1088 , )),
	(( u'cx3d' , u'i' , u'pVal' , ), 62, (62, (), [ (3, 1, None, None) , 
			(5, 1, None, None) , ], 1 , 4 , 4 , 0 , 328 , (3, 0, None, None) , 1088 , )),
	(( u'cx2l' , u'i' , u'pVal' , ), 63, (63, (), [ (3, 1, None, None) , 
			(16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 336 , (3, 0, None, None) , 1088 , )),
	(( u'cx2l' , u'i' , u'pVal' , ), 63, (63, (), [ (3, 1, None, None) , 
			(3, 1, None, None) , ], 1 , 4 , 4 , 0 , 344 , (3, 0, None, None) , 1088 , )),
	(( u'pScaleType' , u'pVal' , ), 73, (73, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 352 , (3, 0, None, None) , 0 , )),
	(( u'pScaleType' , u'pVal' , ), 73, (73, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 360 , (3, 0, None, None) , 0 , )),
	(( u'pScaleThreshold' , u'pVal' , ), 74, (74, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 368 , (3, 0, None, None) , 0 , )),
	(( u'pScaleThreshold' , u'pVal' , ), 74, (74, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 376 , (3, 0, None, None) , 0 , )),
	(( u'ScaleImage' , u'ScaleX' , u'ScaleY' , ), 75, (75, (), [ (5, 1, None, None) , 
			(5, 1, None, None) , ], 1 , 1 , 4 , 0 , 384 , (3, 0, None, None) , 0 , )),
	(( u'pScaleBmpBrightness' , u'pVal' , ), 77, (77, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 392 , (3, 0, None, None) , 0 , )),
	(( u'pScaleBmpBrightness' , u'pVal' , ), 77, (77, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 400 , (3, 0, None, None) , 0 , )),
	(( u'pScaleBmpContrast' , u'pVal' , ), 78, (78, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 408 , (3, 0, None, None) , 0 , )),
	(( u'pScaleBmpContrast' , u'pVal' , ), 78, (78, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 416 , (3, 0, None, None) , 0 , )),
	(( u'pScaleBmpType' , u'pVal' , ), 76, (76, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 424 , (3, 0, None, None) , 0 , )),
	(( u'pScaleBmpType' , u'pVal' , ), 76, (76, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 432 , (3, 0, None, None) , 0 , )),
	(( u'ScaleToDIB' , u'ScaleX' , u'ScaleY' , u'hBitmap' , ), 79, (79, (), [ 
			(5, 1, None, None) , (5, 1, None, None) , (16404, 10, None, None) , ], 1 , 1 , 4 , 0 , 440 , (3, 0, None, None) , 0 , )),
	(( u'MeasureContrast' , u'nArea' , u'pVal' , ), 80, (80, (), [ (3, 49, '1', None) , 
			(16389, 10, None, None) , ], 1 , 1 , 4 , 0 , 448 , (3, 0, None, None) , 1088 , )),
	(( u'o' , u'pVal' , ), 81, (81, (), [ (16404, 10, None, None) , ], 1 , 2 , 4 , 0 , 456 , (3, 0, None, None) , 1088 , )),
	(( u'o' , u'pVal' , ), 81, (81, (), [ (20, 1, None, None) , ], 1 , 4 , 4 , 0 , 464 , (3, 0, None, None) , 1088 , )),
]

ICiView_vtables_dispatch_ = 1
ICiView_vtables_ = [
	(( u'o' , u'pVal' , ), 1, (1, (), [ (16404, 10, None, None) , ], 1 , 2 , 4 , 0 , 56 , (3, 0, None, None) , 1088 , )),
	(( u'o' , u'pVal' , ), 1, (1, (), [ (20, 1, None, None) , ], 1 , 4 , 4 , 0 , 64 , (3, 0, None, None) , 1088 , )),
]

RecordMap = {
}

CLSIDToClassMap = {
	'{90E9D617-A4B1-4DDE-B842-60BECC114254}' : CiDataMatrix,
	'{B8E5EE38-BB0D-4561-B8D3-26C18C8817EE}' : ICiLine,
	'{8CBBAECA-9716-40CA-B8F6-0E9FF213522A}' : ICiAdvColor,
	'{286F56E6-7A78-4541-9D66-92DD901C7DE1}' : CiTools,
	'{8B79E556-FAD7-4339-8A8F-2C35D5C42C6F}' : ICiDataMatrix,
	'{8B79E556-FAD7-4339-8A8F-2C35D5C42C70}' : ICiQR,
	'{63F6480C-997E-4FDE-AD63-A24E5F0FFDC7}' : ICiRepair,
	'{A7E1D34A-24DA-4D97-AF2E-CE7E4481E1E2}' : CiPoint,
	'{21DA65F1-9E63-45E3-B081-F78096F9D6C3}' : ICiBarcodeBasic,
	'{4ED88240-0BE1-11D4-B5F6-009FC6000000}' : ICiBarcode,
	'{4ED88241-0BE1-11D4-B5F6-009FC6000000}' : CiBarcode,
	'{4ED88244-0BE1-11D4-B5F6-009FC6000000}' : ICiRect,
	'{4ED88245-0BE1-11D4-B5F6-009FC6000000}' : CiRect,
	'{D836E300-A317-4C7E-BE61-D650CE242589}' : CiServer,
	'{CB149079-A739-4178-A4DA-BACA546C3728}' : CiRepair,
	'{A34FC1A7-C73F-4706-886E-C4A33E37C6E5}' : ICiServer,
	'{FB2E2C05-DB40-4A6F-8E52-0243621D7734}' : CiPdf,
	'{59A0E32D-5050-47F5-A21B-F00397A21FCC}' : ICiObject,
	'{8C531E23-84B0-431E-B39E-849AB24613AF}' : ICiPoint,
	'{90E9D617-A4B1-4DDE-B842-60BECC114255}' : CiQR,
	'{BCE12DAC-09D5-4E64-AC70-9C7994B5832C}' : CiView,
	'{12806B0A-7754-4297-AE05-631C2A1E928D}' : CiBarcodeBasic,
	'{98AFD5D0-A728-498D-B1DE-0D811D719793}' : ICiView,
	'{8B79E556-FAD7-4339-8A8F-2C35D5C42C6E}' : ICiPdf417,
	'{F2BCF189-0B27-11D4-B5F5-9CC767000000}' : ICiImage,
	'{BDDB0244-0CFD-11D4-B5F8-B89D57000000}' : ICiBarcodePro,
	'{BDDB0245-0CFD-11D4-B5F8-B89D57000000}' : CiBarcodePro,
	'{F2BCF18A-0B27-11D4-B5F5-9CC767000000}' : CiImage,
	'{70A6F899-6298-447E-951C-07430C0FF812}' : ICiPdf,
	'{F2BCF18B-0B27-11D4-B5F5-9CC767000000}' : _ICiImageEvents,
	'{3022D35D-0127-4C24-B1F0-1C66A831807E}' : CiAdvColor,
	'{A7A8BF7F-8CB8-49DC-8A76-D0A1A145189C}' : CiLine,
	'{316BC128-8995-471D-985D-B3E68E87C084}' : ICiTools,
	'{90E9D617-A4B1-4DDE-B842-60BECC114253}' : CiPdf417,
	'{DAB01618-F817-4662-ADBA-46EE1C94921A}' : CiBarcodes,
	'{41F7F4D4-9FC1-46C6-92E5-2A3457CE3D5E}' : ICiBarcodes,
	'{4BBE294D-3C2A-4698-8B5F-84B1D3A6F621}' : CiObject,
}
CLSIDToPackageMap = {}
win32com.client.CLSIDToClass.RegisterCLSIDsFromDict( CLSIDToClassMap )
VTablesToPackageMap = {}
VTablesToClassMap = {
	'{4ED88244-0BE1-11D4-B5F6-009FC6000000}' : 'ICiRect',
	'{316BC128-8995-471D-985D-B3E68E87C084}' : 'ICiTools',
	'{8B79E556-FAD7-4339-8A8F-2C35D5C42C6F}' : 'ICiDataMatrix',
	'{59A0E32D-5050-47F5-A21B-F00397A21FCC}' : 'ICiObject',
	'{98AFD5D0-A728-498D-B1DE-0D811D719793}' : 'ICiView',
	'{8B79E556-FAD7-4339-8A8F-2C35D5C42C6E}' : 'ICiPdf417',
	'{A34FC1A7-C73F-4706-886E-C4A33E37C6E5}' : 'ICiServer',
	'{8CBBAECA-9716-40CA-B8F6-0E9FF213522A}' : 'ICiAdvColor',
	'{F2BCF189-0B27-11D4-B5F5-9CC767000000}' : 'ICiImage',
	'{BDDB0244-0CFD-11D4-B5F8-B89D57000000}' : 'ICiBarcodePro',
	'{8B79E556-FAD7-4339-8A8F-2C35D5C42C70}' : 'ICiQR',
	'{70A6F899-6298-447E-951C-07430C0FF812}' : 'ICiPdf',
	'{63F6480C-997E-4FDE-AD63-A24E5F0FFDC7}' : 'ICiRepair',
	'{B8E5EE38-BB0D-4561-B8D3-26C18C8817EE}' : 'ICiLine',
	'{8C531E23-84B0-431E-B39E-849AB24613AF}' : 'ICiPoint',
	'{21DA65F1-9E63-45E3-B081-F78096F9D6C3}' : 'ICiBarcodeBasic',
	'{4ED88240-0BE1-11D4-B5F6-009FC6000000}' : 'ICiBarcode',
	'{41F7F4D4-9FC1-46C6-92E5-2A3457CE3D5E}' : 'ICiBarcodes',
}


NamesToIIDMap = {
	'ICiImage' : '{F2BCF189-0B27-11D4-B5F5-9CC767000000}',
	'ICiQR' : '{8B79E556-FAD7-4339-8A8F-2C35D5C42C70}',
	'ICiBarcodePro' : '{BDDB0244-0CFD-11D4-B5F8-B89D57000000}',
	'ICiLine' : '{B8E5EE38-BB0D-4561-B8D3-26C18C8817EE}',
	'ICiView' : '{98AFD5D0-A728-498D-B1DE-0D811D719793}',
	'ICiTools' : '{316BC128-8995-471D-985D-B3E68E87C084}',
	'ICiPoint' : '{8C531E23-84B0-431E-B39E-849AB24613AF}',
	'ICiServer' : '{A34FC1A7-C73F-4706-886E-C4A33E37C6E5}',
	'ICiPdf' : '{70A6F899-6298-447E-951C-07430C0FF812}',
	'ICiBarcodeBasic' : '{21DA65F1-9E63-45E3-B081-F78096F9D6C3}',
	'_ICiImageEvents' : '{F2BCF18B-0B27-11D4-B5F5-9CC767000000}',
	'ICiRect' : '{4ED88244-0BE1-11D4-B5F6-009FC6000000}',
	'ICiObject' : '{59A0E32D-5050-47F5-A21B-F00397A21FCC}',
	'ICiPdf417' : '{8B79E556-FAD7-4339-8A8F-2C35D5C42C6E}',
	'ICiAdvColor' : '{8CBBAECA-9716-40CA-B8F6-0E9FF213522A}',
	'ICiDataMatrix' : '{8B79E556-FAD7-4339-8A8F-2C35D5C42C6F}',
	'ICiBarcode' : '{4ED88240-0BE1-11D4-B5F6-009FC6000000}',
	'ICiBarcodes' : '{41F7F4D4-9FC1-46C6-92E5-2A3457CE3D5E}',
	'ICiRepair' : '{63F6480C-997E-4FDE-AD63-A24E5F0FFDC7}',
}

win32com.client.constants.__dicts__.append(constants.__dict__)

