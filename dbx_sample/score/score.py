from dbx_sample.common import Job


class ScoreJob(Job):

    def launch(self):
        import mlflow
        from pyspark.sql.functions import col, lit
        from mlflow.tracking import MlflowClient
        from datetime import date

        self.logger.info("Launching scoring job")

        listing = self.dbutils.fs.ls("dbfs:/")

        for l in listing:
            self.logger.info(f"DBFS directory: {l}")

        input_path = self.conf["score"]["data_source"]
        score_params = self.conf["score"]["params"]
        mlflow_model_name = self.conf["score"]["mlflow_registered_model_name"]
        model_stage = self.conf["score"]["mlflow_model_stage"]
        output_path = self.conf["score"]["data_dest"]

        df = self.spark.read.load(input_path) ## read scoring data from delta by default

        ## load model with mlflow.pyfunc
        model_version = MlflowClient().get_latest_versions(mlflow_model_name, stages=[model_stage])[0].version
        model_uri = f"models:/{mlflow_model_name}/{model_version}"
        predict = mlflow.pyfunc.spark_udf(self.spark, model_uri)

        ## prediction
        input_features = [x.name for x in predict.metadata.get_input_schema().as_spark_schema().fields]
        ## add scoring date, model_name and model_version for meta info
        df_prediction = df.withColumn("prediction",
                                      predict(*input_features)
                         ).withColumn("score_date",
                                      lit(date.today())
                         ).withColumn("model_name",
                                      lit(mlflow_model_name)
                         ).withColumn("model_version",
                                      lit(model_version)
                        )

        ## write to file
        df_prediction.write.mode("overwrite").option("overwriteSchema", True).save(
            output_path
        ) ## write to delta by default

        self.logger.info("Scoring job finished!")


if __name__ == "__main__":
    job = ScoreJob()
    job.launch()
