# Credit Risk Model Journey - Streamlit Cloud Deployment

This is a comprehensive dashboard showcasing the end-to-end machine learning pipeline for credit risk assessment at Conektr.

## Features

- **6 Interactive Stages**: Complete journey from data ingestion to deployment
- **4 Persona Dashboards**: Executive, Technical, Customer Risk, and Credit Officer views
- **Real-time Visualizations**: Interactive charts and metrics using Plotly
- **Model Insights**: Performance metrics, feature importance, and SHAP explanations

## Deployment to Streamlit Cloud

### Prerequisites
- GitHub account
- Streamlit Cloud account (free at share.streamlit.io)

### Deployment Steps

1. **Push to GitHub**
   ```bash
   cd streamlit_deployment
   git init
   git add .
   git commit -m "Initial commit - Credit Risk Model Journey"
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to https://share.streamlit.io
   - Click "New app"
   - Select your GitHub repository
   - Set main file path: `app.py`
   - Click "Deploy"

3. **Configuration**
   - The app will automatically use the `requirements.txt` for dependencies
   - Custom theme settings are in `.streamlit/config.toml`

## Local Testing

Before deploying, test locally:

```bash
cd streamlit_deployment
pip install -r requirements.txt
streamlit run app.py
```

The app will open at http://localhost:8501

## Project Structure

```
streamlit_deployment/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── .streamlit/
│   └── config.toml          # Streamlit configuration
├── README.md                # This file
└── DEPLOYMENT_GUIDE.md      # Detailed deployment instructions
```

## Dashboard Stages

1. **Overview** - Complete journey visualization and key metrics
2. **Data Ingestion** - Multi-source data integration (Conektr, MasterCard, Bank, AECB)
3. **EDA & Profiling** - Data quality assessment and exploratory analysis
4. **Feature Engineering** - 32 engineered features for risk prediction
5. **Model Training** - Logistic Regression with 94.2% accuracy
6. **Dashboards & Personas** - Role-based views for different users

## Key Metrics

- **4,525 Customers** analyzed
- **94.2% Model Accuracy**
- **32 Engineered Features**
- **4 Data Sources** integrated
- **99.9% API Uptime**

## Support

For questions or issues:
- Email: data-science@conektr.com
- Documentation: See DEPLOYMENT_GUIDE.md

## License

© 2024 Conektr. All rights reserved.
