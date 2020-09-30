from spark_pipeline_framework.pipelines.framework_pipeline import FrameworkPipeline
from spark_pipeline_framework.progress_logger.progress_logger import ProgressLogger
from spark_pipeline_framework.transformers.framework_csv_loader import FrameworkCsvLoader
from spark_pipeline_framework.utilities.attr_dict import AttrDict
from spark_pipeline_framework.utilities.flattener import flatten


class PatientPipeline(FrameworkPipeline):
    def __init__(self, parameters: AttrDict, progress_logger: ProgressLogger):
        super(PatientPipeline, self).__init__(parameters=parameters,
                                              progress_logger=progress_logger)
        self.transformers = flatten([
            [
                FrameworkCsvLoader(
                    view="patients",
                    path_to_csv=parameters["patient_csv"]
                ),
                FrameworkCsvLoader(
                    view="diagnosis",
                    path_to_csv=parameters["diagnosis_csv"]
                )
            ]
        ])
