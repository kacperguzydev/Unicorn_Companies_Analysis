# 🦄 Unicorn Companies Analysis Dashboard

Analyze global unicorn companies, explore key metrics, and predict expected valuations using an interactive Streamlit dashboard.


## ✅ Tools Used

- Python 3.11  
- SQLite  
- pandas  
- scikit-learn  
- Streamlit  
- Plotly

## 📦 How to Use

**1️⃣ Clone the repository:**

git clone https://github.com/kacperguzydev/Unicorn_Companies_Analysis.git

**2️⃣ Install required packages:**

pip install -r requirements.txt

**3️⃣ Prepare the data (run these scripts in order):**

- python models/transform.py
- python models/load_to_db.py
- python models/sql_analysis.py
- python models/regression_prediction.py

**4️⃣ Launch the dashboard locally:**

streamlit run dashboard.py


## 🚀 Screenshots
- 🔮 Prediction Tab:
![Prediction Tab](images/1.png)
- 📊 Analysis: Unicorns per Country:
![Unicorns per Country](images/2.png)
- 💰 Analysis: Total Valuation per Country:
![Total Valuation per Country](images/3.png)
- 📉 Analysis: Average Valuation per Country:
![Average Valuation per Country](images/4.png)
- 📈 Analysis: KPIs Overview:
  ![KPIs Overview](images/5.png)
