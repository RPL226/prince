#!/usr/bin/python
# -*- coding: utf-8 -*-

#from bitstring import BitArray
from binascii import unhexlify, hexlify

class Prince:
    RC = (unhexlify('0000000000000000'),
          unhexlify('13198a2e03707344'),
          unhexlify('a4093822299f31d0'),
          unhexlify('082efa98ec4e6c89'),
          unhexlify('452821e638d01377'),
          unhexlify('be5466cf34e90c6c'),
          unhexlify('7ef84f78fd955cb1'),
          unhexlify('85840851f1ac43aa'),
          unhexlify('c882d32f25323c54'),
          unhexlify('64a51195e0e3610d'),
          unhexlify('d3b5a399ca0c2399'),
          unhexlify('c0ac29b7c97c50dd'))

#    S = ('0xb', '0xf', '0x3', '0x2', '0xa', '0xc', '0x9', '0x1',
#         '0x6', '0x7', '0x8', '0x0', '0xe', '0x5', '0xd', '0x4')

    S = ([1,0,1,1], [1,1,1,1], [0,0,1,1], [0,0,1,0], [1,0,1,0], [1,1,0,0], [1,0,0,1], [0,0,0,1],
         [0,1,1,0], [0,1,1,1], [1,0,0,0], [0,0,0,0], [1,1,1,0], [0,1,0,1], [1,1,0,1], [0,1,0,0])

#    Sinv = ('0xb', '0x7', '0x3', '0x2', '0xf', '0xd', '0x8', '0x9',
#            '0xa', '0x6', '0x4', '0x0', '0x5', '0xe', '0xc', '0x1')

    Sinv = ([1,0,1,1], [0,1,1,1], [0,0,1,1], [0,0,1,0], [1,1,1,1], [1,1,0,1], [1,0,0,0], [1,0,0,1],
            [1,0,1,0], [0,1,1,0], [0,1,0,0], [0,0,0,0], [0,1,0,1], [1,1,1,0], [1,1,0,0], [0,0,0,1])

    from_nib = ([0,0,0,0], [0,0,0,1], [0,0,1,0], [0,0,1,1], [0,1,0,0], [0,1,0,1], [0,1,1,0], [0,1,1,1],
                [1,0,0,0], [1,0,0,1], [1,0,1,0], [1,0,1,1], [1,1,0,0], [1,1,0,1], [1,1,1,0], [1,1,1,1])

    #shift_rows = (00, 05, 10, 15, 04, 09, 14, 03, 08, 13, 02, 07, 12, 01, 06, 11)

    def list_xor(self, l1, l2):
      output = []
      if len(l1) != len(l2):
        print("ERROR list xor: input lists of unequal length")
        quit()
      for i in range(0, len(l1)):
        output.append(l1[i] ^ l2[i])
      return output


    def make_bit_array(self, data):
      out = []

      for i in range(0, len(data)):
        temp = data[i]
        byte = []
        for j in range(0, 8):
          byte = [temp & 1] + byte
          temp = temp >> 1
        out = out + byte

      return out


    def sbox(self, data, box):
        ret = []
        #for nibble in data.cut(4):
            #ret.append(box[int(nibble.hex, 16)])
        i = 0
        while i < len(data):
          nib = ((((((data[i] << 1) + data[i+1]) << 1) + data[i+2]) << 1) + data[i+3])
          ret += box[nib]
          i += 4
        return ret


    def m0(self, data):
        ret = [0] * 16
        ret[ 0] = data[4] ^ data[ 8] ^ data[12]
        ret[ 1] = data[1] ^ data[ 9] ^ data[13]
        ret[ 2] = data[2] ^ data[ 6] ^ data[14]
        ret[ 3] = data[3] ^ data[ 7] ^ data[11]
        ret[ 4] = data[0] ^ data[ 4] ^ data[ 8]
        ret[ 5] = data[5] ^ data[ 9] ^ data[13]
        ret[ 6] = data[2] ^ data[10] ^ data[14]
        ret[ 7] = data[3] ^ data[ 7] ^ data[15]
        ret[ 8] = data[0] ^ data[ 4] ^ data[12]
        ret[ 9] = data[1] ^ data[ 5] ^ data[ 9]
        ret[10] = data[6] ^ data[10] ^ data[14]
        ret[11] = data[3] ^ data[11] ^ data[15]
        ret[12] = data[0] ^ data[ 8] ^ data[12]
        ret[13] = data[1] ^ data[ 5] ^ data[13]
        ret[14] = data[2] ^ data[ 6] ^ data[10]
        ret[15] = data[7] ^ data[11] ^ data[15]
        return ret


    def m1(self, data):
        ret = [0] * 16
        ret[ 0] = data[0] ^ data[ 4] ^ data[ 8]
        ret[ 1] = data[5] ^ data[ 9] ^ data[13]
        ret[ 2] = data[2] ^ data[10] ^ data[14]
        ret[ 3] = data[3] ^ data[ 7] ^ data[15]
        ret[ 4] = data[0] ^ data[ 4] ^ data[12]
        ret[ 5] = data[1] ^ data[ 5] ^ data[ 9]
        ret[ 6] = data[6] ^ data[10] ^ data[14]
        ret[ 7] = data[3] ^ data[11] ^ data[15]
        ret[ 8] = data[0] ^ data[ 8] ^ data[12]
        ret[ 9] = data[1] ^ data[ 5] ^ data[13]
        ret[10] = data[2] ^ data[ 6] ^ data[10]
        ret[11] = data[7] ^ data[11] ^ data[15]
        ret[12] = data[4] ^ data[ 8] ^ data[12]
        ret[13] = data[1] ^ data[ 9] ^ data[13]
        ret[14] = data[2] ^ data[ 6] ^ data[14]
        ret[15] = data[3] ^ data[ 7] ^ data[11]
        return ret


    def shiftrows(self, data, inverse):
        #ret = BitArray(length = 64)
        ret = [0] * 64
        idx = 0
        i = 0
        while i < len(data):
          #nib = ((((((data[i] << 1) + data[i+1]) << 1) + data[i+2]) << 1) + data[i+3])
          nib = data[i:i+4]
          ret[idx * 4:(idx + 1) * 4] = nib
          if not inverse:
            idx = (idx + 13) % 16
          else:
            idx = (idx +  5) % 16
          i += 4

        #for nibble in data.cut(4):
            #ret[idx * 4:(idx + 1) * 4] = nibble
            #if not inverse:
                #idx = (idx + 13) % 16
            #else:
                #idx = (idx +  5) % 16

        #out = []
        #for i in range(0, len(ret)):
          #out += Prince.from_nib[ret[i]]
        #return out
        return ret



    def mprime(self, data):
        #ret = BitArray(length = 64)
        ret = [0] * 64
        ret[ 0:16] = self.m0(data[ 0:16])
        ret[16:32] = self.m1(data[16:32])
        ret[32:48] = self.m1(data[32:48])
        ret[48:64] = self.m0(data[48:64])
        return ret


    def firstrounds(self, data, key):
        for idx in (1,2,3,4,5):
            data = self.sbox(data, Prince.S)
            data = self.mprime(data)
            data = self.shiftrows(data, inverse = False)
            #data ^= Prince.RC[idx] ^ key
            round_key = self.list_xor(key, self.make_bit_array(Prince.RC[idx]))
            data = self.list_xor(data, round_key)
        return data


    def lastrounds(self, data, key):
        for idx in (6,7,8,9,10):
            #data ^= key ^ Prince.RC[idx]
            round_key = self.list_xor(key, self.make_bit_array(Prince.RC[idx]))
            data = self.list_xor(data, round_key)
            data = self.shiftrows(data, inverse = True)
            data = self.mprime(data)
            data = self.sbox(data, Prince.Sinv)
        return data


    def princecore(self, data, key):
        #data ^= key ^ Prince.RC[0]
        first_round_key = self.list_xor(key, self.make_bit_array(Prince.RC[0]))
        #print("xored key and rc[0]")
        data = self.list_xor(first_round_key, data)
        #print("xored first_round_key and data")
        data = self.firstrounds(data, key)

        data = self.sbox(data, Prince.S)
        data = self.mprime(data)
        data = self.sbox(data, Prince.Sinv)

        data = self.lastrounds(data, key)
        final_round_key = self.list_xor(key, self.make_bit_array(Prince.RC[11]))
        return self.list_xor(data, final_round_key)
        #return data ^ key ^ Prince.RC[11]

    def list_rotate_right(self, l, num):
      output = list(l)

      for i in range(0, len(l)):
        if i < num:
          output[i] = l[len(l) - num + i]
        else:
          output[i] = l[i - num]
      return output


    def outer(self, data, key, decrypt = False):
        k0 = key[0:64]
        #k0prime = list(k0)
        #k0prime.ror(1)
        #k0prime ^= k0 >> 63
        k0prime = self.list_rotate_right(k0, 1)
        k0prime[len(k0prime) - 1] = k0prime[len(k0prime) - 1] ^ k0prime[1]

        if decrypt:
            tmp = list(k0)
            k0 = list(k0prime)
            k0prime = list(tmp)
        k1 = key[64:128]

        #data = k0 ^ data                                # pre-whitening
        data = self.list_xor(k0, data)                        # pre-whitening
        data = self.princecore(data, k1)
        ret = self.list_xor(data, k0prime)
        conv = []
        i = 0
        while i < (len(ret) - 0):
          out = 0
          for j in range(0, 8):
            out = (out << 1) + ret[i+j]
          conv += [out]
          i += 8

        return (bytes(conv))                     # post-whitening


    def encrypt(self, plaintext, key):
        bitkey = self.make_bit_array(unhexlify(key))
        bittext = self.make_bit_array(unhexlify(plaintext))
        #print(bitkey)
        #print(bittext)
        #return self.outer(bittext, bitkey)
        #return hexlify(self.outer(bittext, bitkey))
        res = hexlify(self.outer(bittext, bitkey))
        ret = ""
        for i in range(0, len(res)):
          ret += chr(res[i])
        return ret



    def decrypt(self, ciphertext, key):
        bitkey = self.make_bit_array(unhexlify(key))
        bittext = self.make_bit_array(unhexlify(ciphertext))
        #bitkey = BitArray('0x' + key.encode('hex'))
        bitkey = self.list_xor(bitkey, self.make_bit_array(unhexlify("0000000000000000c0ac29b7c97c50dd")))  # alpha padded with zero
        #bittext = BitArray('0x' + ciphertext.encode('hex'))
        res = hexlify(self.outer(bittext, bitkey, True))
        ret = ""
        for i in range(0, len(res)):
          ret += chr(res[i])
        return ret
        #return hexlify(self.outer(bittext, bitkey, True))
