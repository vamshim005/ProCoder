import requests

HACKERRANK_API_URL = "https://api.hackerrank.com/checker/submission.json"
HACKERRANK_API_KEY = "YOUR_API_KEY"  # Replace with your actual API key

LANGUAGE_MAP = {
    'c': 'c',
    'cpp': 'cpp',
    'python2': 'python2',
    'python3': 'python3',
    'java': 'java'
}

def judge_with_hackerrank(source_code, language, testcases):
    data = {
        'source': source_code,
        'lang': LANGUAGE_MAP[language],
        'testcases': testcases,  # List of strings
        'api_key': HACKERRANK_API_KEY,
    }
    response = requests.post(HACKERRANK_API_URL, data=data)
    if response.status_code == 200:
        return response.json()
    else:
        return {'error': 'API request failed', 'status_code': response.status_code} 