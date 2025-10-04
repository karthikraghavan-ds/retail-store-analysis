# retail-store-analysis

This repository contains a Streamlit app that queries Google BigQuery and Google Cloud Storage to present retail dataset insights.

Files of interest
- `main.py` — Streamlit app. It uses a service account credential provided via `st.secrets['gcp_service_account']` and initializes BigQuery and Storage clients with those credentials.
- `requirements.txt` — Python dependencies for running the app locally and on Streamlit Cloud.

Prerequisites
- Python 3.10+ (project uses a virtual environment under `ai/` in development).
- A Google Cloud project with BigQuery and Storage access and a service account with appropriate roles (e.g., BigQuery Data Viewer, Storage Object Viewer).

Local development
1. Create and activate a virtual environment (example using Windows PowerShell):

```powershell
C:/path/to/python -m venv ai
ai\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Provide credentials for local testing

The app reads credentials from `st.secrets['gcp_service_account']` (used when running on Streamlit Cloud). For local development you can either:

- Use the Google Application Credentials environment variable pointing to a service account JSON file:

```powershell
$env:GOOGLE_APPLICATION_CREDENTIALS = 'C:\path\to\service-account.json'
python -m streamlit run main.py
```

- Or (easier for local dev) run the app with `st.secrets` by creating a local `.streamlit/secrets.toml` file with your service account JSON content under the `gcp_service_account` key. Example `~/.streamlit/secrets.toml` in project root:

```toml
[gcp_service_account]
# Paste the JSON object as table values, e.g.:
type = "service_account"
project_id = "your-project-id"
# ... other keys from the JSON ...
# Note: TOML does not natively support multi-line strings for private_key easily; instead use a single-line escaped string or set GOOGLE_APPLICATION_CREDENTIALS env var locally.
```

Running locally with Streamlit:

```powershell
ai\Scripts\python.exe -m streamlit run main.py
```

Deploying to Streamlit Cloud
1. Push this repository to GitHub.
2. In Streamlit Cloud, create a new app and point it to your repo and `main.py`.
3. In the Streamlit Cloud app settings go to "Secrets" and add a secret named `gcp_service_account` containing the full JSON object for the service account (paste the JSON). Streamlit exposes secrets via `st.secrets` automatically.

Important security notes
- Do NOT commit service-account JSON files to Git. If you already committed them, rotate/delete the key immediately and remove it from git history (use BFG or `git filter-repo`).
- Limit service account IAM roles to the minimum required privileges.
- Use Streamlit Secrets or your cloud provider's secret manager in production.

Troubleshooting
- Authentication errors: confirm the service account JSON is correct, and that the service account has BigQuery access to `project1-ai-lab-sql.retail`.
- Package errors on Streamlit Cloud: check the deployment logs and ensure `requirements.txt` pins compatible versions.

If you'd like, I can:
- Convert your service-account JSON to a TOML-friendly `secrets.toml` example (redacted), or
- Add a small script to convert JSON to TOML safely for `st.secrets` consumption.

Make it yours
-----------
This repository currently references the owner's Google Cloud project and dataset names (for example `project1-ai-lab-sql.retail`). Other users should replace these with their own project and dataset identifiers before deploying or running queries.

Steps to adapt the project to your environment:

1. Create or choose your Google Cloud project and dataset. Note the `project_id` and dataset names.
2. Update SQL queries in `main.py` to use your `project_id.dataset` (search for occurrences of `project1-ai-lab-sql` and replace).
3. Create a service account in your Google Cloud project and grant it minimum required roles (e.g., BigQuery Data Viewer).
4. Provide credentials:
	- For Streamlit Cloud: add the service account JSON as the `gcp_service_account` secret in the Streamlit app settings.
	- For local testing: either set `GOOGLE_APPLICATION_CREDENTIALS` to your JSON path or create a local `.streamlit/secrets.toml` as described above.
5. Test locally and then push to your GitHub repo and deploy to Streamlit Cloud.

By following these steps you ensure the app runs against your own data and credentials rather than the repository owner's resources.