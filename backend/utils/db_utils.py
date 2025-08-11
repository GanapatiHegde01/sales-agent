import pandas as pd
from app import db
from app.models import Product, Offer, WarrantyInfo
import json

def load_csv_to_db(products_csv, offers_csv, warranty_csv):
    """Load CSV files into the database. Existing records for these tables are removed first."""
    # Remove existing
    Offer.query.delete()
    WarrantyInfo.query.delete()
    Product.query.delete()
    db.session.commit()

    # Load Products
    df_products = pd.read_csv(products_csv)
    for _, row in df_products.iterrows():
        specs = row.get('specs')
        try:
            specs_parsed = json.loads(specs) if isinstance(specs, str) and specs.strip() else {}
        except Exception:
            specs_parsed = {}
        p = Product(
            id=int(row['id']),
            name=row['name'],
            category=row.get('category'),
            price=float(row.get('price') or 0.0),
            description=row.get('description'),
            specs=specs_parsed,
            stock=int(row.get('stock') or 0)
        )
        db.session.add(p)
    
    # Commit products first to satisfy foreign key constraints
    db.session.commit()

    # Load Offers
    try:
        df_off = pd.read_csv(offers_csv)
        for _, row in df_off.iterrows():
            offer = Offer(
                id=int(row['id']),
                product_id=int(row['product_id']),
                discount_percentage=float(row.get('discount_percentage') or 0),
                coupon_code=row.get('coupon_code'),
                valid_till=row.get('valid_till')
            )
            db.session.add(offer)
    except FileNotFoundError:
        pass

    # Load Warranty
    try:
        df_w = pd.read_csv(warranty_csv)
        for _, row in df_w.iterrows():
            w = WarrantyInfo(
                id=int(row['id']),
                product_id=int(row['product_id']),
                warranty_period=row.get('warranty_period'),
                claim_process=row.get('claim_process')
            )
            db.session.add(w)
    except FileNotFoundError:
        pass

    db.session.commit()
    print("CSV data loaded.")