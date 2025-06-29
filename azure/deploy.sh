#!/bin/bash
set -e #Exit on any error

source ./config.sh

echo "🚀 Deploying ${APP_NAME} to ${ENVIRONMENT}"

# 1. Create/ensure resource group exists
az group create --name $RG_NAME --location $LOCATION

# 2. Deploy infrastructure
echo "📦️ Deploying infrastructure..."
DEPLOYMENT_OUTPUT=$(az deployment group create \
--resource-group $RG_NAME \
--template-file ./main.bicep \
--parameters appName=$APP_NAME environment=$ENVIRONMENT \
--query "properties.outputs" \
--output json)

#3 Extract Git URL and Creds
echo "👀 fetching deployment results"
GIT_URL=$(echo $DEPLOYMENT_OUTPUT | jq -r '.gitUrl.value')


CREDS=$(az webapp deployment list-publishing-credentials --name $WEBAPP_NAME --resource-group $RG_NAME)
USERNAME=$(echo $CREDS | jq -r '.publishingUserName')
PASSWORD=$(echo $CREDS | jq -r '.publishingPassword')

# 4. Configure Git remote
echo "🔧 Configuring Git remote..."
git remote remove azure 2>/dev/null || true  # Remove if exists
git remote add azure "https://${USERNAME}:${PASSWORD}@${WEBAPP_NAME}.scm.azurewebsites.net/${WEBAPP_NAME}.git"

# 5. Deploy code
echo "🚀 Pushing code..."
git push azure deploy/azure:master 

echo "✅ Deployment complete!"
echo "🌐 App URL: https://${WEBAPP_NAME}.azurewebsites.net"
