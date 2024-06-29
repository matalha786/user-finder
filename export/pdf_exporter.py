from fpdf import FPDF
import os

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'User-Finder-Zeta Results', 0, 1, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, body)

def saveToPdf(results, result_type):
    pdf = PDF()
    pdf.add_page()
    pdf.chapter_title(f"{result_type.capitalize()} Search Results")
    for result in results:
        pdf.chapter_body(result)
    filename = os.path.join("results", f"{result_type}_results.pdf")
    pdf.output(filename)
