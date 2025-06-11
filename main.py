from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

stations=pd.read_csv("data_small/stations.txt",skiprows=17)
stations=stations[["STAID","STANAME                                 "]]
@app.route("/")
def home():
    return render_template("home.html",data=stations.to_html())


@app.route("/api/v1/<station>/<date>")  # fixed the typo in "vi" -> "v1"
def about(station, date):
    file_name = "data_small/TG_STAID" + str(station).zfill(6) + ".txt"

    try:
        df = pd.read_csv(file_name, skiprows=20, parse_dates=["    DATE"])
        temperature = df.loc[df['    DATE'] == pd.to_datetime(date), '   TG'].squeeze()

        if pd.isna(temperature):
            return {"error": "Temperature not found for this date"}, 404

        return {
            "station": station,
            "date": date,
            "temperature": temperature / 10
        }

    except FileNotFoundError:
        return {"error": f"Station file not found: {file_name}"}, 404
    except Exception as e:
        return {"error": str(e)}, 500


if __name__ == "__main__":
    app.run(debug=True)
