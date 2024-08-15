# Weight Loss Predictor Web Application
#### Video Demo:  [Click here to watch the demo](<URL HERE>)
#### Description:

This tool is designed to provide users with a visual and data-driven approach to understanding and predicting weight loss trajectories based on caloric intake and activity levels.

## Features

- **Dynamic Graph Generation**: Visualize your weight loss or gain over a specified period based on your input parameters.
- **CSV Data Export**: Download detailed CSV files containing daily metrics for deeper analysis or record-keeping.
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

---

*For any questions or feedback, please contact [selimserif123@gmail.com](mailto:selimserif123@gmail.com).*
