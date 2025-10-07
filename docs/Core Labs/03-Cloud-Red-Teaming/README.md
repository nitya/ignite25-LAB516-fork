# Module 3: Cloud Red Teaming with Azure AI Foundry

**Duration:** 30 minutes  
**Type:** Hands-on Lab

Welcome to the cloud-based AI red teaming module! Here you'll learn to leverage Azure AI Foundry's full capabilities for enterprise-scale red teaming, including managing scans at scale, using the Azure portal for monitoring, and implementing cloud-based workflows.

## Module Structure

- [01 - Azure AI Foundry Setup](./01-azure-ai-foundry-setup.md) *(5 minutes)*
- [02 - Cloud Scan Configuration](./02-cloud-scan-configuration.md) *(10 minutes)*
- [03 - Running Cloud Scans](./03-running-cloud-scans.md) *(10 minutes)*
- [04 - Portal Monitoring and Management](./04-portal-monitoring.md) *(5 minutes)*

## Learning Objectives

After completing this module, you will be able to:

- Configure Azure AI Foundry projects for red teaming at scale
- Set up model deployments and connections for cloud scanning
- Execute comprehensive red teaming scans in the cloud
- Monitor and manage scans through the Azure portal
- Implement enterprise-grade red teaming workflows
- Compare local vs. cloud scanning approaches

## Prerequisites for This Module

Before starting, ensure you have:

- ✅ **Completed Module 2** (Local Red Teaming)
- ✅ **Azure AI Foundry project** created and accessible
- ✅ **Azure OpenAI or AI Services** connected to your project
- ✅ **Storage account** connected for evaluation results
- ✅ **Appropriate permissions** for project resources

## What You'll Build

By the end of this module, you'll have:

1. **Cloud Infrastructure**: Fully configured Azure AI Foundry environment
2. **Scalable Scans**: Cloud-based red teaming pipelines
3. **Enterprise Monitoring**: Portal-based result tracking and analysis
4. **Automated Workflows**: Scheduled and triggered security assessments

## Key Advantages of Cloud Red Teaming

### 🚀 Scale and Performance
- **Parallel Processing**: Run multiple scans simultaneously
- **Large Test Suites**: Handle hundreds of attack objectives
- **Resource Optimization**: Leverage Azure's compute power

### 🔐 Enterprise Security
- **Centralized Management**: Single pane of glass for all scans
- **Access Controls**: Role-based permissions and governance
- **Audit Trails**: Complete logging and compliance tracking

### 📊 Advanced Analytics
- **Historical Trends**: Track security posture over time
- **Comparative Analysis**: Benchmark across models and applications
- **Automated Reporting**: Generate compliance and security reports

### 🔄 Integration Capabilities
- **CI/CD Pipeline**: Integrate with DevOps workflows
- **API Access**: Programmatic scan management
- **Alerting**: Automatic notifications for security issues

## Cloud vs. Local Red Teaming Comparison

| Aspect | Local Red Teaming | Cloud Red Teaming |
|--------|-------------------|-------------------|
| **Setup Complexity** | Simple - install packages | Moderate - configure cloud resources |
| **Scale** | Limited by local resources | Unlimited cloud scale |
| **Performance** | Depends on local machine | High-performance cloud compute |
| **Collaboration** | Individual/team focused | Enterprise-wide sharing |
| **Monitoring** | Local files and scripts | Azure portal dashboards |
| **Integration** | Manual process | Automated CI/CD integration |
| **Cost** | Free (except Azure API calls) | Pay-per-use cloud resources |
| **Security** | Local data handling | Enterprise security controls |

## Important Notes

⚠️ **Azure AI Foundry Project Required**
Cloud red teaming requires an Azure AI Foundry project, not just a hub-based project. See the setup guide if you need to create or migrate.

⚠️ **Regional Availability**
AI Red Teaming Agent is currently available in:
- East US2
- Sweden Central  
- France Central
- Switzerland West

⚠️ **Resource Costs**
Cloud scans will consume Azure resources and may incur costs. We'll use cost-effective configurations, but monitor your usage.

⚠️ **Model Deployments**
You'll need Azure OpenAI model deployments accessible to your Azure AI Foundry project.

## Getting Started

Ready to scale up to the cloud? Let's begin with [Azure AI Foundry Setup](./01-azure-ai-foundry-setup.md).

---

**Navigation:** [Workshop Home](../../README.md) | [Previous Module](../02-local-red-teaming/README.md) | **Next:** [Azure AI Foundry Setup](./01-azure-ai-foundry-setup.md)