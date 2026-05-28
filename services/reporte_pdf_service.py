import os
from tkinter import messagebox, filedialog
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def exportar_treeview_a_pdf(treeview, titulo_reporte="Reporte de Operaciones Relacionales", expresion_algebraica=""):
    """
    Toma los datos visualizados actualmente en un Treeview (ya filtrados por el usuario)
    y los exporta a un documento PDF formal con diseño profesional.
    """
    # 1. Obtener los encabezados del Treeview
    columnas = [treeview.heading(col)["text"] for col in treeview["columns"]]
    if not columnas:
        messagebox.showwarning("Sin Datos", "No hay columnas configuradas para exportar.")
        return

    # 2. Obtener las filas visibles del Treeview
    filas = []
    for item in treeview.get_children():
        filas.append([str(valor) for valor in treeview.item(item)["values"]])
        
    if not filas:
        messagebox.showwarning("Sin Datos", "No hay registros en la tabla para exportar.")
        return

    # 3. Cuadro de diálogo para elegir dónde guardar el PDF
    ruta_guardado = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("Archivos PDF", "*.pdf")],
        title="Guardar Reporte Pamicell"
    )
    
    if not ruta_guardado:
        return # El usuario canceló el guardado

    try:
        # 4. Configurar el documento PDF (Tamaño Carta)
        doc = SimpleDocTemplate(
            ruta_guardado, 
            pagesize=letter,
            rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40
        )
        story = []
        
        # Estilos base
        styles = getSampleStyleSheet()
        
        # Estilos personalizados siguiendo la paleta Pamicell
        estilo_titulo = ParagraphStyle(
            'TituloPamicell',
            parent=styles['Heading1'],
            fontName='Helvetica-Bold',
            fontSize=22,
            textColor=colors.HexColor('#1f2022'),
            spaceAfter=6
        )
        
        estilo_subtitulo = ParagraphStyle(
            'SubtituloPamicell',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=10,
            textColor=colors.HexColor('#64748b'),
            spaceAfter=15
        )

        estilo_algebra = ParagraphStyle(
            'AlgebraStyle',
            parent=styles['Code'],
            fontName='Times-BoldItalic',
            fontSize=11,
            textColor=colors.HexColor('#2563eb'),
            backgroundColor=colors.HexColor('#f1f5f9'),
            borderPadding=8,
            spaceAfter=20
        )
        
        estilo_celda_header = ParagraphStyle(
            'CeldaHeader',
            fontName='Helvetica-Bold',
            fontSize=9,
            textColor=colors.white
        )
        
        estilo_celda_body = ParagraphStyle(
            'CeldaBody',
            fontName='Helvetica',
            fontSize=9,
            textColor=colors.HexColor('#111827')
        )

        # 5. Construcción del Contenido (Capa Estética)
        story.append(Paragraph("PAMICELL & CREDICELL", estilo_titulo))
        story.append(Paragraph(f"{titulo_reporte} — Módulo de Auditoría Analítica", estilo_subtitulo))
        story.append(Spacer(1, 10))
        
        # Inyección de la justificación matemática para la maestra de la UAA
        if expresion_algebraica:
            story.append(Paragraph(f"<b>Fórmula Relacional Equivalente:</b> {expresion_algebraica}", styles['Normal']))
            story.append(Spacer(1, 5))
            
        story.append(Spacer(1, 10))

        # 6. Preparación de la Tabla de Datos
        tabla_datos = []
        # Fila de Encabezados
        tabla_datos.append([Paragraph(col, estilo_celda_header) for col in columnas])
        # Filas de Registros
        for fila in filas:
            tabla_datos.append([Paragraph(celda, estilo_celda_body) for celda in fila])

        # Ancho elástico proporcional para las columnas
        tabla_pdf = Table(tabla_datos, hAlign='LEFT', repeatRows=1)
        
        # Estilo de la cuadrícula de datos
        estilo_tabla = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0f172a')), # Fondo oscuro para th
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('TOPPADDING', (0, 0), (-1, 0), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')), # Bordes grises sutiles
        ])
        
        # Zebra striping (Filas alternas claras para legibilidad)
        for i in range(1, len(filas) + 1):
            if i % 2 == 0:
                estilo_tabla.add('BACKGROUND', (0, i), (-1, i), colors.HexColor('#f8fafc'))
                
        tabla_pdf.setStyle(estilo_tabla)
        story.append(tabla_pdf)
        
        # 7. Construcción/Escritura física del archivo
        doc.build(story)
        messagebox.showinfo("Reporte Exportado", "El PDF se generó e imprimió correctamente.")
        
    except Exception as e:
        messagebox.showerror("Error de Impresión", f"No se pudo generar el PDF: {str(e)}")