#!/bin/bash
set -e

PROJECT_ID="${GCP_PROJECT_ID:-skillbridge-rwanda}"
REGION="${GCP_REGION:-us-central1}"
REGISTRY="${REGION}-docker.pkg.dev/${PROJECT_ID}/skillbridge"

echo "🚀 Deploying SkillBridge Rwanda..."
echo "Project: $PROJECT_ID"
echo "Region: $REGION"

gcloud config set project $PROJECT_ID

echo "🔨 Building backend image..."
cd ../backend
gcloud builds submit --tag ${REGISTRY}/backend:latest .

echo "🚀 Deploying backend to Cloud Run..."
gcloud run deploy skillbridge-backend \
    --image ${REGISTRY}/backend:latest \
    --region $REGION \
    --platform managed \
    --allow-unauthenticated \
    --service-account "skillbridge-backend@${PROJECT_ID}.iam.gserviceaccount.com" \
    --set-env-vars "PROJECT_ID=${PROJECT_ID},LOCATION=${REGION}" \
    --memory 1Gi \
    --cpu 1 \
    --min-instances 0 \
    --max-instances 10 \
    --port 8080

BACKEND_URL=$(gcloud run services describe skillbridge-backend \
    --region $REGION \
    --format 'value(status.url)')

echo "✅ Backend deployed at: $BACKEND_URL"

echo "🔨 Building frontend image..."
cd ../frontend
gcloud builds submit \
    --tag ${REGISTRY}/frontend:latest \
    --build-arg NEXT_PUBLIC_API_URL=${BACKEND_URL} \
    .

echo "🚀 Deploying frontend to Cloud Run..."
gcloud run deploy skillbridge-frontend \
    --image ${REGISTRY}/frontend:latest \
    --region $REGION \
    --platform managed \
    --allow-unauthenticated \
    --set-env-vars "NEXT_PUBLIC_API_URL=${BACKEND_URL}" \
    --memory 512Mi \
    --cpu 1 \
    --min-instances 0 \
    --max-instances 5 \
    --port 3000

FRONTEND_URL=$(gcloud run services describe skillbridge-frontend \
    --region $REGION \
    --format 'value(status.url)')

echo ""
echo "✅ Deployment complete!"
echo ""
echo "🌐 Frontend URL: $FRONTEND_URL"
echo "🔌 Backend URL: $BACKEND_URL"
echo ""
echo "📝 Update CORS settings in backend if needed."
