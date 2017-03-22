# Walkthrough: Operationalizing Tensorflow image classification 

In this walkthrough, you will learn how to deploy a Tensorflow model as a web service using the Azure Machine Learning CLI. The walkthrough uses the [MNIST sample dataset](http://yann.lecun.com/exdb/mnist/) to train a model to recognize a handwritten digit and is based on the Tensorflow [MNIST For ML Beginners](https://www.tensorflow.org/get_started/mnist/beginners) tutorial. 

Steps:

1.  Provision a Data Science Virtual Machine.
2.  Prepare the DSVM.
2.  Train the model.
2.  Create the web Service.
3.  Test the web service by scoring an image.

## Provision a Data Science Virtual Machine

To complete the AML CLI tutorials and walkthroughs, you must provision a Microsoft Linux Data Science Virtual Machine (DSVM). If you have not yet provisioned a DSVM, set the [tutorial setup](../../../tutorial_setup.md) document.

## Prepare the DSVM 

To prepare the DSVM to run the walkthrough.

1. Sign into the DSVM. Navigate to the notebooks > azureml folder. 
2. Create a folder named *tensorflow*. 
3. From the folder for this walkthrough on GitHub, copy the driver.py, tensorscorer.py, and tensortrain.py files to your tesnsorflow folder on the DSVM.
3. Install the Tensorflow libraries on the DSVM:

	$ sudo /anaconda/envs/py35/bin/pip install tensorflow

## Train the model

To train the model: 

1. Navigate to the tensoflow folder.
2. Run the training script:
	
	```
	$ python tensortrain.py
	```

The training script trains and saves the model files.

## Deploy the model as web service

To deploy the model as a web service, you must supply a driver program that loads the trained model and recognizes a handwritten image as digit using the input. For this walkthrough, you will use the sample driver.py that you have copied to the tensorflow folder on the DSVM.

The following command creates and deploys the model as a real-time web service:


	$ aml service create realtime -r <runtime type>  -f <driver file> -m <model file> -n <your service name>

Example command for this walkthrough:
		
	$ aml service create realtime -r tensorflow-py -f driver.py -m mnist_model.index -m mnist_model.data-00000-of-00001 -m mnist_model.meta -n tensorflowsrvc1

When the service finishes deploying, the AML CLI returns the service URL and service port which you use to call the service. If you need to retrieve the URL and port, you can call the ```aml service view``` command.

	$ aml service view realtime <your service name>

For information on deploying the web service on an ACS cluster, see the notes section at the end of the walkthrough.

## Test the web service by scoring an image

Once the web service is deployed, you can call it to do predictions:

	```
	$ python tensorscorer.py --imgIdx <index of an image> ---url http://<your service URL>:<your service port>/score --name <your service name>
	```
	Example:
	
	The following example uses the web service to recognize digit for the 10th in image in the dataset against the trained model.

	```
	$  python tensorscorer.py --imgIdx 10 --url http://127.0.0.1:32795/score --name tensorflowsrvc1
	```

## Summary

Using the Azure Machine Learning CLI you can quickly deploy and test a Tensorflow trained model as a web service. When you are satisfied with the results of your testing and want to scale out the service, you can use the same commands to deploy the web service to an ACS cluster.

## Notes

### Deploying to an ACS cluster

A three node ACS is cluster is provisioned as part of the *aml env setup*. The provisioning takes about 20 minutes and updates the *.amlenvrc* file with the information on the cluster.

Source the file to set up your environment variables that include the ACS cluster information:

	$ source ~/.amlenvrc

To set your environment to cluster mode, enter the following command:

	$ aml env cluster

You can then run the AML command to create the service on the cluster.

	$ aml service create realtime -r <runtime type>  -f <driver file> -m <model file> -n <your service name>

Example:
		
	$ aml service create realtime -r tensorflow-py -f driver.py -m mnist_model.index -m mnist_model.data-00000-of-00001 -m mnist_model.meta -n tensorflowsrvc1



When the service finishes deploying, the AML CLI returns the service URL which you use to call the service. If you need to retrieve the URL and port, you can call the ```aml service view``` command. When you call the web service on the ACS cluster, you must always use port 9091.

	$ python tensorscorer.py --imgIdx <index of an image> ---url http://<your service URL>:9091/score --name <your service name>

