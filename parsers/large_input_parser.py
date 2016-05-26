""" File to process the large dataset using spark
"""
import os
import sys

spark_home = '/usr/local/spark'
sys.path.insert(0, spark_home + "/python")

# Add the py4j to the path.
# You may need to change the version number to match your install
sys.path.insert(0, os.path.join(spark_home, 'python/lib/py4j-0.9-src.zip'))

# Initialize PySpark to predefine the SparkContext variable 'sc'
execfile(os.path.join(spark_home, 'python/pyspark/shell.py'))

import re
from pyspark.sql.types import *
from pyspark.sql.functions import *

from pyspark.ml import Pipeline
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.feature import HashingTF, Tokenizer
from pyspark.mllib.evaluation import BinaryClassificationMetrics

targetTag = "java"
textFile = sc.textFile("/projects/PycharmProjects/stackoverflow1/data/android.stackexchange.com/Posts.xml")

postsXml = textFile.map(lambda line: line.strip()).filter(lambda line: line != "<posts>" and line != "</posts>").filter(
    lambda line: not line.startswith("<?xml version=")).filter(lambda line: line.find("Id=") >= 0).filter(
    lambda line: line.find("Tags=") >= 0).filter(lambda line: line.find("Body=") >= 0).filter(
    lambda line: line.find("Title=") >= 0)

postsRDD = postsXml.map(lambda s: pyspark.sql.Row(
    Id=re.search('Id=".+?"', s).group(0)[4:-1].encode('utf-8'),
    Label=1.0 if re.search('Tags=".+?"', s) != None
                 and re.search('Tags=".+?"', s).group(0)[6:-1].encode('utf-8').find(targetTag) >= 0 else 0.0,
    Text=((re.search('Title=".+?"', s).group(0)[7:-1] if re.search('Title=".+?"', s) != None else "") + " " + (
        re.search('Body=".+?"', s).group(0)[6:-1]) if re.search('Body=".+?"', s) != None else "")))

postsLabeled = sqlContext.createDataFrame(postsRDD)

positive = postsLabeled.filter(postsLabeled.Label > 0.0)
negative = postsLabeled.filter(postsLabeled.Label < 1.0)
