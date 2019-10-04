# Master Header 並び順
# Unit Price Master

import pandas as pd

def Header():
    Header_product = ({'Process Mode': 1,
                       'Master ID': 2,
                       'Subsidiary Code': 3,
                       'Inner Code': 4,
                       'Product Code': 5,
                       'Purchase Unit Price Currency Code ': 6,
                       'Supplier Code': 7,
                       'Min.Val.1': 8,
                       'Min.Val.2': 9,
                       'Min.Val.3': 10,
                       'Min.Val.4': 11,
                       'Min.Val.5': 12,
                       'Cost Ratio': 13,
                       'Plate Flag': 14,
                       'Slide Sales Unit Price 1': 15,
                       'Slide Purchase Unit Price 1': 16,
                       'Slide Sales Unit Price 2': 17,
                       'Slide Purchase Unit Price 2': 18,
                       'Slide Sales Unit Price 3': 19,
                       'Slide Purchase Unit Price 3': 20,
                       'Slide Sales Unit Price 4': 21,
                       'Slide Purchase Unit Price 4': 22,
                       'Slide Sales Unit Price 5': 23,
                       'Slide Purchase Unit Price 5': 24,
                       'Slide Sales Unit Price 6': 25,
                       'Slide Purchase Unit Price 6': 26,
                       'Slide Sales Unit Price 7': 27,
                       'Slide Purchase Unit Price 7': 28,
                       'Slide Sales Unit Price 8': 29,
                       'Slide Purchase Unit Price 8': 30,
                       'Slide Sales Unit Price 9': 31,
                       'Slide Purchase Unit Price 9': 32,
                       'Slide Sales Unit Price 10': 33,
                       'Slide Purchase Unit Price 10': 34,
                       'Position 1': 35,
                       'Position 2': 36,
                       'Position 3': 37,
                       'Position 4': 38,
                       'Position 5': 39,
                       'Rounding Place': 40,
                       'Rounding Method': 41})
    df = pd.DataFrame(columns=Header_product)
    return df