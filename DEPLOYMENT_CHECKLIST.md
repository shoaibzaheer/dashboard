# Deployment Checklist

Use this checklist to ensure a smooth deployment to Streamlit Cloud.

## Pre-Deployment

- [ ] **Test locally**
  ```bash
  pip install -r requirements.txt
  streamlit run app.py
  ```
  - [ ] App loads without errors
  - [ ] All stages are accessible
  - [ ] Visualizations render correctly
  - [ ] No console errors

- [ ] **Review files**
  - [ ] `app.py` - Main application file
  - [ ] `requirements.txt` - All dependencies listed
  - [ ] `.streamlit/config.toml` - Configuration is correct
  - [ ] `README.md` - Documentation is complete
  - [ ] `.gitignore` - Sensitive files excluded

- [ ] **Check dependencies**
  - [ ] All imports are in requirements.txt
  - [ ] Version numbers are specified
  - [ ] No local-only packages

- [ ] **Code quality**
  - [ ] No hardcoded secrets or API keys
  - [ ] No absolute file paths
  - [ ] Comments are clear
  - [ ] Code is formatted

## GitHub Setup

- [ ] **Create GitHub repository**
  - [ ] Repository is public (for free tier)
  - [ ] Repository name is descriptive
  - [ ] Description is added

- [ ] **Push code**
  ```bash
  git init
  git add .
  git commit -m "Initial deployment"
  git remote add origin <your-repo-url>
  git push -u origin main
  ```
  - [ ] All files are committed
  - [ ] Push is successful
  - [ ] Files visible on GitHub

## Streamlit Cloud Deployment

- [ ] **Sign up/Login**
  - [ ] Account created at share.streamlit.io
  - [ ] GitHub connected
  - [ ] Permissions granted

- [ ] **Deploy app**
  - [ ] Click "New app"
  - [ ] Select correct repository
  - [ ] Branch: `main`
  - [ ] Main file: `app.py`
  - [ ] Custom URL chosen (optional)
  - [ ] Click "Deploy"

- [ ] **Monitor deployment**
  - [ ] Watch build logs
  - [ ] No error messages
  - [ ] Deployment completes successfully

## Post-Deployment

- [ ] **Test deployed app**
  - [ ] App URL is accessible
  - [ ] All stages load correctly
  - [ ] Visualizations work
  - [ ] Navigation functions properly
  - [ ] No console errors

- [ ] **Performance check**
  - [ ] Page load time is acceptable
  - [ ] Interactions are responsive
  - [ ] Charts render smoothly

- [ ] **Share and document**
  - [ ] Copy app URL
  - [ ] Share with stakeholders
  - [ ] Update documentation with URL
  - [ ] Add URL to GitHub repo description

## Maintenance

- [ ] **Set up monitoring**
  - [ ] Check Streamlit Cloud analytics
  - [ ] Monitor error logs
  - [ ] Track usage metrics

- [ ] **Plan updates**
  - [ ] Document update process
  - [ ] Test changes locally first
  - [ ] Use git for version control

## Troubleshooting

If deployment fails, check:

- [ ] Requirements.txt has all dependencies
- [ ] No syntax errors in app.py
- [ ] Python version compatibility (3.8+)
- [ ] File paths are relative, not absolute
- [ ] No missing imports
- [ ] GitHub repo is public
- [ ] Streamlit Cloud logs for specific errors

## Resources

- Streamlit Docs: https://docs.streamlit.io
- Streamlit Cloud: https://docs.streamlit.io/streamlit-community-cloud
- GitHub Help: https://docs.github.com
- Support: data-science@conektr.com

---

**Deployment Date**: _______________

**Deployed By**: _______________

**App URL**: _______________

**Notes**: 
_______________________________________________
_______________________________________________
_______________________________________________
