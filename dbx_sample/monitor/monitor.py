from dbx_sample.common import Job


class MonitorJob(Job):

    def alert(self):
        pass

    def launch(self):
        from pyspark.sql.functions import col, avg, max
        self.logger.info("Launching monitor job")

        listing = self.dbutils.fs.ls("dbfs:/")

        for l in listing:
            self.logger.info(f"DBFS directory: {l}")

        data_path = self.conf["monitor"]["params"]["data_source"]
        row_count_deviation_threshold = self.conf["monitor"]["alerting_thresholds"]["row_count_deviation"]

        df = self.spark.read.options(delimiter=";", header=True).csv(data_path)
        ## mean batch count
        mean_batch_count = df.groupby("score_date").count().select(avg("count")).first()[0]
        cur_batch_count = df.filter(col("score_date")==df.select(max("score_date")).first()[0]).count()

        if abs(cur_batch_count-mean_batch_count)>row_count_deviation_threshold*mean_batch_count:
            self.alert()

        self.logger.info("Monitor job finished!")


if __name__ == "__main__":
    job = MonitorJob()
    job.launch()
