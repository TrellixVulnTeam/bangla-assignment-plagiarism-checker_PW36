from base.pdf_convertier import PdfConvertre
from base.plagarism_checker import PlagiarismChecker

class MultiFile:

    def __init__(self, files) -> None:
        self.files = files

    def convert_pdf_to_text_from_all_files(self):
        pdfs = self.files
        items_lists = []
        for pdf in pdfs:
            text = PdfConvertre.converter(pdf)
            name = pdf.name
            dic = {'name': name, 'text_array': text}
            items_lists.append(dic)
        return items_lists

    def checking_plug_all_files(self, array_lists):
        result = []
        for index in range(0,len(array_lists)):
            for j in range((index + 1),len(array_lists)):
                pdfPlag = PlagiarismChecker()
                similerText = pdfPlag.santenceSimilarity(array_lists[index]['text_array'], array_lists[j]['text_array'])
                percentage = pdfPlag.percentageOfText(array_lists[index]['text_array'], array_lists[j]['text_array'])
                dic = {'between':array_lists[index]['name'] + " " + array_lists[j]['name'],'text':similerText, 'percen': percentage}
                result.append(dic)
        return result
    
    def multifilePlugCheck(self):
        return self.checking_plug_all_files(self.convert_pdf_to_text_from_all_files())
 