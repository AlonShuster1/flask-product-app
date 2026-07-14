from flask import Flask, render_template, request
from math import ceil
import requests

#create the flask application
app = Flask(__name__)

PRODUCTS_API_URL = "https://dummyjson.com"
PRODUCTS_PER_PAGE = 10
REQUEST_TIMEOUT = 10
PORT = 5000

@app.route("/", methods=["GET"])
def get_products():

    """
    Render a paginated and optionally filtered list of products.

    Returns: 
        the products page with the fetched products, current page, total pages, and search query.
    """

    page = request.args.get("page", 1, type=int)
    page = max(page, 1) # Ensure the page number is at least 1

    skip = (page - 1) * PRODUCTS_PER_PAGE

    search_query = request.args.get("q", default="", type=str).strip()

    if search_query:
        external_api_url = f"{PRODUCTS_API_URL}/products/search"
        params = {
            "q": search_query,
            "limit": PRODUCTS_PER_PAGE,
            "skip": skip,
        }
    else:
        external_api_url = f"{PRODUCTS_API_URL}/products"
        params = {
            "limit": PRODUCTS_PER_PAGE,
            "skip": skip,
        }

    try:
        response = requests.get(external_api_url,
                                params=params,
                                  timeout=REQUEST_TIMEOUT)
        
        response.raise_for_status()

        data = response.json()
        products = data.get("products", [])
        total_products = data.get("total", 0)
        total_pages = ceil(total_products / PRODUCTS_PER_PAGE)



        return render_template(
            "index.html",
            products=products,
            current_page=page,
            total_pages=total_pages,
            search_query=search_query,
            error_message=None,
        )

      

    except requests.RequestException as error:
        app.logger.exception("Failed to fetch products from the external API")
        return render_template(
            "index.html",
            products=[],
            current_page=1,
            total_pages=0,
            search_query=search_query,
            error_message="Could not load products."
        )


if __name__ == "__main__":
    app.run(debug=True, port=PORT)