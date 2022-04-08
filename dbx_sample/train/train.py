from dbx_sample.common import Job


class TrainJob(Job):

    def launch(self):
        from sklearn.ensemble import RandomForestRegressor
        import mlflow
        from mlflow.tracking import MlflowClient

        mlflow.autolog(log_input_examples=True, log_model_signatures=True)
        self.logger.info("Launching training job")

        listing = self.dbutils.fs.ls("dbfs:/")

        for l in listing:
            self.logger.info(f"DBFS directory: {l}")

        input_path = self.conf["train"]["data_source"]
        model_params = self.conf["train"]["params"]
        mlflow_experiment = self.conf["train"]["mlflow_tracking_experiment"]
        mlflow_model_name = self.conf["train"]["mlflow_registered_model_name"]
        model_tags = self.conf["train"]["model_tags"]

        ## inspect existence of mlflow experiments
        if not mlflow_experiment in [x.name for x in mlflow.list_experiments()]:
            mlflow.create_experiment(mlflow_experiment)
        mlflow.set_experiment(experiment_name=mlflow_experiment)

        df = self.spark.read.load(input_path).toPandas() ## read from delta by default
        rf = RandomForestRegressor(**model_params) ## build model

        ## log training
        with mlflow.start_run() as run:
            rf.fit(df.drop(["quality"],axis=1), df["quality"])
        ## register model
        mlflow.register_model(f"runs:/{run.info.run_id}/model",
                              mlflow_model_name,
                              )
        current_version = MlflowClient().get_latest_versions(mlflow_model_name, stages=["None"])[0].version
        for k, v in model_tags["version_tag"].items():
            MlflowClient().set_model_version_tag(mlflow_model_name, current_version, k, v)
        for k, v in model_tags["model_tag"].items():
            MlflowClient().set_registered_model_tag(mlflow_model_name, k, v)

        self.logger.info("Training job finished!")


if __name__ == "__main__":
    job = TrainJob()
    job.launch()
