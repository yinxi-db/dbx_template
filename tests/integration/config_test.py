import unittest
from dbx_sample.common import Job

class SampleJob(Job):

    def launch(self):
        self.logger.info("Launching sample job")

        self.logger.info("config file loaded")

class ConfigurationTest(unittest.TestCase):
    def setUp(self):

        self.job = SampleJob()
        self.spark = self.job.spark
        self.config = self.job.conf

    def test_config(self):

        ## inspect existence of module parameters
        config_keys = self.config.keys()
        self.assertIn("transformation", config_keys, "transformation configs missing")
        self.assertIn("train", config_keys, "train configs missing")
        self.assertIn("score", config_keys, "score configs missing")
        self.assertIn("monitor", config_keys, "monitor configs missing")

        ## inspect transformation configs
        transform_configs = self.config["transformation"]
        self.assertIn("data_source", transform_configs, "data_source of transformation configs missing")
        self.assertIsNotNone(transform_configs["data_source"],  "data_source of transformation configs can't be None")

        self.assertIn("data_output_format", transform_configs, "data_output_format of transformation configs missing")
        self.assertEqual(transform_configs["data_output_format"], "delta", "data_output_format of transformation configs has to be `delta`")

        self.assertIn("data_dest", transform_configs, "data_dest of transformation configs missing")
        self.assertIsNotNone(transform_configs["data_dest"], "data_dest of transformation configs can't be None")

        self.assertIn("refresh_frequency", transform_configs, "refresh_frequency of transformation configs missing")
        self.assertIn("notifications", transform_configs, "notifications of transformation configs missing")
        self.assertIn("params", transform_configs, "params of transformation configs missing")

        ## inspect train configs
        train_configs = self.config["train"]
        self.assertIn("data_source", train_configs, "data_source of train configs missing")
        self.assertIsNotNone(train_configs["data_source"], "data_source of train configs can't be None")

        self.assertIn("mlflow_tracking_experiment", train_configs, "mlflow_tracking_experiment of train configs missing")
        self.assertIsNotNone(train_configs["mlflow_tracking_experiment"],
                         "mlflow_tracking_experiment of train configs can't be None")

        self.assertIn("mlflow_registered_model_name", train_configs, "mlflow_registered_model_name of train configs missing")
        self.assertIsNotNone(train_configs["mlflow_registered_model_name"], "mlflow_registered_model_name of train configs can't be None")

        self.assertIn("refresh_frequency", train_configs, "refresh_frequency of train configs missing")
        self.assertIn("notifications", train_configs, "notifications of train configs missing")
        self.assertIn("params", train_configs, "params of train configs missing")

        self.assertIn("model_tags", train_configs, "params of train configs missing")

        ## inspect score configs
        score_configs = self.config["score"]
        self.assertIn("data_source", score_configs, "data_source of score configs missing")
        self.assertIsNotNone(score_configs["data_source"], "data_source of score configs can't be None")

        self.assertIn("data_dest", score_configs, "data_dest of score configs missing")
        self.assertIsNotNone(transform_configs["data_dest"], "data_dest of score configs can't be None")

        self.assertIn("mlflow_model_stage", score_configs,
                      "mlflow_model_stage of score configs missing")
        self.assertEqual(score_configs["mlflow_model_stage"], "Production",
                             "mlflow_model_stage of score configs has to be `Production`")

        self.assertIn("mlflow_registered_model_name", score_configs,
                      "mlflow_registered_model_name of score configs missing")
        self.assertIsNotNone(train_configs["mlflow_registered_model_name"],
                             "mlflow_registered_model_name of score configs can't be None")

        self.assertIn("refresh_frequency", score_configs, "refresh_frequency of score configs missing")
        self.assertIn("notifications", score_configs, "notifications of score configs missing")
        self.assertIn("params", score_configs, "params of score configs missing")

        ## inspect monitor configs
        monitor_configs = self.config["monitor"]
        self.assertIn("params", monitor_configs, "params of monitor configs missing")
        self.assertIn("data_source", monitor_configs["params"], "data_source of monitor configs missing")
        self.assertIsNotNone(monitor_configs["params"]["data_source"], "data_source of monitor configs can't be None")

        self.assertIn("mlflow_registered_model_name", monitor_configs["params"],
                      "mlflow_registered_model_name of monitor configs missing")
        self.assertIsNotNone(monitor_configs["params"]["mlflow_registered_model_name"],
                             "mlflow_registered_model_name of monitor configs can't be None")

        self.assertIn("alerting_threshold", monitor_configs,
                      "alerting_threshold of monitor configs missing")
        self.assertIsNotNone(monitor_configs["alerting_threshold"],
                             "alerting_threshold of monitor configs can't be None")

        self.assertIn("refresh_frequency", train_configs, "refresh_frequency of train configs missing")
        self.assertIn("notifications", train_configs, "notifications of train configs missing")

    def tearDown(self):
        pass


if __name__ == "__main__":
    # please don't change the logic of test result checks here
    # it's intentionally done in this way to comply with jobs run result checks
    # for other tests, please simply replace the SampleJobIntegrationTest with your custom class name
    loader = unittest.TestLoader()
    tests = loader.loadTestsFromTestCase(ConfigurationTest)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(tests)
    if not result.wasSuccessful():
        raise RuntimeError(
            "One or multiple tests failed. Please check job logs for additional information."
        )
