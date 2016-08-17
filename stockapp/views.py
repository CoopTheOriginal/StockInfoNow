from flask import Blueprint, flash, render_template
import json, os, requests, sys


stockapp = Blueprint("stockapp", __name__)
API_KEY = os.environ['API_KEY']

def flash_errors(form, category="warning"):
    '''Flash all errors for a form.'''
    for field, errors in form.errors.items():
        for error in errors:
            flash("{0} - {1}"
                    .format(getattr(form, field).label.text, error), category)


@stockapp.route("/<ticker>")
def index(ticker):
    print(ticker)
    ticker = ticker.upper()
    ticker_dict = get_ticker_info(ticker)
    return render_template('index.html', ticker_dict=ticker_dict)


def get_ticker_info(ticker):
    """Takes in a stock ticker string and returns a dict of urls and text
    describing those urls."""
    with open(os.path.dirname(os.path.abspath(__file__)) + "/raw_data.json") as f:
        lines = json.load(f)

    for match, values in lines.items():
        if match == ticker:
            ticker_info = {'ticker': ticker, 'company_name': values['company_name']}
            ticker_info['chart_one_narrative'] = wordsmith(values['chart_one_data'],
                                                           "simplr-stock-price")
            print('we have 1 wordsmith response')
            sys.stdout.flush()
            ticker_info['chart_two_narrative'] = wordsmith(values['chart_two_data'],
                                                           "simplr-eps")
            print('we have 2 wordsmith responses')
            sys.stdout.flush()
            ticker_info['chart_three_narrative'] = wordsmith(values['chart_three_data'],
                                                             "simplr-net-income")
            print('we have 3 wordsmith responses')
            sys.stdout.flush()
            ticker_info['chart_four_narrative'] = wordsmith(values['chart_four_data'],
                                                            "simplr-sector-comparison")
            print('we have 4 wordsmith responses')
            sys.stdout.flush()
            return ticker_info


def wordsmith(data_dict, project):
    """Takes in data set to call out to Wordsmith API for a narrative"""

    url = "https://api.automatedinsights.com/v1/projects/" + project + \
          "/templates/new-template/outputs"
    headers = {'Authorization': 'Bearer ' + API_KEY,
               'Content-Type': 'application/json',
               'User-Agent': 'Hackathon Application'}
    data = json.dumps({"data": data_dict})

    response = requests.post(url, headers=headers, data=data)
    print(response.json())
    return response.json()['data']['content']
