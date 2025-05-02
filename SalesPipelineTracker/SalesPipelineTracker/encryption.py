def encrypt_text(text, use_commas=False):
    """
    Encrypt text by:
    1. Converting letters to their position in the alphabet (A=1, Z=26)
    2. Converting numbers to letters (0=A, 1=B, 2=C, ..., 9=J)
    
    Preserves spaces, punctuation, and case information (returns uppercase for uppercase inputs)
    
    Parameters:
    - text: The text to encrypt
    - use_commas: If True, adds commas and spaces between numbers (8, 5, 12, 12, 15)
                  If False, concatenates numbers without separators (85121215)
    """
    result = []
    number_sequence = []
    in_letter_sequence = False
    
    for char in text:
        if char.isalpha():
            # Convert letter to number (A=1, Z=26)
            position = ord(char.lower()) - ord('a') + 1
            
            if use_commas:
                # If we're switching from non-letter to letter, mark that we're in a sequence
                if not in_letter_sequence:
                    in_letter_sequence = True
                
                # Add the number to our sequence
                number_sequence.append(str(position))
            else:
                result.append(str(position))
                
        elif char.isdigit():
            # Convert number to letter (0=A, 1=B, ..., 9=J)
            letter = chr(ord('a') + int(char))
            
            # If we were in a letter sequence, end it and add the comma-separated numbers
            if use_commas and in_letter_sequence and number_sequence:
                result.append(", ".join(number_sequence))
                number_sequence = []
                in_letter_sequence = False
            
            result.append(letter)
        else:
            # Preserve all other characters (spaces, punctuation, etc.)
            
            # If we were in a letter sequence, end it and add the comma-separated numbers
            if use_commas and in_letter_sequence and number_sequence:
                result.append(", ".join(number_sequence))
                number_sequence = []
                in_letter_sequence = False
            
            result.append(char)
    
    # Add any remaining number sequence
    if use_commas and number_sequence:
        result.append(", ".join(number_sequence))
    
    return ''.join(result)

def decrypt_text(text):
    """
    Decrypt text by:
    1. Converting numbers back to letters (1=A, 26=Z)
    2. Converting letters back to numbers (A=0, J=9)
    
    Handles both formats:
    - Numbers without separators (85121215)
    - Numbers with commas (8, 5, 12, 12, 15)
    """
    # First, remove all commas between numbers
    text = text.replace(", ", "").replace(",", "")
    
    result = []
    i = 0
    
    while i < len(text):
        char = text[i]
        
        if char.isdigit():
            # Look ahead to check if this is part of a 2-digit number (10-26)
            if i + 1 < len(text) and text[i+1].isdigit():
                num = int(text[i:i+2])
                if 10 <= num <= 26:  # Valid letter position
                    # Convert number back to letter (1=A, 26=Z)
                    letter = chr(ord('a') + num - 1)
                    result.append(letter)
                    i += 2
                    continue
            
            # Single digit number (1-9)
            num = int(char)
            if 1 <= num <= 9:  # Valid letter position
                # Convert number back to letter (1=A, 9=I)
                letter = chr(ord('a') + num - 1)
                result.append(letter)
            else:
                # Not a valid letter position, leave as is
                result.append(char)
        
        elif char.isalpha():
            # Convert letter back to number (A=0, J=9)
            if 'a' <= char.lower() <= 'j':
                digit = ord(char.lower()) - ord('a')
                result.append(str(digit))
            else:
                # Not in A-J range, leave as is
                result.append(char)
        
        else:
            # Preserve all other characters (spaces, punctuation, etc.)
            result.append(char)
        
        i += 1
    
    return ''.join(result)
