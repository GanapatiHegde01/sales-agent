from flask import Blueprint, request, jsonify
from app import db
from app.models import ChatHistory, User
from utils import require_auth
from sqlalchemy import desc, func
from datetime import datetime, timedelta

chat_history_bp = Blueprint('chat_history_bp', __name__)

@chat_history_bp.route('/test', methods=['GET'])
def test_endpoint():
    """Test endpoint to verify blueprint is working"""
    return jsonify({'message': 'Chat history endpoint is working'})

@chat_history_bp.route('/debug-search', methods=['GET'])
@require_auth
def debug_search():
    """Debug search functionality"""
    try:
        # Get all chats for this user
        all_chats = db.session.query(ChatHistory).filter(
            ChatHistory.user_id == request.current_user.id
        ).all()
        
        # Test simple search for 'bose'
        bose_chats = db.session.query(ChatHistory).filter(
            ChatHistory.user_id == request.current_user.id,
            ChatHistory.query.ilike('%bose%')
        ).all()
        
        # Test case-insensitive search for 'Bose'
        bose_upper_chats = db.session.query(ChatHistory).filter(
            ChatHistory.user_id == request.current_user.id,
            ChatHistory.query.ilike('%Bose%')
        ).all()
        
        return jsonify({
            'total_chats': len(all_chats),
            'all_queries': [chat.query for chat in all_chats],
            'bose_lowercase_matches': len(bose_chats),
            'bose_uppercase_matches': len(bose_upper_chats),
            'user_id': request.current_user.id
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@chat_history_bp.route('/', methods=['GET'])
@require_auth
def get_user_chat_history():
    """Get user's chat history with pagination"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        # Simple query first
        chats = db.session.query(ChatHistory).filter(
            ChatHistory.user_id == request.current_user.id
        ).order_by(desc(ChatHistory.created_at)).limit(per_page).all()
        
        return jsonify({
            'chats': [chat.to_dict() for chat in chats],
            'total': len(chats),
            'current_page': page
        })
    except Exception as e:
        return jsonify({'error': str(e), 'user_id': request.current_user.id}), 500

@chat_history_bp.route('/analytics', methods=['GET'])
@require_auth
def get_user_analytics():
    """Get user's chat analytics"""
    try:
        user_id = request.current_user.id
        
        # Total chats
        total_chats = db.session.query(ChatHistory).filter(ChatHistory.user_id == user_id).count()
        
        # Chats this week
        week_ago = datetime.utcnow() - timedelta(days=7)
        chats_this_week = db.session.query(ChatHistory).filter(
            ChatHistory.user_id == user_id,
            ChatHistory.created_at >= week_ago
        ).count()
        
        # Most common query types (basic intent detection)
        recent_chats = db.session.query(ChatHistory).filter(ChatHistory.user_id == user_id)\
            .order_by(desc(ChatHistory.created_at)).limit(50).all()
        
        intent_counts = {'product_search': 0, 'warranty': 0, 'offer': 0, 'general': 0}
        for chat in recent_chats:
            query_lower = chat.query.lower()
            if any(word in query_lower for word in ['find', 'search', 'looking', 'tell me about']):
                intent_counts['product_search'] += 1
            elif any(word in query_lower for word in ['warranty', 'claim']):
                intent_counts['warranty'] += 1
            elif any(word in query_lower for word in ['offer', 'discount', 'coupon']):
                intent_counts['offer'] += 1
            else:
                intent_counts['general'] += 1
        
        return jsonify({
            'total_chats': total_chats,
            'chats_this_week': chats_this_week,
            'query_types': intent_counts,
            'avg_chats_per_day': round(chats_this_week / 7, 1)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@chat_history_bp.route('/search', methods=['GET'])
@require_auth
def search_chat_history():
    """Search through user's chat history"""
    try:
        query = request.args.get('q', '').strip()
        if not query:
            # Return empty results if no query provided
            return jsonify({
                'results': [],
                'count': 0,
                'message': 'No search query provided'
            })
        
        # Simple direct search first
        from sqlalchemy import or_
        
        # Direct search in both query and response
        chats = db.session.query(ChatHistory).filter(
            ChatHistory.user_id == request.current_user.id,
            or_(
                ChatHistory.query.ilike(f'%{query}%'),
                ChatHistory.response.ilike(f'%{query}%')
            )
        ).order_by(desc(ChatHistory.created_at)).limit(20).all()
        
        # If no direct match, try word-by-word search
        if not chats:
            search_words = query.lower().split()
            word_conditions = []
            for word in search_words:
                word_conditions.append(
                    or_(
                        ChatHistory.query.ilike(f'%{word}%'),
                        ChatHistory.response.ilike(f'%{word}%')
                    )
                )
            
            # Try OR logic (any word matches)
            chats = db.session.query(ChatHistory).filter(
                ChatHistory.user_id == request.current_user.id,
                or_(*word_conditions)
            ).order_by(desc(ChatHistory.created_at)).limit(20).all()
        else:
            search_words = query.lower().split()
        
        # Debug info - get all user chats to see what's in the database
        all_user_chats = db.session.query(ChatHistory).filter(
            ChatHistory.user_id == request.current_user.id
        ).all()
        
        # Show sample of actual chat queries for debugging
        sample_queries = [chat.query[:50] + '...' if len(chat.query) > 50 else chat.query 
                         for chat in all_user_chats[:3]]
        
        return jsonify({
            'results': [chat.to_dict() for chat in chats],
            'count': len(chats),
            'search_query': query,
            'search_words': search_words,
            'total_chats': len(all_user_chats),
            'current_user_id': request.current_user.id,
            'sample_queries': sample_queries,
            'debug': f'Searched for "{query}" (words: {search_words}) in {len(all_user_chats)} total chats'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@chat_history_bp.route('/<int:chat_id>', methods=['DELETE'])
@require_auth
def delete_chat(chat_id):
    """Delete a specific chat"""
    try:
        chat = db.session.query(ChatHistory).filter(
            ChatHistory.id == chat_id, 
            ChatHistory.user_id == request.current_user.id
        ).first()
        
        if not chat:
            return jsonify({'error': 'Chat not found'}), 404
        
        db.session.delete(chat)
        db.session.commit()
        
        return jsonify({'message': 'Chat deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@chat_history_bp.route('/clear', methods=['DELETE'])
@require_auth
def clear_all_chats():
    """Clear all user's chat history"""
    try:
        db.session.query(ChatHistory).filter(ChatHistory.user_id == request.current_user.id).delete()
        db.session.commit()
        
        return jsonify({'message': 'All chats cleared successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500