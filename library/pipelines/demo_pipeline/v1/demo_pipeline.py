from typing import Dict, Any

from spark_pipeline_framework.pipelines.framework_pipeline import FrameworkPipeline
from spark_pipeline_framework.progress_logger.progress_logger import ProgressLogger
from spark_pipeline_framework.transformers.framework_csv_loader import FrameworkCsvLoader
from spark_pipeline_framework.utilities.attr_dict import AttrDict
from spark_pipeline_framework.utilities.flattener import flatten

from library.data_sources.diabetes_codes.data_sources_diabetes_codes import DataSourcesDiabetesCodes
from library.data_sources.icd_lookup.data_sources_icd_lookup import DataSourcesIcdLookup
from library.features.demo.diabetes_flg.features_demo_diabetes_flg import FeaturesDemoDiabetesFlg
from library.features.demo.patient_diagnosis.features_demo_patient_diagnosis import FeaturesDemoPatientDiagnosis


class DemoPipeline(FrameworkPipeline):
    def __init__(self, parameters: Dict[str, Any], progress_logger: ProgressLogger) -> None:
        super(DemoPipeline, self).__init__(parameters=parameters,
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
            ],
            DataSourcesIcdLookup(parameters=parameters, progress_logger=progress_logger).transformers,
            FeaturesDemoPatientDiagnosis(parameters=parameters, progress_logger=progress_logger).transformers,
            DataSourcesDiabetesCodes(parameters=parameters, progress_logger=progress_logger).transformers,
            FeaturesDemoDiabetesFlg(parameters=parameters, progress_logger=progress_logger).transformers
        ])
