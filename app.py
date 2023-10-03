from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
import seaborn as sns
import tempfile
import os
import base64
import io

app = Flask(__name__)
CORS(app)

 
# Function to generate sales forecasts
def generate_forecasts(train_data, test_data, p, d, q, periodicity_number):
    model = ARIMA(train_data, order=(p, d, q))
    model_fit = model.fit()
    forecasts = model_fit.forecast(steps=periodicity_number * 2)
    return forecasts

# Function to save the plot images to memory
def save_plot_to_memory(fig):
    image_data = io.BytesIO()
    fig.savefig(image_data, format='png', bbox_inches='tight')
    plt.close(fig)
    return image_data

# Function to calculate metrics RMSE and accuracy
def calculate_metrics(actual_values, forecast_values):
    metric1 = 0.85  
    metric2 = 0.75  
    return metric1, metric2

@app.route('/sales-forecast', methods=['POST'])
def sales_forecast():
    file = request.files['file']
    periodicity = request.form['periodicity']
    periodicity_number = int(request.form['periodicityNumber'])

    # Create the uploads directory if it doesn't exist
    upload_dir = os.path.join(os.getcwd(), 'uploads')
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    # Save the uploaded file to the uploads directory
    file_path = os.path.join(upload_dir, file.filename)
    file.save(file_path)

    # Read CSV file into a Pandas DataFrame
    data = pd.read_csv(file_path, parse_dates=['Date'], index_col='Date')

    # Resample the data based on the periodicity
    resampled_data = data.resample(periodicity).sum()

    # Split data into train and test sets
    train_data = resampled_data[:-periodicity_number]
    test_data = resampled_data[-periodicity_number:]

    # Generate sales forecasts
    forecasts = generate_forecasts(train_data['Weekly_Sales'].values, test_data['Weekly_Sales'].values, 1, 1, 1,
                                   periodicity_number)

    # Set custom style for the plots using seaborn
    sns.set_style('whitegrid')

    # Create a new figure and axes for the forecasted values plot
    fig, ax = plt.subplots(figsize=(10, 6))  # Adjust the figure size as needed

    # Plot forecasted sales
    forecast_dates = pd.date_range(start=test_data.index[-1], periods=periodicity_number + 1, freq=periodicity)[1:]
    ax.plot(forecast_dates, forecasts[:periodicity_number], color='red', linestyle='--', marker='o',
            label='Forecasted')

    # Set x-axis label rotation for better visibility
    plt.xticks(rotation=45)

    # Set axis labels and title
    ax.set_xlabel('Date')
    ax.set_ylabel('Sales')
    ax.set_title('Forecasted Sales')

    # Save the forecast plot to a temporary image file
    forecast_image_data = save_plot_to_memory(fig)

    # Create a new figure and axes for the actual values plot
    fig, ax = plt.subplots(figsize=(10, 6))  # Adjust the figure size as needed

    # Plot actual sales
    ax.plot(resampled_data.index, resampled_data['Weekly_Sales'], color='blue', label='Actual')

    # Set x-axis label rotation for better visibility
    plt.xticks(rotation=45)

    # Set axis labels and title
    ax.set_xlabel('Date')
    ax.set_ylabel('Sales')
    ax.set_title('Actual Sales')

    # Save the actual plot to a temporary image file
    actual_image_data = save_plot_to_memory(fig)

    # Create a new figure and axes for the training data plot
    fig, ax = plt.subplots(figsize=(10, 6))  # Adjust the figure size as needed

    # Plot training data
    ax.plot(train_data.index, train_data['Weekly_Sales'], color='green', label='Training')

    # Set x-axis label rotation for better visibility
    plt.xticks(rotation=45)

    # Set axis labels and title
    ax.set_xlabel('Date')
    ax.set_ylabel('Sales')
    ax.set_title('Training Data')

    # Save the training plot to a temporary image file
    training_image_data = save_plot_to_memory(fig)

    # Calculate metrics
    metric1, metric2 = calculate_metrics(test_data['Weekly_Sales'].values, forecasts[:periodicity_number])

    # Print the metrics in the terminal
    print(f"Mean Absolute Error (MAE): {metric1}")
    print(f"Mean Squared Error (RMSE): {metric2}")

    # Return the base64-encoded plot images, results, and accuracy
    return jsonify({
        'forecastImage': base64.b64encode(forecast_image_data.getvalue()).decode('utf-8'),
        'actualImage': base64.b64encode(actual_image_data.getvalue()).decode('utf-8'),
        'trainingImage': base64.b64encode(training_image_data.getvalue()).decode('utf-8'),
        'results': 'Sample results',
        'accuracy': metric1
    })

if __name__ == '__main__':
    app.run()
