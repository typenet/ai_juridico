from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph
import os

def generate_example_pdf():
    # Criar pasta pdfs se não existir
    pdfs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "pdfs")
    os.makedirs(pdfs_dir, exist_ok=True)
    
    # Caminho do arquivo
    output_path = os.path.join(pdfs_dir, "exemplo_contrato.pdf")
    
    # Criar o PDF
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter
    
    # Estilos
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=30
    )
    text_style = ParagraphStyle(
        'CustomText',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=12
    )
    
    # Título
    title = "CONTRATO DE PRESTAÇÃO DE SERVIÇOS"
    p = Paragraph(title, title_style)
    p.wrapOn(c, width-100, height)
    p.drawOn(c, 50, height-100)
    
    # Dados do contrato
    dados = [
        "CPF: 123.456.789-00",
        "Processo: 2024/0001",
        "Data: 15/04/2024",
        "Tipo: Contrato de Serviços",
        "Título: Contrato de Desenvolvimento de Software"
    ]
    
    y = height-150
    for dado in dados:
        p = Paragraph(dado, text_style)
        p.wrapOn(c, width-100, height)
        p.drawOn(c, 50, y)
        y -= 30
    
    # Texto do contrato
    texto = """
    Pelo presente instrumento particular, as partes abaixo qualificadas celebram o presente CONTRATO DE PRESTAÇÃO DE SERVIÇOS, que se regerá pelas cláusulas e condições seguintes:
    
    CLÁUSULA PRIMEIRA - DO OBJETO
    O CONTRATADO se obriga a prestar serviços de desenvolvimento de software conforme especificações acordadas entre as partes.
    
    CLÁUSULA SEGUNDA - DO PRAZO
    O presente contrato terá vigência de 12 (doze) meses, contados a partir da data de sua assinatura.
    
    CLÁUSULA TERCEIRA - DO VALOR
    O valor total dos serviços será de R$ 50.000,00 (cinquenta mil reais), a ser pago em 12 parcelas mensais.
    
    E por estarem assim justos e contratados, firmam o presente instrumento em duas vias de igual teor.
    """
    
    p = Paragraph(texto, text_style)
    p.wrapOn(c, width-100, height-300)
    p.drawOn(c, 50, y-50)
    
    # Salvar o PDF
    c.save()
    print(f"✅ PDF de exemplo gerado com sucesso: {output_path}")

if __name__ == "__main__":
    generate_example_pdf() 