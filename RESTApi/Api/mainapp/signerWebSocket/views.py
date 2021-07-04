import base64
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from ..signCreation.models import UserSign, UserSignText, UserSignImage
from ..fileSystem.models import FilesModel
from ..authentication.models import User

rev_dic = {
    "TL": "Top Left",
    "TR": "Top Right",
    "BL": "Bottom Left",
    "BR": "Bottom Right"
}

@authentication_classes([])
@permission_classes([])
class FileSendView(APIView):

    # parser_class = (FileUploadParser,)
    # parser_classes = (FormParser, MultiPartParser,)

#     {
#     "PdfFile": "Base64 string of Pdf File Byte Array",
#     "PageToSign": "First/Last",
#     "PositionOnPage": "Top Right/Top Left/ Bottom Right/Bottom Left",
#     "VisibleText": "",
#     "VisibleTextFont": "",
#     "SignImage": "Base64 string of Sign Image File Byte Array"
# }

    @staticmethod
    def post(request):   

        sign_type = request.data['Type']
        sign_id = request.data['Sign']
        file_id = request.data['File']

        File = FilesModel.objects.get(pk = file_id) 
        File_data = File.File
        
        response = Response()
        # get sign details
        vis_text = None
        vis_img = None

        if sign_type == 'Text':
            # txt_sign = UserSignText.objects.get(pk = sign_id)
            # sign = UserSign.objects.get(pk = txt_sign.Sign_id)
            sign = UserSign.objects.get(pk = sign_id)
            txt_sign = UserSignText.objects.get(Sign = sign)
            vis_text = txt_sign.VisText
        
        elif sign_type == 'Image':
            # img_sign = UserSignImage.objects.get(pk = sign_id)
            # sign = UserSign.objects.get(pk = img_sign.Sign_id)
            sign = UserSign.objects.get(pk = sign_id)
            img_sign = UserSignImage.objects.get(Sign = sign)
            img_path = 'media/'+ str(img_sign.VisImage)
            with open(img_path, "rb") as img_enc:
                vis_img = base64.b64encode(img_enc.read()) 
 
        file_path = 'media/'+ str(File_data) 
        with open(file_path, "rb") as pdf_file:
            encoded_string = base64.b64encode(pdf_file.read())

        
        response.data = {
            "PdfFile": encoded_string,
            "PageToSign": sign.SignPage,
            "PositionOnPage": rev_dic[sign.SignPosition],
            "VisibleText": vis_text,
            "SignImage": vis_img
        }
        return response