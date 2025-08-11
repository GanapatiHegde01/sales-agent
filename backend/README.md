# AI Sales Agent (Backend)
This is the Flask backend for the AI Sales & Support agent project.

## Quick start (local)
1. Create a virtualenv and activate it.
2. Install dependencies: `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and update values.
4. Place `products.csv`, `offers.csv`, `warranty_info.csv` in the project root (or set env vars).
5. Run: `python run.py`
6. API will be available at `http://localhost:5000/api/...`

## Endpoints
- `GET /api/products/` - list products
- `GET /api/products/<id>` - product detail
- `POST /api/products/` - add product
- `GET /api/offers/` - list offers
- `GET /api/warranty/<product_id>` - warranty for product
- `POST /api/chat/` - chat with AI (requires X-API-KEY header)