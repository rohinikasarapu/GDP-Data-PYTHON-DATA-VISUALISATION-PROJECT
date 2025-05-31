GDP Data Visualization Suite:
Welcome to the GDP Data Visualization Suite — a trio of Python projects designed to bring global GDP data to life through interactive line plots and colorful world maps! Whether you want to track economic growth over time or see how GDP is distributed across countries visually, this suite has got you covered.

🚀 Project 1: Create Line Plot Using GDP
What it does:
Watch GDP trends unfold across years for any country with smooth, elegant line plots.

Key Functions:

read_csv_as_nested_dict(filename, keyfield, separator, quote):
Reads CSV GDP data into a nested dictionary for easy lookup.

build_plot_values(gdpinfo, country, years):
Extracts GDP values for a given country over a range of years.

draw_line_plot(gdpinfo, countries):
Generates a comparative line plot showing GDP growth for multiple countries.

Why you’ll love it:
See the story of economic progress unfold visually — from booming giants to emerging economies — all on one chart.

🗺️ Project 2: Plot GDP on World Map by Country Name
What it does:
Paint the world map in shades of wealth, matching countries by their names.

Key Functions:

reconcile_countries_by_name(codeinfo, plot_countries):
Matches country names in GDP data with plotting library’s country names, handling tricky mismatches.

build_map_dict_by_name(gdpinfo, codeinfo, plot_countries, year):
Creates a dictionary mapping country codes to their GDP values for a specific year, based on name reconciliation.

render_world_map(gdpinfo, codeinfo, year, map_style):
Draws the world map with GDP data colored on a logarithmic scale for clarity.

Why you’ll love it:
Visualize global wealth disparities with a simple glance — countries bloom in colors representing their GDP.

🗺️ Project 3: Plot GDP on World Map by Country Code
What it does:
Show GDP on the world map by matching countries via their official country codes — precise and efficient.

Key Functions:

reconcile_countries_by_code(codeinfo, plot_countries):
Matches country codes from GDP data with those used in the plotting library.

build_map_dict_by_code(gdpinfo, codeinfo, plot_countries, year):
Builds a GDP dictionary keyed by country codes for fast and accurate mapping.

render_world_map(gdpinfo, codeinfo, year, map_style):
Displays the GDP data on the map using color scales, with unmatched countries flagged.

Why you’ll love it:
Accuracy meets beauty — explore a perfectly mapped world of economic data without name confusion.

🔧 Common Tools & Setup
Data files:

world_bank_gdp.csv — GDP data by country and year

isp_country_codes.csv — Country name and code mappings

Libraries used:
csv, pygal, math, matplotlib

How to run:

Load your GDP and country code files.

Call functions from your chosen project to parse and visualize data.

Enjoy beautiful, insightful graphs and maps!

🌟 Get Started!
Explore the power of data visualization and economic storytelling by running any of these projects. Dive deep into global GDP trends with just a few lines of Python.

Questions? Feature requests? Reach out anytime!

Author:rohini kasarapu
Contact: rohinikasarapu2110@gmail.com
