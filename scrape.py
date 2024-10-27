from serpapi.google_search import GoogleSearch
from os import environ
from pandas import DataFrame

departure_codes = ['LAX', 'SFO', 'SNA']
destination_codes = ['CDG', 'ORY', 'FCO', 'FRA', 'BCN', 'GVA', 'DUS', 'MXP', 'LIS', 'MAD', 'MUC', 'VIE', 'ZRH', 'AMS', 'BRU', 'CPH', 'OSL', 'ARN', 'HEL', 'KEF', 'LHR']
departure_dates = ['2025-01-06', '2025-01-07', '2025-01-08']
return_dates = ['2025-01-18']

def get_flight_results(departure_code, destination_code, departure_date, return_date):

    params = {
    "api_key": environ["SERP_API"],
    "engine": "google_flights",
    "hl": "en",
    "gl": "us",
    "departure_id": departure_code,
    "arrival_id": destination_code,
    "outbound_date": departure_date,
    "return_date": return_date,
    "currency": "USD"
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    return results

def extract_flights(results: dict):
    flights = []
    url = results[0]['search_metadata']['google_flights_url']
    departure_airport = results[0]['search_parameters']['departure_id']
    arrival_airport = results[0]['search_parameters']['arrival_id']

    for flight in results[0]['best_flights']:
        flights.append({
            'price': flight['price'],
            'departure_airport': departure_airport,
            'arrival_airport': arrival_airport,
            'duration': flight['total_duration'],
            'url': url
        })

    return flights

def find_cheapest_flight(results: DataFrame):
    # print 5 cheapest flights and their destination
    cheapest_flights = results.sort_values('price')
    print(cheapest_flights[['price', 'departure_airport']][:5])
    return


def main():
    results = []
    for departure_code in departure_codes:
        for destination_code in destination_codes:
            for departure_date in departure_dates:
                for return_date in return_dates:
                    print(f"Searching for flights from {departure_code} to {destination_code} on {departure_date} and returning on {return_date}")
                    results.append(get_flight_results(departure_code, destination_code, departure_date, return_date))
                    extracted_flights = extract_flights(results)
                    if extracted_flights == 'fire':
                        return
                    results.append(extracted_flights)

    df = DataFrame(results)
    df.to_csv('flight_results.csv')

    find_cheapest_flight(df)

if __name__ == '__main__':
    main()