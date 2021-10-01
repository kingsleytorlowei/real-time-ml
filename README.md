# recommendation-system
The goal of this project is to set up an API that learns from previous inputs to predict better. I’ll be testing the Boston housing prices dataset provided by sklearn. This is a general-purpose problem but we’ll be using housing prices to get started.

For real-time forecasting, I’ll be using the FastAPI framework, it’s common to use HTTP requests to serve data for real-time forecasting. Our data contains 506 instances and 13 numerical and categorical features. We’re solving a regression problem. The numerical features will be scaled using StandadScaler and the Categorical features will be encoded using OneHotEncoder. We will use Ridge regression for our ML model.

## Components 

* Backend API 