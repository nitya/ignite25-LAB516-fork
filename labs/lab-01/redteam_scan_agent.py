# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------

"""
AI Red Teaming Script for Azure AI Agents

This script demonstrates how to perform automated red teaming security testing
against an Azure AI Agent using the Azure AI Evaluation SDK. It tests the agent's
responses against various attack strategies to identify potential vulnerabilities.

The script follows these key stages:
1. Environment Setup - Load configuration and credentials
2. Agent Discovery - Locate and validate the target agent
3. Agent Callback Setup - Create an interface for the red team to interact with the agent
4. Red Team Scan - Execute automated adversarial testing
5. Results - Output findings for security analysis
"""

from typing import Optional, Dict, Any
import os
import time
import warnings
from pathlib import Path
from dotenv import load_dotenv

# Suppress SyntaxWarning from third-party dependencies
warnings.filterwarnings("ignore", category=SyntaxWarning)

# Azure imports for authentication and AI services
from azure.identity import DefaultAzureCredential
from azure.ai.evaluation.red_team import RedTeam, RiskCategory, AttackStrategy
from azure.ai.projects import AIProjectClient
from azure.ai.agents.models import ListSortOrder


# ============================================================================
# STAGE 1: ENVIRONMENT SETUP
# ============================================================================

def load_environment_configuration() -> Dict[str, Optional[str]]:
    """
    Load and validate environment variables required for the red teaming operation.
    
    This function:
    - Locates the .env file in the workspace root
    - Loads all environment variables
    - Extracts required Azure AI Project configuration
    - Returns a dictionary of configuration values
    
    Returns:
        Dict containing:
            - project_endpoint: Azure AI Project endpoint URL
            - agent_name: Name of the agent to test
            
    Raises:
        ValueError: If required environment variables are missing
    """
    # Load environment variables from .env file
    # The .env file is located at the root of the workspace (two levels up from this script)
    current_dir = Path(__file__).parent
    env_path = current_dir / "../../.env"
    load_dotenv(dotenv_path=env_path)
    
    # Extract Azure AI project parameters from environment
    config = {
        "project_endpoint": os.environ.get("AZURE_AI_PROJECT_ENDPOINT"),
        "agent_name": os.environ.get("AZURE_AI_AGENT_NAME"),
    }
    
    # Validate that essential configuration is present
    if not config["project_endpoint"]:
        raise ValueError("Please set the AZURE_AI_PROJECT_ENDPOINT environment variable.")
        
    if not config["agent_name"]:
        raise ValueError("Please set the AZURE_AI_AGENT_NAME environment variable.")
    
    return config


# ============================================================================
# STAGE 2: AGENT DISCOVERY & VALIDATION
# ============================================================================

def resolve_agent(project_client: AIProjectClient, agent_name: str) -> tuple:
    """
    Locate and retrieve the target agent for red team testing by name.
    
    This function searches through all available agents in the project
    to find one matching the specified name.
    
    Args:
        project_client: Authenticated Azure AI Project client
        agent_name: Name of the agent to find
        
    Returns:
        Tuple of (agent_object, agent_id, deployment_name)
        
    Raises:
        ValueError: If agent with the specified name cannot be found
    """
    print(f"Searching for agent by name: {agent_name}")
    
    # Search through all agents to find one with matching name
    agent_id = None
    for agent in project_client.agents.list_agents():
        if agent.name == agent_name:
            agent_id = agent.id
            print(f"✓ Found agent: {agent_name} (ID: {agent_id})")
            break
    
    # Validate that we found the agent
    if not agent_id:
        raise ValueError(f"Agent with name '{agent_name}' not found. Please check the agent name.")
    
    # Retrieve the full agent object
    agent = project_client.agents.get_agent(agent_id)
    
    # Extract the model deployment name from the agent configuration
    deployment_name = agent.model
    
    return agent, agent_id, deployment_name


# ============================================================================
# STAGE 3: AGENT INTERACTION CALLBACK
# ============================================================================

def create_agent_callback(project_client: AIProjectClient, agent_id: str, thread_id: str):
    """
    Create a callback function that allows the red team to interact with the agent.
    
    The red team scanner uses this callback to send adversarial prompts to the agent
    and receive responses. This function encapsulates the full conversation flow:
    1. Create a user message in the thread
    2. Start an agent run to process the message
    3. Poll until the agent completes processing
    4. Retrieve and return the agent's response
    
    Args:
        project_client: Authenticated Azure AI Project client
        agent_id: ID of the agent to test
        thread_id: Conversation thread ID for maintaining context
        
    Returns:
        Callable that takes a query string and returns the agent's response
    """
    def agent_callback(query: str) -> str:
        """
        Send a query to the agent and return its response.
        
        This inner function is called by the red team scanner for each
        adversarial test case.
        
        Args:
            query: The prompt/question to send to the agent
            
        Returns:
            The agent's text response or an error message
        """
        # Create a new message in the conversation thread
        message = project_client.agents.messages.create(
            thread_id=thread_id, 
            role="user", 
            content=query
        )
        
        # Initiate an agent run to process the message
        run = project_client.agents.runs.create(
            thread_id=thread_id, 
            agent_id=agent_id
        )

        # Poll the run status until completion
        # The agent may be queued, in progress, or requiring action
        while run.status in ["queued", "in_progress", "requires_action"]:
            time.sleep(1)  # Wait before checking status again
            run = project_client.agents.runs.get(
                thread_id=thread_id, 
                run_id=run.id
            )
            print(f"Run status: {run.status}")

        # Handle failure cases
        if run.status == "failed":
            print(f"Run error: {run.last_error}")
            return "Error: Agent run failed."
        
        # Retrieve the agent's response from the message list
        # Messages are ordered with most recent first
        messages = project_client.agents.messages.list(
            thread_id=thread_id, 
            order=ListSortOrder.DESCENDING
        )
        
        # Extract the text content from the latest message
        for msg in messages:
            if msg.text_messages:
                return msg.text_messages[0].text.value
                
        return "Could not get a response from the agent."
    
    return agent_callback


# ============================================================================
# STAGE 4: RED TEAM CONFIGURATION & EXECUTION
# ============================================================================

def configure_red_team(project_endpoint: str, credential: DefaultAzureCredential) -> RedTeam:
    """
    Configure the red team scanner with security testing parameters.
    
    The red team scanner is configured with:
    - Risk categories to test (e.g., Violence, Hate Speech, etc.)
    - Number of test objectives to generate
    - Output directory for detailed results
    
    Args:
        project_endpoint: Azure AI Project endpoint URL
        credential: Authenticated Azure credential
        
    Returns:
        Configured RedTeam scanner instance
    """
    print("\nConfiguring Red Team scanner...")
    print("  - Risk Categories: Violence")
    print("  - Number of Objectives: 1")
    print("  - Output Directory: redteam_outputs/")
    
    red_team = RedTeam(
        azure_ai_project=project_endpoint,
        credential=credential,
        risk_categories=[RiskCategory.Violence],  # Categories of harmful content to test
        num_objectives=1,  # Number of test objectives to generate per category
        output_dir="redteam_outputs/"  # Where to save detailed results
    )
    
    return red_team


async def execute_red_team_scan(red_team: RedTeam, agent_callback: callable) -> Any:
    """
    Execute the red team security scan against the agent.
    
    This function runs the actual adversarial testing by:
    1. Generating adversarial prompts based on attack strategies
    2. Sending prompts to the agent via the callback
    3. Analyzing responses for vulnerabilities
    4. Generating a detailed report
    
    Args:
        red_team: Configured RedTeam scanner
        agent_callback: Function to interact with the target agent
        
    Returns:
        Scan results containing vulnerability findings and metrics
    """
    print("\n" + "="*70)
    print("STARTING RED TEAM SCAN")
    print("="*70)
    print("\nThe scanner will now:")
    print("  1. Generate adversarial test prompts")
    print("  2. Send prompts to the agent")
    print("  3. Analyze responses for vulnerabilities")
    print("  4. Generate a security report")
    print("\nThis may take several minutes...\n")
    
    result = await red_team.scan(
        target=agent_callback,  # The function to test
        scan_name="Agent-Scan",  # Name for this scan session
        attack_strategies=[AttackStrategy.Flip],  # Attack techniques to employ
    )
    
    print("\n" + "="*70)
    print("RED TEAM SCAN COMPLETE")
    print("="*70)
    print("\nResults have been saved to: redteam_outputs/")
    print("Review the output files for detailed vulnerability findings.\n")
    
    return result


# ============================================================================
# MAIN ORCHESTRATION FLOW
# ============================================================================

async def run_red_team():
    """
    Main orchestration function that executes the complete red teaming workflow.
    
    This function coordinates all stages of the red teaming process:
    
    STAGE 1: Load environment configuration and validate settings
    STAGE 2: Connect to Azure AI Project and locate target agent  
    STAGE 3: Set up communication channel with the agent
    STAGE 4: Configure and execute the red team security scan
    STAGE 5: Return results for analysis
    
    The function uses context managers to ensure proper resource cleanup
    and provides detailed console output to track progress.
    """
    print("\n" + "="*70)
    print("AI RED TEAMING - SECURITY TESTING FOR AZURE AI AGENTS")
    print("="*70 + "\n")
    
    # STAGE 1: Environment Setup
    print("STAGE 1: Loading Environment Configuration")
    print("-" * 70)
    config = load_environment_configuration()
    print("✓ Configuration loaded successfully\n")
    
    # Initialize Azure credentials using DefaultAzureCredential
    # This supports multiple authentication methods (CLI, Environment, Managed Identity, etc.)
    credential = DefaultAzureCredential(exclude_interactive_browser_credential=False)
    
    # Use context managers for proper resource management
    with credential:
        with AIProjectClient(
            endpoint=config["project_endpoint"], 
            credential=credential
        ) as project_client:
            
            # STAGE 2: Agent Discovery
            print("STAGE 2: Resolving Target Agent")
            print("-" * 70)
            agent, agent_id, deployment_name = resolve_agent(
                project_client, 
                config["agent_name"]
            )
            print(f"✓ Target Agent Located:")
            print(f"    Agent ID: {agent.id}")
            print(f"    Agent Name: {agent.name}")
            print(f"    Model Deployment: {deployment_name}\n")
            
            # STAGE 3: Communication Setup
            print("STAGE 3: Setting Up Agent Communication")
            print("-" * 70)
            # Create a conversation thread for agent interactions
            thread = project_client.agents.threads.create()
            print(f"✓ Conversation thread created: {thread.id}")
            
            # Create the callback function for red team to use
            agent_callback = create_agent_callback(project_client, agent.id, thread.id)
            print("✓ Agent callback configured\n")
            
            # STAGE 4: Red Team Scan
            print("STAGE 4: Executing Red Team Scan")
            print("-" * 70)
            red_team = configure_red_team(config["project_endpoint"], credential)
            result = await execute_red_team_scan(red_team, agent_callback)
            
            # STAGE 5: Completion
            print("STAGE 5: Scan Complete")
            print("-" * 70)
            print("✓ All stages completed successfully")
            print("✓ Review the output directory for detailed findings\n")
            
            return result


# ============================================================================
# SCRIPT ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    """
    Entry point for the script.
    
    This script must be run asynchronously since the red team scan is async.
    We use asyncio.run() to execute the main async function.
    """
    import asyncio
    asyncio.run(run_red_team())