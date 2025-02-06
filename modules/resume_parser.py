import pdfplumber
import re

__all__ = ['extract_text_from_pdf']

def extract_name(text):
    """
    Extracts name from the resume text (assuming the first line contains the name).
    :param text: Full resume text.
    :return: Name as a string.
    """
    lines = text.strip().split('\n')
    return lines[0].strip() if lines else ""

def extract_email(text):
    """
    Extracts email address from the resume text.
    :param text: Full resume text.
    :return: Email as a string.
    """
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    match = re.search(email_pattern, text)
    return match.group() if match else ""

def extract_phone(text):
    """
    Extracts phone number from the resume text.
    :param text: Full resume text.
    :return: Phone number as a string.
    """
    phone_pattern = r'(\+\d{1,3}[-.]?)?\s*\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
    match = re.search(phone_pattern, text)
    return match.group() if match else ""

def extract_yop(text):
    """
    Extracts the year of passing (YOP) from the resume text.
    :param text: Full resume text.
    :return: Year of Passing as a string.
    """
    yop_pattern = r'20[0-2]\d'  # Matches years from 2000-2029
    match = re.search(yop_pattern, text)
    return match.group() if match else ""

def extract_skills(text):
    """
    Extracts skills from the resume text based on a predefined list.
    :param text: Full resume text.
    :return: List of skills found.
    """
    # Common programming languages and technologies
    skills_list = ['Python', 'Java', 'JavaScript', 'C++', 'SQL', 'HTML', 'CSS',
                   'React', 'Angular', 'Node.js', 'Docker', 'AWS', 'Git']
    found_skills = []
    for skill in skills_list:
        if re.search(r'\b' + re.escape(skill) + r'\b', text, re.IGNORECASE):
            found_skills.append(skill)
    return found_skills

def extract_experience(text):
    """
    Extracts work experience from the resume text.
    :param text: Full resume text.
    :return: List of experiences (years of experience or job descriptions).
    """
    exp_pattern = r'\d+(?:\.\d+)?\s*(?:years?|yrs?)'
    matches = re.finditer(exp_pattern, text, re.IGNORECASE)
    return [match.group() for match in matches] if matches else []

def extract_certifications(text):
    """
    Extracts certifications from the resume text.
    :param text: Full resume text.
    :return: List of certifications.
    """
    # Keywords that indicate certifications
    cert_keywords = [
        'certified', 'certification', 'certificate', 'credential',
        'awarded', 'earned', 'completed'
    ]
    
    # Keywords that indicate education (to exclude)
    education_keywords = [
        'school', 'college', 'university', 'institute', 'vidyalaya',
        'secondary', 'higher secondary', 'hsc', 'ssc', 'cbse', 'icse',
        'bachelor', 'master', 'degree', 'diploma'
    ]
    
    lines = text.split('\n')
    certs = []
    
    for line in lines:
        line = line.strip().lower()
        # Check if line contains certification keywords
        has_cert_keyword = any(keyword in line for keyword in cert_keywords)
        # Check if line contains education keywords
        has_edu_keyword = any(keyword in line for keyword in education_keywords)
        
        # Only include if it has certification keywords but not education keywords
        if has_cert_keyword and not has_edu_keyword:
            # Get the original case version of the line
            original_line = next(ol for ol in text.split('\n') if ol.strip().lower() == line)
            certs.append(original_line.strip())
    
    return certs if certs else []

def extract_text_from_pdf(file_path):
    """
    Extracts and processes relevant details from a PDF resume.
    :param file_path: Path to the PDF file.
    :return: Dictionary with extracted details.
    """
    with pdfplumber.open(file_path) as pdf:
        full_text = " ".join(page.extract_text() for page in pdf.pages if page.extract_text())

    # Extract specific details
    details = {
        "Name": extract_name(full_text),
        "Email": extract_email(full_text),
        "Phone": extract_phone(full_text),
        "Year of Passing (YOP)": extract_yop(full_text),
        "Skills": extract_skills(full_text),
        "Experience": extract_experience(full_text),
        "Certifications": extract_certifications(full_text)
    }

    return details
