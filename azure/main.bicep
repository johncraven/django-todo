// Parameters - things you want to customize per deployment
param appName string = 'django-todo'
param location string = resourceGroup().location
param environment string = 'dev'

// Variables - computed values
var appServicePlanName = '${appName}-plan-${environment}'
var webAppName = '${appName}-webapp-${environment}'

resource appServicePlan 'Microsoft.Web/serverfarms@2024-11-01' = {
  name: appServicePlanName
  location: location
  sku: {
    name: 'B1'
    tier: 'Basic'
    capacity: 1
  }
  properties: {
    reserved: true
  }
}

resource webApp 'Microsoft.Web/sites@2024-11-01' = {
  name: webAppName
  location: location
  kind: 'app,linux'
  properties: {
    serverFarmId: appServicePlan.id
    httpsOnly: true
    siteConfig: {
      linuxFxVersion: 'PYTHON|3.13'
      alwaysOn: true
      ftpsState: 'Disabled'
      appCommandLine: 'bash startup.sh'
      httpLoggingEnabled: true
      logsDirectorySizeLimit: 35
      appSettings: [
        {
          name: 'SCM_DO_BUILD_DURING_DEPLOYMENT'
          value: 'true'
        }
        {
          name: 'DJANGO_SETTINGS_MODULE'
          value: 'myproject.settings'
        }
        {
          name: 'WEBSITES_PORT'
          value: '8000'
        }
        {
          name: 'DEBUG'
          value: 'False'
        }
        {
          name: 'DJANGO_ALLOWED_HOSTS'
          value: 'django-todo-webapp-dev.azurewebsites.net,169.254.129.4'
        }
      ]
    }
  }
}

output webAppUrl string = 'https://${webApp.properties.defaultHostName}'
output gitUrl string = 'https://${webApp.properties.defaultHostName}.git'
output deploymentCredentials string = 'Use: az webapp deployment list-publishing-credentials --name ${webAppName} --resource-group ${resourceGroup().name}'
