#!/bin/bash

source ./config.sh

echo "🗑️ Removing the resource group"
az group delete --name $RG_NAME 