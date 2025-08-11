import os
import google.generativeai as genai
from flask import Blueprint, request, jsonify, current_app
from app import db
from app.models import ChatHistory, Product, Offer, WarrantyInfo
from sqlalchemy import or_, and_

from utils import require_auth

chat_bp = Blueprint("chat_bp", __name__)

def extract_keywords(message, exclude_words=None):
    """Extract meaningful keywords from message"""
    if exclude_words is None:
        exclude_words = ['the', 'is', 'are', 'was', 'were', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'what', 'how', 'where', 'when', 'why', 'there', 'here', 'this', 'that', 'these', 'those']
    
    words = message.lower().split()
    return [w for w in words if len(w) > 2 and w not in exclude_words]

def detect_intent_and_context(message):
    """Advanced intent detection with context"""
    msg_lower = message.lower()
    
    # Multi-intent detection
    intents = []
    context = {}
    
    # Check for product ID queries first
    if 'product id' in msg_lower or 'product-id' in msg_lower:
        intents.append('product_id_lookup')
        # Extract product ID if present
        import re
        id_match = re.search(r'product.?id.?(\d+)', msg_lower)
        if id_match:
            context['product_id'] = int(id_match.group(1))
    
    # Primary intent detection
    if any(word in msg_lower for word in ['warranty', 'claim', 'guarantee', 'repair', 'replace']):
        intents.append('warranty')
    if any(word in msg_lower for word in ['offer', 'discount', 'coupon', 'deal', 'sale', 'promo']):
        intents.append('offer')
    if any(word in msg_lower for word in ['find', 'search', 'looking', 'want', 'need', 'show', 'tell', 'about', 'info']):
        intents.append('product_search')
    if any(word in msg_lower for word in ['compare', 'vs', 'versus', 'difference', 'better']):
        intents.append('comparison')
    if any(word in msg_lower for word in ['price', 'cost', 'expensive', 'cheap', 'budget']):
        intents.append('pricing')
    if any(word in msg_lower for word in ['stock', 'available', 'inventory', 'in stock']):
        intents.append('availability')
    
    # Default to product search if no specific intent but has product mentions
    product_indicators = ['bose', 'apple', 'samsung', 'lenovo', 'hp', 'asus', 'oneplus', 'xiaomi', 'jbl', 'sennheiser', 'garmin', 'fitbit', 'laptop', 'smartphone', 'headphones', 'smartwatch', 'model']
    if not intents and any(word in msg_lower for word in product_indicators):
        intents.append('product_search')
    
    # Context detection
    context['is_specific_model'] = 'model' in msg_lower and any(char.isdigit() for char in message)
    context['has_brand'] = any(brand in msg_lower for brand in ['bose', 'apple', 'samsung', 'lenovo', 'hp', 'asus', 'oneplus', 'xiaomi', 'jbl', 'sennheiser', 'garmin', 'fitbit'])
    context['has_category'] = any(cat in msg_lower for cat in ['laptop', 'smartphone', 'headphones', 'smartwatch'])
    
    return intents if intents else ['general'], context

def build_product_query(keywords, context):
    """Build optimized product query based on context"""
    if not keywords:
        return Product.query.limit(5)
    
    # For specific model queries, use precise AND matching
    if context.get('is_specific_model'):
        # Filter out common words for model queries
        model_keywords = [k for k in keywords if k not in ['model', 'tell', 'about', 'me', 'info', 'information']]
        if model_keywords:
            conditions = [Product.name.ilike(f"%{kw}%") for kw in model_keywords]
            return Product.query.filter(and_(*conditions)).limit(3)
    
    # For brand + category queries, prioritize exact matches
    if context.get('has_brand') and context.get('has_category'):
        conditions = []
        for kw in keywords:
            conditions.extend([
                Product.name.ilike(f"%{kw}%"),
                Product.category.ilike(f"%{kw}%")
            ])
        return Product.query.filter(or_(*conditions)).limit(5)
    
    # General search with OR logic
    conditions = []
    for kw in keywords:
        conditions.extend([
            Product.name.ilike(f"%{kw}%"),
            Product.category.ilike(f"%{kw}%"),
            Product.description.ilike(f"%{kw}%")
        ])
    return Product.query.filter(or_(*conditions)).limit(8)

@chat_bp.route("/", methods=["POST"])
@require_auth
def chat():
    data = request.json or {}
    user_id = request.current_user.id
    message = data.get("message")
    if not message:
        return jsonify({"error": "message is required"}), 400

    # Advanced intent detection
    intents, context = detect_intent_and_context(message)
    keywords = extract_keywords(message)
    
    structured_facts = {}
    products = []

    # Handle product ID lookup first
    if 'product_id_lookup' in intents and 'product_id' in context:
        product = Product.query.get(context['product_id'])
        if product:
            products = [product]
            structured_facts["products"] = [product.to_dict()]
        else:
            structured_facts["error"] = f"Product ID {context['product_id']} not found"
    
    # Handle multiple intents intelligently
    elif 'product_search' in intents or 'general' in intents:
        query = build_product_query(keywords, context)
        
        # Apply warranty filters if warranty intent detected
        if 'warranty' in intents:
            msg_lower = message.lower()
            if "2 year" in msg_lower or "2-year" in msg_lower:
                query = query.join(WarrantyInfo).filter(WarrantyInfo.warranty_period.ilike("%2 year%"))
            elif "1 year" in msg_lower or "1-year" in msg_lower:
                query = query.join(WarrantyInfo).filter(WarrantyInfo.warranty_period.ilike("%1 year%"))
            elif "6 month" in msg_lower or "6-month" in msg_lower:
                query = query.join(WarrantyInfo).filter(WarrantyInfo.warranty_period.ilike("%6 month%"))
        
        products = query.all()
        
        # Only include products in response for pure product searches
        if 'product_search' in intents and len(intents) == 1:
            structured_facts["products"] = [p.to_dict() for p in products]
        elif products:
            # For mixed intents, use products as context only
            structured_facts["_product_context"] = [p.to_dict() for p in products]
    
    # Handle warranty queries
    if 'warranty' in intents and products:
        product_ids = [p.id for p in products]
        warranties = WarrantyInfo.query.filter(WarrantyInfo.product_id.in_(product_ids)).all()
        structured_facts["warranty"] = [w.to_dict() for w in warranties]
    elif 'warranty' in intents and not products:
        # General warranty query without specific products
        warranties = WarrantyInfo.query.limit(5).all()
        structured_facts["warranty"] = [w.to_dict() for w in warranties]
    
    # Handle offer queries
    if 'offer' in intents and products:
        product_ids = [p.id for p in products]
        offers = Offer.query.filter(Offer.product_id.in_(product_ids)).all()
        structured_facts["offers"] = [o.to_dict() for o in offers]
        # Include product details for offers
        structured_facts["offer_products"] = [p.to_dict() for p in products]
    elif 'offer' in intents and not products:
        # General offer query without specific products
        offers = Offer.query.limit(5).all()
        structured_facts["offers"] = [o.to_dict() for o in offers]
        # Include product details for all offers
        offer_product_ids = [o.product_id for o in offers]
        offer_products = Product.query.filter(Product.id.in_(offer_product_ids)).all()
        structured_facts["offer_products"] = [p.to_dict() for p in offer_products]
    
    # Handle pricing queries
    if 'pricing' in intents and products:
        # Products already included, AI will focus on pricing
        pass
    
    # Handle availability queries
    if 'availability' in intents and products:
        # Products already included with stock info, AI will focus on availability
        pass
    
    # Handle comparison queries
    if 'comparison' in intents and products:
        # Limit to top matches for comparison
        if len(products) > 4:
            products = products[:4]
            if "products" in structured_facts:
                structured_facts["products"] = structured_facts["products"][:4]
            if "_product_context" in structured_facts:
                structured_facts["_product_context"] = structured_facts["_product_context"][:4]

    # Configure Gemini
    genai.configure(api_key=current_app.config.get('GEMINI_API_KEY'))
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Build enhanced sales-focused prompt
    intent_context = ", ".join(intents)
    system_prompt = f"""You are a professional sales assistant helping customers with {intent_context} queries. 
    
Guidelines:
    - Use ONLY the provided structured facts
    - Be helpful, concise, and sales-oriented
    - For product searches: highlight key features, pricing, and availability
    - For warranty queries: explain coverage and claim process clearly
    - For offer queries: emphasize savings and validity periods, and ALWAYS mention the product name with the offer
    - For product ID lookups: provide complete product information
    - For comparisons: highlight differences and recommend based on needs
    - For pricing: mention value proposition
    - Always be customer-focused and solution-oriented
    - When showing offers, always include the product name, not just the ID
    
    If no relevant data is found, politely explain and suggest alternatives."""
    
    prompt = f"{system_prompt}\n\nCustomer Query: {message}\nAvailable Data: {structured_facts}"

    # Call Gemini
    try:
        response = model.generate_content(prompt)
        ai_reply = response.text
    except Exception as e:
        ai_reply = "Sorry, I couldn't contact the AI service right now."

    # Save chat history
    chat = ChatHistory(user_id=user_id, query=message, response=ai_reply)
    db.session.add(chat)
    db.session.commit()

    return jsonify({
        "reply": ai_reply,
        "facts": structured_facts
    })