import csv
import pygal


def read_csv_as_nested_dict(filename, keyfield, separator, quote):
    """
    Inputs:
      filename  - Name of CSV file
      keyfield  - Field to use as key for rows
      separator - Character that separates fields
      quote     - Character used to optionally quote fields

    Output:
      Returns a dictionary of dictionaries where the outer dictionary
      maps the value in the key_field to the corresponding row in the
      CSV file. The inner dictionaries map the field names to the
      field values for that row.
    """
    table = {}
    with open(filename, 'r', newline='') as csvfile:  # Added newline='' for universal newlines
        reader = csv.DictReader(csvfile, delimiter=separator, quotechar=quote)
        for row in reader:
            # DictReader already returns a dictionary, so 'row' is already what we need.
            table[row[keyfield]] = row
    return table


def build_plot_values(gdpinfo, gdpdata):
    """
    Inputs:
      gdpinfo - GDP data information dictionary
      gdpdata - A single country's GDP stored in a dictionary whose
                keys are strings indicating a year and whose values
                are strings indicating the country's corresponding GDP
                for that year.

    Output:
      Returns a list of tuples of the form (year, GDP) for the years
      between "min_year" and "max_year", inclusive, from gdpinfo that
      exist in gdpdata. The year will be an integer and the GDP will
      be a float.
    """
    result = []
    min_year = gdpinfo.get("min_year")
    max_year = gdpinfo.get("max_year")

    for year in range(min_year, max_year + 1):
        year_str = str(year)
        if year_str in gdpdata:  # Check if the year exists in the gdpdata dictionary
            gdp_value_str = gdpdata[year_str].strip()  # Get value and strip whitespace
            if gdp_value_str:  # Ensure the string is not empty
                try:
                    # Convert GDP to float, year to int
                    result.append((year, float(gdp_value_str)))
                except ValueError:
                    # If conversion fails (e.g., non-numeric data), skip this entry
                    continue
    return result


def build_plot_dict(gdpinfo, country_list):
    """
    Inputs:
      gdpinfo     - GDP data information dictionary
      country_list - List of strings that are country names

    Output:
      Returns a dictionary whose keys are the country names in
      country_list and whose values are lists of XY plot values
      computed from the CSV file described by gdpinfo.

      Countries from country_list that do not appear in the
      CSV file should still be in the output dictionary, but
      with an empty XY plot value list.
    """
    final = {}
    # Read the GDP file once to get all country data
    all_gdp_data = read_csv_as_nested_dict(gdpinfo.get("gdpfile"),
                                           gdpinfo.get("country_name"),
                                           gdpinfo.get("separator"),
                                           gdpinfo.get("quote"))

    for country in country_list:
        country_gdp_data = all_gdp_data.get(country)
        if country_gdp_data:
            # If country data exists, build plot values for it
            final[country] = build_plot_values(gdpinfo, country_gdp_data)
        else:
            # If country not found, add with an empty list
            final[country] = []
    return final


def render_xy_plot(gdpinfo, country_list, plot_file):
    """
    Inputs:
      gdpinfo      - GDP data information dictionary
      country_list - List of strings that are country names
      plot_file    - String that is the output plot file name

    Output:
      Returns None.

    Action:
      Creates an SVG image of an XY plot for the GDP data
      specified by gdpinfo for the countries in country_list.
      The image will be stored in a file named by plot_file.
    """
    gdp_chart = pygal.XY(
        title=f'Plot of GDP for select countries spanning {gdpinfo["min_year"]} to {gdpinfo["max_year"]}',
        x_title='Year',  # Added X-axis title for clarity
        y_title='GDP in current US dollars'
    )

    # Build the plot data dictionary once
    plot_data_dict = build_plot_dict(gdpinfo, country_list)

    for country in country_list:
        # Get the pre-computed data from the dictionary
        data_to_plot = plot_data_dict.get(country, [])
        gdp_chart.add(country, data_to_plot)

    # gdp_chart.render_in_browser() # Commented out as per project instructions
    gdp_chart.render_to_file(plot_file)


def test_render_xy_plot():
    """
    Code to exercise render_xy_plot and generate plots from
    actual GDP data.
    """
    gdpinfo = {
        "gdpfile": "isp_gdp.csv",
        "separator": ",",
        "quote": '"',
        "min_year": 1960,
        "max_year": 2015,
        "country_name": "Country Name",
        "country_code": "Country Code"
    }

    print("Generating plots...")
    render_xy_plot(gdpinfo, [], "isp_gdp_xy_none.svg")
    render_xy_plot(gdpinfo, ["China"], "isp_gdp_xy_china.svg")
    render_xy_plot(gdpinfo, ["United Kingdom", "United States"],
                   "isp_gdp_xy_uk+usa.svg")
    print("Plots generated successfully!")


# Make sure the following call to test_render_xy_plot is commented out
# when submitting to OwlTest/CourseraTest.

# test_render_xy_plot()