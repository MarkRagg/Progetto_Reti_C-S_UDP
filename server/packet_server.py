# -*- coding: utf-8 -*-
"""
Created on Tue May 17 09:15:33 2022

@author: huawei
"""

import hashlib

class Packet :

    def __init__(self, number, body) :
        self.packet_number = number
        self.body = body
        self.checksum = hashlib.md5(body).digest()
        
    def compare_checksum(ck1, ck2) :
        return ck1 == ck2
    

