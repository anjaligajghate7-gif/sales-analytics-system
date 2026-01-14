# Sales Analytics & Data Enrichment System

A comprehensive Python-based data engineering pipeline that analyzes raw sales data, interfaces with external REST APIs for instantaneous product enrichment, and produces expert executive reports.

## 📊 Project Summary
This system manages the sales data processing process automatically:
1. **Reading:** Reads text files in a variety of encodings (CP1252, Latin-1, and UTF-8).
2. **Cleaning:** It eliminates corrupted data records and confirms data integrity based on specific prefix criteria (T, P, and C).
3. **Analytics:** Performs complex analysis at the customer, item, and local scales, involving sales patterns and high-performance days.
4. **Enrichment:** Interfaces to the DummyJSON API to obtain current item information and offers real-time exchange rates (USD to EUR).
5. **Reporting:** Generates an organized pipe-limited enhanced dataset and a highly formatted narrative summary.

---

## 📁 Project Structure
```text
sales-analytics-system/
├── data/
│   ├── sales_data.txt            # Raw input data
│   └── enriched_sales_data.txt   # Output: API-enriched data
├── utils/
│   ├── __init__.py               # Makes utils a Python package
│   ├── file_handler.py           # File I/O and encoding logic
│   ├── data_processor.py         # Business logic and analytics
│   └── api_handler.py            # REST API integration logic
├── output/
│   ├── summary_report.txt        # Basic filtered report
│   └── sales_report.txt          # Final comprehensive executive report
├── main.py                       # Application entry point
├── requirements.txt              # Project dependencies (requests)
└── README.md                     # Documentation

🛠️ Installation & Setup
1. Prerequisites
Python 3.8 or higher installed.

Internet connection (required for API integration tasks).

2. Install Dependencies
Open your terminal in the project folder and run:

Bash
pip install -r requirements.txt

🚀 How to Run
Execute the main script from the root directory:

Bash
python main.py

User Interaction Flow:

Initialization: The system displays the "SALES ANALYTICS SYSTEM" header.

Data Loading: Automatically detects and reads the sales file using robust encoding detection.

Filter Prompt: The system displays available regions and amount ranges found in the data.

Type 'y' to apply a specific region/price filter.
OR
Type 'n' to process all valid data.

API Integration: The system determines exchange rates for each currency by retrieving 100 products from dummyjson.com.

Data Enrichment: To extract Category, Brand, and Rating data, Local Product IDs (such as P101) are mapped to API IDs (101).

Finalization: The /output and /data folders contain all generated reports.

📈 Key Features & Logic Encoding Resilience: Avoids "UnicodeDecodeError" by handling various file types.

Advanced Mapping: For optimal performance, map API data to local transactions using dictionary-based O(1) lookup.

Enrichment Logic: Applies logic to deal with "Missing Products" by naturally filling in empty values while setting API_Match to False.

Formatted Reporting: To ensure that the tables are precisely positioned for text-based reading, the final analysis uses exact f-string padding.

Error Handling: To avoid system failures and offer user-friendly feedback, every pipeline operation is enclosed in an international try-except block.

📝 Evaluation Checklist
 Part 1: File Encodings & Cleaning

 Part 2: Data Processing & Summary Calculations

 Part 3: API Integration & Data Enrichment

 Part 4: Comprehensive Text Reporting

 Part 5: Main Execution Flow & User Interaction