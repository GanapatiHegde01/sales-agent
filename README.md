# AI Sales Agent

An intelligent sales assistant application that helps customers find products, get warranty information, discover offers, and make informed purchasing decisions through natural language conversations.

## 🚀 Features

- **Intelligent Chat Interface**: Natural language processing for product queries
- **Product Search & Discovery**: Advanced search with intent detection
- **Warranty Information**: Comprehensive warranty details and claim processes
- **Special Offers**: Real-time discount and coupon information
- **User Authentication**: Secure login and registration system
- **Chat History**: Persistent conversation tracking
- **Responsive Design**: Modern UI with dark/light theme support

## 🏗️ Architecture

### Backend (Flask)
- **Framework**: Flask with SQLAlchemy ORM
- **Database**: PostgreSQL
- **AI Integration**: Google Gemini AI for natural language processing
- **Authentication**: JWT-based auth with bcrypt password hashing
- **API**: RESTful API with CORS support

### Frontend (React)
- **Framework**: React 19 with Vite
- **Styling**: Tailwind CSS
- **Routing**: React Router DOM
- **State Management**: Context API
- **HTTP Client**: Axios

## 📋 Prerequisites

- **Node.js** (v18 or higher)
- **Python** (v3.8 or higher)
- **PostgreSQL** (v12 or higher)
- **Google Gemini API Key**

## 🛠️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/GanapatiHegde01/Sales-agent.git
cd Sales-agent
```

### 2. Database Setup

Create a PostgreSQL database:

```sql
CREATE DATABASE ai_sales_agent;
CREATE USER postgres WITH PASSWORD '12345';
GRANT ALL PRIVILEGES ON DATABASE ai_sales_agent TO postgres;
```

### 3. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
```

Edit the `.env` file with your configuration:

```env
SECRET_KEY=your_secret_key_here
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/ai_sales_agent
GEMINI_API_KEY=your_gemini_api_key_here
AUTH_API_KEY=your_dev_api_key_here
PRODUCTS_CSV=datasets/products.csv
OFFERS_CSV=datasets/offers.csv
WARRANTY_CSV=datasets/warranty_info.csv
```

### 4. Database Migration

```bash
# Initialize database
flask db init

# Create migration
flask db migrate -m "Initial migration"

# Apply migration
flask db upgrade
```

### 5. Frontend Setup

```bash
cd ../frontend

# Install dependencies
npm install

# Setup environment variables
# Create .env file with:
echo "VITE_API_BASE_URL=http://localhost:5000/api" > .env
```

## 🚀 Running the Application

### Start Backend Server

```bash
cd backend
python run.py
```

The backend will be available at `http://localhost:5000`

### Start Frontend Development Server

```bash
cd frontend
npm run dev
```

The frontend will be available at `http://localhost:5173`

## 📊 Sample Data

The application includes sample datasets in the `backend/datasets/` directory:

- `products.csv` - Product catalog with specifications
- `offers.csv` - Special offers and discounts
- `warranty_info.csv` - Warranty information for products

These are automatically loaded when the backend starts if the files exist.

## 🔧 API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login

### Products
- `GET /api/products` - Get all products
- `GET /api/products/{id}` - Get specific product

### Chat
- `POST /api/chat` - Send chat message and get AI response

### Offers
- `GET /api/offers` - Get all offers
- `GET /api/offers/product/{id}` - Get offers for specific product

### Warranty
- `GET /api/warranty` - Get all warranty information
- `GET /api/warranty/product/{id}` - Get warranty for specific product

### Chat History
- `GET /api/chat-history` - Get user's chat history

### Admin Analytics
- `GET /api/admin/analytics` - Get analytics data (admin only)

## 🤖 AI Features

The AI assistant can handle various types of queries:

- **Product Search**: "Show me laptops under $1000"
- **Specific Models**: "Tell me about iPhone 15 Pro"
- **Warranty Queries**: "What's the warranty on Samsung Galaxy S24?"
- **Offers & Discounts**: "Any deals on headphones?"
- **Comparisons**: "Compare MacBook Air vs MacBook Pro"
- **Product ID Lookup**: "Show me product ID 123"

## 🎨 Frontend Features

- **Responsive Design**: Works on desktop, tablet, and mobile
- **Dark/Light Theme**: Toggle between themes
- **Protected Routes**: Authentication-based navigation
- **Real-time Chat**: Instant AI responses
- **Product Cards**: Rich product information display
- **Search & Filter**: Advanced product filtering

## 🔒 Security Features

- **Password Hashing**: bcrypt for secure password storage
- **JWT Authentication**: Stateless authentication tokens
- **CORS Protection**: Configured for secure cross-origin requests
- **Input Validation**: Server-side validation for all inputs
- **SQL Injection Prevention**: SQLAlchemy ORM protection

## 📱 Usage Examples

### Chat Interactions

```
User: "I need a laptop for gaming under $1500"
AI: "I found several gaming laptops under $1500..."

User: "What's the warranty on the ASUS ROG?"
AI: "The ASUS ROG comes with a 2-year warranty..."

User: "Any discounts available?"
AI: "Yes! Here are the current offers..."
```

## 🚀 Deployment

### Backend Deployment

1. Set production environment variables
2. Use a production WSGI server like Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

### Frontend Deployment

```bash
npm run build
# Deploy the dist/ folder to your hosting service
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Ganapati Hegde**
- GitHub: [@GanapatiHegde01](https://github.com/GanapatiHegde01)
- Project: [Sales-agent](https://github.com/GanapatiHegde01/Sales-agent)

© 2024 Ganapati Hegde. All rights reserved.

## 🆘 Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Ensure PostgreSQL is running
   - Check database credentials in `.env`

2. **Gemini API Error**
   - Verify your Gemini API key is valid
   - Check API quota and billing

3. **CORS Issues**
   - Ensure frontend URL is in CORS configuration
   - Check that both servers are running

4. **Module Import Errors**
   - Activate virtual environment
   - Reinstall requirements: `pip install -r requirements.txt`

### Getting Help

- Check the [Issues](https://github.com/GanapatiHegde01/Sales-agent/issues) page
- Create a new issue with detailed error information
- Include logs and environment details

## 🔮 Future Enhancements

- [ ] Voice chat integration
- [ ] Multi-language support
- [ ] Advanced analytics dashboard
- [ ] Product recommendation engine
- [ ] Integration with payment systems
- [ ] Mobile app development
- [ ] Real-time notifications
- [ ] Advanced search filters

---

**Built with ❤️ by Ganapati Hegde using Flask, React, and Google Gemini AI**