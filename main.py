from utils.file_handler import read_sales_data
from utils.data_processor import (clean_data, calculate_total_revenue, calculate_metrics, region_wise_sales, 
 top_selling_products, customer_analysis, daily_sales_trend, find_peak_sales_day, low_performing_products, generate_report, validate_and_filter, generate_sales_report)
from utils.api_handler import fetch_all_products, get_currency_rate, create_product_mapping, enrich_sales_data, save_enriched_data

def main():
    print("=" * 40)
    print("        SALES ANALYTICS SYSTEM")
    print("=" * 40)

    try:
        # 1. Setup Paths
        input_file = "data/sales_data.txt"
        report_file = "output/summary_report.txt"
        
        # [1/10] Reading Data
        print("\n[1/10] Reading sales data...")
        raw_data = read_sales_data(input_file)
        print(f"✓ Successfully read {len(raw_data)} transactions")

        # [2/10] Cleaning Data
        print("\n[2/10] Parsing and cleaning data...")
        cleaned_data = clean_data(raw_data)
        total_rev = calculate_total_revenue(cleaned_data)
        print(f"✓ Parsed {len(cleaned_data)} records")
        print(f"Task 2.1 - Total Revenue: {total_rev}")

        # [3/10] Display Filter Options (User Interaction Requirement)
        print("\n[3/10] Filter Options Available:")
        available_regions = sorted(list(set(t['Region'] for t in cleaned_data)))
        amounts = [t['Quantity'] * t['UnitPrice'] for t in cleaned_data]
        print(f"Regions: {', '.join(available_regions)}")
        print(f"Amount Range: ${min(amounts):,.2f} - ${max(amounts):,.2f}")

        do_filter = input("\nDo you want to filter data? (y/n): ").lower().strip()
        
        # [4/10] Validation and Filtering
        print("\n[4/10] Validating transactions...")
        if do_filter == 'y':
            target_region = input(f"Enter Region to filter: ").strip()
            min_amt = float(input("Enter minimum amount (default 1000): ") or 1000)
            filtered_data, inv_count, summary = validate_and_filter(cleaned_data, region=target_region, min_amount=min_amt)
        else:
            # Matches your existing logic
            filtered_data, inv_count, summary = validate_and_filter(cleaned_data, min_amount=1000)
        print(f"✓ Valid: {len(filtered_data)} | Invalid: {inv_count}")

        # [5/10] Data Analyses (Running your Part 2 functions)
        print("\n[5/10] Analyzing sales data...")
        # (Your existing analysis calls)
        regions = region_wise_sales(cleaned_data)
        top_prods = top_selling_products(cleaned_data, n=3)
        customers = customer_analysis(cleaned_data)
        trend = daily_sales_trend(cleaned_data)
        peak = find_peak_sales_day(cleaned_data)
        low_prods = low_performing_products(cleaned_data, threshold=15)
        print("✓ Analysis complete")

        # [6/10] API Fetch
        print("\n[6/10] Fetching product data from API...")
        api_products = fetch_all_products()
        if api_products:
            print(f"✓ Fetched {len(api_products)} products")
            print(f"Sample Product from API: {api_products[0]}")
        
        # [7/10] Enrichment
        print("\n[7/10] Enriching sales data...")
        product_map = create_product_mapping(api_products)
        if product_map:
            print(f"Mapping Check (ID 1): {product_map.get(1)}")
        
        enriched_data = enrich_sales_data(cleaned_data, product_map)
        if enriched_data:
            match_count = sum(1 for t in enriched_data if t.get('API_Match'))
            print(f"✓ Enriched {match_count} transactions")
            print(f"Sample Enriched Record (Match={enriched_data[0]['API_Match']})")

        # [8/10] Saving Data
        print("\n[8/10] Saving enriched data...")
        save_enriched_data(enriched_data)
        print("✓ Saved to: data/enriched_sales_data.txt")

        # [9/10] Generating Final Report
        print("\n[9/10] Generating comprehensive report...")
        generate_sales_report(cleaned_data, enriched_data) 
        
        # [10/10] Final Analytics and Reporting
        print("\n[10/10] Finalizing Global Summary...")
        rate = get_currency_rate("USD", "EUR")
        rev_usd, qty = calculate_metrics(filtered_data)
        rev_eur = rev_usd * rate
        
        print(f"\n--- Final Global Summary ---")
        print(f"Total Revenue (USD): ${rev_usd:,.2f}")
        print(f"Total Revenue (EUR): €{rev_eur:,.2f} (at rate {rate})")
        
        generate_report(filtered_data, report_file)
        print("\n" + "=" * 40)
        print("✓ Process Complete! All reports generated.")
        print("=" * 40)

    except Exception as e:
        # Task 5.1 Error Handling Requirement
        print("\n" + "!" * 40)
        print(f"An error occurred during execution: {e}")
        print("!" * 40)

if __name__ == "__main__":
    main()