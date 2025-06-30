🦄 Unicorn Companies Dashboard
Analyze global unicorn companies and predict expected valuations based on country and region. Includes an interactive Streamlit dashboard with separate tabs for predictions and data exploration.

✅ Tools Used
Python 3.11

SQLite

pandas

scikit-learn

Streamlit

Plotly

📦 How to Use
1️⃣ Clone the repository:

bash
Copy
Edit
git clone https://github.com/yourusername/unicorn-companies-dashboard.git
cd unicorn-companies-dashboard
2️⃣ (Optional) Create a virtual environment:

bash
Copy
Edit
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
3️⃣ Install required packages:

bash
Copy
Edit
pip install -r requirements.txt
4️⃣ Prepare the data (run these scripts in order):

bash
Copy
Edit
python models/transform.py
python models/load_to_db.py
python models/sql_analysis.py
python models/regression_prediction.py
5️⃣ Launch the dashboard locally:

bash
Copy
Edit
streamlit run dashboard.py
🚀 Screenshots
🔮 Prediction Tab:

📊 Analysis: Unicorns per Country

💰 Analysis: Total Valuation per Country

📉 Analysis: Average Valuation per Country

📈 Analysis: KPIs Overview
