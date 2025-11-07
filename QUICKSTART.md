# Quick Start Guide

## 🚀 Deploy in 5 Minutes

### Option 1: Deploy to Streamlit Cloud (Recommended)

1. **Fork or clone this repository to your GitHub account**

2. **Go to Streamlit Cloud**
   - Visit: https://share.streamlit.io
   - Sign in with GitHub

3. **Click "New app"**
   - Repository: Select your forked repo
   - Branch: `main`
   - Main file: `app.py`
   - Click "Deploy"

4. **Done!** Your app will be live in 2-3 minutes

### Option 2: Run Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

Open http://localhost:8501 in your browser.

## 📊 What You'll See

The dashboard includes 6 main stages:

1. **🏠 Overview** - Journey flow and key metrics
2. **📥 Data Ingestion** - Multi-source integration
3. **📊 EDA & Profiling** - Data quality analysis
4. **🔧 Feature Engineering** - 32 engineered features
5. **🤖 Model Training** - 94.2% accuracy model
6. **📈 Dashboards** - 4 persona-specific views

## 🎯 Key Features

- Interactive visualizations with Plotly
- Real-time metrics and KPIs
- Model performance tracking
- SHAP explanations
- Role-based dashboards

## 📝 Requirements

- Python 3.8+
- Streamlit 1.28+
- Pandas 2.0+
- Plotly 5.17+
- NumPy 1.24+

## 🔧 Configuration

Edit `.streamlit/config.toml` to customize:
- Theme colors
- Server settings
- Browser behavior

## 📚 Documentation

- Full deployment guide: `DEPLOYMENT_GUIDE.md`
- Project overview: `README.md`

## 💡 Tips

- Use sidebar navigation to explore stages
- Click on metrics for detailed tooltips
- Interactive charts support zoom and pan
- Export visualizations as PNG

## 🆘 Need Help?

- Check `DEPLOYMENT_GUIDE.md` for troubleshooting
- Review Streamlit docs: https://docs.streamlit.io
- Contact: data-science@conektr.com

---

**Ready to deploy?** Follow Option 1 above! 🚀
