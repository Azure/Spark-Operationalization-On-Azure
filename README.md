# Private preview of Azure Machine Learning vNext

## Overview
The new version of Azure Machine Learning (ML) is powered by Spark, and leverages many of the high-scale Azure Services including HDInsight, Azure Container Service (ACS), and Azure Container Registry (ACR). You can do both real-time (RRS) and batch (BES) scoring scenarios using this new feature set.

## Private preview scope
The private preview of Azure ML vNext, uses a Data Science VM (DSVM) as the getting started environment. Using the Azure ML Command Line Interface (CLI), you can deploy Spark ML models and pipelines that you create in a Jupyter Notebook written in PySpark.

The web services can run locally on the DSVM or remotely on the ACS cluster for real-time or on the HDI cluster for batch scnarios. 

The DSVM deployment is meant for development and testing. ACS and HDI (i.e. remote) deployments are meant for high-scale, production scenarios.

## Provision DSVM

To start using the Azure ML Private Preview, you must first provision a DSVM. The following steps will guide you through the process.

1. Sign in to the [Azure portal](https://portal.azure.com).
2. Click **New** and then type Linux Data Science Virtual Machine in the search box.
3. Select Linux Data Science Virtual Machine from the returned results.
4. Click Linux Data Science Virtual Machine [Staged] and then click **Create** to begin configuring and provisioning the virtual machine. 

When provisioning the DSVM, configure **Authentication type** as Password rather than SSH Public Key. Note: To successfully sign into the Jupyter hub, any alpha characters in the user name must be lower case. Using any upper case characters in the user ID will cause the sign in to the Jupyter hub to fail.

Once the DSVM is provisioned, note the IP address of the machine.
## Set up DSVM
connect to the DSVM machine configure it.

### X2GO stuff

#### Provision ACR (required)

Run the following command to set up an Azure Container Registry (ACR) to host your web service's container:

    az acr create -name myRegistry -resource-group myResourceGroup -l southcentralus --storage-account-name myStorageAccount

For more information on managing Azure container  with the Azure CLI, see [az acr](https://docs.microsoft.com/en-us/cli/azure/acr).

#### Login to Jupyter server
Instructions how to connect to the jupyter hub....
Includes log in...
Need log in instrucitons...
Click AzureML.

## For Real-time service (RRS)
To run the RRS service in the production scenario (not on DSVM), you need to set up an ACS cluster. The command is below:

...ACS provisioning command

Open the notebook from here <> and follow the instructions.

## For Batch service (BES)
To run a batch job in the production scenario (not on DSVM), you need to set up and HDI cluster. The command is below:

... HDI provisiong command

Open the notebook from here<> and follow the instruction.
