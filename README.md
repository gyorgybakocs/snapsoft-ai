# SnapSoft AI Homework – End-to-End Serverless Data Ingestion & ML Pipeline

This repository contains a professional-grade, event-driven data pipeline and machine learning workflow hosted on AWS.  
It demonstrates expertise in Infrastructure as Code (Terraform), Serverless ETL (Lambda), and Machine Learning (SageMaker).

---

## 🚀 Overview

The system automates the following lifecycle for car price data:

- **Ingestion:** A raw CSV file is uploaded to an S3 Landing bucket.
- **Processing:** An AWS Lambda (Python/Pandas) is triggered to clean the data and extract feature-rich attributes (e.g., brand names).
- **Curated Storage:** The processed file is moved to a Curated bucket.
- **Machine Learning:** A SageMaker Studio notebook dynamically discovers the data, trains a Random Forest Regressor, and generates diagnostic reports.

---

## 📂 Source Code & Access

### Option A – Google Drive (Recommended for Submission)

**Download:** Obtain the project ZIP archive from the following link:  
`https://drive.google.com/file/d/1k6J__OrD2k7nFQU--FnC8LEeq0B19ARJ/view?usp=sharing`

**Unzip locally:**

```bash
unzip snapsoft-ai.zip
cd snapsoft-ai
```
---

### Option B – Git Repository

```bash
git clone git@github.com:gyorgybakocs/snapsoft-ai.git
cd snapsoft-ai
```

---

## ⚙️ Prerequisites & AWS Setup

- **AWS Account:** Admin access to a standard AWS account.
- **Tools:** AWS CLI v2, Terraform (v1.0.0+).

**Configuration – set credentials locally:**

```bash
aws configure
# Input your Access Key, Secret Key, and Region (default: eu-central-1)
```

---

## 💡 Technical Highlight – Dynamic S3 Naming

To avoid the common `BucketAlreadyExists` error caused by S3's global namespace, this project uses identity-based dynamic naming.

**providers.tf:**

```hcl
data "aws_caller_identity" "current" {}

locals {
  account_id  = data.aws_caller_identity.current.account_id
  user_suffix = replace(lower(data.aws_caller_identity.current.user_id), "/[^a-z0-9]/", "-")
}
```

**Bucket template:**

```hcl
${var.name_prefix}-landing-${local.account_id}-${local.user_suffix}
```

**Benefit:**  
Ensures global uniqueness and keeps buckets grouped logically in the AWS console.

---

## 🛠️ Deployment Guide

### 1. Provision Infrastructure

```bash
cd infra
terraform init
terraform plan
terraform apply -auto-approve
```

Terraform outputs the generated bucket names.

---

### 2. Trigger the ETL Pipeline

Upload the dataset to the landing bucket:

```bash
LANDING_BUCKET=$(terraform output -raw landing_bucket_name)

aws s3 cp ../data/ml_sample_data_snapsoft.csv \
s3://$LANDING_BUCKET/input/ml_sample_data_snapsoft.csv
```

---

## 🧠 Machine Learning Pipeline

Notebook: `notebooks/car_price_prediction.ipynb`

**Key Features & Workflow:**

- **Dynamic Data Discovery:** Automatically locates the curated dataset in S3 without hardcoded paths.
- **Robust Preprocessing:** Handles missing values (Imputation) and categorical features (One-Hot Encoding) with transparent diagnostics.
- **Model Training:** Random Forest Regressor (80/20 Train/Test split).
- **Business Logic Integration:** Implements a **"Safety Buffer" strategy (Underestimation)** to prioritize rapid inventory turnover, ensuring predicted prices are competitive.
- **Advanced Diagnostics:**
    - **Actual vs. Predicted:** Visual comparison of model fit.
    - **Residual Analysis:** Verifies that errors are randomly distributed (or intentionally shifted).
    - **Error Distribution:** Histograms confirming the intentional pricing bias to meet business safety goals.

---

## 📁 Project Structure

```
infra/       Terraform manifests
lambda/      Python ETL script
notebooks/   SageMaker notebook
data/        Sample CSV files
```

---

## 🧹 Cleanup

```bash
cd infra
terraform destroy -auto-approve
```

Force destroy is enabled on S3 buckets to ensure removal.
