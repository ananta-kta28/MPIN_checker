# 🔐 MPIN Strength Analyzer

This Flask-based web application evaluates the strength of a user-provided MPIN (4 or 6 digits) by checking if it's commonly used, based on user demographics, or follows predictable/repeated patterns. It is structured in progressive parts and includes automated test coverage for validation.

---

## 🚀 Features

### ✅ Part A: Commonly Used MPIN Check

* Checks if a 4-digit MPIN is part of a known list of commonly used and predictable values.
* Ignores any user demographic information at this stage.

### ✅ Part B: Basic Strength Analysis with Demographics

* Accepts user's:

  * **Date of Birth (Self)**
  * **Date of Birth (Spouse)**
  * **Anniversary**
* Returns **MPIN Strength** as `STRONG` or `WEAK`.

### ✅ Part C: Detailed Weakness Reasoning

* If strength is `WEAK`, the application provides a **list of reasons**:

  * `COMMONLY_USED`: Popular MPINs known to be insecure.
  * `REPEATED_PATTERN`: MPINs like `1111`, `1212`, etc.
  * `DEMOGRAPHIC_DOB_SELF`: Derived from user’s date of birth.
  * `DEMOGRAPHIC_DOB_SPOUSE`: Matches patterns from spouse’s DOB.
  * `DEMOGRAPHIC_ANNIVERSARY`: Matches anniversary-related values.

### ✅ Part D: 6-Digit MPIN Support

* All the above checks work seamlessly for both 4-digit and 6-digit MPINs.

### ✅ Test Suite

* Contains a built-in testing feature to validate multiple scenarios.
* Edge cases, common MPINs, demographic matches, and repeated patterns are covered.
* Output displayed directly in the web interface.

---

## 🛠 How It Works

1. User inputs an MPIN (4 or 6 digits).
2. Optional: Enter DOB (Self), DOB (Spouse), and Anniversary.
3. Click **Check MPIN Strength**.
4. Application returns:

   * Strength: `STRONG` or `WEAK`
   * Reasons (if weak): List of identifiers explaining why.

---

## 📂 Technologies Used

* Python
* Flask
* HTML/CSS (Jinja2 templates)
* `datetime` for pattern extraction
* In-browser test results via Flask route

---

## 🧪 Running Tests

1. Click on the **"Run Tests"** button in the UI.
2. The app will run a predefined suite of test scenarios.
3. Results will be shown below the form.

---

## ⚙️ Installation & Usage

1. **Clone the repository**

   ```bash
   git clone https://github.com/ananta-kta28/MPIN_checker.git
   cd MPIN_checker
   ```

2. **Set up a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   pip3 install Flask
   ```

3. **Run the application**

   ```bash
   python3 APP2.py #copy the file as pathname if giving error
   ```

4. **Access via browser**

   ```
   http://127.0.0.1:5000/
   ```

---

## 📄 Notes

* The code avoids hardcoded input values in the logic. All checks are dynamic based on user input.
* DOB formats accepted: `YYYY-MM-DD` or `DD/MM/YYYY`.

---

