import marimo

__generated_with = "0.16.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import json
    import polars as pl
    from typing import Optional, Dict, Any, List

    from pathlib import Path
    import zipfile
    import os

    import marimo as mo

    import logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    return Any, Dict, Optional, Path, json, logger, os, pl, zipfile


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
    return extract_data_paths, extract_registration_list


@app.cell
def _(extract_data_paths, extract_registration_list):
    registration_data_paths = extract_data_paths(dir_path='./data/raw/', file_pattern='*.csv')

    for registration_path in registration_data_paths:
        year = str(registration_path)[9:13]
        extract_registration_list(input_path=registration_path, output_path=f'./data/interim/{year}_registration_list.csv', write_data=True)
    return


@app.cell
def _():
    # one-time unzip and delete zipped folders
    # zip_file_data_paths = extract_data_paths(dir_path='./data/raw/', file_pattern='*.zip')
    # for zipped_folder in zip_file_data_paths:
    #     unzip_and_delete(zipped_folder)
    return


@app.cell
def _():
    # one-time rename and move of required data files
    # for folder in Path('./data/raw/').iterdir():
    #     if folder.is_dir():
    #         data_file_data_paths = extract_data_paths(dir_path=folder, file_pattern='data.csv')
    #         value_type_file_data_paths = extract_data_paths(dir_path=folder, file_pattern='ValueType.csv')

    #     data_file_target_names = [Path('./data/interim/' + str(x).split('/')[3] + '_' + str(x).split('/')[4]) for x in data_file_data_paths]
    #     value_type_file_target_names = [Path('./data/interim/' + str(x).split('/')[3] + '_' + str(x).split('/')[4]) for x in value_type_file_data_paths]

    #     for data_file_data_path, data_file_target_name in zip(data_file_data_paths, data_file_target_names):
    #         try:
    #             data_file_data_path.rename(data_file_target_name)
    #         except FileNotFoundError as e:
    #             print(e)
    #     for value_type_file_data_path, value_type_file_target_name in zip(value_type_file_data_paths, value_type_file_target_names):
    #         try:
    #             value_type_file_data_path.rename(value_type_file_target_name)
    #         except FileNotFoundError as e:
    #             print(e)
        
    return


@app.cell
def _():
    # one-time remove diacritics from value type files
    # moved_value_types = extract_data_paths(dir_path='./data/', file_pattern='*_ValueType.csv')

    # for moved_value_type in moved_value_types:
    #     moved_file = pl.read_csv(moved_value_type)
    #     for column in moved_file.columns:
    #         if moved_file[column].dtype == pl.Utf8:  # String columns in Polars
    #             moved_file = moved_file.with_columns(
    #                 pl.col(column).map_elements(
    #                     lambda x: remove_diacritics(x) if x is not None else None,
    #                     return_dtype=pl.Utf8
    #                 ).alias(column)
    #             )
            
    #     moved_file.write_csv(moved_value_type)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
