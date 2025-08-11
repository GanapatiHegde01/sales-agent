from app import create_app, db
from utils import load_csv_to_db
import os

app = create_app()

if __name__ == "__main__":
    # Optionally load CSVs if present in project root
    products_csv = os.getenv("PRODUCTS_CSV", "products.csv")
    offers_csv = os.getenv("OFFERS_CSV", "offers.csv")
    warranty_csv = os.getenv("WARRANTY_CSV", "warranty_info.csv")

    with app.app_context():
        # Create DB tables if not exist
        db.create_all()

        # Try to auto-load sample CSVs if files exist
        if os.path.exists(products_csv):
            try:
                load_csv_to_db(products_csv, offers_csv, warranty_csv)
            except Exception as e:
                print("Failed to load CSVs:", e)

    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=True)