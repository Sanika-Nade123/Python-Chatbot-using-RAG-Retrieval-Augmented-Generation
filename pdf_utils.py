from fpdf import FPDF
from datetime import datetime

def create_user_report_pdf(users):
    pdf = FPDF(orientation='L')  # Set to Landscape orientation
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "User Report", ln=True, align='C')
    pdf.ln(10)
    
    # Add headers with adjusted column widths
    pdf.set_font("Arial", "B", 12)
    col_widths = [60, 50, 100, 50]  # Adjusted widths for each column
    headers = ["Name", "User ID", "Email", "Phone"]
    
    for header, width in zip(headers, col_widths):
        pdf.cell(width, 10, header, 1)
    pdf.ln()
    
    # Add user data
    pdf.set_font("Arial", "", 11)  # Slightly smaller font for content
    for user in users:
        pdf.cell(col_widths[0], 10, user.name[:20], 1)  # Limit name length
        pdf.cell(col_widths[1], 10, user.user_id, 1)
        pdf.cell(col_widths[2], 10, user.email, 1)
        pdf.cell(col_widths[3], 10, user.phone, 1)
        pdf.ln()
    
    return pdf

def create_chat_history_pdf(chat_history, username):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, f"Chat History - {username}", ln=True, align='C')
    pdf.ln(10)
    
    pdf.set_font("Arial", "", 12)
    for chat in chat_history:
        # Timestamp
        pdf.set_font("Arial", "I", 10)
        pdf.cell(0, 10, f"Time: {chat.timestamp.strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
        
        # Question
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "Question:", ln=True)
        pdf.set_font("Arial", "", 12)
        pdf.multi_cell(0, 10, chat.message)
        pdf.ln(5)
        
        # Answer
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "Answer:", ln=True)
        pdf.set_font("Arial", "", 12)
        pdf.multi_cell(0, 10, chat.response)
        pdf.ln(10)
    
    return pdf