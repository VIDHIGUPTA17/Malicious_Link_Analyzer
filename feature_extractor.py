from urllib.parse import urlparse
import tldextract
import re
import requests
import whois
from datetime import datetime
from bs4 import BeautifulSoup
import requests


# numerical_df = df1.select_dtypes(include=['float64', 'int64'])

# # Compute the correlation matrix on the numerical columns
# corr_matrix = numerical_df.corr()
# status_corr = corr_matrix['status']
# status_corr.shape

# def feature_selector_correlation(cmatrix, threshold):

#     selected_features = []
#     feature_score = []
#     i=0
#     for score in cmatrix:
#         if abs(score)>threshold:
#             selected_features.append(cmatrix.index[i])
#             feature_score.append( ['{:3f}'.format(score)])
#         i+=1
#     result = list(zip(selected_features,feature_score))
#     return result


# features_selected = feature_selector_correlation(status_corr, 0.2)
# features_selected
# selected_features = []
# for feature, score in features_selected:
#     if feature != 'status':
#         selected_features.append(feature)
selected_features=['length_url',
 'length_hostname',
 'ip',
 'nb_dots',
 'nb_qm',
 'nb_eq',
 'nb_slash',
 'nb_www',
 'ratio_digits_url',
 'ratio_digits_host',
 'tld_in_subdomain',
 'prefix_suffix',
 'shortest_word_host',
 'longest_words_raw',
 'longest_word_path',
 'phish_hints',
 'nb_hyperlinks',
 'ratio_intHyperlinks',
 'empty_title',
 'domain_in_title',
 'domain_age',
 'google_index',
 'page_rank']

from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("OPR_API_KEY")


def get_empty_title(url):
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string if soup.title else ""
        return int(title.strip() == "")
    except:
        return 1  # assume bad if error

def get_nb_hyperlinks(url):
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        return len(soup.find_all('a'))
    except:
        return 0
def get_domain_age(url):
    try:
        domain = tldextract.extract(url).top_domain_under_public_suffix
        w = whois.whois(domain)
        creation = w.creation_date
        if isinstance(creation, list):
            creation = creation[0]
        age_days = (datetime.now() - creation).days
        return age_days
    except:
        return 0

def get_page_rank(domain: str, api_key: str) -> int:
    url = "https://openpagerank.com/api/v1.0/getPageRank"
    headers = {
        "API-OPR": api_key
    }
    params = {
        "domains[]": domain
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=5)
        response.raise_for_status()
        result = response.json()
        rank = result['response'][0].get('page_rank_integer', 0)
        return int(rank)
    except Exception as e:
        print("Error getting PageRank:", e)
        return 0  # fallback rank
def extract_features_from_url_full(url, opr_api_key):
    parsed = urlparse(url)
    hostname = parsed.hostname if parsed.hostname else ""
    path = parsed.path if parsed.path else ""

    tld_parts = tldextract.extract(url)
    subdomain = tld_parts.subdomain
    domain = tld_parts.top_domain_under_public_suffix
    suffix = tld_parts.suffix

    digits_url = sum(c.isdigit() for c in url)
    digits_host = sum(c.isdigit() for c in hostname)

    def safe_div(x, y): return x / y if y != 0 else 0

    features = {
        'length_url': len(url),
        'length_hostname': len(hostname),
        'ip': 1 if re.match(r'^\d{1,3}(\.\d{1,3}){3}$', hostname) else 0,
        'nb_dots': url.count('.'),
        'nb_qm': url.count('?'),
        'nb_eq': url.count('='),
        'nb_slash': url.count('/'),
        'nb_www': url.count('www'),
        'ratio_digits_url': safe_div(digits_url, len(url)),
        'ratio_digits_host': safe_div(digits_host, len(hostname)),
        'tld_in_subdomain': 1 if suffix in subdomain else 0,
        'prefix_suffix': 1 if '-' in hostname else 0,
        'shortest_word_host': min([len(w) for w in hostname.split('.')]) if hostname else 0,
        'longest_words_raw': max([len(w) for w in re.split(r'\W+', url)]) if url else 0,
        'longest_word_path': max([len(w) for w in path.split('/')]) if path else 0,
        'phish_hints': int('secure' not in hostname.lower()),
        'nb_hyperlinks': get_nb_hyperlinks(url),
        'ratio_intHyperlinks': 0.0,  # replace if you calculate it later
        'empty_title': get_empty_title(url),
        'domain_in_title': 0,  # optional to improve
        'domain_age': get_domain_age(url),
        'google_index': 1,  # improve if needed
        'page_rank': get_page_rank(domain, opr_api_key)
    }

    return [features[f] for f in selected_features]