# Data Engineering Intern Project

This project demonstrates a small data engineering workflow using Python and SQLite3.  
It involves collecting data from an API, storing it locally, processing and analyzing it through a Jupyter Notebook, and finalizing it into a reproducible Python script.

---

## 📂 Project Structure

├── raw_data/ # Folder for raw files fetched from the API
├── db/ # SQLite3 database files
├── Working Notebook.ipynb # Jupyter notebook used for exploration and development
├── final_project.py # Finalized, cleaned-up Python script
└── README.md # Project documentation


---

## Technologies Used

- **Python 3**
- **SQLite3** – lightweight local database for storing and querying data
- **Jupyter Notebook** – for iterative coding, analysis, and visualization
- **Pandas / Requests/ Pydantic** – for data manipulation and API integration

---

## Project Description

1. **Data Collection**  
   Data is fetched from an external API and stored as raw files in the `raw_data/` folder.  
   This ensures data persistence and allows reprocessing without repeated API calls.

2. **Database Layer**  
   The collected data is cleaned and stored in a local **SQLite3 database** under the `db/` directory (`stocks.db`).  
   SQLite is used for its simplicity and integration with Python’s standard library.

3. **Development Notebook**  
   The `Working Notebook.ipynb` file contains exploratory work — initial data loading, transformations, visualizations, and logic testing.

4. **Final Code**  
   Once stable, all logic is consolidated into `final_project.py`, a reproducible, self-contained Python script.

---

## 🗃️ Database

- Database Engine: **SQLite3**
- Location: `db/stocks.db`

---

## 🧩 How to Run

```bash
# Clone the repository
git clone https://github.com/datageek06/Data-Engineering-Intern-Project-.git
cd Data-Engineering-Intern-Project-

# Run the final script
python final_project.py
