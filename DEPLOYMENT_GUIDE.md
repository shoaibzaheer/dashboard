# Streamlit Cloud Deployment Guide

## Complete Step-by-Step Instructions

### Step 1: Prepare Your Repository

1. **Create a new GitHub repository**
   - Go to https://github.com/new
   - Name: `credit-risk-model-journey`
   - Description: "Interactive ML pipeline dashboard for credit risk assessment"
   - Make it Public (required for free Streamlit Cloud)
   - Don't initialize with README (we have our own)

2. **Push this deployment folder to GitHub**
   ```bash
   cd streamlit_deployment
   
   # Initialize git if not already done
   git init
   
   # Add all files
   git add .
   
   # Commit
   git commit -m "Initial deployment - Credit Risk Model Journey"
   
   # Add your GitHub repo as remote
   git remote add origin https://github.com/YOUR_USERNAME/credit-risk-model-journey.git
   
   # Push to GitHub
   git branch -M main
   git push -u origin main
   ```

### Step 2: Deploy on Streamlit Cloud

1. **Sign up for Streamlit Cloud**
   - Go to https://share.streamlit.io
   - Click "Sign up" or "Continue with GitHub"
   - Authorize Streamlit to access your GitHub account

2. **Create New App**
   - Click "New app" button
   - Select your repository: `YOUR_USERNAME/credit-risk-model-journey`
   - Branch: `main`
   - Main file path: `app.py`
   - App URL: Choose a custom URL (e.g., `credit-risk-journey`)

3. **Advanced Settings (Optional)**
   - Python version: 3.11 (recommended)
   - Secrets: Not needed for this app
   - Click "Deploy!"

### Step 3: Wait for Deployment

- Initial deployment takes 2-5 minutes
- Streamlit Cloud will:
  - Clone your repository
  - Install dependencies from requirements.txt
  - Start the Streamlit server
  - Provide you with a public URL

### Step 4: Access Your Dashboard

Your app will be available at:
```
https://YOUR_APP_NAME.streamlit.app
```

Example: `https://credit-risk-journey.streamlit.app`

## Troubleshooting

### Common Issues

1. **Import Errors**
   - Check that all packages are in `requirements.txt`
   - Verify package versions are compatible

2. **App Won't Start**
   - Check Streamlit Cloud logs
   - Ensure `app.py` is in the root of your repo
   - Verify Python syntax is correct

3. **Slow Performance**
   - Streamlit Cloud free tier has resource limits
   - Consider caching with `@st.cache_data`
   - Optimize data loading

### Viewing Logs

1. Go to your app on Streamlit Cloud
2. Click "Manage app" (bottom right)
3. View logs in the "Logs" tab

## Updating Your App

After making changes:

```bash
git add .
git commit -m "Update: description of changes"
git push
```

Streamlit Cloud will automatically redeploy your app within 1-2 minutes.

## Resource Limits (Free Tier)

- **CPU**: 1 vCPU
- **Memory**: 1 GB RAM
- **Storage**: Limited
- **Apps**: Up to 3 public apps
- **Uptime**: Apps sleep after inactivity

## Upgrading to Pro

For production use, consider Streamlit Cloud Pro:
- More resources (4 GB RAM)
- Private apps
- Custom domains
- Priority support
- No sleep mode

Visit: https://streamlit.io/cloud

## Best Practices

1. **Keep requirements.txt minimal**
   - Only include necessary packages
   - Pin versions for stability

2. **Optimize performance**
   - Use `@st.cache_data` for expensive computations
   - Load data efficiently
   - Minimize API calls

3. **Security**
   - Don't commit secrets or API keys
   - Use Streamlit Secrets for sensitive data
   - Validate user inputs

4. **Monitoring**
   - Check app analytics in Streamlit Cloud
   - Monitor error logs regularly
   - Test after each deployment

## Additional Resources

- Streamlit Documentation: https://docs.streamlit.io
- Streamlit Cloud Docs: https://docs.streamlit.io/streamlit-community-cloud
- Streamlit Forum: https://discuss.streamlit.io
- GitHub Issues: Report bugs in your repo

## Support

For help with this specific dashboard:
- Email: data-science@conektr.com
- Check README.md for feature documentation
