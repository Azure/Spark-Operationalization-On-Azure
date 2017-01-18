# Deploying a Batch web service on an HDInsight Cluster

If you haven't already, provision an Azure HDInsight Spark 2.0 cluster. 

To provision an HDInsight Spark 2.0 cluster:

1. Sign in to the the [Azure portal](https://portal.azure.com).
2. click **New** and type HDInsight
3. Select HDInsight from the list returned results.
4. Click **Create**.
5. Enter a **Cluster name**.
6. Click **Cluster configuration**.
	1. In **Cluster type**, select **Spark**. 
	2. in **Version**, select **Spark 2.0.1 (HDI 3.5)**.
	3. Click **Select**.
7. Click **Credentials** and configure the credentials for the cluster. To access Jupyter notebooks, the SSH user name must be all lower case and you must select password authentication.
8. Click **Cluster size**, then click **Select** to accept the default options.
9. Select a resource group to to contain the cluster.
10. Click **Create**.

After the cluster deployment is complete must install the Azure Machine Learning Batch application to enable the cluster to execute on the commands submitted through the Azure ML CLI from your local machine.

To install the AMLBatch app on your HDInsight cluster, click the following link: 

<a href="https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fazuremlbatchtest.blob.core.windows.net%2Ftemplates%2FinstallTemplate.json" target="_blank">AML Batch Install Template</a>.

When the template opens, provide the Resource Group and name of the HDInsight Cluster where the web service will be deployed. Leave the node size and count fields as is. Accept the license agreement and click **purchase**.

## On Your HDInsight Cluster

Your HDInsight cluster comes with the *05 - Spark Machine Learning - Predictive analysis on food inspection data using MLLib.ipynb* Jupyter Notebook Sample located in the PySpark folder.

To open the Jupyter notebook on your cluster:

1. Sign in to the the <a href="https://portal.azure.com" target="_blank">Azure portal</a>.
2. Open HDInsight blade for your cluster.
3. Click **Cluster dashboards**, then click **Jupyter Notebook.**

Open the notebook and execute all the cells in it till you reach the model creation cell. The title for this cell is 'Create a logistic regression model from the input dataframe'.

Add the following line at the end of this cell to save your model.

```
model.write().overwrite().save('wasb:///HdiSamples/HdiSamples/FoodInspectionModel/')
```

Execute this cell. You can choose to proceed further to execute the remaining cells or skip to continue to create the web service from the CLI.

### On your local machine 

Perform the following steps on a Linux or Windows machine that has Python installed.

Install the Azure Machine Learning CLI. **Note**: You will be prompted for a username and password:
```
user: pypi
Rpassword: aml$parkR0cks
```

Use the following pip command to install the Azure CLI on Linux:
```
pip install azuremlcli --extra-index-url https://pypi-amlbd.southcentralus.cloudapp.azure.com/simple --trusted-host pypi-amlbd.southcentralus.cloudapp.azure.com --upgrade
```

If you're installing the CLI on Windows, append **--ignore-installed** to your pip command:
```
pip install azuremlcli --extra-index-url https://pypi-amlbd.southcentralus.cloudapp.azure.com/simple --trusted-host pypi-amlbd.southcentralus.cloudapp.azure.com --upgrade --ignore-installed
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

To target the HDInsight Cluster and associated storage, set the following environment variables:

	AML_STORAGE_ACCT_NAME:  <your storage account name>
	AML_STORAGE_ACCT_KEY: <your storage account key>
	AML_HDI_CLUSTER: <the url to your hdinsight cluster. Do not include https://>
	AML_HDI_USER: <your hdinsight user name>
	AML_HDI_PW: <your hdinsight user password>

**Important**: Make sure the storage account you use is the one that's associated with your HDInsight Cluster.

example command for linux:

	export AML_STORAGE_ACCT_NAME=<name>

example command for windows:

	set AML_STORAGE_ACCT_NAME=<name>

On Windows, to persist the settings between sessions, you can add the Environment Variables in the System Properties.  Open your control panel, click **System** and then click **Advanced System Properties**.


Copy the batch_score.py from the <a href="https://github.com/Azure/AzureML-vNext" target="_blank:>Azure ML vNext Github repo</a> to your local machine. 

The batch_score.py defines web service. It specifies the inputs that your web service will expect and the outputs it produces. You must provide these input and output parameters as commandline arguments when calling the Azure Machine Learning CLI web service create command.

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



[batchappinatlltemplate]: "https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fazuremlbatchtest.blob.core.windows.net%2Ftemplates%2FinstallTemplate.json" target="_blank"
