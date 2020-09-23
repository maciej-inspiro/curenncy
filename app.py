import requests, csv

response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
data = response.json()
data_dict = data[0]
data_dict = data_dict['rates']

with open('bank_currencies.csv', 'w') as csvfile:
    fieldnames = ["currency", "code", "bid", "ask"]
    writer = csv.DictWriter(csvfile, delimiter =";", fieldnames=fieldnames)
    writer.writeheader()
    for x,n in enumerate(data_dict):
        writer.writerow(n)


from flask import Flask, request, render_template, redirect, url_for
import csv

app = Flask(__name__)

@app.route('/')
def hello():
    my_name = "Maciej"
    return f'Hello, {my_name}!'

if __name__ == "__main__":
    app.run(debug=True)


@app.route("/calc", methods = ["GET","POST"])
def calc():
    if request.method == "POST":
        data = request.form
        currency = data.get("currency")
        amount = data.get("amount")
        with open('bank_currencies.csv') as cs_vfile:
            csv_reader = csv.DictReader(open("bank_currencies.csv"), delimiter = ';')
            csv_reader = [row for row in csv_reader if row]
            for row in csv_reader:
                print(row['currency'])
                if row['currency'] == currency:
                    price = float(amount) * float(row['ask'])
                    return(f"za {amount} {currency}, zapłacisz {price} polskie złote")
    else:
        return render_template("curr.html")

if __name__ == "__main__":
    app.run(debug=True)

#GOTOWE, DO PRZESŁANIA NA GIT'A I MENTOROWI
