import marimo

__generated_with = "0.16.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import json
    import polars as pl
    from typing import Optional, Dict, Any, List

    from pathlib import Path

    import marimo as mo

    import logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    return Any, Dict, Optional, Path, json, logger, pl


@app.cell
def _(Any, Dict, Optional, Path, json, logger, pl, validate):
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
            with open(input_path, 'r', encoding='utf-8') as f:
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
                        if registration_dict:
                            registration_list.append(registration_dict)
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
    return (extract_registration_list,)


@app.cell
def _(Path, extract_registration_list):
    directory_path = Path('./data/raw/')
    file_pattern = '*.json'

    data_paths = []
    for dir in directory_path.iterdir():
        if dir.is_dir():
            for file in dir.iterdir():
                if file.match(path_pattern=file_pattern):
                    data_paths.append(file)

    for path in data_paths:
        year = str(path)[9:13]
        extract_registration_list(input_path=path, output_path=f'./data/interim/{year}_registration_list.csv', write_data=True)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
