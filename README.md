# Azure Machine Learning vNext

## Overview

The new version of Azure Machine Learning (ML) is powered by Spark, and leverages many of the high-scale Azure Services including HDInsight, Azure Container Service (ACS), and Azure Container Registry (ACR). This new feature set supports both real-time (RRS) and batch (BES) scoring scenarios.

## Scope

The private preview of Azure ML vNext, uses a Data Science VM (DSVM) as the getting started environment. Using the Azure ML Command Line Interface (CLI), you can deploy Spark ML models and pipelines that you create in a Jupyter Notebook written in PySpark.

In this bug bash you deploy and run the web service locally on the DSVM. You then deploy and run the web service remotely on an ACS cluster. 

## Prerequisites

You will need configure the following items to complete the scenario.

1. Provision a DSVM
2. Install SSH software to access the DSVM
3. Provision Azure Container Registry (ACR) to host your web service's container Azure Container Service cluster to host your remote web service.

### Provision DSVM

To start using the Azure ML Private Preview, you must first provision a DSVM. The following steps will guide you through the process.

1. Sign in to the [Azure portal](https://portal.azure.com).
2. Click **New** and then type Linux Data Science Virtual Machine in the search box.
3. Select Linux Data Science Virtual Machine from the returned results.
4. Click Linux Data Science Virtual Machine [Staged] and then click **Create** to begin configuring and provisioning the virtual machine. 

When provisioning the DSVM, configure **Authentication type** as Password rather than SSH Public Key. 

**Important**: To successfully sign into the Jupyter hub, any alpha characters in the user name must be lower case. Using any upper case characters in the user ID will cause the sign in to the Jupyter hub to fail.

Once the DSVM is provisioned, note the IP address of the machine.

While in the Azure portal, record the information for the storage account you will use. You can use and existing account or create a new one.

You will need to SSH into the DSVM. We recommend you use MobaXterm Home Edition. You can install the MobaXterm software from [http://mobaxterm.mobatek.net/download-home-edition.html](http://mobaxterm.mobatek.net/download-home-edition.html).

Once you have installed MobaXTerm, open an SSH session to the DSVM.

Run the following command to provision your ACR and ACS:

	ACR/ACR

The ACR provisioning will complete quickly. Record the ACR Home, User, and Password information. Leave the session open until the ACS setup completes.

In Moba xTerm, start a second SSH session. Note: Do not open a new window on your current session.

In the new SSH session, change directory to the azureml folder:

```
cd ~/notebooks/azureml
```

Edit the sample_Env.sh file.


```
nano sample_env.sh
```
use the the information that you saved from the ACR create command output and the storage account credentials to update the following environment variables:

```
AML_STORAGE_ACCT_NAME=
AML_STORAGE_ACCT_KEY=
AML_ACR_HOME=
AML_ACR_USER=
AML_ACR_PW=
```

## Use the Jupyter notebook to train a model and deploy a RRS web service

Jupyter is running on the DSVM at https://&lt;machine-ip-address&gt;:8000. Open Jupyter in a browser and sign in. The user name and password are the those that you configured for the DSVM.  Note that you will receive a certificate warning that you can safely click through. 

### Run the Notebook 

The notebooks are located in the **AzureML** folder. 

To run the RRS scenario, open the realtimewebservices.ipynb notebook and follow the provided instructions to train, save, and deploy a model as an RRS web service.  The notebook contains instructions for deploying to the DSVM and for deployment to a production environment using ACS.

## For Batch service (BES)
To run a batch job in a production scenario (not on the DSVM), you need to set up an HDI cluster. To setup the HDI cluster, run the following command

... HDI provisioning command

To run the RRS scenario, open the batchwebservice.ipynb notebook and follow the provided instructions.

