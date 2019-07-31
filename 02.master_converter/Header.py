# Master Header 並び順
# Product Master

import pandas as pd

def Header():
    Header_product = ({'Process Mode':1,
                        'Master ID':2,
                        'Subsidiary Code':3,
                        'Inner Code':4,
                        'Product Code':5,
                        'Stock / MTO':6,
                        'Product Component':7,
                        'Production LT':8,
                        'Min Qty of Big Order':9,
                        'Max Qty of Big Order':10,
                        'Supplier Code of BO':11,
                        'Slide Qty 1':12,
                        'Slide Sales Pc/Unit 1':13,
                        'Slide Purchase Pc/Unit 1':14,
                        'Slide Production LT 1':15,
                        'Slide Days TS 1':16,
                        'Slide Qty 2':17,
                        'Slide Sales Pc/Unit 2':18,
                        'Slide Purchase Pc/Unit 2':19,
                        'Slide Production LT 2':20,
                        'Slide Days TS 2':21,
                        'Slide Qty 3':22,
                        'Slide Sales Pc/Unit 3':23,
                        'Slide Purchase Pc/Unit 3':24,
                        'Slide Production LT 3':25,
                        'Slide Days TS 3':26,
                        'Slide Qty 4':27,
                        'Slide Sales Pc/Unit 4':28,
                        'Slide Purchase Pc/Unit 4':29,
                        'Slide Production LT 4':30,
                        'Slide Days TS 4':31,
                        'Slide Qty 5':32,
                        'Slide Sales Pc/Unit 5':33,
                        'Slide Purchase Pc/Unit 5':34,
                        'Slide Production LT 5':35,
                        'Slide Days TS 5':36,
                        'Slide Qty 6':37,
                        'Slide Sales Pc/Unit 6':38,
                        'Slide Purchase Pc/Unit 6':39,
                        'Slide Production LT 6':40,
                        'Slide Days TS 6':41,
                        'Slide Qty 7':42,
                        'Slide Sales Pc/Unit 7':43,
                        'Slide Purchase Pc/Unit 7':44,
                        'Slide Production LT 7':45,
                        'Slide Days TS 7':46,
                        'Slide Qty 8':47,
                        'Slide Sales Pc/Unit 8':48,
                        'Slide Purchase Pc/Unit 8':49,
                        'Slide Production LT 8':50,
                        'Slide Days TS 8':51,
                        'Slide Qty 9':52,
                        'Slide Sales Pc/Unit 9':53,
                        'Slide Purchase Pc/Unit 9':54,
                        'Slide Production LT 9':55,
                        'Slide Days TS 9':56,
                        'Slide Qty 10':57,
                        'Slide Sales Pc/Unit 10':58,
                        'Slide Purchase Pc/Unit 10':59,
                        'Slide Production LT 10':60,
                        'Slide Days TS 10':61,
                        'Unit Price Check':62,
                        'Express T Calc Type for Sales':63,
                        'Express T Sales Pc/Unit':64,
                        'Express T Purchase Pc/Unit':65,
                        'Express A Calc Type for Sales':66,
                        'Express A Sales Pc/Unit':67,
                        'Express A Calc Type for Purchase':68,
                        'Express A Purchase Pc/Unit':69,
                        'Express A Production LT':70,
                        'Special Express A Calc Type for Sales':71,
                        'Special Express A Sales Pc/Unit':72,
                        'Plant Express A Purchase Calc':73,
                        'Plant Express A Purchase Pc/Unit':74,
                        'Express B Calc Type for Sales':75,
                        'Express B Sales Pc/Unit':76,
                        'Express B Purchase Pc/Unit':77,
                        'Express B Production LT':78,
                        'Express C Calc Type for Sales':79,
                        'Express C Sales Pc/Unit':80,
                        'Express C Purchase Pc/Unit':81,
                        'Express C Production LT':82,
                        'Weight':83,
                        'Weight Calc Mode':84,
                        'Weight Coefficient':85,
                        'Weight Calc':86,
                        'Classify Code':87,
                        'Launch Date':88,
                        'Prod Mst for Alt Supplier':89,
                        'Supplier Code':90,
                        'Spec Condition Code':91,
                        'Ordering Message Code':92,
                        'Alt Dsct Rt:S 1':93,
                        'Alt Dsct Rt:P 1':94,
                        'Alt Dsct Rt:S 2':95,
                        'Alt Dsct Rt:P 2':96,
                        'Alt Dsct Rt:S 3':97,
                        'Alt Dsct Rt:P 3':98,
                        'Alt Dsct Rt:S 4':99,
                        'Alt Dsct Rt:P 4':100,
                        'Alt Dsct Rt:S 5':101,
                        'Alt Dsct Rt:P 5':102,
                        'Alt Dsct Rt:S 6':103,
                        'Alt Dsct Rt:P 6':104,
                        'Alt Dsct Rt:S 7':105,
                        'Alt Dsct Rt:P 7':106,
                        'Alt Dsct Rt:S 8':107,
                        'Alt Dsct Rt:P 8':108,
                        'Alt Dsct Rt:S 9':109,
                        'Alt Dsct Rt:P 9':110,
                        'Alt Dsct Rt:S 10':111,
                        'Alt Dsct Rt:P 10':112,
                        'Product Special Flg':113,
                        'Country Of Origin':114,
                        'Discontinued on Date':115,
                        'Production Days Calc Opt':116,
                        'SO Suspension':117,
                        'Abolishment MSG':118,
                        'Product Group Code':119,
                        'BU Code':120,
                        'Qty / Order':121,
                        'Each Time QT':122,
                        'Product Delivery':123,
                        'Packing List Delivery':124,
                        'PO Format Div':125,
                        'SO Cancel Charge Rate':126,
                        '1st Day After SO Cancel Charge Rate':127,
                        '3rd Days After SO Cancel Charge Rate':128,
                        'Production LT for STOCK':129,
                        'Developed on Date':130,
                        'CSS Div':131,
                        'Pressure Div':132,
                        'Pressure Length':133,
                        'Tax Free Div':134,
                        'Dsct Rt :Sales':135,
                        'Dsct Rt :Purchase':136,
                        'Product LT of ExpZ':137,
                        'Supplier Code of ExpZ':138,
                        'Direct Ship (ref Check Mst)':139,
                        'Production Days Count':140,
                        'Reorder level Logic':141,
                        'MTO Calc':142,
                        'Period':143,
                        'Safety':144,
                        'Heavy Product':145,
                        'Expensive Product Div':146,
                        'Heavy Threshold':147,
                        'Expensive Threshold':148,
                        'Cutoff Time for Direct':149,
                        'Cutoff Time for 1day MTO':150,
                        'Limited MBO Product':151,
                        'Minimum Charge':152,
                        'Max Qty 1':153,
                        'Amount 1':154,
                        'Max Qty 2':155,
                        'Amount 2':156,
                        'Qty / Pack':157,
                        'Brand Code':158,
                        'Qty / Purchase':159,
                        'PO Product Code':160,
                        'Currency(Sales) Code':161,
                        'Currency(Purchase) Code':162,
                        'Purchase Mode':163,
                        'HS Code':164,
                        'Product Name':165,
                        'Native Product Name':166,
                        'IO Supply Means':167,
                        'IO Supply Means (URG)':168,
                        'Days to Ship on Catalog':169,
                        'Express T Production LT':170,
                        'Express T Days TS':171,
                        'Express A Days TS':172,
                        'Express B Days TS':173,
                        'Express C Days TS':174,
                        'Print Weight Unit':175,
                        'Days to Ship of ExpZ':176,
                        'Currency(Purchase of BO)':177,
                        'Purchase Mode of BO':178,
                        'Shipment Stop Div':179,
                        'Express A Direct Ship Flg':180,
                        'Express B Direct Ship Flg':181,
                        'Express C Direct Ship Flg':182,
                        'Express T Direct Ship Flg':183,
                        'Apply TI to Plant 1':184,
                        'Cutoff Time for TI to Plant 1':185,
                        'Apply TI to Plant 2':186,
                        'Cutoff Time for TI to Plant 2':187,
                        'Apply TI to Plant 3':188,
                        'Cutoff Time for TI to Plant 3':189,
                        'Apply TI to Plant 4':190,
                        'Cutoff Time for TI to Plant 4':191,
                        'Apply TI to Plant 5':192,
                        'Cutoff Time for TI to Plant 5':193,
                        'Apply TI to Plant 6':194,
                        'Cutoff Time for TI to Plant 6':195,
                        'Apply TI to Plant 7':196,
                        'Cutoff Time for TI to Plant 7':197,
                        'Apply TI to Plant 8':198,
                        'Cutoff Time for TI to Plant 8':199,
                        'Apply TI to Plant 9':200,
                        'Cutoff Time for TI to Plant 9':201,
                        'Distribution Flg':202,
                        'PO as STOCK':203,
                        'Remarks':204,
                        'Hazardous Product':205,
                        'GTI Apply':206,
                        'Message Mst to Imp Sub':207,
                        'Print Qty Unit':208,
                        'QC Product':209,
                        'Partial Delivery Threshold':210,
                        'Express L Calc Type for Sales':211,
                        'Express L Message Code':212,
                        'Express L Supplier Code':213,
                        'Express L Dsct Rt:S 1':214,
                        'Express L Dsct Rt:P 1':215,
                        'Express L Slide Days 1':216,
                        'Express L Dsct Rt:S 2':217,
                        'Express L Dsct Rt:P 2':218,
                        'Express L Slide Days 2':219,
                        'Express L Dsct Rt:S 3':220,
                        'Express L Dsct Rt:P 3':221,
                        'Express L Slide Days 3':222,
                        'Express L Dsct Rt:S 4':223,
                        'Express L Dsct Rt:P 4':224,
                        'Express L Slide Days 4':225,
                        'Express L Dsct Rt:S 5':226,
                        'Express L Dsct Rt:P 5':227,
                        'Express L Slide Days 5':228,
                        'Express L Dsct Rt:S 6':229,
                        'Express L Dsct Rt:P 6':230,
                        'Express L Slide Days 6':231,
                        'Express L Dsct Rt:S 7':232,
                        'Express L Dsct Rt:P 7':233,
                        'Express L Slide Days 7':234,
                        'Express L Dsct Rt:S 8':235,
                        'Express L Dsct Rt:P 8':236,
                        'Express L Slide Days 8':237,
                        'Express L Dsct Rt:S 9':238,
                        'Express L Dsct Rt:P 9':239,
                        'Express L Slide Days 9':240,
                        'Express L Dsct Rt:S 10':241,
                        'Express L Dsct Rt:P 10':242,
                        'Express L Slide Days 10':243})
    df = pd.DataFrame(columns=Header_product)
    return df

#if __name__ == '__main__':
#    Header()