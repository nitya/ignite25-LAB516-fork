# LAB 516 Setup: Red Teaming

## 1. Infrastructure Setup

This project uses the [get-started-with-ai-agents](https://github.com/Azure-Samples/get-started-with-ai-agents) template to provision infrastructure for this project.

For simplicity, all steps are coded in `scripts/` that you can just run at command line to get things done.


### 1.1. Authenticate with Azure

Run this command from root of repo:

```bash
./scripts/setup-auth
```

### 1.2. Setup Template

Run this command from the root of repo:

```bash
./scripts/setup-azd
```

#### **Recommendation**: 
Once the `.azure/MSIGNITE25-LAB516/.env` is created, specify `AZURE_LOCATION="swedencentral"` proactively to have it pick up that location. This may not always show as an option if run using default `azd up`

#### **Execution**: 

Once the setup is complete, you can deploy:

```bash
cd .azd
azd up
```


### 1.3. Teardown Template

Run this command from the root of repo:

```bash
./scripts/teardown-azd
```

---

## 2. Red Teaming Test

