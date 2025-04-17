@app.route("/api/stockx")
def get_stockx_data():
    slug = request.args.get("slug")
    if not slug:
        return jsonify({"error": "Missing slug parameter"}), 400

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': f'https://stockx.com/{slug}',
        'Origin': 'https://stockx.com',
        'Connection': 'keep-alive'
    }

    url = f'https://stockx.com/api/products/{slug}?includes=market,children'

    try:
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code != 200:
            return jsonify({"error": f"StockX fetch failed – status {res.status_code}"}), res.status_code

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
