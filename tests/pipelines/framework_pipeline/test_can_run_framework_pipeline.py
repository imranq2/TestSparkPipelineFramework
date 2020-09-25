from pathlib import Path

from pyspark.sql.dataframe import DataFrame
from pyspark.sql.session import SparkSession
from pyspark.sql.types import StructType
from spark_pipeline_framework.pipelines.framework_pipeline import FrameworkPipeline
from spark_pipeline_framework.progress_logger.progress_logger import ProgressLogger
from spark_pipeline_framework.transformers.framework_csv_loader import FrameworkCsvLoader
from spark_pipeline_framework.utilities.attr_dict import AttrDict
from spark_pipeline_framework.utilities.flattener import flatten

from library.features.flightpaths.features_flightpaths import FeaturesFlightpaths


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
            FeaturesFlightpaths(parameters=parameters).transformers,
        ])


def test_can_run_framework_pipeline(spark_session: SparkSession) -> None:
    # Arrange
    data_dir: Path = Path(__file__).parent.joinpath('./')
    flights_path: str = f"file://{data_dir.joinpath('flights.csv')}"

    schema = StructType([])

    df: DataFrame = spark_session.createDataFrame(
        spark_session.sparkContext.emptyRDD(), schema)

    spark_session.sql("DROP TABLE IF EXISTS default.flights")

    # Act
    parameters = AttrDict(
        {
            "flights_path": flights_path
        }
    )

    with ProgressLogger() as progress_logger:
        pipeline: MyPipeline = MyPipeline(parameters=parameters, progress_logger=progress_logger)
        transformer = pipeline.fit(df)
        transformer.transform(df)

    # Assert
    result_df: DataFrame = spark_session.sql("SELECT * FROM flights2")
    result_df.show()

    assert result_df.count() > 0