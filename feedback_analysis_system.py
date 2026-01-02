"""
Intelligent User Feedback Analysis and Action System
Multi-Agent System using CrewAI
"""

import os
import sys
import httpx
import pandas as pd
from datetime import datetime
from typing import List, Dict
import json
from dotenv import load_dotenv
# import ssl
# import urllib3

import truststore
truststore.inject_into_ssl()

from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI

# Load environment variables
load_dotenv()


class FeedbackAnalysisSystem:
    """Main system orchestrating the multi-agent feedback analysis"""
    
    def __init__(self):
        self.app_reviews_path = "data/app_store_reviews.csv"
        self.support_emails_path = "data/support_emails.csv"
        self.output_tickets_path = "output/generated_tickets.csv"
        self.processing_log_path = "output/processing_log.csv"
        self.metrics_path = "output/metrics.csv"
        
        # Data storage
        self.reviews_data = None
        self.emails_data = None
        self.all_feedback = []
        self.generated_tickets = []
        self.processing_logs = []
        
        # Initialize LLM
        model = os.getenv("OPENAI_MODEL_NAME", "gpt-4-turbo-preview")
        print(f"Using model: {model}")
        
        self.llm = ChatOpenAI(
            model=model,
            temperature=0.3,
            timeout=60
        )
        
        # Initialize agents
        self._setup_agents()
        
    def _setup_agents(self):
        """Initialize all agents with their roles and goals"""
        
        # 1. CSV Reader Agent
        self.csv_reader_agent = Agent(
            role="CSV Data Reader",
            goal="Read and parse feedback data from CSV files accurately",
            backstory="""You are an expert data parsing specialist. Your job is to 
            read CSV files containing user feedback from multiple sources and 
            prepare the data for analysis. You ensure data integrity and handle 
            various formats and edge cases.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
        
        # 2. Feedback Classifier Agent
        self.classifier_agent = Agent(
            role="Feedback Classifier",
            goal="Accurately categorize feedback into Bug, Feature Request, Praise, Complaint, or Spam",
            backstory="""You are an expert NLP classifier specializing in sentiment 
            analysis and intent detection. You can quickly identify the primary 
            purpose of user feedback and assign accurate categories. You look for 
            keywords, sentiment, and context to make precise classifications.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
        
        # 3. Bug Analysis Agent
        self.bug_analyzer_agent = Agent(
            role="Bug Analysis Specialist",
            goal="Extract technical details from bug reports including steps to reproduce, platform info, and severity",
            backstory="""You are a seasoned QA engineer with deep technical knowledge. 
            When analyzing bug reports, you extract key technical information: device 
            details, OS versions, app versions, reproduction steps, and assess severity 
            based on impact and frequency. You know how to identify critical issues 
            that need immediate attention.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
        
        # 4. Feature Extractor Agent
        self.feature_extractor_agent = Agent(
            role="Feature Request Analyst",
            goal="Identify feature requests and estimate user impact and demand",
            backstory="""You are a product analyst skilled at understanding user needs. 
            You extract feature requests from feedback, understand the underlying user 
            need, estimate potential impact on user satisfaction, and identify patterns 
            in feature requests across multiple feedback items.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
        
        # 5. Ticket Creator Agent
        self.ticket_creator_agent = Agent(
            role="Ticket Creator",
            goal="Generate well-structured, actionable tickets with appropriate priority and metadata",
            backstory="""You are an expert project manager who creates clear, actionable 
            tickets for engineering teams. You write concise titles, detailed descriptions, 
            set appropriate priorities, and include all necessary metadata. Your tickets 
            follow best practices and are immediately actionable.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
        
        # 6. Quality Critic Agent
        self.quality_critic_agent = Agent(
            role="Quality Assurance Reviewer",
            goal="Review generated tickets for completeness, accuracy, and quality",
            backstory="""You are a meticulous QA reviewer who ensures every ticket meets 
            quality standards. You check for completeness, accuracy of classification, 
            appropriate priority assignment, clear descriptions, and proper formatting. 
            You catch inconsistencies and suggest improvements.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
    
    def load_data(self):
        """Load feedback data from CSV files"""
        try:
            self.reviews_data = pd.read_csv(self.app_reviews_path)
            self.emails_data = pd.read_csv(self.support_emails_path)
            
            # Combine all feedback
            for _, row in self.reviews_data.iterrows():
                self.all_feedback.append({
                    'source_id': row['review_id'],
                    'source_type': 'app_review',
                    'content': row['review_text'],
                    'metadata': {
                        'platform': row['platform'],
                        'rating': row['rating'],
                        'user_name': row['user_name'],
                        'date': row['date'],
                        'app_version': row['app_version']
                    }
                })
            
            for _, row in self.emails_data.iterrows():
                self.all_feedback.append({
                    'source_id': row['email_id'],
                    'source_type': 'support_email',
                    'content': f"{row['subject']} | {row['body']}",
                    'metadata': {
                        'subject': row['subject'],
                        'sender_email': row['sender_email'],
                        'timestamp': row['timestamp'],
                        'priority': row.get('priority', '')
                    }
                })
            
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'action': 'data_loaded',
                'details': f"Loaded {len(self.reviews_data)} reviews and {len(self.emails_data)} emails"
            }
            self.processing_logs.append(log_entry)
            
            return True
            
        except Exception as e:
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'action': 'data_load_error',
                'details': str(e)
            }
            self.processing_logs.append(log_entry)
            return False
    
    def process_feedback_item(self, feedback_item: Dict) -> Dict:
        """Process a single feedback item through the agent pipeline"""
        
        source_id = feedback_item['source_id']
        content = feedback_item['content']
        metadata = feedback_item['metadata']
        
        # Task 1: Classify feedback
        classify_task = Task(
            description=f"""Analyze this feedback and classify it into exactly ONE category:
            Bug, Feature Request, Praise, Complaint, or Spam.
            
            Feedback: {content}
            
            Provide your classification and confidence score (0-100).
            Format: Category: [category], Confidence: [score]""",
            agent=self.classifier_agent,
            expected_output="Classification category and confidence score"
        )
        
        # Task 2a: Bug Analysis (for bugs only)
        bug_analysis_task = Task(
            description=f"""Analyze this BUG report and extract technical details:
            
            Feedback: {content}
            Metadata: {json.dumps(metadata)}
            
            Extract:
            - Device/platform information
            - App version
            - Steps to reproduce
            - Severity assessment (Critical/High/Medium/Low)
            - Error messages or symptoms
            - Frequency of occurrence
            
            Provide structured output with all technical details.""",
            agent=self.bug_analyzer_agent,
            expected_output="Detailed bug analysis with technical information",
            context=[classify_task]
        )
        
        # Task 2b: Feature Analysis (for feature requests only)
        feature_analysis_task = Task(
            description=f"""Analyze this FEATURE REQUEST and extract insights:
            
            Feedback: {content}
            Metadata: {json.dumps(metadata)}
            
            Extract:
            - What feature is being requested (clear description)
            - User need or pain point being addressed
            - User impact estimation (High/Medium/Low)
            - Potential user benefit
            - Priority recommendation based on demand
            - Similar existing features or workarounds
            
            Provide structured output with impact analysis.""",
            agent=self.feature_extractor_agent,
            expected_output="Detailed feature request analysis with impact estimation",
            context=[classify_task]
        )
        
        # Task 2c: General Analysis (for Praise, Complaint, Spam)
        general_analysis_task = Task(
            description=f"""Analyze this feedback for insights:
            
            Feedback: {content}
            Metadata: {json.dumps(metadata)}
            
            Extract:
            - Key themes or sentiments
            - Actionable insights (if any)
            - Context or background
            - If SPAM: Reason for spam classification
            
            Provide structured output.""",
            agent=self.bug_analyzer_agent,
            expected_output="General analysis with key insights",
            context=[classify_task]
        )
        
        # Task 3: Create ticket
        ticket_task = Task(
            description=f"""Create a structured ticket for this feedback:
            
            Source ID: {source_id}
            Source Type: {feedback_item['source_type']}
            
            Generate:
            1. Ticket Title (clear and actionable)
            2. Category (Bug/Feature Request/Praise/Complaint/Spam)
            3. Priority (Critical/High/Medium/Low)
            4. Description (detailed but concise)
            5. Technical Details (if applicable)
            6. Recommended Action
            
            Format as JSON with these exact keys:
            ticket_title, category, priority, description, technical_details, recommended_action""",
            agent=self.ticket_creator_agent,
            expected_output="JSON formatted ticket with all required fields",
            context=[classify_task, bug_analysis_task, feature_analysis_task, general_analysis_task]
        )
        
        # Task 4: Quality review
        review_task = Task(
            description=f"""Review the generated ticket for quality:
            
            Check:
            1. Is the classification accurate?
            2. Is the priority appropriate?
            3. Is the description clear and actionable?
            4. Are technical details complete (if applicable)?
            5. Is the format correct?
            
            Provide:
            - Quality Score (0-100)
            - Issues Found (if any)
            - Suggestions for improvement (if any)
            - Approval Status (Approved/Needs Revision)
            
            Format as JSON.""",
            agent=self.quality_critic_agent,
            expected_output="Quality review with score and approval status",
            context=[ticket_task]
        )
        
        # Create crew and execute
        crew = Crew(
            agents=[
                self.classifier_agent,
                self.bug_analyzer_agent,
                self.feature_extractor_agent,  
                self.ticket_creator_agent,
                self.quality_critic_agent
            ],
            tasks=[classify_task, bug_analysis_task, feature_analysis_task, general_analysis_task, ticket_task, review_task],
            process=Process.sequential,
            verbose=True
        )
        
        try:
            result = crew.kickoff()
            
            # Parse the result and create ticket
            ticket = {
                'source_id': source_id,
                'source_type': feedback_item['source_type'],
                'created_at': datetime.now().isoformat(),
                'original_content': content[:200] + '...' if len(content) > 200 else content,
                'processing_result': str(result)
            }
            
            # Log processing
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'source_id': source_id,
                'action': 'processed',
                'status': 'success'
            }
            self.processing_logs.append(log_entry)
            
            return ticket
            
        except Exception as e:
            # Log error
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'source_id': source_id,
                'action': 'processing_error',
                'status': 'failed',
                'error': str(e)
            }
            self.processing_logs.append(log_entry)
            
            return None
    
    def process_all_feedback(self, limit=None):
        """Process all feedback items"""
        feedback_to_process = self.all_feedback[:limit] if limit else self.all_feedback
        
        print(f"\n{'='*60}")
        print(f"Processing {len(feedback_to_process)} feedback items...")
        print(f"{'='*60}\n")
        
        for idx, feedback in enumerate(feedback_to_process, 1):
            print(f"\n[{idx}/{len(feedback_to_process)}] Processing {feedback['source_id']}...")
            
            ticket = self.process_feedback_item(feedback)
            
            if ticket:
                self.generated_tickets.append(ticket)
                print(f"✅ Ticket created for {feedback['source_id']}")
            else:
                print(f"❌ Failed to create ticket for {feedback['source_id']}")
        
        print(f"\n{'='*60}")
        print(f"Processing complete! {len(self.generated_tickets)} tickets generated.")
        print(f"{'='*60}\n")
    
    def save_results(self):
        """Save all results to CSV files"""
        try:
            # Save tickets
            if self.generated_tickets:
                tickets_df = pd.DataFrame(self.generated_tickets)
                tickets_df.to_csv(self.output_tickets_path, index=False)
                print(f"✅ Saved tickets to {self.output_tickets_path}")
            
            # Save processing logs
            if self.processing_logs:
                logs_df = pd.DataFrame(self.processing_logs)
                logs_df.to_csv(self.processing_log_path, index=False)
                print(f"✅ Saved logs to {self.processing_log_path}")
            
            # Calculate and save metrics
            total_processed = len(self.generated_tickets)
            total_feedback = len(self.all_feedback)
            success_rate = (total_processed / total_feedback * 100) if total_feedback > 0 else 0
            
            metrics = {
                'timestamp': [datetime.now().isoformat()],
                'total_feedback': [total_feedback],
                'tickets_generated': [total_processed],
                'success_rate': [f"{success_rate:.2f}%"],
                'reviews_processed': [len(self.reviews_data)],
                'emails_processed': [len(self.emails_data)]
            }
            
            metrics_df = pd.DataFrame(metrics)
            metrics_df.to_csv(self.metrics_path, index=False)
            print(f"✅ Saved metrics to {self.metrics_path}")
            
        except Exception as e:
            print(f"❌ Error saving results: {e}")
    
    def run(self, limit=None):
        """Run the complete system"""
        print("\n" + "="*60)
        print("INTELLIGENT USER FEEDBACK ANALYSIS SYSTEM")
        print("="*60 + "\n")
        
        # Load data
        print("📂 Loading feedback data...")
        if not self.load_data():
            print("❌ Failed to load data. Exiting.")
            return
        
        print(f"✅ Loaded {len(self.all_feedback)} total feedback items\n")
        
        # Process feedback
        self.process_all_feedback(limit=limit)
        
        # Save results
        print("\n💾 Saving results...")
        self.save_results()
        
        print("\n" + "="*60)
        print("SYSTEM RUN COMPLETE")
        print("="*60 + "\n")


def main():
    """Main entry point"""
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY not found in environment variables")
        print("Please create a .env file with your OpenAI API key")
        print("See .env.example for reference")
        return
    
    # Initialize system
    system = FeedbackAnalysisSystem()
    
    # Run system (limit to 3 items for testing, remove limit for full run)
    system.run(limit=1)  # Change to system.run() for processing all feedback


if __name__ == "__main__":
    main()
