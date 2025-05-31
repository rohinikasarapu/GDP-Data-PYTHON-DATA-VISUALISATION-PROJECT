# GDP XY Plotter

This project is part of **Data Visualization - Module 2 Project 1** by **Rice University** (Coursera).
It uses **Python** and **Pygal** to read GDP data from a CSV file and generate XY line plots for selected countries over a range of years.

## 📌 Project Description

The goal of this project is to:

* Read GDP data for various countries from a CSV file.
* Allow selection of specific countries.
* Extract and format GDP data for valid years.
* Visualize GDP trends using an XY line chart created with Pygal.
* Output the plot as an SVG file.

## 📊 Features

* Load and parse CSV GDP data with proper quoting and separators.
* Support for user-defined minimum and maximum year ranges.
* Clean error handling for invalid data points.
* Generates high-quality SVG plots using Pygal.
* Handles missing countries gracefully by displaying empty plots.

## 🛠️ Technologies Used

* **Python 3**
* **CSV module** – for reading structured data
* **Pygal** – for rendering SVG-based interactive plots

## 📁 File Structure

```
gdp_plot.py         # Main Python script
isp_gdp.csv         # Sample input CSV file (not included here)
README.md           # Project documentation
```

## 🧪 How to Run

1. Install `pygal` if not already installed:

   ```bash
   pip install pygal
   ```

2. Place your GDP CSV file in the same directory (e.g., `isp_gdp.csv`).

3. Make sure to edit the `gdpinfo` dictionary in the script to match your CSV structure if necessary.

4. Run the script and generate the plots:

   ```python
   # Uncomment the test call to run:
   test_render_xy_plot()
   ```

5. SVG files will be created such as:

   * `isp_gdp_xy_none.svg`
   * `isp_gdp_xy_china.svg`
   * `isp_gdp_xy_uk+usa.svg`

## 📌 Sample Plot

> ![Sample Output](sample_plot.svg)
> *(Replace with actual image link if hosted)*

## 🗏️ Credits

* Project developed as part of the **"Data Visualization" specialization by Rice University** on Coursera.
* Developed using concepts taught in Module 2: *Working with CSV and plotting GDP trends*.

---

Feel free to contribute or raise issues if you're extending the project!
