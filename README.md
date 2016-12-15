# Azure Machine Learning vNext

The new version of Azure Machine Learning (ML) is powered by Spark, and leverages many of the high-scale Azure Services including HDInsight, Azure Container Service (ACS), and Azure Container Registry (ACR).

## Private preview
The private preview of Azure ML vNext, uses the Data Science VM (DS VM) as the getting started environment. Using the Azure ML Command Line Interface (CLI), you can deploy Spark ML models and pipelines that you create in a Jupyter Notebook written in PySpark.

Using Docker Container, you can deploy these models as Real-time or Batch web services. The web services can run locally on the DS VM or remotely on the ACS cluster for real-time or on the HDI cluster for batch scnarios. 

The DS VM deployment is meant for development and testing. ACS and HDI (i.e. remote) deployments are meant for high-scale, production scenarios.

The following are the steps to start using Azure ML Private Preview.
6. Click **Create** to begin configuring and provisioning the virtual machine. Q: Are there any guidelines we should give them for the configuration?

Do they need to log on do any additional configuration at this point?

#### 1.1 Install the CLI

    pip install azuremlcli –extra-index-url https://pypi-amlbd.southcentralus.cloudapp.azure.com/simple --trusted-host https://pypi-amlbd.southcentralus.cloudapp.azure.com

### 2. Set up the environment

Install version 2.0 of the [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-az-cli2).

#### 2.1 Provision ACR (required)

    az acr create -name myRegistry -resource-group myResourceGroup -l southcentralus --storage-account-name myStorageAccount

For more information on managing Azure container  with the Azure CLI, see [az acr](https://docs.microsoft.com/en-us/cli/azure/acr).

#### 2.2 Provision ACS (optional for production deployment scenario)

  az group deployment create -g mygroup --template-uri https://myresource/azuredeploy.json --parameters @myparameters.json

For more information on deploying Azure container service templates with the Azure CLI, see [az group deployment](https://docs.microsoft.com/en-us/cli/azure/group/deployment).

#### 2.3 Provision HDI Spark (optional for production deployment scenario)

### 3. Open Sample Jupyter Noteook

Start Jupyter Notebook on the DS VM. Then open the AML Sample Notebook.
--- where?
Follow the instructions to create and deploy a model as a web service for real-time or batch scoring.
