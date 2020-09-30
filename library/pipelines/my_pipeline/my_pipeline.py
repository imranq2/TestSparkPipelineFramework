from typing import Dict, Any

# noinspection Mypy
from spark_pipeline_framework.pipelines.framework_pipeline import FrameworkPipeline
# noinspection Mypy
from spark_pipeline_framework.progress_logger.progress_logger import ProgressLogger
# noinspection Mypy
from spark_pipeline_framework.transformers.framework_csv_loader import FrameworkCsvLoader
# noinspection Mypy
from spark_pipeline_framework.transformers.framework_parquet_exporter import FrameworkParquetExporter
# noinspection Mypy
from spark_pipeline_framework.utilities.flattener import flatten

from library.features.carriers.v1.features_carriers_v1 import FeaturesCarriersV1


class MyPipeline(FrameworkPipeline):
    def __init__(self, parameters: Dict[str, Any], progress_logger: ProgressLogger):
        super(MyPipeline, self).__init__(parameters=parameters,
                                         progress_logger=progress_logger)
        self.transformers = flatten([
            [
                FrameworkCsvLoader(
                    view="flights",
                    path_to_csv=parameters["flights_path"]
                )
            ],
            FeaturesCarriersV1(parameters=parameters, progress_logger=progress_logger).transformers,
            FrameworkParquetExporter(
                view="flights2",
                file_path=parameters["export_path"],
                progress_logger=progress_logger
            )
        ])
