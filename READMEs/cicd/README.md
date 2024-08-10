# TLDR

Setting up CICD for Embedding API

##

- added Service Account creds to GitHub secrets config
- change .github/workflows/cicd.yaml
- Enable the Artifact Registry API on your GCP project if needed
- `gcloud artifacts repositories create fullstack-rag-embedding-api --repository-format docker --project fullstack-rag --location us-central1` √
- 