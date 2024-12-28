# My Hero Academia Dashboard

This project is a fan-created dashboard for **My Hero Academia**, showcasing detailed character metadata, high-quality images, and visualizations. It's designed to provide fans with an interactive way to explore the characters of this iconic anime and manga series.

---

## Features

### 1. Character Data
- Metadata about heroes, villains, students, and civilians fetched from the [My Hero Academia API](https://myheroacademia-api.onrender.com/characters).
- Attributes include:
  - **Name**
  - **Japanese Name**
  - **Quirk**
  - **Hero/Villain Affiliation**
  - **Description**

### 2. Character Images
- High-quality character images stored locally in the `images/characters/` directory.
- Images are linked to character data for easy integration into visualizations.

### 3. Python Scripts
- Automated scripts for managing data and images:
  - `fetch_data.py`: Fetches character metadata and saves it to `data/characters.csv`.
  - `download_images.py`: Downloads character images from the web.
  - `verify_images.py`: Verifies that all characters have corresponding images.

### 4. Dashboard Visualization
- The project is designed for integration with visualization tools like Power BI or Tableau, featuring:
  - Character details with images.
  - Filters and search functionality.
  - Interactive visualizations for an engaging experience.

---

## Setup Instructions

### Clone the Repository
```bash
git clone https://github.com/<your-username>/my-hero-academia-dashboard.git
cd my-hero-academia-dashboard
```

### Set Up a Python Environment
1. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```
2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Fetch Character Data
```bash
python scripts/fetch_data.py
```

### Download Character Images
```bash
python scripts/download_images.py
```

### Verify Images
```bash
python scripts/verify_images.py
```

---

## Project Directory Structure

```
My Hero Academia/
├── data/
│   └── characters.csv       # Character data in CSV format
├── images/
│   └── characters/          # Directory for character images
├── scripts/
│   ├── fetch_data.py        # Fetches character metadata
│   ├── download_images.py   # Downloads character images
│   ├── verify_images.py     # Verifies image integrity
├── venv/                    # Python virtual environment
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation
```

---

## Dependencies

Install the following Python libraries:
- `requests`: For API requests.
- `pandas`: For handling and saving data.
- `beautifulsoup4`: For web scraping images.
- `Pillow`: For image verification and manipulation.

To install all dependencies:
```bash
pip install -r requirements.txt
```

---

## Future Enhancements

1. **Interactive Features**
   - Add dynamic filters for quirks, classes, and affiliations.
   - Display additional stats like popularity rankings.
2. **Automated Updates**
   - Implement a cron job or GitHub Actions workflow to fetch and download updated data.
3. **Web Dashboard**
   - Deploy the dashboard online using tools like Streamlit or Tableau Public.

---

## Contributing

Contributions are welcome! Here's how:
1. Fork the repository.
2. Create a new branch:
```bash
git checkout -b feature/your-feature-name
```
3. Commit your changes:
```bash
git commit -m "Add your feature or fix"
```
4. Push to your branch:
```bash
git push origin feature/your-feature-name
```
5. Open a pull request on GitHub.

---

## Acknowledgments

- **API Source:** [My Hero Academia API](https://myheroacademia-api.onrender.com/characters) for character metadata.
- **Libraries Used:** `requests`, `pandas`, `beautifulsoup4`, and `Pillow`.

---

## License

This project is for educational and fan purposes only. All character names, images, and related content are the property of their respective owners.
