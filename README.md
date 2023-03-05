![cover photo](https://www.firstpost.com/wp-content/uploads/2022/07/shutterstock_1499350838-1-scaled-1.jpg)

### RENTER - Real Estate Price Prediction Tool

RENTER is a machine learning project that aims to predict the asking price of rental properties in Belgrade, Serbia.

RENTER finds the best deals on properties by identifying undervalued rentals. By predicting the asking price of a property, RENTER can estimate when a property is undervalued, i.e. predicted asking price is higher (by a certain margin) than the actual asking price.

The models are trained on the collected dataset to predict the asking price of a rental property, based on various features such as property location, size, number of rooms, etc.

- ML Models: Linear Regression, Decision Trees
- Stack: AWS + Python + Web Scraping

### Problem Definition

The demand for real estate properties in Belgrade has been skyrocketing recently, making it challenging for rentees to find the right property at the right price, before it's already rented out. The competition for rental properties with the "right price" is high, and people do not have time to constantly search for those properties.

This motivated me to create RENTER, a tool that can predict the asking price of a rental property and help rentees find undervalued properties quickly and easily.

### High Level Overview

![Draw io diagram](https://i.postimg.cc/vZbkJxHg/draw-io-diagram.png)

### Dataset

The dataset used in this project was collected by a crawler from the popular real estate website www.nekretnine.rs

The focus was on rental properties in Belgrade, Serbia (~4500 properties), and on structured data (property location, size, number of rooms etc.) - images were not included.

### Project status

1. **DONE** - Schedule fetch_ids execution that fetches property IDs of all active properties, on a daily basis, using AWS Lambda, and store its result in `property-ids-fetch` S3 bucket as CSV file.

2. **WIP** - As soon as new CSV file is uploaded to `property-ids-fetch` S3 bucket, run scrape_data execution using AWS Lambda, which scrapes the data from newly created property webpages, and stores it in `property-data-fetch` S3 bucket as CSV file. This file contains the features required by the models.

3. As soon new CSV file is uploaded to `property-data-fetch` S3 bucket, run clean_data execution using AWS Lambda, which cleans the data and prepares it for analysis. Clean data is stored in `clean-data` S3 bucket as CSV file.

4. Use data from `clean-data` S3 bucket and AWS Sagemaker, to build and train ML models.

5. Create a webpage with a dashboard, that would take input parameters (such as property location, size, number of rooms, etc.) and would provide you with a list of undervalued renting properties that match them.
