#!/bin/bash

RG_NAME="rg-django-todo-dev"
LOCATION="eastus2"
MANAGED_IDENTITY_NAME="django-todo-github-identity"

echo "📦️ Creating a new resource group if it doesn't exist"
az group create --name $RG_NAME --location $LOCATION

echo "🧑‍🔧 Creating the managed identity"
az identity create --resource-group $RG_NAME --name $MANAGED_IDENTITY_NAME

echo "🧑‍🏭 Granting permissions"
PRINCIPAL_ID=$(az identity show --resource-group $RG_NAME --name $MANAGED_IDENTITY_NAME --query principalId --output tsv)
az role assignment create --assignee $PRINCIPAL_ID --role Contributor --scope /subscriptions/$(az account show --query id --output tsv)/resourceGroups/$RG_NAME

echo "🏗️ deploying infrastructure"
az deployment group create --resource-group $RG_NAME --template-file main.bicep