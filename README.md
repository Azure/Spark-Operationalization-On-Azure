# Azure Machine Learning vNext (Private Preview)

## Overview

The new version of Azure Machine Learning (ML) is powered by Spark and supports the operationlization of both the real-time and batch scoring scenarios. Using the new Azure Machine Learning CLI you can deploy machine learning models as RESTful web services in a high scale cluster environments.

Most of the features of the private preview are available for anyone. To use the Azure ML CLI, you must have an API key. If you have not been officially on boarded as part of the private preview, you can obtain an API key by emailing raymondl@microsoft.com. 

## Getting Started

The getting started environment uses a Data Science VM (DSVM). For information on provisioning a DSVM, see [Provision the Linux Data Science Virtual Machine](https://docs.microsoft.com/en-us/azure/machine-learning/machine-learning-data-science-linux-dsvm-intro).

Once you have signed into the DSVM, run the following command and follow the prompts:

	aml env setup

Once the setup command has finished, it outputs environment export commands for Azure Machine Learning CLI environment. We suggest that you create a shell script containing the commands so that you can run them again in the future.

## Jupyter notebook

Jupyter is running on the DSVM at https://&lt;machine-ip-address&gt;:8000. Open Jupyter in a browser and sign in. The user name and password are the those that you configured for the DSVM. Note that you will receive a certificate warning that you can safely click through. 

### Run the Notebook 

The notebooks are located in the **azureml\realtime** and **azureml\batch** folders. 

**Note**: There are notebooks for both the real-time and Batch web service scenarios. Jupyter does not allow multiple notebooks to be running at the same time. Once you have finished with one scenario, stop the notebook before starting the next one. To stop the notebook:

* If you are still in the notebook, select **File** and then click **Close and Halt**.
* Otherwise, open the azureml folder, click the checkbox to select the notebook and then click **Shutdown**.

To run the real-time scenario, from the azureml folder, change to the realtime folder and open the  realtimewebservices.ipynb notebook. Follow the instructions to train, save, and deploy a model as a real-time web service.  The notebook contains instructions for deploying to the DSVM and for deployment to a production environment using ACS.

To run the batch scenario on the DSVM, from the azureml folder, change to the batch folder and open the batchwebservices.ipynb notebook. Follow the provided instructions to train, save, and deploy a model as a local web service. 

To deploy a batch web service to an HDInsight cluster, see [Deploying a Batch web service on an HDInsight Cluster](batch-hdinsight.md).


