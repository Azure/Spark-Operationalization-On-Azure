# Azure Machine Learning vNext (Private Preview)

## Overview

The new version of Azure Machine Learning (ML) is powered by Spark, and leverages many of the high-scale Azure Services including HDInsight, Azure Container Service (ACS), and Azure Container Registry (ACR). This new feature set supports both real-time (RRS) and batch (BES) scoring scenarios.

## Scope

The private preview of Azure ML vNext, uses a Data Science VM (DSVM) as the getting started environment. Using the Azure ML Command Line Interface (CLI), you can deploy Spark ML models and pipelines that you create in a Jupyter Notebook written in PySpark. 

In this private preview scenario, you will deploy and run web services locally on the DSVM. You will then deploy and run an RRS web service remotely on an ACS cluster or a BES web service on an HDInsight cluster.

Most of the features of the private preview are available for anyone. To use the Azure ML CLI, you must have an API key. If you have not been officially on boarded as part of the private preview, you can obtain an API key by emailing raymondl@microsoft.com. 

## Prerequisites

You need configure the following items to complete the scenario.

1. Provision a DSVM
2. Choose or create a storage account in which to store web service information.
2. Install SSH software to access the DSVM.
3. Install the Azure CLI version 2.0 on the DSVM.
3. Provision Azure Container Registry (ACR) to host your web service's container Azure Container Service cluster to host your remote web service.
4. For the real-time scenario, provision an Azure Container Service instance.
4. For the batch scenario, provision an HDInsight Spark 2.0 cluster or use an existing one.

### Provision DSVM

To start using the Azure ML Private Preview, you must first provision a DSVM. 

The following steps will guide you through the process.

1. Sign in to the [Azure portal](https://portal.azure.com).
2. Click **New** and then type Linux Data Science Virtual Machine in the search box.
3. Select Linux Data Science Virtual Machine from the returned results.
4. Click **Linux Data Science Virtual Machine [Staged]** and then click **Create** to begin configuring and provisioning the virtual machine. 
	1. When provisioning the DSVM, configure **Authentication type** as Password rather than SSH Public Key. 
	2. **Important**: To successfully sign into the Jupyter hub, any alpha characters in the user name must be lower case. Using any upper-case characters in the user ID will cause the sign in to the Jupyter hub to fail.

Once the DSVM is provisioned, note the IP address of the machine.

### Storage account

While in the Azure portal, choose or create a storage account in which to store web service information. Record the storage account name and access key to use later.

### Install the SSH software 

You will need to SSH into the DSVM. We recommend you use MobaXterm Home Edition. You can install the MobaXterm software from [http://mobaxterm.mobatek.net/download-home-edition.html](http://mobaxterm.mobatek.net/download-home-edition.html).

Once you have installed MobaXterm, open an SSH session to the DSVM.

Run the following command in SSH session:

	$ wget -q http://ritbhatrrs.blob.core.windows.net/release/dsvmsimplesetup.sh -O - | sudo bash /dev/stdin $USER

Then sign out of the DSVM and then sign back in.

### Install the Azure CLI version 2

To install the CLI, start an SSH session in Moba xTerm. Then run the following command:

	sudo /anaconda/envs/py35/bin/pip install azure-cli 

### Provision the ACR

Sign in to the azure cli on the DSVM using the ```az login``` command.
Open a browser on your local machine and navigate to ```https://aka.ms/devicelogin```. Enter the authentication code and follow the prompts.

To provision the ACR, you must run the Azure CLI acr create command. 

The acr create command requires the following parameters:

* name - A name that you supply for the registry.
* resource-group - A resource group in your subscription, this can be an existing group or one that you create for the private preview. Note that the resource group must be in the same region as the ACR.
* l - The region in which the ACR is created. At this time, you can only create an ACR in eastus,southcenteralus, and westus.
* storage-account-name - Use the storage account you selected earlier.
* admin-enabled - Set to **true**.

The following is an example of the acr create command, replace the parameters with values that you supply:

	az acr create --name myRegistry --resource-group myResourceGroup -l southcentralus --storage-account-name myStorageAccount --admin-enabled true

Get the ACR password:

	az acr credential show -n myRegistry

The ACR provisioning will complete quickly. Record the ACR Home, User, and Password information. 

### Provision ACS (For RRS production "cluster" deployment only)

click the following and complete the ACS deployment (this will take up to 20 minutes so start, then continue with the next step):

<a href="https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Famlacstemplateresources.blob.core.windows.net%3A443%2Ftemplates%2Fproduction%2FAmlMesosTemplate.json" target="_blank"><img src="http://azuredeploy.net/deploybutton.png"/></a> 

### Edit the environment configuration file

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

## Jupyter notebook

Jupyter is running on the DSVM at https://&lt;machine-ip-address&gt;:8000. Open Jupyter in a browser and sign in. The user name and password are the those that you configured for the DSVM.  Note that you will receive a certificate warning that you can safely click through. 

### Run the Notebook 

The notebooks are located in the **azureml** folder. 

**Note**: There are notebooks for both the RRS and Batch web service scenarios. Jupyter does not allow multiple notebooks to be running at the same time. Once you have finished with one scenario, stop the notebook before starting the next one. To stop the notebook:

* If you are still in the notebook, select **File** and then click **Close and Halt**.
* Otherwise, open the azureml folder, click the checkbox to select the notebook and then click **Shutdown**.

### Deploying an RRS web service

To run the RRS scenario, open the realtimewebservices.ipynb notebook and follow the provided instructions to train, save, and deploy a model as an RRS web service.  The notebook contains instructions for deploying to the DSVM and for deployment to a production environment using ACS.

### Deploying the Batch web service

You can operationalize your model as a batch web service in two environments through the private preview offering.

1. Author your model and deploy the web service within a provisioned Data Science VM using the Azure ML CLI. You use this option in a dev/test or local environment when you are testing out your web service.
2. Author your model and deploy the web service on a provisioned HDInsight Spark 2.0 cluster. You use this option when you're ready to deploy your web service to production. In this case, you can install Azure ML CLI on your local Linux or Windows machine and execute the CLI commands in a cluster environment

#### Deploying the Batch web service on a DSVM

To run the Batch scenario, open Jupyter in a browser and sign in. The user name and password are the those that you configured for the DSVM. Open  the azureml folder and then click on the food_inspections.ipynb notebook. You can also find this sample file in the git repo. Follow the provided instructions to train and save your model and create a Batch web service that makes predictions on a given set of data using the model.

#### Deploying the Batch web service on an HDInsight Cluster

If you haven't already, provision a HDInsight Spark 2.0 cluster. 

To provision an HDInsight Spark 2.0 cluster:

1. Sign in to the the [Azure portal](https://portal.azure.com)
2. click **New** and type HDInsight

After the cluster deployment is complete must install the Azure Machine Learning Batch application to enable the cluster to execute on the commands submitted through the Azure ML CLI from your local machine.

To install the AMLBatch app on your HDInsight cluster, click the following link: 
[https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fazuremlbatchtest.blob.core.windows.net%2Ftemplates%2FinstallTemplate.json](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fazuremlbatchtest.blob.core.windows.net%2Ftemplates%2FinstallTemplate.json)

When the template opens, provide the Resource Group and name of the HDInsight Cluster where the web service will be deployed. Leave the node size and count fields as is. Accept the license agreement and click **purchase**.

##### On Your HDInsight Cluster

Your HDInsight cluster already comes with a Food Inspections Jupyter Notebook Sample in the folder located at  HdiSamples/HdiSamples/FoodInspectionData.

Open the notebook and execute all the cells in it till you reach the model creation cell. The title for this cell is ‘Create a logistic regression model from the input dataframe’.


Add the following line at the end of this cell to save your model.

-```
model.write().overwrite().save('wasb:///HdiSamples/HdiSamples/FoodInspectionModel/')
```

Execute this cell. You can choose to proceed further to execute the remaining cells or skip to continue to create the web service from the CLI.

##### On your local machine 

Perform the following steps on a Linux or Windows machine that has Python installed.

Install the Azure Machine Learning CLI using the following pip command:
```
pip install azuremlcli --extra-index-url https://pypi-amlbd.southcentralus.cloudapp.azure.com/simple --trusted-host pypi-amlbd.southcentralus.cloudapp.azure.com --upgrade
```
If you're installing the CLI on a windows machine, you will need to append **--ignore-installed** to your pip command:
```
pip install azuremlcli --extra-index-url https://pypi-amlbd.southcentralus.cloudapp.azure.com/simple --trusted-host pypi-amlbd.southcentralus.cloudapp.azure.com --upgrade --ignore-installed
```
You will be prompted for a username and password:
```
user: pypi
Rpassword: aml$parkR0cks
```
Once the CLI is successfully installed/upgraded, run the following command to set your CLI environment to run in cluster mode.

```
aml env cluster
```
You will see the below prompt:
```
Would you like to set up port forwarding to your ACS cluster (Y/n)? n
```
Type **n** at the above prompt since you are not running the RRS scenario on ACS.

Type **y** to continue with cluster mode at the below prompt:
```
Could not connect to ACS cluster. Continue with cluster mode anyway (y/N)? y
```

To target the HDInsight Cluster and associated storage, set the following environment variables.

**Important**: Make sure the storage account you use is the one that's associated with your HDInsight Cluster, 

```
AML_STORAGE_ACCT_NAME:  <your storage account name>
AML_STORAGE_ACCT_KEY: <your storage account key>
AML_HDI_CLUSTER: <the url to your hdinsight cluster. Do not include https://>
AML_HDI_USER: <your hdinsight user name>
AML_HDI_PW: <your hdinsight user password>

example command for linux:
export AML_STORAGE_ACCT_NAME=<name>

example command for windows:
set AML_STORAGE_ACCT_NAME=<name>
```

Copy the batch_score.py from the [Azure ML vNext git repo](https://github.com/Azure/AzureML-vNext) to your local machine. 

This is the web service definition file that defines the inputs that your web service will expect and the outputs it will produce. You will need to provide these input and output parameters as commandline arguments when calling the web service create command from the Azure Machine Learning CLI

From the command prompt on your machine, type the following CLI command to deploy your web service:

```
aml service create batch -n batch_webservice -f batch_score.py --input=--input-data --output=--output-data
```

This command creates your web service using the provided web service definition file(batch_score.py) and saves it in the storage associated with the HDInsight cluster. 

Run the following command for guidance on calling the web service:

```
aml service view batch -n batch_webservice
```
Run the following command for calling jobs against the web service you created

```
aml service run batch -n batch_webservice --input=--input-data:wasb://HdiSamples/HdiSamples/FoodInspectionData/Food_Inspections1.csv --output=--output-data:wasb://HdiSamples/HdiSamples/FoodInspectionWebServiceOutput -w
```
The **-w** parameter indicates a synchronous call, i.e. wait till the job run completes.
