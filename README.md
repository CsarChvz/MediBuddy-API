# FastAPI on AWS Lambda (Terraform + ECR Image)

A simple, extensible FastAPI scaffold designed for AWS Lambda behind API Gateway, deployed as a container image in ECR. Terraform manages the infra, Mangum adapts ASGI to Lambda.

## Features
- Service/Repository project layout
- AWS Lambda + API Gateway (HTTP API) via Terraform
- ECR container image support (bypass Lambda ZIP size limits, include native libs)
- Mangum to bridge ASGI to Lambda
- .env config via pydantic-settings + python-dotenv
- Blazing fast dependency management using `uv`
- Easy to extend (add SQS, DB, multiple Lambdas)

## Project Structure
```text
app/
  api/
    routes.py
  services/
    hello_service.py
  repositories/
    stub_repo.py
  dependencies/
  core/
    config.py
  main.py
handler.py
requirements.txt
.env
Dockerfile
.dockerignore
scripts/
terraform/
  main.tf
  variables.tf
  outputs.tf
  lambda.tf
```

## Quickstart (one command deploy)

Prereqs: AWS CLI configured, Terraform >= 1.6, Docker, and [uv](https://docs.astral.sh/uv/) installed. Set your `.env` values to drive the deploy (fallback defaults are provided):

```env
# .env
AWS_REGION=us-east-1
STAGE=dev
LAMBDA_NAME=fastapi_aws_lambda
ECR_REPO=fastapi-aws-lambda
IMAGE_TAG=latest
LAMBDA_MEMORY=512  # Lambda memory size in MB
LAMBDA_TIMEOUT=30  # Lambda timeout in seconds

DEV_DATABASE_URL=postgresql://postgres:postgres@127.0.0.1:5433/medibuddy
TEST_DATABASE_URL=postgresql://postgres:postgres@127.0.0.1:5434/medibuddy
```

Deploy (builds the image, pushes to ECR, applies Terraform):

```bash
make deploy
```

Manual override (optional):

```bash
make deploy AWS_REGION=us-east-1 STAGE=dev LAMBDA_NAME=my-func ECR_REPO=my-repo IMAGE_TAG=v1
```

The `api_endpoint` will be printed. Test it:

```bash
curl "$API_ENDPOINT/"
```

## Local development

We use **`uv`** for lightning-fast virtual environment creation and dependency installation:

```bash
# 1. Create a virtual environment using uv
uv venv

# 2. Activate it
source .venv/bin/activate

# 3. Install dependencies from requirements.txt instantly
uv pip install -r requirements.txt

# 4. Run the local server
uvicorn app.main:app --reload --port 8000
```

*(Note: If you migrated the project to use `pyproject.toml`, you can simply run `uv sync` instead of the pip install command).*

Or via Makefile (auto-creates .venv and installs):

```bash
make dev
```

Or with Docker (uses the `dev` stage):

```bash
make docker-run
```

Visit http://localhost:8000/ and http://localhost:8000/docs

## Teardown: destroy infra and ECR image/repo

One command (uses `.env`):

```bash
make destroy-all
```

Manual override:

```bash
make destroy-all AWS_REGION=us-east-1 STAGE=dev LAMBDA_NAME=my-func ECR_REPO=my-repo IMAGE_TAG=v1
```

## Extensibility
- Add new endpoints under `app/api`
- Add services under `app/services` and repositories under `app/repositories`
- Add new Lambda handlers by creating more entrypoints like `handler.py` and updating Terraform
- Introduce SQS, DynamoDB, or other AWS services in Terraform, then wire repos/services

## Environment
`.env` controls runtime defaults; Terraform also passes the key ones into Lambda.

```env
APP_ENV=dev
STAGE=dev
AWS_REGION=us-east-1
LAMBDA_NAME=fastapi_aws_lambda

POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
# Notice we use standard synchronous postgresql:// now!
DEV_DATABASE_URL=postgresql://postgres:postgres@127.0.0.1:5433/medibuddy
```

## Notes
- Lambda runtime is Python 3.12 for the base image. Keep native wheels compatible.
- Minimal dependencies purposely kept small.
- The project currently uses `requirements.txt`, but it is fully ready to be migrated to a modern `pyproject.toml` workflow using `uv init`.