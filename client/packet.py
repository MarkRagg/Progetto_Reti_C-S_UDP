import hashlib

class Packet :

    def __init__(self, number, body) :
        self.packet_number = number
        self.body = body
        self.checksum = hashlib.md5(body).digest()
        
    def compare_checksum(ck1, ck2) :
        return ck1 == ck2
    

