# Weight Loss Predictor Web Application
#### Video Demo:  [Click here to watch the demo](<URL HERE>)
#### Description:

Welcome to the **Weight Loss Predictor Web Application**. This tool is designed to provide users with a visual and data-driven approach to understanding and predicting weight loss trajectories based on caloric intake and activity levels. Leveraging the Mifflin-St Jeor Equation and advanced data visualization techniques, this application offers both graphical and tabular insights into weight management.

## Features

- **Dynamic Graph Generation**: Visualize your weight loss or gain over a specified period based on your input parameters.
- **CSV Data Export**: Download detailed CSV files containing daily metrics for deeper analysis or record-keeping.
- **Session-Based Data Storage**: Each user's session data is stored temporarily, ensuring privacy and data integrity.
- **Responsive Design**: Accessible on various devices, ensuring a seamless user experience.

## How It Works

1. **User Input**: Users provide essential details such as age, gender, height, weight, activity level, desired caloric deficit, and the duration for the prediction.

2. **Calculations**:
   - **Basal Metabolic Rate (BMR)**: Calculated using the Mifflin-St Jeor Equation, which considers age, gender, height, and weight.
   - **Total Daily Energy Expenditure (TDEE)**: Adjusted based on the user's specified activity level.
   - **Daily Caloric Intake**: Determined by subtracting the desired caloric deficit from the TDEE.
   - **Weight Loss Prediction**: Based on the caloric deficit and the duration, the application predicts the potential weight change.

3. **Output**:
   - **Graph**: Displays a projected weight change over the specified period.
   - **CSV File**: Contains daily breakdowns of weight, BMR, TDEE, and caloric intake.

## Technologies Used

- **Front-End**: HTML5, CSS3, Bootstrap 5
- **Back-End**: Python 3.10, Flask Framework
- **Database**: SQLite3 for session-based data storage
- **Data Visualization**: Matplotlib for generating dynamic graphs
- **Hosting**: Deployed on PythonAnywhere

## Setup & Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/weight-loss-predictor.git
   ```

2. **Navigate to the Project Directory**:
   ```bash
   cd weight-loss-predictor
   ```

3. **Create a Virtual Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Initialize the Database**:
   ```bash
   python
   >>> from app import init_db
   >>> init_db()
   >>> exit()
   ```

6. **Run the Application**:
   ```bash
   flask run
   ```

7. **Access the Application**:
   Navigate to `http://127.0.0.1:5000` in your web browser.

## Usage

1. **Fill in the Form**: Provide all the required information in the input form on the homepage.

2. **Generate Predictions**: Click on the "Predict" button to generate the weight loss graph and download the CSV file.

3. **Review Results**:
   - **Graph**: Visual representation of your weight trajectory.
   - **CSV**: Detailed daily data for personal records or further analysis.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your feature or bug fix. Ensure that your code adheres to the project's coding standards and includes appropriate documentation.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- **CS50 Course**: Inspiration and foundational knowledge.
- **Flask**: For providing an excellent web framework.
- **Matplotlib**: For the powerful data visualization capabilities.

---

*For any questions or feedback, please contact [your.email@example.com](mailto:your.email@example.com).*
