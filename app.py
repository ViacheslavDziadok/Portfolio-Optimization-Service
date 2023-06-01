from flask import Flask, render_template, request
from main import whole_pipeline

app = Flask(__name__)

companies = {
    "MSFT": "Microsoft Corporation",
    "AMZN": "Amazon.com, Inc.",
    "KO": "The Coca-Cola Company",
    "MA": "Mastercard Incorporated",
    "COST": "Costco Wholesale Corporation",
    "LUV": "Southwest Airlines Co.",
    "XOM": "Exxon Mobil Corporation",
    "PFE": "Pfizer Inc.",
    "JPM": "JPMorgan Chase & Co.",
    "UNH": "UnitedHealth Group Incorporated",
    "ACN": "Accenture plc",
    "DIS": "The Walt Disney Company",
    "GILD": "Gilead Sciences, Inc.",
    "F": "Ford Motor Company",
    "TSLA": "Tesla, Inc.",
    "AAPL": "Apple Inc.",
    "GOOGL": "Alphabet Inc.",
    "META": "Meta Platforms, Inc.",
    "V": "Visa Inc.",
    "WMT": "Walmart Inc.",
    "VZ": "Verizon Communications Inc.",
    "PG": "The Procter & Gamble Company",
    "NKE": "NIKE, Inc.",
    "NFLX": "Netflix, Inc.",
    "NVDA": "NVIDIA Corporation",
    "IBM": "International Business Machines Corporation",
    "PEP": "PepsiCo, Inc.",
    "HD": "The Home Depot, Inc.",
    "MCD": "McDonald's Corporation",
    "MRK": "Merck & Co., Inc.",
    "INTC": "Intel Corporation",
    "CMCSA": "Comcast Corporation",
    "BAC": "Bank of America Corporation",
    "CSCO": "Cisco Systems, Inc.",
    "ABT": "Abbott Laboratories",
    "T": "AT&T Inc.",
    "ORCL": "Oracle Corporation",
    "TMO": "Thermo Fisher Scientific Inc.",
    "UNP": "Union Pacific Corporation",
    "AMD": "Advanced Micro Devices, Inc.",
    "MS": "Morgan Stanley",
    "ABBV": "AbbVie Inc.",
    "CVX": "Chevron Corporation",
    "LMT": "Lockheed Martin Corporation",
    "MO": "Altria Group, Inc.",
    "MMM": "3M Company",
    "BA": "The Boeing Company",
    "CAT": "Caterpillar Inc.",
    "GS": "The Goldman Sachs Group, Inc.",
    "TXN": "Texas Instruments Incorporated",
    "AMGN": "Amgen Inc.",
    "UPS": "United Parcel Service, Inc."
}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        selected_companies = request.form.getlist('companies[]')
        start_date = request.form['start-date']
        end_date = request.form['end-date']
        
        graph_data = whole_pipeline(selected_companies, start_date, end_date)
        
        return render_template('result.html', graph_data=graph_data)

    return render_template('index.html', companies=companies)

if __name__ == '__main__':
    app.run(debug=True)