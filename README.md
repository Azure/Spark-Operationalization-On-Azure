 # Private preview of Azure Machine Learning vNext

## Overview

The new version of Azure Machine Learning (ML) is powered by Spark, and leverages many of the high-scale Azure Services including HDInsight, Azure Container Service (ACS), and Azure Container Registry (ACR). This new feature set supports both real-time (RRS) and batch (BES) scoring scenarios.

## Private preview scope

The private preview of Azure ML vNext, uses a Data Science VM (DSVM) as the getting started environment. Using the Azure ML Command Line Interface (CLI), you can deploy Spark ML models and pipelines that you create in a Jupyter Notebook written in PySpark.

The web services can run locally on the DSVM or remotely on the ACS cluster for real-time or on the HDI cluster for batch scenarios. 

## Set up the Azure Container Registry (ACR)

You must configure the Azure Container Registry (ACR) to host your web service's container. 

#### Provision your ACR 

If you have not already done so, install version 2.0 of the [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-az-cli2) on your local machine.

Once the Azure CLI is installed, open a command prompt and run the following command to set up the ACR:

    az acr create --name myRegistry --resource-group myResourceGroup -l southcentralus --storage-account-name myStorageAccount --admin-enabled true

After you have created the ACR, retrieve the ACR credentials. Save the user name and password as you will need them to deploy the web service. To retrieve the credentials, run the following command:

	az acr credential show -n myRegistry

For more information on managing Azure containers with the Azure CLI, see [az acr](https://docs.microsoft.com/en-us/cli/azure/acr).

The supplied Jupyter notebooks run the services on your DSVM. 

#### Sign in to the Jupyter server

Jupyter is running on the DSVM at https://&lt;machine-ip-address&gt;:8000. Open Jupyter in a browser and sign in. The user name and password are the those that you configured for the DSVM.  Note that you will receive a certificate warning that you can safely click through. 

The notebooks for the private preview scenarios are located in the **AzureML** folder.

## For Real-time service (RRS)

### Provision your ACS (Only for Production "cluster" scenario) 
To run the RRS service in a production scenario (not on the DSVM), you need to set up an ACS cluster. You don't need to run this if you will only want to run your web service on the DSVM. To setup the ACS cluster, run the following command:

<a href="https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Famlacstemplateresources.blob.core.windows.net%3A443%2Ftemplates%2Fproduction%2FAmlMesosTemplate.json" target="_blank"><img src="http://azuredeploy.net/deploybutton.png"/></a>

### Run the Notebook 
To run the RRS scenario, open the realtimewebservices.ipynb notebook and follow the provided instructions to train, save and deploy a model as a web service.

## For Batch service (BES)
To run a batch job in a production scenario (not on the DSVM), you need to set up an HDI cluster. To setup the HDI cluster, run the following command

... HDI provisioning command

To run the RRS scenario, open the batchwebservice.ipynb notebook and follow the provided instructions.
