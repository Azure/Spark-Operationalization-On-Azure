#if you are planning to deploy your web service to an HDInsight cluster, be sure to do the following before creating your web service:
# run the cells of the Notebook sample: 05 - Spark Machine Learning - Predictive analysis on food inspection data using MLLib
# this Jupyter sample exists with every provisioned HDInsight Spark2.0 cluster
# the sample web service we will be creating will be using the model from this sample. 
# add a cell right after a model is created (model.fit()) to save the model.
# model.save('wasb:///HdiSamples/HdiSamples/FoodInspectionDataModel/') 

from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.ml import Pipeline, PipelineModel
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.feature import HashingTF, Tokenizer
from pyspark.sql import Row
from pyspark.sql.functions import UserDefinedFunction
from pyspark.sql.types import *
import argparse

sc = SparkContext.getOrCreate()
sqlContext = SQLContext.getOrCreate(sc)

parser = argparse.ArgumentParser()
parser.add_argument("--input-data")
parser.add_argument("--output-data")

args = parser.parse_args()
print str(args.input_data)
print str(args.trained_model)
print str(args.output_data)

def csvParse(s):
    import csv
    from StringIO import StringIO
    sio = StringIO(s)
    value = csv.reader(sio).next()
    sio.close()
    return value

model = PipelineModel.load(str(args.trained_model))

testData = sc.textFile(str(args.input_data))\
             .map(csvParse) \
             .map(lambda l: (int(l[0]), l[1], l[12], l[13]))

schema = StructType([StructField("id", IntegerType(), False), 
                     StructField("name", StringType(), False), 
                     StructField("results", StringType(), False), 
                     StructField("violations", StringType(), True)])

testDf = sqlContext.createDataFrame(testData, schema).where("results = 'Fail' OR results = 'Pass' OR results = 'Pass w/ Conditions'")

predictionsDf = model.transform(testDf)

predictionsDf.write.parquet('wasb:///HdiSamples/HdiSamples/FoodInspectionDataModel')