import crcmod
import qrcode
from PIL import Image
import io
import win32clipboard

class Payload:
    def __init__(self, nome, chavePix, valor, cidade, textId):
        self.nome = nome
        self.chavePix = chavePix
        self.valor = valor
        self.cidade = cidade
        self.textId = textId

        self.nome_tam = len(self.nome)
        self.chavePix_tam = len(self.chavePix)
        self.valor_tam = len(self.valor)
        self.cidade_tam = len(self.cidade)
        self.textId_tam = len(self.textId)
        self.merchantAccount_tam = f"0014BR.GOV.BCB.PIX01{self.chavePix_tam}{self.chavePix}"

        self.payloadFormat = "000201"
        self.merchantAccount = f"26{len(self.merchantAccount_tam)}{self.merchantAccount_tam}"

        if self.valor_tam <= 9:
            self.transactionAmount_tam = f"0{self.valor_tam}{self.valor}"
        else:
            self.transactionAmount_tam = f"{self.valor_tam}{self.valor}"
        if self.textId_tam <= 9:
            self.addDataField_tam = f"050{self.textId_tam}{self.textId}"
        else:
            self.addDataField_tam = f"05{self.textId_tam}{self.textId}"
        if self.nome_tam <= 9:
            self.nome_tam = f"0{self.nome_tam}"
        if self.cidade_tam <= 9:
            self.cidade_tam = f"0{self.cidade_tam}"

        self.merchantCateCod = "52040000"
        self.transactionCurrecy = "5303986"
        self.transactionAmount = f"54{self.transactionAmount_tam}"
        self.countryCode = "5802BR"
        self.merchantName = f"59{self.nome_tam}{self.nome}"
        self.merchantCity = f"60{self.cidade_tam}{self.cidade}"
        self.addDataField = f"62{len(self.addDataField_tam)}{self.addDataField_tam}"
        self.crc16 = "6304"

    def generatePayload(self):
        self.payload = f"{self.payloadFormat}{self.merchantAccount}{self.merchantCateCod}{self.transactionCurrecy}{self.transactionAmount}{self.countryCode}{self.merchantName}{self.merchantCity}{self.addDataField}{self.crc16}"

        self.generateCrc16(self.payload)

    def generateCrc16(self, payload):
        crc16 = crcmod.mkCrcFun(poly=0x11021, initCrc=0xFFFF, rev=False, xorOut=0x0000)
        self.crc16Code = hex(crc16(str(payload).encode("utf-8")))

        self.crc16Code_formated = str(self.crc16Code).replace("0x", "").upper()
        self.completePayload = f"{payload}{self.crc16Code_formated}"

        self.generateQrCode(self.completePayload)
        return self.completePayload

    def generateQrCode(self, payload):
        qr = qrcode.make(payload)
        output = io.BytesIO()
        qr.save(output, format="PNG")
        output.seek(0)
        self.send_to_clipboard(output)
        

    def send_to_clipboard(self, image_data):
        image = Image.open(image_data)
        with io.BytesIO() as output:
            image.convert("RGB").save(output, "BMP")
            data = output.getvalue()[14:]
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
            win32clipboard.CloseClipboard()

payload = Payload.generateCrc16

#if __name__ == "__main__":
 #   p = Payload("vinicius miguel", "+5581989945697", "10.00", "bezerros", "loja01")
 #   p.generatePayload()
