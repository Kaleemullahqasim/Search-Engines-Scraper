import time
import random
from tqdm import tqdm
from search_engines import Google
from search_engines import Bing
from search_engines import Yahoo
from concurrent.futures import ThreadPoolExecutor

# Function to handle the search and write results to a file
def search_and_write(query, output_file, max_retries=5, current_retry=0):
    try:
        time.sleep(5)
        engine = Google()
        results = engine.search(query)
        links = results.links()

        engine = Bing()
        time.sleep(5)
        results = engine.search(query)
        links += results.links()

        engine = Yahoo()
        time.sleep(5)
        results = engine.search(query)
        links += results.links()
        

        with open(output_file, 'a') as f:
            for link in links:
                f.write(link + '\n')

    except Exception as e:
        if current_retry < max_retries:
            print(f"An error occurred: {e}. Retrying ({current_retry + 1}/{max_retries})...")
            time.sleep(random.randint(1, 10))  # Delay for a random time between 1 and 10 seconds
            search_and_write(query, output_file, max_retries, current_retry + 1)  # Retry the same query
        else:
            print(f"An error occurred: {e}. Maximum retries reached. Skipping this query.")

# Read the queries from the input file
with open('/Users/kaleemullahqasim/Desktop/Website Intention Classification/dork/products/product.txt', 'r') as f:
    queries = f.readlines()

# Process each query
with ThreadPoolExecutor(max_workers=2) as executor:
    for query in tqdm(queries, desc="Processing queries"):
        query = query.strip()  # Remove newline characters
        executor.submit(search_and_write, query, '/Users/kaleemullahqasim/Desktop/Website Intention Classification/dork/products/product-results.txt')
