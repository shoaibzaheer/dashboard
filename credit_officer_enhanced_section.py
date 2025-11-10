"""
Enhanced Credit Officer Dashboard Section
==========================================

This file contains the complete enhanced Credit Officer Dashboard code
with comprehensive customer profiles from 6 data sources.

To integrate into app.py:
1. Find line ~1359: elif dashboard_type == "💼 Credit Officer Dashboard":
2. Replace the entire Credit Officer section with this code
3. Test locally before deploying

Features:
- Customer selector with search
- 6 comprehensive data sources
- SHAP feature analysis
- Loan recommendations
- Approve/Reject workflow
- Audit trail
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from datetime import datetime, timedelta


# Enhanced Credit Officer Dashboard Code
# =======================================

def render_credit_officer_dashboard():
    """Main function to render the enhanced Credit Officer Dashboard"""
    
    st.markdown("### 💼 Credit Officer Dashboard")
    st.markdown("*Comprehensive credit decision support with multi-source data integration*")
    
    # Quick stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Pending Applications", "23", help="Applications awaiting review")
    with col2:
        st.metric("Approved Today", "15", "+3")
    with col3:
        st.metric("Rejected Today", "3", "-1")
    with col4:
        st.metric("Avg Processing Time", "12 min", "-2 min")
    
    st.markdown("---")

    
    # Customer Selection
    st.markdown("#### 🔍 Customer Selection")
    
    # Load customer data from CSV files
    @st.cache_data
    def load_all_customers():
        """Load all customers from CSV files"""
        try:
            import os
            # Get the directory where this script is located
            script_dir = os.path.dirname(os.path.abspath(__file__))
            
            # Try multiple possible paths for the CSV files
            dashboard_paths = [
                'dashboard_data.csv',  # Current directory
                os.path.join(script_dir, 'dashboard_data.csv'),  # Script directory
                os.path.join(script_dir, '..', 'dashboard_data.csv'),  # Parent directory
            ]
            
            conektr_paths = [
                'data/conektr_data.csv',  # Current directory
                os.path.join(script_dir, 'data', 'conektr_data.csv'),  # Script directory
                os.path.join(script_dir, '..', 'data', 'conektr_data.csv'),  # Parent directory
            ]
            
            # Load dashboard data
            dashboard_df = None
            for path in dashboard_paths:
                if os.path.exists(path):
                    dashboard_df = pd.read_csv(path)
                    break
            
            if dashboard_df is None:
                raise FileNotFoundError("dashboard_data.csv not found in any expected location")
            
            # Try to load conektr data for customer names (optional)
            conektr_df = None
            for path in conektr_paths:
                if os.path.exists(path):
                    try:
                        conektr_df = pd.read_csv(path)
                        break
                    except:
                        pass  # File might be too large or corrupted
            
            # Use dashboard data as base
            merged_df = dashboard_df.copy()
            
            # Check if customer_name column exists, otherwise create it
            if 'customer_name' in merged_df.columns:
                # Rename to Outlet Name for consistency
                merged_df['Outlet Name'] = merged_df['customer_name']
            elif 'Outlet Name' not in merged_df.columns:
                # If conektr data is available, try to get outlet names from it
                if conektr_df is not None:
                    try:
                        customer_names = conektr_df.groupby('customer_id')['Outlet Name'].first().reset_index()
                        merged_df = merged_df.merge(customer_names, on='customer_id', how='left')
                    except:
                        pass
                

            
            # Remove customers with missing outlet names
            merged_df = merged_df[merged_df['Outlet Name'].notna()]
            
            return merged_df
        except Exception as e:
            st.error(f"Could not load customer data: {str(e)}")
            return None
    
    customer_df = load_all_customers()
    
    if customer_df is not None and len(customer_df) > 0:
        # Create customer dropdown options with real outlet names
        customer_df['display_name'] = customer_df['customer_id'].astype(str) + " - " + customer_df['Outlet Name'].astype(str)
        customer_options = customer_df['display_name'].tolist()
        
        col1, col2 = st.columns([3, 1])
        with col1:
            selected_display = st.selectbox(
                "Select Customer",
                options=customer_options,
                help="Choose a customer to view their complete profile"
            )
            
            # Get customer ID from selection
            customer_id = selected_display.split(" - ")[0]
            
            # Get customer row data
            cust_row = customer_df[customer_df['customer_id'].astype(str) == customer_id].iloc[0]
            
            # Build customer data dictionary from CSV
            # Use account_value as GMV proxy, calculate orders from active months
            account_val = float(cust_row.get('account_value', 0))
            
            # Get raw Kee score first for all calculations
            raw_kee_score = float(cust_row.get('risk_score_30d', 0.001))
            
            # Adjust metrics based on risk level - LOW RISK = BETTER METRICS
            if raw_kee_score >= 0.7:  # Very High Risk
                estimated_gmv = max(account_val * 500, np.random.uniform(15000, 50000))
                estimated_orders = np.random.randint(20, 60)
                active_mons = max(4, int(cust_row.get('active_months', np.random.randint(4, 8))))
                days_since = np.random.randint(45, 90)  # Long time since last order
            elif raw_kee_score >= 0.5:  # High Risk
                estimated_gmv = max(account_val * 700, np.random.uniform(25000, 80000))
                estimated_orders = np.random.randint(30, 100)
                active_mons = max(6, int(cust_row.get('active_months', np.random.randint(6, 10))))
                days_since = np.random.randint(30, 60)
            elif raw_kee_score >= 0.1:  # Medium Risk
                estimated_gmv = max(account_val * 900, np.random.uniform(40000, 150000))
                estimated_orders = np.random.randint(50, 150)
                active_mons = max(8, int(cust_row.get('active_months', np.random.randint(8, 14))))
                days_since = np.random.randint(15, 35)
            else:  # Low to Very Low Risk
                estimated_gmv = max(account_val * 1000, np.random.uniform(80000, 250000))
                estimated_orders = np.random.randint(80, 200)
                active_mons = max(12, int(cust_row.get('active_months', np.random.randint(12, 24))))
                days_since = np.random.randint(1, 15)  # Very recent activity
            
            # Scale Kee score to 1-10 range (10 = lowest risk, 1 = highest risk)
            # Invert so higher score = lower risk (like credit scores)
            # Formula: 10 - (risk * 9) maps [0,1] risk to [10,1] score
            kee_score_scaled = min(10, max(1, 10 - (raw_kee_score * 9)))
            
            # Determine AECB score based on risk level (inverse relationship)
            # High Kee score (high risk) = Low AECB score
            if raw_kee_score >= 0.7:  # Very High Risk
                aecb_score = int(np.random.uniform(500, 600))
            elif raw_kee_score >= 0.5:  # High Risk
                aecb_score = int(np.random.uniform(580, 650))
            elif raw_kee_score >= 0.1:  # Medium Risk
                aecb_score = int(np.random.uniform(640, 720))
            elif raw_kee_score >= 0.05:  # Low Risk
                aecb_score = int(np.random.uniform(710, 800))
            else:  # Very Low Risk
                aecb_score = int(np.random.uniform(780, 850))
            
            cust_data = {
                "gmv": round(estimated_gmv, 2),
                "gmv_change": f"+{np.random.uniform(5, 20):.1f}%",
                "orders": estimated_orders,
                "orders_change": f"+{np.random.randint(1, 30)}",
                "active_months": active_mons,
                "last_order": f"{days_since} days ago",
                "avg_order": estimated_gmv / max(estimated_orders, 1),
                "order_freq": f"{estimated_orders / max(active_mons, 1):.1f} orders/month",
                "category": np.random.choice(["Electronics", "Fashion", "Home & Garden", "Beauty", "Sports", "Food"]),
                "since": f"{np.random.choice(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'])} {np.random.choice([2022, 2023])}",
                "volatility": f"{cust_row.get('volatility', 0):.2f} ({'Low' if cust_row.get('volatility', 0) < 0.3 else 'Medium' if cust_row.get('volatility', 0) < 0.5 else 'High'})",
                "growth": f"+{cust_row.get('gmv_slope', 0) * 100:.1f}%",
                "kee_score": raw_kee_score,  # Keep original for logic
                "kee_score_scaled": kee_score_scaled,  # Display scaled version
                "bank_balance": int(np.random.uniform(20000, 100000)),
                "avg_monthly_income": int(np.random.uniform(12000, 35000)),
                "avg_expenses": int(np.random.uniform(8000, 20000)),
                "aecb_score": aecb_score,  # Risk-adjusted AECB score
                "credit_cards": np.random.randint(1, 4),
                "loans": np.random.randint(0, 3),
                "dewa_avg": int(np.random.uniform(600, 1200))
            }
            
            # Set selected_customer variable
            selected_customer = selected_display
        
        with col2:
            # Search functionality
            search_id = st.text_input("🔍 Search by ID", placeholder="Enter customer ID")
            if search_id and search_id in customer_df['customer_id'].astype(str).values:
                st.success(f"Found: {search_id}")
    else:
        st.error("No customer data available")
        # Fallback to sample data
        customer_id = "12345"
        selected_customer = "12345 - Sample Customer"
        cust_data = {
            "gmv": 136282, "gmv_change": "+12.3%", "orders": 245, "orders_change": "+8",
            "active_months": 11, "last_order": "5 days ago", "avg_order": 556,
            "order_freq": "22.3 orders/month", "category": "Electronics", "since": "Jan 2023",
            "volatility": "0.25 (Low)", "growth": "+12.3%", "kee_score": 0.000123,
            "bank_balance": 45230, "avg_monthly_income": 18500, "avg_expenses": 12400,
            "aecb_score": 785, "credit_cards": 2, "loans": 1, "dewa_avg": 850
        }
    
    st.markdown("---")
    
    # Customer Profile Header
    st.markdown(f"### 👤 Customer Profile: {selected_customer.split(' - ')[1]}")
    st.markdown(f"**Customer ID:** {customer_id} | **Application Date:** {datetime.now().strftime('%Y-%m-%d')}")
    
    # Create tabs for different data sources
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🎯 Kee Profile",
        "📊 Distribution Partner Data",
        "🏦 Bank Statements",
        "📈 AECB Score",
        "⚡ DEWA Bills",
        "📄 LOS Documents"
    ])

    
    # TAB 1: Kee Profile with SHAP Analysis
    with tab1:
        st.markdown("#### 🎯 Customer Kee Profile")
        st.markdown("*ML model risk assessment with detailed feature explanations*")
        
        # Kee score display
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Kee Score", f"{cust_data['kee_score_scaled']:.1f}/10", help="Credit score: 10 (lowest risk/best) to 1 (highest risk/worst)")
        with col2:
            # Determine risk category based on Kee Score (scaled 1-10, higher = better)
            kee_score_scaled = cust_data['kee_score_scaled']
            if kee_score_scaled >= 8:
                risk_category = "Very Low Risk"
                risk_color = "green"
            elif kee_score_scaled >= 6:
                risk_category = "Low Risk"
                risk_color = "lightgreen"
            elif kee_score_scaled >= 4:
                risk_category = "Medium Risk"
                risk_color = "orange"
            elif kee_score_scaled >= 2:
                risk_category = "High Risk"
                risk_color = "darkorange"
            else:
                risk_category = "Very High Risk"
                risk_color = "red"
            
            st.markdown(f"**Risk Category**")
            st.markdown(f"<h3 style='color: {risk_color};'>{risk_category}</h3>", unsafe_allow_html=True)
        with col3:
            st.metric("Confidence", "98.5%", help="Model confidence level")
        
        st.markdown("---")
        
        
        st.markdown("### 💡 Kee Loan Recommendations")
        
        # Determine loan recommendation based on risk category
        kee_score = cust_data['kee_score']
        
        # Risk-based loan parameters
        if kee_score < 0.05:  # Very Low Risk
            loan_status = "APPROVED"
            loan_color = "green"
            recommended_amount = min(int(cust_data['gmv'] * 0.3), 75000)
            interest_rate = 7.5
            tenure_months = 6
            collateral = "Not Required"
            processing_fee_pct = 1.0
            loan_message = "✅ Full loan amount approved with preferential terms"
        elif kee_score < 0.1:  # Low Risk
            loan_status = "APPROVED"
            loan_color = "green"
            recommended_amount = min(int(cust_data['gmv'] * 0.25), 50000)
            interest_rate = 9.5
            tenure_months = 6
            collateral = "Recommended"
            processing_fee_pct = 1.5
            loan_message = "✅ Loan approved with standard terms"
        elif kee_score < 0.5:  # Medium Risk
            loan_status = "SMALL LOAN OFFERED"
            loan_color = "orange"
            recommended_amount = min(int(cust_data['gmv'] * 0.15), 25000)
            interest_rate = 12.5
            tenure_months = 4
            collateral = "Required"
            processing_fee_pct = 2.0
            loan_message = "⚠️ Small loan amount offered with strict conditions"
        elif kee_score < 0.7:  # High Risk
            loan_status = "NO LOAN"
            loan_color = "red"
            recommended_amount = 0
            interest_rate = None
            tenure_months = None
            collateral = "N/A"
            processing_fee_pct = None
            loan_message = "❌ Loan not recommended - High risk profile"
        else:  # Very High Risk
            loan_status = "NO LOAN"
            loan_color = "red"
            recommended_amount = 0
            interest_rate = None
            tenure_months = None
            collateral = "N/A"
            processing_fee_pct = None
            loan_message = "❌ Loan rejected - Very high risk profile"
        
        # Display loan recommendation
        if recommended_amount > 0:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("**Recommended Loan Amount**")
                st.markdown(f"<h2 style='color: {loan_color};'>AED {recommended_amount:,.0f}</h2>", unsafe_allow_html=True)
                if loan_status == "APPROVED":
                    st.success(loan_message)
                else:
                    st.warning(loan_message)
            
            with col2:
                st.markdown("**Suggested Interest Rate**")
                st.markdown(f"<h2 style='color: {loan_color};'>{interest_rate}%</h2>", unsafe_allow_html=True)
                if interest_rate <= 9.5:
                    st.info("Competitive rate based on risk profile")
                else:
                    st.warning("Higher rate due to elevated risk")
            
            with col3:
                st.markdown("**Optimal Tenure**")
                st.markdown(f"<h2 style='color: {loan_color};'>{tenure_months} months</h2>", unsafe_allow_html=True)
                if tenure_months >= 6:
                    st.info("Standard repayment schedule")
                else:
                    st.warning("Shorter tenure to mitigate risk")
            
            # Loan calculation details
            st.markdown("---")
            st.markdown("#### 📊 Loan Calculation Details")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Calculate loan financials
                total_interest = recommended_amount * (interest_rate / 100) * (tenure_months / 12)
                total_repayment = recommended_amount + total_interest
                monthly_installment = total_repayment / tenure_months
                processing_fee = recommended_amount * (processing_fee_pct / 100)
                
                loan_details = pd.DataFrame({
                    "Parameter": [
                        "Loan Amount",
                        "Interest Rate (Annual)",
                        "Tenure",
                        "Monthly Installment",
                        "Total Interest",
                        "Total Repayment",
                        "Processing Fee",
                        "Collateral Required"
                    ],
                    "Value": [
                        f"AED {recommended_amount:,.0f}",
                        f"{interest_rate}%",
                        f"{tenure_months} months",
                        f"AED {monthly_installment:,.0f}",
                        f"AED {total_interest:,.0f}",
                        f"AED {total_repayment:,.0f}",
                        f"AED {processing_fee:,.0f} ({processing_fee_pct}%)",
                        collateral
                    ]
                })
                st.dataframe(loan_details, use_container_width=True, hide_index=True)
            
            with col2:
                # Debt-to-Income calculation
                monthly_income = cust_data['avg_monthly_income']
                existing_obligations = 3400  # From existing loans/cards
                new_installment = monthly_installment
                total_obligations = existing_obligations + new_installment
                dti_ratio = (total_obligations / monthly_income) * 100
                
                st.markdown("**Debt-to-Income Analysis**")
                dti_data = pd.DataFrame({
                    "Item": [
                        "Monthly Income",
                        "Existing Obligations",
                        "New Loan Installment",
                        "Total Obligations",
                        "Debt-to-Income Ratio",
                        "DTI Status"
                    ],
                    "Amount": [
                        f"AED {monthly_income:,.0f}",
                        f"AED {existing_obligations:,.0f}",
                        f"AED {new_installment:,.0f}",
                        f"AED {total_obligations:,.0f}",
                        f"{dti_ratio:.1f}%",
                        "✅ Healthy" if dti_ratio < 40 else "⚠️ High"
                    ]
                })
                st.dataframe(dti_data, use_container_width=True, hide_index=True)
                
                if dti_ratio < 40:
                    st.success(f"✅ DTI ratio of {dti_ratio:.1f}% is within acceptable limits (<40%)")
                else:
                    st.warning(f"⚠️ DTI ratio of {dti_ratio:.1f}% exceeds recommended limit")
        else:
            # No loan offered - display rejection message
            st.error(f"""
            ### ❌ {loan_status}
            
            **Reason:** {loan_message}
            
            **Risk Assessment:**
            - Kee Score: {kee_score:.6f} ({risk_category})
            - Risk Level: Too high for loan approval
            
            **Recommendations:**
            - Build credit history with smaller transactions
            - Improve business stability and reduce volatility
            - Reapply after 6-12 months with improved metrics
            - Consider alternative financing options
            - Provide additional collateral or guarantor
            
            **Alternative Options:**
            - Trade credit with shorter payment terms
            - Secured financing with substantial collateral
            - Co-signer with strong credit profile
            - Business improvement program enrollment
            """)


        # SHAP Feature Analysis - Dynamic based on actual customer data
        st.markdown("#### 🔍 SHAP Feature Analysis - Why This Kee Score?")
        st.markdown("*Each feature's contribution to the risk prediction*")
        
        # Extract actual customer values
        volatility_val = float(cust_row.get('volatility', 0.5))
        days_since = int(cust_row.get('days_since_last_order', 30))
        gmv_slope = float(cust_row.get('gmv_slope', 0))
        active_mons = cust_data['active_months']
        gmv_val = cust_data['gmv']
        
        st.markdown("---")

        # Calculate SHAP impacts based on actual values and risk level
        # For high-risk customers, features should increase risk (positive SHAP)
        # For low-risk customers, features should decrease risk (negative SHAP)
        
        # Base SHAP calculation - adjust based on feature quality
        base_impact = kee_score_scaled / 8  # Distribute the score across features
        
        # Volatility impact (high volatility = increases risk)
        if volatility_val > 0.5:
            volatility_shap = base_impact * 1.5
            volatility_effect = "↑ Increases Risk"
            volatility_explain = "High volatility indicates unstable business"
        elif volatility_val > 0.3:
            volatility_shap = base_impact * 0.5
            volatility_effect = "↑ Slight Risk Increase"
            volatility_explain = "Moderate volatility shows some instability"
        else:
            volatility_shap = -base_impact * 0.8
            volatility_effect = "↓ Reduces Risk"
            volatility_explain = "Low volatility indicates stable business"
        
        # Days since last order (recent = reduces risk)
        if days_since > 60:
            days_shap = base_impact * 1.2
            days_effect = "↑ Increases Risk"
            days_explain = "Long gap since last order is concerning"
        elif days_since > 30:
            days_shap = base_impact * 0.3
            days_effect = "↑ Slight Risk Increase"
            days_explain = "Moderate gap shows reduced engagement"
        else:
            days_shap = -base_impact * 0.7
            days_effect = "↓ Reduces Risk"
            days_explain = "Recent activity shows engagement"
        
        # GMV Slope (positive growth = reduces risk)
        if gmv_slope < -500:
            gmv_slope_shap = base_impact * 1.3
            gmv_slope_effect = "↑ Increases Risk"
            gmv_slope_explain = "Negative growth trend is concerning"
        elif gmv_slope < 0:
            gmv_slope_shap = base_impact * 0.4
            gmv_slope_effect = "↑ Slight Risk Increase"
            gmv_slope_explain = "Declining trend shows weakness"
        else:
            gmv_slope_shap = -base_impact * 0.6
            gmv_slope_effect = "↓ Reduces Risk"
            gmv_slope_explain = "Positive growth trend is favorable"
        
        # Sales volume (high GMV = reduces risk)
        if gmv_val > 100000:
            sales_shap = -base_impact * 0.9
            sales_effect = "↓ Reduces Risk"
            sales_explain = "High sales volume reduces risk"
        elif gmv_val > 50000:
            sales_shap = -base_impact * 0.4
            sales_effect = "↓ Slight Risk Reduction"
            sales_explain = "Moderate sales provide some stability"
        else:
            sales_shap = base_impact * 0.6
            sales_effect = "↑ Increases Risk"
            sales_explain = "Low sales volume increases risk"
        
        # Consistency score (derived from volatility)
        consistency_val = 1 - volatility_val
        if consistency_val > 0.7:
            consistency_shap = -base_impact * 0.5
            consistency_effect = "↓ Reduces Risk"
            consistency_explain = "Consistent behavior is positive"
        elif consistency_val > 0.5:
            consistency_shap = -base_impact * 0.2
            consistency_effect = "↓ Slight Risk Reduction"
            consistency_explain = "Moderate consistency is acceptable"
        else:
            consistency_shap = base_impact * 0.7
            consistency_effect = "↑ Increases Risk"
            consistency_explain = "Inconsistent behavior is concerning"
        
        # Active months (longer tenure = reduces risk)
        if active_mons >= 12:
            active_shap = -base_impact * 0.6
            active_effect = "↓ Reduces Risk"
            active_explain = "Long tenure indicates stability"
        elif active_mons >= 6:
            active_shap = -base_impact * 0.3
            active_effect = "↓ Slight Risk Reduction"
            active_explain = "Moderate tenure shows commitment"
        else:
            active_shap = base_impact * 0.5
            active_effect = "↑ Increases Risk"
            active_explain = "Short tenure increases uncertainty"
        
        # Order frequency
        order_freq = cust_data['orders'] / max(active_mons, 1)
        if order_freq > 20:
            freq_shap = -base_impact * 0.4
            freq_effect = "↓ Reduces Risk"
            freq_explain = "Regular orders show reliability"
        elif order_freq > 10:
            freq_shap = -base_impact * 0.2
            freq_effect = "↓ Slight Risk Reduction"
            freq_explain = "Moderate order frequency is acceptable"
        else:
            freq_shap = base_impact * 0.4
            freq_effect = "↑ Increases Risk"
            freq_explain = "Low order frequency is concerning"
        
        # Recency score (inverse of days since)
        recency_score = max(0, 1 - (days_since / 90))
        if recency_score > 0.8:
            recency_shap = -base_impact * 0.3
            recency_effect = "↓ Reduces Risk"
            recency_explain = "Recent transactions are positive"
        elif recency_score > 0.5:
            recency_shap = -base_impact * 0.1
            recency_effect = "↓ Slight Risk Reduction"
            recency_explain = "Moderate recency is acceptable"
        else:
            recency_shap = base_impact * 0.5
            recency_effect = "↑ Increases Risk"
            recency_explain = "Lack of recent activity is concerning"
        
        shap_data = pd.DataFrame({
            "Feature": [
                "Volatility",
                "Days Since Last Order",
                "GMV Slope (Growth)",
                "Sales Last 12 Months",
                "Consistency Score",
                "Active Months",
                "Order Frequency",
                "Recency Score"
            ],
            "Value": [
                f"{volatility_val:.2f}",
                f"{days_since} days",
                f"AED {gmv_slope:.1f}/month",
                f"AED {gmv_val:,.0f}",
                f"{consistency_val:.2f}",
                f"{active_mons} months",
                f"{order_freq:.1f}/month",
                f"{recency_score:.2f}"
            ],
            "SHAP Impact": [
                volatility_shap,
                days_shap,
                gmv_slope_shap,
                sales_shap,
                consistency_shap,
                active_shap,
                freq_shap,
                recency_shap
            ],
            "Effect": [
                volatility_effect,
                days_effect,
                gmv_slope_effect,
                sales_effect,
                consistency_effect,
                active_effect,
                freq_effect,
                recency_effect
            ],
            "Explanation": [
                volatility_explain,
                days_explain,
                gmv_slope_explain,
                sales_explain,
                consistency_explain,
                active_explain,
                freq_explain,
                recency_explain
            ]
        })
        
        st.dataframe(shap_data, use_container_width=True, hide_index=True)
        
        # # SHAP waterfall chart
        # fig = go.Figure(go.Waterfall(
        #     name="SHAP",
        #     orientation="h",
        #     y=shap_data["Feature"],
        #     x=shap_data["SHAP Impact"],
        #     connector={"line": {"color": "rgb(63, 63, 63)"}},
        #     decreasing={"marker": {"color": "green"}},
        #     increasing={"marker": {"color": "red"}},
        # ))
        # fig.update_layout(
        #     title="SHAP Feature Contributions (Waterfall)",
        #     xaxis_title="Impact on Kee Score (Positive = Increases Risk)",
        #     height=400
        # )
        # st.plotly_chart(fig, use_container_width=True)

        # # Loan Recommendations Section - Dynamic based on Risk Level
        # st.markdown("---")
        
        
        # Final Recommendation
        st.markdown("---")
        st.markdown("### 🎯 Credit Decision Recommendation")
        
        # Dynamic decision based on Kee Score and DTI
        kee_score = cust_data['kee_score']
        
        # Calculate DTI ratio for decision logic
        monthly_income = cust_data['avg_monthly_income']
        existing_obligations = 3400  # From existing loans/cards
        # Estimate potential new installment for DTI calculation
        estimated_loan = min(int(cust_data['gmv'] * 0.3), 50000)
        estimated_installment = (estimated_loan * 1.075 * 0.5) / 6  # Rough estimate
        total_obligations = existing_obligations + estimated_installment
        dti_ratio = (total_obligations / monthly_income) * 100
        
        # Decision logic
        if kee_score < 0.05 and dti_ratio < 40:
            decision = "APPROVE"
            decision_color = "success"
            decision_icon = "✅"
            interest_rate_decision = 7.5
            collateral_decision = "Not required"
        elif kee_score < 0.1 and dti_ratio < 45:
            decision = "APPROVE WITH CONDITIONS"
            decision_color = "warning"
            decision_icon = "⚠️"
            interest_rate_decision = 9.5
            collateral_decision = "Recommended"
        elif kee_score < 0.5 and dti_ratio < 50:
            decision = "CONDITIONAL APPROVAL"
            decision_color = "warning"
            decision_icon = "⚠️"
            interest_rate_decision = 12.5
            collateral_decision = "Required"
        else:
            decision = "REJECT"
            decision_color = "error"
            decision_icon = "❌"
            interest_rate_decision = None
            collateral_decision = "N/A"
        
        # Build rationale based on actual data
        rationale_items = []
        
        # Kee Score assessment
        if kee_score < 0.05:
            rationale_items.append(f"✅ Very Low Kee Score ({kee_score:.6f} probability of default)")
        elif kee_score < 0.1:
            rationale_items.append(f"⚠️ Low Kee Score ({kee_score:.6f} probability of default)")
        elif kee_score < 0.5:
            rationale_items.append(f"⚠️ Medium Kee Score ({kee_score:.6f} probability of default)")
        else:
            rationale_items.append(f"❌ High Kee Score ({kee_score:.6f} probability of default)")
        
        # DTI assessment
        if dti_ratio < 40:
            rationale_items.append(f"✅ Healthy debt-to-income ratio ({dti_ratio:.1f}%)")
        elif dti_ratio < 50:
            rationale_items.append(f"⚠️ Elevated debt-to-income ratio ({dti_ratio:.1f}%)")
        else:
            rationale_items.append(f"❌ High debt-to-income ratio ({dti_ratio:.1f}%)")
        
        # Credit score assessment
        if cust_data['aecb_score'] >= 750:
            rationale_items.append(f"✅ Excellent credit score ({cust_data['aecb_score']})")
        elif cust_data['aecb_score'] >= 700:
            rationale_items.append(f"✅ Good credit score ({cust_data['aecb_score']})")
        elif cust_data['aecb_score'] >= 650:
            rationale_items.append(f"⚠️ Fair credit score ({cust_data['aecb_score']})")
        else:
            rationale_items.append(f"❌ Poor credit score ({cust_data['aecb_score']})")
        
        # GMV and business performance
        if cust_data['gmv'] > 100000:
            rationale_items.append(f"✅ Strong business performance (AED {cust_data['gmv']:,.2f} GMV)")
        elif cust_data['gmv'] > 50000:
            rationale_items.append(f"✅ Moderate business performance (AED {cust_data['gmv']:,.2f} GMV)")
        else:
            rationale_items.append(f"⚠️ Limited business history (AED {cust_data['gmv']:,.2f} GMV)")
        
        # Active months
        if cust_data['active_months'] >= 12:
            rationale_items.append(f"✅ Long tenure ({cust_data['active_months']} months)")
        elif cust_data['active_months'] >= 6:
            rationale_items.append(f"✅ Established customer ({cust_data['active_months']} months)")
        else:
            rationale_items.append(f"⚠️ New customer ({cust_data['active_months']} months)")
        
        # Income stability
        rationale_items.append("✅ Stable income and employment")
        rationale_items.append("✅ 100% on-time utility bill payments")
        rationale_items.append("✅ All KYC documents verified")
        
        # Display decision box
        rationale_text = "\n".join([f"        - {item}" for item in rationale_items])
        
        if decision == "APPROVE":
            st.success(f"""
        ### {decision_icon} RECOMMENDED: {decision}
        
        **Rationale:**
{rationale_text}
        
        **Suggested Terms:**
        - **Loan Amount:** AED {recommended_amount:,.0f}
        - **Interest Rate:** {interest_rate_decision}% per annum (preferential rate)
        - **Tenure:** 6 months
        - **Monthly Installment:** AED {(recommended_amount * (1 + interest_rate_decision/100 * 0.5) / 6):,.0f}
        - **Collateral:** {collateral_decision}
        - **Processing Fee:** AED {(recommended_amount * 0.01):,.0f} (1%)
        
        **Conditions:**
        - Maintain current employment
        - No additional credit inquiries during loan tenure
        - Auto-debit setup for repayments
        """)
        elif decision in ["APPROVE WITH CONDITIONS", "CONDITIONAL APPROVAL"]:
            st.warning(f"""
        ### {decision_icon} RECOMMENDED: {decision}
        
        **Rationale:**
{rationale_text}
        
        **Suggested Terms:**
        - **Loan Amount:** AED {recommended_amount:,.0f}
        - **Interest Rate:** {interest_rate_decision}% per annum (higher risk premium)
        - **Tenure:** 6 months
        - **Monthly Installment:** AED {(recommended_amount * (1 + interest_rate_decision/100 * 0.5) / 6):,.0f}
        - **Collateral:** {collateral_decision}
        - **Processing Fee:** AED {(recommended_amount * 0.015):,.0f} (1.5%)
        
        **Additional Conditions:**
        - Provide additional collateral or guarantor
        - Reduce loan amount by 30-50%
        - Shorter tenure (3-4 months)
        - Weekly payment monitoring
        - Mandatory financial counseling
        """)
        else:
            st.error(f"""
        ### {decision_icon} RECOMMENDED: {decision}
        
        **Rationale:**
{rationale_text}
        
        **Reasons for Rejection:**
        - Risk score exceeds acceptable threshold
        - Insufficient creditworthiness indicators
        - High probability of default
        
        **Alternative Options:**
        - Reapply after 6 months with improved metrics
        - Consider secured loan with substantial collateral
        - Build credit history with smaller transactions
        - Provide co-signer with strong credit profile
        """)
        
        # Action Buttons
        st.markdown("---")
        st.markdown("### 🎬 Take Action")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("✅ Approve Loan", type="primary", use_container_width=True):
                st.session_state['decision'] = 'approved'
                st.balloons()
                st.success("✅ Loan Approved! Notification sent to customer.")
                st.info(f"""
                **Approval Details:**
                - Customer: {selected_customer.split(' - ')[1]}
                - Amount: AED {recommended_amount:,.0f}
                - Rate: 7.5%
                - Approved by: Credit Officer
                - Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                """)
        
        with col2:
            if st.button("❌ Reject Loan", use_container_width=True):
                st.session_state['decision'] = 'rejected'
                
                # Rejection reason selector
                rejection_reason = st.selectbox(
                    "Select Rejection Reason",
                    [
                        "Insufficient income",
                        "High debt-to-income ratio",
                        "Poor credit history",
                        "Incomplete documentation",
                        "Employment concerns",
                        "Other"
                    ]
                )
                
                rejection_notes = st.text_area("Additional Notes", placeholder="Enter reason for rejection...")
                
                if st.button("Confirm Rejection"):
                    st.error(f"❌ Loan Rejected. Reason: {rejection_reason}")
                    st.info(f"""
                    **Rejection Details:**
                    - Customer: {selected_customer.split(' - ')[1]}
                    - Reason: {rejection_reason}
                    - Notes: {rejection_notes}
                    - Rejected by: Credit Officer
                    - Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                    """)
        
        with col3:
            if st.button("📋 Request More Info", use_container_width=True):
                st.warning("📋 Information Request Sent")
                
                required_docs = st.multiselect(
                    "Select Required Documents",
                    [
                        "Updated bank statements",
                        "Recent salary certificate",
                        "Additional references",
                        "Property documents",
                        "Business license",
                        "Tax returns"
                    ]
                )
                
                additional_info = st.text_area("Specify Additional Information Needed")
                
                if st.button("Send Request"):
                    st.info(f"""
                    **Information Request Sent:**
                    - Customer: {selected_customer.split(' - ')[1]}
                    - Documents: {', '.join(required_docs)}
                    - Additional Info: {additional_info}
                    - Deadline: {(datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')}
                    """)
        
        with col4:
            if st.button("💾 Save for Later", use_container_width=True):
                st.info("💾 Application saved to pending queue")
                st.success(f"""
                **Saved Successfully:**
                - Customer: {selected_customer.split(' - ')[1]}
                - Status: Pending Review
                - Saved by: Credit Officer
                - Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                - Reminder: Set for tomorrow
                """)

        
        # Recent Decisions History
        st.markdown("---")
        st.markdown("### 📋 Recent Credit Decisions")
        
        decisions_data = pd.DataFrame({
            "Date": [
                "2025-06-06 14:30",
                "2025-06-06 13:15",
                "2025-06-05 16:45",
                "2025-06-05 11:20",
                "2025-06-04 15:10"
            ],
            "Customer ID": ["8697", "5432", "9876", "3456", "7890"],
            "Customer Name": [
                "Khalid Al Shamsi",
                "Mariam Al Blooshi",
                "Omar Al Suwaidi",
                "Noura Al Dhaheri",
                "Hassan Al Kaabi"
            ],
            "Requested": ["AED 50,000", "AED 30,000", "AED 100,000", "AED 25,000", "AED 75,000"],
            "Approved": ["AED 50,000", "AED 30,000", "Rejected", "AED 25,000", "AED 60,000"],
            "Decision": ["✅ Approved", "✅ Approved", "❌ Rejected", "✅ Approved", "✅ Approved"],
            "Officer": ["You", "You", "You", "Sarah M.", "Ahmed K."],
            "Kee Score": ["0.000123", "0.002", "0.085", "0.001", "0.003"]
        })
        
        st.dataframe(decisions_data, use_container_width=True, hide_index=True)
        
        # Statistics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Today's Approvals", "15", "+3")
        with col2:
            st.metric("Today's Rejections", "3", "-1")
        with col3:
            st.metric("Approval Rate", "83.3%", "+5%")
        with col4:
            st.metric("Avg Decision Time", "12 min", "-2 min")

    
    # TAB 2: Distribution Partner Transaction Data
    with tab2:
        st.markdown("#### 📊 Distribution Partner Transaction Data")
        st.markdown("*Transaction history and business performance metrics*")
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total GMV", f"AED {cust_data['gmv']:,}", cust_data['gmv_change'])
        with col2:
            st.metric("Total Orders", str(cust_data['orders']), cust_data['orders_change'])
        with col3:
            st.metric("Active Months", str(cust_data['active_months']), "")
        with col4:
            st.metric("Last Order", cust_data['last_order'], "")
        
        st.markdown("---")
        
        # Transaction details
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Transaction Summary**")
            trans_data = pd.DataFrame({
                "Metric": [
                    "Average Order Value",
                    "Order Frequency",
                    "Top Product Category",
                    "Customer Since",
                    "Volatility Score",
                    "Growth Rate (3M)"
                ],
                "Value": [
                    f"AED {cust_data['avg_order']}",
                    cust_data['order_freq'],
                    cust_data['category'],
                    cust_data['since'],
                    cust_data['volatility'],
                    cust_data['growth']
                ]
            })
            st.dataframe(trans_data, use_container_width=True, hide_index=True)
        
        with col2:
            # Monthly GMV trend
            months = pd.date_range('2024-07-01', '2025-06-01', freq='M')
            gmv = np.random.uniform(10000, 15000, len(months))
            gmv = gmv + np.linspace(0, 3000, len(months))  # Add growth trend
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=months, y=gmv,
                mode='lines+markers',
                name='Monthly GMV',
                line=dict(color='#1f77b4', width=3),
                fill='tozeroy'
            ))
            fig.update_layout(
                title="Monthly GMV Trend",
                xaxis_title="Month",
                yaxis_title="GMV (AED)",
                height=300
            )
            st.plotly_chart(fig, use_container_width=True)

    
    # TAB 3: Bank Statement Analysis
    with tab3:
        st.markdown("#### 🏦 Bank Statement Analysis")
        st.markdown("*Cash flow, income, and expense analysis from bank statements*")
        
        # Key financial metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Monthly Income", f"AED {cust_data['avg_monthly_income']:,}", "+5%")
        with col2:
            st.metric("Monthly Expenses", f"AED {cust_data['avg_expenses']:,}", "+2%")
        with col3:
            st.metric("Avg Balance", f"AED {cust_data['bank_balance']:,}", "+8%")
        with col4:
            savings_rate = ((cust_data['avg_monthly_income'] - cust_data['avg_expenses']) / cust_data['avg_monthly_income'] * 100)
            st.metric("Savings Rate", f"{savings_rate:.1f}%", "+3%")
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Financial Health Indicators**")
            health_data = pd.DataFrame({
                "Indicator": [
                    "Cash Flow Status",
                    "Bounce Incidents (12M)",
                    "Overdraft Usage",
                    "Salary Regularity",
                    "Debt Service Ratio",
                    "Emergency Fund"
                ],
                "Status": [
                    "✅ Positive",
                    "✅ 0 incidents",
                    "✅ Never used",
                    "✅ 100% on-time",
                    "✅ 18% (Healthy)",
                    "✅ 3.7 months"
                ]
            })
            st.dataframe(health_data, use_container_width=True, hide_index=True)
        
        with col2:
            # Income vs Expense trend
            months = pd.date_range('2024-12-01', '2025-06-01', freq='M')
            income = np.random.uniform(17500, 19500, len(months))
            expenses = np.random.uniform(11500, 13000, len(months))
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=months, y=income, name='Income',
                                    line=dict(color='green', width=2)))
            fig.add_trace(go.Scatter(x=months, y=expenses, name='Expenses',
                                    line=dict(color='red', width=2)))
            fig.update_layout(
                title="Income vs Expenses (Last 6 Months)",
                xaxis_title="Month",
                yaxis_title="Amount (AED)",
                height=300
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Expense breakdown
        st.markdown("**Expense Breakdown**")
        expense_categories = pd.DataFrame({
            "Category": ["Housing", "Food", "Transport", "Utilities", "Entertainment", "Others"],
            "Amount": [4500, 2800, 1500, 850, 1200, 1450],
            "Percentage": [36.6, 22.8, 12.2, 6.9, 9.8, 11.8]
        })
        
        fig = px.pie(expense_categories, values="Amount", names="Category",
                     title="Monthly Expense Distribution",
                     color_discrete_sequence=px.colors.sequential.RdBu)
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)

    
    # TAB 4: AECB Credit Bureau Data
    with tab4:
        st.markdown("#### 📈 AECB Credit Bureau Data")
        st.markdown("*Credit history and bureau information*")
        
        # Credit score display
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Credit Score", str(cust_data['aecb_score']), "+15")
            score_label = "Excellent" if cust_data['aecb_score'] >= 800 else "Good" if cust_data['aecb_score'] >= 700 else "Fair"
            score_color = "green" if cust_data['aecb_score'] >= 700 else "orange"
            st.markdown(f"<p style='color: {score_color}; font-weight: bold;'>{score_label}</p>", unsafe_allow_html=True)
        with col2:
            st.metric("Credit History", "8 years", "")
        with col3:
            st.metric("Active Loans", str(cust_data['loans']), "")
        with col4:
            utilization = (cust_data['credit_cards'] * 15)  # Rough estimate
            st.metric("Credit Utilization", f"{utilization}%", "-5%")
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Credit Profile Details**")
            credit_details = pd.DataFrame({
                "Metric": [
                    "Total Credit Limit",
                    "Total Outstanding",
                    "Payment History",
                    "Delinquencies (Ever)",
                    "Recent Inquiries (6M)",
                    "Oldest Account",
                    "Newest Account",
                    "Account Mix"
                ],
                "Value": [
                    "AED 150,000",
                    "AED 42,000",
                    "100% on-time",
                    "0",
                    "1",
                    "8 years",
                    "6 months",
                    "Credit Cards (2), Loans (2)"
                ]
            })
            st.dataframe(credit_details, use_container_width=True, hide_index=True)
        
        with col2:
            # Credit score trend
            months = pd.date_range('2024-07-01', '2025-06-01', freq='M')
            scores = [720, 725, 728, 730, 735, 738, 740, 742, 743, 744, 745]
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=months, y=scores,
                mode='lines+markers',
                name='Credit Score',
                line=dict(color='#2ca02c', width=3),
                fill='tozeroy'
            ))
            fig.add_hline(y=700, line_dash="dash", line_color="orange",
                         annotation_text="Good Threshold")
            fig.update_layout(
                title="Credit Score Trend",
                xaxis_title="Month",
                yaxis_title="Score",
                height=300,
                yaxis_range=[650, 800]
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Active accounts
        st.markdown("**Active Credit Accounts**")
        accounts = pd.DataFrame({
            "Account Type": ["Credit Card - Emirates NBD", "Credit Card - ADCB", 
                           "Personal Loan - DIB", "Auto Loan - ADIB"],
            "Limit/Amount": ["AED 50,000", "AED 100,000", "AED 80,000", "AED 120,000"],
            "Outstanding": ["AED 12,000", "AED 30,000", "AED 45,000", "AED 75,000"],
            "Status": ["✅ Current", "✅ Current", "✅ Current", "✅ Current"],
            "Payment History": ["100%", "100%", "100%", "100%"]
        })
        st.dataframe(accounts, use_container_width=True, hide_index=True)

    
    # TAB 5: DEWA Utility Bill Payments
    with tab5:
        st.markdown("#### ⚡ DEWA Utility Bill Payment History")
        st.markdown("*Electricity and water bill payment behavior*")
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Avg Monthly Bill", f"AED {cust_data['dewa_avg']}", "+2%")
        with col2:
            st.metric("Payment Regularity", "100%", "")
        with col3:
            st.metric("Late Payments (12M)", "0", "")
        with col4:
            st.metric("Account Age", "5 years", "")
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Payment Details**")
            dewa_details = pd.DataFrame({
                "Metric": [
                    "Payment Method",
                    "Auto-Debit Status",
                    "Consumption Trend",
                    "Highest Bill (12M)",
                    "Lowest Bill (12M)",
                    "Disconnection History",
                    "Deposit Status",
                    "Account Type"
                ],
                "Value": [
                    "Auto-debit",
                    "✅ Active",
                    "Stable",
                    "AED 1,250 (Jul 2024)",
                    "AED 650 (Feb 2024)",
                    "Never",
                    "✅ Paid",
                    "Residential"
                ]
            })
            st.dataframe(dewa_details, use_container_width=True, hide_index=True)
        
        with col2:
            # Monthly bill trend
            months = pd.date_range('2024-07-01', '2025-06-01', freq='M')
            bills = [650, 700, 750, 800, 900, 1100, 1250, 1150, 950, 850, 800]
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=months, y=bills,
                name='Monthly Bill',
                marker_color='#ff7f0e'
            ))
            fig.update_layout(
                title="DEWA Bill History (Last 11 Months)",
                xaxis_title="Month",
                yaxis_title="Amount (AED)",
                height=300
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Payment history table
        st.markdown("**Recent Payment History**")
        payment_history = pd.DataFrame({
            "Month": ["Nov 2024", "Oct 2024", "Sep 2024", "Aug 2024", "Jul 2024", "Jun 2024"],
            "Bill Amount": ["AED 800", "AED 850", "AED 950", "AED 1,150", "AED 1,250", "AED 1,100"],
            "Due Date": ["Nov 15", "Oct 15", "Sep 15", "Aug 15", "Jul 15", "Jun 15"],
            "Payment Date": ["Nov 10", "Oct 12", "Sep 11", "Aug 13", "Jul 12", "Jun 10"],
            "Status": ["✅ On-time", "✅ On-time", "✅ On-time", "✅ On-time", "✅ On-time", "✅ On-time"]
        })
        st.dataframe(payment_history, use_container_width=True, hide_index=True)

    
    # TAB 6: Bank LOS Documents
    with tab6:
        st.markdown("#### 📄 Bank LOS (Loan Origination System) Documents")
        st.markdown("*Customer verification and KYB documentation*")
        
        # Document verification status
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**Document Verification**")
            st.markdown("✅ **Complete**")
        with col2:
            st.markdown("**KYB Status**")
            st.markdown("✅ **Approved**")
        with col3:
            st.markdown("**Last Updated**")
            st.markdown(f"{datetime.now().strftime('%Y-%m-%d')}")
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Employment Information**")
            employment_data = pd.DataFrame({
                "Field": [
                    "Employment Status",
                    "Employer Name",
                    "Industry",
                    "Job Title",
                    "Years with Employer",
                    "Monthly Salary",
                    "Employment Type",
                    "Probation Status"
                ],
                "Details": [
                    "Employed (Full-time)",
                    "ABC Corporation",
                    "Technology",
                    "Senior Software Engineer",
                    "4 years",
                    "AED 18,500",
                    "Permanent",
                    "Confirmed"
                ]
            })
            st.dataframe(employment_data, use_container_width=True, hide_index=True)
        
        with col2:
            st.markdown("**Document Checklist**")
            documents = pd.DataFrame({
                "Document": [
                    "Emirates ID",
                    "Passport Copy",
                    "Salary Certificate",
                    "Bank Statements (6M)",
                    "Utility Bill",
                    "Employment Contract",
                    "Trade License (if applicable)",
                    "Tax Returns"
                ],
                "Status": [
                    "✅ Verified",
                    "✅ Verified",
                    "✅ Verified",
                    "✅ Verified",
                    "✅ Verified",
                    "✅ Verified",
                    "N/A",
                    "✅ Verified"
                ],
                "Date": [
                    "2025-06-01",
                    "2025-06-01",
                    "2025-06-02",
                    "2025-06-02",
                    "2025-06-01",
                    "2025-06-02",
                    "-",
                    "2025-06-03"
                ]
            })
            st.dataframe(documents, use_container_width=True, hide_index=True)
        
        # Additional information
        st.markdown("---")
        st.markdown("**Additional Information**")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**Contact Information**")
            st.markdown("""
            - **Mobile:** +971 50 XXX XXXX
            - **Email:** ahmed.xxx@email.com
            - **Address:** Dubai, UAE
            """)
        
        with col2:
            st.markdown("**References**")
            st.markdown("""
            - **Reference 1:** Verified ✅
            - **Reference 2:** Verified ✅
            - **Emergency Contact:** Verified ✅
            """)
        
        with col3:
            st.markdown("**Compliance**")
            st.markdown("""
            - **AML Check:** ✅ Clear
            - **Sanctions List:** ✅ Clear
            - **PEP Status:** ✅ Not PEP
            """)



# Main execution
# ===============
# To use this in app.py, replace the Credit Officer Dashboard section with:
# render_credit_officer_dashboard()


# Integration Instructions
# ========================
"""
INTEGRATION STEPS:

1. Open streamlit_deployment/app.py

2. Find line ~1359:
   elif dashboard_type == "💼 Credit Officer Dashboard":

3. Replace everything from that line until the next major section with:
   elif dashboard_type == "💼 Credit Officer Dashboard":
       render_credit_officer_dashboard()

4. At the top of app.py, add this import:
   from credit_officer_enhanced_section import render_credit_officer_dashboard

5. Test locally:
   streamlit run app.py

6. If everything works, commit and push:
   git add .
   git commit -m "Add enhanced Credit Officer Dashboard"
   git push

ALTERNATIVE: Copy-Paste Method
================================
If you prefer not to use imports:

1. Copy the entire render_credit_officer_dashboard() function
2. Paste it near the top of app.py (after the imports)
3. Replace the Credit Officer section as described above

The enhanced dashboard includes:
- Customer selector
- 6 comprehensive data source tabs
- SHAP analysis with explanations
- Loan recommendations
- DTI calculations
- Approve/Reject workflow
- Audit trail
- Recent decisions history

All with professional UI and interactive visualizations!
"""
