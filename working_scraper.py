from search_engines import Google , yahoo, bing
from tqdm import tqdm
import threading
import time
import json
from concurrent.futures import ThreadPoolExecutor

def read_queries(file_path):
    with open(file_path, 'r') as file:
        queries = [line.strip() for line in file]
    return queries

def search_query(query, output_file):
    retries = 3
    backoff_time = 3

    while retries > 0:
        try:
            # Adding a delay to avoid rate-limiting
            time.sleep(1)
            engine = bing()
            results = engine.search(query)
            links = results.links()

            if not links:
                print(f"Warning: No results found for query '{query}'.")
                return

            with open(output_file, 'a') as file:
                json.dump({query: links}, file)
                file.write('\n')

            break
        except Exception as e:
            print(f"Error occurred for query '{query}': {e}. Retrying...")
            retries -= 1
            time.sleep(backoff_time)
            backoff_time *= 2

def main():
    # File containing queries
    file_path = '/Users/kaleemullahqasim/Desktop/Website Intention Classification/dork/products/product.txt'
    # Output file for the results
    output_file = '/Users/kaleemullahqasim/Desktop/Website Intention Classification/dork/products/product-results.json'

    # Read queries
    queries = read_queries(file_path)

    # Using ThreadPoolExecutor to manage threads
    with ThreadPoolExecutor(max_workers=2) as executor:
        list(tqdm(executor.map(search_query, queries, [output_file] * len(queries)), total=len(queries), desc="Processing queries"))

    print("All queries processed successfully.")

if __name__ == "__main__":
    main()
