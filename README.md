# Azure Machine Learning vNext

The new version of Azure Machine Learning is powered by Spark, and will leverage many of high-scale Azure Services including HDInsight, Azure Container Service (ACS) and Azure Container Registry (ACR).

## Private Preview
For Privew Preview of Azure ML, we are using the Data Science VM (DS VM) as the environment to get started using the Azure ML vNext. Using the Azure ML Command Line Interface (CLI), you can deploy Spark ML models and pipelines you create in the Jupyter Notebook written in PySpark.

These models can be deployed, using Docker Container, as Real-time or Batch web services to run locally on the DS VM or remotely on the ACS cluster for real-time or on the HDI cluster for batch scnarios. 

The DS VM deployment is meant for development and testing. ACS and HDI (i.e. remote) deployments are meant for high-scale, production scenarios.

The following are the steps to start using Azure ML Private Preview.

### 1. Provision Data Science VM
Provision the Linux Data Science VM. Using this VM, you can deploy a model or pipeline as a web service and call the web service for testing.

#### 1.1 Install the Azure ML CLI
--- from where
--- what is the command

### 2. Set up the environment

#### 2.1 Provision ACR (required)

#### 2.2 Provision ACS (optional for production deployment scenario)

#### 2.3 Provision HDI Spark (optional for production deployment scenario)

### 3. Open Sample Jupyter Noteook
Start Jupyter Notebook on the DS VM. Then open the AML Sample Notebook.
--- where?
Follow the instructions to create and deploy a model as a web service for real-time or batch scoring.
