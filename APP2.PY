from flask import Flask, render_template, request
from datetime import datetime
import webbrowser
import threading

app = Flask(__name__)

COMMONLY_USED_MPINS = {
    "1234", "2345", "3456", "4567", "5678", "6789", "7890", "0123",
    "0000", "1111", "2222", "3333", "4444", "5555", "6666", "7777", "8888", "9999",
    "1212", "1122", "1221", "2112", "1001", "2002", "3003", "4004",
    "4321", "9876", "6789", "1010", "2020", "0101", "1313",
    "1990", "1980", "2000", "2022", "2023", "2024",
    "0707", "0808", "0911", "1110", "1212", "0606", "0311", "0101", "1111",
    "6969", "1230", "1004", "1211", "1110", "1919", "1987", "1985",
    "123456", "111111", "000000", "121212", "777777", "654321", "112233",
    "999999", "555555", "666666", "112211", "101010", "121314", "123123",
    "987654", "159753", "456789", "147258", "741852", "369258"
}

REASON_MESSAGES = {
    "COMMONLY_USED": "COMMONLY_USED",
    "REPEATED_PATTERN": "REPEATED_PATTERN",
    "DEMOGRAPHIC_DOB_SELF": "DEMOGRAPHIC_DOB_SELF",
    "DEMOGRAPHIC_DOB_SPOUSE": "DEMOGRAPHIC_DOB_SPOUSE",
    "DEMOGRAPHIC_ANNIVERSARY": "DEMOGRAPHIC_ANNIVERSARY"
}

def is_common_mpin_part_a(mpin):
    if len(mpin) == 4:
        return mpin in COMMONLY_USED_MPINS
    return False

def extract_date_parts(date_str):
    patterns = set()
    if not date_str:
        return patterns
    try:
        if '-' in date_str:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        elif '/' in date_str:
            date_obj = datetime.strptime(date_str, "%d/%m/%Y")
        else:
            return patterns

        day = f"{date_obj.day:02d}"
        month = f"{date_obj.month:02d}"
        year_full = f"{date_obj.year}"
        year_short = year_full[-2:]

        # 4-digit combos
        patterns.update({
            day + month,
            year_short + month,
            month + year_short,
            day + year_short,
            year_short + day,
        })

        # 6-digit combos
        patterns.update({
            day + month + year_short,
            year_short + month + day,
            month + day + year_short,
            month + year_short + day,
            year_full[-6:],
        })

        return patterns
    except Exception:
        return patterns

def is_repeated_pattern(mpin):
    length = len(mpin)
    for sub_len in range(1, length // 2 + 1):
        if length % sub_len == 0:
            sub = mpin[:sub_len]
            if sub * (length // sub_len) == mpin:
                return True
    return False

def analyze_mpin(mpin, user_dob, spouse_dob, anniversary):
    reasons = set()

    if mpin in COMMONLY_USED_MPINS:
        reasons.add("COMMONLY_USED")

    if is_repeated_pattern(mpin):
        reasons.add("REPEATED_PATTERN")

    if mpin in extract_date_parts(user_dob):
        reasons.add("DEMOGRAPHIC_DOB_SELF")

    if mpin in extract_date_parts(spouse_dob):
        reasons.add("DEMOGRAPHIC_DOB_SPOUSE")

    if mpin in extract_date_parts(anniversary):
        reasons.add("DEMOGRAPHIC_ANNIVERSARY")

    strength = "WEAK" if reasons else "STRONG"

    return {"strength": strength, "reasons": reasons}

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    test_output = None
    mpin = ''
    user_dob = ''
    spouse_dob = ''
    anniversary = ''

    if request.method == 'POST':
        if 'run_tests' in request.form:
            test_output = run_tests()
        else:
            mpin = request.form.get('mpin', '').strip()
            user_dob = request.form.get('user_dob', '').strip()
            spouse_dob = request.form.get('spouse_dob', '').strip()
            anniversary = request.form.get('anniversary', '').strip()

            if not mpin:
                result = {"error": "please enter an MPIN."}
            elif not mpin.isdigit() or len(mpin) not in (4, 6):
                result = {"error": "MPIN must be a 4 or 6 digit number."}
            else:
                result = analyze_mpin(mpin, user_dob, spouse_dob, anniversary)
                # Format reasons output as requested:
                if result and "reasons" in result and result["reasons"]:
                    sorted_reasons = sorted(result["reasons"])  # sort alphabetically for consistency
                    formatted_reasons = sorted_reasons[0]  # first without bullet
                    for r in sorted_reasons[1:]:
                        formatted_reasons += "\n• " + r
                    result["formatted_reasons"] = formatted_reasons
                else:
                    result["formatted_reasons"] = ""

    return render_template('index.html',
                           result=result,
                           test_output=test_output,
                           mpin=mpin,
                           user_dob=user_dob,
                           spouse_dob=spouse_dob,
                           anniversary=anniversary)

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/")

def run_tests():
    output = []

    def assert_equal(actual, expected, test_name):
        if actual == expected:
            output.append(f"PASS: {test_name}")
        else:
            output.append(f"FAIL: {test_name} - Expected: {expected}, Got: {actual}")

    test_cases = [
        {"mpin": "1234", "user_dob": "", "spouse_dob": "", "anniversary": "", "expected_strength": "WEAK", "expected_reasons": ["COMMONLY_USED"]},
        {"mpin": "0000", "user_dob": "", "spouse_dob": "", "anniversary": "", "expected_strength": "WEAK", "expected_reasons": ["COMMONLY_USED"]},
        {"mpin": "9999", "user_dob": "", "spouse_dob": "", "anniversary": "", "expected_strength": "WEAK", "expected_reasons": ["COMMONLY_USED"]},
        {"mpin": "6789", "user_dob": "", "spouse_dob": "", "anniversary": "", "expected_strength": "WEAK", "expected_reasons": ["COMMONLY_USED"]},
        {"mpin": "3749", "user_dob": "", "spouse_dob": "", "anniversary": "", "expected_strength": "STRONG", "expected_reasons": []},
        {"mpin": "0201", "user_dob": "02/01/1998", "spouse_dob": "", "anniversary": "", "expected_strength": "WEAK", "expected_reasons": ["DEMOGRAPHIC_DOB_SELF"]},
        {"mpin": "9802", "user_dob": "02/01/1998", "spouse_dob": "", "anniversary": "", "expected_strength": "WEAK", "expected_reasons": ["DEMOGRAPHIC_DOB_SELF"]},
        {"mpin": "0102", "user_dob": "02/01/1998", "spouse_dob": "", "anniversary": "", "expected_strength": "STRONG", "expected_reasons": []},
        {"mpin": "0201", "user_dob": "", "spouse_dob": "02/01/1999", "anniversary": "", "expected_strength": "WEAK", "expected_reasons": ["DEMOGRAPHIC_DOB_SPOUSE"]},
        {"mpin": "3110", "user_dob": "", "spouse_dob": "", "anniversary": "31/10/2020", "expected_strength": "WEAK", "expected_reasons": ["DEMOGRAPHIC_ANNIVERSARY"]},
        {"mpin": "1111", "user_dob": "11/11/2011", "spouse_dob": "11/11/2012", "anniversary": "11/11/2013", "expected_strength": "WEAK",
         "expected_reasons": ["COMMONLY_USED", "REPEATED_PATTERN", "DEMOGRAPHIC_DOB_SELF", "DEMOGRAPHIC_DOB_SPOUSE", "DEMOGRAPHIC_ANNIVERSARY"]},
        {"mpin": "123456", "user_dob": "", "spouse_dob": "", "anniversary": "", "expected_strength": "WEAK", "expected_reasons": ["COMMONLY_USED"]},
        {"mpin": "111111", "user_dob": "", "spouse_dob": "", "anniversary": "", "expected_strength": "WEAK", "expected_reasons": ["COMMONLY_USED", "REPEATED_PATTERN"]},
        {"mpin": "101010", "user_dob": "", "spouse_dob": "", "anniversary": "", "expected_strength": "WEAK", "expected_reasons": ["COMMONLY_USED"]},
        {"mpin": "654321", "user_dob": "", "spouse_dob": "", "anniversary": "", "expected_strength": "WEAK", "expected_reasons": ["COMMONLY_USED"]},
        {"mpin": "827364", "user_dob": "01/01/2000", "spouse_dob": "02/02/2002", "anniversary": "03/03/2003", "expected_strength": "STRONG", "expected_reasons": []},
        {"mpin": "123", "user_dob": "", "spouse_dob": "", "anniversary": "", "expected_strength": "WEAK", "expected_reasons": []},
    ]

    for i, case in enumerate(test_cases):
        res = analyze_mpin(case["mpin"], case["user_dob"], case["spouse_dob"], case["anniversary"])
        # Map reasons to formatted messages
        actual_reasons = [REASON_MESSAGES.get(code, code) for code in res["reasons"]]
        test_name = f"Test case {i+1} - MPIN: {case['mpin']}"

        assert_equal(res["strength"], case["expected_strength"], f"{test_name} - Strength")
        assert_equal(set(actual_reasons), set(case["expected_reasons"]), f"{test_name} - Reasons")

    return "\n".join(output)

if __name__ == "__main__":
    threading.Timer(1.0, open_browser).start()
    app.run(debug=True)
