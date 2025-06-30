// Parameters - things you want to customize per deployment
param appName string = 'django-todo'
param location string = resourceGroup().location
param environment string = 'dev'

// Variables - computed values
var appServicePlanName = '${appName}-plan-${environment}'
var webAppName = '${appName}-webapp-${environment}'
var postgresServerName = '${appName}-webapp-${environment}'
var postgresDatabaseName = '${appName}-db'
var dbPassword = uniqueString(resourceGroup().id, 'postgres-password')
var dbUsername = 'dbadmin'

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

resource postgresServer 'Microsoft.DBforPostgreSQL/flexibleServers@2024-08-01' = {
  name: postgresServerName
  location: location
  sku: {
    name: 'Standard_B1ms'
    tier: 'Burstable'
  }
  properties: {
    administratorLogin: dbUsername
    administratorLoginPassword: dbPassword
    version: '15'
    storage: {
      storageSizeGB: 32
    }
    network: {
      publicNetworkAccess: 'Enabled'
    }
  }
}

resource allowAzureServices 'Microsoft.DBforPostgreSQL/flexibleServers/firewallRules@2024-08-01' = {
  parent: postgresServer
  name: 'AllowAllAzureServices'
  properties: {
    startIpAddress: '0.0.0.0'
    endIpAddress: '0.0.0.0'
  }
}

resource postgresDatabase 'Microsoft.DBforPostgreSQL/flexibleServers/databases@2024-08-01' = {
  parent: postgresServer
  name: postgresDatabaseName
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
          value: 'django-todo-webapp-dev.azurewebsites.net,azurewebsites.net'
        }
        {
          name: 'POSTGRES_HOST'
          value: postgresServer.properties.fullyQualifiedDomainName
        }
        {
          name: 'POSTGRES_DB'
          value: postgresDatabaseName
        }
        {
          name: 'POSTGRES_USER'
          value: dbUsername
        }
        {
          name: 'POSTGRES_PASSWORD'
          value: dbPassword
        }
        {
          name: 'POSTGRES_PORT'
          value: '5432'
        }
      ]
    }
  }
  dependsOn: [
    postgresDatabase
  ]
}

output webAppUrl string = 'https://${webApp.properties.defaultHostName}'
output gitUrl string = 'https://${webApp.properties.defaultHostName}.git'
output deploymentCredentials string = 'Use: az webapp deployment list-publishing-credentials --name ${webAppName} --resource-group ${resourceGroup().name}'
output postgresServer string = postgresServer.properties.fullyQualifiedDomainName
output databaseName string = postgresDatabaseName
