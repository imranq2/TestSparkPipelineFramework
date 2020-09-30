from os import path
from pathlib import Path
from shutil import rmtree

from pyspark.sql.dataframe import DataFrame
from pyspark.sql.session import SparkSession
from pyspark.sql.types import StructType
from spark_pipeline_framework.progress_logger.progress_logger import ProgressLogger
from spark_pipeline_framework.utilities.attr_dict import AttrDict

from library.pipelines.demo_pipeline.v1.demo_pipeline import DemoPipeline


def test_can_run_demo_pipeline(spark_session: SparkSession):
    # Arrange
    data_dir: Path = Path(__file__).parent.joinpath('./')
    patient_csv: str = f"file://{data_dir.joinpath('patient.csv')}"
    diagnosis_csv: str = f"file://{data_dir.joinpath('diagnosis.csv')}"

    temp_folder = data_dir.joinpath('temp')
    if path.isdir(temp_folder):
        rmtree(temp_folder)

    schema = StructType([])

    df: DataFrame = spark_session.createDataFrame(
        spark_session.sparkContext.emptyRDD(), schema)
    # Act
    parameters = AttrDict(
        {
            "patient_csv": patient_csv,
            "diagnosis_csv": diagnosis_csv
        }
    )

    with ProgressLogger() as progress_logger:
        pipeline: DemoPipeline = DemoPipeline(parameters=parameters, progress_logger=progress_logger)
        transformer = pipeline.fit(df)
        transformer.transform(df)

    # Assert
    result_df: DataFrame = spark_session.sql("SELECT * FROM patients")
    result_df.show(truncate=False)

    assert result_df.count() > 0
