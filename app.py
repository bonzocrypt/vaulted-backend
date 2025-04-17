from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return "Vaulted backend is running."

@app.route("/api/stockx")
def get_stockx_data():
    slug = request.args.get("slug")
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
            "name": data['title'],
            "last_sale": data['market']['lastSale'],
            "lowest_ask": data['market']['lowestAsk'],
            "highest_bid": data['market']['highestBid'],
            "url": f"https://stockx.com/{slug}"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ This part is critical for Railway to run the app properly
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
