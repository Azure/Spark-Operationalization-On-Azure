# Azure Machine Learning vNext (Private Preview)

## Overview

The new version of Azure Machine Learning (AML) is powered by Spark and supports the operationlization of both real-time and batch scoring scenarios. Using the new Azure Machine Learning CLI you can deploy machine learning models as RESTful web services in high scale cluster environments.

## Getting Started

The getting started environment uses a Data Science VM (DSVM). For information on provisioning a DSVM, see [Provision the Linux Data Science Virtual Machine](https://docs.microsoft.com/en-us/azure/machine-learning/machine-learning-data-science-linux-dsvm-intro).

Once you have signed into the DSVM, run the following commands and follow the prompts:

	$ sudo /opt/microsoft/azureml/initial_setup.sh
	$ aml env show

Once the setup command has finished, it outputs environment export commands for the AML CLI environment. We suggest that you create a shell script containing the commands so that you can run them again in the future.

## Jupyter notebook

Jupyter is running on the DSVM at https://&lt;machine-ip-address&gt;:8000. Open Jupyter in a browser and sign in. The user name and password are those that you configured for the DSVM. Note that you will receive a certificate warning that you can safely click through. 

### Run the Notebook 

There are notebooks for both the real-time and batch web service scenarios. The notebooks are located in the **azureml\realtime** and **azureml\batch** folders. 



To run the real-time scenario, from the azureml folder, change to the realtime folder and open the  realtimewebservices.ipynb notebook. Follow the instructions to train, save, and deploy a model as a real-time web service.  The notebook contains instructions for deploying to the DSVM and for deployment to a production ACS environment.

To run the batch scenario on the DSVM, from the azureml folder, change to the batch folder and open the batchwebservices.ipynb notebook. Follow the provided instructions to train, save, and deploy a model as a local web service to the DSVM or to a production HDInsight environment. 

## Updating the DSVM environment

To update the Azure ML bits on the DSVM, run the following command.

	$ wget -q http://ritbhatrrs.blob.core.windows.net/release/amlupdate.sh -O - | sudo bash /dev/stdin
