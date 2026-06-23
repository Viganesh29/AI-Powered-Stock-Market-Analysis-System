# 📈 VIAN FINSERVE

An AI-Powered Stock Market Analysis and Prediction Platform built using Python, Streamlit, Machine Learning, and Financial Data Analytics.

## 🚀 Overview

VIAN FINSERVE is an intelligent financial analytics platform that helps investors analyze stock performance, compare stocks, visualize historical trends, and generate AI-powered insights.

The system integrates financial data retrieval, machine learning-based forecasting, interactive visualizations, and AI explanations into a single dashboard.

---

## ✨ Features

### 📊 Stock Analysis
- Search stocks using ticker symbols
- Historical stock price analysis
- Interactive charts and visualizations
- Return and volatility calculations

### 🏢 Fundamental Analysis
- Market Capitalization
- Revenue Analysis
- Net Income
- PE Ratio
- Debt-to-Equity Ratio
- ROE
- Free Cash Flow

### 🤖 AI Financial Assistant
- AI-generated stock explanations
- Ask questions about selected stocks
- Financial insight generation
- Investment-oriented analysis

### 📈 Stock Prediction
- Machine Learning based forecasting
- Future stock price prediction
- Buy / Hold / Sell recommendations
- Risk level estimation
- Confidence score generation

### ⚖️ Stock Comparison
- Compare two stocks
- Return comparison
- Volatility comparison
- AI-generated verdict

### 🗄️ Database Analytics
- Search History Storage
- AI Report Storage
- Stock Comparison History
- Prediction History

---

## 🛠️ Technology Stack

### Frontend
- Streamlit

### Backend
- Python

### Data Analysis
- Pandas
- NumPy

### Machine Learning
- Scikit-Learn
- TensorFlow/Keras

### Data Visualization
- Plotly
- Matplotlib

### Financial Data Source
- Yahoo Finance API (yfinance)

### Database
- MySQL

### AI Integration
- Ollama
- Llama 3

---

## 📂 Project Structure

```text
VIAN-FINSERVE
│
├── app.py
│
├── backend
│   ├── ai_agent.py
│   ├── ai_analysis.py
│   ├── comparison.py
│   ├── currency.py
│   ├── database.py
│   ├── fundamentals.py
│   ├── performance.py
│   ├── prediction.py
│   └── trading_signal.py
│
├── requirements.txt
│
└── README.md
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/yourusername/VIAN-FINSERVE.git
```

### Navigate to Project

```bash
cd VIAN-FINSERVE
```

### Create Virtual Environment

```bash
python -m venv myenv
```

### Activate Environment

Windows

```bash
myenv\Scripts\activate
```

Linux/Mac

```bash
source myenv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🗃️ Database Setup

Create MySQL Database:

```sql
CREATE DATABASE vian_finserve;
```

Create required tables:

- search_history
- ai_reports
- asset_comparisons
- predictions

Update database credentials inside:

```python
backend/database.py
```

---

## ▶️ Run Application

```bash
streamlit run app.py
```

Application runs at:

```text
http://localhost:8501
```

---

## 📸 Screenshots

### Dashboard
(Add Screenshot)

### AI Explanation
(Add Screenshot)

### Stock Comparison
(Add Screenshot)

### Prediction Module
(Add Screenshot)

---

## 📊 Future Enhancements

- Cryptocurrency Analysis
- ETF Analysis
- Mutual Fund Analytics
- Advanced Deep Learning Models
- Portfolio Optimization
- Real-Time News Sentiment Analysis
- Risk Management Dashboard

---

## 👨‍💻 Author

Viganesh Anand

B.Sc Data Science

AI / ML Enthusiast | Data Analyst | AI Engineer

---

## 📄 License

This project is developed for educational and research purposes.
