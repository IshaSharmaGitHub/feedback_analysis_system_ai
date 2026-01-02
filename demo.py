"""
Complete Demo and Presentation Script
Demonstrates all system capabilities
"""

import os
import time
from datetime import datetime


class SystemDemo:
    """Comprehensive system demonstration"""
    
    def __init__(self):
        self.demo_steps = [
            "System Overview",
            "Data Inspection",
            "Agent Architecture",
            "Processing Demo",
            "Results Analysis",
            "Validation",
            "Dashboard Tour"
        ]
    
    def print_header(self, title):
        """Print formatted header"""
        print("\n" + "="*70)
        print(f" {title}")
        print("="*70 + "\n")
    
    def print_section(self, title):
        """Print section header"""
        print(f"\n{'─'*70}")
        print(f"  {title}")
        print(f"{'─'*70}\n")
    
    def step_1_overview(self):
        """System overview"""
        self.print_header("STEP 1: SYSTEM OVERVIEW")
        
        print("""
🎯 INTELLIGENT USER FEEDBACK ANALYSIS AND ACTION SYSTEM

Business Problem:
- Manual triaging of user feedback is slow and inconsistent
- Critical bugs get missed
- Feature requests are delayed
- Poor prioritization across teams

Our Solution:
- Multi-agent AI system using CrewAI
- Automatic classification and prioritization
- Structured ticket generation
- Quality assurance built-in
- Web dashboard for monitoring

Key Metrics:
- Processes 7 feedback items (5 reviews + 2 emails)
- Expected 90-95% classification accuracy
- Reduces 1-2 hours daily work to minutes
- Consistent formatting and prioritization
        """)
        
        input("\nPress Enter to continue...")
    
    def step_2_data_inspection(self):
        """Inspect data files"""
        self.print_header("STEP 2: DATA INSPECTION")
        
        try:
            import pandas as pd
            
            # App Store Reviews
            self.print_section("App Store Reviews Sample")
            reviews_df = pd.read_csv('app_store_reviews.csv')
            print(f"Total Reviews: {len(reviews_df)}")
            print(f"\nRating Distribution:")
            print(reviews_df['rating'].value_counts().sort_index())
            print(f"\nPlatform Distribution:")
            print(reviews_df['platform'].value_counts())
            print(f"\nSample Reviews:")
            print(reviews_df[['review_id', 'rating', 'review_text']].head(3).to_string())
            
            # Support Emails
            self.print_section("Support Emails Sample")
            emails_df = pd.read_csv('support_emails.csv')
            print(f"Total Emails: {len(emails_df)}")
            print(f"\nSample Emails:")
            print(emails_df[['email_id', 'subject']].head(3).to_string())
            
            # Expected Classifications
            self.print_section("Expected Classifications Distribution")
            expected_df = pd.read_csv('expected_classifications.csv')
            print(f"\nCategory Distribution:")
            print(expected_df['category'].value_counts())
            print(f"\nPriority Distribution:")
            print(expected_df['priority'].value_counts())
            
        except Exception as e:
            print(f"❌ Error loading data: {e}")
        
        input("\nPress Enter to continue...")
    
    def step_3_agent_architecture(self):
        """Explain agent architecture"""
        self.print_header("STEP 3: MULTI-AGENT ARCHITECTURE")
        
        print("""
🤖 SIX SPECIALIZED AGENTS:

1. CSV Reader Agent
   Role: Data parsing specialist
   Goal: Read and parse feedback from CSV files accurately
   Skills: Data integrity, format handling, edge case management

2. Feedback Classifier Agent
   Role: NLP classification expert
   Goal: Categorize feedback (Bug/Feature/Praise/Complaint/Spam)
   Skills: Sentiment analysis, intent detection, keyword extraction

3. Bug Analysis Agent
   Role: QA engineer
   Goal: Extract technical details from bug reports
   Skills: Device info extraction, severity assessment, reproduction steps

4. Feature Extractor Agent
   Role: Product analyst
   Goal: Analyze feature requests and estimate user impact
   Skills: User needs analysis, impact assessment, pattern recognition

5. Ticket Creator Agent
   Role: Project manager
   Goal: Generate structured, actionable tickets
   Skills: Clear writing, prioritization, metadata tagging

6. Quality Critic Agent
   Role: QA reviewer
   Goal: Review tickets for completeness and accuracy
   Skills: Quality checking, consistency validation, improvement suggestions

🔄 WORKFLOW:
Input → CSV Reader → Classifier → [Bug Analyzer OR Feature Extractor] → Ticket Creator → Quality Critic → Output

Note: After classification, the system uses:
- Bug Analyzer Agent for bugs
- Feature Extractor Agent for feature requests
- General analysis for praise, complaints, and spam
        """)
        
        input("\nPress Enter to continue...")
    
    def step_4_processing_demo(self):
        """Run processing demo"""
        self.print_header("STEP 4: PROCESSING DEMONSTRATION")
        
        print("Running system with limited feedback (3 items for demo)...\n")
        
        response = input("Start processing? (y/n): ").lower().strip()
        
        if response == 'y':
            try:
                from feedback_ai_system.feedback_analysis_system import FeedbackAnalysisSystem
                
                system = FeedbackAnalysisSystem()
                system.run(limit=3)
                
            except Exception as e:
                print(f"❌ Error during processing: {e}")
        else:
            print("Skipped processing demo")
        
        input("\nPress Enter to continue...")
    
    def step_5_results_analysis(self):
        """Analyze results"""
        self.print_header("STEP 5: RESULTS ANALYSIS")
        
        try:
            import pandas as pd
            
            # Check if results exist
            if not os.path.exists('generated_tickets.csv'):
                print("⚠️  No results found. Run processing first.")
                return
            
            # Load results
            tickets_df = pd.read_csv('generated_tickets.csv')
            
            self.print_section("Generated Tickets Summary")
            print(f"Total Tickets: {len(tickets_df)}")
            print(f"\nSource Distribution:")
            print(tickets_df['source_type'].value_counts())
            
            self.print_section("Sample Generated Ticket")
            if len(tickets_df) > 0:
                sample = tickets_df.iloc[0]
                print(f"Source ID: {sample['source_id']}")
                print(f"Source Type: {sample['source_type']}")
                print(f"Created At: {sample['created_at']}")
                print(f"\nOriginal Content:")
                print(sample['original_content'])
                print(f"\nProcessing Result (first 500 chars):")
                print(sample['processing_result'][:500] + "...")
            
            # Processing logs
            if os.path.exists('processing_log.csv'):
                self.print_section("Processing Logs")
                logs_df = pd.read_csv('processing_log.csv')
                print(f"Total Log Entries: {len(logs_df)}")
                print(f"\nAction Distribution:")
                print(logs_df['action'].value_counts())
            
            # Metrics
            if os.path.exists('metrics.csv'):
                self.print_section("System Metrics")
                metrics_df = pd.read_csv('metrics.csv')
                latest = metrics_df.iloc[-1]
                print(f"Total Feedback: {latest['total_feedback']}")
                print(f"Tickets Generated: {latest['tickets_generated']}")
                print(f"Success Rate: {latest['success_rate']}")
                print(f"Reviews Processed: {latest['reviews_processed']}")
                print(f"Emails Processed: {latest['emails_processed']}")
            
        except Exception as e:
            print(f"❌ Error analyzing results: {e}")
        
        input("\nPress Enter to continue...")
    
    def step_6_validation(self):
        """Run validation"""
        self.print_header("STEP 6: VALIDATION AGAINST EXPECTED RESULTS")
        
        print("Comparing generated tickets with expected classifications...\n")
        
        response = input("Run validation? (y/n): ").lower().strip()
        
        if response == 'y':
            try:
                from feedback_ai_system.validate_results import SystemValidator
                
                validator = SystemValidator()
                validator.validate()
                
            except Exception as e:
                print(f"❌ Error during validation: {e}")
        else:
            print("Skipped validation")
        
        input("\nPress Enter to continue...")
    
    def step_7_dashboard_tour(self):
        """Dashboard tour instructions"""
        self.print_header("STEP 7: DASHBOARD TOUR")
        
        print("""
🎨 STREAMLIT DASHBOARD FEATURES:

To launch the dashboard:
   streamlit run dashboard.py

Dashboard Tabs:

📊 Dashboard Tab:
   - System overview and metrics
   - Recent reviews and emails
   - Quick statistics

🚀 Process Feedback Tab:
   - Run the multi-agent system
   - Configure processing limits
   - Real-time progress tracking
   - View processing summary

🎫 Generated Tickets Tab:
   - View all generated tickets
   - Filter by source type
   - Download results as CSV
   - Detailed ticket inspection

📈 Analytics Tab:
   - Overall metrics and performance
   - Processing history
   - Success rates
   - Detailed logs with filtering

🔍 Manual Review Tab:
   - Review individual tickets
   - Edit ticket details
   - Approve or reject tickets
   - Manual override capability

Key Features:
✅ Real-time processing updates
✅ Interactive filters and search
✅ CSV download for all data
✅ Configuration without code changes
✅ Responsive design for all screen sizes
        """)
        
        response = input("\nLaunch dashboard now? (y/n): ").lower().strip()
        
        if response == 'y':
            print("\nLaunching dashboard...")
            print("Press Ctrl+C to stop the server\n")
            time.sleep(2)
            os.system("streamlit run dashboard.py")
        else:
            print("\nTo launch later, run: streamlit run dashboard.py")
    
    def run_complete_demo(self):
        """Run complete demonstration"""
        self.print_header("🎓 INTELLIGENT FEEDBACK ANALYSIS SYSTEM - COMPLETE DEMO")
        
        print("""
This demonstration will cover:
1. System Overview
2. Data Inspection
3. Agent Architecture
4. Processing Demo
5. Results Analysis
6. Validation
7. Dashboard Tour

Estimated time: 3-5 minutes
        """)
        
        response = input("Start complete demo? (y/n): ").lower().strip()
        
        if response != 'y':
            print("Demo cancelled")
            return
        
        # Run all steps
        self.step_1_overview()
        self.step_2_data_inspection()
        self.step_3_agent_architecture()
        self.step_4_processing_demo()
        self.step_5_results_analysis()
        self.step_6_validation()
        self.step_7_dashboard_tour()
        
        # Final summary
        self.print_header("🎉 DEMONSTRATION COMPLETE")
        
        print("""
Summary of Achievements:

✅ Created complete multi-agent system
✅ Implemented 6 specialized agents
✅ Built data processing pipeline
✅ Generated structured tickets
✅ Quality assurance automation
✅ Web-based monitoring dashboard
✅ Validation against expected results

Key Deliverables:
- feedback_analysis_system.py (main system)
- dashboard.py (Streamlit UI)
- 3 input CSV files with 7 total feedback items
- Generated tickets with processing logs
- Validation reports
- Comprehensive documentation

Next Steps:
1. Process all 7 feedback items (remove limit in code)
2. Integrate with real data sources (API)
3. Add database storage
4. Deploy to production
5. Monitor and optimize performance

Thank you for watching the demonstration! 🚀
        """)


def main():
    """Main entry point"""
    demo = SystemDemo()
    demo.run_complete_demo()


if __name__ == "__main__":
    main()
