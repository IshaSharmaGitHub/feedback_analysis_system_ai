"""
Streamlit Dashboard for Intelligent Feedback Analysis System
"""

import streamlit as st
import pandas as pd
import os
from datetime import datetime
import json
from feedback_analysis_system import FeedbackAnalysisSystem

# Page configuration
st.set_page_config(
    page_title="Feedback Analysis Dashboard",
    page_icon="🎯",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        color: #856404;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'system' not in st.session_state:
    st.session_state.system = None
if 'processing_complete' not in st.session_state:
    st.session_state.processing_complete = False
if 'tickets_df' not in st.session_state:
    st.session_state.tickets_df = None

# Header
st.markdown('<h1 class="main-header">🎯 Intelligent Feedback Analysis Dashboard</h1>', unsafe_allow_html=True)

# Sidebar - Configuration Panel
st.sidebar.header("⚙️ Configuration")

# Check for API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.sidebar.error("❌ OPENAI_API_KEY not found")
    st.sidebar.info("Please set your OpenAI API key in a .env file")
else:
    st.sidebar.success("✅ API Key configured")

# Processing settings
st.sidebar.subheader("Processing Settings")
process_limit = st.sidebar.number_input(
    "Max items to process (0 = all)",
    min_value=0,
    max_value=100,
    value=5,
    help="Limit the number of feedback items to process (0 for all)"
)

classification_confidence = st.sidebar.slider(
    "Classification Confidence Threshold",
    min_value=0,
    max_value=100,
    value=70,
    help="Minimum confidence score for classifications"
)

# Priority settings
st.sidebar.subheader("Priority Rules")
critical_keywords = st.sidebar.text_area(
    "Critical Keywords",
    value="crash, data loss, can't login, critical, urgent",
    help="Comma-separated keywords that trigger Critical priority"
)

high_keywords = st.sidebar.text_area(
    "High Keywords",
    value="bug, error, broken, not working, fails",
    help="Comma-separated keywords that trigger High priority"
)

# Main content area
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Dashboard",
    "🚀 Process Feedback",
    "🎫 Generated Tickets",
    "📈 Analytics",
    "🔍 Manual Review"
])

# Tab 1: Dashboard Overview
with tab1:
    st.header("System Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    # Load data to show stats
    try:
        reviews_df = pd.read_csv("data/app_store_reviews.csv")
        emails_df = pd.read_csv("data/support_emails.csv")
        
        with col1:
            st.metric("📱 App Reviews", len(reviews_df))
        with col2:
            st.metric("📧 Support Emails", len(emails_df))
        with col3:
            total_feedback = len(reviews_df) + len(emails_df)
            st.metric("📝 Total Feedback", total_feedback)
        with col4:
            if os.path.exists("output/generated_tickets.csv"):
                tickets_df = pd.read_csv("output/generated_tickets.csv")
                st.metric("🎫 Tickets Generated", len(tickets_df))
            else:
                st.metric("🎫 Tickets Generated", 0)
        
        st.divider()
        
        # Show recent reviews
        st.subheader("📱 Recent App Reviews")
        st.dataframe(reviews_df.head(10), use_container_width=True)
        
        st.subheader("📧 Recent Support Emails")
        st.dataframe(emails_df.head(10), use_container_width=True)
        
    except FileNotFoundError:
        st.error("❌ CSV files not found. Please ensure app_store_reviews.csv and support_emails.csv exist.")

# Tab 2: Process Feedback
with tab2:
    st.header("🚀 Process Feedback")
    
    st.markdown("""
    This will run the multi-agent system to:
    1. ✅ Load feedback from CSV files
    2. 🔍 Classify feedback (Bug/Feature/Praise/Complaint/Spam)
    3. 🔬 Analyze with specialized agents:
       • Bug Analyzer for bugs
       • Feature Extractor for feature requests
       • General analysis for other types
    4. 🎫 Generate structured tickets
    5. ✔️ Quality review of generated tickets
    6. 💾 Save results to CSV files
    """)
    
    if st.button("▶️ Start Processing", type="primary", use_container_width=True):
        if not api_key:
            st.error("❌ Cannot process: OpenAI API key not configured")
        else:
            with st.spinner("🔄 Initializing multi-agent system..."):
                try:
                    st.session_state.system = FeedbackAnalysisSystem()
                    st.success("✅ System initialized")
                except Exception as e:
                    st.error(f"❌ Initialization error: {e}")
                    st.stop()
            
            # Load data
            with st.spinner("📂 Loading feedback data..."):
                if st.session_state.system.load_data():
                    total_items = len(st.session_state.system.all_feedback)
                    items_to_process = process_limit if process_limit > 0 else total_items
                    st.success(f"✅ Loaded {total_items} feedback items")
                    st.info(f"📊 Will process {items_to_process} items")
                else:
                    st.error("❌ Failed to load data")
                    st.stop()
            
            # Process feedback
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            feedback_to_process = (st.session_state.system.all_feedback[:process_limit] 
                                  if process_limit > 0 
                                  else st.session_state.system.all_feedback)
            
            for idx, feedback in enumerate(feedback_to_process, 1):
                status_text.text(f"Processing {idx}/{len(feedback_to_process)}: {feedback['source_id']}")
                progress_bar.progress(idx / len(feedback_to_process))
                
                ticket = st.session_state.system.process_feedback_item(feedback)
                
                if ticket:
                    st.session_state.system.generated_tickets.append(ticket)
                
            progress_bar.progress(100)
            status_text.text("✅ Processing complete!")
            
            # Save results
            with st.spinner("💾 Saving results..."):
                st.session_state.system.save_results()
            
            st.session_state.processing_complete = True
            
            st.balloons()
            st.success(f"🎉 Successfully processed {len(st.session_state.system.generated_tickets)} feedback items!")
            
            # Show summary
            st.subheader("📊 Processing Summary")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Processed", len(feedback_to_process))
            with col2:
                st.metric("Tickets Generated", len(st.session_state.system.generated_tickets))
            with col3:
                success_rate = len(st.session_state.system.generated_tickets) / len(feedback_to_process) * 100
                st.metric("Success Rate", f"{success_rate:.1f}%")

# Tab 3: Generated Tickets
with tab3:
    st.header("🎫 Generated Tickets")
    
    if os.path.exists("output/generated_tickets.csv"):
        tickets_df = pd.read_csv("output/generated_tickets.csv")
        st.session_state.tickets_df = tickets_df
        
        st.success(f"✅ {len(tickets_df)} tickets generated")
        
        # Filter options
        col1, col2 = st.columns(2)
        with col1:
            source_filter = st.multiselect(
                "Filter by Source Type",
                options=tickets_df['source_type'].unique(),
                default=tickets_df['source_type'].unique()
            )
        
        # Apply filters
        filtered_df = tickets_df[tickets_df['source_type'].isin(source_filter)]
        
        # Display tickets
        st.dataframe(filtered_df, use_container_width=True, height=400)
        
        # Download button
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Tickets CSV",
            data=csv,
            file_name=f"tickets_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
        
        # Show individual tickets
        st.subheader("📋 Ticket Details")
        selected_ticket = st.selectbox(
            "Select ticket to view",
            options=filtered_df['source_id'].tolist()
        )
        
        if selected_ticket:
            ticket_data = filtered_df[filtered_df['source_id'] == selected_ticket].iloc[0]
            
            st.markdown(f"**Source ID:** {ticket_data['source_id']}")
            st.markdown(f"**Source Type:** {ticket_data['source_type']}")
            st.markdown(f"**Created At:** {ticket_data['created_at']}")
            
            st.text_area("Original Content", ticket_data['original_content'], height=100, key="view_original_content")
            st.text_area("Processing Result", ticket_data['processing_result'], height=300, key="view_processing_result")
    else:
        st.info("ℹ️ No tickets generated yet. Go to 'Process Feedback' tab to start processing.")

# Tab 4: Analytics
with tab4:
    st.header("📈 Analytics & Metrics")
    
    if os.path.exists("output/metrics.csv"):
        metrics_df = pd.read_csv("output/metrics.csv")
        
        st.subheader("Overall Metrics")
        latest_metrics = metrics_df.iloc[-1]
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Feedback", latest_metrics['total_feedback'])
        with col2:
            st.metric("Tickets Generated", latest_metrics['tickets_generated'])
        with col3:
            st.metric("Success Rate", latest_metrics['success_rate'])
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Reviews Processed", latest_metrics['reviews_processed'])
        with col2:
            st.metric("Emails Processed", latest_metrics['emails_processed'])
        
        st.divider()
        st.subheader("Processing History")
        st.dataframe(metrics_df, use_container_width=True)
    else:
        st.info("ℹ️ No metrics available yet.")
    
    # Processing logs
    if os.path.exists("output/processing_log.csv"):
        st.subheader("📜 Processing Logs")
        logs_df = pd.read_csv("output/processing_log.csv")
        
        # Filter logs
        log_action_filter = st.multiselect(
            "Filter by Action",
            options=logs_df['action'].unique(),
            default=logs_df['action'].unique()
        )
        
        filtered_logs = logs_df[logs_df['action'].isin(log_action_filter)]
        st.dataframe(filtered_logs, use_container_width=True, height=300)

# Tab 5: Manual Review
with tab5:
    st.header("🔍 Manual Review & Override")
    
    st.markdown("""
    Use this section to manually review and edit generated tickets before they are finalized.
    """)
    
    if st.session_state.tickets_df is not None:
        tickets_df = st.session_state.tickets_df
        
        # Select ticket to edit
        ticket_to_edit = st.selectbox(
            "Select ticket to review",
            options=tickets_df['source_id'].tolist(),
            key="edit_ticket_selector"
        )
        
        if ticket_to_edit:
            ticket_data = tickets_df[tickets_df['source_id'] == ticket_to_edit].iloc[0]
            
            st.subheader("Edit Ticket")
            
            col1, col2 = st.columns(2)
            
            with col1:
                new_source_id = st.text_input("Source ID", value=ticket_data['source_id'])
                new_source_type = st.selectbox(
                    "Source Type",
                    options=['app_review', 'support_email'],
                    index=0 if ticket_data['source_type'] == 'app_review' else 1
                )
            
            with col2:
                new_created_at = st.text_input("Created At", value=ticket_data['created_at'])
            
            new_original_content = st.text_area(
                "Original Content",
                value=ticket_data['original_content'],
                height=150,
                key="edit_original_content"
            )
            
            new_processing_result = st.text_area(
                "Processing Result",
                value=ticket_data['processing_result'],
                height=300,
                key="edit_processing_result"
            )
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("💾 Save Changes", type="primary"):
                    st.success("✅ Changes saved (feature in development)")
            
            with col2:
                if st.button("✅ Approve Ticket"):
                    st.success("✅ Ticket approved")
            
            with col3:
                if st.button("🗑️ Delete Ticket", type="secondary"):
                    st.warning("⚠️ Ticket deleted (feature in development)")
    else:
        st.info("ℹ️ No tickets available for review. Process feedback first.")

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>Intelligent User Feedback Analysis System | Multi-Agent AI | Powered by CrewAI</p>
</div>
""", unsafe_allow_html=True)
