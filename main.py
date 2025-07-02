# --- Importing Required Libraries ---
import streamlit as st          # For GUI interface
from fpdf import FPDF           # For PDF generation
import qrcode                   # To create QR codes for GitHub and LinkedIn
import tempfile                 # To create temporary file for PDF
import base64                   # To convert PDF to downloadable base64 link
import os                       # For file/folder operations
import re                       # For validating user input using regular expressions

# --- Streamlit Page Setup ---
st.set_page_config(page_title="Resume Builder", layout="wide", page_icon="📄")

# --- Custom Dark Theme CSS ---
css = """
<style>
    .stApp { background-color: #1e1e1e; color: white; }
    textarea, input, .stTextInput > div > div > input,
    .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {
        background-color: #2c2f33 !important;
        color: white !important;
    }
    h1, h2, h3, h4, h5, h6, p, label {
        color: white !important;
    }
    button[kind="primary"] {
        background-color: #3a3a3a !important;
        color: white !important;
        border: 1px solid #555 !important;
    }
    .stSlider > div[data-baseweb="slider"] {
        background-color: #3a3a3a !important;
    }
</style>
"""
st.markdown(css, unsafe_allow_html=True)

# --- Sidebar Options ---
st.sidebar.title("Options")
selected_template = st.sidebar.selectbox("Choose Resume Template", ["Classic", "Modern"])  # Template selector
font_style = st.sidebar.selectbox("Choose Font", ["Arial", "Times", "Courier"])           # Font selector

# --- Function to Set Font Safely in PDF ---
def safe_set_font(pdf, font, style='', size=12):
    try:
        pdf.set_font(font, style, size)     # Set font if available
    except RuntimeError:
        pdf.set_font("Arial", style, size)  # Fallback to Arial

# -------------------- Main Input Section --------------------
col1, col2 = st.columns([1.2, 1])  # Split screen into input (left) and preview (right)

with col1:
    st.title("📄 Resume Builder")

    # --- Contact Details ---
    name = st.text_input("Full Name")
    title = st.text_input("Professional Title (e.g. Software Developer)")
    email = st.text_input("Email")
    phone = st.text_input("Phone")
    linkedin = st.text_input("LinkedIn URL")
    github = st.text_input("GitHub URL")

    # --- Input Validations ---
    email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    if name and not re.fullmatch(r"[A-Za-z\s]+", name):
        st.warning("⚠️ Name should contain only letters and spaces.")
    if email and not re.fullmatch(email_pattern, email):
        st.warning("⚠️ Please enter a valid email address.")
    if phone and (not phone.isdigit() or len(phone) != 10):
        st.warning("⚠️ Phone number must be exactly 10 digits and contain digits only.")
        import re

        # LinkedIn URL check
    linkedin_pattern = r"^https:\/\/(www\.)?linkedin\.com\/in\/[A-Za-z0-9-_%]+\/?$"
    if linkedin and not re.match(linkedin_pattern, linkedin):
         st.warning("⚠️ Please enter a valid LinkedIn profile URL (e.g., https://www.linkedin.com/in/yourname)")
    # --- GitHub URL validation ---
    github_pattern = r"^https:\/\/(www\.)?github\.com\/[A-Za-z0-9-_%]+\/?$"
    if github and not re.match(github_pattern, github):
        st.warning("⚠️ Please enter a valid GitHub profile URL (e.g., https://github.com/yourusername)")

    # --- Education Section ---
    st.subheader("Education")
    edu_count = st.number_input("Number of education entries", min_value=1, max_value=5, value=1)
    education = []
    for i in range(edu_count):
        degree = st.text_input(f"Degree #{i+1}", key=f"deg{i}")
        institute = st.text_input(f"Institute #{i+1}", key=f"inst{i}")
        year = st.text_input(f"Year #{i+1}", key=f"year{i}")
        desc = st.text_area(f"Description #{i+1}", key=f"edesc{i}")
        if degree or institute or year or desc:
            education.append((degree, institute, year, desc))  # Store tuple in list

    # --- Experience Section ---
    st.subheader("Experience")
    is_fresher = st.checkbox("I am a fresher and have no work experience")
    experiences = []
    if not is_fresher:
        exp_count = st.number_input("Number of experience entries", min_value=1, max_value=5, value=1)
        for i in range(exp_count):
            company = st.text_input(f"Company #{i+1}", key=f"comp{i}")
            role = st.text_input(f"Role #{i+1}", key=f"role{i}")
            duration = st.text_input(f"Duration #{i+1}", key=f"dur{i}")
            desc = st.text_area(f"Description #{i+1}", key=f"desc{i}")
            if company or role or duration or desc:
                experiences.append((company, role, duration, desc))

    # --- Skills Section ---
    st.subheader("Skills")
    skills = st.text_area("List your skills")  # One per line

    # --- Certifications Section ---
    st.subheader("Certifications")
    certs = st.text_area("List your certifications")

    # --- Projects Section ---
    st.subheader("💻 Projects")
    proj_count = st.number_input("Number of projects", min_value=1, max_value=5, value=1)
    projects = []
    for i in range(proj_count):
        proj_title = st.text_input(f"Project #{i+1} Title", key=f"proj{i}")
        proj_desc = st.text_area(f"Project #{i+1} Description", key=f"projdesc{i}")
        if proj_title or proj_desc:
            projects.append((proj_title, proj_desc))

    # --- Languages Section ---
    st.subheader("🌐 Languages Known")
    languages = st.text_area("List languages")

    # --- Custom Additional Section ---
    st.subheader("➕ Additional Section")
    custom_title = st.text_input("Section Title")
    custom_content = st.text_area("Section Content")

    # --- Filename & Generate Button ---
    filename = st.text_input("Filename", value="resume")
    save_dir = st.text_input("Folder to save in (optional)")
    generate = st.button("Generate PDF")

# -------------------- Live Resume Preview (Right Column) --------------------
with col2:
    st.subheader("Live Preview")
    st.markdown(f"### {name}")
    if title: st.markdown(f"*{title}*")
    st.markdown(f"**Email:** {email}")
    st.markdown(f"**Phone:** {phone}")
    st.markdown(f"**LinkedIn:** {linkedin}")
    st.markdown(f"**GitHub:** {github}")

    if education:
        st.markdown("### Education")
        for deg, inst, year, desc in education:
            st.markdown(f"**{deg}**, {inst} ({year})")
            for line in desc.splitlines():
                st.markdown(f"- {line.strip()}")

    if is_fresher:
        st.markdown("### Experience")
        st.markdown("*Looking for opportunities as a fresher.*")
    elif experiences:
        st.markdown("### Experience")
        for comp, role, dur, desc in experiences:
            st.markdown(f"**{role}**, {comp} ({dur})")
            for line in desc.splitlines():
                st.markdown(f"- {line.strip()}")

    if skills.strip():
        st.markdown("### 🛠 Skills")
        for skill in skills.splitlines():
            if skill.strip():
                st.markdown(f"- {skill.strip()}")

    if certs.strip():
        st.markdown("### Certifications")
        for cert in certs.splitlines():
            if cert.strip():
                st.markdown(f"- {cert.strip()}")

    if projects:
        st.markdown("### 💻 Projects")
        for proj, desc in projects:
            st.markdown(f"**{proj.strip()}**")
            for line in desc.splitlines():
                st.markdown(f"- {line.strip()}")

    if languages.strip():
        st.markdown("### 🌐 Languages")
        for lang in languages.splitlines():
            if lang.strip():
                st.markdown(f"- {lang.strip()}")

    if custom_title and custom_content.strip():
        st.markdown(f"### {custom_title}")
        for line in custom_content.splitlines():
            st.markdown(f"- {line.strip()}")

# -------------------- PDF Generation Logic --------------------
valid_inputs = (
    re.fullmatch(r"[A-Za-z\s]+", name or "") and
    (phone.isdigit() if phone else False) and
    re.fullmatch(email_pattern, email or "")
)

if generate:
    if not valid_inputs:
        st.error("🚫 Please correct invalid inputs before generating the PDF.")
    else:
        pdf = FPDF("P", "mm", "A4")
        pdf.set_auto_page_break(auto=False)
        pdf.add_page()

        # --- Helper Functions for Sections ---
        def section(title):
            safe_set_font(pdf, font_style, 'B', 11)
            pdf.cell(200, 6, txt=title, ln=True)
            safe_set_font(pdf, font_style, '', 9)

        def bullet(text):
            for line in text.splitlines():
                if line.strip():
                    pdf.cell(200, 5, f"- {line.strip()}", ln=True)

        # --- PDF Header ---
        pdf.set_text_color(0, 0, 0)
        safe_set_font(pdf, font_style, 'B', 16)
        pdf.cell(200, 8, txt=name.upper(), ln=True, align='C')
        if title:
            safe_set_font(pdf, font_style, 'I', 10)
            pdf.cell(200, 5, txt=title, ln=True, align='C')
        pdf.line(60, pdf.get_y(), 150, pdf.get_y())  # Horizontal line
        pdf.ln(3)

        # --- Contact Info ---
        safe_set_font(pdf, font_style, '', 9)
        if email: pdf.cell(200, 5, f"Email: {email}", ln=True)
        if phone: pdf.cell(200, 5, f"Phone: {phone}", ln=True)
        if linkedin: pdf.cell(200, 5, f"LinkedIn: {linkedin}", ln=True)
        if github: pdf.cell(200, 5, f"GitHub: {github}", ln=True)
        pdf.ln(1)

        # --- Education Section in PDF ---
        if education:
            section("Education")
            for deg, inst, year, desc in education:
                pdf.cell(200, 5, f"{deg}, {inst} ({year})", ln=True)
                bullet(desc)

        # --- Experience Section in PDF ---
        section("Experience")
        if is_fresher:
            pdf.cell(200, 5, "Looking for opportunities as a fresher.", ln=True)
        else:
            for comp, role, dur, desc in experiences:
                pdf.cell(200, 5, f"{role} at {comp} ({dur})", ln=True)
                bullet(desc)

        # --- Skills, Certs, Projects, Languages ---
        if skills.strip():
            section("Skills")
            bullet(skills)
        if certs.strip():
            section("Certifications")
            bullet(certs)
        if projects:
            section("Projects")
            for proj, desc in projects:
                pdf.cell(200, 5, f"{proj.strip()}", ln=True)
                bullet(desc)
        if languages.strip():
            section("Languages")
            bullet(languages)

        # --- Custom Section if provided ---
        if custom_title and custom_content.strip():
            section(custom_title)
            bullet(custom_content)

        # --- QR Code Generation (LinkedIn and GitHub) ---
        try:
            qr_y = pdf.h - 35  # Position QR codes near bottom of page
            if github:
                qr1 = qrcode.make(github)
                path1 = "qr_github.png"
                qr1.save(path1)
                pdf.image(path1, x=10, y=qr_y, w=20)
                os.remove(path1)
            if linkedin:
                qr2 = qrcode.make(linkedin)
                path2 = "qr_linkedin.png"
                qr2.save(path2)
                pdf.image(path2, x=40, y=qr_y, w=20)
                os.remove(path2)
        except Exception as e:
            st.warning(f"⚠️ Error handling QR codes: {e}")

        # --- Saving the PDF ---
        if save_dir:
            os.makedirs(save_dir, exist_ok=True)
            save_path = os.path.join(save_dir, f"{filename}.pdf")
        else:
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
            save_path = tmp.name

        pdf.output(save_path)

        # --- PDF Download Link using base64 encoding ---
        with open(save_path, "rb") as f: #read binary ("rb") mode.
            b64 = base64.b64encode(f.read()).decode()
            href = f'<a href="data:application/pdf;base64,{b64}" download="{filename}.pdf">📅 Download Resume</a>'
            st.markdown(f"<div style='text-align:center'>{href}</div>", unsafe_allow_html=True)

        st.success("✅ Resume generated!")
