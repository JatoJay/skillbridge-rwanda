#!/bin/bash
set -e

PROJECT_ID="${GCP_PROJECT_ID:-skillbridge-rwanda}"
REGION="${GCP_REGION:-us-central1}"

echo "🚀 Setting up SkillBridge Rwanda on GCP..."
echo "Project: $PROJECT_ID"
echo "Region: $REGION"

gcloud config set project $PROJECT_ID

echo "📦 Enabling required APIs..."
gcloud services enable \
    aiplatform.googleapis.com \
    translate.googleapis.com \
    language.googleapis.com \
    run.googleapis.com \
    cloudbuild.googleapis.com \
    secretmanager.googleapis.com \
    firestore.googleapis.com \
    sqladmin.googleapis.com \
    storage.googleapis.com \
    artifactregistry.googleapis.com

echo "🔐 Creating service account..."
SA_NAME="skillbridge-backend"
SA_EMAIL="${SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"

gcloud iam service-accounts create $SA_NAME \
    --display-name="SkillBridge Backend Service Account" \
    --description="Service account for SkillBridge Rwanda backend" \
    || echo "Service account may already exist"

echo "📝 Granting IAM roles..."
for ROLE in \
    "roles/aiplatform.user" \
    "roles/cloudtranslate.user" \
    "roles/datastore.user" \
    "roles/cloudsql.client" \
    "roles/storage.objectViewer" \
    "roles/secretmanager.secretAccessor"
do
    gcloud projects add-iam-policy-binding $PROJECT_ID \
        --member="serviceAccount:${SA_EMAIL}" \
        --role="$ROLE" \
        --quiet
done

echo "📁 Creating Artifact Registry repository..."
gcloud artifacts repositories create skillbridge \
    --repository-format=docker \
    --location=$REGION \
    --description="SkillBridge Rwanda container images" \
    || echo "Repository may already exist"

echo "🔥 Setting up Firestore..."
gcloud firestore databases create \
    --location=$REGION \
    --type=firestore-native \
    || echo "Firestore may already be set up"

echo "🗄️ Creating Cloud Storage bucket..."
BUCKET_NAME="${PROJECT_ID}-uploads"
gsutil mb -l $REGION gs://${BUCKET_NAME} || echo "Bucket may already exist"
gsutil iam ch allUsers:objectViewer gs://${BUCKET_NAME} || true

echo "🔑 Creating secrets..."
echo "placeholder" | gcloud secrets create database-url \
    --data-file=- \
    --replication-policy=automatic \
    || echo "Secret may already exist"

echo ""
echo "✅ GCP setup complete!"
echo ""
echo "Next steps:"
echo "1. Update secrets in Secret Manager with real values"
echo "2. Run ./deploy.sh to deploy the application"
echo ""
echo "Environment variables needed in .env:"
echo "  PROJECT_ID=$PROJECT_ID"
echo "  LOCATION=$REGION"
