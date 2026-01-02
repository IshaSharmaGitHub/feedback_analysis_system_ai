# System Architecture Diagram

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    USER INTERFACE LAYER                          │
│                                                                   │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │          Streamlit Dashboard (dashboard.py)                │  │
│  │  • Configuration Panel  • Real-time Monitoring             │  │
│  │  • Manual Review        • Analytics & Reports              │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────────┐
│              CORE PROCESSING LAYER (CrewAI)                      │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │   FeedbackAnalysisSystem (feedback_analysis_system.py)   │   │
│  │                                                            │   │
│  │   ┌──────────────────────────────────────────────────┐   │   │
│  │   │         MULTI-AGENT PIPELINE                     │   │   │
│  │   │                                                  │   │   │
│  │   │  1. CSV Reader Agent                            │   │   │
│  │   │     ↓                                            │   │   │
│  │   │  2. Feedback Classifier Agent                   │   │   │
│  │   │     ↓                                            │   │   │
│  │   │  3a. Bug Analyzer (bugs)                        │   │   │
│  │   │  3b. Feature Extractor (features)               │   │   │
│  │   │  3c. General Analysis (other)                   │   │   │
│  │   │     ↓                                            │   │   │
│  │   │  4. Ticket Creator Agent                        │   │   │
│  │   │     ↓                                            │   │   │
│  │   │  5. Quality Critic Agent                        │   │   │
│  │   └──────────────────────────────────────────────────┘   │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────────┐
│                      DATA LAYER                                  │
│                                                                   │
│  INPUT FILES:                      OUTPUT FILES:                 │
│  ┌──────────────────────┐         ┌──────────────────────┐      │
│  │ app_store_reviews    │         │ generated_tickets    │      │
│  │ (5 reviews)          │         │                      │      │
│  └──────────────────────┘         └──────────────────────┘      │
│                                                                   │
│  ┌──────────────────────┐         ┌──────────────────────┐      │
│  │ support_emails       │         │ processing_log       │      │
│  │ (2 emails)           │         │                      │      │
│  └──────────────────────┘         └──────────────────────┘      │
│                                                                   │
│  ┌──────────────────────┐         ┌──────────────────────┐      │
│  │ expected_            │         │ metrics              │      │
│  │ classifications      │         │                      │      │
│  └──────────────────────┘         └──────────────────────┘      │
└─────────────────────────────────────────────────────────────────┘
```

## Agent Interaction Flow

```
                        ┌─────────────────┐
                        │  Feedback Item  │
                        └────────┬────────┘
                                 │
                                 ↓
                   ┌─────────────────────────┐
                   │  1. CSV Reader Agent    │
                   │  • Parse data           │
                   │  • Validate format      │
                   └───────────┬─────────────┘
                               │
                               ↓
                   ┌─────────────────────────┐
                   │  2. Classifier Agent    │
                   │  • Analyze sentiment    │
                   │  • Detect intent        │
                   │  • Assign category      │
                   └───────────┬─────────────┘
                               │
                ┌──────────────┴──────────────┐
                │                             │
                ↓                             ↓
    ┌───────────────────────┐   ┌───────────────────────┐
    │ 3a. Bug Analyzer      │   │ 3b. Feature Extractor │
    │ • Extract tech details│   │ • Identify feature    │
    │ • Assess severity     │   │ • Estimate impact     │
    │ • Reproduction steps  │   │ • Priority suggestion │
    └───────────┬───────────┘   └───────────┬───────────┘
                │                           │
                └──────────────┬────────────┘
                               │
                               ↓
                   ┌─────────────────────────┐
                   │  4. Ticket Creator      │
                   │  • Generate ticket      │
                   │  • Format properly      │
                   │  • Add metadata         │
                   └───────────┬─────────────┘
                               │
                               ↓
                   ┌─────────────────────────┐
                   │  5. Quality Critic      │
                   │  • Review completeness  │
                   │  • Validate accuracy    │
                   │  • Approve/suggest fix  │
                   └───────────┬─────────────┘
                               │
                               ↓
                        ┌──────────────┐
                        │ Final Ticket │
                        └──────────────┘
```

## Data Flow Diagram

```
┌────────────────────────────────────────────────────────────────┐
│                       DATA FLOW                                 │
└────────────────────────────────────────────────────────────────┘

INPUT SOURCES
    │
    ├─→ App Store Reviews (CSV)
    │   • review_id
    │   • platform (Google Play/App Store)
    │   • rating (1-5)
    │   • review_text
    │   • user_name
    │   • date
    │   • app_version
    │
    └─→ Support Emails (CSV)
        • email_id
        • subject
        • body
        • sender_email
        • timestamp
        • priority
                ↓
        ┌──────────────┐
        │   COMBINE    │
        │   7 items    │
        └──────┬───────┘
               ↓
    ┌─────────────────────┐
    │  AGENT PROCESSING   │
    │  • Classification   │
    │  • Analysis         │
    │  • Ticket Creation  │
    │  • Quality Review   │
    └─────────┬───────────┘
              ↓
OUTPUT FILES
    │
    ├─→ generated_tickets.csv
    │   • source_id
    │   • source_type
    │   • created_at
    │   • original_content
    │   • processing_result
    │
    ├─→ processing_log.csv
    │   • timestamp
    │   • source_id
    │   • action
    │   • status
    │   • details/error
    │
    └─→ metrics.csv
        • timestamp
        • total_feedback
        • tickets_generated
        • success_rate
        • reviews_processed
        • emails_processed
```

## Classification Decision Tree

```
                        Feedback Text
                             │
                             ↓
                    ┌────────────────┐
                    │   Keywords?    │
                    └────────┬───────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ↓                    ↓                    ↓
   ┌─────────┐         ┌─────────┐         ┌─────────┐
   │  Spam   │         │Technical│         │Positive │
   │Keywords?│         │Keywords?│         │Emotion? │
   └────┬────┘         └────┬────┘         └────┬────┘
        │                   │                    │
        ↓                   ↓                    ↓
    [SPAM]              ┌───────┐           [PRAISE]
                        │       │
                    ┌───┴──┐ ┌──┴───┐
                    │      │ │      │
                    ↓      ↓ ↓      ↓
              [BUG]  [FEATURE] [COMPLAINT]
                        REQUEST

Priority Assignment:
    │
    ├─→ Critical: "crash", "data loss", "can't login"
    ├─→ High: "bug", "broken", "not working"
    ├─→ Medium: "slow", "suggestion", "would like"
    └─→ Low: "praise", "spam", "minor complaint"
```

## Technology Stack

```
┌─────────────────────────────────────────────────────────┐
│                    TECHNOLOGY STACK                      │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  FRAMEWORK LAYER                                         │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐        │
│  │  CrewAI    │  │ Streamlit  │  │   Pandas   │        │
│  │  v0.28.8   │  │  v1.31.0   │  │   v2.2.0   │        │
│  └────────────┘  └────────────┘  └────────────┘        │
│                                                          │
│  AI/ML LAYER                                             │
│  ┌────────────┐  ┌────────────┐                         │
│  │ LangChain  │  │  OpenAI    │                         │
│  │  v0.1.9    │  │ GPT-4-turbo│                         │
│  └────────────┘  └────────────┘                         │
│                                                          │
│  DATA LAYER                                              │
│  ┌────────────┐  ┌────────────┐                         │
│  │    CSV     │  │   Python   │                         │
│  │   Files    │  │  Dicts     │                         │
│  └────────────┘  └────────────┘                         │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

## Dashboard Architecture

```
┌──────────────────────────────────────────────────────────────┐
│              STREAMLIT DASHBOARD LAYOUT                       │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  SIDEBAR                      MAIN CONTENT AREA              │
│  ┌─────────────────┐         ┌───────────────────────────┐  │
│  │ Configuration   │         │                           │  │
│  │ • API Key Check │         │  TAB 1: Dashboard         │  │
│  │ • Settings      │         │  • Metrics cards          │  │
│  │ • Thresholds    │         │  • Data preview           │  │
│  │ • Keywords      │         │                           │  │
│  └─────────────────┘         └───────────────────────────┘  │
│                               ┌───────────────────────────┐  │
│                               │  TAB 2: Process Feedback  │  │
│                               │  • Start button           │  │
│                               │  • Progress bar           │  │
│                               │  • Status updates         │  │
│                               └───────────────────────────┘  │
│                               ┌───────────────────────────┐  │
│                               │  TAB 3: Generated Tickets │  │
│                               │  • Table view             │  │
│                               │  • Filters                │  │
│                               │  • Download button        │  │
│                               └───────────────────────────┘  │
│                               ┌───────────────────────────┐  │
│                               │  TAB 4: Analytics         │  │
│                               │  • Charts                 │  │
│                               │  • Logs                   │  │
│                               └───────────────────────────┘  │
│                               ┌───────────────────────────┐  │
│                               │  TAB 5: Manual Review     │  │
│                               │  • Edit tickets           │  │
│                               │  • Approve/reject         │  │
│                               └───────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

## Deployment Architecture (Future)

```
┌──────────────────────────────────────────────────────────────┐
│                  PRODUCTION DEPLOYMENT                        │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌────────────┐         ┌────────────┐      ┌────────────┐  │
│  │   Users    │────────▶│  Streamlit │─────▶│ CrewAI     │  │
│  │  Browser   │         │   Cloud    │      │ Backend    │  │
│  └────────────┘         └────────────┘      └──────┬─────┘  │
│                                                     │         │
│                                              ┌──────▼─────┐  │
│                                              │  OpenAI    │  │
│                                              │    API     │  │
│                                              └──────┬─────┘  │
│                                                     │         │
│  ┌────────────┐         ┌────────────┐      ┌─────▼──────┐  │
│  │  App Store │────────▶│  API       │─────▶│ PostgreSQL │  │
│  │  Reviews   │         │ Gateway    │      │  Database  │  │
│  └────────────┘         └────────────┘      └────────────┘  │
│                                                               │
│  ┌────────────┐                              ┌────────────┐  │
│  │  Support   │─────────────────────────────▶│   Jira     │  │
│  │  Emails    │                              │ Integration│  │
│  └────────────┘                              └────────────┘  │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```
