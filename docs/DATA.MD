# Data Collection & Transformation Process

This document details the lifecycle of the data used to train and evaluate the Clickbait Analyzer model, ensuring transparency and reproducibility as per SPŠE Ječná requirements.

## 1. Data Collection (Scraping)

The training data was collected using a custom-built RSS scraper located in `src/data/scraper.py`. Instead of using pre-processed datasets, the data is fetched directly from real-world news outlets.

### Data Sources
We categorize sources into two groups to create a labeled dataset:

*   **Non-Clickbait (True News):**
    *   **ČT24**: Public service news (RSS: `ct24.ceskatelevize.cz`)
    *   **iROZHLAS**: Investigative and verified news (RSS: `irozhlas.cz`)
    *   **Seznam Zprávy**: General news coverage (RSS: `seznamzpravy.cz`)
    *   **Novinky.cz**: General news (RSS: `novinky.cz`)

*   **Clickbait (Tabloid/Entertainment):**
    *   **Blesk.cz**: Entertainment and celebrity news
    *   **eXtra.cz**: High-intensity tabloid content
    *   **Super.cz**: Celebrity-focused clickbait

### Collection Mechanism
The `scraper.py` script:
1.  Iterates through defined RSS feeds.
2.  Extracts the `title` of each entry.
3.  Assigns a binary label: `0` (News) or `1` (Clickbait).
4.  Appends data to `dataset.csv` while automatically filtering out duplicates based on the headline text.

## 2. Data Transformation (Feature Engineering)

Raw headlines are not directly fed into the Machine Learning model. Instead, they are transformed into numerical features within `src/model/clickbait.py` using the following encapsulation logic:

| Feature | Description | Rationale |
| :--- | :--- | :--- |
| **Word Count** | Total number of words in the headline. | Clickbait often uses shorter or intentionally long "teaser" sentences. |
| **Uppercase Ratio** | Percentage of uppercase characters. | Overuse of CAPS is a common clickbait technique. |
| **Buzzword Count** | Occurrences of words like "šokující", "drama", "odhalena". | Direct indicators of sensationalist content. |
| **Contains Number** | Binary flag (0/1) if the headline has digits. | Listicles ("7 věcí...") are frequently clickbait. |
| **Punctuation** | Count of `,`, `!`, and `?`. | Excessive exclamation or question marks signal emotional manipulation. |

### Preprocessing Pipeline
1.  **Cleaning**: The scraper removes whitespace and discards duplicate headlines.
2.  **Vectorization**: The `Clickbait` class transforms raw text into a data frame of 7 numerical attributes.
3.  **Encapsulation**: All processing logic is hidden within the `Clickbait` model class, providing a clean `analyze_headline(text)` API for the Controller.

---
*Created by Jan Vavroušek as part of the Machine Learning project documentation.*
