# Module 2: Local Red Teaming with PyRIT

**Duration:** 30 minutes  
**Type:** Hands-on Lab

Welcome to the hands-on portion of our workshop! In this module, you'll set up and run AI red teaming scans locally using Microsoft's PyRIT framework and Azure AI Evaluation SDK.

## Module Structure

- [01 - Environment Setup](./01-environment-setup.md) *(5 minutes)*
- [02 - Installing Dependencies](./02-installing-dependencies.md) *(5 minutes)*
- [03 - Your First Red Team Scan](./03-first-red-team-scan.md) *(10 minutes)*
- [04 - Understanding Results](./04-understanding-results.md) *(5 minutes)*
- [05 - Advanced Scanning Techniques](./05-advanced-scanning.md) *(5 minutes)*

## Learning Objectives

After completing this module, you will be able to:

- Set up a development environment for AI red teaming
- Install and configure PyRIT and Azure AI Evaluation SDK
- Create and execute basic red teaming scans locally
- Understand and interpret Attack Success Rate (ASR) metrics
- Customize scans with different risk categories and attack strategies
- Export and analyze red teaming results

## Prerequisites for This Module

Before starting, ensure you have:

- ✅ **Python 3.10, 3.11, or 3.12** installed (check with `python --version`)
- ✅ **Azure subscription** with access to Azure AI Foundry
- ✅ **Azure CLI** installed and authenticated (`az login`)
- ✅ **Git** for cloning repositories
- ✅ **Text editor or IDE** (VS Code recommended)

## What You'll Build

By the end of this module, you'll have:

1. **Working Environment**: Fully configured local setup for AI red teaming
2. **Basic Scanner**: Python script that runs red teaming scans
3. **Results Dashboard**: Understanding of how to interpret scan results
4. **Custom Configurations**: Ability to modify scans for your specific needs

## Key Concepts Covered

### Technical Skills
- Python environment management
- Azure authentication and configuration
- PyRIT framework usage
- Result analysis and visualization

### AI Safety Skills
- Practical application of red teaming concepts
- Hands-on experience with attack strategies
- Real-world result interpretation
- Safety threshold determination

## Lab Environment Options

### Option 1: Local Machine
- Install everything on your local development machine
- Full control over environment configuration
- Persistent setup for future use

### Option 2: GitHub Codespaces
- Cloud-based development environment
- Pre-configured with necessary tools
- No local installation required

### Option 3: Azure VM
- Dedicated cloud environment
- Scalable compute resources
- Isolated from personal machine

## Important Notes

⚠️ **Python Version Compatibility**
PyRIT requires Python 3.10, 3.11, or 3.12. It does NOT support Python 3.9.

⚠️ **Azure Resources**
Some exercises will create Azure resources that may incur costs. We'll use the smallest/cheapest options available.

⚠️ **Safety Considerations**
Red teaming involves testing with potentially harmful content. Always follow responsible disclosure practices.

## Getting Started

Ready to set up your environment? Let's begin with [Environment Setup](./01-environment-setup.md).

---

**Navigation:** [Workshop Home](../../README.md) | [Previous Module](../01-intro/README.md) | **Next:** [Environment Setup](./01-environment-setup.md)