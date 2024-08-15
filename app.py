import sqlite3
import csv
import io
import uuid
import os
from flask import Flask, render_template, request, session, url_for, send_file, make_response
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from helper import apology

app = Flask(__name__)
app.secret_key = 'ihatewebdev'  # Required for session management

DB_PATH = '/home/selimserif/mysite/database.db'

# Initialize the database
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS images (
                        session_id TEXT,
                        image_type TEXT,
                        image_data BLOB
                      )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS csvs (
                        session_id TEXT,
                        csv_data BLOB
                      )''')
    conn.commit()
    conn.close()

# Function to save image to database
def save_image_to_db(session_id, image_type, image_data):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO images (session_id, image_type, image_data)
        VALUES (?, ?, ?)
    """, (session_id, image_type, image_data))
    conn.commit()
    conn.close()

# Function to retrieve image from database
def get_image_from_db(session_id, image_type):
    conn = sqlite3.connect('/home/selimserif/mysite/database.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT image_data FROM images WHERE session_id = ? AND image_type = ?
    """, (session_id, image_type))
    image_data = cursor.fetchone()[0]
    conn.close()
    return image_data

# Function to save CSV to database
def save_csv_to_db(session_id, csv_data):
    conn = sqlite3.connect('/home/selimserif/mysite/database.db')
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO csvs (session_id, csv_data)
        VALUES (?, ?)
    """, (session_id, csv_data))
    conn.commit()
    conn.close()

# Function to retrieve CSV from database
def get_csv_from_db(session_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT csv_data FROM csvs WHERE session_id = ?
    """, (session_id,))
    csv_data = cursor.fetchone()[0]
    conn.close()
    return csv_data

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            # Retrieve input values
            current_bfp = float(request.form.get("current_bfp"))
            target_bfp = float(request.form.get("target_bfp"))
            weight = float(request.form.get("weight"))
            weight_unit = request.form.get("weight_unit")
            activity_level = float(request.form.get("activity_level"))
            fat_loss_percentage = float(request.form.get("fat_loss_percentage")) if request.form.get("fat_loss_percentage") else 100
            macro_dict = {
                "protein": float(request.form.get("macro_protein")) if request.form.get("macro_protein") else 0,
                "fat": float(request.form.get("macro_fat")) if request.form.get("macro_fat") else 0,
                "carb": float(request.form.get("macro_carbs")) if request.form.get("macro_carbs") else 0,
            }
            extra_options = request.form.get("extra_options")

            # Validate and process input
            if not (3 <= current_bfp <= 50) or not (3 <= target_bfp <= 50):
                return apology("BFP% values must be between 3 and 50.", 1)
            if weight_unit == "lbs":
                weight *= 0.453592  # Convert lbs to kg
            elif weight_unit != "kg":
                return apology("Invalid unit of weight.", 1)
            if extra_options == "on" and 0 not in macro_dict.values():
                if not (0 < fat_loss_percentage <= 100):
                    return apology("Invalid percentage for fat loss as total weight loss.", 1)
                if sum(macro_dict.values()) != 100:
                    return apology("Macros don't add up to 100%", 1)

            # Main calculations
            week = 0
            extra_options = 1 if extra_options == 'on' and 0 not in macro_dict.values() else 0

            def maincalc(week, weight, bfp, extra_options):
                weeks, weights, bfps, listdict = [], [], [], []
                while bfp > target_bfp:
                    weight_loss = round(((bfp / 20) / 100) * weight, 2)
                    lbm = weight - (bfp / 100) * weight
                    caloric_deficit = round((weight_loss * 7700) / 7)
                    tdee = round((370 + (21.6 * lbm)) * activity_level)
                    calorie_target = tdee - caloric_deficit
                    fat_loss = round(weight_loss * (fat_loss_percentage / 100), 2)
                    lbm_loss = round(weight_loss - fat_loss, 2)
                    lbm = round(lbm - lbm_loss, 2)

                    if extra_options == 0:
                        protein = round(weight * 2.4)
                        fat = round(0.66 * weight)
                        carb = round((calorie_target - (protein * 4 + fat * 9)) / 4)
                        macro_percentage_dict = {
                            'protein': round((protein * 4 / calorie_target) * 100, 2),
                            'carb': round((carb * 4 / calorie_target) * 100, 2),
                            'fat': round((fat * 9 / calorie_target) * 100, 2)
                        }
                    else:
                        protein = round((calorie_target * macro_dict["protein"] / 100) / 4, 2)
                        carb = round((calorie_target * macro_dict["carb"] / 100) / 4, 2)
                        fat = round((calorie_target * macro_dict["fat"] / 100) / 9, 2)
                        macro_percentage_dict = {key: round(macro_dict[key], 2) for key in macro_dict}

                    new_weight = round(weight - weight_loss, 2)
                    new_bfp = round((new_weight - lbm) / (weight / 100), 2)

                    listdict.append({
                        "week": week + 1,
                        "tdee": tdee,
                        "caloric_deficit": caloric_deficit,
                        "caloric_goal": calorie_target,
                        "weight_loss_goal": weight_loss,
                        "new_bfp": new_bfp,
                        "new_weight": new_weight,
                        "macros": {"protein": protein, "carbs": carb, "fats": fat},
                        "macros_percent": macro_percentage_dict
                    })

                    # Store data for plotting
                    weeks.append(f"Week {week + 1}")
                    weights.append(new_weight)
                    bfps.append(new_bfp)

                    # Update for next iteration
                    weight, bfp, week = new_weight, new_bfp, week + 1

                return listdict, weeks, weights, bfps

            listdict, weeks, weights, bfps = maincalc(week, weight, current_bfp, extra_options)
            session['results'] = listdict

            # Generate session ID
            session_id = str(uuid.uuid4())
            session['session_id'] = session_id

            # Generate graphs and save to database
            plt.figure(figsize=(10, 5))

            # Weight loss graph
            plt.plot(weeks, weights, marker='o')
            plt.title('Weight Loss Over Time')
            plt.xlabel('Weeks')
            plt.ylabel('Weight (kg)')
            plt.grid(True)
            weight_loss_img = io.BytesIO()
            plt.savefig(weight_loss_img, format='png')
            weight_loss_img.seek(0)
            save_image_to_db(session_id, 'weight_loss_image', weight_loss_img.read())
            plt.close()

            # BFP change graph
            plt.plot(weeks, bfps, marker='o')
            plt.title('Body Fat Percentage (BFP) Over Time')
            plt.xlabel('Weeks')
            plt.ylabel('BFP (%)')
            plt.grid(True)
            bfp_img = io.BytesIO()
            plt.savefig(bfp_img, format='png')
            bfp_img.seek(0)
            save_image_to_db(session_id, 'bfp_image', bfp_img.read())
            plt.close()

            return render_template("results.html", results=listdict, session_id=session_id)

        except (ValueError, TypeError):
            return apology("Invalid input. Please check your data and try again.", 1)
    else:
        activity_levels = [
            {"label": "Completely Paralyzed, Comatose, Unable to Move Without the Aid of Others (1.0)", "value": 1.0},
            {"label": "Immobile, Stationary with Some Arm Movement, Bedridden or Partially Paralyzed (1.05)", "value": 1.05},
            {"label": "Constricted Lifestyle, Movement is Limited to a Confined Space, Almost Always Sitting or Laying (1.1)", "value": 1.1},
            {"label": "Working From Home with Little to No Travel, No Exercise, Some Walking, Mostly Sitting or Laying (1.16)", "value": 1.16},
            {"label": "Sedentary Lifestyle, Little or No Exercise, Moderate Walking, Desk Job (Away from Home) (1.2)", "value": 1.2},
            {"label": "Slightly Active, Exercise or Light Sports 1 to 3 Days a Week, Light Jogging or Walking 3 to 4 Days a Week (1.375)", "value": 1.375},
            {"label": "Lightly Active, Exercise or Moderate Sports 2 to 3 Days a Week, Light Jogging or Walking 5 to 7 Days a Week (1.425)", "value": 1.425},
            {"label": "Moderately Active, Physical Work, Exercise, or Sports 4 to 5 Days a Week, Construction Laborer (1.55)", "value": 1.55},
            {"label": "Very Active, Heavy Physical Work, Exercise, or Sports 6 to 7 Days a Week, Hard Laborer (1.75)", "value": 1.75},
            {"label": "Extremely Active, Very Heavy Physical Work or Exercise Every Day, Professional/Olympic Athlete (1.9)", "value": 1.9},
        ]
        return render_template("index.html", activity_levels=activity_levels)

@app.route('/image/<session_id>/<image_type>')
def serve_image(session_id, image_type):
    image_data = get_image_from_db(session_id, image_type)
    response = make_response(image_data)
    response.headers.set('Content-Type', 'image/png')
    return response

@app.route("/download_csv/<session_id>")
def download_csv(session_id):
    listdict = session.get('results')
    if not listdict:
        return apology("No results to download.", 1)

    csv_data = io.StringIO()
    writer = csv.DictWriter(csv_data, fieldnames=["week", "tdee", "caloric_deficit", "caloric_goal", "weight_loss_goal", "new_bfp", "new_weight", "protein", "carbs", "fats"])
    writer.writeheader()
    for result in listdict:
        writer.writerow({
            "week": result["week"],
            "tdee": result["tdee"],
            "caloric_deficit": result["caloric_deficit"],
            "caloric_goal": result["caloric_goal"],
            "weight_loss_goal": result["weight_loss_goal"],
            "new_bfp": result["new_bfp"],
            "new_weight": result["new_weight"],
            "protein": result["macros"]["protein"],
            "carbs": result["macros"]["carbs"],
            "fats": result["macros"]["fats"]
        })

    csv_data.seek(0)
    save_csv_to_db(session_id, csv_data.getvalue())

    # Re-fetching the CSV data from the database to ensure it was saved
    csv_data = get_csv_from_db(session_id)
    if csv_data is None:
        return apology("Failed to retrieve CSV data from the database.", 1)

    response = make_response(csv_data)
    response.headers.set('Content-Disposition', 'attachment', filename=f'results_{session_id}.csv')
    response.headers.set('Content-Type', 'text/csv')
    return response

@app.route("/bfp")
def bfp():
    return render_template("bfp.html")

@app.route("/faq")
def faq():
    return render_template('faq.html')

@app.route("/calories")
def calories():
    return render_template('calories.html')

if __name__ == "__main__":
    init_db()
    app.run()
