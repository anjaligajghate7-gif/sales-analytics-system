def clean_data(raw_lines):
    valid_records = []
    invalid_count = 0
    total_parsed = len(raw_lines)

    for line in raw_lines:
        parts = line.split('|') # Requirement: Split by pipe delimiter 
        
        if len(parts) < 8:
            invalid_count += 1
            continue

        tid, date, pid, pname, qty, price, cid, region = parts

        # Requirement: Handle commas in ProductNames and Numbers 
        pname = pname.replace(',', '')
        qty_str = qty.replace(',', '')
        price_str = price.replace(',', '')

        try:
            qty_val = int(qty_str)
            price_val = float(price_str.replace(',', '')) # Handle potential commas in prices 

            # Requirement: Validation Rules 
            if (tid.startswith('T') and # TransactionID must start with 'T'
                qty_val > 0 and          # Quantity > 0
                price_val > 0 and        # UnitPrice > 0
                cid.strip() != "" and    # Missing CustomerID -> Remove
                region.strip() != ""):   # Missing Region -> Remove
                
                # Matching the "Expected Output Format" from your screenshot
                valid_records.append({
                    'TransactionID': tid,
                    'Date': date,
                    'ProductID': pid,
                    'ProductName': pname,
                    'Quantity': qty_val,
                    'UnitPrice': price_val,
                    'CustomerID': cid,
                    'Region': region
                })
            else:
                invalid_count += 1
        except ValueError:
            invalid_count += 1

    # Required Validation Output 
    print(f"Total records parsed: {total_parsed}")
    print(f"Invalid records removed: {invalid_count}")
    print(f"Valid records after cleaning: {len(valid_records)}")
    
    return valid_records

def clean_data(raw_lines):
    valid_records = []
    invalid_count = 0
    total_parsed = len(raw_lines)

    for line in raw_lines:
        parts = line.split('|')
        if len(parts) < 8:
            invalid_count += 1
            continue

        tid, date, pid, pname, qty, price, cid, region = parts
        pname = pname.replace(',', '')
        qty_str = qty.replace(',', '')
        price_str = price.replace(',', '')

        try:
            qty_val = int(qty_str)
            price_val = float(price_str)

            if (tid.startswith('T') and qty_val > 0 and price_val > 0 and 
                cid.strip() != "" and region.strip() != ""):
                
                valid_records.append({
                    'TransactionID': tid,
                    'Date': date,
                    'ProductID': pid,
                    'ProductName': pname,
                    'Quantity': qty_val,
                    'UnitPrice': price_val,
                    'CustomerID': cid,
                    'Region': region
                })
            else:
                invalid_count += 1
        except ValueError:
            invalid_count += 1

    print(f"Total records parsed: {total_parsed}")
    print(f"Invalid records removed: {invalid_count}")
    print(f"Valid records after cleaning: {len(valid_records)}")
    return valid_records
def calculate_total_revenue(transactions):
    """
    Calculates total revenue from all transactions.
    
    Returns: float (total revenue)
    """
    total = 0.0
    for t in transactions:
        # Multiply Quantity by UnitPrice for each record
        total += float(t['Quantity']) * float(t['UnitPrice'])
    
    return float(total)
#Task 1.3: Data Validation and Filtering 
def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    valid_transactions = []
    invalid_count = 0
    total_input = len(transactions)
    filtered_by_region = 0
    filtered_by_amount = 0

    all_regions = sorted(list(set(t['Region'] for t in transactions)))
    amounts = [t['Quantity'] * t['UnitPrice'] for t in transactions]
    
    print("\n--- Data Validation & Filtering ---")
    print(f"Available Regions: {', '.join(all_regions)}")
    print(f"Transaction Amount Range: ${min(amounts):,.2f} to ${max(amounts):,.2f}")

    for t in transactions:
        # Strict validation prefixes required by Task 1.3
        is_valid = (
            t.get('TransactionID', '').startswith('T') and
            t.get('ProductID', '').startswith('P') and
            t.get('CustomerID', '').startswith('C')
        )

        if not is_valid:
            invalid_count += 1
            continue

        amount = t['Quantity'] * t['UnitPrice']

        if region and t['Region'] != region:
            filtered_by_region += 1
            continue
        
        if (min_amount is not None and amount < min_amount) or \
           (max_amount is not None and amount > max_amount):
            filtered_by_amount += 1
            continue

        valid_transactions.append(t)

    summary = {
        'total_input': total_input,
        'invalid': invalid_count,
        'filtered_by_region': filtered_by_region,
        'filtered_by_amount': filtered_by_amount,
        'final_count': len(valid_transactions)
    }
    return valid_transactions, invalid_count, summary

def calculate_metrics(cleaned_data):
    total_revenue = sum(item['Quantity'] * item['UnitPrice'] for item in cleaned_data)
    total_quantity = sum(item['Quantity'] for item in cleaned_data)
    print(f"Total Revenue: ${total_revenue:,.2f}")
    print(f"Total Items Sold: {total_quantity}")
    return total_revenue, total_quantity

#task 2.1 
# b) Region-wise Sales Analysis
def region_wise_sales(transactions):
    """
    Analyzes sales by region and calculates percentages.
    """
    overall_total = sum(t['Quantity'] * t['UnitPrice'] for t in transactions)
    region_stats = {}

    # 1. Aggregate data
    for t in transactions:
        reg = t['Region']
        sales = t['Quantity'] * t['UnitPrice']
        
        if reg not in region_stats:
            region_stats[reg] = {'total_sales': 0.0, 'transaction_count': 0}
        
        region_stats[reg]['total_sales'] += sales
        region_stats[reg]['transaction_count'] += 1

    # 2. Calculate percentages
    for reg in region_stats:
        total_reg_sales = region_stats[reg]['total_sales']
        region_stats[reg]['percentage'] = round((total_reg_sales / overall_total) * 100, 2)

    # 3. Sort by total_sales descending (Requirement)
    sorted_regions = dict(sorted(region_stats.items(), 
                                 key=lambda x: x[1]['total_sales'], 
                                 reverse=True))
    return sorted_regions

# c) Top Selling Products
def top_selling_products(transactions, n=5):
    """
    Finds top n products by total quantity sold.
    """
    product_data = {}

    # 1. Aggregate by ProductName
    for t in transactions:
        name = t['ProductName']
        qty = t['Quantity']
        rev = qty * t['UnitPrice']
        
        if name not in product_data:
            product_data[name] = {'qty': 0, 'rev': 0.0}
        
        product_data[name]['qty'] += qty
        product_data[name]['rev'] += rev

    # 2. Convert to list of tuples: (Name, TotalQty, TotalRev)
    product_list = [(name, data['qty'], data['rev']) for name, data in product_data.items()]

    # 3. Sort by TotalQuantity descending
    product_list.sort(key=lambda x: x[1], reverse=True)

    # 4. Return top n
    return product_list[:n]

# d) Customer Purchase Analysis
def customer_analysis(transactions):
    """
    Analyzes customer purchase patterns.
    """
    cust_stats = {}

    for t in transactions:
        cid = t['CustomerID']
        val = t['Quantity'] * t['UnitPrice']
        prod = t['ProductName']
        
        if cid not in cust_stats:
            cust_stats[cid] = {'total_spent': 0.0, 'purchase_count': 0, 'products': set()}
        
        cust_stats[cid]['total_spent'] += val
        cust_stats[cid]['purchase_count'] += 1
        cust_stats[cid]['products'].add(prod) # set() ensures uniqueness

    # Final calculations and formatting
    final_analysis = {}
    for cid, data in cust_stats.items():
        avg_val = data['total_spent'] / data['purchase_count']
        final_analysis[cid] = {
            'total_spent': round(data['total_spent'], 2),
            'purchase_count': data['purchase_count'],
            'avg_order_value': round(avg_val, 2),
            'products_bought': sorted(list(data['products'])) # Unique list
        }

    # Sort by total_spent descending
    sorted_customers = dict(sorted(final_analysis.items(), 
                                   key=lambda x: x[1]['total_spent'], 
                                   reverse=True))
    return sorted_customers
#Data-based Analysis
def daily_sales_trend(transactions):
    """
    Analyzes sales trends by date.
    Returns: dictionary sorted chronologically.
    """
    daily_stats = {}

    for t in transactions:
        date = t['Date']
        revenue = t['Quantity'] * t['UnitPrice']
        customer = t['CustomerID']

        if date not in daily_stats:
            # Initialize with a set for unique customers
            daily_stats[date] = {
                'revenue': 0.0,
                'transaction_count': 0,
                'customers': set() 
            }
        
        daily_stats[date]['revenue'] += revenue
        daily_stats[date]['transaction_count'] += 1
        daily_stats[date]['customers'].add(customer)

    # Format the final dictionary and calculate unique customer count
    formatted_trend = {}
    # Sorting keys (dates) chronologically
    for date in sorted(daily_stats.keys()):
        formatted_trend[date] = {
            'revenue': round(daily_stats[date]['revenue'], 2),
            'transaction_count': daily_stats[date]['transaction_count'],
            'unique_customers': len(daily_stats[date]['customers'])
        }

    return formatted_trend


def find_peak_sales_day(transactions):
    """
    Identifies the date with the highest revenue.
    Returns: tuple (date, revenue, transaction_count)
    """
    # Reuse our daily_sales_trend function to get the data
    trend = daily_sales_trend(transactions)
    
    if not trend:
        return None

    # Find the date with the maximum revenue
    peak_date = max(trend, key=lambda d: trend[d]['revenue'])
    peak_data = trend[peak_date]

    return (peak_date, peak_data['revenue'], peak_data['transaction_count'])
#Task2.3: Product Performance
def low_performing_products(transactions, threshold=10):
    """
    Identifies products with total quantity sold below the threshold.
    Returns: list of tuples (ProductName, TotalQuantity, TotalRevenue)
    """
    product_totals = {}

    # 1. Aggregate totals for all products
    for t in transactions:
        name = t['ProductName']
        qty = t['Quantity']
        rev = qty * t['UnitPrice']
        
        if name not in product_totals:
            product_totals[name] = {'qty': 0, 'rev': 0.0}
        
        product_totals[name]['qty'] += qty
        product_totals[name]['rev'] += rev

    # 2. Filter by threshold and convert to list of tuples
    low_performers = []
    for name, data in product_totals.items():
        if data['qty'] < threshold:
            low_performers.append((name, data['qty'], data['rev']))

    # 3. Sort by TotalQuantity ascending (Requirement)
    low_performers.sort(key=lambda x: x[1])

    return low_performers

def generate_report(cleaned_data, output_path):
    region_sales = {}
    for record in cleaned_data:
        region = record["Region"]
        revenue = record["Quantity"] * record["UnitPrice"]
        region_sales[region] = region_sales.get(region, 0) + revenue
    with open(output_path, 'w') as f:
        f.write("SALES ANALYTICS REPORT\n======================\n\n")
        for region, total in region_sales.items():
            f.write(f"Region: {region:10} | Total Revenue: ${total:,.2f}\n")
    print(f"Report successfully generated at: {output_path}")

from datetime import datetime

def generate_sales_report(transactions, enriched_transactions, output_file='output/sales_report.txt'):
    """
    Generates a comprehensive formatted text report combining all analytics.
    """
    # 1. Pre-calculate data using your existing functions
    total_rev = sum(t['Quantity'] * t['UnitPrice'] for t in transactions)
    total_txns = len(transactions)
    avg_order = total_rev / total_txns if total_txns > 0 else 0
    dates = sorted([t['Date'] for t in transactions])
    date_range = f"{dates[0]} to {dates[-1]}" if dates else "N/A"

    # Get data from your Task 2 functions
    from utils.data_processor import (region_wise_sales, top_selling_products, 
                                    customer_analysis, daily_sales_trend, 
                                    find_peak_sales_day, low_performing_products)
    
    reg_perf = region_wise_sales(transactions)
    top_5_prods = top_selling_products(transactions, n=5)
    cust_perf = customer_analysis(transactions)
    daily_trend = daily_sales_trend(transactions)
    peak_day = find_peak_sales_day(transactions)
    low_prods = low_performing_products(transactions, threshold=15)

    # API Summary calculations
    enriched_count = sum(1 for t in enriched_transactions if t.get('API_Match'))
    success_rate = (enriched_count / len(enriched_transactions) * 100) if enriched_transactions else 0
    failed_pids = sorted(list(set(t['ProductID'] for t in enriched_transactions if not t.get('API_Match'))))

    with open(output_file, 'w', encoding='utf-8') as f:
        # SECTION 1: HEADER
        f.write("=" * 60 + "\n")
        f.write(" " * 15 + "SALES ANALYTICS REPORT\n")
        f.write(f" " * 10 + f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f" " * 10 + f"Records Processed: {total_txns}\n")
        f.write("=" * 60 + "\n\n")

        # SECTION 2: OVERALL SUMMARY
        f.write("OVERALL SUMMARY\n" + "-" * 60 + "\n")
        f.write(f"Total Revenue:       ${total_rev:,.2f}\n")
        f.write(f"Total Transactions:  {total_txns}\n")
        f.write(f"Average Order Value: ${avg_order:,.2f}\n")
        f.write(f"Date Range:          {date_range}\n\n")

        # SECTION 3: REGION-WISE PERFORMANCE
        f.write("REGION-WISE PERFORMANCE\n" + "-" * 60 + "\n")
        f.write(f"{'Region':<15} {'Sales':<15} {'% Total':<12} {'Transactions':<12}\n")
        for reg, stats in reg_perf.items():
            f.write(f"{reg:<15} ${stats['total_sales']:<14,.2f} {stats['percentage']:<11}% {stats['transaction_count']:<12}\n")
        f.write("\n")

        # SECTION 4: TOP 5 PRODUCTS
        f.write("TOP 5 PRODUCTS\n" + "-" * 60 + "\n")
        f.write(f"{'Rank':<6} {'Product Name':<20} {'Qty':<10} {'Revenue':<15}\n")
        for i, (name, qty, rev) in enumerate(top_5_prods, 1):
            f.write(f"{i:<6} {name:<20} {qty:<10} ${rev:<14,.2f}\n")
        f.write("\n")

        # SECTION 5: TOP 5 CUSTOMERS
        f.write("TOP 5 CUSTOMERS\n" + "-" * 60 + "\n")
        f.write(f"{'Rank':<6} {'Customer ID':<15} {'Total Spent':<15} {'Order Count':<12}\n")
        top_5_custs = list(cust_perf.items())[:5]
        for i, (cid, stats) in enumerate(top_5_custs, 1):
            f.write(f"{i:<6} {cid:<15} ${stats['total_spent']:<14,.2f} {stats['purchase_count']:<12}\n")
        f.write("\n")

        # SECTION 6: DAILY SALES TREND
        f.write("DAILY SALES TREND\n" + "-" * 60 + "\n")
        f.write(f"{'Date':<15} {'Revenue':<15} {'Txns':<10} {'Unique Cust':<12}\n")
        for date, stats in list(daily_trend.items())[:10]: # Showing first 10 days for brevity
            f.write(f"{date:<15} ${stats['revenue']:<14,.2f} {stats['transaction_count']:<10} {stats['unique_customers']:<12}\n")
        f.write("\n")

        # SECTION 7: PRODUCT PERFORMANCE ANALYSIS
        f.write("PRODUCT PERFORMANCE ANALYSIS\n" + "-" * 60 + "\n")
        f.write(f"Peak Sales Day: {peak_day[0]} (${peak_day[1]:,.2f} with {peak_day[2]} txns)\n")
        f.write("Low Performing Products (Qty < 15):\n")
        for p in low_prods:
            f.write(f" - {p[0]} ({p[1]} sold)\n")
        f.write("\n")

        # SECTION 8: API ENRICHMENT SUMMARY
        f.write("API ENRICHMENT SUMMARY\n" + "-" * 60 + "\n")
        f.write(f"Total Products Enriched: {enriched_count}\n")
        f.write(f"Success Rate:            {success_rate:.2f}%\n")
        f.write(f"Failed Product IDs:      {', '.join(failed_pids) if failed_pids else 'None'}\n")
        f.write("=" * 60 + "\n")

    print(f"Comprehensive report generated at: {output_file}")
