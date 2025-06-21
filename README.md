# Malicious URL Detection using Machine Learning

This project is a **Phishing URL Detection Web Application** built using **Streamlit**. It uses a trained **Random Forest Classifier** to classify URLs as either `Phishing` or `Legit`. The model is trained on a dataset containing engineered features that represent characteristics of URLs commonly used in phishing attacks.

---

## 🔍 Features Used for Detection

The following 23 features are extracted from the given URL before prediction:

| Feature Name          | Description                                               |
| --------------------- | --------------------------------------------------------- |
| `length_url`          | Total length of the URL                                   |
| `length_hostname`     | Length of the domain/hostname part                        |
| `ip`                  | Whether an IP address is used instead of a domain (1/0)   |
| `nb_dots`             | Number of `.` in the URL                                  |
| `nb_qm`               | Number of `?` characters                                  |
| `nb_eq`               | Number of `=` characters                                  |
| `nb_slash`            | Number of `/` characters                                  |
| `nb_www`              | Number of `www` substrings in the URL                     |
| `ratio_digits_url`    | Ratio of digits in the entire URL                         |
| `ratio_digits_host`   | Ratio of digits in the hostname/domain                    |
| `tld_in_subdomain`    | Whether the TLD appears in subdomain                      |
| `prefix_suffix`       | Presence of hyphen (`-`) in the domain                    |
| `shortest_word_host`  | Length of the shortest subdomain word                     |
| `longest_words_raw`   | Length of longest word in raw URL                         |
| `longest_word_path`   | Longest word in the URL path section                      |
| `phish_hints`         | Whether the word "secure" is missing in the domain        |
| `nb_hyperlinks`       | Number of hyperlinks in the HTML content                  |
| `ratio_intHyperlinks` | Ratio of internal hyperlinks (placeholder for future use) |
| `empty_title`         | Whether the HTML page has an empty `<title>` tag          |
| `domain_in_title`     | If domain name is found in page title (placeholder)       |
| `domain_age`          | Age of domain in days (using WHOIS data)                  |
| `google_index`        | If the site is indexed on Google (default to 1)           |
| `page_rank`           | Page rank score (via Open Page Rank API)                  |

---

## 📈 Model Overview

* **Algorithm Used**: Random Forest Classifier
* **Accuracy**: \~96%
* **Precision**: \~95%
* **Recall**: \~94%
* **F1 Score**: \~94.5%
* **Scaler Used**: StandardScaler

---

## 🎯 Use Cases

1. **Browser Extensions**: Warn users before visiting suspicious URLs.
2. **Email Filters**: Automatically flag emails containing phishing links.
3. **Cybersecurity Dashboards**: Integrate into internal tools for real-time detection.
4. **Educational Tools**: Teach users about malicious URL patterns.

---

## 🚀 How to Run Locally

1. **Install dependencies**:

```bash
pip install -r requirements.txt
```

2. **Run the Streamlit app**:

```bash
streamlit run app.py
```

---

## 📦 Folder Structure

```
Malicious_Link_Analyzer/
├── app.py                   # Streamlit App
├── feature_extractor.py    # Custom feature extraction logic
├── rf_model.pkl            # Trained Random Forest model
├── scaler.pkl              # Trained scaler for preprocessing
├── requirements.txt        # Dependencies
└── README.md               # Project Overview
```

---

## 🔐 API Key and Environment Setup

To use Open Page Rank API securely, store your key in a `.env` file:

```env
OPR_API_KEY=your_api_key_here
```

Then load it using:

```python
from dotenv import load_dotenv
load_dotenv()
```

---

## ⚠️ Limitations & Improvements

* `ratio_intHyperlinks` and `domain_in_title` are currently placeholders.
* Google Index check is static (not dynamic).
* PageRank API has usage limits.

---

## 🙌 Acknowledgements

* [Open Page Rank API](https://www.domcop.com/openpagerank/)
* Python libraries: `sklearn`, `streamlit`, `bs4`, `requests`, `whois`, `tldextract`

---

## 📫 Contact

For any queries, contact [Vidhi Gupta](mailto:vidhigupta@example.com) or raise an issue in the GitHub repository.
