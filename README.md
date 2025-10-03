# retail-store-analysis

## Running locally

1. Create a virtual environment and install dependencies:

```powershell
C:/path/to/python -m venv ai
ai\Scripts\activate
pip install -r requirements.txt
```

2. Copy `.env.example` to `.env` and update the `GOOGLE_APPLICATION_CREDENTIALS` path.

```powershell
Copy-Item .env.example .env
# then edit .env to point to your JSON key
```

3. Run Streamlit locally:

```powershell
ai\Scripts\python.exe -m streamlit run main.py
```

## Deploying to Streamlit Cloud (or other CI)

- Do NOT commit your `.env` or JSON key to the repo. Use Streamlit Secrets or your platform's secrets manager.
- Streamlit Cloud: go to your app's settings → Secrets and add a key named `GOOGLE_CLOUD_SERVICE_ACCOUNT` (or similar) with the full JSON contents (not the path). In `main.py`, detect whether the env var value is JSON and write it to a temporary file at runtime, then set `GOOGLE_APPLICATION_CREDENTIALS` to that file path.

Example pattern in `main.py` to handle JSON credentials stored as a secret:

```python
import os
from pathlib import Path

gcreds = os.getenv('GOOGLE_CLOUD_SERVICE_ACCOUNT')
if gcreds and gcreds.strip().startswith('{'):
    p = Path('/tmp') / 'gcloud-creds.json'
    p.write_text(gcreds)
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = str(p)
```

For other hosts, consult their secrets documentation to inject either the path or the JSON contents.
# Security notes

- If a service-account JSON was accidentally committed, rotate the key immediately in the Google Cloud Console (IAM & Admin → Service Accounts → Keys → Delete key / Create new key).
- To remove secrets from your Git history, use the BFG Repo Cleaner or `git filter-repo`. Example (BFG):

    1. Install BFG: https://rtyley.github.io/bfg-repo-cleaner/
    2. Run: bfg --delete-files "*.json"
    3. Follow with: git reflog expire --expire=now --all && git gc --prune=now --aggressive

- After cleaning history, force-push to the remote (only if you understand the consequences):
    git push --force

# retail-store-analysis