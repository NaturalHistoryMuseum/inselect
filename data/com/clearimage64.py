# -*- coding: mbcs -*-
# Created by makepy.py version 0.5.01
# By python version 3.5.2 |Continuum Analytics, Inc.| (default, Jul  5 2016, 11:41:13) [MSC v.1900 64 bit (AMD64)]
# On Fri Dec  9 00:04:35 2016
'ClearImage COM Server'
makepy_version = '0.5.01'
python_version = 0x30502f0

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
	cibDataBarLimited             =38         # from enum EBarcodeType
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
	cibfDataBar                   =134217728  # from enum FBarcodeType
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
			ret = Dispatch(ret, 'FirstBarcode', '{4ED88240-0BE1-11D4-B5F6-009FC6000000}')
		return ret

	# Result is of type ICiBarcode
	def NextBarcode(self):
		'Find another barcode'
		ret = self._oleobj_.InvokeTypes(3, LCID, 1, (9, 0), (),)
		if ret is not None:
			ret = Dispatch(ret, 'NextBarcode', '{4ED88240-0BE1-11D4-B5F6-009FC6000000}')
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
			ret = Dispatch(ret, 'FirstBarcode', '{4ED88240-0BE1-11D4-B5F6-009FC6000000}')
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
			ret = Dispatch(ret, 'Fx1', None)
		return ret

	# Result is of type ICiBarcode
	def NextBarcode(self):
		'Find another barcode'
		ret = self._oleobj_.InvokeTypes(9, LCID, 1, (9, 0), (),)
		if ret is not None:
			ret = Dispatch(ret, 'NextBarcode', '{4ED88240-0BE1-11D4-B5F6-009FC6000000}')
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
			ret = Dispatch(ret, 'Item', '{4ED88240-0BE1-11D4-B5F6-009FC6000000}')
		return ret

	# Result is of type ICiBarcode
	def Remove(self, n=defaultNamedNotOptArg):
		'method Remove'
		ret = self._oleobj_.InvokeTypes(2, LCID, 1, (9, 0), ((3, 1),),n
			)
		if ret is not None:
			ret = Dispatch(ret, 'Remove', '{4ED88240-0BE1-11D4-B5F6-009FC6000000}')
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

	def __str__(self, *args):
		return str(self.__call__(*args))
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
			ret = Dispatch(ret, 'FirstBarcode', '{4ED88240-0BE1-11D4-B5F6-009FC6000000}')
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
			ret = Dispatch(ret, 'Fx1', None)
		return ret

	# Result is of type ICiBarcode
	def NextBarcode(self):
		'Find another barcode'
		ret = self._oleobj_.InvokeTypes(3, LCID, 1, (9, 0), (),)
		if ret is not None:
			ret = Dispatch(ret, 'NextBarcode', '{4ED88240-0BE1-11D4-B5F6-009FC6000000}')
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
			ret = Dispatch(ret, 'CreateZone', '{F2BCF189-0B27-11D4-B5F5-9CC767000000}')
		return ret

	# Result is of type ICiImage
	def CreateZoneRect(self, Rect=defaultNamedNotOptArg):
		'Create new Zone within image'
		ret = self._oleobj_.InvokeTypes(43, LCID, 1, (9, 0), ((9, 1),),Rect
			)
		if ret is not None:
			ret = Dispatch(ret, 'CreateZoneRect', '{F2BCF189-0B27-11D4-B5F5-9CC767000000}')
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
			ret = Dispatch(ret, 'Duplicate', '{F2BCF189-0B27-11D4-B5F5-9CC767000000}')
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
		return self._ApplyTypes_(32, 1, (12, 0), (), 'SaveToMemory', None,)

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
			ret = Dispatch(ret, 'FirstBarcode', '{4ED88240-0BE1-11D4-B5F6-009FC6000000}')
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
			ret = Dispatch(ret, 'Fx1', None)
		return ret

	# Result is of type ICiBarcode
	def NextBarcode(self):
		'Find another barcode'
		ret = self._oleobj_.InvokeTypes(3, LCID, 1, (9, 0), (),)
		if ret is not None:
			ret = Dispatch(ret, 'NextBarcode', '{4ED88240-0BE1-11D4-B5F6-009FC6000000}')
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
			ret = Dispatch(ret, 'FirstBarcode', '{4ED88240-0BE1-11D4-B5F6-009FC6000000}')
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
			ret = Dispatch(ret, 'Fx1', None)
		return ret

	# Result is of type ICiBarcode
	def NextBarcode(self):
		'Find another barcode'
		ret = self._oleobj_.InvokeTypes(3, LCID, 1, (9, 0), (),)
		if ret is not None:
			ret = Dispatch(ret, 'NextBarcode', '{4ED88240-0BE1-11D4-B5F6-009FC6000000}')
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
			ret = Dispatch(ret, 'CreateAdvColor', '{8CBBAECA-9716-40CA-B8F6-0E9FF213522A}')
		return ret

	# Result is of type ICiBarcode
	def CreateBarcode(self):
		ret = self._oleobj_.InvokeTypes(18, LCID, 1, (9, 0), (),)
		if ret is not None:
			ret = Dispatch(ret, 'CreateBarcode', '{4ED88240-0BE1-11D4-B5F6-009FC6000000}')
		return ret

	# Result is of type ICiBarcodeBasic
	def CreateBarcodeBasic(self):
		'Create new CiBarcodeBasic object'
		ret = self._oleobj_.InvokeTypes(8, LCID, 1, (9, 0), (),)
		if ret is not None:
			ret = Dispatch(ret, 'CreateBarcodeBasic', '{21DA65F1-9E63-45E3-B081-F78096F9D6C3}')
		return ret

	# Result is of type ICiBarcodePro
	def CreateBarcodePro(self):
		'Create new CiBarcodePro object'
		ret = self._oleobj_.InvokeTypes(2, LCID, 1, (9, 0), (),)
		if ret is not None:
			ret = Dispatch(ret, 'CreateBarcodePro', '{BDDB0244-0CFD-11D4-B5F8-B89D57000000}')
		return ret

	# Result is of type ICiBarcodes
	def CreateBarcodes(self):
		ret = self._oleobj_.InvokeTypes(19, LCID, 1, (9, 0), (),)
		if ret is not None:
			ret = Dispatch(ret, 'CreateBarcodes', '{41F7F4D4-9FC1-46C6-92E5-2A3457CE3D5E}')
		return ret

	# Result is of type ICiDataMatrix
	def CreateDataMatrix(self):
		'Create new CiDataMatrix object'
		ret = self._oleobj_.InvokeTypes(15, LCID, 1, (9, 0), (),)
		if ret is not None:
			ret = Dispatch(ret, 'CreateDataMatrix', '{8B79E556-FAD7-4339-8A8F-2C35D5C42C6F}')
		return ret

	# Result is of type ICiImage
	def CreateImage(self):
		'Create new CiImage object'
		ret = self._oleobj_.InvokeTypes(1, LCID, 1, (9, 0), (),)
		if ret is not None:
			ret = Dispatch(ret, 'CreateImage', '{F2BCF189-0B27-11D4-B5F5-9CC767000000}')
		return ret

	# Result is of type ICiPdf417
	def CreatePdf417(self):
		'Create new CiPdf417 object'
		ret = self._oleobj_.InvokeTypes(9, LCID, 1, (9, 0), (),)
		if ret is not None:
			ret = Dispatch(ret, 'CreatePdf417', '{8B79E556-FAD7-4339-8A8F-2C35D5C42C6E}')
		return ret

	# Result is of type ICiQR
	def CreateQR(self):
		'Create new CiQR object'
		ret = self._oleobj_.InvokeTypes(23, LCID, 1, (9, 0), (),)
		if ret is not None:
			ret = Dispatch(ret, 'CreateQR', '{8B79E556-FAD7-4339-8A8F-2C35D5C42C70}')
		return ret

	# Result is of type ICiRect
	def CreateRect(self, left=0, top=0, right=0, bottom=0):
		'Create new CiRect object'
		ret = self._oleobj_.InvokeTypes(11, LCID, 1, (9, 0), ((3, 49), (3, 49), (3, 49), (3, 49)),left
			, top, right, bottom)
		if ret is not None:
			ret = Dispatch(ret, 'CreateRect', '{4ED88244-0BE1-11D4-B5F6-009FC6000000}')
		return ret

	# Result is of type ICiRepair
	def CreateRepair(self):
		'Create new CiRepair object'
		ret = self._oleobj_.InvokeTypes(5, LCID, 1, (9, 0), (),)
		if ret is not None:
			ret = Dispatch(ret, 'CreateRepair', '{63F6480C-997E-4FDE-AD63-A24E5F0FFDC7}')
		return ret

	# Result is of type ICiTools
	def CreateTools(self):
		'Create new CiTools object'
		ret = self._oleobj_.InvokeTypes(6, LCID, 1, (9, 0), (),)
		if ret is not None:
			ret = Dispatch(ret, 'CreateTools', '{316BC128-8995-471D-985D-B3E68E87C084}')
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
		return self._ApplyTypes_(22, 1, (3, 0), ((12, 1), (16387, 3), (16396, 2)), 'uncompress', None,DataIn
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
			ret = Dispatch(ret, 'ExtractObject', '{F2BCF189-0B27-11D4-B5F5-9CC767000000}')
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
			ret = Dispatch(ret, 'FirstLine', '{B8E5EE38-BB0D-4561-B8D3-26C18C8817EE}')
		return ret

	# Result is of type ICiObject
	def FirstObject(self):
		'Find first object'
		ret = self._oleobj_.InvokeTypes(1, LCID, 1, (9, 0), (),)
		if ret is not None:
			ret = Dispatch(ret, 'FirstObject', '{59A0E32D-5050-47F5-A21B-F00397A21FCC}')
		return ret

	def MeasureContrast(self, nArea=1):
		'Measure contrast'
		return self._oleobj_.InvokeTypes(80, LCID, 1, (5, 0), ((3, 49),),nArea
			)

	def MeasureHorzHistogram(self):
		'Measure horizontal histogram'
		return self._ApplyTypes_(25, 1, (12, 0), (), 'MeasureHorzHistogram', None,)

	# Result is of type ICiRect
	def MeasureMargins(self):
		'Measure image margins'
		ret = self._oleobj_.InvokeTypes(14, LCID, 1, (9, 0), (),)
		if ret is not None:
			ret = Dispatch(ret, 'MeasureMargins', '{4ED88244-0BE1-11D4-B5F6-009FC6000000}')
		return ret

	def MeasureRotation(self):
		'Measure image rotation'
		return self._oleobj_.InvokeTypes(42, LCID, 1, (3, 0), (),)

	def MeasureSkew(self):
		'Measure image skew'
		return self._oleobj_.InvokeTypes(19, LCID, 1, (5, 0), (),)

	def MeasureVertHistogram(self):
		'Measure vertical histogram'
		return self._ApplyTypes_(24, 1, (12, 0), (), 'MeasureVertHistogram', None,)

	# Result is of type ICiLine
	def NextLine(self):
		'Find another line'
		ret = self._oleobj_.InvokeTypes(13, LCID, 1, (9, 0), (),)
		if ret is not None:
			ret = Dispatch(ret, 'NextLine', '{B8E5EE38-BB0D-4561-B8D3-26C18C8817EE}')
		return ret

	# Result is of type ICiObject
	def NextObject(self):
		'Find another object'
		ret = self._oleobj_.InvokeTypes(2, LCID, 1, (9, 0), (),)
		if ret is not None:
			ret = Dispatch(ret, 'NextObject', '{59A0E32D-5050-47F5-A21B-F00397A21FCC}')
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
	(( 'Image' , 'pVal' , ), 1, (1, (), [ (16393, 10, None, "IID('{F2BCF189-0B27-11D4-B5F5-9CC767000000}')") , ], 1 , 2 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'Image' , 'pVal' , ), 1, (1, (), [ (9, 1, None, "IID('{F2BCF189-0B27-11D4-B5F5-9CC767000000}')") , ], 1 , 4 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( 'ConvertToBitonal' , 'mode' , 'Par0' , 'par1' , 'par2' , 
			 ), 2, (2, (), [ (3, 49, '2', None) , (3, 49, '0', None) , (3, 49, '0', None) , (3, 49, '0', None) , ], 1 , 1 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( 'ConvertToGrayscale' , 'mode' , 'Par0' , 'par1' , 'par2' , 
			 ), 3, (3, (), [ (3, 49, '2', None) , (3, 49, '0', None) , (3, 49, '0', None) , (3, 49, '0', None) , ], 1 , 1 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( 'ScaleToDpi' , 'mode' , 'Par0' , ), 4, (4, (), [ (3, 49, '1', None) , 
			 (3, 49, '0', None) , ], 1 , 1 , 4 , 0 , 88 , (3, 0, None, None) , 1088 , )),
	(( 'cx2l' , 'i' , 'pVal' , ), 5, (5, (), [ (3, 1, None, None) , 
			 (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 96 , (3, 0, None, None) , 1088 , )),
	(( 'cx2l' , 'i' , 'pVal' , ), 5, (5, (), [ (3, 1, None, None) , 
			 (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 104 , (3, 0, None, None) , 1088 , )),
	(( 'cx3d' , 'i' , 'pVal' , ), 6, (6, (), [ (3, 1, None, None) , 
			 (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 112 , (3, 0, None, None) , 1088 , )),
	(( 'cx3d' , 'i' , 'pVal' , ), 6, (6, (), [ (3, 1, None, None) , 
			 (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 120 , (3, 0, None, None) , 1088 , )),
	(( 'o' , 'pVal' , ), 7, (7, (), [ (16404, 10, None, None) , ], 1 , 2 , 4 , 0 , 128 , (3, 0, None, None) , 1088 , )),
	(( 'o' , 'pVal' , ), 7, (7, (), [ (20, 1, None, None) , ], 1 , 4 , 4 , 0 , 136 , (3, 0, None, None) , 1088 , )),
]

ICiBarcode_vtables_dispatch_ = 1
ICiBarcode_vtables_ = [
	(( 'Rect' , 'pVal' , ), 1, (1, (), [ (16393, 10, None, "IID('{4ED88244-0BE1-11D4-B5F6-009FC6000000}')") , ], 1 , 2 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'Type' , 'pVal' , ), 2, (2, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( 'Rotation' , 'pVal' , ), 3, (3, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( 'Length' , 'pVal' , ), 4, (4, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( 'Text' , 'pVal' , ), 5, (5, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( 'Data' , 'pVal' , ), 6, (6, (), [ (16396, 10, None, None) , ], 1 , 2 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
	(( 'ErrorFlags' , 'pVal' , ), 8, (8, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 104 , (3, 0, None, None) , 0 , )),
	(( 'Confidence' , 'pVal' , ), 9, (9, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 112 , (3, 0, None, None) , 0 , )),
	(( 'ModuleSize' , 'pVal' , ), 12, (12, (), [ (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 120 , (3, 0, None, None) , 0 , )),
	(( 'IsBinary' , 'pVal' , ), 15, (15, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 128 , (3, 0, None, None) , 0 , )),
	(( 'IsChecksumVerified' , 'pVal' , ), 16, (16, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 136 , (3, 0, None, None) , 0 , )),
	(( 'Quality' , 'pVal' , ), 17, (17, (), [ (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 144 , (3, 0, None, None) , 1088 , )),
	(( 'Type' , 'pVal' , ), 2, (2, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 152 , (3, 0, None, None) , 1024 , )),
	(( 'Rotation' , 'pVal' , ), 3, (3, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 160 , (3, 0, None, None) , 1024 , )),
	(( 'Text' , 'pVal' , ), 5, (5, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 168 , (3, 0, None, None) , 1024 , )),
	(( 'Data' , 'pVal' , ), 6, (6, (), [ (12, 1, None, None) , ], 1 , 4 , 4 , 0 , 176 , (3, 0, None, None) , 1024 , )),
	(( 'ErrorFlags' , 'pVal' , ), 8, (8, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 184 , (3, 0, None, None) , 1024 , )),
	(( 'Confidence' , 'pVal' , ), 9, (9, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 192 , (3, 0, None, None) , 1024 , )),
	(( 'ModuleSize' , 'pVal' , ), 12, (12, (), [ (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 200 , (3, 0, None, None) , 1024 , )),
	(( 'IsBinary' , 'pVal' , ), 15, (15, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 208 , (3, 0, None, None) , 1024 , )),
	(( 'IsChecksumVerified' , 'pVal' , ), 16, (16, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 216 , (3, 0, None, None) , 1024 , )),
	(( 'Quality' , 'pVal' , ), 17, (17, (), [ (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 224 , (3, 0, None, None) , 1088 , )),
	(( 'Info' , 'Type' , 'pVal' , ), 18, (18, (), [ (8, 1, None, None) , 
			 (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 232 , (3, 0, None, None) , 1088 , )),
	(( 'Info' , 'Type' , 'pVal' , ), 18, (18, (), [ (8, 1, None, None) , 
			 (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 240 , (3, 0, None, None) , 1088 , )),
	(( 'Skew' , 'pVal' , ), 19, (19, (), [ (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 248 , (3, 0, None, None) , 1088 , )),
	(( 'Skew' , 'pVal' , ), 19, (19, (), [ (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 256 , (3, 0, None, None) , 1088 , )),
	(( 'Encoding' , 'pVal' , ), 20, (20, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 264 , (3, 0, None, None) , 0 , )),
	(( 'Encoding' , 'pVal' , ), 20, (20, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 272 , (3, 0, None, None) , 1024 , )),
	(( 'o' , 'pVal' , ), 21, (21, (), [ (16404, 10, None, None) , ], 1 , 2 , 4 , 0 , 280 , (3, 0, None, None) , 1088 , )),
	(( 'o' , 'pVal' , ), 21, (21, (), [ (20, 1, None, None) , ], 1 , 4 , 4 , 0 , 288 , (3, 0, None, None) , 1088 , )),
]

ICiBarcodeBasic_vtables_dispatch_ = 1
ICiBarcodeBasic_vtables_ = [
	(( 'FirstBarcode' , 'pVal' , ), 2, (2, (), [ (16393, 10, None, "IID('{4ED88240-0BE1-11D4-B5F6-009FC6000000}')") , ], 1 , 1 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'NextBarcode' , 'pVal' , ), 3, (3, (), [ (16393, 10, None, "IID('{4ED88240-0BE1-11D4-B5F6-009FC6000000}')") , ], 1 , 1 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( 'Image' , 'pVal' , ), 5, (5, (), [ (16393, 10, None, "IID('{F2BCF189-0B27-11D4-B5F5-9CC767000000}')") , ], 1 , 2 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( 'Image' , 'pVal' , ), 5, (5, (), [ (9, 1, None, "IID('{F2BCF189-0B27-11D4-B5F5-9CC767000000}')") , ], 1 , 4 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( 'Type' , 'pVal' , ), 7, (7, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( 'Type' , 'pVal' , ), 7, (7, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
	(( 'AutoDetect1D' , 'pVal' , ), 8, (8, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 104 , (3, 0, None, None) , 0 , )),
	(( 'AutoDetect1D' , 'pVal' , ), 8, (8, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 112 , (3, 0, None, None) , 0 , )),
	(( 'ValidateOptChecksum' , 'pVal' , ), 9, (9, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 120 , (3, 0, None, None) , 0 , )),
	(( 'ValidateOptChecksum' , 'pVal' , ), 9, (9, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 128 , (3, 0, None, None) , 0 , )),
	(( 'Barcodes' , 'pVal' , ), 10, (10, (), [ (16393, 10, None, "IID('{41F7F4D4-9FC1-46C6-92E5-2A3457CE3D5E}')") , ], 1 , 2 , 4 , 0 , 136 , (3, 0, None, None) , 0 , )),
	(( 'Find' , 'MaxBarcodes' , 'pVal' , ), 11, (11, (), [ (3, 49, '0', None) , 
			 (16387, 10, None, None) , ], 1 , 1 , 4 , 0 , 144 , (3, 0, None, None) , 0 , )),
	(( 'o' , 'pVal' , ), 12, (12, (), [ (16404, 10, None, None) , ], 1 , 2 , 4 , 0 , 152 , (3, 0, None, None) , 1088 , )),
	(( 'o' , 'pVal' , ), 12, (12, (), [ (20, 1, None, None) , ], 1 , 4 , 4 , 0 , 160 , (3, 0, None, None) , 1088 , )),
]

ICiBarcodePro_vtables_dispatch_ = 1
ICiBarcodePro_vtables_ = [
	(( 'Type' , 'pVal' , ), 1, (1, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'Type' , 'pVal' , ), 1, (1, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( 'Directions' , 'pVal' , ), 2, (2, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( 'Directions' , 'pVal' , ), 2, (2, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( 'AutoDetect1D' , 'pVal' , ), 10, (10, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( 'AutoDetect1D' , 'pVal' , ), 10, (10, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
	(( 'ValidateOptChecksum' , 'pVal' , ), 11, (11, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 104 , (3, 0, None, None) , 0 , )),
	(( 'ValidateOptChecksum' , 'pVal' , ), 11, (11, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 112 , (3, 0, None, None) , 0 , )),
	(( 'Barcodes' , 'pVal' , ), 12, (12, (), [ (16393, 10, None, "IID('{41F7F4D4-9FC1-46C6-92E5-2A3457CE3D5E}')") , ], 1 , 2 , 4 , 0 , 120 , (3, 0, None, None) , 0 , )),
	(( 'Algorithm' , 'pVal' , ), 4, (4, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 128 , (3, 0, None, None) , 0 , )),
	(( 'Algorithm' , 'pVal' , ), 4, (4, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 136 , (3, 0, None, None) , 0 , )),
	(( 'DiagFlags' , 'pVal' , ), 5, (5, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 144 , (3, 0, None, None) , 0 , )),
	(( 'DiagFlags' , 'pVal' , ), 5, (5, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 152 , (3, 0, None, None) , 0 , )),
	(( 'Image' , 'pVal' , ), 6, (6, (), [ (16393, 10, None, "IID('{F2BCF189-0B27-11D4-B5F5-9CC767000000}')") , ], 1 , 2 , 4 , 0 , 160 , (3, 0, None, None) , 0 , )),
	(( 'Image' , 'pVal' , ), 6, (6, (), [ (9, 1, None, "IID('{F2BCF189-0B27-11D4-B5F5-9CC767000000}')") , ], 1 , 4 , 4 , 0 , 168 , (3, 0, None, None) , 0 , )),
	(( 'FirstBarcode' , 'pVal' , ), 8, (8, (), [ (16393, 10, None, "IID('{4ED88240-0BE1-11D4-B5F6-009FC6000000}')") , ], 1 , 1 , 4 , 0 , 176 , (3, 0, None, None) , 0 , )),
	(( 'NextBarcode' , 'pVal' , ), 9, (9, (), [ (16393, 10, None, "IID('{4ED88240-0BE1-11D4-B5F6-009FC6000000}')") , ], 1 , 1 , 4 , 0 , 184 , (3, 0, None, None) , 0 , )),
	(( 'Find' , 'MaxBarcodes' , 'pVal' , ), 13, (13, (), [ (3, 49, '0', None) , 
			 (16387, 10, None, None) , ], 1 , 1 , 4 , 0 , 192 , (3, 0, None, None) , 0 , )),
	(( 'Fx1' , 'par1' , 'par2' , 'ppRet' , ), 14, (14, (), [ 
			 (3, 49, '0', None) , (3, 49, '0', None) , (16397, 10, None, None) , ], 1 , 1 , 4 , 0 , 200 , (3, 0, None, None) , 1088 , )),
	(( 'cx2l' , 'i' , 'pVal' , ), 15, (15, (), [ (3, 1, None, None) , 
			 (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 208 , (3, 0, None, None) , 1088 , )),
	(( 'cx2l' , 'i' , 'pVal' , ), 15, (15, (), [ (3, 1, None, None) , 
			 (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 216 , (3, 0, None, None) , 1088 , )),
	(( 'Encodings' , 'pVal' , ), 16, (16, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 224 , (3, 0, None, None) , 0 , )),
	(( 'Encodings' , 'pVal' , ), 16, (16, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 232 , (3, 0, None, None) , 0 , )),
	(( 'o' , 'pVal' , ), 17, (17, (), [ (16404, 10, None, None) , ], 1 , 2 , 4 , 0 , 240 , (3, 0, None, None) , 1088 , )),
	(( 'o' , 'pVal' , ), 17, (17, (), [ (20, 1, None, None) , ], 1 , 4 , 4 , 0 , 248 , (3, 0, None, None) , 1088 , )),
]

ICiBarcodes_vtables_dispatch_ = 1
ICiBarcodes_vtables_ = [
	(( 'Add' , 'pVal' , ), 1, (1, (), [ (9, 1, None, "IID('{4ED88240-0BE1-11D4-B5F6-009FC6000000}')") , ], 1 , 1 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'Remove' , 'n' , 'ppVal' , ), 2, (2, (), [ (3, 1, None, None) , 
			 (16393, 10, None, "IID('{4ED88240-0BE1-11D4-B5F6-009FC6000000}')") , ], 1 , 1 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( 'Count' , 'pnCount' , ), 3, (3, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( 'Item' , 'n' , 'ppItem' , ), 0, (0, (), [ (3, 1, None, None) , 
			 (16393, 10, None, "IID('{4ED88240-0BE1-11D4-B5F6-009FC6000000}')") , ], 1 , 2 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( '_NewEnum' , 'ppEnum' , ), -4, (-4, (), [ (16397, 10, None, None) , ], 1 , 2 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( 'o' , 'pVal' , ), 4, (4, (), [ (16404, 10, None, None) , ], 1 , 2 , 4 , 0 , 96 , (3, 0, None, None) , 1088 , )),
	(( 'o' , 'pVal' , ), 4, (4, (), [ (20, 1, None, None) , ], 1 , 4 , 4 , 0 , 104 , (3, 0, None, None) , 1088 , )),
	(( 'AddLocal' , 'pVal' , ), 5, (5, (), [ (9, 1, None, "IID('{4ED88240-0BE1-11D4-B5F6-009FC6000000}')") , ], 1 , 1 , 4 , 0 , 112 , (3, 0, None, None) , 1088 , )),
]

ICiDataMatrix_vtables_dispatch_ = 1
ICiDataMatrix_vtables_ = [
	(( 'FirstBarcode' , 'pVal' , ), 2, (2, (), [ (16393, 10, None, "IID('{4ED88240-0BE1-11D4-B5F6-009FC6000000}')") , ], 1 , 1 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'NextBarcode' , 'pVal' , ), 3, (3, (), [ (16393, 10, None, "IID('{4ED88240-0BE1-11D4-B5F6-009FC6000000}')") , ], 1 , 1 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( 'Image' , 'pVal' , ), 5, (5, (), [ (16393, 10, None, "IID('{F2BCF189-0B27-11D4-B5F5-9CC767000000}')") , ], 1 , 2 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( 'Image' , 'pVal' , ), 5, (5, (), [ (9, 1, None, "IID('{F2BCF189-0B27-11D4-B5F5-9CC767000000}')") , ], 1 , 4 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( 'Algorithm' , 'pVal' , ), 4, (4, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( 'Algorithm' , 'pVal' , ), 4, (4, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
	(( 'DiagFlags' , 'pVal' , ), 7, (7, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 104 , (3, 0, None, None) , 0 , )),
	(( 'DiagFlags' , 'pVal' , ), 7, (7, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 112 , (3, 0, None, None) , 0 , )),
	(( 'Barcodes' , 'pVal' , ), 9, (9, (), [ (16393, 10, None, "IID('{41F7F4D4-9FC1-46C6-92E5-2A3457CE3D5E}')") , ], 1 , 2 , 4 , 0 , 120 , (3, 0, None, None) , 0 , )),
	(( 'Directions' , 'pVal' , ), 8, (8, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 128 , (3, 0, None, None) , 0 , )),
	(( 'Directions' , 'pVal' , ), 8, (8, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 136 , (3, 0, None, None) , 0 , )),
	(( 'Find' , 'MaxBarcodes' , 'pVal' , ), 10, (10, (), [ (3, 49, '0', None) , 
			 (16387, 10, None, None) , ], 1 , 1 , 4 , 0 , 144 , (3, 0, None, None) , 0 , )),
	(( 'Fx1' , 'par1' , 'par2' , 'ppRet' , ), 11, (11, (), [ 
			 (3, 49, '0', None) , (3, 49, '0', None) , (16397, 10, None, None) , ], 1 , 1 , 4 , 0 , 152 , (3, 0, None, None) , 1088 , )),
	(( 'cx2l' , 'i' , 'pVal' , ), 12, (12, (), [ (3, 1, None, None) , 
			 (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 160 , (3, 0, None, None) , 1088 , )),
	(( 'cx2l' , 'i' , 'pVal' , ), 12, (12, (), [ (3, 1, None, None) , 
			 (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 168 , (3, 0, None, None) , 1088 , )),
	(( 'Encodings' , 'pVal' , ), 13, (13, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 176 , (3, 0, None, None) , 0 , )),
	(( 'Encodings' , 'pVal' , ), 13, (13, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 184 , (3, 0, None, None) , 0 , )),
	(( 'o' , 'pVal' , ), 14, (14, (), [ (16404, 10, None, None) , ], 1 , 2 , 4 , 0 , 192 , (3, 0, None, None) , 1088 , )),
	(( 'o' , 'pVal' , ), 14, (14, (), [ (20, 1, None, None) , ], 1 , 4 , 4 , 0 , 200 , (3, 0, None, None) , 1088 , )),
]

ICiImage_vtables_dispatch_ = 1
ICiImage_vtables_ = [
	(( 'Create' , 'Width' , 'Height' , ), 1, (1, (), [ (3, 1, None, None) , 
			 (3, 1, None, None) , ], 1 , 1 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'Close' , ), 2, (2, (), [ ], 1 , 1 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( 'Open' , 'FileName' , 'PageNumber' , ), 3, (3, (), [ (8, 1, None, None) , 
			 (3, 49, '1', None) , ], 1 , 1 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( 'Zone' , 'pVal' , ), 4, (4, (), [ (16393, 10, None, "IID('{4ED88244-0BE1-11D4-B5F6-009FC6000000}')") , ], 1 , 2 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( 'SaveAs' , 'FileName' , 'Format' , ), 5, (5, (), [ (8, 1, None, None) , 
			 (3, 49, '1', None) , ], 1 , 1 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( 'Invert' , ), 6, (6, (), [ ], 1 , 1 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
	(( 'Clear' , ), 8, (8, (), [ ], 1 , 1 , 4 , 0 , 104 , (3, 0, None, None) , 0 , )),
	(( 'FlipVert' , ), 9, (9, (), [ ], 1 , 1 , 4 , 0 , 112 , (3, 0, None, None) , 0 , )),
	(( 'FlipHorz' , ), 10, (10, (), [ ], 1 , 1 , 4 , 0 , 120 , (3, 0, None, None) , 0 , )),
	(( 'RotateRight' , ), 11, (11, (), [ ], 1 , 1 , 4 , 0 , 128 , (3, 0, None, None) , 0 , )),
	(( 'RotateLeft' , ), 12, (12, (), [ ], 1 , 1 , 4 , 0 , 136 , (3, 0, None, None) , 0 , )),
	(( 'Flip' , ), 13, (13, (), [ ], 1 , 1 , 4 , 0 , 144 , (3, 0, None, None) , 0 , )),
	(( 'Append' , 'FileName' , 'Format' , ), 14, (14, (), [ (8, 1, None, None) , 
			 (3, 49, '7', None) , ], 1 , 1 , 4 , 0 , 152 , (3, 0, None, None) , 0 , )),
	(( 'Width' , 'pVal' , ), 16, (16, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 160 , (3, 0, None, None) , 0 , )),
	(( 'Height' , 'pVal' , ), 17, (17, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 168 , (3, 0, None, None) , 0 , )),
	(( 'pScaleType' , 'pVal' , ), 33, (33, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 176 , (3, 0, None, None) , 1089 , )),
	(( 'pScaleType' , 'pVal' , ), 33, (33, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 184 , (3, 0, None, None) , 1089 , )),
	(( 'pScaleThreshold' , 'pVal' , ), 34, (34, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 192 , (3, 0, None, None) , 1089 , )),
	(( 'pScaleThreshold' , 'pVal' , ), 34, (34, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 200 , (3, 0, None, None) , 1089 , )),
	(( 'ScaleImage' , 'ScaleX' , 'ScaleY' , ), 35, (35, (), [ (5, 1, None, None) , 
			 (5, 1, None, None) , ], 1 , 1 , 4 , 0 , 208 , (3, 0, None, None) , 1089 , )),
	(( 'HorzDpi' , 'pVal' , ), 18, (18, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 216 , (3, 0, None, None) , 0 , )),
	(( 'HorzDpi' , 'pVal' , ), 18, (18, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 224 , (3, 0, None, None) , 0 , )),
	(( 'VertDpi' , 'pVal' , ), 19, (19, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 232 , (3, 0, None, None) , 0 , )),
	(( 'VertDpi' , 'pVal' , ), 19, (19, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 240 , (3, 0, None, None) , 0 , )),
	(( 'Copy' , 'ImageFrom' , ), 20, (20, (), [ (9, 0, None, "IID('{F2BCF189-0B27-11D4-B5F5-9CC767000000}')") , ], 1 , 1 , 4 , 0 , 248 , (3, 0, None, None) , 0 , )),
	(( 'IsModified' , 'pVal' , ), 21, (21, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 256 , (3, 0, None, None) , 0 , )),
	(( 'FileName' , 'pVal' , ), 22, (22, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 264 , (3, 0, None, None) , 0 , )),
	(( 'PageNumber' , 'pVal' , ), 23, (23, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 272 , (3, 0, None, None) , 0 , )),
	(( 'PageCount' , 'pVal' , ), 24, (24, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 280 , (3, 0, None, None) , 0 , )),
	(( 'Save' , ), 25, (25, (), [ ], 1 , 1 , 4 , 0 , 288 , (3, 0, None, None) , 0 , )),
	(( 'CopyToClipboard' , ), 29, (29, (), [ ], 1 , 1 , 4 , 0 , 296 , (3, 0, None, None) , 0 , )),
	(( 'SaveToBitmap' , 'hBitmap' , ), 30, (30, (), [ (16404, 10, None, None) , ], 1 , 1 , 4 , 0 , 304 , (3, 0, None, None) , 0 , )),
	(( 'SaveToDIB' , 'hDib' , ), 31, (31, (), [ (16404, 10, None, None) , ], 1 , 1 , 4 , 0 , 312 , (3, 0, None, None) , 0 , )),
	(( 'SaveToMemory' , 'pData' , ), 32, (32, (), [ (16396, 10, None, None) , ], 1 , 1 , 4 , 0 , 320 , (3, 0, None, None) , 0 , )),
	(( 'OpenFromClipboard' , ), 26, (26, (), [ ], 1 , 1 , 4 , 0 , 328 , (3, 0, None, None) , 0 , )),
	(( 'OpenFromBitmap' , 'hBitmap' , ), 27, (27, (), [ (20, 1, None, None) , ], 1 , 1 , 4 , 0 , 336 , (3, 0, None, None) , 0 , )),
	(( 'LoadFromMemory' , 'pData' , ), 28, (28, (), [ (12, 1, None, None) , ], 1 , 1 , 4 , 0 , 344 , (3, 0, None, None) , 0 , )),
	(( 'pScaleBmpBrightness' , 'pVal' , ), 37, (37, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 352 , (3, 0, None, None) , 1089 , )),
	(( 'pScaleBmpBrightness' , 'pVal' , ), 37, (37, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 360 , (3, 0, None, None) , 1089 , )),
	(( 'pScaleBmpContrast' , 'pVal' , ), 38, (38, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 368 , (3, 0, None, None) , 1089 , )),
	(( 'pScaleBmpContrast' , 'pVal' , ), 38, (38, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 376 , (3, 0, None, None) , 1089 , )),
	(( 'pScaleBmpType' , 'pVal' , ), 36, (36, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 384 , (3, 0, None, None) , 1088 , )),
	(( 'pScaleBmpType' , 'pVal' , ), 36, (36, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 392 , (3, 0, None, None) , 1088 , )),
	(( 'ScaleToDIB' , 'ScaleX' , 'ScaleY' , 'hBitmap' , ), 40, (40, (), [ 
			 (5, 1, None, None) , (5, 1, None, None) , (16404, 10, None, None) , ], 1 , 1 , 4 , 0 , 400 , (3, 0, None, None) , 1088 , )),
	(( 'Format' , 'pVal' , ), 41, (41, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 408 , (3, 0, None, None) , 0 , )),
	(( 'Handle' , 'pVal' , ), 42, (42, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 416 , (3, 0, None, None) , 1088 , )),
	(( 'CreateZoneRect' , 'Rect' , 'ppInt' , ), 43, (43, (), [ (9, 1, None, "IID('{4ED88244-0BE1-11D4-B5F6-009FC6000000}')") , 
			 (16393, 10, None, "IID('{F2BCF189-0B27-11D4-B5F5-9CC767000000}')") , ], 1 , 1 , 4 , 0 , 424 , (3, 0, None, None) , 0 , )),
	(( 'CreateZone' , 'left' , 'top' , 'right' , 'bottom' , 
			 'ppInt' , ), 45, (45, (), [ (3, 49, '0', None) , (3, 49, '0', None) , (3, 49, '0', None) , 
			 (3, 49, '0', None) , (16393, 10, None, "IID('{F2BCF189-0B27-11D4-B5F5-9CC767000000}')") , ], 1 , 1 , 4 , 0 , 432 , (3, 0, None, None) , 0 , )),
	(( 'IsZone' , 'pVal' , ), 44, (44, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 440 , (3, 0, None, None) , 0 , )),
	(( 'Parent' , 'pVal' , ), 46, (46, (), [ (16393, 10, None, "IID('{F2BCF189-0B27-11D4-B5F5-9CC767000000}')") , ], 1 , 2 , 4 , 0 , 448 , (3, 0, None, None) , 0 , )),
	(( 'Duplicate' , 'ppInt' , ), 47, (47, (), [ (16393, 10, None, "IID('{F2BCF189-0B27-11D4-B5F5-9CC767000000}')") , ], 1 , 1 , 4 , 0 , 456 , (3, 0, None, None) , 0 , )),
	(( 'LogFlags' , 'LogType' , 'pVal' , ), 49, (49, (), [ (3, 1, None, None) , 
			 (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 464 , (3, 0, None, None) , 1088 , )),
	(( 'LogFlags' , 'LogType' , 'pVal' , ), 49, (49, (), [ (3, 1, None, None) , 
			 (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 472 , (3, 0, None, None) , 1088 , )),
	(( 'LogSignature' , 'pVal' , ), 50, (50, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 480 , (3, 0, None, None) , 1088 , )),
	(( 'LogSignature' , 'pVal' , ), 50, (50, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 488 , (3, 0, None, None) , 1088 , )),
	(( 'Crop' , 'left' , 'top' , 'right' , 'bottom' , 
			 ), 51, (51, (), [ (3, 1, None, None) , (3, 1, None, None) , (3, 1, None, None) , (3, 1, None, None) , ], 1 , 1 , 4 , 0 , 496 , (3, 0, None, None) , 0 , )),
	(( 'LineBytes' , 'pVal' , ), 52, (52, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 504 , (3, 0, None, None) , 0 , )),
	(( 'BitsPerPixel' , 'pVal' , ), 53, (53, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 512 , (3, 0, None, None) , 0 , )),
	(( 'CreateBpp' , 'Width' , 'Height' , 'BitsPerPixel' , ), 54, (54, (), [ 
			 (3, 1, None, None) , (3, 1, None, None) , (3, 1, None, None) , ], 1 , 1 , 4 , 0 , 520 , (3, 0, None, None) , 0 , )),
	(( 'Buffer' , 'pVal' , ), 55, (55, (), [ (16404, 10, None, None) , ], 1 , 2 , 4 , 0 , 528 , (3, 0, None, None) , 1088 , )),
	(( 'IsBitonal' , 'pVal' , ), 57, (57, (), [ (16387, 10, None, None) , ], 1 , 1 , 4 , 0 , 536 , (3, 0, None, None) , 1088 , )),
	(( 'CiCx' , 'pVal' , ), 58, (58, (), [ (16393, 10, None, None) , ], 1 , 2 , 4 , 0 , 544 , (3, 0, None, None) , 1088 , )),
	(( 'FileSize' , 'pVal' , ), 59, (59, (), [ (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 552 , (3, 0, None, None) , 1088 , )),
	(( 'JpegQuality' , 'pVal' , ), 60, (60, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 560 , (3, 0, None, None) , 0 , )),
	(( 'JpegQuality' , 'pVal' , ), 60, (60, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 568 , (3, 0, None, None) , 0 , )),
	(( 'IsValid' , 'pVal' , ), 61, (61, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 576 , (3, 0, None, None) , 0 , )),
	(( 'cx2l' , 'i' , 'pVal' , ), 62, (62, (), [ (3, 1, None, None) , 
			 (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 584 , (3, 0, None, None) , 1088 , )),
	(( 'cx2l' , 'i' , 'pVal' , ), 62, (62, (), [ (3, 1, None, None) , 
			 (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 592 , (3, 0, None, None) , 1088 , )),
	(( 'Pdf' , 'pVal' , ), 63, (63, (), [ (16393, 10, None, "IID('{70A6F899-6298-447E-951C-07430C0FF812}')") , ], 1 , 2 , 4 , 0 , 600 , (3, 0, None, None) , 0 , )),
	(( 'ToBitonal' , ), 64, (64, (), [ ], 1 , 1 , 4 , 0 , 608 , (3, 0, None, None) , 0 , )),
	(( 'ToGrayscale' , ), 65, (65, (), [ ], 1 , 1 , 4 , 0 , 616 , (3, 0, None, None) , 0 , )),
	(( 'pComprColor' , 'pVal' , ), 66, (66, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 624 , (3, 0, None, None) , 0 , )),
	(( 'pComprColor' , 'pVal' , ), 66, (66, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 632 , (3, 0, None, None) , 0 , )),
	(( 'pComprBitonal' , 'pVal' , ), 67, (67, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 640 , (3, 0, None, None) , 0 , )),
	(( 'pComprBitonal' , 'pVal' , ), 67, (67, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 648 , (3, 0, None, None) , 0 , )),
	(( 'Info' , 'Type' , 'pVal' , ), 68, (68, (), [ (8, 1, None, None) , 
			 (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 656 , (3, 0, None, None) , 1088 , )),
	(( 'Info' , 'Type' , 'pVal' , ), 68, (68, (), [ (8, 1, None, None) , 
			 (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 664 , (3, 0, None, None) , 1088 , )),
	(( 'o' , 'pVal' , ), 69, (69, (), [ (16404, 10, None, None) , ], 1 , 2 , 4 , 0 , 672 , (3, 0, None, None) , 1088 , )),
	(( 'o' , 'pVal' , ), 69, (69, (), [ (20, 1, None, None) , ], 1 , 4 , 4 , 0 , 680 , (3, 0, None, None) , 1088 , )),
]

ICiLine_vtables_dispatch_ = 1
ICiLine_vtables_ = [
	(( 'Direction' , 'pVal' , ), 35, (35, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'Thickness' , 'pVal' , ), 36, (36, (), [ (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( 'Angle' , 'pVal' , ), 37, (37, (), [ (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( 'Rect' , 'pVal' , ), 38, (38, (), [ (16393, 10, None, "IID('{4ED88244-0BE1-11D4-B5F6-009FC6000000}')") , ], 1 , 2 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( 'Start' , 'pVal' , ), 39, (39, (), [ (16393, 10, None, "IID('{8C531E23-84B0-431E-B39E-849AB24613AF}')") , ], 1 , 2 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( 'End' , 'pVal' , ), 40, (40, (), [ (16393, 10, None, "IID('{8C531E23-84B0-431E-B39E-849AB24613AF}')") , ], 1 , 2 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
	(( 'o' , 'pVal' , ), 41, (41, (), [ (16404, 10, None, None) , ], 1 , 2 , 4 , 0 , 104 , (3, 0, None, None) , 1088 , )),
	(( 'o' , 'pVal' , ), 41, (41, (), [ (20, 1, None, None) , ], 1 , 4 , 4 , 0 , 112 , (3, 0, None, None) , 1088 , )),
]

ICiObject_vtables_dispatch_ = 1
ICiObject_vtables_ = [
	(( 'Pixels' , 'pVal' , ), 3, (3, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'Intervals' , 'pVal' , ), 4, (4, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( 'Rect' , 'pVal' , ), 5, (5, (), [ (16393, 10, None, "IID('{4ED88244-0BE1-11D4-B5F6-009FC6000000}')") , ], 1 , 2 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( 'cx3d' , 'i' , 'pVal' , ), 6, (6, (), [ (3, 1, None, None) , 
			 (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 80 , (3, 0, None, None) , 1088 , )),
	(( 'cx3d' , 'i' , 'pVal' , ), 6, (6, (), [ (3, 1, None, None) , 
			 (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 88 , (3, 0, None, None) , 1088 , )),
	(( 'cx2l' , 'i' , 'pVal' , ), 7, (7, (), [ (3, 1, None, None) , 
			 (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 96 , (3, 0, None, None) , 1088 , )),
	(( 'cx2l' , 'i' , 'pVal' , ), 7, (7, (), [ (3, 1, None, None) , 
			 (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 104 , (3, 0, None, None) , 1088 , )),
	(( 'o' , 'pVal' , ), 8, (8, (), [ (16404, 10, None, None) , ], 1 , 2 , 4 , 0 , 112 , (3, 0, None, None) , 1088 , )),
	(( 'o' , 'pVal' , ), 8, (8, (), [ (20, 1, None, None) , ], 1 , 4 , 4 , 0 , 120 , (3, 0, None, None) , 1088 , )),
]

ICiPdf_vtables_dispatch_ = 1
ICiPdf_vtables_ = [
	(( 'readEnabled' , 'pVal' , ), 1, (1, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 56 , (3, 0, None, None) , 1089 , )),
	(( 'writeEnabled' , 'pVal' , ), 2, (2, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 64 , (3, 0, None, None) , 1089 , )),
	(( 'dpiRasterBw' , 'pVal' , ), 3, (3, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( 'dpiRasterBw' , 'pVal' , ), 3, (3, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( 'dpiRasterGs' , 'pVal' , ), 4, (4, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( 'dpiRasterGs' , 'pVal' , ), 4, (4, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
	(( 'dpiRasterRgb' , 'pVal' , ), 5, (5, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 104 , (3, 0, None, None) , 0 , )),
	(( 'dpiRasterRgb' , 'pVal' , ), 5, (5, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 112 , (3, 0, None, None) , 0 , )),
	(( 'readMode' , 'pVal' , ), 6, (6, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 120 , (3, 0, None, None) , 0 , )),
	(( 'readMode' , 'pVal' , ), 6, (6, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 128 , (3, 0, None, None) , 0 , )),
	(( 'rasterColorMode' , 'pVal' , ), 7, (7, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 136 , (3, 0, None, None) , 0 , )),
	(( 'rasterColorMode' , 'pVal' , ), 7, (7, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 144 , (3, 0, None, None) , 0 , )),
	(( 'minImageWidth' , 'pVal' , ), 8, (8, (), [ (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 152 , (3, 0, None, None) , 0 , )),
	(( 'minImageWidth' , 'pVal' , ), 8, (8, (), [ (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 160 , (3, 0, None, None) , 0 , )),
	(( 'minImageHeight' , 'pVal' , ), 9, (9, (), [ (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 168 , (3, 0, None, None) , 0 , )),
	(( 'minImageHeight' , 'pVal' , ), 9, (9, (), [ (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 176 , (3, 0, None, None) , 0 , )),
	(( 'useMinImageColors' , 'pVal' , ), 10, (10, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 184 , (3, 0, None, None) , 0 , )),
	(( 'useMinImageColors' , 'pVal' , ), 10, (10, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 192 , (3, 0, None, None) , 0 , )),
	(( 'Creator' , 'pVal' , ), 11, (11, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 200 , (3, 0, None, None) , 0 , )),
	(( 'Creator' , 'pVal' , ), 11, (11, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 208 , (3, 0, None, None) , 0 , )),
	(( 'CreationDate' , 'pVal' , ), 12, (12, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 216 , (3, 0, None, None) , 0 , )),
	(( 'CreationDate' , 'pVal' , ), 12, (12, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 224 , (3, 0, None, None) , 0 , )),
	(( 'Author' , 'pVal' , ), 13, (13, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 232 , (3, 0, None, None) , 0 , )),
	(( 'Author' , 'pVal' , ), 13, (13, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 240 , (3, 0, None, None) , 0 , )),
	(( 'Producer' , 'pVal' , ), 14, (14, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 248 , (3, 0, None, None) , 0 , )),
	(( 'Producer' , 'pVal' , ), 14, (14, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 256 , (3, 0, None, None) , 0 , )),
	(( 'Title' , 'pVal' , ), 15, (15, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 264 , (3, 0, None, None) , 0 , )),
	(( 'Title' , 'pVal' , ), 15, (15, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 272 , (3, 0, None, None) , 0 , )),
	(( 'Subject' , 'pVal' , ), 16, (16, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 280 , (3, 0, None, None) , 0 , )),
	(( 'Subject' , 'pVal' , ), 16, (16, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 288 , (3, 0, None, None) , 0 , )),
	(( 'Keywords' , 'pVal' , ), 17, (17, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 296 , (3, 0, None, None) , 0 , )),
	(( 'Keywords' , 'pVal' , ), 17, (17, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 304 , (3, 0, None, None) , 0 , )),
	(( 'ModDate' , 'pVal' , ), 18, (18, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 312 , (3, 0, None, None) , 0 , )),
	(( 'ModDate' , 'pVal' , ), 18, (18, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 320 , (3, 0, None, None) , 0 , )),
	(( 'Ptr' , 'pVal' , ), 19, (19, (), [ (16408, 10, None, None) , ], 1 , 2 , 4 , 0 , 328 , (3, 0, None, None) , 1089 , )),
	(( 'PageSize' , 'pVal' , ), 20, (20, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 336 , (3, 0, None, None) , 1089 , )),
	(( 'PageSize' , 'pVal' , ), 20, (20, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 344 , (3, 0, None, None) , 1089 , )),
	(( 'PageOrientation' , 'pVal' , ), 21, (21, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 352 , (3, 0, None, None) , 1089 , )),
	(( 'PageOrientation' , 'pVal' , ), 21, (21, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 360 , (3, 0, None, None) , 1089 , )),
	(( 'ImageAlignment' , 'pVal' , ), 22, (22, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 368 , (3, 0, None, None) , 1089 , )),
	(( 'ImageAlignment' , 'pVal' , ), 22, (22, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 376 , (3, 0, None, None) , 1089 , )),
	(( 'o' , 'pVal' , ), 23, (23, (), [ (16404, 10, None, None) , ], 1 , 2 , 4 , 0 , 384 , (3, 0, None, None) , 1088 , )),
	(( 'o' , 'pVal' , ), 23, (23, (), [ (20, 1, None, None) , ], 1 , 4 , 4 , 0 , 392 , (3, 0, None, None) , 1088 , )),
]

ICiPdf417_vtables_dispatch_ = 1
ICiPdf417_vtables_ = [
	(( 'FirstBarcode' , 'pVal' , ), 2, (2, (), [ (16393, 10, None, "IID('{4ED88240-0BE1-11D4-B5F6-009FC6000000}')") , ], 1 , 1 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'NextBarcode' , 'pVal' , ), 3, (3, (), [ (16393, 10, None, "IID('{4ED88240-0BE1-11D4-B5F6-009FC6000000}')") , ], 1 , 1 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( 'Image' , 'pVal' , ), 5, (5, (), [ (16393, 10, None, "IID('{F2BCF189-0B27-11D4-B5F5-9CC767000000}')") , ], 1 , 2 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( 'Image' , 'pVal' , ), 5, (5, (), [ (9, 1, None, "IID('{F2BCF189-0B27-11D4-B5F5-9CC767000000}')") , ], 1 , 4 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( 'Algorithm' , 'pVal' , ), 4, (4, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( 'Algorithm' , 'pVal' , ), 4, (4, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
	(( 'DiagFlags' , 'pVal' , ), 7, (7, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 104 , (3, 0, None, None) , 0 , )),
	(( 'DiagFlags' , 'pVal' , ), 7, (7, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 112 , (3, 0, None, None) , 0 , )),
	(( 'Barcodes' , 'pVal' , ), 9, (9, (), [ (16393, 10, None, "IID('{41F7F4D4-9FC1-46C6-92E5-2A3457CE3D5E}')") , ], 1 , 2 , 4 , 0 , 120 , (3, 0, None, None) , 0 , )),
	(( 'Directions' , 'pVal' , ), 8, (8, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 128 , (3, 0, None, None) , 0 , )),
	(( 'Directions' , 'pVal' , ), 8, (8, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 136 , (3, 0, None, None) , 0 , )),
	(( 'Find' , 'MaxBarcodes' , 'pVal' , ), 10, (10, (), [ (3, 49, '0', None) , 
			 (16387, 10, None, None) , ], 1 , 1 , 4 , 0 , 144 , (3, 0, None, None) , 0 , )),
	(( 'Fx1' , 'par1' , 'par2' , 'ppRet' , ), 11, (11, (), [ 
			 (3, 49, '0', None) , (3, 49, '0', None) , (16397, 10, None, None) , ], 1 , 1 , 4 , 0 , 152 , (3, 0, None, None) , 1088 , )),
	(( 'cx2l' , 'i' , 'pVal' , ), 12, (12, (), [ (3, 1, None, None) , 
			 (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 160 , (3, 0, None, None) , 1088 , )),
	(( 'cx2l' , 'i' , 'pVal' , ), 12, (12, (), [ (3, 1, None, None) , 
			 (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 168 , (3, 0, None, None) , 1088 , )),
	(( 'Encodings' , 'pVal' , ), 13, (13, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 176 , (3, 0, None, None) , 0 , )),
	(( 'Encodings' , 'pVal' , ), 13, (13, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 184 , (3, 0, None, None) , 0 , )),
	(( 'o' , 'pVal' , ), 14, (14, (), [ (16404, 10, None, None) , ], 1 , 2 , 4 , 0 , 192 , (3, 0, None, None) , 1088 , )),
	(( 'o' , 'pVal' , ), 14, (14, (), [ (20, 1, None, None) , ], 1 , 4 , 4 , 0 , 200 , (3, 0, None, None) , 1088 , )),
]

ICiPoint_vtables_dispatch_ = 1
ICiPoint_vtables_ = [
	(( 'x' , 'pVal' , ), 1, (1, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'x' , 'pVal' , ), 1, (1, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( 'y' , 'pVal' , ), 2, (2, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( 'y' , 'pVal' , ), 2, (2, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( 'o' , 'pVal' , ), 3, (3, (), [ (16404, 10, None, None) , ], 1 , 2 , 4 , 0 , 88 , (3, 0, None, None) , 1088 , )),
	(( 'o' , 'pVal' , ), 3, (3, (), [ (20, 1, None, None) , ], 1 , 4 , 4 , 0 , 96 , (3, 0, None, None) , 1088 , )),
]

ICiQR_vtables_dispatch_ = 1
ICiQR_vtables_ = [
	(( 'FirstBarcode' , 'pVal' , ), 2, (2, (), [ (16393, 10, None, "IID('{4ED88240-0BE1-11D4-B5F6-009FC6000000}')") , ], 1 , 1 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'NextBarcode' , 'pVal' , ), 3, (3, (), [ (16393, 10, None, "IID('{4ED88240-0BE1-11D4-B5F6-009FC6000000}')") , ], 1 , 1 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( 'Image' , 'pVal' , ), 5, (5, (), [ (16393, 10, None, "IID('{F2BCF189-0B27-11D4-B5F5-9CC767000000}')") , ], 1 , 2 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( 'Image' , 'pVal' , ), 5, (5, (), [ (9, 1, None, "IID('{F2BCF189-0B27-11D4-B5F5-9CC767000000}')") , ], 1 , 4 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( 'Algorithm' , 'pVal' , ), 4, (4, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( 'Algorithm' , 'pVal' , ), 4, (4, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
	(( 'DiagFlags' , 'pVal' , ), 7, (7, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 104 , (3, 0, None, None) , 0 , )),
	(( 'DiagFlags' , 'pVal' , ), 7, (7, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 112 , (3, 0, None, None) , 0 , )),
	(( 'Barcodes' , 'pVal' , ), 9, (9, (), [ (16393, 10, None, "IID('{41F7F4D4-9FC1-46C6-92E5-2A3457CE3D5E}')") , ], 1 , 2 , 4 , 0 , 120 , (3, 0, None, None) , 0 , )),
	(( 'Directions' , 'pVal' , ), 8, (8, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 128 , (3, 0, None, None) , 1088 , )),
	(( 'Directions' , 'pVal' , ), 8, (8, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 136 , (3, 0, None, None) , 1088 , )),
	(( 'Find' , 'MaxBarcodes' , 'pVal' , ), 10, (10, (), [ (3, 49, '0', None) , 
			 (16387, 10, None, None) , ], 1 , 1 , 4 , 0 , 144 , (3, 0, None, None) , 0 , )),
	(( 'Fx1' , 'par1' , 'par2' , 'ppRet' , ), 11, (11, (), [ 
			 (3, 49, '0', None) , (3, 49, '0', None) , (16397, 10, None, None) , ], 1 , 1 , 4 , 0 , 152 , (3, 0, None, None) , 1088 , )),
	(( 'cx2l' , 'i' , 'pVal' , ), 12, (12, (), [ (3, 1, None, None) , 
			 (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 160 , (3, 0, None, None) , 1088 , )),
	(( 'cx2l' , 'i' , 'pVal' , ), 12, (12, (), [ (3, 1, None, None) , 
			 (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 168 , (3, 0, None, None) , 1088 , )),
	(( 'Encodings' , 'pVal' , ), 13, (13, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 176 , (3, 0, None, None) , 0 , )),
	(( 'Encodings' , 'pVal' , ), 13, (13, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 184 , (3, 0, None, None) , 0 , )),
	(( 'o' , 'pVal' , ), 14, (14, (), [ (16404, 10, None, None) , ], 1 , 2 , 4 , 0 , 192 , (3, 0, None, None) , 1088 , )),
	(( 'o' , 'pVal' , ), 14, (14, (), [ (20, 1, None, None) , ], 1 , 4 , 4 , 0 , 200 , (3, 0, None, None) , 1088 , )),
]

ICiRect_vtables_dispatch_ = 1
ICiRect_vtables_ = [
	(( 'top' , 'pVal' , ), 1, (1, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'top' , 'pVal' , ), 1, (1, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( 'bottom' , 'pVal' , ), 2, (2, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( 'bottom' , 'pVal' , ), 2, (2, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( 'left' , 'pVal' , ), 3, (3, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( 'left' , 'pVal' , ), 3, (3, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
	(( 'right' , 'pVal' , ), 4, (4, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 104 , (3, 0, None, None) , 0 , )),
	(( 'right' , 'pVal' , ), 4, (4, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 112 , (3, 0, None, None) , 0 , )),
	(( 'Empty' , ), 5, (5, (), [ ], 1 , 1 , 4 , 0 , 120 , (3, 0, None, None) , 0 , )),
	(( 'IsEmpty' , 'pVal' , ), 6, (6, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 128 , (3, 0, None, None) , 0 , )),
	(( 'o' , 'pVal' , ), 7, (7, (), [ (16404, 10, None, None) , ], 1 , 2 , 4 , 0 , 136 , (3, 0, None, None) , 1088 , )),
	(( 'o' , 'pVal' , ), 7, (7, (), [ (20, 1, None, None) , ], 1 , 4 , 4 , 0 , 144 , (3, 0, None, None) , 1088 , )),
]

ICiRepair_vtables_dispatch_ = 1
ICiRepair_vtables_ = [
	(( 'FaxStandardToFine' , ), 1, (1, (), [ ], 1 , 1 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'FaxRemoveBlankLines' , ), 2, (2, (), [ ], 1 , 1 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( 'FaxRemoveHeader' , ), 3, (3, (), [ ], 1 , 1 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( 'AutoDeskew' , 'pVal' , ), 36, (36, (), [ (16389, 10, None, None) , ], 1 , 1 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( 'AutoRotate' , 'pVal' , ), 37, (37, (), [ (16387, 10, None, None) , ], 1 , 1 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( 'Image' , 'pVal' , ), 39, (39, (), [ (16393, 10, None, "IID('{F2BCF189-0B27-11D4-B5F5-9CC767000000}')") , ], 1 , 2 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
	(( 'Image' , 'pVal' , ), 39, (39, (), [ (9, 1, None, "IID('{F2BCF189-0B27-11D4-B5F5-9CC767000000}')") , ], 1 , 4 , 4 , 0 , 104 , (3, 0, None, None) , 0 , )),
	(( 'pMinLineLength' , 'pVal' , ), 16, (16, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 112 , (3, 0, None, None) , 0 , )),
	(( 'pMinLineLength' , 'pVal' , ), 16, (16, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 120 , (3, 0, None, None) , 0 , )),
	(( 'pMaxLineGap' , 'pVal' , ), 17, (17, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 128 , (3, 0, None, None) , 0 , )),
	(( 'pMaxLineGap' , 'pVal' , ), 17, (17, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 136 , (3, 0, None, None) , 0 , )),
	(( 'pMaxLineAngle' , 'pVal' , ), 18, (18, (), [ (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 144 , (3, 0, None, None) , 0 , )),
	(( 'pMaxLineAngle' , 'pVal' , ), 18, (18, (), [ (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 152 , (3, 0, None, None) , 0 , )),
	(( 'pLineCurvature' , 'pVal' , ), 19, (19, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 160 , (3, 0, None, None) , 0 , )),
	(( 'pLineCurvature' , 'pVal' , ), 19, (19, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 168 , (3, 0, None, None) , 0 , )),
	(( 'CleanBorders' , ), 20, (20, (), [ ], 1 , 1 , 4 , 0 , 176 , (3, 0, None, None) , 1088 , )),
	(( 'RemovePunchHoles' , ), 21, (21, (), [ ], 1 , 1 , 4 , 0 , 184 , (3, 0, None, None) , 0 , )),
	(( 'RemoveHalftone' , ), 22, (22, (), [ ], 1 , 1 , 4 , 0 , 192 , (3, 0, None, None) , 0 , )),
	(( 'SmoothCharacters' , 'Type' , ), 23, (23, (), [ (3, 1, None, None) , ], 1 , 1 , 4 , 0 , 200 , (3, 0, None, None) , 0 , )),
	(( 'CleanNoise' , 'NoiseSize' , ), 24, (24, (), [ (3, 1, None, None) , ], 1 , 1 , 4 , 0 , 208 , (3, 0, None, None) , 0 , )),
	(( 'AutoInvertImage' , 'Threshold' , ), 25, (25, (), [ (3, 1, None, None) , ], 1 , 1 , 4 , 0 , 216 , (3, 0, None, None) , 0 , )),
	(( 'AutoInvertBlocks' , 'MinWidth' , 'MinHeight' , ), 26, (26, (), [ (3, 1, None, None) , 
			 (3, 1, None, None) , ], 1 , 1 , 4 , 0 , 224 , (3, 0, None, None) , 1088 , )),
	(( 'ReconstructLines' , 'Direction' , ), 29, (29, (), [ (3, 1, None, None) , ], 1 , 1 , 4 , 0 , 232 , (3, 0, None, None) , 0 , )),
	(( 'AutoCrop' , 'NewLeftMargin' , 'NewTopMargin' , 'NewRightMargin' , 'NewBottomMargin' , 
			 ), 30, (30, (), [ (3, 1, None, None) , (3, 1, None, None) , (3, 1, None, None) , (3, 1, None, None) , ], 1 , 1 , 4 , 0 , 240 , (3, 0, None, None) , 0 , )),
	(( 'AutoRegister' , 'NewLeftMargin' , 'NewTopMargin' , ), 31, (31, (), [ (3, 1, None, None) , 
			 (3, 1, None, None) , ], 1 , 1 , 4 , 0 , 248 , (3, 0, None, None) , 0 , )),
	(( 'DeleteLines' , 'Direction' , 'bRepair' , ), 40, (40, (), [ (3, 1, None, None) , 
			 (3, 49, '65535', None) , ], 1 , 1 , 4 , 0 , 256 , (3, 0, None, None) , 0 , )),
	(( 'BorderExtract' , 'Flags' , 'Algorithm' , ), 41, (41, (), [ (3, 49, '3', None) , 
			 (3, 49, '2', None) , ], 1 , 1 , 4 , 0 , 264 , (3, 0, None, None) , 0 , )),
	(( 'ClearBackground' , 'ThrLevel' , ), 42, (42, (), [ (5, 49, '30.0', None) , ], 1 , 1 , 4 , 0 , 272 , (3, 0, None, None) , 0 , )),
	(( 'Resize' , 'PageSize' , 'PageOrientation' , 'ImageAlignment' , 'Width' , 
			 'Height' , 'Unit' , ), 43, (43, (), [ (3, 1, None, None) , (3, 49, '0', None) , 
			 (3, 49, '0', None) , (5, 49, '8.5', None) , (5, 49, '11.0', None) , (3, 49, '1', None) , ], 1 , 1 , 4 , 0 , 280 , (3, 0, None, None) , 0 , )),
	(( 'IsBlankImage' , 'reserved0' , 'reserved1' , 'reserved2' , 'pVal' , 
			 ), 44, (44, (), [ (3, 49, '0', None) , (5, 49, '0.0', None) , (5, 49, '0.0', None) , (16387, 10, None, None) , ], 1 , 1 , 4 , 0 , 288 , (3, 0, None, None) , 0 , )),
	(( 'cx2l' , 'i' , 'pVal' , ), 45, (45, (), [ (3, 1, None, None) , 
			 (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 296 , (3, 0, None, None) , 1088 , )),
	(( 'cx2l' , 'i' , 'pVal' , ), 45, (45, (), [ (3, 1, None, None) , 
			 (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 304 , (3, 0, None, None) , 1088 , )),
	(( 'cx3d' , 'i' , 'pVal' , ), 46, (46, (), [ (3, 1, None, None) , 
			 (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 312 , (3, 0, None, None) , 1088 , )),
	(( 'cx3d' , 'i' , 'pVal' , ), 46, (46, (), [ (3, 1, None, None) , 
			 (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 320 , (3, 0, None, None) , 1088 , )),
	(( 'AdvancedBinarize' , 'targetDpi' , 'reserved1' , 'reserved2' , ), 47, (47, (), [ 
			 (3, 49, '0', None) , (5, 49, '0.0', None) , (5, 49, '0.0', None) , ], 1 , 1 , 4 , 0 , 328 , (3, 0, None, None) , 0 , )),
	(( 'MinimizeBitsPerPixel' , 'reserved1' , 'reserved2' , ), 48, (48, (), [ (5, 49, '0.0', None) , 
			 (5, 49, '0.0', None) , ], 1 , 1 , 4 , 0 , 336 , (3, 0, None, None) , 1088 , )),
	(( 'CleanNoiseExt' , 'Flags' , 'maxNoiseSizeHorz' , 'maxNoiseSizeVert' , 'minObjectDistance' , 
			 'reserved0' , ), 50, (50, (), [ (3, 1, None, None) , (3, 1, None, None) , (3, 1, None, None) , 
			 (3, 1, None, None) , (3, 1, None, None) , ], 1 , 1 , 4 , 0 , 344 , (3, 0, None, None) , 0 , )),
	(( 'o' , 'pVal' , ), 51, (51, (), [ (16404, 10, None, None) , ], 1 , 2 , 4 , 0 , 352 , (3, 0, None, None) , 1088 , )),
	(( 'o' , 'pVal' , ), 51, (51, (), [ (20, 1, None, None) , ], 1 , 4 , 4 , 0 , 360 , (3, 0, None, None) , 1088 , )),
]

ICiServer_vtables_dispatch_ = 1
ICiServer_vtables_ = [
	(( 'CreateImage' , 'ppInt' , ), 1, (1, (), [ (16393, 10, None, "IID('{F2BCF189-0B27-11D4-B5F5-9CC767000000}')") , ], 1 , 1 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'CreateBarcodePro' , 'ppInt' , ), 2, (2, (), [ (16393, 10, None, "IID('{BDDB0244-0CFD-11D4-B5F8-B89D57000000}')") , ], 1 , 1 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( 'OpenExt' , 'hModule' , 'MasterId' , 'pParam' , ), 10, (10, (), [ 
			 (20, 1, None, None) , (3, 1, None, None) , (20, 1, None, None) , ], 1 , 1 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( 'CreateRect' , 'left' , 'top' , 'right' , 'bottom' , 
			 'ppInt' , ), 11, (11, (), [ (3, 49, '0', None) , (3, 49, '0', None) , (3, 49, '0', None) , 
			 (3, 49, '0', None) , (16393, 10, None, "IID('{4ED88244-0BE1-11D4-B5F6-009FC6000000}')") , ], 1 , 1 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( 'VerMajor' , 'pVal' , ), 12, (12, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( 'VerMinor' , 'pVal' , ), 13, (13, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
	(( 'VerRelease' , 'pVal' , ), 14, (14, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 104 , (3, 0, None, None) , 0 , )),
	(( 'CreateRepair' , 'ppInt' , ), 5, (5, (), [ (16393, 10, None, "IID('{63F6480C-997E-4FDE-AD63-A24E5F0FFDC7}')") , ], 1 , 1 , 4 , 0 , 112 , (3, 0, None, None) , 0 , )),
	(( 'CreateTools' , 'ppInt' , ), 6, (6, (), [ (16393, 10, None, "IID('{316BC128-8995-471D-985D-B3E68E87C084}')") , ], 1 , 1 , 4 , 0 , 120 , (3, 0, None, None) , 0 , )),
	(( 'CreateBarcodeBasic' , 'ppInt' , ), 8, (8, (), [ (16393, 10, None, "IID('{21DA65F1-9E63-45E3-B081-F78096F9D6C3}')") , ], 1 , 1 , 4 , 0 , 128 , (3, 0, None, None) , 0 , )),
	(( 'CreatePdf417' , 'ppInt' , ), 9, (9, (), [ (16393, 10, None, "IID('{8B79E556-FAD7-4339-8A8F-2C35D5C42C6E}')") , ], 1 , 1 , 4 , 0 , 136 , (3, 0, None, None) , 0 , )),
	(( 'CreateDataMatrix' , 'ppInt' , ), 15, (15, (), [ (16393, 10, None, "IID('{8B79E556-FAD7-4339-8A8F-2C35D5C42C6F}')") , ], 1 , 1 , 4 , 0 , 144 , (3, 0, None, None) , 0 , )),
	(( 'Info' , 'Type' , 'nParam' , 'pVal' , ), 16, (16, (), [ 
			 (3, 1, None, None) , (3, 49, '0', None) , (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 152 , (3, 0, None, None) , 0 , )),
	(( 'CreateAdvColor' , 'ppInt' , ), 17, (17, (), [ (16393, 10, None, "IID('{8CBBAECA-9716-40CA-B8F6-0E9FF213522A}')") , ], 1 , 1 , 4 , 0 , 160 , (3, 0, None, None) , 0 , )),
	(( 'CreateBarcode' , 'ppInt' , ), 18, (18, (), [ (16393, 10, None, "IID('{4ED88240-0BE1-11D4-B5F6-009FC6000000}')") , ], 1 , 1 , 4 , 0 , 168 , (3, 0, None, None) , 1088 , )),
	(( 'CreateBarcodes' , 'ppInt' , ), 19, (19, (), [ (16393, 10, None, "IID('{41F7F4D4-9FC1-46C6-92E5-2A3457CE3D5E}')") , ], 1 , 1 , 4 , 0 , 176 , (3, 0, None, None) , 1088 , )),
	(( 'DevMode' , 'bGlobalDevMode' , 'pVal' , ), 20, (20, (), [ (3, 49, '0', None) , 
			 (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 184 , (3, 0, None, None) , 0 , )),
	(( 'DevMode' , 'bGlobalDevMode' , 'pVal' , ), 20, (20, (), [ (3, 49, '0', None) , 
			 (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 184 , (3, 0, None, None) , 0 , )),
	(( 'DevMode' , 'bGlobalDevMode' , 'pVal' , ), 20, (20, (), [ (3, 49, '0', None) , 
			 (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 192 , (3, 0, None, None) , 0 , )),
	(( 'DevMode' , 'bGlobalDevMode' , 'pVal' , ), 20, (20, (), [ (3, 49, '0', None) , 
			 (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 192 , (3, 0, None, None) , 0 , )),
	(( 'Var' , 'Name' , 'pVal' , ), 21, (21, (), [ (8, 1, None, None) , 
			 (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 200 , (3, 0, None, None) , 1088 , )),
	(( 'Var' , 'Name' , 'pVal' , ), 21, (21, (), [ (8, 1, None, None) , 
			 (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 208 , (3, 0, None, None) , 1088 , )),
	(( 'uncompress' , 'DataIn' , 'Encoding' , 'DataOut' , 'RetCodeLng' , 
			 ), 22, (22, (), [ (12, 1, None, None) , (16387, 3, None, None) , (16396, 2, None, None) , (16387, 10, None, None) , ], 1 , 1 , 4 , 0 , 216 , (3, 0, None, None) , 1088 , )),
	(( 'CreateQR' , 'ppInt' , ), 23, (23, (), [ (16393, 10, None, "IID('{8B79E556-FAD7-4339-8A8F-2C35D5C42C70}')") , ], 1 , 1 , 4 , 0 , 224 , (3, 0, None, None) , 0 , )),
	(( 'OpenUser' , 'User' , 'key' , 'reserved' , ), 24, (24, (), [ 
			 (8, 1, None, None) , (8, 1, None, None) , (8, 1, None, None) , ], 1 , 1 , 4 , 0 , 232 , (3, 0, None, None) , 1088 , )),
	(( 'o' , 'pVal' , ), 25, (25, (), [ (16404, 10, None, None) , ], 1 , 2 , 4 , 0 , 240 , (3, 0, None, None) , 1088 , )),
	(( 'o' , 'pVal' , ), 25, (25, (), [ (20, 1, None, None) , ], 1 , 4 , 4 , 0 , 248 , (3, 0, None, None) , 1088 , )),
]

ICiTools_vtables_dispatch_ = 1
ICiTools_vtables_ = [
	(( 'FirstObject' , 'pVal' , ), 1, (1, (), [ (16393, 10, None, "IID('{59A0E32D-5050-47F5-A21B-F00397A21FCC}')") , ], 1 , 1 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'NextObject' , 'pVal' , ), 2, (2, (), [ (16393, 10, None, "IID('{59A0E32D-5050-47F5-A21B-F00397A21FCC}')") , ], 1 , 1 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( 'ExtractObject' , 'Object' , 'ppInt' , ), 6, (6, (), [ (9, 1, None, "IID('{59A0E32D-5050-47F5-A21B-F00397A21FCC}')") , 
			 (16393, 10, None, "IID('{F2BCF189-0B27-11D4-B5F5-9CC767000000}')") , ], 1 , 1 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( 'pMinLineLength' , 'pVal' , ), 8, (8, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( 'pMinLineLength' , 'pVal' , ), 8, (8, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( 'pMaxLineGap' , 'pVal' , ), 9, (9, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
	(( 'pMaxLineGap' , 'pVal' , ), 9, (9, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 104 , (3, 0, None, None) , 0 , )),
	(( 'pMaxLineAngle' , 'pVal' , ), 10, (10, (), [ (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 112 , (3, 0, None, None) , 0 , )),
	(( 'pMaxLineAngle' , 'pVal' , ), 10, (10, (), [ (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 120 , (3, 0, None, None) , 0 , )),
	(( 'pLineCurvature' , 'pVal' , ), 11, (11, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 128 , (3, 0, None, None) , 0 , )),
	(( 'pLineCurvature' , 'pVal' , ), 11, (11, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 136 , (3, 0, None, None) , 0 , )),
	(( 'FirstLine' , 'pVal' , ), 12, (12, (), [ (16393, 10, None, "IID('{B8E5EE38-BB0D-4561-B8D3-26C18C8817EE}')") , ], 1 , 1 , 4 , 0 , 144 , (3, 0, None, None) , 0 , )),
	(( 'NextLine' , 'pVal' , ), 13, (13, (), [ (16393, 10, None, "IID('{B8E5EE38-BB0D-4561-B8D3-26C18C8817EE}')") , ], 1 , 1 , 4 , 0 , 152 , (3, 0, None, None) , 0 , )),
	(( 'MeasureMargins' , 'pVal' , ), 14, (14, (), [ (16393, 10, None, "IID('{4ED88244-0BE1-11D4-B5F6-009FC6000000}')") , ], 1 , 1 , 4 , 0 , 160 , (3, 0, None, None) , 0 , )),
	(( 'MeasureSkew' , 'pVal' , ), 19, (19, (), [ (16389, 10, None, None) , ], 1 , 1 , 4 , 0 , 168 , (3, 0, None, None) , 0 , )),
	(( 'MeasureRotation' , 'pVal' , ), 42, (42, (), [ (16387, 10, None, None) , ], 1 , 1 , 4 , 0 , 176 , (3, 0, None, None) , 0 , )),
	(( 'CountPixels' , 'Pixels' , ), 23, (23, (), [ (16387, 10, None, None) , ], 1 , 1 , 4 , 0 , 184 , (3, 0, None, None) , 0 , )),
	(( 'MeasureVertHistogram' , 'pData' , ), 24, (24, (), [ (16396, 10, None, None) , ], 1 , 1 , 4 , 0 , 192 , (3, 0, None, None) , 0 , )),
	(( 'MeasureHorzHistogram' , 'pData' , ), 25, (25, (), [ (16396, 10, None, None) , ], 1 , 1 , 4 , 0 , 200 , (3, 0, None, None) , 0 , )),
	(( 'Image' , 'pVal' , ), 26, (26, (), [ (16393, 10, None, "IID('{F2BCF189-0B27-11D4-B5F5-9CC767000000}')") , ], 1 , 2 , 4 , 0 , 208 , (3, 0, None, None) , 0 , )),
	(( 'Image' , 'pVal' , ), 26, (26, (), [ (9, 1, None, "IID('{F2BCF189-0B27-11D4-B5F5-9CC767000000}')") , ], 1 , 4 , 4 , 0 , 216 , (3, 0, None, None) , 0 , )),
	(( 'rConfidence' , 'pVal' , ), 22, (22, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 224 , (3, 0, None, None) , 0 , )),
	(( 'pLineDirection' , 'pVal' , ), 41, (41, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 232 , (3, 0, None, None) , 0 , )),
	(( 'pLineDirection' , 'pVal' , ), 41, (41, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 240 , (3, 0, None, None) , 0 , )),
	(( 'Skew' , 'Angle' , ), 38, (38, (), [ (5, 1, None, None) , ], 1 , 1 , 4 , 0 , 248 , (3, 0, None, None) , 0 , )),
	(( 'Fatten' , 'Pixels' , 'Direction' , ), 54, (54, (), [ (3, 1, None, None) , 
			 (3, 1, None, None) , ], 1 , 1 , 4 , 0 , 256 , (3, 0, None, None) , 0 , )),
	(( 'Trim' , 'Pixels' , 'Direction' , ), 55, (55, (), [ (3, 1, None, None) , 
			 (3, 1, None, None) , ], 1 , 1 , 4 , 0 , 264 , (3, 0, None, None) , 0 , )),
	(( 'Outline' , ), 56, (56, (), [ ], 1 , 1 , 4 , 0 , 272 , (3, 0, None, None) , 1088 , )),
	(( 'Skeleton' , ), 57, (57, (), [ ], 1 , 1 , 4 , 0 , 280 , (3, 0, None, None) , 1088 , )),
	(( 'AndImage' , 'ImgSrc' , 'left' , 'top' , ), 58, (58, (), [ 
			 (9, 1, None, "IID('{F2BCF189-0B27-11D4-B5F5-9CC767000000}')") , (3, 49, '0', None) , (3, 49, '0', None) , ], 1 , 1 , 4 , 0 , 288 , (3, 0, None, None) , 0 , )),
	(( 'OrImage' , 'ImgSrc' , 'left' , 'top' , ), 59, (59, (), [ 
			 (9, 1, None, "IID('{F2BCF189-0B27-11D4-B5F5-9CC767000000}')") , (3, 49, '0', None) , (3, 49, '0', None) , ], 1 , 1 , 4 , 0 , 296 , (3, 0, None, None) , 0 , )),
	(( 'XorImage' , 'ImgSrc' , 'left' , 'top' , ), 60, (60, (), [ 
			 (9, 1, None, "IID('{F2BCF189-0B27-11D4-B5F5-9CC767000000}')") , (3, 49, '0', None) , (3, 49, '0', None) , ], 1 , 1 , 4 , 0 , 304 , (3, 0, None, None) , 0 , )),
	(( 'PasteImage' , 'ImgSrc' , 'left' , 'top' , ), 61, (61, (), [ 
			 (9, 1, None, "IID('{F2BCF189-0B27-11D4-B5F5-9CC767000000}')") , (3, 49, '0', None) , (3, 49, '0', None) , ], 1 , 1 , 4 , 0 , 312 , (3, 0, None, None) , 0 , )),
	(( 'cx3d' , 'i' , 'pVal' , ), 62, (62, (), [ (3, 1, None, None) , 
			 (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 320 , (3, 0, None, None) , 1088 , )),
	(( 'cx3d' , 'i' , 'pVal' , ), 62, (62, (), [ (3, 1, None, None) , 
			 (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 328 , (3, 0, None, None) , 1088 , )),
	(( 'cx2l' , 'i' , 'pVal' , ), 63, (63, (), [ (3, 1, None, None) , 
			 (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 336 , (3, 0, None, None) , 1088 , )),
	(( 'cx2l' , 'i' , 'pVal' , ), 63, (63, (), [ (3, 1, None, None) , 
			 (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 344 , (3, 0, None, None) , 1088 , )),
	(( 'pScaleType' , 'pVal' , ), 73, (73, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 352 , (3, 0, None, None) , 0 , )),
	(( 'pScaleType' , 'pVal' , ), 73, (73, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 360 , (3, 0, None, None) , 0 , )),
	(( 'pScaleThreshold' , 'pVal' , ), 74, (74, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 368 , (3, 0, None, None) , 0 , )),
	(( 'pScaleThreshold' , 'pVal' , ), 74, (74, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 376 , (3, 0, None, None) , 0 , )),
	(( 'ScaleImage' , 'ScaleX' , 'ScaleY' , ), 75, (75, (), [ (5, 1, None, None) , 
			 (5, 1, None, None) , ], 1 , 1 , 4 , 0 , 384 , (3, 0, None, None) , 0 , )),
	(( 'pScaleBmpBrightness' , 'pVal' , ), 77, (77, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 392 , (3, 0, None, None) , 0 , )),
	(( 'pScaleBmpBrightness' , 'pVal' , ), 77, (77, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 400 , (3, 0, None, None) , 0 , )),
	(( 'pScaleBmpContrast' , 'pVal' , ), 78, (78, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 408 , (3, 0, None, None) , 0 , )),
	(( 'pScaleBmpContrast' , 'pVal' , ), 78, (78, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 416 , (3, 0, None, None) , 0 , )),
	(( 'pScaleBmpType' , 'pVal' , ), 76, (76, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 424 , (3, 0, None, None) , 0 , )),
	(( 'pScaleBmpType' , 'pVal' , ), 76, (76, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 432 , (3, 0, None, None) , 0 , )),
	(( 'ScaleToDIB' , 'ScaleX' , 'ScaleY' , 'hBitmap' , ), 79, (79, (), [ 
			 (5, 1, None, None) , (5, 1, None, None) , (16404, 10, None, None) , ], 1 , 1 , 4 , 0 , 440 , (3, 0, None, None) , 0 , )),
	(( 'MeasureContrast' , 'nArea' , 'pVal' , ), 80, (80, (), [ (3, 49, '1', None) , 
			 (16389, 10, None, None) , ], 1 , 1 , 4 , 0 , 448 , (3, 0, None, None) , 1088 , )),
	(( 'o' , 'pVal' , ), 81, (81, (), [ (16404, 10, None, None) , ], 1 , 2 , 4 , 0 , 456 , (3, 0, None, None) , 1088 , )),
	(( 'o' , 'pVal' , ), 81, (81, (), [ (20, 1, None, None) , ], 1 , 4 , 4 , 0 , 464 , (3, 0, None, None) , 1088 , )),
]

ICiView_vtables_dispatch_ = 1
ICiView_vtables_ = [
	(( 'o' , 'pVal' , ), 1, (1, (), [ (16404, 10, None, None) , ], 1 , 2 , 4 , 0 , 56 , (3, 0, None, None) , 1088 , )),
	(( 'o' , 'pVal' , ), 1, (1, (), [ (20, 1, None, None) , ], 1 , 4 , 4 , 0 , 64 , (3, 0, None, None) , 1088 , )),
]

RecordMap = {
}

CLSIDToClassMap = {
	'{BCE12DAC-09D5-4E64-AC70-9C7994B5832C}' : CiView,
	'{90E9D617-A4B1-4DDE-B842-60BECC114255}' : CiQR,
	'{F2BCF189-0B27-11D4-B5F5-9CC767000000}' : ICiImage,
	'{12806B0A-7754-4297-AE05-631C2A1E928D}' : CiBarcodeBasic,
	'{98AFD5D0-A728-498D-B1DE-0D811D719793}' : ICiView,
	'{8B79E556-FAD7-4339-8A8F-2C35D5C42C6E}' : ICiPdf417,
	'{8CBBAECA-9716-40CA-B8F6-0E9FF213522A}' : ICiAdvColor,
	'{286F56E6-7A78-4541-9D66-92DD901C7DE1}' : CiTools,
	'{8B79E556-FAD7-4339-8A8F-2C35D5C42C6F}' : ICiDataMatrix,
	'{F2BCF18A-0B27-11D4-B5F5-9CC767000000}' : CiImage,
	'{F2BCF18B-0B27-11D4-B5F5-9CC767000000}' : _ICiImageEvents,
	'{BDDB0244-0CFD-11D4-B5F8-B89D57000000}' : ICiBarcodePro,
	'{DAB01618-F817-4662-ADBA-46EE1C94921A}' : CiBarcodes,
	'{70A6F899-6298-447E-951C-07430C0FF812}' : ICiPdf,
	'{316BC128-8995-471D-985D-B3E68E87C084}' : ICiTools,
	'{BDDB0245-0CFD-11D4-B5F8-B89D57000000}' : CiBarcodePro,
	'{63F6480C-997E-4FDE-AD63-A24E5F0FFDC7}' : ICiRepair,
	'{A7E1D34A-24DA-4D97-AF2E-CE7E4481E1E2}' : CiPoint,
	'{21DA65F1-9E63-45E3-B081-F78096F9D6C3}' : ICiBarcodeBasic,
	'{4ED88240-0BE1-11D4-B5F6-009FC6000000}' : ICiBarcode,
	'{4ED88241-0BE1-11D4-B5F6-009FC6000000}' : CiBarcode,
	'{90E9D617-A4B1-4DDE-B842-60BECC114254}' : CiDataMatrix,
	'{4ED88244-0BE1-11D4-B5F6-009FC6000000}' : ICiRect,
	'{4ED88245-0BE1-11D4-B5F6-009FC6000000}' : CiRect,
	'{A7A8BF7F-8CB8-49DC-8A76-D0A1A145189C}' : CiLine,
	'{D836E300-A317-4C7E-BE61-D650CE242589}' : CiServer,
	'{8B79E556-FAD7-4339-8A8F-2C35D5C42C70}' : ICiQR,
	'{CB149079-A739-4178-A4DA-BACA546C3728}' : CiRepair,
	'{A34FC1A7-C73F-4706-886E-C4A33E37C6E5}' : ICiServer,
	'{3022D35D-0127-4C24-B1F0-1C66A831807E}' : CiAdvColor,
	'{FB2E2C05-DB40-4A6F-8E52-0243621D7734}' : CiPdf,
	'{59A0E32D-5050-47F5-A21B-F00397A21FCC}' : ICiObject,
	'{B8E5EE38-BB0D-4561-B8D3-26C18C8817EE}' : ICiLine,
	'{8C531E23-84B0-431E-B39E-849AB24613AF}' : ICiPoint,
	'{90E9D617-A4B1-4DDE-B842-60BECC114253}' : CiPdf417,
	'{41F7F4D4-9FC1-46C6-92E5-2A3457CE3D5E}' : ICiBarcodes,
	'{4BBE294D-3C2A-4698-8B5F-84B1D3A6F621}' : CiObject,
}
CLSIDToPackageMap = {}
win32com.client.CLSIDToClass.RegisterCLSIDsFromDict( CLSIDToClassMap )
VTablesToPackageMap = {}
VTablesToClassMap = {
	'{4ED88244-0BE1-11D4-B5F6-009FC6000000}' : 'ICiRect',
	'{316BC128-8995-471D-985D-B3E68E87C084}' : 'ICiTools',
	'{F2BCF189-0B27-11D4-B5F5-9CC767000000}' : 'ICiImage',
	'{63F6480C-997E-4FDE-AD63-A24E5F0FFDC7}' : 'ICiRepair',
	'{98AFD5D0-A728-498D-B1DE-0D811D719793}' : 'ICiView',
	'{8B79E556-FAD7-4339-8A8F-2C35D5C42C6E}' : 'ICiPdf417',
	'{B8E5EE38-BB0D-4561-B8D3-26C18C8817EE}' : 'ICiLine',
	'{8CBBAECA-9716-40CA-B8F6-0E9FF213522A}' : 'ICiAdvColor',
	'{A34FC1A7-C73F-4706-886E-C4A33E37C6E5}' : 'ICiServer',
	'{BDDB0244-0CFD-11D4-B5F8-B89D57000000}' : 'ICiBarcodePro',
	'{8B79E556-FAD7-4339-8A8F-2C35D5C42C70}' : 'ICiQR',
	'{70A6F899-6298-447E-951C-07430C0FF812}' : 'ICiPdf',
	'{8B79E556-FAD7-4339-8A8F-2C35D5C42C6F}' : 'ICiDataMatrix',
	'{59A0E32D-5050-47F5-A21B-F00397A21FCC}' : 'ICiObject',
	'{8C531E23-84B0-431E-B39E-849AB24613AF}' : 'ICiPoint',
	'{21DA65F1-9E63-45E3-B081-F78096F9D6C3}' : 'ICiBarcodeBasic',
	'{4ED88240-0BE1-11D4-B5F6-009FC6000000}' : 'ICiBarcode',
	'{41F7F4D4-9FC1-46C6-92E5-2A3457CE3D5E}' : 'ICiBarcodes',
}


NamesToIIDMap = {
	'ICiRect' : '{4ED88244-0BE1-11D4-B5F6-009FC6000000}',
	'ICiAdvColor' : '{8CBBAECA-9716-40CA-B8F6-0E9FF213522A}',
	'ICiQR' : '{8B79E556-FAD7-4339-8A8F-2C35D5C42C70}',
	'ICiObject' : '{59A0E32D-5050-47F5-A21B-F00397A21FCC}',
	'ICiBarcodePro' : '{BDDB0244-0CFD-11D4-B5F8-B89D57000000}',
	'ICiPdf' : '{70A6F899-6298-447E-951C-07430C0FF812}',
	'ICiBarcode' : '{4ED88240-0BE1-11D4-B5F6-009FC6000000}',
	'ICiBarcodeBasic' : '{21DA65F1-9E63-45E3-B081-F78096F9D6C3}',
	'ICiTools' : '{316BC128-8995-471D-985D-B3E68E87C084}',
	'ICiRepair' : '{63F6480C-997E-4FDE-AD63-A24E5F0FFDC7}',
	'ICiBarcodes' : '{41F7F4D4-9FC1-46C6-92E5-2A3457CE3D5E}',
	'_ICiImageEvents' : '{F2BCF18B-0B27-11D4-B5F5-9CC767000000}',
	'ICiDataMatrix' : '{8B79E556-FAD7-4339-8A8F-2C35D5C42C6F}',
	'ICiPdf417' : '{8B79E556-FAD7-4339-8A8F-2C35D5C42C6E}',
	'ICiLine' : '{B8E5EE38-BB0D-4561-B8D3-26C18C8817EE}',
	'ICiView' : '{98AFD5D0-A728-498D-B1DE-0D811D719793}',
	'ICiImage' : '{F2BCF189-0B27-11D4-B5F5-9CC767000000}',
	'ICiServer' : '{A34FC1A7-C73F-4706-886E-C4A33E37C6E5}',
	'ICiPoint' : '{8C531E23-84B0-431E-B39E-849AB24613AF}',
}

win32com.client.constants.__dicts__.append(constants.__dict__)

