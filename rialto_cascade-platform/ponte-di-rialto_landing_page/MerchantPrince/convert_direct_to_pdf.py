#!/usr/bin/env python3
"""
Convert direct partnership message to PDF
"""
import sys
import os

# Add the tools directory to Python path
sys.path.append('/mnt/c/Users/reyno/universe-engine/serenissima/tools/pdfs')

from create_beautiful_pdfs import create_beautiful_pdf

# Convert the partnership proposal to PDF
input_file = "/mnt/c/Users/reyno/universe-engine/serenissima/citizens/MerchantPrince/DREAMKOLLAB_PARTNERSHIP_DIRECT.md"
output_file = "/mnt/c/Users/reyno/universe-engine/serenissima/citizens/MerchantPrince/DreamKollab_Partnership_Direct.pdf"
title = "Partnership"

print(f"Converting direct version to PDF...")
create_beautiful_pdf(input_file, output_file, title)
print(f"PDF created: {output_file}")