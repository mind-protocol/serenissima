#!/usr/bin/env python3
"""
Convert Deite partnership value proposition to PDF
"""
import sys
import os

# Add the tools directory to Python path
sys.path.append('/mnt/c/Users/reyno/universe-engine/serenissima/tools/pdfs')

from create_beautiful_pdfs import create_beautiful_pdf

# Convert the partnership proposal to PDF
input_file = "/mnt/c/Users/reyno/universe-engine/serenissima/citizens/MerchantPrince/DEITE_PARTNERSHIP_VALUE.md"
output_file = "/mnt/c/Users/reyno/universe-engine/serenissima/citizens/MerchantPrince/Deite_Partnership_Value.pdf"
title = "Real Value for Deite"

print(f"Converting Deite value proposition to PDF...")
create_beautiful_pdf(input_file, output_file, title)
print(f"PDF created: {output_file}")