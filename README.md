# 🌾 MilletMitra – Smart Food Identifier & Translator

MilletMitra is a smart food assistant built with Python and Streamlit to help users **translate local/phonetic food names**, identify their **standard English, Hindi, Telugu** names, and categorize them under Millets, Pulses, Grains, Spices, and Seeds.

It enriches raw CSV data automatically and provides a powerful user interface with search, comparison, and meal suggestions.

---

## 🚀 Features

### 🔍 Search Food Item
Type a local or phonetic name like `Samalu`, `Kabun Shenigalu`, or `Mysore pappu`, and instantly get the:
- Telugu Native Script
- English Name
- Hindi Name
- Food Category (Millet, Pulse, Grain, Spice, Seed)

### ⚖️ Compare Nutrition
Get quick comparisons between food items across their categories. This helps users choose healthy alternatives or diversify their meals.

### 🍽️ Meal Suggestions
Based on selected food categories, the app suggests balanced meals and combinations (coming soon with ML support!).

### 📂 Browse by Category
Users can explore food items based on:
- **Millets**
- **Pulses**
- **Grains**
- **Spices**
- **Seeds**

---

## 🧠 Technologies Used

- **Python** for data processing
- **pandas**, **deep-translator**, **requests**, **BeautifulSoup** for translation and scraping
- **Streamlit** for building an interactive web UI
- **Google Translate API** (via `deep-translator`) for phonetic → native language mapping

---

## 📁 File Structure

```
├── Dataset/               # Contains raw and enriched CSV files
├── app.py                 # Streamlit UI file
├── trans.py               # Translation + enrichment script
├── requirements.txt       # Python dependencies
├── README.md              # Project documentation
└── .env                   # Environment variables (if any)
```

---

## 📦 Dataset

- `list(Sheet1).csv`: The raw CSV input with two columns: `S.No`, `Names`
- `millets_enriched.csv`: Auto-generated file with enriched columns:
  - `Telugu Native`
  - `English Name`
  - `Hindi Name`
  - `Category`

---

## 🛠️ Setup Instructions

### 🔧 Step 1: Install dependencies

```bash
pip install -r requirements.txt
```

### 📂 Step 2: Run the translator script

```bash
python trans.py
```
This reads your raw CSV and outputs an enriched version.

### 💻 Step 3: Launch the Streamlit app

```bash
streamlit run app.py
```

---

## 🌐 Deployment

To deploy the app live:

1. Push your code to GitHub.
2. Sign up at [Streamlit Cloud](https://streamlit.io/cloud) (or use [Render](https://render.com)).
3. Connect your repo and deploy the app – Streamlit will handle the hosting!

---

## 🔒 .gitignore

Make sure not to push unnecessary or sensitive files:

```
.env
venv/
env/
__pycache__/
*.pyc
```

---

## 🙌 Contributions

Pull requests are welcome! If you'd like to contribute translations, food items, or improve UI/UX, feel free to fork the project.

---

## 📢 Acknowledgments

* [MilletAdvisor.com](https://milletadvisor.com/millets-name-in-different-languages/) – for food translation references
* [deep-translator](https://pypi.org/project/deep-translator/) – for multilingual translation
* [Streamlit](https://streamlit.io) – for UI framework

---
