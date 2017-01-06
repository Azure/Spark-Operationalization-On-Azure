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
4. Provision an HDInsight Spark 2.0 cluster or use an existing one


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

## Deploying the Batch web service

You can operationalize your model as a batch web service in 2 environments through our private preview offering.

1. Author your model and deploy the web service within a provisioned Data Science VM using the AzureML CLI that will also need to be installed on the Data Science VM. This is your local environment

2. Author your model and deploy the web service on a provisioned HDInsight Spark2.0 cluster. You will install the Azure ML CLI on your local Linux or Windows machine. In this case the Azure ML CLI will be operating with the remote environment settings.

### Deploying the Batch web service on a DSVM

Look for the food_inspections.ipynb in the AzureML folder[provide folder name]. You can also find this sample file in the git repo.

To run the Batch scenario, open the food_inspections.ipynb notebook and follow the provided instructions to train and save your model and create a Batch web service that makes predictions on a given set of data using the model.

### Deploying the Batch web service on an HDInsight Cluster

By this step you will have a provisioned an HDInsight Cluster for your web service deployment.

Follow the below instructions to deploy your batch web service. 

Click on the link https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fazuremlbatchtest.blob.core.windows.net%2Ftemplates%2FinstallTemplate.json and provide the Resource Group and name of the HDInsight Cluster. Leave the node size and count fields as is. Accept the license terms and click purchase. This template installs amlBatch app on your HDInsight Cluster. 

#### On Your HDInsight Cluster

Your HDInsight cluster already comes with a Food Inspections Jupyter Notebook Sample in the location HdiSamples/HdiSamples/FoodInspectionData.

Open the notebook and execute all the cells in this Notebook till you reach the model creation cell. The title above this cell is ‘Create a logistic regression model from the input dataframe’
Add the below line at the end of this cell to save your model.
model.write().overwrite().save('wasb:///HdiSamples/HdiSamples/FoodInspectionDataModel/')

Now execute this cell. You may choose to proceed further to execute the remaining cells or skip to continue to create the web service from the CLI.

#### On your machine that has the Azure CLI installed

Set the environment to cluster mode using the below command
> aml env cluster

Set the following environment variables on your local machine so the CLI web service commands are targeted at your HDInsight Cluster and associated storage.

```
AML_STORAGE_ACCT_NAME:  <your storage account name>
AML_STORAGE_ACCT_KEY: <your storage account key>
AML_HDI_CLUSTER: <the url to your hdinsight cluster. Do not include https://>
AML_HDI_USER: <your hdinsight user name>
AML_HDI_PW: <your hdinsight user password>
```

Copy over batch_score.py from the git repo[add git repo link] on your local machine. 
This is the pySpark program that will be deployed as the batch scoring web service for your food inspections model.
On the command prompt on your machine, type the following CLI command to deploy your web service.

>aml service create batch -n batch_score_webservice -i --input-data -i --trained-model='wasb:///HdiSamples/HdiSamples/FoodInspectionDataModel’ -o --output-data

This command creates your web service and saves it in the storage associated with the HDInsight cluster. After the web service is created, you will see instructions to run jobs against this web service.

