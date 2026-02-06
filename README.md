# SnapSoft AI Homework – Serverless Data Ingestion Pipeline (AWS + Terraform)

This project contains my implementation of the SnapSoft AI homework assignment.  
The goal is to demonstrate a minimal, reproducible, event-driven data ingestion pipeline on AWS using Infrastructure as Code (Terraform).

---

## Overview

At a high level, the system works as follows:

- A CSV file is uploaded to an S3 **landing** bucket
- The upload triggers an AWS **Lambda** function
- The Lambda processes the input file and writes the result to an S3 **curated** bucket

The infrastructure is defined entirely in Terraform and split into small, focused files (S3, IAM, Lambda, triggers) to keep the project readable and easy to review.

---

## Source Code

You can obtain the project in one of the following ways.

### Option A – Download ZIP from Google Drive (as requested in the assignment)

1. Download: `XXX_GOOGLE_DRIVE_LINK_XXX`
2. Unzip locally:
   ```bash
   unzip snapsoft-ai.zip
   cd snapsoft-ai
   ```

### Option B – Clone the public Git repository

```bash
git@github.com:gyorgybakocs/snapsoft-ai.git
cd snapsoft-ai
```

---

## Prerequisites

- AWS account (Free Tier is sufficient)
- AWS CLI v2 installed and configured
- Terraform installed

---

## AWS Credentials

This project does **not** require sharing any credentials.

All resources are created in the **reviewer’s own AWS account**.  
Please configure AWS access locally using one of the standard methods:

### AWS CLI configuration

```bash
aws configure
```

### Environment variables (optional)

```bash
export AWS_ACCESS_KEY_ID="YOUR_KEY"
export AWS_SECRET_ACCESS_KEY="YOUR_SECRET"
export AWS_DEFAULT_REGION="eu-central-1"
```

Credentials must **never** be committed into the repository.

---

## Important Note About S3 Bucket Names

Before running Terraform, you MUST change the value of `name_prefix` in infra/variables.tf.

S3 bucket names are globally unique.  
The default prefix in this repository is already taken, because it was used during development.

---

## Deploy Infrastructure

From the project root:

```bash
cd infra
terraform init
terraform plan
terraform apply
```

Terraform will output the created S3 bucket names.

---

## Upload a CSV File (Trigger the Lambda)

After the infrastructure is created, upload a CSV file into the **landing** bucket.

You can use either AWS Console or CLI.

### Using AWS CLI

```bash
cd infra
LANDING_BUCKET=$(terraform output -raw landing_bucket_name)
aws s3 cp ../data/ml_sample_data_snapsoft.csv s3://$LANDING_BUCKET/input/ml_sample_data_snapsoft.csv
```

### Using AWS Console

1. Open S3 in AWS Console
2. Open the **landing** bucket
3. Create a folder named `input` (optional but recommended)
4. Upload a `.csv` file into this folder

---

## Expected Behavior

- Uploading a `.csv` file triggers the Lambda function
- The Lambda processes the file
- The result is written into the **curated** bucket
