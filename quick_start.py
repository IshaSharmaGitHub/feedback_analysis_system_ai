"""
Quick Start Demo Script
Run this to test the system with a small sample
"""

import os
import sys

def check_requirements():
    """Check if all requirements are met"""
    print("🔍 Checking requirements...\n")
    
    # Check Python version
    print(f"✅ Python version: {sys.version.split()[0]}")
    
    # Check for required packages
    required_packages = ['crewai', 'streamlit', 'pandas', 'dotenv']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package} installed")
        except ImportError:
            print(f"❌ {package} not installed")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    # Check for .env file
    if not os.path.exists('.env'):
        print("\n⚠️  .env file not found")
        print("Create a .env file with your OPENAI_API_KEY")
        print("See .env.example for reference")
        return False
    else:
        print("✅ .env file found")
    
    # Check for API key
    from dotenv import load_dotenv
    load_dotenv()
    
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY not set in .env file")
        return False
    else:
        print("✅ OPENAI_API_KEY configured")
    
    # Check for CSV files
    required_files = ['app_store_reviews.csv', 'support_emails.csv']
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file} found")
        else:
            print(f"❌ {file} not found")
            return False
    
    print("\n✅ All requirements met!")
    return True


def run_demo():
    """Run a quick demo with limited feedback"""
    print("\n" + "="*60)
    print("RUNNING QUICK DEMO (3 feedback items)")
    print("="*60 + "\n")
    
    from feedback_ai_system.feedback_analysis_system import FeedbackAnalysisSystem
    
    # Initialize system
    print("🚀 Initializing system...")
    system = FeedbackAnalysisSystem()
    
    # Run with limit
    system.run(limit=3)
    
    print("\n" + "="*60)
    print("DEMO COMPLETE!")
    print("="*60)
    print("\n📋 Next steps:")
    print("1. Check generated_tickets.csv for output")
    print("2. Check processing_log.csv for detailed logs")
    print("3. Check metrics.csv for statistics")
    print("\n🎨 To launch the web dashboard:")
    print("   streamlit run dashboard.py")
    print("\n📚 For full processing, edit feedback_analysis_system.py")
    print("   Change: system.run(limit=3)")
    print("   To:     system.run()")


def main():
    """Main entry point"""
    print("\n" + "="*60)
    print("INTELLIGENT FEEDBACK ANALYSIS SYSTEM - QUICK START")
    print("="*60 + "\n")
    
    # Check requirements
    if not check_requirements():
        print("\n❌ Please fix the issues above before running the demo")
        return
    
    # Ask user if they want to run demo
    print("\n" + "="*60)
    response = input("Run quick demo? (y/n): ").lower().strip()
    
    if response == 'y':
        run_demo()
    else:
        print("\n📖 To run manually:")
        print("   python feedback_analysis_system.py")
        print("\n🎨 To launch dashboard:")
        print("   streamlit run dashboard.py")


if __name__ == "__main__":
    main()
