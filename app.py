from flask import Flask, render_template, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
import x
import re
app = Flask(__name__)

# settng some constants, all fields will check for it just for simplicity
CHARACTERS_MIN = 5
CHARACTERS_MAX = 40

# This secret key should be in env variable ideally!
SECRET_KEY = "some_secret_key"

# load base template for any existing route

@app.get("/")
@app.get("/login")
@app.get("/signup")
@app.get("/profile")
@app.get("/add_destination")
def spa_router():
    return render_template("_base.html")

# routes for partials
@app.get("/partials/home")
def partial_home():
    db = cursor = None
    try:
        # detect logged user
        auth_header = request.headers.get("Authorization")
        logged_user_id = None

        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
                logged_user_id = payload.get("user_id")
            except:
                pass

        db, cursor = x.db()

        q = """
        SELECT
            destination_id,
            destination_name,
            destination_desc,
            destination_country,
            destination_author,
            destination_uts,
            users.user_username
        FROM destinations
        JOIN users
        ON users.user_id = destinations.destination_author
        ORDER BY destination_uts DESC
        """

        cursor.execute(q)
        rows = cursor.fetchall()

        destinations = []

        for row in rows:
            destinations.append({
                "id": row["destination_id"],
                "name": row["destination_name"],
                "description": row["destination_desc"],
                "country": row["destination_country"],
                "author": row["user_username"],
                "author_id": row["destination_author"],
                "time_ago": time_since(row["destination_uts"])
            })

        return render_template(
            "partials/home.html",
            destinations=destinations,
            logged_user_id=logged_user_id
        )

    except Exception as ex:
        print("HOME ERROR:", ex, flush=True)
        return ""

    finally:
        if cursor: cursor.close()
        if db: db.close()

@app.get("/partials/login")
def partial_login():
    auth_header = request.headers.get("Authorization")
    user_data = None

    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        user_data = get_user_profile(token)

    if user_data:
        return render_template("partials/profile.html", user=user_data)
    else:
        return render_template("partials/login.html")
    
@app.get("/partials/signup")
def partial_signup():
    return render_template("partials/signup.html")

@app.get("/partials/add_destination")
def partial_add_destination():
    return render_template("partials/add_destination.html")

@app.get("/partials/profile")
def partial_profile():
    auth_header = request.headers.get("Authorization")
    user_data = None

    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        user_data = get_user_profile(token)

    if user_data:
        return render_template("partials/profile.html", user=user_data)
    else:
        return render_template("partials/login.html")

# Create new user
@app.post("/signup")
def create_user():
    resultMsg = ""
    try:
        # Validate form fields
        # All validation error messages will be bulked together. Returns json message.

        data = request.get_json()

        user_name = data.get("username")
        user_password = data.get("password")
        user_password_confirm = data.get("password_confirm")
        user_email = data.get("email")

        errors = []

        # Required fields
        if not user_name or not user_password or not user_password_confirm or not user_email:
            errors.append("All fields are required.")

        # Length validation
        if not (CHARACTERS_MIN <= len(user_name) <= CHARACTERS_MAX):
            errors.append(f"Username must be {CHARACTERS_MIN}-{CHARACTERS_MAX} characters.")

        if not (CHARACTERS_MIN <= len(user_password) <= CHARACTERS_MAX):
            errors.append(f"Password must be {CHARACTERS_MIN}-{CHARACTERS_MAX} characters.")

        if not (CHARACTERS_MIN <= len(user_email) <= CHARACTERS_MAX):
            errors.append(f"Email must be {CHARACTERS_MIN}-{CHARACTERS_MAX} characters.")

        # Password match
        if user_password != user_password_confirm:
            errors.append("Passwords do not match.")

        # Email format
        email_regex = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
        if not re.match(email_regex, user_email):
           errors.append("Invalid email format.")

        if errors:
            return jsonify({
                "success": False,
                "message": " ".join(errors)
            }), 400

        # if fields are valid, proceed to sending a sql query

        db, cursor = x.db()

        # Check duplicate username
        cursor.execute(
            "SELECT user_id FROM users WHERE user_username = %s",
            (user_name,)
        )
        if cursor.fetchone():
            return jsonify({
                "success": False,
                "message": "Username already exists."
            }), 409

        # Check duplicate email
        cursor.execute(
            "SELECT user_id FROM users WHERE user_email = %s",
            (user_email,)
        )
        if cursor.fetchone():
            return jsonify({
                "success": False,
                "message": "Email already registered."
            }), 409

        # Hash password
        hashed_password = generate_password_hash(user_password)

        q = "INSERT INTO users (user_username, user_password, user_email, user_reg) VALUES(%s, %s, %s, NOW())"
        cursor.execute(q, (user_name, hashed_password, user_email))
        db.commit()

        resultMsg = "User registered successfully."

        return jsonify({
            "success": True,
            "message": resultMsg
        })
    except Exception as ex:
        print(ex, flush = True)
        return jsonify({
            "success": False,
            "message": "Critical error. Evacuate all personnel immediately."
        }), 500
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()

# Login user
@app.post("/login")
def login_user():
    try:
        data = request.get_json()

        user_name = data.get("username")
        user_password = data.get("password")

        if not user_name or not user_password:
            return jsonify({
                "success": False,
                "message": "Username and password are required."
            }), 400

        db, cursor = x.db()

        # Query by username only
        cursor.execute("SELECT * FROM users WHERE user_username = %s", (user_name,))
        user = cursor.fetchone()

        if not user or not check_password_hash(user["user_password"], user_password):
            return jsonify({
                "success": False,
                "message": "Invalid username or password."
            }), 401

        # Generate JWT token, expires in 2 hours
        token = jwt.encode({
            "user_id": user["user_id"],
            "username": user["user_username"],
            "exp": datetime.datetime.now() + datetime.timedelta(hours=2)
        }, SECRET_KEY, algorithm="HS256")

        return jsonify({
            "success": True,
            "token": token
        })

    except Exception as ex:
        print(ex, flush=True)
        return jsonify({
            "success": False,
            "message": "Critical error. Evacuate all personnel immediately."
        }), 500
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()

# Add destination
@app.post("/add_destination")
def add_destination():
    try:
        # Authorization check
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({
                "success": False,
                "message": "Unauthorized."
            }), 401

        token = auth_header.split(" ")[1]

        # Decode JWT
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get("user_id")
        except jwt.ExpiredSignatureError:
            return jsonify({"success": False, "message": "Token expired."}), 401
        except jwt.InvalidTokenError:
            return jsonify({"success": False, "message": "Invalid token."}), 401

        data = request.get_json()

        destination_name = data.get("name")
        destination_country = data.get("country")
        destination_desc = data.get("description")

        errors = []

        # Required fields
        if not destination_name or not destination_country:
            errors.append("All fields are required.")

        # Length validation
        if not (CHARACTERS_MIN <= len(destination_name) <= CHARACTERS_MAX):
            errors.append(f"Name must be {CHARACTERS_MIN}-{CHARACTERS_MAX} characters.")

        if not (CHARACTERS_MIN <= len(destination_country) <= CHARACTERS_MAX):
            errors.append(f"Country must be {CHARACTERS_MIN}-{CHARACTERS_MAX} characters.")

        if errors:
            return jsonify({
                "success": False,
                "message": " ".join(errors)
            }), 400

        # Generate unix timestamp
        timestamp = int(datetime.datetime.now().timestamp())

        db, cursor = x.db()

        q = """
        INSERT INTO destinations
        (destination_name, destination_desc, destination_country, destination_uts, destination_author)
        VALUES (%s, %s, %s, %s, %s)
        """

        cursor.execute(q, (
            destination_name,
            destination_desc,
            destination_country,
            timestamp,
            user_id
        ))

        db.commit()

        return jsonify({
            "success": True,
            "message": "Destination added successfully."
        })

    except Exception as ex:
        print(ex, flush=True)
        return jsonify({
            "success": False,
            "message": "Critical error. Evacuate all personnel immediately."
        }), 500

    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()

@app.delete("/destination/<int:dest_id>")
def delete_destination(dest_id: int):
    try:
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"success": False, "message": "Unauthorized."}), 401

        token = auth_header.split(" ")[1]

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get("user_id")
        except jwt.ExpiredSignatureError:
            return jsonify({"success": False, "message": "Token expired."}), 401
        except jwt.InvalidTokenError:
            return jsonify({"success": False, "message": "Invalid token."}), 401

        db, cursor = x.db()

        # Secure delete: only if the logged user is the author
        cursor.execute(
            "DELETE FROM destinations WHERE destination_id = %s AND destination_author = %s",
            (dest_id, user_id)
        )
        db.commit()

        if cursor.rowcount == 0:
            # nothing deleted → either wrong id or not owner
            return jsonify({
                "success": False,
                "message": "Destination not found or not authorized."
            }), 404

        return jsonify({"success": True, "message": "Destination deleted successfully."})

    except Exception as ex:
        print("DELETE DESTINATION ERROR:", ex, flush=True)
        return jsonify({
            "success": False,
            "message": "Critical error. Evacuate all personnel immediately."
        }), 500

    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()

@app.get("/partials/edit_destination/<int:dest_id>")
def partial_edit_destination(dest_id: int):
    try:
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return "", 401

        token = auth_header.split(" ")[1]
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get("user_id")
        except:
            return "", 401

        db, cursor = x.db()

        # Fetch the destination
        cursor.execute("""
            SELECT destination_name, destination_desc, destination_country, destination_author
            FROM destinations
            WHERE destination_id = %s
        """, (dest_id,))
        dest = cursor.fetchone()

        if not dest:
            return "Destination not found", 404

        # Only author can edit
        if dest["destination_author"] != user_id:
            return "Unauthorized", 403

        # Render edit form
        return render_template("partials/edit_destination.html", destination=dest, destination_id=dest_id)

    except Exception as ex:
        print("EDIT DESTINATION ERROR:", ex, flush=True)
        return "", 500

    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()

@app.patch("/destination/<int:dest_id>")
def update_destination(dest_id: int):
    try:
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"success": False, "message": "Unauthorized"}), 401

        token = auth_header.split(" ")[1]
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get("user_id")
        except:
            return jsonify({"success": False, "message": "Invalid token"}), 401

        data = request.get_json() or {}
        name = data.get("name")
        country = data.get("country")
        description = data.get("description")

        if not name or not country:
            return jsonify({"success": False, "message": "Name and country required"}), 400

        if not (CHARACTERS_MIN <= len(name) <= CHARACTERS_MAX):
            return jsonify({"success": False, "message": f"Name must be {CHARACTERS_MIN}-{CHARACTERS_MAX} characters."}), 400

        if not (CHARACTERS_MIN <= len(country) <= CHARACTERS_MAX):
            return jsonify({"success": False, "message": f"Country must be {CHARACTERS_MIN}-{CHARACTERS_MAX} characters."}), 400

        db, cursor = x.db()

        # Ensure user is the author
        cursor.execute("""
            UPDATE destinations
            SET destination_name = %s, destination_country = %s, destination_desc = %s
            WHERE destination_id = %s AND destination_author = %s
        """, (name, country, description, dest_id, user_id))
        db.commit()

        if cursor.rowcount == 0:
            return jsonify({"success": False, "message": "Destination not found or not authorized"}), 404

        return jsonify({"success": True, "message": "Destination updated successfully"})

    except Exception as ex:
        print("UPDATE DESTINATION ERROR:", ex, flush=True)
        return jsonify({"success": False, "message": "Critical error"}), 500

    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()

# helper functions
def get_user_profile(token: str):
    db = cursor = None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("user_id")
        if not user_id:
            return None

        db, cursor = x.db()
        cursor.execute(
            "SELECT user_username, user_email, user_reg FROM users WHERE user_id = %s",
            (user_id,)
        )
        user = cursor.fetchone()
        if not user:
            return None

        return {
            "username": user["user_username"],
            "email": user["user_email"],
            "registered": user["user_reg"].strftime("%Y-%m-%d %H:%M:%S")
        }

    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None
    except Exception as ex:
        print("get_user_profile error:", ex, flush=True)
        return None
    finally:
        try:
            if cursor: cursor.close()
            if db: db.close()
        except Exception as ex:
            print("DB cleanup error:", ex, flush=True)

def time_since(timestamp: int) -> str:
    now = int(datetime.datetime.now().timestamp())
    diff = now - timestamp

    minutes = diff // 60
    hours = diff // 3600
    days = diff // 86400
    months = diff // (86400 * 30)
    years = diff // (86400 * 365)

    if minutes < 60:
        return f"{minutes} minutes ago"
    elif hours < 24:
        return f"{hours} hours ago"
    elif days < 30:
        return f"{days} days ago"
    elif months < 12:
        return f"{months} months ago"
    else:
        return f"{years} years ago"