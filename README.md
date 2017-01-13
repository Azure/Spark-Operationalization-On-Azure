# Azure Machine Learning vNext (Private Preview)

## Overview

The new version of Azure Machine Learning (ML) is powered by Spark and supports the operationlization of both the real-time and batch scoring scenarios through the new Azure Machine Learning CLI.

Most of the features of the private preview are available for anyone. To use the Azure ML CLI, you must have an API key. If you have not been officially on boarded as part of the private preview, you can obtain an API key by emailing raymondl@microsoft.com. 

## Getting Started

The getting started environment uses a Data Science VM (DSVM). For information on provisioning a DSVM, see [Provision the Linux Data Science Virtual Machine](https://docs.microsoft.com/en-us/azure/machine-learning/machine-learning-data-science-linux-dsvm-intro).

Once you have signed into the DSVM, run the following commands:

	ssh-keygen -t rsa -b 2048 -f ~/.ssh/id_rsa
	<ACR/ACS/Storage Creation command>

## Jupyter notebook

Jupyter is running on the DSVM at https://&lt;machine-ip-address&gt;:8000. Open Jupyter in a browser and sign in. The user name and password are the those that you configured for the DSVM. Note that you will receive a certificate warning that you can safely click through. 

### Run the Notebook 

The notebooks are located in the **azureml** folder. 

**Note**: There are notebooks for both the real-time and Batch web service scenarios. Jupyter does not allow multiple notebooks to be running at the same time. Once you have finished with one scenario, stop the notebook before starting the next one. To stop the notebook:

* If you are still in the notebook, select **File** and then click **Close and Halt**.
* Otherwise, open the azureml folder, click the checkbox to select the notebook and then click **Shutdown**.

To run the real-time scenario, open the realtimewebservices.ipynb notebook and follow the provided instructions to train, save, and deploy a model as a real-time web service.  The notebook contains instructions for deploying to the DSVM and for deployment to a production environment using ACS.