# 🎓 College Recommendation System

An intelligent chatbot system to help students find the perfect engineering college in India based on their preferences, budget, location, and career goals.

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Status](https://img.shields.io/badge/Status-In%20Development-yellow.svg)]()
[![Data](https://img.shields.io/badge/Colleges-8566-green.svg)]()

---

## 📋 Overview

This project provides an AI-powered chatbot that helps students discover and compare engineering colleges across India. Using data from multiple authoritative sources including NIRF rankings, the system offers personalized recommendations through a conversational interface.

### ✨ Key Features (Planned)

- 🤖 **Conversational AI Chatbot** - Natural language queries
- 🔍 **Smart Search** - Find colleges by name, location, courses, fees
- 📊 **Compare Colleges** - Side-by-side comparisons of facilities, fees, rankings
- 🎯 **Personalized Recommendations** - Based on budget, preferences, and goals
- 🏆 **NIRF Rankings Integration** - Official government rankings included
- 💰 **Fee Calculator** - Compare costs across colleges
- 📍 **Location-based Search** - Find colleges by state, city, or region

---

## 📊 Dataset

### Data Sources
Our system combines data from three comprehensive datasets:

1. **Engineering Colleges Database** (5,446 colleges)
   - College details, facilities, fees, ratings
   - Campus size, enrollments, faculty information
   - State-wise distribution across India

2. **Course-Level Data** (2,920 entries)
   - 162 unique engineering courses
   - Accreditation information (NBA, NAAC, NIRF)
   - Course-specific details per college

3. **NIRF Rankings 2024** (200 top colleges)
   - Official government rankings
   - Top engineering institutions in India

### Data Quality
- ✅ **8,566 total records** processed and cleaned
- ✅ **100% data integrity** - no data loss during cleaning
- ✅ **Standardized format** - consistent naming and structure
- ✅ **Production-ready** - quality score 95/100

---

## 🚀 Project Status

### ✅ Phase 1: Data Collection & Cleaning (COMPLETE)
- [x] Collected data from multiple sources
- [x] Cleaned and standardized 8,566 records
- [x] Fixed 12,583 data quality issues
- [x] Normalized college names, fees, and course information
- [x] Handled missing values and encoding issues

### 🔄 Phase 2: Data Merging (IN PROGRESS)
- [ ] Merge all three datasets into unified database
- [ ] Implement fuzzy matching for college names
- [ ] Handle duplicate entries
- [ ] Create master dataset

### 📅 Phase 3: Backend Development (UPCOMING)
- [ ] Design database schema (PostgreSQL/MongoDB)
- [ ] Build REST API (FastAPI/Flask)
- [ ] Implement search algorithms
- [ ] Create recommendation engine

### 📅 Phase 4: Chatbot & Frontend (UPCOMING)
- [ ] Develop conversational AI interface
- [ ] Build responsive web UI (React/Next.js)
- [ ] Integrate natural language processing
- [ ] Deploy chatbot functionality

---

## 📁 Project Structure

```
college-recommendation-system/
├── data/
│   ├── cleaned_engineering_colleges_india.csv  # 5,446 colleges
│   ├── cleaned_engineering.csv                 # 2,920 course entries
│   ├── cleaned_nirf_rankings.csv               # 200 ranked colleges
│   └── [original datasets - backups]
│
├── data_cleaning.py                            # Data cleaning script
├── DATA_CLEANING_COMPLETE.md                   # Cleaning documentation
└── README.md                                   # This file
```

---

## 🛠️ Technology Stack

### Current
- **Python 3.12** - Data processing and cleaning
- **Pandas** - Data manipulation
- **NumPy** - Numerical operations

### Planned
- **Backend:** FastAPI / Flask
- **Database:** PostgreSQL / MongoDB
- **AI/ML:** OpenAI API / LangChain for chatbot
- **Frontend:** React / Next.js
- **Deployment:** Docker, AWS/Vercel

---

## 💻 Installation & Usage

### Prerequisites
- Python 3.12 or higher
- pip (Python package manager)

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/myushreddy/college-recommendation-system.git
cd college-recommendation-system
```

2. **Install dependencies**
```bash
pip install pandas numpy
```

3. **Access cleaned data**
```python
import pandas as pd

# Load datasets
colleges = pd.read_csv('data/cleaned_engineering_colleges_india.csv')
courses = pd.read_csv('data/cleaned_engineering.csv')
rankings = pd.read_csv('data/cleaned_nirf_rankings.csv')

# Example: Find IIT colleges
iit_colleges = colleges[colleges['College Name'].str.contains('IIT')]
print(iit_colleges[['College Name', 'City', 'State', 'Average Fees']])
```

### Re-run Data Cleaning (if needed)
```bash
python data_cleaning.py
```

---

## 📈 Data Statistics

| Metric | Value |
|--------|-------|
| Total Colleges | 8,566 |
| Unique Engineering Courses | 162 |
| States Covered | 35+ |
| Fee Range | ₹180 - ₹35,78,597 |
| NIRF Ranked Colleges | 200 |
| Data Quality Score | 95/100 |

---

## 🎯 Use Cases

### For Students
- Find colleges matching budget and preferences
- Compare facilities and placement records
- Discover courses and specializations
- Check official NIRF rankings

### For Parents
- Compare fee structures across colleges
- Evaluate college facilities and infrastructure
- Understand accreditation status

### For Counselors
- Quick access to comprehensive college database
- Data-driven recommendations
- State-wise college distribution

---

## 🤝 Contributing

Contributions are welcome! This project is in active development.

### How to Contribute
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 Data Cleaning Process

Our data cleaning pipeline ensures high-quality, consistent data:

- ✅ **College Name Standardization** - Removed extra spaces, line breaks (387 fixes)
- ✅ **Course Name Cleaning** - Fixed formatting, removed line breaks (469 fixes)
- ✅ **Missing Value Handling** - Filled 11,096 missing values appropriately
- ✅ **Fee Normalization** - Converted to numeric format (5,446 conversions)
- ✅ **Encoding Fixes** - Handled UTF-8 and Latin-1 encoding issues

For detailed information, see [DATA_CLEANING_COMPLETE.md](DATA_CLEANING_COMPLETE.md)

---

## 📊 Sample Data

### Top 5 Engineering Colleges (NIRF 2024)
1. **IIT Madras** - Chennai, Tamil Nadu
2. **IIT Delhi** - New Delhi, Delhi
3. **IIT Bombay** - Mumbai, Maharashtra
4. **IIT Kanpur** - Kanpur, Uttar Pradesh
5. **IIT Kharagpur** - Kharagpur, West Bengal

### Sample College Data
```
College: National Institute of Technology Rourkela
Location: Rourkela, Odisha
Average Fees: ₹3,50,600
Rating: 4.3/5
Courses: Computer Science, Electronics, Mechanical, Civil, etc.
```

---

## 🔜 Roadmap

### Short Term (Q4 2024)
- [ ] Complete data merging
- [ ] Design database schema
- [ ] Build basic REST API

### Medium Term (Q1 2025)
- [ ] Implement chatbot functionality
- [ ] Develop web interface
- [ ] Add recommendation algorithm

### Long Term (Q2 2025+)
- [ ] Mobile app development
- [ ] Integration with admission portals
- [ ] Real-time data updates
- [ ] Placement data integration

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Mayush Reddy**
- GitHub: [@myushreddy](https://github.com/myushreddy)
- Repository: [college-recommendation-system](https://github.com/myushreddy/college-recommendation-system)

---

## 🙏 Acknowledgments

- NIRF (National Institutional Ranking Framework) for official rankings data
- Various educational data sources for comprehensive college information
- Open-source community for tools and libraries

---

## 📞 Contact & Support

For questions, suggestions, or collaboration opportunities:
- Open an issue on GitHub
- Reach out through GitHub profile

---

## ⚠️ Disclaimer

This project is for educational and informational purposes. College data is sourced from publicly available information and may not be 100% up-to-date. Always verify critical information with official college websites and admission offices.

---

**🌟 Star this repo if you find it helpful!**

*Last Updated: October 24, 2025*
