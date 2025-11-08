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
    
    # Sample customer list
    customers = {
        "12345 - Ahmed Al Mansoori": "12345",
        "23456 - Fatima Al Zaabi": "23456",
        "34567 - Mohammed Al Hashimi": "34567",
        "45678 - Sara Al Mazrouei": "45678",
        "56789 - Ali Al Ketbi": "56789"
    }
    
    col1, col2 = st.columns([2, 1])
    with col1:
        selected_customer = st.selectbox(
            "Select Customer",
            options=list(customers.keys()),
            help="Choose a customer to view their complete profile"
        )
        customer_id = customers[selected_customer]
    
    with col2:
        requested_limit = st.number_input(
            "Requested Credit Limit (AED)",
            value=50000,
            step=5000,
            help="Amount requested by customer"
        )
    
    st.markdown("---")
    
    # Customer Profile Header
    st.markdown(f"### 👤 Customer Profile: {selected_customer.split(' - ')[1]}")
    st.markdown(f"**Customer ID:** {customer_id} | **Application Date:** {datetime.now().strftime('%Y-%m-%d')}")
    
    # Create tabs for different data sources
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📊 Conektr Data",
        "🎯 Risk Profile",
        "🏦 Bank Statements",
        "📈 AECB Score",
        "⚡ DEWA Bills",
        "📄 LOS Documents"
    ])

    
    # TAB 1: Conektr Transaction Data
    with tab1:
        st.markdown("#### 📊 Conektr Transaction Data")
        st.markdown("*Transaction history and business performance metrics*")
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total GMV", "AED 136,282", "+12.3%")
        with col2:
            st.metric("Total Orders", "245", "+8")
        with col3:
            st.metric("Active Months", "11", "")
        with col4:
            st.metric("Last Order", "5 days ago", "")
        
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
                    "AED 556",
                    "22.3 orders/month",
                    "Electronics",
                    "Jan 2023",
                    "0.25 (Low)",
                    "+12.3%"
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

    
    # TAB 2: Risk Profile with SHAP Analysis
    with tab2:
        st.markdown("#### 🎯 Customer Risk Profile & SHAP Analysis")
        st.markdown("*ML model risk assessment with detailed feature explanations*")
        
        # Risk score display
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Risk Score", "0.000123", help="Probability of default")
        with col2:
            risk_category = "Very Low Risk"
            st.markdown(f"**Risk Category**")
            st.markdown(f"<h3 style='color: green;'>{risk_category}</h3>", unsafe_allow_html=True)
        with col3:
            st.metric("Confidence", "98.5%", help="Model confidence level")
        
        st.markdown("---")
        
        # SHAP Feature Analysis
        st.markdown("**🔍 SHAP Feature Analysis - Why This Risk Score?**")
        st.markdown("*Each feature's contribution to the risk prediction*")
        
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
            "Value": [0.25, 5, 1234.5, 136282, 0.75, 11, 22.3, 0.95],
            "SHAP Impact": [-0.0020, -0.0015, -0.0010, -0.0008, -0.0006, -0.0004, -0.0003, -0.0002],
            "Effect": [
                "↓ Reduces Risk",
                "↓ Reduces Risk",
                "↓ Reduces Risk",
                "↓ Reduces Risk",
                "↓ Reduces Risk",
                "↓ Reduces Risk",
                "↓ Reduces Risk",
                "↓ Reduces Risk"
            ],
            "Explanation": [
                "Low volatility indicates stable business",
                "Recent activity shows engagement",
                "Positive growth trend is favorable",
                "High sales volume reduces risk",
                "Consistent behavior is positive",
                "Long tenure indicates stability",
                "Regular orders show reliability",
                "Recent transactions are positive"
            ]
        })
        
        st.dataframe(shap_data, use_container_width=True, hide_index=True)
        
        # SHAP waterfall chart
        fig = go.Figure(go.Waterfall(
            name="SHAP",
            orientation="h",
            y=shap_data["Feature"],
            x=shap_data["SHAP Impact"],
            connector={"line": {"color": "rgb(63, 63, 63)"}},
            decreasing={"marker": {"color": "green"}},
            increasing={"marker": {"color": "red"}},
        ))
        fig.update_layout(
            title="SHAP Feature Contributions (Waterfall)",
            xaxis_title="Impact on Risk Score",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)

    
    # TAB 3: Bank Statement Analysis
    with tab3:
        st.markdown("#### 🏦 Bank Statement Analysis")
        st.markdown("*Cash flow, income, and expense analysis from bank statements*")
        
        # Key financial metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Monthly Income", "AED 18,500", "+5%")
        with col2:
            st.metric("Monthly Expenses", "AED 12,300", "+2%")
        with col3:
            st.metric("Avg Balance", "AED 45,230", "+8%")
        with col4:
            st.metric("Savings Rate", "33.5%", "+3%")
        
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
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)

    
    # TAB 4: AECB Credit Bureau Data
    with tab4:
        st.markdown("#### 📈 AECB Credit Bureau Data")
        st.markdown("*Credit history and bureau information*")
        
        # Credit score display
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Credit Score", "745", "+15")
            st.markdown("<p style='color: green; font-weight: bold;'>Good</p>", unsafe_allow_html=True)
        with col2:
            st.metric("Credit History", "8 years", "")
        with col3:
            st.metric("Active Loans", "2", "")
        with col4:
            st.metric("Credit Utilization", "28%", "-5%")
        
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
            st.metric("Avg Monthly Bill", "AED 850", "+2%")
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
        st.markdown("*Employment verification and KYC documentation*")
        
        # Document verification status
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**Document Verification**")
            st.markdown("✅ **Complete**")
        with col2:
            st.markdown("**KYC Status**")
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

    
    # Loan Recommendations Section
    st.markdown("---")
    st.markdown("### 💡 AI-Powered Loan Recommendations")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Recommended Loan Amount**")
        recommended_amount = min(requested_limit * 1.5, 75000)
        st.markdown(f"<h2 style='color: green;'>AED {recommended_amount:,.0f}</h2>", unsafe_allow_html=True)
        if recommended_amount > requested_limit:
            st.success(f"✅ Customer qualifies for AED {recommended_amount - requested_limit:,.0f} more than requested!")
    
    with col2:
        st.markdown("**Suggested Interest Rate**")
        st.markdown("<h2 style='color: #1f77b4;'>7.5%</h2>", unsafe_allow_html=True)
        st.info("Preferential rate based on risk profile")
    
    with col3:
        st.markdown("**Optimal Tenure**")
        st.markdown("<h2 style='color: #ff7f0e;'>24 months</h2>", unsafe_allow_html=True)
        st.info("Balanced repayment schedule")
    
    # Loan calculation details
    st.markdown("---")
    st.markdown("#### 📊 Loan Calculation Details")
    
    col1, col2 = st.columns(2)
    
    with col1:
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
                "7.5%",
                "24 months",
                f"AED {(recommended_amount * 1.09 / 24):,.0f}",
                f"AED {(recommended_amount * 0.09):,.0f}",
                f"AED {(recommended_amount * 1.09):,.0f}",
                f"AED {(recommended_amount * 0.01):,.0f}",
                "Not Required"
            ]
        })
        st.dataframe(loan_details, use_container_width=True, hide_index=True)
    
    with col2:
        # Debt-to-Income calculation
        monthly_income = 18500
        existing_obligations = 3400
        new_installment = recommended_amount * 1.09 / 24
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

    
    # Final Recommendation
    st.markdown("---")
    st.markdown("### 🎯 Credit Decision Recommendation")
    
    # Decision box
    st.success("""
    ### ✅ RECOMMENDED: APPROVE
    
    **Rationale:**
    - ✅ Very Low Risk Score (0.000123 probability of default)
    - ✅ Excellent payment history across all sources
    - ✅ Stable income and employment (4 years)
    - ✅ Strong cash flow and savings behavior
    - ✅ Good credit score (745) with no delinquencies
    - ✅ 100% on-time utility bill payments
    - ✅ Low volatility and positive growth trend
    - ✅ Healthy debt-to-income ratio (18.4%)
    - ✅ All KYC documents verified
    
    **Suggested Terms:**
    - **Loan Amount:** AED 75,000 (50% higher than requested)
    - **Interest Rate:** 7.5% per annum (preferential rate)
    - **Tenure:** 24 months
    - **Monthly Installment:** AED 3,406
    - **Collateral:** Not required
    - **Processing Fee:** AED 750 (1%)
    
    **Conditions:**
    - Maintain current employment
    - No additional credit inquiries during loan tenure
    - Auto-debit setup for repayments
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
        "Approved": ["AED 75,000", "AED 30,000", "Rejected", "AED 25,000", "AED 60,000"],
        "Decision": ["✅ Approved", "✅ Approved", "❌ Rejected", "✅ Approved", "✅ Approved"],
        "Officer": ["You", "You", "You", "Sarah M.", "Ahmed K."],
        "Risk Score": ["0.000123", "0.002", "0.085", "0.001", "0.003"]
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
