import marimo

__generated_with = "0.16.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import polars as pl

    import marimo as mo
    return mo, pl


@app.cell
def _(pl):
    df_ozone = pl.scan_parquet('./data/processed/alltime_historical_ozon.parquet').unique()
    return (df_ozone,)


@app.cell
def _(df_ozone):
    df_ozone.head()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Inspect measurement_date""")
    return


@app.cell
def _(pl):
    datetime_column = pl.read_parquet('./data/processed/alltime_historical_ozon.parquet', columns=['measurement_date', 'locality_code'])
    return (datetime_column,)


@app.cell
def _(datetime_column, pl):
    min_date = datetime_column.min()
    max_date = datetime_column.max()
    interval = (
        datetime_column
            .with_columns(pl.col('measurement_date').str.to_datetime(time_zone='UTC'))
            .with_columns(
                year=pl.col('measurement_date').dt.year(),
                date=pl.col('measurement_date').dt.date()
            )
            .with_columns(
                diff_minutes=pl.col('measurement_date').diff().dt.total_minutes()
            )
            .group_by(['date', 'locality_code'])
            .agg([
                pl.first('year').alias('year'),  # Keep the year
                pl.len().alias('n_records_per_day'),
                pl.col('diff_minutes').median().alias('daily_median_diff')
            ])
            .group_by(['year', 'locality_code'])
            .agg([
                pl.len().alias('n_days'),
                pl.col('n_records_per_day').median().alias('median_records_per_day'),
                pl.col('daily_median_diff').median().alias('median_minutes_between_records')
            ])
            .sort('year')
    )
    return (interval,)


@app.cell
def _(interval):
    interval
    return


@app.cell
def _(datetime_column, pl):
    datetime_column.with_columns(pl.col('measurement_date').str.to_datetime(time_zone='UTC')).with_columns( year=pl.col('measurement_date').dt.year(), date=pl.col('measurement_date').dt.date()).with_columns(diff_minutes=pl.col('measurement_date').diff().dt.total_minutes().over('date')).group_by(['date', 'locality_code']).agg([
                pl.first('year').alias('year'),
                pl.len().alias('n_records_per_day'),
                pl.col('diff_minutes').median().alias('daily_median_diff')
            ])
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
