from search_engines import Google
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
            engine = Google()
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
    file_path = '/Users/kaleemullahqasim/Desktop/YouTube Project Data/dorks/4/selected_domains_range_500000_1000000.txt'
    # Output file for the results
    output_file = '/Users/kaleemullahqasim/Desktop/YouTube Project Data/dorks/4/data/500000_1000000.json'

    # Read queries
    queries = read_queries(file_path)

    # Using ThreadPoolExecutor to manage threads
    with ThreadPoolExecutor(max_workers=60) as executor:
        list(tqdm(executor.map(search_query, queries, [output_file] * len(queries)), total=len(queries), desc="Processing queries"))

    print("All queries processed successfully.")

if __name__ == "__main__":
    main()
