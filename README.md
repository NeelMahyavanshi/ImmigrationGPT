# ImmigrationGPT 🇨🇦

An AI-powered Canadian immigration assistant that provides comprehensive guidance on eligibility, document checklists, and professional document drafting. Built with Streamlit, powered by advanced AI agents, and featuring a robust RAG system for accurate, up-to-date information.

## 🌟 Live Demo

Experience ImmigrationGPT in action: **[https://immigrationgpt.streamlit.app/](https://immigrationgpt.streamlit.app/)**

## ✨ Key Features

### 🤖 Multi-Agent Architecture
- **Chitchat Agent**: Intelligent routing and general immigration queries with live web research
- **Eligibility Agent**: Comprehensive CRS scoring and program eligibility assessment
- **Document Agent**: Exhaustive document checklists with official IRCC forms and practical tips
- **SOP Agent**: Professional document drafting (SOPs, PR Letters, EOI, LORs) with PDF generation

### 📊 Eligibility Assessment
- **CRS Score Calculation**: Accurate Comprehensive Ranking System scoring
- **Program Matching**: Evaluates eligibility across 20+ Canadian immigration programs
- **IELTS to CLB Conversion**: Automatic language score conversion
- **Improvement Suggestions**: Actionable steps to boost eligibility
- **Memory-Aware**: Remembers user profiles across sessions

### 📄 Document Management
- **Interactive Checklists**: Tabbed interface for required, conditional, and recommended documents
- **Official Forms**: Direct links to IRCC forms with PDF downloads
- **Country-Specific Guidance**: Biometrics, PCC routing, and regional quirks
- **Practical Tips**: Common mistakes, validity periods, and processing advice
- **Session Persistence**: Document checklists saved across conversations

### ✍️ Professional Document Generation
- **PDF Generation**: Professional documents with proper formatting and typography
- **Multiple Document Types**: SOPs, PR Letters, EOIs, LORs
- **Cloud Storage**: Secure document storage and sharing via Supabase
- **Unicode Support**: Proper handling of international characters and symbols

### 🔍 Research & Knowledge Base
- **RAG System**: Vector database with 1000+ processed immigration documents
- **Live Web Research**: Google Search integration for current information
- **Multi-Source Data**: IRCC, Canadavisa, and provincial government sources
- **Automated Scraping**: Continuous data collection and processing pipeline

## 🏗️ Architecture

### Core Components
```
ImmigrationGPT/
├── app/                          # Main application
│   ├── agents/                   # AI agent implementations
│   │   ├── chitchat_agent.py     # General queries & routing
│   │   ├── eligibility_agent.py  # CRS & eligibility assessment
│   │   ├── document_agent.py     # Document checklists
│   │   └── sop_agent.py         # Document drafting
│   └── bridge/router_bridge.py  # Agent orchestration
├── scrapers/                     # Data collection pipeline
│   ├── content_scraper_ircc.py   # IRCC website scraping
│   ├── embedding_helper.py       # Vector database creation
│   └── forms_scraper.py          # IRCC forms collection
├── data/                         # Knowledge base
│   ├── embeddings/               # ChromaDB vector store
│   ├── chunks/                   # Processed text chunks
│   └── forms/                    # IRCC forms database
└── generated_files/              # User document storage
```

### Technology Stack
- **Frontend**: Streamlit with custom CSS styling
- **AI Framework**: Agno agents with Groq/Gemini models
- **Database**: PostgreSQL with memory persistence
- **Vector Store**: ChromaDB for RAG
- **Storage**: Supabase for document hosting
- **Scraping**: Crawl4AI for web content extraction
- **Embeddings**: HuggingFace transformers

## 🚀 Achievements

### 📈 Performance Metrics
- **20+ Immigration Programs**: Comprehensive coverage of federal, provincial, and territorial programs
- **1000+ Documents**: Processed and indexed immigration content
- **Real-time Updates**: Live web research for current processing times and fees
- **Multi-language Support**: English and French content processing

### 🎯 User Experience
- **Interactive UI**: Rich document checklists with expandable details
- **Session Management**: Persistent conversations with document library
- **Professional Output**: Publication-ready PDF documents
- **Error Handling**: Robust error recovery and user feedback

### 🔧 Technical Achievements
- **Automated Data Pipeline**: End-to-end scraping, processing, and embedding
- **Memory-Augmented Agents**: Context-aware conversations with user history
- **Scalable Architecture**: Modular agent design for easy expansion
- **Production-Ready**: Deployed on Streamlit Cloud with proper error handling

### 📋 Sample Generated Documents
- **SOP_Ananya_Singh_UofT_MSc_Computer_Science.pdf**: University admission SOP
- **PR_Letter_Request.pdf**: Permanent residency application letter
- **PR_Letter_Valued_Applicant.pdf**: Enhanced PR letter with detailed qualifications
- **StudyPermit_PR_Letter.pdf**: Combined study permit and PR documentation

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- PostgreSQL database
- Supabase account (for document storage)

### Local Development
```bash
# Clone the repository
git clone https://github.com/yourusername/ImmigrationGPT.git
cd ImmigrationGPT

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys and database credentials

# Run data ingestion (optional - for local RAG)
python scrapers/embedding_helper.py

# Start the application
streamlit run app_streamlit.py
```

### Environment Variables
```env
# AI Models
GROQ_API_KEY=your_groq_key
GOOGLE_API_KEY=your_google_key

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/immigration_db

# Storage
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key

# Optional
SAVE_LOCAL_PDF=true
```

## 📊 Data Sources

### Primary Sources
- **Immigration, Refugees and Citizenship Canada (IRCC)**: Official government website
- **Canadavisa**: Immigration news and updates
- **Provincial Immigration Websites**: Program-specific requirements

### Data Processing
- **Web Scraping**: Automated content extraction with Crawl4AI
- **Text Chunking**: Intelligent document splitting for optimal retrieval
- **Embedding Generation**: HuggingFace models for semantic search
- **Vector Storage**: ChromaDB for efficient similarity search

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines for details on:
- Adding new immigration programs
- Improving agent responses
- Enhancing the data pipeline
- UI/UX improvements

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Agno Framework**: For the powerful agent architecture
- **Streamlit**: For the intuitive web interface
- **IRCC**: For providing comprehensive immigration information
- **Open Source Community**: For the amazing tools and libraries

---

**Built with ❤️ for the Canadian immigration community**
