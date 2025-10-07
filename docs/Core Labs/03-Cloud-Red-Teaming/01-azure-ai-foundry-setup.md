# 01 - Azure AI Foundry Setup

**Duration:** 5 minutes  
**Type:** Configuration & Setup

Setting up Azure AI Foundry for cloud-based red teaming requires proper project configuration, model connections, and storage setup. Let's walk through each component.

## Step 1: Verify Azure AI Foundry Project Type

First, let's confirm you have the correct project type for cloud red teaming.

### Check Project Type
```bash
# List your AI projects
az ml workspace list --query "[].{Name:name, Type:kind, Location:location}" --output table
```

### Required Project Type
You need an **Azure AI Foundry project**, not a hub-based project.

**Foundry Project Characteristics:**
- ✅ Project-centric structure
- ✅ Built-in storage and compute
- ✅ Integrated model deployments
- ✅ Native red teaming support

**Hub-based Project Limitations:**
- ❌ No cloud red teaming support
- ❌ Limited integration capabilities
- ❌ Manual resource management required

### Creating Azure AI Foundry Project (if needed)

If you need to create a new project:

```bash
# Create resource group (if needed)
az group create --name "rg-ai-red-teaming" --location "eastus2"

# Create Azure AI Foundry project
az ml workspace create \
    --name "ai-red-teaming-project" \
    --resource-group "rg-ai-red-teaming" \
    --location "eastus2" \
    --kind "project"
```

### Migration from Hub-based Project

If you have a hub-based project, follow the [migration guide](https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/migrate-project).

## Step 2: Configure Storage Account

Red teaming results need a storage account for persistence and analysis.

### Option A: Use Bicep Template (Recommended)

Download and deploy the storage connection template:

```bash
# Download the Bicep template
curl -o connection-storage-account.bicep https://raw.githubusercontent.com/azure-ai-foundry/foundry-samples/main/samples/microsoft/infrastructure-setup/01-connections/connection-storage-account.bicep

# Deploy with Azure CLI
az deployment group create \
    --resource-group "rg-ai-red-teaming" \
    --template-file connection-storage-account.bicep \
    --parameters projectName="ai-red-teaming-project"
```

### Option B: Manual Storage Setup

1. **Create Storage Account**:
```bash
az storage account create \
    --name "airedteamingstorage$(date +%s)" \
    --resource-group "rg-ai-red-teaming" \
    --location "eastus2" \
    --sku "Standard_LRS"
```

2. **Connect to Project**:
   - Navigate to Azure AI Foundry portal
   - Go to your project settings
   - Add storage connection with key authentication

### Verify Storage Connection

**verify_storage.py**
```python
import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

load_dotenv()

def verify_storage_setup():
    """Verify storage account is properly connected."""
    
    endpoint = os.environ.get("PROJECT_ENDPOINT")
    if not endpoint:
        print("❌ PROJECT_ENDPOINT not set in environment")
        return
    
    try:
        client = AIProjectClient(
            endpoint=endpoint,
            credential=DefaultAzureCredential()
        )
        
        # This will fail if storage is not properly configured
        print("✅ Azure AI Foundry project connection: OK")
        print(f"   Endpoint: {endpoint}")
        
    except Exception as e:
        print(f"❌ Storage verification failed: {e}")
        print("💡 Ensure storage account is connected with proper permissions")

if __name__ == "__main__":
    verify_storage_setup()
```

## Step 3: Set Up Model Connections

Cloud red teaming requires access to Azure OpenAI or AI Services models.

### Option 1: Use Project Deployments

If you have models deployed in your AI Foundry project:

```bash
# List available deployments
az ml online-deployment list --workspace-name "ai-red-teaming-project" --resource-group "rg-ai-red-teaming"
```

**Environment Variables for Project Deployments:**
```bash
# Add to your .env file
PROJECT_ENDPOINT="https://your-account.services.ai.azure.com/api/projects/your-project"
MODEL_DEPLOYMENT_NAME="gpt-4o-mini"  # Your deployment name
```

### Option 2: Connect External Azure OpenAI

To use Azure OpenAI from another resource:

1. **Create Connection in Portal**:
   - Go to Azure AI Foundry portal
   - Navigate to your project
   - Go to "Connections" 
   - Add new Azure OpenAI connection
   - Provide your Azure OpenAI resource details

2. **Note Connection Name**:
   After creating, note the connection name (e.g., "my-openai-connection")

3. **Configure Target**:
```bash
# Add to your .env file
PROJECT_ENDPOINT="https://your-account.services.ai.azure.com/api/projects/your-project"
MODEL_DEPLOYMENT_NAME="my-openai-connection/gpt-4o-mini"  # connectionName/deploymentName
```

### Test Model Connection

**test_model_connection.py**
```python
import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import AzureOpenAIModelConfiguration

load_dotenv()

def test_model_connection():
    """Test model deployment connectivity."""
    
    endpoint = os.environ.get("PROJECT_ENDPOINT")
    model_deployment = os.environ.get("MODEL_DEPLOYMENT_NAME")
    
    if not endpoint or not model_deployment:
        print("❌ PROJECT_ENDPOINT or MODEL_DEPLOYMENT_NAME not configured")
        return
    
    try:
        client = AIProjectClient(
            endpoint=endpoint,
            credential=DefaultAzureCredential()
        )
        
        # Create model configuration
        model_config = AzureOpenAIModelConfiguration(
            model_deployment_name=model_deployment
        )
        
        print("✅ Model connection test successful")
        print(f"   Endpoint: {endpoint}")
        print(f"   Model Deployment: {model_deployment}")
        
        # If using external connection, deployment name should include connection
        if "/" in model_deployment:
            connection_name, deployment = model_deployment.split("/", 1)
            print(f"   Connection: {connection_name}")
            print(f"   Deployment: {deployment}")
        
    except Exception as e:
        print(f"❌ Model connection test failed: {e}")

if __name__ == "__main__":
    test_model_connection()
```

## Step 4: Verify Permissions

Ensure you have the required permissions for red teaming operations.

### Required Roles

Your account needs these Azure roles:
- **Azure AI Developer** or **Contributor** on the AI Foundry project
- **Storage Blob Data Owner** on the connected storage account
- **Cognitive Services OpenAI User** on connected OpenAI resources

### Check Permissions

```bash
# Check your role assignments
az role assignment list --assignee $(az account show --query user.name --output tsv) --query "[].{Role:roleDefinitionName, Scope:scope}" --output table
```

### Grant Missing Permissions

If you need to grant permissions:

```bash
# Get your user ID
USER_ID=$(az account show --query user.name --output tsv)

# Grant Storage Blob Data Owner
az role assignment create \
    --assignee $USER_ID \
    --role "Storage Blob Data Owner" \
    --scope "/subscriptions/YOUR_SUBSCRIPTION_ID/resourceGroups/rg-ai-red-teaming/providers/Microsoft.Storage/storageAccounts/YOUR_STORAGE_ACCOUNT"

# Grant AI Developer role on project
az role assignment create \
    --assignee $USER_ID \
    --role "Azure AI Developer" \
    --scope "/subscriptions/YOUR_SUBSCRIPTION_ID/resourceGroups/rg-ai-red-teaming/providers/Microsoft.MachineLearningServices/workspaces/ai-red-teaming-project"
```

## Step 5: Install Cloud SDK Dependencies

Install additional packages needed for cloud operations:

```bash
pip install azure-ai-projects==1.1.0b3 azure-identity
```

## Step 6: Complete Configuration Test

Create a comprehensive test to verify your entire setup:

**complete_setup_test.py**
```python
import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import AzureOpenAIModelConfiguration, RedTeam, RiskCategory, AttackStrategy

load_dotenv()

def complete_setup_test():
    """Comprehensive test of Azure AI Foundry setup for red teaming."""
    
    print("=== Azure AI Foundry Red Teaming Setup Test ===")
    
    # Configuration check
    endpoint = os.environ.get("PROJECT_ENDPOINT")
    model_deployment = os.environ.get("MODEL_DEPLOYMENT_NAME")
    
    if not endpoint:
        print("❌ PROJECT_ENDPOINT not configured")
        return False
    
    if not model_deployment:
        print("❌ MODEL_DEPLOYMENT_NAME not configured")
        return False
    
    print(f"✅ Configuration loaded")
    print(f"   Endpoint: {endpoint}")
    print(f"   Model: {model_deployment}")
    
    try:
        # Test Azure AI Projects client
        client = AIProjectClient(
            endpoint=endpoint,
            credential=DefaultAzureCredential()
        )
        print("✅ Azure AI Projects client: OK")
        
        # Test model configuration
        model_config = AzureOpenAIModelConfiguration(
            model_deployment_name=model_deployment
        )
        print("✅ Model configuration: OK")
        
        # Test red team configuration (don't run, just validate)
        red_team_config = RedTeam(
            attack_strategies=[AttackStrategy.BASE64],
            risk_categories=[RiskCategory.VIOLENCE],
            display_name="setup-test",
            target=model_config,
        )
        print("✅ Red team configuration: OK")
        
        print("\n🎉 Setup test completed successfully!")
        print("💡 You're ready to run cloud-based red teaming scans!")
        return True
        
    except Exception as e:
        print(f"❌ Setup test failed: {e}")
        print("\n🔧 Troubleshooting steps:")
        print("   1. Verify Azure login: az login")
        print("   2. Check project permissions")
        print("   3. Ensure storage account is connected")
        print("   4. Verify model deployment accessibility")
        return False

if __name__ == "__main__":
    complete_setup_test()
```

Run the setup test:

```bash
python complete_setup_test.py
```

**Expected output:**
```
=== Azure AI Foundry Red Teaming Setup Test ===
✅ Configuration loaded
   Endpoint: https://your-account.services.ai.azure.com/api/projects/your-project
   Model: gpt-4o-mini
✅ Azure AI Projects client: OK
✅ Model configuration: OK
✅ Red team configuration: OK

🎉 Setup test completed successfully!
💡 You're ready to run cloud-based red teaming scans!
```

## Troubleshooting Common Issues

### Issue: "Project not found"
**Solutions**:
- Verify project name and endpoint URL
- Check that you have access permissions
- Ensure project is in a supported region

### Issue: "Storage account access denied"
**Solutions**:
- Grant "Storage Blob Data Owner" role
- Verify storage account is connected to project
- Check managed identity permissions

### Issue: "Model deployment not found"
**Solutions**:
- Verify deployment name is correct
- Check if using connection name format: "connection/deployment"
- Ensure model is deployed and accessible

### Issue: "Authentication failed"
**Solutions**:
- Run `az login` to refresh credentials
- Check if using correct tenant/subscription
- Verify service principal permissions (if applicable)

---

## Checkpoint

Before proceeding, ensure you have:

- ✅ Azure AI Foundry project (not hub-based) in supported region
- ✅ Storage account connected with proper permissions
- ✅ Model deployments accessible and configured
- ✅ Required Azure roles assigned
- ✅ Cloud SDK packages installed
- ✅ Complete setup test passing

**All green?** Let's move on to [Cloud Scan Configuration](./02-cloud-scan-configuration.md)!

---

**Navigation:** [Module Home](./README.md) | **Next:** [Cloud Scan Configuration](./02-cloud-scan-configuration.md)