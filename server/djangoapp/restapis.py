import requests
import json
from .models import CarDealer, DealerReview
# import related models here
from requests.auth import HTTPBasicAuth
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions


def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    apiKey = kwargs.get('api_key')
    try:
        # Call get method of requests library with URL and parameters
        if apiKey:
            # Basic authentication GET
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('apikey', apiKey),
                                    params=kwargs)
        else:
            # no authentication GET
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)

        print("With status {} ".format(response.status_code))
        json_data = json.loads(response.text)
        return json_data
    except:
        # If any error occurs
        print("Network exception occurred")


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)

def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["rows"]

        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"],
                                   full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   state=dealer_doc["state"], zip=dealer_doc["zip"])
            results.append(dealer_obj)
    return results


def get_dealer_by_id(url, dealerId):
    results = []
    json_result = get_request(url + "?id=" + dealerId)
    if json_result:
        dealers = json_result["docs"]

        # For each dealer object
        for dealer_doc in dealers:
            # Get its content in `doc` object
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"],
                                   full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)
    return results


def get_dealer_reviews_from_cf(url, dealerId):
    reviews = []
    json_result = get_request(url + "?dealerId=" + str(dealerId))

    for review in json_result['docs']:
        # Use Watson NLU to determine sentiment
        # Replace the following line with Watson NLU code
        sentiment = analyze_review_sentiments(review['review'])

        dealer_review = DealerReview(review['dealership'],
                                     review['name'],
                                     review['purchase'],
                                     review['review'],
                                     review['purchase_date'],
                                     review['car_make'],
                                     review['car_model'],
                                     review['car_year'],
                                     sentiment['document']['label'],
                                     review['id']
                                     )

        reviews.append(dealer_review)
    return reviews


def analyze_review_sentiments(dealerreview):
    authenticator = IAMAuthenticator('c2N0GM1OkMSa3eNsqrwCxDnnI4OM9klXQjavkqO_2uYK')
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2022-04-07',
        authenticator=authenticator
    )

    natural_language_understanding.set_service_url(
        'https://api.au-syd.natural-language-understanding.watson.cloud.ibm.com/instances/6654a5e9-b78f-4f4e-aa50-8dc422e46f1e')

    result = natural_language_understanding.analyze(
        text=dealerreview,
        features=Features(sentiment=SentimentOptions())).get_result()

    return result['sentiment']


def post_request(url, json_payload, **kwargs):
    response = requests.post(url, json=json_payload, **kwargs)
    # Handle the response here
    return response
