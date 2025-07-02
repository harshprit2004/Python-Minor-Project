
# 📄 Streamlit Resume Builder

This is a fully functional Resume Builder app built using **Python** and **Streamlit**. It allows users to input their professional and educational information, choose a resume template and font style, preview the resume live, and generate a **PDF resume** with QR codes for LinkedIn and GitHub profiles.

## 🚀 Features

- Streamlit-based modern UI with a dark theme.
- Custom font and resume template selector.
- Real-time resume preview while filling out information.
- Add sections like:
  - Contact Info
  - Education
  - Experience
  - Skills
  - Certifications
  - Projects
  - Languages
  - Custom Sections
- Validations for Email, Phone Number, LinkedIn, and GitHub URLs.
- Generates a downloadable PDF.
- Adds QR codes for LinkedIn and GitHub profile links.

## 🛠 Technologies Used

- Python 3.x
- Streamlit
- fpdf
- qrcode
- base64
- tempfile
- os, re (standard libraries)

## ▶️ How to Run

1. Install dependencies:

```
pip install streamlit fpdf qrcode[pil]
```

2. Run the Streamlit app:

```
streamlit run resume_builder.py
```

3. Fill in the form, preview your resume live, and click **Generate PDF**.

4. Download your resume from the provided link.

## 📁 File Structure

- `resume_builder.py` - Main application file.
- `README.md` - This file.

## 📦 Output

A downloadable `.pdf` resume file saved locally or through temporary download link.

## 🧾 License

This project is licensed for educational and personal use.

---
Happy Resume Building! 💼
