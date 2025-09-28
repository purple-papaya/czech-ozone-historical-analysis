import marimo

__generated_with = "0.16.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return


@app.cell
def _():
    import polars as pl
    import json
    return json, pl


@app.cell
def _(json, pl):
    # Parse and flatten nested JSON
    registration_dict = {}

    with open('./data/raw/1969/1969_RegistrationList.json', 'r') as f:
        registration_data = json.load(f)

        for region in registration_data['RegionList']:
            for locality in region['LocalityList']:
                for substance in locality['RegistrationList']:
                    # Extract region info
                    registration_dict['RegionCode'] = region['Code']
                    registration_dict['RegionName'] = region['Name']
    
                    # Extract locality info
                    registration_dict['LocalityCode'] = locality['Code']
                    registration_dict['LocalityName'] = locality['Name']
    
                    registration_dict['OwnerAbbrev'] = locality['Owner']['Abbrev']
                    registration_dict['OwnerName'] = locality['Owner']['Name']
    
                    registration_dict['Latitude'] = locality['geometry']['coordinates'][0]
                    registration_dict['Longitude'] = locality['geometry']['coordinates'][1]
                    registration_dict['Altitude'] = locality['geometry']['coordinates'][2]
    
                    registration_dict['CoordinateReferenceSystem'] = locality['crs']['properties']['name']
                    registration_dict['Classification'] = locality['Classification']

                    # Extract measured substances info
                    registration_dict['SubstanceId'] = substance['Id']
                    registration_dict['SubstanceAbbrev'] = substance['Component']['Abbrev']
                    registration_dict['SubstanceName'] = substance['Component']['Name']
                    registration_dict['SubstanceUnit'] = substance['Component']['Unit']

                    registration_dict['DataInterval'] = substance['DataInterval']
                    registration_dict['SamplingInterval'] = substance['SamplingInterval']

                    registration_dict['MeasureMethodAbbrev'] = substance['MeasureMethod']['Abbrev']
                    registration_dict['MeasureMethodName'] = substance['MeasureMethod']['Name']

                    registration_dict['ActiveFrom'] = substance['ActiveFrom']
                    registration_dict['ActiveTo'] = substance['ActiveTo']

        registration_dataframe = pl.DataFrame(data=registration_dict)
        registration_dataframe.write_csv('./data/raw/1969/1969_registration_list.csv')




            

    
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
