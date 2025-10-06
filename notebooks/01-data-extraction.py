import marimo

__generated_with = "0.16.5"
app = marimo.App(width="medium")


@app.cell
def _():
    import json
    import polars as pl
    from typing import Optional, Dict, Any, List

    from pathlib import Path
    import zipfile
    import os
    import gc

    import marimo as mo

    import logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    return Any, Dict, Optional, Path, gc, json, logger, mo, os, pl, zipfile


@app.cell
def _():
    CZECH_DIACRITIC_MAP = {
        # Lowercase vowels
        'á': 'a', 'à': 'a', 'ä': 'a', 'â': 'a', 'ǎ': 'a', 'ă': 'a', 'ā': 'a',
        'é': 'e', 'è': 'e', 'ě': 'e', 'ë': 'e', 'ê': 'e', 'ē': 'e', 'ė': 'e',
        'í': 'i', 'ì': 'i', 'ï': 'i', 'î': 'i', 'ī': 'i', 'ĭ': 'i',
        'ó': 'o', 'ò': 'o', 'ö': 'o', 'ô': 'o', 'ō': 'o', 'ŏ': 'o', 'ő': 'o',
        'ú': 'u', 'ù': 'u', 'ů': 'u', 'ü': 'u', 'û': 'u', 'ū': 'u', 'ŭ': 'u',
        'ý': 'y', 'ÿ': 'y', 'ŷ': 'y',

        # Lowercase consonants
        'č': 'c', 'ć': 'c', 'ç': 'c', 'ĉ': 'c',
        'ď': 'd', 'đ': 'd',
        'ň': 'n', 'ń': 'n', 'ñ': 'n',
        'ř': 'r', 'ŕ': 'r',
        'š': 's', 'ś': 's', 'ş': 's', 'ŝ': 's',
        'ť': 't', 'ţ': 't', 'ŧ': 't',
        'ž': 'z', 'ź': 'z', 'ż': 'z',
        'ľ': 'l', 'ĺ': 'l', 'ł': 'l',

        # Uppercase vowels
        'Á': 'A', 'À': 'A', 'Ä': 'A', 'Â': 'A', 'Ǎ': 'A', 'Ă': 'A', 'Ā': 'A',
        'É': 'E', 'È': 'E', 'Ě': 'E', 'Ë': 'E', 'Ê': 'E', 'Ē': 'E', 'Ė': 'E',
        'Í': 'I', 'Ì': 'I', 'Ï': 'I', 'Î': 'I', 'Ī': 'I', 'Ĭ': 'I',
        'Ó': 'O', 'Ò': 'O', 'Ö': 'O', 'Ô': 'O', 'Ō': 'O', 'Ŏ': 'O', 'Ő': 'O',
        'Ú': 'U', 'Ù': 'U', 'Ů': 'U', 'Ü': 'U', 'Û': 'U', 'Ū': 'U', 'Ŭ': 'U',
        'Ý': 'Y', 'Ÿ': 'Y', 'Ŷ': 'Y',

        # Uppercase consonants
        'Č': 'C', 'Ć': 'C', 'Ç': 'C', 'Ĉ': 'C',
        'Ď': 'D', 'Đ': 'D',
        'Ň': 'N', 'Ń': 'N', 'Ñ': 'N',
        'Ř': 'R', 'Ŕ': 'R',
        'Š': 'S', 'Ś': 'S', 'Ş': 'S', 'Ŝ': 'S',
        'Ť': 'T', 'Ţ': 'T', 'Ŧ': 'T',
        'Ž': 'Z', 'Ź': 'Z', 'Ż': 'Z',
        'Ľ': 'L', 'Ĺ': 'L', 'Ł': 'L'
    }
    return (CZECH_DIACRITIC_MAP,)


@app.cell
def _(
    Any,
    CZECH_DIACRITIC_MAP,
    Dict,
    Optional,
    Path,
    json,
    logger,
    os,
    pl,
    validate,
    zipfile,
):
    def remove_diacritics(text: str) -> str:
        """
        Remove diacritics from a string.
        """
        if not isinstance(text, str):
            return text

        return ''.join(CZECH_DIACRITIC_MAP.get(char, char) for char in text)

    def remove_diacritics_from_object(obj: Any, process_keys: bool = False) -> Any:
        """
        Recursively remove diacritics from all string values in an object.
        """
        if obj is None:
            return obj

        if isinstance(obj, str):
            return remove_diacritics(obj)

        if isinstance(obj, list):
            return [remove_diacritics_from_object(item, process_keys) for item in obj]

        if isinstance(obj, dict):
            result = {}
            for key, value in obj.items():
                new_key = remove_diacritics(key) if process_keys else key
                result[new_key] = remove_diacritics_from_object(value, process_keys)
            return result

        # For other types (int, float, bool, etc.), return as is
        return obj

    def _extract_registration_record(
        region: Dict[str, Any],
        locality: Dict[str, Any],
        substance: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Extract a single registration record from nested dictionaries.
        """
        registration_dict = {}

        # Extract region info
        registration_dict['RegionCode'] = region.get('Code')
        registration_dict['RegionName'] = region.get('Name')

        # Extract locality info
        registration_dict['LocalityCode'] = locality.get('Code')
        registration_dict['LocalityName'] = locality.get('Name')

        # Extract owner info
        owner = locality.get('Owner', {})
        registration_dict['OwnerAbbrev'] = owner.get('Abbrev')
        registration_dict['OwnerName'] = owner.get('Name')

        # Extract coordinates
        coordinates = locality.get('geometry', {}).get('coordinates', [])
        if len(coordinates) >= 3:
            registration_dict['Longitude'] = coordinates[0]
            registration_dict['Latitude'] = coordinates[1]   
            registration_dict['Altitude'] = coordinates[2]
        else:
            registration_dict['Longitude'] = None
            registration_dict['Latitude'] = None
            registration_dict['Altitude'] = None
            if validate:
                logger.debug(f"Missing coordinates for locality {locality.get('Name')}")

        # Extract CRS information
        crs_properties = locality.get('crs', {}).get('properties', {})
        registration_dict['CoordinateReferenceSystem'] = crs_properties.get('name')

        # Extract classification
        registration_dict['Classification'] = locality.get('Classification')

        # Extract substance/measurement info
        registration_dict['SubstanceId'] = substance.get('Id')

        component = substance.get('Component', {})
        registration_dict['SubstanceAbbrev'] = component.get('Abbrev')
        registration_dict['SubstanceName'] = component.get('Name')
        registration_dict['SubstanceUnit'] = component.get('Unit')

        # Extract measurement intervals
        registration_dict['DataInterval'] = substance.get('DataInterval')
        registration_dict['SamplingInterval'] = substance.get('SamplingInterval')

        # Extract measurement method
        measure_method = substance.get('MeasureMethod', {})
        registration_dict['MeasureMethodAbbrev'] = measure_method.get('Abbrev')
        registration_dict['MeasureMethodName'] = measure_method.get('Name')

        # Extract active period
        registration_dict['ActiveFrom'] = substance.get('ActiveFrom')
        registration_dict['ActiveTo'] = substance.get('ActiveTo')

        return registration_dict

    def extract_registration_list(
        input_path: Path = None,
        output_path: Path = None,
        write_data: bool = True
    ) -> pl.DataFrame:
        """
        Extract meteostation registration information from JSON for a specific year.
        """
        try:
            logger.info(f"Loading registration data from {input_path}")
            with open(input_path, 'r', encoding='utf-8-sig') as f:
                registration_data = json.load(f)
        except FileNotFoundError:
            error_msg = f"Registration file not found: {input_path}"
            logger.error(error_msg)
            raise FileNotFoundError(error_msg)
        except json.JSONDecodeError as e:
            error_msg = f"Invalid JSON in registration file: {e}"
            logger.error(error_msg)
            raise ValueError(error_msg)

        # Extract and flatten data
        registration_list = []
        error_count = 0

        # Check for required top-level structure
        if 'RegionList' not in registration_data:
            raise ValueError("Missing 'RegionList' in registration data")

        for region in registration_data['RegionList']:
            for locality in region.get('LocalityList', []):
                for substance in locality.get('RegistrationList', []):
                    try:
                        registration_dict = _extract_registration_record(
                            region, locality, substance
                        )
                        registration_dict_sanitized = remove_diacritics_from_object(registration_dict)
                        if registration_dict_sanitized:
                            registration_list.append(registration_dict_sanitized)
                    except Exception as e:
                        error_count += 1
                        logger.warning(
                            f"Error extracting record for {locality.get('Name', 'Unknown')}: {e}"
                        )
                        if error_count > 100:  # Fail if too many errors
                            raise ValueError(f"Too many extraction errors ({error_count})")

        if not registration_list:
            logger.warning("No registration records were extracted")
            return pl.DataFrame()  # Return empty DataFrame with no schema

        df_registration = pl.DataFrame(registration_list)
        logger.info(f"Successfully extracted {len(df_registration)} registration records")

        if write_data:
            try:
                df_registration.write_csv(output_path)
                logger.info(f"Data saved to {output_path}")
            except Exception as e:
                logger.error(f"Failed to save data: {e}")
                raise

        return df_registration

    def extract_data_paths(dir_path: str, file_pattern: str) -> list:
        '''Extract data paths from a directory according to pattern.'''
        directory_path = Path(dir_path)
        file_pattern = file_pattern

        data_paths = []
        for dir in directory_path.iterdir():
            if dir.is_dir():
                for file in dir.iterdir():
                    if file.match(path_pattern=file_pattern):
                        data_paths.append(file)

        return data_paths

    def unzip_and_delete(folder):
        '''Unzip and delete zipped folders.'''
        # Extract the zip file
        try:
            with zipfile.ZipFile(folder, 'r') as zip_ref:
                # Extract to subfolder named after the zip
                extract_to = Path(str(folder)[:-4])
                zip_ref.extractall(extract_to)
                print(f"Extracted: {folder}")

            # Delete the zip file after successful extraction
            os.remove(folder)
            print(f"Deleted: {folder}")

        except Exception as e:
            print(f"Error with {folder}: {e}")
    return (
        extract_data_paths,
        extract_registration_list,
        remove_diacritics,
        unzip_and_delete,
    )


@app.cell
def _(extract_data_paths, extract_registration_list, mo):
    mo.stop(predicate=True)
    # one-time extraction of registrations lists
    registration_data_paths = extract_data_paths(dir_path='./data/raw/', file_pattern='*.json')

    for registration_path in registration_data_paths:
        year = str(registration_path)[9:13]
        extract_registration_list(input_path=registration_path, output_path=f'./data/interim/{year}_registration_list.csv', write_data=True)
    return


@app.cell
def _(extract_data_paths, mo, unzip_and_delete):
    mo.stop(predicate=True)
    # one-time unzip and delete zipped folders
    zip_file_data_paths = extract_data_paths(dir_path='./data/raw/', file_pattern='*.zip')
    for zipped_folder in zip_file_data_paths:
        unzip_and_delete(zipped_folder)
    return


@app.cell
def _(Path, extract_data_paths, mo):
    mo.stop(predicate=True)
    # one-time rename and move of required data files
    for folder in Path('./data/raw/').iterdir():
        if folder.is_dir():
            data_file_data_paths = extract_data_paths(dir_path=folder, file_pattern='data.csv')
            value_type_file_data_paths = extract_data_paths(dir_path=folder, file_pattern='ValueType.csv')

        data_file_target_names = [Path('./data/interim/' + str(x).split('/')[3] + '_' + str(x).split('/')[4]) for x in data_file_data_paths]
        value_type_file_target_names = [Path('./data/interim/' + str(x).split('/')[3] + '_' + str(x).split('/')[4]) for x in value_type_file_data_paths]

        for data_file_data_path, data_file_target_name in zip(data_file_data_paths, data_file_target_names):
            try:
                data_file_data_path.rename(data_file_target_name)
            except FileNotFoundError as e:
                print(e)
        for value_type_file_data_path, value_type_file_target_name in zip(value_type_file_data_paths, value_type_file_target_names):
            try:
                value_type_file_data_path.rename(value_type_file_target_name)
            except FileNotFoundError as e:
                print(e)
    return


@app.cell
def _(extract_data_paths, mo, pl, remove_diacritics):
    mo.stop(predicate=True)
    # one-time remove diacritics from value type files
    moved_value_types = extract_data_paths(dir_path='./data/', file_pattern='*_ValueType.csv')

    for moved_value_type in moved_value_types:
        moved_file = pl.read_csv(moved_value_type)
        for column in moved_file.columns:
            if moved_file[column].dtype == pl.Utf8:  # String columns in Polars
                moved_file = moved_file.with_columns(
                    pl.col(column).map_elements(
                        lambda x: remove_diacritics(x) if x is not None else None,
                        return_dtype=pl.Utf8
                    ).alias(column)
                )

        moved_file.write_csv(moved_value_type)
    return


@app.cell
def _(extract_data_paths, mo, pl):
    mo.stop(predicate=True)
    # one-time add substance-place-id to required data
    moved_data_files = extract_data_paths(dir_path='./data/', file_pattern='*_data.csv')

    for moved_data in moved_data_files:
        moved_data_file = pl.read_csv(moved_data, schema_overrides={'VALUE': pl.Float64})

        sub_place_year_id = str(moved_data).split('_')[1]

        moved_data_file = moved_data_file.with_columns(pl.lit(sub_place_year_id).alias('SUB_PLACE_YEAR_ID'))

        moved_data_file.write_csv(moved_data)
    return


@app.cell
def _(extract_data_paths, mo, pl):
    mo.stop(predicate=True)
    # one-time merge of data, value type and registration files
    sub_place_year_paths = sorted(extract_data_paths(dir_path='./data/', file_pattern='*_data.csv'))
    registration_list_paths = sorted(extract_data_paths(dir_path='./data/', file_pattern='*_registration_list.csv'))
    value_type_paths = sorted(extract_data_paths(dir_path='./data/', file_pattern='*_ValueType.csv'))

    merged_count = 0

    for rl_path in registration_list_paths:
        yr = rl_path.name[:4]  

        print(f"\nProcessing registration year: {yr} from {rl_path.name}")

        try:
            rl_data = pl.read_csv(rl_path)
            print(f"  Loaded registration data: {len(rl_data)} rows")
        except Exception as e:
            print(f"  ERROR loading {rl_path}: {e}")
            continue

        # Look for matching spy and vt files
        for spy_path, vt_path in zip(sub_place_year_paths, value_type_paths):

            spy_filename = spy_path.name
            substance = spy_filename.split('_')[1]
            year_sub = f"{yr}_{substance}"

            # Check if this combination matches both files
            if year_sub in spy_filename and year_sub in vt_path.name:
                print(f"  Found match: {year_sub}")
                print(f"    SPY: {spy_filename}")
                print(f"    VT: {vt_path.name}")

                try:
                    spy_data = pl.read_csv(spy_path)
                    vt_data = pl.read_csv(vt_path)

                    print(f"    SPY data: {len(spy_data)} rows, columns: {spy_data.columns}")
                    print(f"    VT data: {len(vt_data)} rows, columns: {vt_data.columns}")

                    merged_df = (
                        spy_data
                        .join(rl_data, left_on='SUB_PLACE_YEAR_ID', right_on='SubstanceId', how='left')
                        .join(vt_data, on='ID_VALUE_TYPE', how='left')
                    )

                    output_file = f'./data/processed/{year_sub}_merged_data.parquet'
                    merged_df.write_parquet(output_file)
                    print(f"    SUCCESS: Saved {output_file} with {len(merged_df)} rows")
                    merged_count += 1

                except Exception as e:
                    print(f"    ERROR during merge: {e}")

    print(f"\n{'='*50}")
    print(f"Total files merged: {merged_count}")
    return


@app.cell
def _(Path, extract_data_paths, gc, mo, pl):
    mo.stop(predicate=True)
    years = pl.int_range(1969, 2025, eager=True)
    paths = []
    for y in years:
        target_file = Path(f'./data/processed/{y}_historical_meteodata.parquet')
        if not target_file.exists():
            print(f'Output file {target_file} does not exist. Preparing...')
            paths.extend(extract_data_paths(dir_path='./data/', file_pattern=f'{y}_*_merged_data.parquet'))
            dfs = [pl.read_parquet(path) for path in paths]
            combined_df = pl.concat(dfs, how='vertical')
            print(f'Files for year {y} were combined.')
            combined_df.write_parquet(f'./data/processed/{y}_historical_meteodata.parquet')
            print(f'SUCCESS: Files for year {y} were written in a parquet file.')

            # Clean up memory
            del dfs
            del combined_df
            gc.collect()
    return


@app.cell
def _(Path, extract_data_paths, mo, pl):
    mo.stop(predicate=True)
    target_file_pattern = extract_data_paths(dir_path='./data/', file_pattern=f'./data/processed/*_historical_meteodata.parquet')
    output_file_final = Path('./data/processed/alltime_historical_meteodata.parquet')

    # Process all files using lazy concat and sink
    lazy_dfs = [pl.scan_parquet(path) for path in target_file_pattern]
    combined_lazy = pl.concat(lazy_dfs, how='vertical')

    # Stream to disk without loading into memory
    combined_lazy.sink_parquet(output_file_final)
    print('All files combined successfully')
    return


@app.cell
def _(mo, pl):
    mo.stop(predicate=True)
    ozon = pl.scan_parquet('./data/processed/alltime_historical_meteodata.parquet').filter(
        (pl.col('SubstanceAbbrev') == 'O3') & (pl.col('SubstanceName') == 'ozon') & (pl.col('NAME') == 'Verifikovana data')
    )

    df_renamed = ozon.rename(mapping={'START_TIME': 'measurement_date', 'ID_VALUE_TYPE': 'value_type_id', 'VALUE': 'ozone_level', 'SUB_PLACE_YEAR_ID': 'substance_place_year_id', 'RegionCode': 'region_code', 'RegionName': 'region_name', 'LocalityCode': 'locality_code', 'LocalityName': 'locality_name', 'OwnerName': 'owner_name', 'Longitude': 'longitude', 'Latitude': 'latitude', 'Altitude': 'altitude', 'CoordinateReferenceSystem': 'crs', 'Classification': 'locality_classification', 'SubstanceAbbrev': 'substance_abbrev', 'SubstanceName': 'substance_name', 'SubstanceUnit': 'measurement_units', 'DataInterval': 'data_interval', 'SamplingInterval': 'sampling_interval', 'MeasureMethodAbbrev': 'measure_method_abbrev', 'MeasureMethodName': 'measure_method_name', 'ActiveFrom': 'active_from', 'ActiveTo': 'active_to', 'NAME': 'data_quality_flag'})

    df_renamed.sink_parquet('./data/processed/alltime_historical_ozon.parquet')
    return


if __name__ == "__main__":
    app.run()
