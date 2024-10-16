from flask import Flask, jsonify, request
from Models import Session, Pixel, User
from config import config
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = config["APP_SECRET_KEY"]

def check_cooldown(pixel):
    session = Session()
    try:
        existing_pixel = session.query(Pixel).filter_by(x=pixel["X"], y=pixel["Y"]).order_by(Pixel.updated_at.desc()).first()

        if existing_pixel:
            last_updated_time = existing_pixel.updated_at
            if last_updated_time > datetime.utcnow() - timedelta(minutes=5):
                print(f"{pixel} has a cooldown rn")
                return False
        return True
    finally:
        session.close()

@app.route("/api/update_pixel", methods=['POST'])
def update_pixel():
    if request.method == "POST":
        try:
            data = request.json
            session = Session()
            pixel_list = data["pixel_list"]
            print(pixel_list)
            for pixel_data in pixel_list:
                
                user = session.query(User).filter_by(username=pixel_data["user"]).first()
                if not user:
                    user = User(username=pixel_data["user"])
                    session.add(user)
                    session.commit()  
                
                existing_pixel = session.query(Pixel).filter_by(x=pixel_data["X"], y=pixel_data["Y"]).first()

                if existing_pixel:
                    if check_cooldown(pixel_data):
                        existing_pixel.color_hex = pixel_data["hex-code"]
                        existing_pixel.updated_at = datetime.utcnow()
                else:
                    new_pixel = Pixel(
                        user_id=user.username,
                        x=pixel_data["X"],
                        y=pixel_data["Y"],
                        color_hex=pixel_data["hex-code"],
                        updated_at=datetime.utcnow()
                    )
                    session.add(new_pixel)
            
            session.commit()

            return jsonify({"success": True}), 200
        except Exception as e:
            session.rollback() 
            return jsonify({"success": False, "message": str(e)}), 404
        finally:
            session.close()

@app.route("/api/get_pixel")
def get_pixel_details():
    pass

if __name__ == "__main__":
    app.run(debug=True)