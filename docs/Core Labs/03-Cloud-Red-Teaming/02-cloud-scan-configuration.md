# 02 - Cloud Scan Configuration

**Duration:** 10 minutes  
**Type:** Hands-on Lab

With your Azure AI Foundry environment set up, let's configure and run cloud-based red teaming scans. Cloud scans offer more power and scalability than local scans.

## Step 1: Basic Cloud Scan Configuration

Let's start with a simple cloud scan to test your setup:

**basic_cloud_scan.py**
```python
import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    RedTeam,
    AzureOpenAIModelConfiguration,
    AttackStrategy,
    RiskCategory,
)

load_dotenv()

def basic_cloud_scan():
    """Run a basic red teaming scan in the cloud."""
    
    print("=== Basic Cloud Red Team Scan ===")
    
    # Configuration
    endpoint = os.environ.get("PROJECT_ENDPOINT")
    model_deployment = os.environ.get("MODEL_DEPLOYMENT_NAME")
    
    if not endpoint or not model_deployment:
        print("❌ Missing configuration. Check PROJECT_ENDPOINT and MODEL_DEPLOYMENT_NAME")
        return
    
    try:
        # Create Azure AI Projects client
        client = AIProjectClient(
            endpoint=endpoint,
            credential=DefaultAzureCredential(exclude_interactive_browser_credential=False),
        )
        
        # Create target configuration
        target_config = AzureOpenAIModelConfiguration(
            model_deployment_name=model_deployment
        )
        
        # Create red team configuration
        red_team_config = RedTeam(
            attack_strategies=[AttackStrategy.BASE64],
            risk_categories=[RiskCategory.VIOLENCE],
            display_name="basic-cloud-scan",
            target=target_config,
        )
        
        print("✅ Configuration created successfully")
        print(f"   Target: {model_deployment}")
        print(f"   Risk Categories: Violence")
        print(f"   Attack Strategies: Base64")
        
        # Determine headers based on deployment type
        if "/" in model_deployment:
            # External connection format: connectionName/deploymentName
            headers = {}  # No additional headers needed for connected resources
            print("   Connection Type: External Azure OpenAI connection")
        else:
            # Project deployment - need endpoint and key
            model_endpoint = os.environ.get("MODEL_ENDPOINT")
            model_api_key = os.environ.get("MODEL_API_KEY")
            
            if model_endpoint and model_api_key:
                headers = {
                    "model-endpoint": model_endpoint,
                    "api-key": model_api_key
                }
                print("   Connection Type: Project deployment with credentials")
            else:
                headers = {}
                print("   Connection Type: Project deployment with managed identity")
        
        # Start the red team scan
        print("\n🚀 Starting cloud red team scan...")
        print("   This may take 2-3 minutes...")
        
        response = client.red_teams.create(red_team=red_team_config, headers=headers)
        
        print("✅ Red team scan started successfully!")
        print(f"📊 Scan ID: {response.name}")
        print(f"🔍 Status: {response.status}")
        
        return response.name
        
    except Exception as e:
        print(f"❌ Error starting cloud scan: {e}")
        print("\n🔧 Common issues:")
        print("   - Check model deployment accessibility")
        print("   - Verify storage account permissions")
        print("   - Ensure project is in supported region")
        return None

if __name__ == "__main__":
    scan_id = basic_cloud_scan()
    if scan_id:
        print(f"\n💡 Use scan ID '{scan_id}' to check status and get results")
```

Run the basic cloud scan:

```bash
python basic_cloud_scan.py
```

## Step 2: Monitor Scan Progress

Create a script to monitor your scan progress:

**monitor_scan.py**
```python
import os
import time
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

load_dotenv()

def monitor_scan(scan_id=None):
    """Monitor the progress of a red team scan."""
    
    endpoint = os.environ.get("PROJECT_ENDPOINT")
    
    if not endpoint:
        print("❌ PROJECT_ENDPOINT not configured")
        return
    
    try:
        client = AIProjectClient(
            endpoint=endpoint,
            credential=DefaultAzureCredential(exclude_interactive_browser_credential=False),
        )
        
        if scan_id:
            # Monitor specific scan
            print(f"🔍 Monitoring scan: {scan_id}")
            
            while True:
                response = client.red_teams.get(name=scan_id)
                status = response.status
                
                print(f"   Status: {status}")
                
                if status in ["Completed", "Failed", "Cancelled"]:
                    print(f"✅ Scan {status.lower()}!")
                    
                    if status == "Completed":
                        print("🎉 Results are ready for analysis!")
                    elif status == "Failed":
                        print("❌ Scan failed. Check logs for details.")
                    
                    break
                
                print("   ⏳ Waiting 30 seconds before next check...")
                time.sleep(30)
        else:
            # List all scans
            print("📋 All Red Team Scans:")
            
            scans = list(client.red_teams.list())
            
            if not scans:
                print("   No scans found")
                return
            
            for scan in scans:
                print(f"   {scan.name}: {scan.status}")
            
            # Get latest scan for monitoring
            latest_scan = scans[0] if scans else None
            if latest_scan:
                print(f"\n🔍 Latest scan: {latest_scan.name}")
                monitor_scan(latest_scan.name)
                
    except Exception as e:
        print(f"❌ Error monitoring scan: {e}")

if __name__ == "__main__":
    import sys
    scan_id = sys.argv[1] if len(sys.argv) > 1 else None
    monitor_scan(scan_id)
```

Monitor your scan:

```bash
# Monitor specific scan
python monitor_scan.py your-scan-id

# Or list all scans and monitor latest
python monitor_scan.py
```

## Step 3: Comprehensive Cloud Scan

Now let's create a more comprehensive scan with multiple risk categories and attack strategies:

**comprehensive_cloud_scan.py**
```python
import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    RedTeam,
    AzureOpenAIModelConfiguration,
    AttackStrategy,
    RiskCategory,
)

load_dotenv()

def comprehensive_cloud_scan():
    """Run a comprehensive red teaming scan in the cloud."""
    
    print("=== Comprehensive Cloud Red Team Scan ===")
    
    endpoint = os.environ.get("PROJECT_ENDPOINT")
    model_deployment = os.environ.get("MODEL_DEPLOYMENT_NAME")
    
    try:
        client = AIProjectClient(
            endpoint=endpoint,
            credential=DefaultAzureCredential(exclude_interactive_browser_credential=False),
        )
        
        # Create comprehensive target configuration
        target_config = AzureOpenAIModelConfiguration(
            model_deployment_name=model_deployment
        )
        
        # Create comprehensive red team configuration
        red_team_config = RedTeam(
            attack_strategies=[
                # Easy complexity attacks
                AttackStrategy.BASE64,
                AttackStrategy.FLIP,
                AttackStrategy.MORSE,
                AttackStrategy.ROT13,
                AttackStrategy.LEETSPEAK,
                
                # Moderate complexity
                AttackStrategy.TENSE,
                
                # Note: Difficult attacks (compositions) might need special handling
            ],
            risk_categories=[
                RiskCategory.VIOLENCE,
                RiskCategory.HATE_UNFAIRNESS,
                RiskCategory.SEXUAL,
                RiskCategory.SELF_HARM
            ],
            display_name="comprehensive-security-assessment",
            target=target_config,
        )
        
        print("✅ Comprehensive configuration created")
        print(f"   Target: {model_deployment}")
        print(f"   Risk Categories: 4 (Violence, Hate/Unfairness, Sexual, Self-Harm)")
        print(f"   Attack Strategies: 6 techniques")
        print("   Expected Duration: 5-10 minutes")
        
        # Determine headers
        headers = {}
        if "/" not in model_deployment:
            model_endpoint = os.environ.get("MODEL_ENDPOINT")
            model_api_key = os.environ.get("MODEL_API_KEY")
            if model_endpoint and model_api_key:
                headers = {
                    "model-endpoint": model_endpoint,
                    "api-key": model_api_key
                }
        
        # Start comprehensive scan
        print("\n🚀 Starting comprehensive cloud red team scan...")
        
        response = client.red_teams.create(red_team=red_team_config, headers=headers)
        
        print("✅ Comprehensive scan started!")
        print(f"📊 Scan ID: {response.name}")
        print(f"🔍 Initial Status: {response.status}")
        
        # Auto-monitor this scan
        print("\n⏳ Auto-monitoring scan progress...")
        monitor_comprehensive_scan(client, response.name)
        
        return response.name
        
    except Exception as e:
        print(f"❌ Error starting comprehensive scan: {e}")
        return None

def monitor_comprehensive_scan(client, scan_id):
    """Monitor comprehensive scan with detailed progress updates."""
    
    import time
    
    start_time = time.time()
    
    while True:
        try:
            response = client.red_teams.get(name=scan_id)
            status = response.status
            elapsed = time.time() - start_time
            
            print(f"   [{elapsed:.0f}s] Status: {status}")
            
            if status in ["Completed", "Failed", "Cancelled"]:
                if status == "Completed":
                    print(f"\n🎉 Comprehensive scan completed in {elapsed:.0f} seconds!")
                    print("📊 Results are ready for analysis in Azure AI Foundry portal")
                elif status == "Failed":
                    print(f"\n❌ Scan failed after {elapsed:.0f} seconds")
                
                break
            
            time.sleep(30)  # Check every 30 seconds
            
        except KeyboardInterrupt:
            print(f"\n⏹️ Monitoring stopped. Scan continues running...")
            print(f"   Use scan ID '{scan_id}' to check status later")
            break
        except Exception as e:
            print(f"❌ Error during monitoring: {e}")
            break

if __name__ == "__main__":
    comprehensive_cloud_scan()
```

Run the comprehensive scan:

```bash
python comprehensive_cloud_scan.py
```

## Step 4: Custom Cloud Scan Configuration

Create a customizable scan configuration:

**custom_cloud_scan.py**
```python
import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    RedTeam,
    AzureOpenAIModelConfiguration,
    AttackStrategy,
    RiskCategory,
)

load_dotenv()

def custom_cloud_scan(
    scan_name="custom-red-team-scan",
    risk_categories=None,
    attack_strategies=None,
    model_deployment=None
):
    """Run a customizable red teaming scan in the cloud."""
    
    print(f"=== Custom Cloud Red Team Scan: {scan_name} ===")
    
    # Default configurations
    if risk_categories is None:
        risk_categories = [RiskCategory.VIOLENCE, RiskCategory.HATE_UNFAIRNESS]
    
    if attack_strategies is None:
        attack_strategies = [AttackStrategy.BASE64, AttackStrategy.FLIP]
    
    if model_deployment is None:
        model_deployment = os.environ.get("MODEL_DEPLOYMENT_NAME")
    
    endpoint = os.environ.get("PROJECT_ENDPOINT")
    
    try:
        client = AIProjectClient(
            endpoint=endpoint,
            credential=DefaultAzureCredential(exclude_interactive_browser_credential=False),
        )
        
        target_config = AzureOpenAIModelConfiguration(
            model_deployment_name=model_deployment
        )
        
        red_team_config = RedTeam(
            attack_strategies=attack_strategies,
            risk_categories=risk_categories,
            display_name=scan_name,
            target=target_config,
        )
        
        print("✅ Custom configuration created")
        print(f"   Scan Name: {scan_name}")
        print(f"   Target Model: {model_deployment}")
        print(f"   Risk Categories: {[cat.value for cat in risk_categories]}")
        print(f"   Attack Strategies: {[strat.value for strat in attack_strategies]}")
        
        # Headers configuration
        headers = {}
        if "/" not in model_deployment:
            model_endpoint = os.environ.get("MODEL_ENDPOINT")
            model_api_key = os.environ.get("MODEL_API_KEY")
            if model_endpoint and model_api_key:
                headers = {
                    "model-endpoint": model_endpoint,
                    "api-key": model_api_key
                }
        
        print(f"\n🚀 Starting custom scan...")
        
        response = client.red_teams.create(red_team=red_team_config, headers=headers)
        
        print("✅ Custom scan started!")
        print(f"📊 Scan ID: {response.name}")
        
        return response.name
        
    except Exception as e:
        print(f"❌ Error starting custom scan: {e}")
        return None

def predefined_scan_configurations():
    """Run several predefined scan configurations for comprehensive testing."""
    
    print("=== Running Predefined Scan Suite ===")
    
    scan_configs = [
        {
            "scan_name": "violence-focus-scan",
            "risk_categories": [RiskCategory.VIOLENCE],
            "attack_strategies": [
                AttackStrategy.BASE64,
                AttackStrategy.FLIP,
                AttackStrategy.MORSE,
                AttackStrategy.TENSE
            ]
        },
        {
            "scan_name": "encoding-attacks-scan", 
            "risk_categories": [RiskCategory.VIOLENCE, RiskCategory.HATE_UNFAIRNESS],
            "attack_strategies": [
                AttackStrategy.BASE64,
                AttackStrategy.ROT13,
                AttackStrategy.LEETSPEAK,
                AttackStrategy.UNICODE_CONFUSABLE
            ]
        },
        {
            "scan_name": "comprehensive-safety-scan",
            "risk_categories": [
                RiskCategory.VIOLENCE,
                RiskCategory.HATE_UNFAIRNESS,
                RiskCategory.SEXUAL,
                RiskCategory.SELF_HARM
            ],
            "attack_strategies": [
                AttackStrategy.BASE64,
                AttackStrategy.FLIP,
                AttackStrategy.TENSE
            ]
        }
    ]
    
    scan_ids = []
    
    for config in scan_configs:
        print(f"\n--- Starting {config['scan_name']} ---")
        scan_id = custom_cloud_scan(**config)
        if scan_id:
            scan_ids.append((config['scan_name'], scan_id))
        
        # Brief pause between scans
        import time
        time.sleep(5)
    
    print(f"\n📋 Started {len(scan_ids)} scans:")
    for name, scan_id in scan_ids:
        print(f"   {name}: {scan_id}")
    
    return scan_ids

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "suite":
        # Run predefined suite
        predefined_scan_configurations()
    else:
        # Run single custom scan
        custom_cloud_scan()
```

Run custom scans:

```bash
# Single custom scan
python custom_cloud_scan.py

# Predefined scan suite
python custom_cloud_scan.py suite
```

## Step 5: Scan Management Utilities

Create utilities for managing multiple scans:

**scan_manager.py**
```python
import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

load_dotenv()

def list_all_scans():
    """List all red team scans with status."""
    
    endpoint = os.environ.get("PROJECT_ENDPOINT")
    
    try:
        client = AIProjectClient(
            endpoint=endpoint,
            credential=DefaultAzureCredential(exclude_interactive_browser_credential=False),
        )
        
        print("=== All Red Team Scans ===")
        
        scans = list(client.red_teams.list())
        
        if not scans:
            print("No scans found.")
            return []
        
        print(f"Found {len(scans)} scan(s):")
        print()
        
        for i, scan in enumerate(scans, 1):
            print(f"{i}. Name: {scan.name}")
            print(f"   Status: {scan.status}")
            if hasattr(scan, 'created_at') and scan.created_at:
                print(f"   Created: {scan.created_at}")
            print()
        
        return scans
        
    except Exception as e:
        print(f"❌ Error listing scans: {e}")
        return []

def get_scan_details(scan_id):
    """Get detailed information about a specific scan."""
    
    endpoint = os.environ.get("PROJECT_ENDPOINT")
    
    try:
        client = AIProjectClient(
            endpoint=endpoint,
            credential=DefaultAzureCredential(exclude_interactive_browser_credential=False),
        )
        
        print(f"=== Scan Details: {scan_id} ===")
        
        scan = client.red_teams.get(name=scan_id)
        
        print(f"Name: {scan.name}")
        print(f"Status: {scan.status}")
        
        if hasattr(scan, 'display_name') and scan.display_name:
            print(f"Display Name: {scan.display_name}")
            
        if hasattr(scan, 'created_at') and scan.created_at:
            print(f"Created: {scan.created_at}")
            
        if hasattr(scan, 'target') and scan.target:
            print(f"Target: {scan.target}")
        
        return scan
        
    except Exception as e:
        print(f"❌ Error getting scan details: {e}")
        return None

def cleanup_completed_scans(keep_recent=5):
    """Clean up old completed scans, keeping the most recent ones."""
    
    print(f"=== Cleanup: Keeping {keep_recent} most recent completed scans ===")
    
    endpoint = os.environ.get("PROJECT_ENDPOINT")
    
    try:
        client = AIProjectClient(
            endpoint=endpoint,
            credential=DefaultAzureCredential(exclude_interactive_browser_credential=False),
        )
        
        scans = list(client.red_teams.list())
        
        # Filter completed scans
        completed_scans = [s for s in scans if s.status == "Completed"]
        
        if len(completed_scans) <= keep_recent:
            print(f"Only {len(completed_scans)} completed scans found. No cleanup needed.")
            return
        
        # Sort by creation time (if available) or name
        try:
            completed_scans.sort(key=lambda x: x.created_at or x.name, reverse=True)
        except:
            completed_scans.sort(key=lambda x: x.name, reverse=True)
        
        scans_to_delete = completed_scans[keep_recent:]
        
        print(f"Found {len(completed_scans)} completed scans.")
        print(f"Will delete {len(scans_to_delete)} old scans:")
        
        for scan in scans_to_delete:
            print(f"  - {scan.name}")
        
        confirm = input("\nProceed with deletion? (yes/no): ")
        
        if confirm.lower() == 'yes':
            for scan in scans_to_delete:
                try:
                    # Note: Actual deletion API might vary
                    print(f"   Deleting {scan.name}...")
                    # client.red_teams.delete(name=scan.name)  # API may not support deletion
                    print(f"   Note: Check Azure portal for manual cleanup of {scan.name}")
                except Exception as e:
                    print(f"   ❌ Failed to delete {scan.name}: {e}")
        else:
            print("Cleanup cancelled.")
            
    except Exception as e:
        print(f"❌ Error during cleanup: {e}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "list":
            list_all_scans()
        elif command == "details" and len(sys.argv) > 2:
            get_scan_details(sys.argv[2])
        elif command == "cleanup":
            cleanup_completed_scans()
        else:
            print("Usage: python scan_manager.py [list|details <scan_id>|cleanup]")
    else:
        list_all_scans()
```

Use the scan manager:

```bash
# List all scans
python scan_manager.py list

# Get details for specific scan
python scan_manager.py details your-scan-id

# Cleanup old completed scans
python scan_manager.py cleanup
```

---

## Step 6: Configuration Best Practices

### Resource Optimization
- Start with smaller scans to test configuration
- Use fewer attack objectives for faster results
- Monitor costs and adjust based on usage

### Security Considerations
- Use managed identities when possible
- Regularly rotate API keys if using them
- Monitor scan results for sensitive information

### Performance Tips
- Run scans during off-peak hours for better performance
- Use appropriate model deployments (faster models for testing)
- Consider parallel scans for different risk categories

---

## Checkpoint

Before proceeding, ensure you have:

- ✅ Successfully run basic cloud scan
- ✅ Monitored scan progress programmatically
- ✅ Executed comprehensive multi-category scan
- ✅ Created custom scan configurations
- ✅ Used scan management utilities

**Ready to run and monitor scans?** Let's move on to [Running Cloud Scans](./03-running-cloud-scans.md)!

---

**Navigation:** [Previous](./01-azure-ai-foundry-setup.md) | [Module Home](./README.md) | **Next:** [Running Cloud Scans](./03-running-cloud-scans.md)