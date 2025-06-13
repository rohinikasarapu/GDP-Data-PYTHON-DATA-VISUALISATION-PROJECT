"""
Project for Week 3 of "Python Data Visualization".
Unify data via common country name.

Be sure to read the project description page for further information
about the expected behavior of the program.

"""

import csv
import math
import pygal


# --- Functions from previous weeks (re-included for self-containment) ---

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
    with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=separator, quotechar=quote)
        for row in reader:
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
        if year_str in gdpdata:
            gdp_value_str = gdpdata[year_str].strip()
            if gdp_value_str:
                try:
                    result.append((year, float(gdp_value_str)))
                except ValueError:
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
    all_gdp_data = read_csv_as_nested_dict(gdpinfo.get("gdpfile"),
                                           gdpinfo.get("country_name"),
                                           gdpinfo.get("separator"),
                                           gdpinfo.get("quote"))

    for country in country_list:
        country_gdp_data = all_gdp_data.get(country)
        if country_gdp_data:
            final[country] = build_plot_values(gdpinfo, country_gdp_data)
        else:
            final[country] = []
    return final

# --- End of functions from previous weeks ---


def reconcile_countries_by_name(plot_countries, gdp_countries):
    """
    Inputs:
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      gdp_countries  - Dictionary whose keys are country names used in GDP data

    Output:
      A tuple containing a dictionary and a set. The dictionary maps
      country codes from plot_countries to country names from
      gdp_countries. The set contains the country codes from
      plot_countries that were not found in gdp_countries.
    """
    matched_countries = {}
    unmatched_plot_codes = set()

    for code, name in plot_countries.items():
        if name in gdp_countries:
            matched_countries[code] = name
        else:
            unmatched_plot_codes.add(code)

    return (matched_countries, unmatched_plot_codes)


def build_map_dict_by_name(gdpinfo, plot_countries, year):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      year           - String year to create GDP mapping for

    Output:
      A tuple containing a dictionary and two sets. The dictionary
      maps country codes from plot_countries to the log (base 10) of
      the GDP value for that country in the specified year. The first
      set contains the country codes from plot_countries that were not
      found in the GDP data file. The second set contains the country
      codes from plot_countries that were found in the GDP data file, but
      have no GDP data for the specified year.
    """
    gdp_data_map = {}
    missing_from_gdp_file = set()
    no_gdp_data_for_year = set()

    # Read the entire GDP file once
    all_gdp_data = read_csv_as_nested_dict(gdpinfo["gdpfile"],
                                           gdpinfo["country_name"],
                                           gdpinfo["separator"],
                                           gdpinfo["quote"])

    # Reconcile plot_countries with the country names present in all_gdp_data
    reconciled_names, not_in_gdp_data_overall = \
        reconcile_countries_by_name(plot_countries, all_gdp_data)

    missing_from_gdp_file.update(not_in_gdp_data_overall)

    for plot_code, gdp_country_name in reconciled_names.items():
        country_record = all_gdp_data.get(gdp_country_name)

        if country_record:
            gdp_value_str = country_record.get(year, '').strip()

            if gdp_value_str:
                try:
                    gdp_value = float(gdp_value_str)
                    if gdp_value > 0:
                        gdp_data_map[plot_code] = math.log10(gdp_value)
                    else:
                        no_gdp_data_for_year.add(plot_code)
                except ValueError:
                    no_gdp_data_for_year.add(plot_code)
            else:
                no_gdp_data_for_year.add(plot_code)
        else:
            # This case should ideally be covered by reconcile_countries_by_name
            # but as a safeguard, add to missing.
            missing_from_gdp_file.add(plot_code)

    return (gdp_data_map, missing_from_gdp_file, no_gdp_data_for_year)


def render_world_map(gdpinfo, plot_countries, year, map_file):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      year           - String year to create GDP mapping for
      map_file       - Name of output file to create

    Output:
      Returns None.

    Action:
      Creates a world map plot of the GDP data for the given year and
      writes it to a file named by map_file.
    """
    worldmap_chart = pygal.maps.world.World()
    worldmap_chart.title = (f'GDP by country for {year} (log scale), '
                            'unified by common country NAME')

    # Get the data for the map once
    gdp_data_map, missing_from_gdp_file, no_gdp_data_for_year = \
        build_map_dict_by_name(gdpinfo, plot_countries, year)

    worldmap_chart.add(f'GDP For {year}', gdp_data_map)
    worldmap_chart.add('Missing from World Bank Data', missing_from_gdp_file)
    worldmap_chart.add('No GDP Data', no_gdp_data_for_year)

    # For CodeSkulptor, you might need to use render_in_browser()
    # for local testing, but for submission, render_to_file() is typical.
    # worldmap_chart.render_in_browser()
    worldmap_chart.render_to_file(map_file)


def test_render_world_map():
    """
    Test the project code for several years.
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

    # Get pygal country code map
    pygal_countries = pygal.maps.world.COUNTRIES

    print("Generating plots...")
    # 1960
    render_world_map(gdpinfo, pygal_countries, "1960", "isp_gdp_world_name_1960.svg")

    # 1980
    render_world_map(gdpinfo, pygal_countries, "1980", "isp_gdp_world_name_1980.svg")

    # 2000
    render_world_map(gdpinfo, pygal_countries, "2000", "isp_gdp_world_name_2000.svg")

    # 2010
    render_world_map(gdpinfo, pygal_countries, "2010", "isp_gdp_world_name_2010.svg")
    print("Plots generated successfully!")


# Make sure the following call to test_render_world_map is commented
# out when submitting to OwlTest/CourseraTest.

# test_render_world_map()
