from flask import Blueprint, jsonify
from app import db
from app.models import ChatHistory, User, Product
from sqlalchemy import func, desc, text
from datetime import datetime, timedelta

admin_bp = Blueprint('admin_bp', __name__)


@admin_bp.route('/analytics/overview', methods=['GET'])
def get_system_analytics():
    """Get system-wide analytics for admin dashboard"""
    
    # Basic counts
    total_users = User.query.count()
    total_chats = ChatHistory.query.count()
    total_products = Product.query.count()
    
    # Recent activity (last 30 days)
    month_ago = datetime.utcnow() - timedelta(days=30)
    recent_chats = ChatHistory.query.filter(ChatHistory.created_at >= month_ago).count()
    new_users = User.query.filter(User.created_at >= month_ago).count()
    
    # Most active users
    active_users = db.session.query(
        User.name, 
        func.count(ChatHistory.id).label('chat_count')
    ).join(ChatHistory).group_by(User.id, User.name)\
     .order_by(desc('chat_count')).limit(10).all()
    
    # Popular queries (basic analysis)
    recent_queries = ChatHistory.query.filter(
        ChatHistory.created_at >= month_ago
    ).all()
    
    intent_analysis = {'product_search': 0, 'warranty': 0, 'offer': 0, 'general': 0}
    brand_mentions = {'apple': 0, 'samsung': 0, 'bose': 0, 'hp': 0, 'lenovo': 0}
    
    for chat in recent_queries:
        query_lower = chat.query.lower()
        
        # Intent analysis
        if any(word in query_lower for word in ['find', 'search', 'looking', 'tell me about']):
            intent_analysis['product_search'] += 1
        elif any(word in query_lower for word in ['warranty', 'claim']):
            intent_analysis['warranty'] += 1
        elif any(word in query_lower for word in ['offer', 'discount', 'coupon']):
            intent_analysis['offer'] += 1
        else:
            intent_analysis['general'] += 1
        
        # Brand analysis
        for brand in brand_mentions.keys():
            if brand in query_lower:
                brand_mentions[brand] += 1
    

    daily_chats = []
    for i in range(7):
        date = datetime.utcnow() - timedelta(days=i)
        day_start = date.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = day_start + timedelta(days=1)
        
        count = ChatHistory.query.filter(
            ChatHistory.created_at >= day_start,
            ChatHistory.created_at < day_end
        ).count()
        
        daily_chats.append({
            'date': day_start.strftime('%Y-%m-%d'),
            'count': count
        })
    
    return jsonify({
        'overview': {
            'total_users': total_users,
            'total_chats': total_chats,
            'total_products': total_products,
            'recent_chats': recent_chats,
            'new_users': new_users
        },
        'active_users': [{'name': name, 'chat_count': count} for name, count in active_users],
        'intent_analysis': intent_analysis,
        'brand_mentions': brand_mentions,
        'daily_activity': daily_chats
    })

@admin_bp.route('/analytics/user-behavior', methods=['GET'])
def get_user_behavior():
    """Analyze user behavior patterns"""
    
    # Average session length (chats per user)
    user_chat_counts = db.session.query(
        func.count(ChatHistory.id).label('chat_count')
    ).join(User).group_by(User.id).all()
    
    avg_chats_per_user = sum([count[0] for count in user_chat_counts]) / len(user_chat_counts) if user_chat_counts else 0
    
    # Most common query patterns
    common_queries = db.session.query(
        ChatHistory.query,
        func.count(ChatHistory.id).label('frequency')
    ).group_by(ChatHistory.query)\
     .having(func.count(ChatHistory.id) > 1)\
     .order_by(desc('frequency')).limit(20).all()
    
    # User engagement levels
    engagement_levels = {
        'high': 0,  # >10 chats
        'medium': 0,  # 3-10 chats
        'low': 0   # 1-2 chats
    }
    
    for count in user_chat_counts:
        if count[0] > 10:
            engagement_levels['high'] += 1
        elif count[0] >= 3:
            engagement_levels['medium'] += 1
        else:
            engagement_levels['low'] += 1
    
    return jsonify({
        'avg_chats_per_user': round(avg_chats_per_user, 2),
        'common_queries': [{'query': q, 'frequency': f} for q, f in common_queries],
        'engagement_levels': engagement_levels
    })

@admin_bp.route('/analytics/product-insights', methods=['GET'])
def get_product_insights():
    """Get insights about product queries and interests"""
    
    # Most queried products/brands
    recent_chats = ChatHistory.query.filter(
        ChatHistory.created_at >= datetime.utcnow() - timedelta(days=30)
    ).all()
    
    product_mentions = {}
    category_mentions = {'laptop': 0, 'smartphone': 0, 'headphones': 0, 'smartwatch': 0}
    
    for chat in recent_chats:
        query_lower = chat.query.lower()
        
        # Extract product model mentions
        if 'model' in query_lower:
            words = query_lower.split()
            for i, word in enumerate(words):
                if word == 'model' and i + 1 < len(words):
                    model = f"model {words[i+1]}"
                    product_mentions[model] = product_mentions.get(model, 0) + 1
        
        # Category analysis
        for category in category_mentions.keys():
            if category in query_lower:
                category_mentions[category] += 1
    
    # Sort product mentions
    top_products = sorted(product_mentions.items(), key=lambda x: x[1], reverse=True)[:10]
    
    return jsonify({
        'top_product_models': [{'model': model, 'mentions': count} for model, count in top_products],
        'category_interest': category_mentions
    })