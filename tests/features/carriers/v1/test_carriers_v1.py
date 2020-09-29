from pathlib import Path

from pyspark.sql.dataframe import DataFrame
from pyspark.sql.session import SparkSession
from pyspark.sql.types import StructType
from spark_pipeline_framework.transformers.framework_csv_loader import FrameworkCsvLoader
from spark_pipeline_framework.utilities.attr_dict import AttrDict

from library.features.carriers.v1.features_carriers_v1 import FeaturesCarriersV1


def test_carriers_v1(spark_session: SparkSession):
    # Arrange
    data_dir: Path = Path(__file__).parent.joinpath('./')
    flights_path: str = f"file://{data_dir.joinpath('flights.csv')}"

    schema = StructType([])

    df: DataFrame = spark_session.createDataFrame(
        spark_session.sparkContext.emptyRDD(), schema)

    spark_session.sql("DROP TABLE IF EXISTS default.flights")

    FrameworkCsvLoader(
        view="flights",
        path_to_csv=flights_path
    ).transform(dataset=df)

    parameters = AttrDict({
    })

    FeaturesCarriersV1(parameters=parameters).transformers[0].transform(dataset=df)

    result_df: DataFrame = spark_session.sql("SELECT * FROM flights2")
    result_df.show()

    assert result_df.count() > 0
