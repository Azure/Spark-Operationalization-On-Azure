# Azure Machine Learning vNext

The new version of Azure Machine Learning (ML) is powered by Spark, and leverages many of the high-scale Azure Services including HDInsight, Azure Container Service (ACS), and Azure Container Registry (ACR).

## Private preview
The private preview of Azure ML vNext, uses the Data Science VM (DS VM) as the getting started environment. Using the Azure ML Command Line Interface (CLI), you can deploy Spark ML models and pipelines that you create in a Jupyter Notebook written in PySpark.

Using Docker Container, you can deploy these models as Real-time or Batch web services. The web services can run locally on the DS VM or remotely on the ACS cluster for real-time or on the HDI cluster for batch scnarios. 

The DS VM deployment is meant for development and testing. ACS and HDI (i.e. remote) deployments are meant for high-scale, production scenarios.

The following are the steps to start using Azure ML Private Preview.

### 1. Provision Data Science VM
Provision the Linux Data Science VM. Using this VM, you can deploy a model or pipeline as a web service and call the web service for testing.

1. Sign into the [Azure portal](https://portal.azure.com).
2. Click **New**.
3. Search for "Linux Data Science Virtual Machine".
4. Click Linux Data Data Science Virtual Machine from the returned results dropdown.
5. Click Linux Data Data Science Virtual Machine.
6. Click **Create** to begin configuring and provisioning the virtual machine. Q: Are there any guidelines we should give them for the configuration?

Do they need to log on do any additional configuration at this point?

#### 1.1 Install the Azure ML CLI

Do they need to install the Azure CLI first?

* from where
  * what is the command

### 2. Set up the environment

#### 2.1 Provision ACR (required)

az acr create -name myRegistry -resource-group myResourceGroup -l southcentralus --storage-account-name myStorageAccount

For more information on managing Azure container  with the Azure CLI, see [az acr](https://docs.microsoft.com/en-us/cli/azure/acr).

#### 2.2 Provision ACS (optional for production deployment scenario)

az acs create -name myCluster -resource-group myResourceGroup

For more information on managing Azure container services with the Azure CLI, see [az acs](https://docs.microsoft.com/en-us/cli/azure/acs).

#### 2.3 Provision HDI Spark (optional for production deployment scenario)

### 3. Open Sample Jupyter Noteook
Start Jupyter Notebook on the DS VM. Then open the AML Sample Notebook.
--- where?
Follow the instructions to create and deploy a model as a web service for real-time or batch scoring.
