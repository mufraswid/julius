

#List of rotors and reflectors used in Enigma M3
#Source: https://en.wikipedia.org/wiki/Enigma_rotor_details#Rotor_wiring_tables
rotors = {'I' : 'EKMFLGDQVZNTOWYHXUSPAIBRCJ',
          'II' : 'AJDKSIRUXBLHWTMCQGZNPYFVOE',
          'III' : 'BDFHJLCPRTXVZNYEIWGAKMUSQO',
          'IV' : 'ESOVPZJAYQUIRHXLNFTGKDCMWB',
          'V' : 'VZBRGITYUPSDNHLXAWMJQOFECK'}
rotors_notch = {'I' : 'Q',
                'II' : 'E',
                'III' : 'V',
                'IV' : 'J',
                'V' : 'Z'}
reflectors = {'UKW-B' : 'YRUHQSLDPXNGOKMIEBFZCWVJAT',
             'UKW-C' : 'FVPJIAOYEDRZXWGCTKUQSBNMHL'}
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def next_alphabet(a):
  return chr(((ord(a) - ord('A') + 1) % 26) + ord('A'))

def get_index(a):
  return ord(a) - ord('A')

def shift_caesar(word, num_shift):
  '''
  Shift each letter in the word alphabetically
  '''
  shifted_word = ""
  for ch in word:
    shifted_ch = chr((((ord(ch) - ord('A') + num_shift) % 26) + ord('A')))
    shifted_word += shifted_ch
  return shifted_word

def shift_permutation(permutation, num_shift):
  '''
  Shift a permutation by a number
  '''
  #TODO
  if num_shift == 0:
    return permutation
  permutation_length = len(permutation)
  return permutation[permutation_length-num_shift:] + permutation[0:permutation_length-num_shift]


def encrypt(plaintext, rotor_index, reflector, plugboard, ring, position):
    '''
    For encrypting plaintext with Enigma
    The enigma consists of three rotors, a reflector, a plugboard for increased security
    ring config, and initial letter position
    '''
    reflector = reflectors[reflector]
    rotor_used = ['' for i in range(3)]
    rotor_notch = ['' for i in range(3)]
    rotor_letter = ['' for i in range(3)]
    offset_rotor = [0 for i in range(3)]

    for i in range(3):
      rotor_used[i] = rotors[rotor_index[i]]
      rotor_notch[i] = rotors_notch[rotor_index[i]]
      rotor_letter[i] = position[i]
      offset_rotor[i] = ord(ring[i]) - ord('A')
      rotor_used[i] = shift_caesar(rotor_used[i], offset_rotor[i])
      rotor_used[i] = shift_permutation(rotor_used[i], offset_rotor[i])

    ciphertext = ""

    #Plugboard processing
    plugboard_list = plugboard.split(',')
    plugboard_dict = {}
    for i in alphabet:
      plugboard_dict[i] = i
    for i in plugboard_list:
      plugboard_dict[i[0]] = i[1]
      plugboard_dict[i[1]] = i[0]


    #Convert letter by letter in the plaintext
    for letter in plaintext:

      encrypted_letter = letter

      #First, initialize the letter to check rotation in the rotors
      rotor_trigger = False
      if rotor_letter[2] == rotor_notch[2]:
        rotor_trigger = True
      rotor_letter[2] = next_alphabet(rotor_letter[2])
      if rotor_trigger:
        rotor_trigger = False
        if rotor_letter[1] == rotor_notch[1]:
          rotor_trigger = True
        rotor_letter[1] = next_alphabet(rotor_letter[1])
        if rotor_trigger:
          rotor_trigger = False
          rotor_letter[0] = next_alphabet(rotor_letter[0])
      else:
        if rotor_letter[1] == rotor_notch[1]:
          rotor_letter[1] = next_alphabet(rotor_letter[1])
          rotor_letter[0] = next_alphabet(rotor_letter[0])

      #Letter enters the plugboard
      encrypted_letter = plugboard_dict[encrypted_letter]

      current_offset = [get_index(rotor_letter[i]) for i in range(3)]

      # print(encrypted_letter)

      #Letter enters the rotors (2,1,0)
      for i in range(2, -1, -1):
        # print(i, "lol")
        current_pos = get_index(encrypted_letter)
        enc = rotor_used[i][(current_offset[i] + current_pos) % 26]
        new_pos = get_index(enc)
        encrypted_letter = alphabet[(new_pos - current_offset[i] + 26) % 26]
        # print(new_pos, enc, current_offset[i], rotor_used[i])
        # print(encrypted_letter)
      
      #Letter enters the reflector
      encrypted_letter = reflector[get_index(encrypted_letter)]
      # print(encrypted_letter, "LOL")

      #Letter enters the rotors again (0,1,2)
      for i in range(3):
        current_pos = get_index(encrypted_letter)
        # print(rotor_used[i], current_offset[i], current_pos, "hehehe")
        enc = alphabet[(current_offset[i] + current_pos) % 26]
        # print(enc, "yah")
        new_pos = rotor_used[i].index(enc)
        encrypted_letter = alphabet[(new_pos - current_offset[i] + 26) % 26]
        # print(new_pos, enc, current_offset[i], rotor_used[i])
        # print(encrypted_letter)

      #Letter enters the plugboard again
      encrypted_letter = plugboard_dict[encrypted_letter]

      ciphertext += encrypted_letter

    return ciphertext


def decrypt(ciphertext, rotor_index, reflector, plugboard, ring, position):
    '''
    For decrypting plaintext with enigma
    '''
    return encrypt(ciphertext, rotor_index, reflector, plugboard, ring, position)

def test_shift():
  '''
  Test Shift function
  '''
  permutations = ['qwertyuiopasdfghjklzxcvbnm', 'abcdefghijklmnopqrstuvwxyz']
  shifts = [2,4,5,6]
  for i in permutations:
    for j in shifts:
      print(shift_permutation(i, j))

def test():
  '''
  For testing purposes
  '''
  plaintexts = ["holaa", "kepalaPUndaKluTutKakilututKaKi", "peManasaNGlobal"]
  # plaintexts = ["h"]

  rotor_index = ['IV', 'V', 'III']
  reflector = 'UKW-B'
  plugboard = 'AB,CD,EF,GH,XT'
  ring = 'JAV'
  position = 'AXA'
  
  for plaintext in plaintexts:
    plaintext = plaintext.upper()
    ciphertext = encrypt(plaintext, rotor_index, reflector, plugboard, ring, position)
    print(plaintext, ciphertext)
    revert = decrypt(ciphertext, rotor_index, reflector, plugboard, ring, position)
    print(revert)


if __name__ == '__main__':
  # test_shift()
  test()
