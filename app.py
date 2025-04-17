from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "Vaulted backend is running."

@app.route("/api/stockx")
def get_stockx_data():
    slug = request.args.get("slug")
    if not slug:
        return jsonify({"error": "Missing slug parameter"}), 400

    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Accept': 'application/json',
        'Referer': f'https://stockx.com/{slug}',
    }

    url = f'https://stockx.com/api/products/{slug}?includes=market,children'

    try:
        res = requests.get(url, headers=headers)
        if res.status_code != 200:
            return jsonify({"error": "StockX fetch failed"}), res.status_code

        data = res.json()['Product']
        return jsonify({
            "name": data.get('title'),
            "last_sale": data['market'].get('lastSale'),
            "lowest_ask": data['market'].get('lowestAsk'),
            "highest_bid": data['market'].get('highestBid'),
            "url": f"https://stockx.com/{slug}"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
