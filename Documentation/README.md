# Intelligent User Feedback Analysis and Action System

A multi-agent AI system that automatically processes user feedback from app stores and support emails, classifies them, and generates structured tickets for engineering teams.

## 🎯 Project Overview

This system solves the problem of manual feedback triaging by:
- Automatically reading feedback from CSV files
- Classifying content into categories (Bug/Feature Request/Praise/Complaint/Spam)
- Extracting actionable insights and technical details
- Creating structured tickets with appropriate priority levels
- Ensuring quality through automated review
- Providing a user interface for monitoring and manual overrides

## 🏗️ System Architecture

### Multi-Agent System (6 Agents)

1. **CSV Reader Agent**: Reads and parses feedback data from CSV files
2. **Feedback Classifier Agent**: Categorizes feedback using NLP
3. **Bug Analysis Agent**: Extracts technical details, steps to reproduce, severity (for bugs)
4. **Feature Extractor Agent**: Analyzes feature requests and estimates user impact (for features)
5. **Ticket Creator Agent**: Generates structured tickets with proper formatting
6. **Quality Critic Agent**: Reviews tickets for completeness and accuracy

**Note**: After classification, the system intelligently routes to the appropriate specialist:
- Bugs → Bug Analysis Agent
- Feature Requests → Feature Extractor Agent
- Other types → General analysis

## 📁 Project Structure

```
feedback_ai_system/
├── feedback_analysis_system.py   # Main multi-agent system
├── dashboard.py                   # Streamlit UI dashboard
├── requirements.txt               # Python dependencies
├── .gitignore                     # Git ignore rules
├── setup.bat                      # Windows setup script
│
├── data/                          # Input data directory
│   ├── app_store_reviews.csv     # Mock app store reviews (5 entries)
│   ├── support_emails.csv        # Mock support emails (2 entries)
│   └── expected_classifications.csv  # Expected results for validation
│
├── output/                        # Output directory (created on first run)
│   ├── generated_tickets.csv     # Generated tickets
│   ├── processing_log.csv        # Processing logs
│   └── metrics.csv                # Performance metrics
│
├── agents/                        # Agents directory (optional/future use)
│
├── quick_start.py                 # Quick setup and demo script
├── validate_results.py            # Validation script
├── demo.py                        # Complete demonstration script
│
└── Documentation/
    ├── README.md                  # This file
    ├── ARCHITECTURE.md            # System architecture diagrams
    ├── PROJECT_SUMMARY.md         # Quick reference guide
    └── COMPLETION_CHECKLIST.md    # Project completion checklist
```

## 🚀 Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Key

Create a `.env` file in the project root:

```bash
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL_NAME=gpt-4-turbo-preview
```

### 3. Verify Data Files

Ensure these CSV files exist in the `data/` directory:
- `data/app_store_reviews.csv` (5 sample reviews)
- `data/support_emails.csv` (2 sample emails)
- `data/expected_classifications.csv` (7 expected results)

## 💻 Usage

### Option 1: Run CLI System

Process feedback via command line:

```bash
python feedback_analysis_system.py
```

This will:
1. Load all feedback from CSV files
2. Process each item through the agent pipeline
3. Generate tickets and save to CSV files
4. Display processing summary

**Note**: By default, the system processes 3 items for testing. To process all feedback, edit `feedback_analysis_system.py` line 443:

```python
# Change from:
system.run(limit=3)

# To:
system.run()  # Process all feedback
```

### Option 2: Run Streamlit Dashboard

Launch the interactive web UI:

```bash
streamlit run dashboard.py
```

The dashboard provides:
- 📊 **Dashboard Tab**: Overview of all feedback
- 🚀 **Process Feedback Tab**: Run the multi-agent system
- 🎫 **Generated Tickets Tab**: View and download tickets
- 📈 **Analytics Tab**: Metrics and processing logs
- 🔍 **Manual Review Tab**: Edit and approve tickets

## 📊 Data Files

### Input Files

#### app_store_reviews.csv
Columns: `review_id, platform, rating, review_text, user_name, date, app_version`

Contains:
- 8 Bug reports (crashes, login issues, data loss)
- 6 Feature requests (calendar sync, widgets, voice-to-text)
- 6 Praise reviews
- 3 Complaints
- 2 Spam entries

#### support_emails.csv
Columns: `email_id, subject, body, sender_email, timestamp, priority`

Contains:
- 6 Bug reports with detailed technical information
- 4 Feature requests
- 3 Complaints (pricing, customer service)
- 2 Praise emails

#### expected_classifications.csv
Ground truth for validating system accuracy.

### Output Files

#### generated_tickets.csv
Contains processed tickets with:
- `source_id`: Original feedback ID
- `source_type`: app_review or support_email
- `created_at`: Timestamp
- `original_content`: Original feedback text
- `processing_result`: Agent analysis and ticket details

#### processing_log.csv
Detailed logs of each processing step:
- `timestamp`: When action occurred
- `source_id`: Feedback being processed
- `action`: Type of action
- `status`: Success or failed
- `details/error`: Additional information

#### metrics.csv
Overall system performance:
- `total_feedback`: Total items processed
- `tickets_generated`: Successfully created tickets
- `success_rate`: Percentage of successful processing
- `reviews_processed`: App store reviews count
- `emails_processed`: Support emails count

## 🎯 Key Features

### Automated Classification
- Accurately categorizes feedback into 5 types
- Uses NLP and context analysis
- Confidence scoring for each classification

### Intelligent Priority Assignment
- **Critical**: Data loss, login failures, crashes affecting many users
- **High**: Bugs blocking functionality, file upload issues
- **Medium**: Performance issues, feature requests with high impact
- **Low**: Praise, spam, minor complaints

### Technical Detail Extraction
For bugs:
- Device and OS information
- App version
- Steps to reproduce
- Severity assessment

For features:
- User impact estimation
- Implementation complexity hints
- Priority recommendations

### Quality Assurance
- Automated review of generated tickets
- Completeness checks
- Format validation
- Approval workflow

## 🔧 Configuration

### Processing Settings (in dashboard.py)
- **Max items to process**: Limit for testing (0 = all)
- **Classification confidence threshold**: Minimum confidence score (default: 70)
- **Critical keywords**: Triggers Critical priority
- **High keywords**: Triggers High priority

### Agent Settings (in feedback_analysis_system.py)
- **LLM Model**: GPT-4 Turbo (configurable in .env)
- **Temperature**: 0.3 (lower = more consistent)
- **Agent verbosity**: True (shows detailed processing)

## 📈 Performance Metrics

Expected performance with provided data:
- **Total feedback**: 7 items (5 reviews + 2 emails)
- **Processing time**: ~2-3 minutes per item (with GPT-4)
- **Accuracy**: ~90-95% classification accuracy
- **Success rate**: ~95-100% ticket generation

## 🧪 Testing

### Test with Limited Data
To test quickly, process only a few items:

```python
system.run(limit=3)  # Process first 3 items
```

### Validate Against Expected Results
Compare `generated_tickets.csv` with `expected_classifications.csv`:

1. Check if categories match
2. Verify priority assignments
3. Confirm technical details extracted

### Sample Test Cases

**Critical Bug (R003)**:
- Expected: Bug, Critical priority
- Keywords: "Can't login", "authentication failed"
- Should extract: Device (Pixel 7 Pro), Version (2.9.8)

**Feature Request (R004)**:
- Expected: Feature Request, Medium priority
- Should extract: Calendar integration request
- User impact: High (productivity enhancement)

**Spam (R016)**:
- Expected: Spam, Low priority
- Keywords: "CRYPTO", "GET RICH", suspicious links
- Should flag as non-actionable

## 🐛 Troubleshooting

### API Key Issues
```
Error: OPENAI_API_KEY not found
```
**Solution**: Create `.env` file with your OpenAI API key

### Import Errors
```
ModuleNotFoundError: No module named 'crewai'
```
**Solution**: Run `pip install -r requirements.txt`

### CSV File Not Found
```
FileNotFoundError: app_store_reviews.csv
```
**Solution**: Ensure CSV files are in the same directory as the scripts

### Rate Limiting
```
Error: Rate limit exceeded
```
**Solution**: 
- Add delays between processing
- Use a lower processing limit
- Upgrade OpenAI API tier

## 🎓 Learning Objectives Covered

✅ Multi-agent system design and orchestration  
✅ Agent role definition and specialization  
✅ Task decomposition and workflow  
✅ NLP for classification and extraction  
✅ Data pipeline (input → processing → output)  
✅ Quality assurance automation  
✅ User interface for monitoring  
✅ Error handling and logging  
✅ CSV data processing  
✅ Real-world business problem solving  

## 🚀 Future Enhancements

- [ ] Real-time processing (API integration)
- [ ] Database storage (PostgreSQL/MongoDB)
- [ ] Email notifications for critical issues
- [ ] Advanced analytics and dashboards
- [ ] Multi-language support
- [ ] Sentiment analysis scores
- [ ] Automated ticket routing to teams
- [ ] Integration with Jira/Linear/GitHub Issues
- [ ] ML model for classification (reduce API costs)
- [ ] Duplicate detection

## 📝 License

This is a capstone project for educational purposes.

## 👥 Author

Capstone Project - Agentic AI Certification Training Course

---

**Built with**: Python 🐍 | CrewAI 🤖 | Streamlit 📊 | OpenAI GPT-4 🧠
