![cover photo](https://www.firstpost.com/wp-content/uploads/2022/07/shutterstock_1499350838-1-scaled-1.jpg)

### RENTER - Real Estate Price Prediction Tool

RENTER is a machine learning project that aims to predict the asking price of rental properties in Belgrade, Serbia.

RENTER finds the best deals on properties by identifying undervalued rentals. By predicting the asking price of a property, RENTER can estimate when a property is undervalued, i.e. predicted asking price is higher (by a certain margin) than the actual asking price.

The models have been trained on the collected dataset to predict the asking price of a rental property based on various features such as location, size, number of rooms, etc.

- ML Models: Linear Regression, Decision Trees
- Stack: AWS + Python + Web Scraping

### Problem Definintion

The demand for real estate properties in Belgrade has been skyrocketing recently, making it challenging for renters to find the right property at the right price.

The competition for rental properties with the "right price" is high, and people do not have time to constantly search for those properties. This motivated me to create RENTER, a tool that can predict the asking price of a rental property and help renters find undervalued properties quickly and easily.

### High Level Overview

![Draw io diagram](https://i.postimg.cc/vZbkJxHg/draw-io-diagram.png)

### Dataset

The dataset used in this project was collected by a crawler from the popular real estate website www.nekretnine.rs

The focus was on rental properties in Belgrade, Serbia (~4500 properties), and on structured data (property location, size, number of rooms etc.) - images were not included.
