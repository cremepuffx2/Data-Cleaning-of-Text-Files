import re
import os
from pathlib import Path

def remove_page_numbers(text):
    # Define the regex pattern to match lines with only page numbers (1 to 3 digits)
    page_number_pattern = re.compile(r'^\d{1,3}$', re.MULTILINE)

    # Remove the lines with page numbers
    cleaned_text = page_number_pattern.sub('', text)
    return cleaned_text

def remove_footers_from_doc(text):
    '''
    This function removes the footers from the text file. Lines that appear directly above and below a line containing only digits
    are footers, and any line containing the word "Annual Report" is considered a footer. Hence, the regex pattern identifies these
    lines and removes them from the text file.
    '''
    
    # Pattern to match lines containing "Annual Report"
    footers_pattern1 = re.compile(r'^.*annual report.*$', re.IGNORECASE | re.MULTILINE)
    cleaned_text = footers_pattern1.sub('', text)

    # Pattern to match lines directly above and below a line containing only digits
    footers_pattern2 = re.compile(r'(^.*\n)?(^\d{1,3})(\n.*)?', re.MULTILINE)

    def replace_match(match):
        before = match.group(1) if match.group(1) else ""
        digits = match.group(2) if match.group(2) else ""
        after = match.group(3) if match.group(3) else ""

        # If there's a line before and after, remove all three lines
        if before and after:
            return ""
        # If only digits line found, remove it
        elif digits:
            return ""
        # Otherwise, return the original match
        else:
            return match.group(0)

    cleaned_text = footers_pattern2.sub(replace_match, cleaned_text)
    return cleaned_text

def remove_headers(text):
    '''
    This function removes the headers from the text file. There is a master list of common words that can be found in the content page
    of a report, which are also the headers. The function then matches words found in the text file based on the regex pattern, and performs
    a secondary check by checking if the words found are also found in this master list. Again, this function is not perfect as it will 
    remove the content page as well.
    '''
     common_words_in_reports = [
    "ABSTRACT", "ACCOUNT", "ACCOUNTING", "ACCOUNTS", "ACCRUAL", "ACQUISITION", 
    "ADMINISTRATION", "ANALYSIS", "ANNUAL", "APPENDIX", "APPLICATION", "ASSETS", 
    "ASSUMPTIONS", "AUDIT", "AUDITOR", "BALANCE", "BANK", "BENEFIT", "BENEFITS", 
    "BOARD", "BUDGET", "BUSINESS", "CASH", "CHANGES", "CHARTER", "CLOSING", 
    "COMMISSION", "COMMITTEE", "COMMUNICATION", "COMPANY", "COMPLIANCE", 
    "COMPONENTS", "CONCLUSION", "CONSOLIDATED", "CONSULTING", "CONTENTS", 
    "CONTRACT", "CONTRACTS", "CONTRIBUTION", "CONTRIBUTIONS", "CONTROL", 
    "CORPORATE", "COST", "COSTS", "CREDIT", "CREATE", "CAPITALISE","CONNECT","CURRENCY", "CURRENT", "DATE", 
    "DEBT", "DECLARATION", "DEPRECIATION", "DERIVATIVE", "DESCRIPTION", 
    "DETAILS", "DEVELOPMENT", "DIRECTORS", "DIVIDEND", "DIVIDENDS", "EARNINGS", 
    "ECONOMIC", "EQUITY", "EXPENDITURE", "EXPENSE", "EXPENSES", "EXPORT", 
    "EXPOSURE", "EXTENSIONS", "FACILITIES", "FEE", "FEES", "FINANCE", 
    "FINANCIAL", "FISCAL", "FLOW", "FORECAST", "FOREIGN", "FUND", "FUNDS", 
    "GAINS", "GENERAL", "GOVERNANCE", "GOVERNMENT", "GROWTH", "IMPAIRMENT", 
    "INCOME", "INDEPENDENT", "INDEX", "INDICATORS", "INDUSTRY", "INFLATION", 
    "INFORMATION", "INITIATIVE", "INITIATIVES", "INNOVATION", "INSIGHT", 
    "INSIGHTS", "INSTITUTION", "INSURANCE", "INTEREST", "INTERNAL", 
    "INTERNATIONAL", "INVESTMENT", "INVESTMENTS", "INVESTOR", "INVESTORS", 
    "ITEM", "ITEMS", "JOURNAL", "LIABILITIES", "LIABILITY", "LIQUIDITY", 
    "LOSS", "LOSSES", "MANAGEMENT", "MANAGER", "MARKET", "MEASURES", "MERGER", 
    "MISSION", "MONTH", "NARRATIVE", "NET", "NOTE", "NOTES", "OBJECTIVE", 
    "OBJECTIVES", "OPERATIONS", "OPERATIONAL", "OPINION", "OUTCOME", "OUTCOMES", 
    "OUTLOOK", "OVERVIEW", "OWNERSHIP", "PAGE", "PAGES", "PARTNERSHIP", 
    "PAYABLE", "PAYOUT", "PERFORMANCE", "PERIOD", "PLAN", "PLANNING", "POLICY", 
    "PORTFOLIO", "POSITION", "POTENTIAL", "PRACTICES", "PRELIMINARY", "PREMIUM", 
    "PRESENTATION", "PRICE", "PRINCIPAL", "PRINCIPLES", "PROCEDURE", 
    "PROCEDURES", "PROFIT", "PROFITS","PROFILE", "PROJECTION", "PROJECTIONS", "PROPERTY", 
    "PROPOSAL", "PROSPECTS", "PROVISION", "PURCHASE", "PURCHASING", "QUARTER", 
    "QUARTERLY", "RATIO", "RECEIVABLES", "RECOMMENDATION", "RECOMMENDATIONS", 
    "RECONCILIATION", "RECOVERY", "REDUCTION", "REGULATION", "REGULATIONS", 
    "RELATIONSHIP", "REPORT", "REPORTING", "REQUIREMENT", "REQUIREMENTS", 
    "RESERVE", "RESERVES", "RESOLUTION", "RESOURCE", "RESOURCES", "RESULT", 
    "RESULTS", "RESTRUCTURING", "RETAINED", "REVENUE", "REVIEW", "RISK", 
    "RISKS", "SALES", "SCHEDULE", "SECTOR", "SEGMENT", "SHEET", "SHARE", 
    "SHAREHOLDER", "SHAREHOLDERS", "SHARES", "SIGNIFICANT", "SOLUTIONS", 
    "SPECIFIC", "STATEMENT", "STATEMENTS", "STATISTICS", "STRATEGIC", 
    "STRATEGY", "STRUCTURE", "SUBSIDIARIES", "SUMMARY", "SUPPLEMENTARY", 
    "SUPPORT", "SURPLUS", "SUSTAINABILITY", "TAX", "TAXES", "TERM", "TERMS", 
    "TOTAL", "TRANSACTION", "TRANSACTIONS", "TREASURY", "TREND", "TRENDS", 
    "VALUE", "VARIANCE", "VISION", "VOLUME", "WARRANTY", "YEAR", "YIELD"] 

    # Define helper function "is_common_word" to recognize if the headers are found in a common list of words and not a name
    def is_common_word(word):
        return word.upper() in common_words_in_reports

    headers_pattern = re.compile(r'^[A-Z][a-z]*\s*|[A-Z\s]*$')
    lines = text.split('\n')
    filtered_lines = []

    for line in lines:
        if headers_pattern.match(line):
            # Check if the words in the line are common financial words
            words = line.split()
            if all(is_common_word(word) for word in words):
                continue  # Skip this line
        filtered_lines.append(line)
    cleaned_text = '\n'.join(filtered_lines).strip()
    cleaned_text = cleaned_text.lower()
    return cleaned_text

def process_parsed_files(input_folder, output_folder):
    """
    This function processes all text files in the input_folder, applies custom processing functions,
    and saves the processed files to the output_folder with the same name.
    """
    # Ensure the output directory exists
    os.makedirs(output_folder, exist_ok=True)

    # Loop through all files in the input_folder
    for filename in os.listdir(input_folder):
        file_path = os.path.join(input_folder, filename)
        
        # Check if the file is a text file
        if os.path.isfile(file_path) and filename.endswith('.txt'):
            # Read the content of the file
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                content = file.read()
            
            # Apply your custom processing functions
            processed_content = remove_page_numbers(content)
            processed_content = remove_footers_from_doc(processed_content)
            processed_content = remove_headers(processed_content)
            
            # Define the output path
            output_path = os.path.join(output_folder, filename)
            
            # Save the processed content to the output folder
            with open(output_path, 'w', encoding='utf-8') as file:
                file.write(processed_content)   