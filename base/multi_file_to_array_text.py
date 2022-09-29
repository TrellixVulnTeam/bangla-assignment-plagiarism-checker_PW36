from base.pdf_convertier import PdfConvertre


class MultiFile:

    
    def convert_pdf_to_text_from_all_files(self, files):
        pdfs = files
        items_lists = []
        for pdf in pdfs:
            text = PdfConvertre.converter(pdf)
            name = pdf.name
            dic = {'name': name, 'text_array': text}
            items_lists.append(dic)
        return items_lists
