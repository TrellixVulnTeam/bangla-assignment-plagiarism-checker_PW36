from unittest import result
from base.pdf_convertier import PdfConvertre
from base.plagarism_checker import PlagiarismChecker


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

    
    def checking_plug_all_files(self, array_lists):
        result = []
        for index, i in enumerate(array_lists):
            for j in range((index + 1),len(array_lists)):
                pdfPlag = PlagiarismChecker()
                similerText = pdfPlag.santenceSimilarity(array_lists[index].text_array, array_lists[j].text_array)
                dic = {'between':array_lists[index].name + " " + array_lists[j].name,'text':similerText, 'percen': 20}
                result.append(dic)
            
        return result
 