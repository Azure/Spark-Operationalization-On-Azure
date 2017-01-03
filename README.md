# Private preview of Azure Machine Learning vNext

## Overview
The new version of Azure Machine Learning (ML) is powered by Spark, and leverages many of the high-scale Azure Services including HDInsight, Azure Container Service (ACS), and Azure Container Registry (ACR). You can do both real-time (RRS) and batch (BES) scoring scenarios using this new feature set.

## Private preview scope
The private preview of Azure ML vNext, uses a Data Science VM (DSVM) as the getting started environment. Using the Azure ML Command Line Interface (CLI), you can deploy Spark ML models and pipelines that you create in a Jupyter Notebook written in PySpark.

The web services can run locally on the DSVM or remotely on the ACS cluster for real-time or on the HDI cluster for batch scnarios. 

The DSVM deployment is meant for development and testing. ACS and HDI (i.e. remote) deployments are meant for high-scale, production scenarios.

To start using the Azure ML Private Preview, you must first provision a DSVM. The following steps will guide you through the process.

1. Sign in to the [Azure portal](https://portal.azure.com).
2. Click **New** and then type Linux Data Science Virtual Machine in the search box.
3. Select Linux Data Science Virtual Machine from the returned results.
4. Click Linux Data Science Virtual Machine [Staged] and then click **Create** to begin configuring and provisioning the virtual machine. 

When provisioning the DSVM, configure **Authentication type** as Password rather than SSH Public Key. Note: To successfully sign into the Jupyter hub, any alpha characters in the user name must be lower case. Using any upper case characters in the user ID will cause the sign in to the Jupyter hub to fail.

Once the DSVM is provisioned, note the IP address of the machine.

## For Real-time service (RRS)

When deploying RRS services, Azure ML uses Docker containers. The container then can be deploye locally to the DSVM or to an ACS cluster for high-scale production scenarios. 

The following are the steps to set up an RRS service (local or production).

### Provision ACR (required)

Run the following command to set up an Azure Container Registry (ACR) to host your web service's container:

    az acr create -name myRegistry -resource-group myResourceGroup -l southcentralus --storage-account-name myStorageAccount

For more information on managing Azure container  with the Azure CLI, see [az acr](https://docs.microsoft.com/en-us/cli/azure/acr).

### Open the sample Jupyter noteook

Jupyter is running on the DSVM at https://&lt;machine-ip-address&gt;:8000. Open Jupyter in a browser and sign in. The username and password are the those that you configured for the DSVM.  Note that you will recieve a certifiate warning that you can safely click through. 

The *realtimewebservices.ipynb* sample notebook is located in the azureml folder. 
   
Click the notebook to open it. Follow the instructions to create and deploy a model as a web service for real-time scoring.


