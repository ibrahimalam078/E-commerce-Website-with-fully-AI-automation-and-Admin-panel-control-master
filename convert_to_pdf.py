#!/usr/bin/env python3
"""
Convert markdown project description to PDF
"""
import markdown
import weasyprint
from pathlib import Path

def convert_markdown_to_pdf(markdown_file, pdf_file):
    """Convert markdown file to PDF with styling"""
    
    # Read markdown content
    with open(markdown_file, 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    
    # Convert markdown to HTML
    md = markdown.Markdown(extensions=['codehilite', 'tables', 'toc'])
    html_content = md.convert(markdown_content)
    
    # Add CSS styling for professional look
    css_style = """
    <style>
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        line-height: 1.6;
        margin: 40px;
        color: #333;
        background-color: white;
    }
    
    h1 {
        color: #2c3e50;
        border-bottom: 3px solid #3498db;
        padding-bottom: 10px;
        margin-top: 30px;
        font-size: 28px;
    }
    
    h2 {
        color: #34495e;
        border-bottom: 2px solid #ecf0f1;
        padding-bottom: 8px;
        margin-top: 25px;
        font-size: 22px;
    }
    
    h3 {
        color: #2980b9;
        margin-top: 20px;
        font-size: 18px;
    }
    
    h4 {
        color: #27ae60;
        margin-top: 15px;
        font-size: 16px;
    }
    
    pre, code {
        background-color: #f8f9fa;
        border: 1px solid #e9ecef;
        border-radius: 4px;
        padding: 12px;
        font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
        font-size: 12px;
        overflow-x: auto;
    }
    
    pre {
        margin: 15px 0;
        white-space: pre-wrap;
    }
    
    code {
        padding: 2px 4px;
        display: inline;
    }
    
    blockquote {
        border-left: 4px solid #3498db;
        margin: 15px 0;
        padding: 10px 20px;
        background-color: #ecf0f1;
        font-style: italic;
    }
    
    ul, ol {
        margin: 10px 0;
        padding-left: 30px;
    }
    
    li {
        margin: 5px 0;
    }
    
    table {
        border-collapse: collapse;
        width: 100%;
        margin: 15px 0;
    }
    
    th, td {
        border: 1px solid #ddd;
        padding: 8px;
        text-align: left;
    }
    
    th {
        background-color: #f2f2f2;
        font-weight: bold;
    }
    
    .emoji {
        font-size: 16px;
    }
    
    strong {
        color: #2c3e50;
        font-weight: 600;
    }
    
    .page-break {
        page-break-before: always;
    }
    
    .header-info {
        text-align: center;
        margin-bottom: 30px;
        padding: 20px;
        background-color: #f8f9fa;
        border-radius: 8px;
    }
    
    .footer-info {
        text-align: center;
        margin-top: 30px;
        padding: 15px;
        background-color: #2c3e50;
        color: white;
        border-radius: 8px;
        font-style: italic;
    }
    
    @page {
        size: A4;
        margin: 2cm;
        @top-center {
            content: "AI E-Commerce Automation System";
            font-size: 12px;
            color: #666;
        }
        @bottom-center {
            content: counter(page) " / " counter(pages);
            font-size: 10px;
            color: #666;
        }
    }
    </style>
    """
    
    # Create complete HTML document
    full_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AI-Powered E-Commerce Automation System</title>
        {css_style}
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """
    
    # Convert HTML to PDF
    print("Converting to PDF...")
    weasyprint.HTML(string=full_html).write_pdf(pdf_file)
    print(f"✅ PDF created successfully: {pdf_file}")

if __name__ == "__main__":
    # File paths
    markdown_file = "AI_ECOMMERCE_AUTOMATION_PROJECT_DESCRIPTION.md"
    pdf_file = "AI_ECOMMERCE_AUTOMATION_PROJECT_DESCRIPTION.pdf"
    
    # Check if markdown file exists
    if not Path(markdown_file).exists():
        print(f"❌ Markdown file not found: {markdown_file}")
        exit(1)
    
    try:
        convert_markdown_to_pdf(markdown_file, pdf_file)
        print(f"🎉 Conversion completed! PDF saved as: {pdf_file}")
    except Exception as e:
        print(f"❌ Error during conversion: {str(e)}")
        exit(1)
