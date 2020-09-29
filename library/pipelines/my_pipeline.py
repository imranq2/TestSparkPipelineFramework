from spark_pipeline_framework.pipelines.framework_pipeline import FrameworkPipeline
from spark_pipeline_framework.progress_logger.progress_logger import ProgressLogger
from spark_pipeline_framework.transformers.framework_csv_loader import FrameworkCsvLoader
from spark_pipeline_framework.utilities.attr_dict import AttrDict
from spark_pipeline_framework.utilities.flattener import flatten

from library.features.carriers.v1.features_carriers_v1 import FeaturesCarriersV1


class MyPipeline(FrameworkPipeline):
    def __init__(self, parameters: AttrDict, progress_logger: ProgressLogger):
        super(MyPipeline, self).__init__(parameters=parameters,
                                         progress_logger=progress_logger)
        self.transformers = flatten([
            [
                FrameworkCsvLoader(
                    view="flights",
                    path_to_csv=parameters["flights_path"]
                )
            ],
            FeaturesCarriersV1(parameters=parameters).transformers,
        ])

