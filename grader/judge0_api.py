import requests
import time

JUDGE0_API_URL = "https://judge0-ce.p.rapidapi.com/submissions"
JUDGE0_API_HOST = "judge0-ce.p.rapidapi.com"
JUDGE0_API_KEY = "86f89cae64msh7573637c57744a7p128c9cjsn0d067254dbad"

LANGUAGE_MAP = {
    'c': 50,
    'cpp': 54,
    'python2': 70,
    'python3': 71,
    'java': 62
}

def judge_with_judge0(source_code, language, testcases):
    results = []
    for testcase in testcases:
        payload = {
            "source_code": source_code,
            "language_id": LANGUAGE_MAP[language],
            "stdin": testcase
        }
        headers = {
            "content-type": "application/json",
            "X-RapidAPI-Host": JUDGE0_API_HOST,
            "X-RapidAPI-Key": JUDGE0_API_KEY
        }
        # Submit code for execution
        response = requests.post(JUDGE0_API_URL + "?base64_encoded=false&wait=false", json=payload, headers=headers)
        if response.status_code != 201:
            results.append({'error': 'Submission failed', 'status_code': response.status_code})
            continue
        token = response.json()['token']
        # Poll for result
        for _ in range(10):
            res = requests.get(f"{JUDGE0_API_URL}/{token}?base64_encoded=false", headers=headers)
            if res.status_code == 200 and res.json().get('status', {}).get('id') in [3, 6, 11]:  # 3: Accepted, 6: Compilation Error, 11: Runtime Error
                results.append(res.json())
                break
            time.sleep(1)
        else:
            results.append({'error': 'Timeout waiting for result'})
    return results 