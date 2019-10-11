# Master Header 並び順
# Unit Price Product Master

import pandas as pd

def type():
    type_p =({'Process Mode': str,
            'Master ID': str,
            'Subsidiary Code': str,
            'Inner Code': str,
            'Product Code': str,
            'Purchase Unit Price Currency Code ': str,
            'Supplier Code': str,
            'Min.Val.1': float,
            'Min.Val.2': float,
            'Min.Val.3': float,
            'Min.Val.4': float,
            'Min.Val.5': float,
            'Cost Ratio': float,
            'Plate Flag': str,
            'Slide Sales Unit Price 1': float,
            'Slide Purchase Unit Price 1': float,
            'Slide Sales Unit Price 2': float,
            'Slide Purchase Unit Price 2': float,
            'Slide Sales Unit Price 3': float,
            'Slide Purchase Unit Price 3': float,
            'Slide Sales Unit Price 4': float,
            'Slide Purchase Unit Price 4': float,
            'Slide Sales Unit Price 5': float,
            'Slide Purchase Unit Price 5': float,
            'Slide Sales Unit Price 6': float,
            'Slide Purchase Unit Price 6': float,
            'Slide Sales Unit Price 7': float,
            'Slide Purchase Unit Price 7': float,
            'Slide Sales Unit Price 8': float,
            'Slide Purchase Unit Price 8': float,
            'Slide Sales Unit Price 9': float,
            'Slide Purchase Unit Price 9': float,
            'Slide Sales Unit Price 10': float,
            'Slide Purchase Unit Price 10': float,
            'Position 1': float,
            'Position 2': float,
            'Position 3': float,
            'Position 4': float,
            'Position 5': float,
            'Rounding Place': str,
            'Rounding Method': str})
    return type_p
if __name__ == "__main__":
    print(type())
