import re
import requests
from bs4 import BeautifulSoup
import time
from typing import Dict, List
from collections import defaultdict

def fetch_and_process_stamps(url):
    print(f"Attempting to fetch data from: {url}")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        print("Sending request...")
        response = requests.get(url, headers=headers, timeout=10)
        print(f"Response status code: {response.status_code}")

        if response.status_code != 200:
            print(f"Error: Received status code {response.status_code}")
            return

        print("Parsing HTML content...")
        soup = BeautifulSoup(response.text, 'html.parser')

        print(f"\nNumber of <span> tags found: {len(soup.find_all('span'))}")
        print("\nProcessing stamps...\n")

        # Year pattern to match stamps from 1800s to 1940
        year_pattern = r'18\d{2}|19[0-3]\d|1940'

        # Keywords to exclude (collections, covers, etc. - not individual stamps)
        exclude_keywords = [
            "CATALOGUE", "Booklets", "SPECIMEN", "cover", "Cover", "COVER",
            "Souvenir", "CINDERELLAS", "BANK NOTE", "POSTCARDS", "COVERS",
            "COINS", "Accum", "Range of", "approx.", "Annual", "Packs",
            "POSTAGE", "Face $", "sheets", "SHEETS", "Plate blocks",
            "Plate Blocks", "P.O.", "FIRST DAY", "FDC", "CANCELS",
            "POSTAL STATIONERY", "FIELDPOST", "FLIGHT", "Registration"
        ]

        # Countries to exclude
        exclude_countries = ["CANADA", "PRINCE EDWARD ISLAND", "NOVA SCOTIA", "GIBRALTAR", "BRITISH COLUMBIA"]

        # Dictionary to store results by country
        results: Dict[str, List[tuple]] = defaultdict(list)

        spans = soup.find_all('span')
        current_lot = None

        for span in spans:
            text = span.get_text().strip()

            # Check if this is a lot number (e.g., "11." or "123.")
            lot_match = re.match(r'^(\d{1,3})\.\s*$', text)
            if lot_match:
                current_lot = lot_match.group(1)
                continue

            # Skip if no current lot or text is too short
            if not current_lot or len(text) < 20:
                continue

            # Check if this looks like a stamp listing (starts with country name)
            country_match = re.match(r'^([A-Z][A-Z\s:\.&]+?)(?:\s+(?:Semi-Postals|Syncopated|Blocks|SEMI-OFFICIAL))?[\s\d]', text)
            if not country_match:
                continue

            country = country_match.group(1).strip().rstrip(':')

            # Fix multi-word country names (common philatelic entities)
            # Multi-word country names, longest match first per prefix
            multi_word_countries = [
                "BRITISH COLUMBIA",
                "BRITISH GUIANA",
                "BRITISH HONDURAS",
                "CAPE OF GOOD HOPE",
                "CAYMAN ISLANDS",
                "COOK ISLANDS",
                "COSTA RICA",
                "FALKLAND ISLANDS",
                "FEDERATED MALAY STATES",
                "GOLD COAST",
                "GREAT BRITAIN",
                "HONG KONG",
                "NEW BRUNSWICK",
                "NEW GUINEA",
                "NEW ZEALAND",
                "NORTH BORNEO",
                "NOVA SCOTIA",
                "ORANGE FREE STATE",
                "PAPUA NEW GUINEA",
                "PITCAIRN ISLANDS",
                "PRINCE EDWARD ISLAND",
                "SAN MARINO",
                "SIERRA LEONE",
                "SOLOMON ISLANDS",
                "SOUTH AFRICA",
                "SOUTH AUSTRALIA",
                "SOUTH WEST AFRICA",
                "STRAITS SETTLEMENTS",
                "TRINIDAD AND TOBAGO",
                "TURKS AND CAICOS",
                "UNITED STATES",
                "VIRGIN ISLANDS",
            ]

            # Try to match multi-word country names from the text
            text_upper = text.upper()
            for mw_country in multi_word_countries:
                if text_upper.startswith(mw_country):
                    country = mw_country
                    break

            # Skip excluded countries
            if country in exclude_countries:
                current_lot = None
                continue

            # Skip excluded items
            if any(keyword in text for keyword in exclude_keywords):
                current_lot = None
                continue

            # Check for year in valid range
            if not re.search(year_pattern, text):
                current_lot = None
                continue

            # Find stamp numbers (e.g., #55, #102, #168-82)
            stamp_numbers = re.findall(r'#(\d+[a-zA-Z]?(?:-\d+[a-zA-Z]?)?)', text)

            if stamp_numbers:
                clean_text = text.encode('ascii', 'replace').decode('ascii')
                for stamp_num in stamp_numbers:
                    results[country].append((current_lot, stamp_num, clean_text))
                    print(f"Lot #{current_lot}: {country} - Stamp #{stamp_num}")

            current_lot = None

        # Print results in a clean format
        if results:
            print("\n" + "="*80)
            print("STAMP AUCTION RESULTS")
            print("="*80 + "\n")
            
            for country in sorted(results.keys()):
                print(f"\n{country}:")
                print("-" * len(country) + "-\n")
                
                for auction_ref, stamp_num, description in sorted(results[country], key=lambda x: int(x[0])):
                    print(f"\nLot #{auction_ref}")
                    print(f"  Stamp #: {stamp_num}")
                    print(f"  Description: {description}")
                
            print("\n" + "="*80)
            print(f"Total countries: {len(results)}")
            print(f"Total stamps found: {sum(len(stamps) for stamps in results.values())}")
            print("="*80 + "\n")
        else:
            print("\nNo matching stamps found.")

    except requests.exceptions.Timeout:
        print("Error: The request timed out")
    except requests.exceptions.ConnectionError:
        print("Error: Failed to connect to the website")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

def main():
    url = "http://www.fvhstamps.com/WeeklyAuctions/FvhWA.htm"
    print("Starting stamp scraper...")
    start_time = time.time()
    
    try:
        fetch_and_process_stamps(url)
    except Exception as e:
        print(f"Fatal error: {e}")
    
    end_time = time.time()
    print(f"Script completed in {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    main() 