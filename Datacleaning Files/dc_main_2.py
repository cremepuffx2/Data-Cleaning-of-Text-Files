import os
from pathlib import Path
import dc_functions as dcf
import time
import re

input_folder = r"C:\Users\somes\OneDrive\Desktop\NLP Project\DataCleaning\NLP-SMU-Parsing-with-the-boys\Phase 1.2 PDF parsing\Output"
output_folder = r"C:\Users\somes\OneDrive\Desktop\NLP Project\DataCleaning\NLP-SMU-Parsing-with-the-boys\Phase 1.2 PDF parsing\cleaned_text_files"

if __name__ == "__main__":
    start_time = time.time()
    dcf.process_parsed_files(input_folder, output_folder)
    end_time = time.time()

    # Calculate and print execution time
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time:.2f} seconds")

    print("Processing of parsed files completed.")