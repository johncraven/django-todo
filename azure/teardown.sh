#!/bin/bash

echo "💣️ Starting the teardown"
az resource list --resource-group rg-django-todo-dev --query "[].id" --output tsv | xargs -I {} az resource delete --ids {}