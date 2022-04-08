from dbx_sample.common import Job


class TransformJob(Job):

    def launch(self):
        from pyspark.sql.functions import col, lit
        self.logger.info("Launching transformation job")

        listing = self.dbutils.fs.ls("dbfs:/")

        for l in listing:
            self.logger.info(f"DBFS directory: {l}")

        input_path = self.conf["transformation"]["data_source"]
        output_path = self.conf["transformation"]["data_dest"]
        output_format = self.conf["transformation"]["data_output_format"]

        df = self.spark.read.options(delimiter=";", header=True).csv(input_path)
        df_rename = df.select([col(c).alias(c.replace(' ', '_')) for c in df.columns])
        df_rename.write.format(output_format).mode("overwrite").option("overwriteSchema", True).save(
            output_path
        )

        self.logger.info("Transformation job finished!")


if __name__ == "__main__":
    job = TransformJob()
    job.launch()
