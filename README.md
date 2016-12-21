# Private preview of Azure Machine Learning vNext

## Overview
The new version of Azure Machine Learning (ML) is powered by Spark, and leverages many of the high-scale Azure Services including HDInsight, Azure Container Service (ACS), and Azure Container Registry (ACR).

## Private preview
The private preview of Azure ML vNext, uses a Data Science VM (DSVM) as the getting started environment. Using the Azure ML Command Line Interface (CLI), you can deploy Spark ML models and pipelines that you create in a Jupyter Notebook written in PySpark.

Using Docker Container, you can deploy these models as Real-time or Batch web services. The web services can run locally on the DSVM or remotely on the ACS cluster for real-time or on the HDI cluster for batch scnarios. 

The DSVM deployment is meant for development and testing. ACS and HDI (i.e. remote) deployments are meant for high-scale, production scenarios.

To start using Azure ML Private Preview, you must first provision a DSVM. The following steps will guide you through the process.

1. Sign in to the [Azure portal](https://portal.azure.com).
2. Click **New** and then type Linux Data Science Virtual Machine in the search box.
3. Select Linux Data Science Virtual Machine from the returned results.
4. Click Linux Data Science Virtual Machine [Staged] and then click **Create** to begin configuring and provisioning the virtual machine. 

When provisioning the DSVM, configure **Authentication type** as Password rather than SSH Public Key. Note: To successfully sign into the Jupyter hub, any alpha characters in the user name must be lower case. Using any upper case characters in the user ID will cause the sign in to the Jupyter hub to fail.

Once the DSVM is provisioned, note the IP address of the machine.

Next, ssh into the DSVM, we recommend you use [X2Go](http://code.x2go.org/releases/binary-win32/x2goclient/releases/4.0.5.2-2016.09.20/).

Create an X2Go session with the following details:

1. Host: (host IP) or (host DNS name)
2. Port: Get from DSVM Assignments
3. User: The DSVM user ID that you configured.
4. Password: The DSVM password that you configured.
5. Session type: XFCE

Uncheck Client side printing (under session preference -> media).

### Configure the DSVM

Open a terminal session, and run the following command:

    $ wget –q http://ritbhatrrs.blob.core.windows.net/release/dsvmsetup.sh -O - | sudo bash /dev/stdin $USER

The sudo password is the password you specified when you set the authentication type for the DSVM.

Once the script has finished running, sign out and then sign back into the DSVM.

#### Install the CLI

Install the ML CLI by entering the following command:

    pip install azuremlcli –extra-index-url https://pypi-amlbd.southcentralus.cloudapp.azure.com/simple --trusted-host https://pypi-amlbd.southcentralus.cloudapp.azure.com

### 2. Set up the environment

Install version 2.0 of the [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-az-cli2).

#### 2.1 Provision ACR (required)

    az acr create -name myRegistry -resource-group myResourceGroup -l southcentralus --storage-account-name myStorageAccount

For more information on managing Azure container  with the Azure CLI, see [az acr](https://docs.microsoft.com/en-us/cli/azure/acr).

#### 2.2 Provision ACS (optional for production deployment scenario)

  az group deployment create -g mygroup --template-uri https://myresource/azuredeploy.json --parameters @myparameters.json

For more information on deploying Azure container service templates with the Azure CLI, see [az group deployment](https://docs.microsoft.com/en-us/cli/azure/group/deployment).

#### 2.3 Provision HDI Spark (optional for production deployment scenario)

### 3. Open Sample Jupyter Noteook

Jupyter is running on the DSVM at https://<machine-ip-address>:8000. Open Jupyter in a browser and sign in. The username and password are the those that you configured for the DSVM.  Note that you will recieve a certifiate warning that you can safely click through. 

The *realtimewebservices.ipynb* sample notebook is located in the azureml folder. 
   
Click the notebook to open it. Follow the instructions to create and deploy a model as a web service for real-time or batch scoring.

