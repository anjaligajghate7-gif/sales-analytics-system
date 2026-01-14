import requests

def get_currency_rate(base="USD", target="EUR"):
    """
    Fetches real-time exchange rates using a public API.
    """
    url = f"https://api.exchangerate-api.com/v4/latest/{base}"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status() 
        data = response.json()
        
        rate = data['rates'].get(target)
        print(f"Successfully fetched exchange rate: 1 {base} = {rate} {target}")
        return rate
    except Exception as e:
        print(f"API Error fetching rate: {e}. Using fallback rate 0.85")
        return 0.85
    
def create_product_mapping(api_products):
    """
    Creates a mapping of product IDs to specific product info.
    Returns: dictionary mapping product IDs to info.
    """
    mapping = {}
    
    for product in api_products:
        # The 'id' becomes the key
        p_id = product.get('id')
        
        # The values are the requested metadata fields
        mapping[p_id] = {
            'title': product.get('title'),
            'category': product.get('category'),
            'brand': product.get('brand'),
            'rating': product.get('rating')
        }
    
    return mapping

def enrich_sales_data(transactions, product_mapping):
    """
    Enriches transaction data with API product information.
    """
    enriched_list = []

    for t in transactions:
        # Create a copy to avoid changing the original data
        enriched_t = t.copy()
        
        # 1. Extract numeric ID (P101 -> 101)
        # Requirement: Correctly extracts numeric IDs
        raw_pid = t.get('ProductID', '')
        try:
            # Removes 'P' and converts the rest to an integer
            numeric_id = int(raw_pid.replace('P', '').strip())
        except ValueError:
            numeric_id = None

        # 2. Enrich with API data
        # Requirement: Handles enrichment and missing products
        if numeric_id in product_mapping:
            info = product_mapping[numeric_id]
            enriched_t['API_Category'] = info.get('category')
            enriched_t['API_Brand'] = info.get('brand')
            enriched_t['API_Rating'] = info.get('rating')
            enriched_t['API_Match'] = True
        else:
            # Requirement: Handles Missing products
            enriched_t['API_Category'] = None
            enriched_t['API_Brand'] = None
            enriched_t['API_Rating'] = None
            enriched_t['API_Match'] = False
            
        enriched_list.append(enriched_t)

    return enriched_list

def save_enriched_data(enriched_transactions, filename='data/enriched_sales_data.txt'):
    """
    Saves enriched transactions back to a pipe-delimited file.
    """
    # Requirement: Include new columns in header
    header = "TransactionID|Date|ProductID|ProductName|Quantity|UnitPrice|CustomerID|Region|API_Category|API_Brand|API_Rating|API_Match\n"
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(header)
            for t in enriched_transactions:
                # Handle None values by converting them to empty strings
                line = [
                    str(t.get('TransactionID', '')),
                    str(t.get('Date', '')),
                    str(t.get('ProductID', '')),
                    str(t.get('ProductName', '')),
                    str(t.get('Quantity', 0)),
                    str(t.get('UnitPrice', 0.0)),
                    str(t.get('CustomerID', '')),
                    str(t.get('Region', '')),
                    str(t.get('API_Category') if t.get('API_Category') else ""),
                    str(t.get('API_Brand') if t.get('API_Brand') else ""),
                    str(t.get('API_Rating') if t.get('API_Rating') else ""),
                    str(t.get('API_Match', False))
                ]
                f.write("|".join(line) + "\n")
        print(f"Enriched data successfully saved to {filename}")
    except Exception as e:
        print(f"Error saving enriched data: {e}")
    
def fetch_all_products():
    """
    Fetches all products from DummyJSON API using limit=100.
    """
    url = "https://dummyjson.com/products?limit=100"
    
    try:
        # Attempt to get data from API
        response = requests.get(url, timeout=10)
        
        # Check if the request was successful (Status Code 200)
        response.raise_for_status()
        
        data = response.json()
        raw_products = data.get('products', [])
        
        # Format the products to match the Expected Output Format
        formatted_products = []
        for p in raw_products:
            formatted_products.append({
                'id': p.get('id'),
                'title': p.get('title'),
                'category': p.get('category'),
                'brand': p.get('brand'),
                'price': p.get('price'),
                'rating': p.get('rating')
            })
            
        print(f"Successfully fetched {len(formatted_products)} products from API.")
        return formatted_products

    except requests.exceptions.RequestException as e:
        # Proper error handling (Requirement)
        print(f"API Failure: Could not connect to DummyJSON. Error: {e}")
        return [] # Return empty list if API fails (Requirement)