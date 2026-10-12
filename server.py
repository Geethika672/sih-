# ============================================================
# PRIVI-BROWSER
# Privacy Protection + AI Browser Agent Backend
# ============================================================

from executor import ActionExecutor

from flask import Flask, request, send_file, jsonify
from flask_cors import CORS

import pytesseract
from pytesseract import Output

from PIL import Image, ImageDraw

import re
import json
import os


# ============================================================
# FLASK SETUP
# ============================================================

app = Flask(__name__)

executor = ActionExecutor()

CORS(app)


# ============================================================
# TESSERACT PATH
# ============================================================

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


# ============================================================
# PROJECT DIRECTORY
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def normalize(text):
    """
    Convert text into lowercase normalized format.
    """

    return re.sub(
        r"\s+",
        " ",
        str(text or "")
    ).strip().lower()


def clamp(value, minimum, maximum):
    """
    Keep value inside a safe range.
    """

    return max(
        minimum,
        min(value, maximum)
    )


def hide_rectangle(
    draw,
    x,
    y,
    w,
    h,
    image_width,
    image_height
):
    """
    Strongly hide a sensitive rectangular area.
    """

    padding_x = 12
    padding_y = 10

    left = int(
        x - padding_x
    )

    top = int(
        y - padding_y
    )

    right = int(
        x + w + padding_x
    )

    bottom = int(
        y + h + padding_y
    )

    left = clamp(
        left,
        0,
        image_width
    )

    top = clamp(
        top,
        0,
        image_height
    )

    right = clamp(
        right,
        0,
        image_width
    )

    bottom = clamp(
        bottom,
        0,
        image_height
    )

    if right <= left or bottom <= top:
        return

    draw.rectangle(
        [
            left,
            top,
            right,
            bottom
        ],
        fill="black"
    )


def hide_word(
    draw,
    x,
    y,
    w,
    h,
    image_width,
    image_height
):
    """
    Hide OCR-detected sensitive text.
    """

    padding = 7

    left = clamp(
        int(x - padding),
        0,
        image_width
    )

    top = clamp(
        int(y - padding),
        0,
        image_height
    )

    right = clamp(
        int(x + w + padding),
        0,
        image_width
    )

    bottom = clamp(
        int(y + h + padding),
        0,
        image_height
    )

    if right <= left or bottom <= top:
        return

    draw.rectangle(
        [
            left,
            top,
            right,
            bottom
        ],
        fill="black"
    )


# ============================================================
# 🔐 PRIVACY PROTECTION
# ============================================================

@app.route(
    "/protect",
    methods=["POST"]
)
def protect():

    try:

        # ====================================================
        # 1. GET SCREENSHOT
        # ====================================================

        screenshot_file = (
            request.files.get("screenshot")
            or request.files.get("image")
        )

        if not screenshot_file:

            return jsonify({
                "success": False,
                "message": "Screenshot not received."
            }), 400


        # ====================================================
        # 2. FILE PATHS
        # ====================================================

        received_path = os.path.join(
            BASE_DIR,
            "received.png"
        )

        protected_path = os.path.join(
            BASE_DIR,
            "protected.png"
        )


        # ====================================================
        # 3. SAVE ORIGINAL SCREENSHOT
        # ====================================================

        screenshot_file.save(
            received_path
        )

        print("")
        print("==============================================")
        print("📸 SCREENSHOT RECEIVED")
        print("==============================================")


        # ====================================================
        # 4. OPEN IMAGE
        # ====================================================

        image = Image.open(
            received_path
        ).convert("RGB")

        draw = ImageDraw.Draw(
            image
        )

        screenshot_width, screenshot_height = (
            image.size
        )

        print(
            "🖼️ Screenshot size:",
            screenshot_width,
            "x",
            screenshot_height
        )


        # ====================================================
        # 5. GET VIEWPORT SIZE
        # ====================================================

        try:

            viewport_width = float(
                request.form.get(
                    "viewportWidth",
                    screenshot_width
                )
            )

            viewport_height = float(
                request.form.get(
                    "viewportHeight",
                    screenshot_height
                )
            )

        except Exception:

            viewport_width = screenshot_width
            viewport_height = screenshot_height


        if viewport_width <= 0:
            viewport_width = screenshot_width

        if viewport_height <= 0:
            viewport_height = screenshot_height


        # ====================================================
        # 6. SCREENSHOT SCALE
        # ====================================================

        scale_x = (
            screenshot_width /
            viewport_width
        )

        scale_y = (
            screenshot_height /
            viewport_height
        )

        print(
            "🌐 Viewport:",
            viewport_width,
            "x",
            viewport_height
        )

        print(
            "📐 Scale:",
            round(scale_x, 3),
            round(scale_y, 3)
        )


        # ====================================================
        # 7. GET DOM SENSITIVE FIELDS
        # ====================================================

        fields_raw = request.form.get(
            "fields",
            "[]"
        )

        try:

            fields = json.loads(
                fields_raw
            )

            if not isinstance(
                fields,
                list
            ):
                fields = []

        except Exception:

            fields = []


        print("")

        print(
            "🔎 DOM sensitive fields:",
            len(fields)
        )


        # ====================================================
        # 8. PROCESS DOM FIELDS
        # ====================================================

        protected_field_count = 0

        for index, field in enumerate(fields):

            if not isinstance(
                field,
                dict
            ):
                continue


            # ------------------------------------------------
            # Field information
            # ------------------------------------------------

            field_type = normalize(
                field.get("type")
            )

            name = normalize(
                field.get("name")
            )

            field_id = normalize(
                field.get("id")
            )

            placeholder = normalize(
                field.get("placeholder")
            )

            aria_label = normalize(
                field.get("ariaLabel")
            )

            autocomplete = normalize(
                field.get("autocomplete")
            )


            combined = " ".join([
                field_type,
                name,
                field_id,
                placeholder,
                aria_label,
                autocomplete
            ])


            # ------------------------------------------------
            # Sensitive detection
            # ------------------------------------------------

            sensitive = False
            reason = ""


            # PASSWORD

            if field_type == "password":

                sensitive = True
                reason = "password"


            # SENSITIVE WORDS

            sensitive_words = [
                "password",
                "passcode",
                "pass",
                "email",
                "e-mail",
                "phone",
                "mobile",
                "telephone",
                "upi",
                "vpa",
                "aadhaar",
                "aadhar",
                "pan",
                "account",
                "account number",
                "card",
                "card number",
                "cvv",
                "security code"
            ]


            if not sensitive:

                for word in sensitive_words:

                    if word in combined:

                        sensitive = True
                        reason = word
                        break


            # ------------------------------------------------
            # Ignore non-sensitive fields
            # ------------------------------------------------

            if not sensitive:
                continue


            # =================================================
            # 9. GET COORDINATES
            # =================================================

            try:

                x = float(
                    field.get("x", 0)
                )

                y = float(
                    field.get("y", 0)
                )

                w = float(
                    field.get("width", 0)
                )

                h = float(
                    field.get("height", 0)
                )

            except Exception:

                print(
                    "⚠️ Invalid coordinates for field:",
                    index
                )

                continue


            # =================================================
            # 10. CHECK COORDINATES
            # =================================================

            if w <= 0 or h <= 0:

                print(
                    "⚠️ Empty field dimensions:",
                    index
                )

                continue


            # =================================================
            # 11. CSS PIXELS → SCREENSHOT PIXELS
            # =================================================

            x = x * scale_x
            y = y * scale_y
            w = w * scale_x
            h = h * scale_y


            # =================================================
            # 12. LOG FIELD
            # =================================================

            print("")

            print(
                "🔐 Protecting field #",
                index + 1
            )

            print(
                "   Type:",
                field_type
            )

            print(
                "   Reason:",
                reason
            )

            print(
                "   Metadata:",
                combined
            )

            print(
                "   Position:",
                round(x, 2),
                round(y, 2),
                round(w, 2),
                round(h, 2)
            )


            # =================================================
            # 13. MASK FIELD
            # =================================================

            hide_rectangle(
                draw,
                x,
                y,
                w,
                h,
                screenshot_width,
                screenshot_height
            )

            protected_field_count += 1


        # ====================================================
        # 14. OCR PROTECTION
        # ====================================================

        print("")

        print(
            "=============================================="
        )

        print(
            "🔎 RUNNING OCR"
        )

        print(
            "=============================================="
        )


        try:

            data = pytesseract.image_to_data(
                image,
                output_type=Output.DICT
            )

        except Exception as ocr_error:

            print(
                "⚠️ OCR error:",
                str(ocr_error)
            )

            data = {
                "text": [],
                "left": [],
                "top": [],
                "width": [],
                "height": []
            }


        # ====================================================
        # 15. PROCESS OCR RESULTS
        # ====================================================

        ocr_protected_count = 0


        for i, raw_text in enumerate(
            data.get("text", [])
        ):

            text = str(
                raw_text or ""
            ).strip()


            if not text:
                continue


            try:

                x = int(
                    data["left"][i]
                )

                y = int(
                    data["top"][i]
                )

                w = int(
                    data["width"][i]
                )

                h = int(
                    data["height"][i]
                )

            except Exception:

                continue


            # =================================================
            # EMAIL
            # =================================================

            email_pattern = (
                r"[A-Za-z0-9._%+-]+"
                r"@"
                r"[A-Za-z0-9.-]+"
                r"\.[A-Za-z]{2,}"
            )


            if re.fullmatch(
                email_pattern,
                text
            ):

                print(
                    "🔐 OCR Email:",
                    text
                )

                hide_word(
                    draw,
                    x,
                    y,
                    w,
                    h,
                    screenshot_width,
                    screenshot_height
                )

                ocr_protected_count += 1

                continue


            # =================================================
            # UPI / VPA
            # =================================================

            upi_pattern = (
                r"[A-Za-z0-9._-]+"
                r"@[A-Za-z]{2,}"
            )


            if re.fullmatch(
                upi_pattern,
                text
            ):

                print(
                    "🔐 OCR UPI:",
                    text
                )

                hide_word(
                    draw,
                    x,
                    y,
                    w,
                    h,
                    screenshot_width,
                    screenshot_height
                )

                ocr_protected_count += 1

                continue


            # =================================================
            # MOBILE NUMBER
            # =================================================

            digits = re.sub(
                r"\D",
                "",
                text
            )


            if re.fullmatch(
                r"[6-9]\d{9}",
                digits
            ):

                print(
                    "🔐 OCR Mobile:",
                    text
                )

                hide_word(
                    draw,
                    x,
                    y,
                    w,
                    h,
                    screenshot_width,
                    screenshot_height
                )

                ocr_protected_count += 1

                continue


            # =================================================
            # AADHAAR-LIKE 12 DIGITS
            # =================================================

            if re.fullmatch(
                r"\d{12}",
                digits
            ):

                print(
                    "🔐 OCR ID:",
                    text
                )

                hide_word(
                    draw,
                    x,
                    y,
                    w,
                    h,
                    screenshot_width,
                    screenshot_height
                )

                ocr_protected_count += 1

                continue


            # =================================================
            # PAN-LIKE VALUE
            # =================================================

            pan_pattern = (
                r"[A-Z]{5}[0-9]{4}[A-Z]"
            )


            if re.fullmatch(
                pan_pattern,
                text.upper()
            ):

                print(
                    "🔐 OCR PAN:",
                    text
                )

                hide_word(
                    draw,
                    x,
                    y,
                    w,
                    h,
                    screenshot_width,
                    screenshot_height
                )

                ocr_protected_count += 1

                continue


        # ====================================================
        # 16. SAVE PROTECTED IMAGE
        # ====================================================

        image.save(
            protected_path
        )


        # ====================================================
        # 17. FINAL LOG
        # ====================================================

        print("")

        print(
            "=============================================="
        )

        print(
            "✅ PRIVACY PROTECTION COMPLETE"
        )

        print(
            "🔐 DOM fields protected:",
            protected_field_count
        )

        print(
            "🔎 OCR items protected:",
            ocr_protected_count
        )

        print(
            "🛡️ Protected image:",
            protected_path
        )

        print(
            "=============================================="
        )

        print("")


        # ====================================================
        # 18. RETURN PROTECTED SCREENSHOT
        # ====================================================

        return send_file(
            protected_path,
            mimetype="image/png"
        )


    # ========================================================
    # PROTECTION ERROR
    # ========================================================

    except Exception as e:

        print("")

        print(
            "❌ Protection error:",
            str(e)
        )

        print("")

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


# ============================================================
# 🤖 ACTION EXECUTION
# ============================================================

@app.route(
    "/execute",
    methods=["POST"]
)
def execute_action():

    try:

        data = request.get_json(
            silent=True
        ) or {}


        if not data or "action" not in data:

            return jsonify({
                "success": False,
                "message": "No action provided."
            }), 400


        result = executor.execute(
            data
        )


        return jsonify(
            result
        )


    except Exception as e:

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


# ============================================================
# 🤖 AI PLANNER
# ============================================================

@app.route(
    "/plan",
    methods=["POST"]
)
def plan_task():

    try:

        from agent import BrowserAgent


        data = request.get_json(
            silent=True
        ) or {}


        task = data.get(
            "task",
            ""
        ).strip()


        if not task:

            return jsonify({
                "success": False,
                "message": "Task is empty."
            }), 400


        print("")

        print(
            "=============================================="
        )

        print(
            "🤖 AI BROWSER AGENT"
        )

        print(
            "=============================================="
        )

        print(
            "Task received:",
            task
        )


        # --------------------------------------------
        # Agent understands + Planner creates plan
        # --------------------------------------------

        agent = BrowserAgent()

        result = agent.process_task(
            task
        )


        print("")

        print(
            "🧠 Understanding:"
        )

        print(
            result["understanding"]
        )


        print("")

        print(
            "📋 Generated Plan:"
        )


        for index, step in enumerate(
            result["plan"],
            start=1
        ):

            print(
                f"{index}. "
                f"{step['action']} "
                f"→ "
                f"{step['target']}"
            )


        print(
            "=============================================="
        )

        print("")


        return jsonify({

            "success": True,

            "task": task,

            "understanding":
                result["understanding"],

            "plan":
                result["plan"]

        })


    except Exception as e:

        print("")

        print(
            "❌ Agent/Planner error:",
            str(e)
        )

        print("")


        return jsonify({

            "success": False,

            "message":
                str(e)

        }), 500


# ============================================================
# 🏠 HOME / HEALTH CHECK
# ============================================================

@app.route(
    "/",
    methods=["GET"]
)
def home():

    return jsonify({

        "status":
            "running",

        "project":
            "PRIVI-BROWSER",

        "privacy":
            "active",

        "ai_planner":
            "active"

    })


# ============================================================
# 🚀 START SERVER
# ============================================================

if __name__ == "__main__":

    print("")

    print(
        "=============================================="
    )

    print(
        "🔐 PRIVI-BROWSER BACKEND"
    )

    print(
        "=============================================="
    )

    print(
        "🛡️ Privacy Protection : ACTIVE"
    )

    print(
        "🤖 AI Browser Agent   : ACTIVE"
    )

    print(
        "🔎 OCR                : ACTIVE"
    )

    print(
        "=============================================="
    )

    print(
        "🚀 Server:"
    )

    print(
        "http://127.0.0.1:5000"
    )

    print(
        "=============================================="
    )

    print("")


    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )