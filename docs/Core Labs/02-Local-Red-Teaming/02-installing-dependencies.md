# 02 - Validate Setup

**Duration:** 5 minutes  
**Type:** Validation & Configuration

Now that we've deployed our infrastructure, let's validate that the template has all the dependencies pre-installed and update our environment variables with the actual deployment values.

## Step 1: Validate Template Dependencies

The Azure AI Agents template should have automatically installed all required dependencies. Let's verify:

### 1.1 Check PyRIT Installation

![PyRIT Attack Strategies](https://learn.microsoft.com/en-us/azure/ai-foundry/media/evaluations/red-teaming-agent/how-ai-red-teaming-works.png)

*How AI Red Teaming Works - Direct attacks vs. Attack strategies to bypass AI safety measures*

```bash
# Test PyRIT availability
python -c "
try:
    from azure.ai.evaluation.red_team import RedTeam, RiskCategory
    print('✅ PyRIT red teaming capabilities available')
    print('   - RedTeam class imported successfully')
    print('   - Risk categories available:', [cat.value for cat in RiskCategory])
except ImportError as e:
    print(f'❌ PyRIT not available: {e}')
    print('💡 Run: uv pip install \"azure-ai-evaluation[redteam]\"')
"
```

### 1.2 Check Azure AI Projects SDK

```bash
# Test Azure AI Projects integration
python -c "
try:
    from azure.ai.projects import AIProjectClient
    from azure.identity import DefaultAzureCredential
    print('✅ Azure AI Projects SDK available')
    print('   - AIProjectClient imported successfully')
    print('   - DefaultAzureCredential available')
except ImportError as e:
    print(f'❌ Azure AI Projects SDK not available: {e}')
    print('💡 Check template installation')
"
```

### 1.3 Verify Python Version Compatibility

```bash
# Check Python version for PyRIT compatibility
python -c "
import sys
version = sys.version_info

if version >= (3, 10) and version < (3, 13):
    print(f'✅ Python {version.major}.{version.minor} - Compatible with PyRIT')
else:
    print(f'❌ Python {version.major}.{version.minor} - PyRIT requires Python 3.10-3.12')
"
```

## Step 2: Update Environment Variables from Deployment

Our deployment created actual Azure resources. Now we need to capture their details in our `.env` file.

### 2.1 Get Azure AI Foundry Project Details

```bash
# Navigate to the infrastructure directory
cd .infra-setup

# Get the deployed project information
azd env get-values
```

This will show you the actual deployed values. Look for these key variables:

```bash
AZURE_PROJECT_NAME="your-actual-project-name"
AZURE_OPENAI_ENDPOINT="https://your-openai-resource.openai.azure.com/"
PROJECT_ENDPOINT="https://your-account.services.ai.azure.com/api/projects/your-project"
```

### 2.2 Update Your .env File

Navigate back to the workshop root and update your `.env` file:

```bash
# Return to workshop root
cd ..

# Edit your .env file with the actual values
# Replace the placeholder values with the ones from `azd env get-values`
```

**Required Updates in `.env`:**
```bash
# Update these with your actual deployment values
AZURE_PROJECT_NAME="redteam-lab-ai-foundry-project"
AZURE_OPENAI_ENDPOINT="https://redteam-lab-openai-12345.openai.azure.com/"
AZURE_OPENAI_KEY="your-actual-api-key-from-deployment"
PROJECT_ENDPOINT="https://eastus2.services.ai.azure.com/api/projects/your-project-id"

# These should match your OpenAI endpoint values
PYRIT_AZURE_OPENAI_ENDPOINT="${AZURE_OPENAI_ENDPOINT}"
PYRIT_AZURE_OPENAI_KEY="${AZURE_OPENAI_KEY}"
PYRIT_AZURE_OPENAI_DEPLOYMENT="${AZURE_OPENAI_DEPLOYMENT}"
```

### 2.3 Validate Environment Variables

```bash
# Test that all required variables are set
python -c "
import os
from dotenv import load_dotenv

load_dotenv()

required_vars = {
    'AZURE_SUBSCRIPTION_ID': 'Azure subscription ID',
    'AZURE_RESOURCE_GROUP': 'Resource group name',
    'AZURE_PROJECT_NAME': 'AI Foundry project name',
    'AZURE_OPENAI_ENDPOINT': 'OpenAI endpoint URL',
    'AZURE_OPENAI_KEY': 'OpenAI API key',
    'PROJECT_ENDPOINT': 'AI Foundry project endpoint',
    'AZURE_OPENAI_DEPLOYMENT': 'Model deployment name'
}

print('🔍 Environment Variable Validation')
print('=' * 40)

all_good = True
for var, description in required_vars.items():
    value = os.getenv(var)
    if value:
        # Mask sensitive information
        display_value = value[:10] + '...' if 'key' in var.lower() else value
        print(f'✅ {var}: {display_value}')
    else:
        print(f'❌ {var}: Not set ({description})')
        all_good = False

if all_good:
    print('\\n🎉 All environment variables properly configured!')
else:
    print('\\n⚠️  Please update missing variables in your .env file')
"
```

## Step 3: Test Azure Connectivity

Let's verify we can connect to our deployed Azure resources:

### 3.1 Test Azure AI Foundry Connection

```bash
# Test connection to Azure AI Foundry project
python -c "
import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

load_dotenv()

try:
    # Test Azure AI Foundry connection
    project_endpoint = os.getenv('PROJECT_ENDPOINT')
    if not project_endpoint:
        raise ValueError('PROJECT_ENDPOINT not configured')
    
    client = AIProjectClient(
        endpoint=project_endpoint,
        credential=DefaultAzureCredential(exclude_interactive_browser_credential=False)
    )
    
    print('✅ Azure AI Foundry connection successful')
    print(f'   Endpoint: {project_endpoint}')
    
except Exception as e:
    print(f'❌ Azure AI Foundry connection failed: {e}')
    print('💡 Check your PROJECT_ENDPOINT and Azure authentication')
"
```

### 3.2 Test OpenAI Model Access

```bash
# Test OpenAI model deployment access
python -c "
import os
from dotenv import load_dotenv

load_dotenv()

try:
    # Import here to check availability
    from openai import AzureOpenAI
    from azure.identity import DefaultAzureCredential
    
    endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
    deployment = os.getenv('AZURE_OPENAI_DEPLOYMENT', 'gpt-4o-mini')
    
    if not endpoint:
        raise ValueError('AZURE_OPENAI_ENDPOINT not configured')
    
    print('✅ OpenAI model access configured')
    print(f'   Endpoint: {endpoint}')
    print(f'   Deployment: {deployment}')
    
except ImportError:
    print('❌ OpenAI client not available')
    print('💡 Dependencies may need to be installed')
except Exception as e:
    print(f'❌ OpenAI connection test failed: {e}')
    print('💡 Check your AZURE_OPENAI_ENDPOINT configuration')
"
```

## Step 4: Verify Regional Support

AI Red Teaming Agent is only available in specific regions. Let's verify our deployment region:

```bash
# Check deployment region
python -c "
import os
from dotenv import load_dotenv

load_dotenv()

supported_regions = ['eastus2', 'swedencentral', 'francecentral', 'switzerlandwest']
location = os.getenv('AZURE_LOCATION', '').lower()

print(f'🌍 Deployment Region: {location}')

if location in supported_regions:
    print('✅ Region supports AI Red Teaming Agent')
else:
    print('⚠️  Region may not fully support AI Red Teaming Agent')
    print(f'   Supported regions: {supported_regions}')
    print('   💡 Consider redeploying to swedencentral for full support')
"
```

## 🎯 Validation Complete!

If all tests pass, your template validation is successful! You now have:

- ✅ **Verified Dependencies**: PyRIT and Azure AI SDKs properly installed
- ✅ **Environment Variables**: All required variables configured with actual values  
- ✅ **Azure Connectivity**: Connection to AI Foundry and OpenAI resources verified
- ✅ **Regional Support**: Deployment in supported region confirmed

## Troubleshooting Common Issues

### Issue: Missing Dependencies
```bash
# If dependencies are missing, install them manually
uv pip install "azure-ai-evaluation[redteam]"
uv pip install azure-ai-projects
uv pip install openai
```

### Issue: Authentication Problems
```bash
# Re-authenticate with Azure
az login --use-device-code
az account set --subscription "your-subscription-id"
```

### Issue: Environment Variables Not Loading
```bash
# Check .env file location and format
ls -la .env
head -5 .env
```

---

**Navigation:** [Previous](./01-environment-setup.md) | [Module Home](./README.md) | **Next:** [First Red Team Scan](./03-first-red-team-scan.md)
print("\n=== Functionality Tests ===")

try:
    from azure.ai.evaluation.red_team import RedTeam, RiskCategory
    print("✅ RedTeam import: OK")
except ImportError as e:
    print(f"❌ RedTeam import failed: {e}")

try:
    from azure.identity import DefaultAzureCredential
    credential = DefaultAzureCredential()
    print("✅ Azure credentials: OK")
except Exception as e:
    print(f"❌ Azure credentials failed: {e}")

try:
    import pandas as pd
    df = pd.DataFrame({'test': [1, 2, 3]})
    print("✅ Pandas functionality: OK")
except Exception as e:
    print(f"❌ Pandas failed: {e}")

print("\n=== Verification Complete ===")
```

Run the verification:

```bash
python verify_dependencies.py
```

**Expected output:**
```
=== Dependency Verification ===
Python version: 3.11.x

✅ azure.ai.evaluation: 1.x.x
✅ azure.identity: 1.x.x
✅ azure.ai.projects: 1.x.x
✅ pyrit: 0.x.x
✅ pandas: 2.x.x
✅ matplotlib: 3.x.x
✅ dotenv: 1.x.x

🎉 All dependencies installed successfully!

=== Functionality Tests ===
✅ RedTeam import: OK
✅ Azure credentials: OK
✅ Pandas functionality: OK

=== Verification Complete ===
```

## Step 5: Create Requirements File

Save your dependencies for future use:

```bash
pip freeze > requirements.txt
```

This creates a `requirements.txt` file that others can use to install the same dependencies:

```bash
pip install -r requirements.txt
```

## Step 6: Test PyRIT Import

Create a simple test to ensure PyRIT is properly installed:

**test_pyrit.py**
```python
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Test PyRIT imports
try:
    from azure.ai.evaluation.red_team import RedTeam, RiskCategory, AttackStrategy
    print("✅ Successfully imported RedTeam classes")
    
    # Test enum values
    print("Available Risk Categories:")
    for category in RiskCategory:
        print(f"  - {category.value}")
    
    print("\nSample Attack Strategies:")
    strategies = [AttackStrategy.BASE64, AttackStrategy.FLIP, AttackStrategy.MORSE]
    for strategy in strategies:
        print(f"  - {strategy.value}")
        
except ImportError as e:
    print(f"❌ Failed to import PyRIT components: {e}")

# Test Azure integration
try:
    azure_ai_project = {
        "subscription_id": os.environ.get("AZURE_SUBSCRIPTION_ID"),
        "resource_group_name": os.environ.get("AZURE_RESOURCE_GROUP"),
        "project_name": os.environ.get("AZURE_PROJECT_NAME"),
    }
    
    if all(azure_ai_project.values()):
        print("✅ Azure project configuration loaded")
        print(f"   Subscription: {azure_ai_project['subscription_id'][:8]}...")
        print(f"   Resource Group: {azure_ai_project['resource_group_name']}")
        print(f"   Project: {azure_ai_project['project_name']}")
    else:
        print("⚠️ Azure project configuration incomplete")
        
except Exception as e:
    print(f"❌ Azure configuration error: {e}")
```

Run the test:

```bash
python test_pyrit.py
```

**Expected output:**
```
✅ Successfully imported RedTeam classes
Available Risk Categories:
  - Violence
  - HateUnfairness
  - Sexual
  - SelfHarm

Sample Attack Strategies:
  - Base64
  - Flip
  - Morse

✅ Azure project configuration loaded
   Subscription: 12345678...
   Resource Group: my-resource-group
   Project: my-ai-project
```

## Troubleshooting Common Issues

### Issue: "Failed to build pyrit"
**Symptoms**: Installation fails with compilation errors
**Solutions**:
1. Update pip: `pip install --upgrade pip`
2. Install build tools:
   - Windows: Install Visual Studio Build Tools
   - macOS: Install Xcode command line tools: `xcode-select --install`
   - Linux: Install build essentials: `sudo apt install build-essential`

### Issue: "Azure authentication failed"
**Symptoms**: DefaultAzureCredential fails
**Solutions**:
1. Re-login to Azure: `az logout && az login`
2. Check subscription access: `az account show`
3. Verify permissions for AI Foundry

### Issue: "ModuleNotFoundError: No module named 'pyrit'"
**Symptoms**: PyRIT import fails despite installation
**Solutions**:
1. Verify virtual environment is activated
2. Reinstall with verbose output: `pip install -v "azure-ai-evaluation[redteam]"`
3. Check Python path: `python -c "import sys; print(sys.path)"`

### Issue: Version conflicts
**Symptoms**: Dependency version conflicts during installation
**Solutions**:
1. Create fresh virtual environment
2. Install packages one by one to identify conflicts
3. Use pip-tools for dependency resolution: `pip install pip-tools`

## Alternative Installation Methods

### Using Conda
If you prefer conda environments:

```bash
conda create -n ai-red-teaming python=3.11
conda activate ai-red-teaming
pip install "azure-ai-evaluation[redteam]" azure-identity azure-ai-projects
```

### Using Poetry
If you use Poetry for dependency management:

```bash
poetry init
poetry add "azure-ai-evaluation[redteam]" azure-identity azure-ai-projects
poetry install
```

## Development Environment Setup

### VS Code Extensions (Recommended)
Install these VS Code extensions for better development experience:

1. **Python** - Python language support
2. **Azure Account** - Azure integration
3. **Azure CLI Tools** - Azure CLI support
4. **Jupyter** - Notebook support
5. **Python Docstring Generator** - Documentation help

### Jupyter Notebook Setup
If you want to use Jupyter notebooks:

```bash
# Install Jupyter kernel for your virtual environment
python -m ipykernel install --user --name=ai-red-teaming --display-name="AI Red Teaming"

# Start Jupyter
jupyter notebook
```

---

## Checkpoint

Before proceeding, ensure you have:

- ✅ All required packages installed successfully
- ✅ PyRIT imports working correctly
- ✅ Azure authentication functioning
- ✅ Environment variables loaded properly
- ✅ Development environment configured

**All set?** Time to run your [First Red Team Scan](./03-first-red-team-scan.md)!

---

**Navigation:** [Previous](./01-environment-setup.md) | [Module Home](./README.md) | **Next:** [First Red Team Scan](./03-first-red-team-scan.md)