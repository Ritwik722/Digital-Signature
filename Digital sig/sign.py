# from cryptography.hazmat.primitives import hashes
# from cryptography.hazmat.primitives.asymmetric import padding
# from cryptography.hazmat.primitives import serialization

# def sign_message(student_id, message):
#     """
#     Sign a message using the student's private key stored in a file.

#     Args:
#         student_id (str): The ID of the student.
#         message (bytes): The message to be signed.

#     Returns:
#         bytes: The digital signature.
#     """
#     try:
#         # Load private key from file
#         with open(f"{student_id}_private_key.pem", "rb") as private_file:
#             private_key = serialization.load_pem_private_key(
#                 private_file.read(),
#                 password=None
#             )

#         # Sign the message
#         signature = private_key.sign(
#             message,
#             padding.PSS(
#                 mgf=padding.MGF1(hashes.SHA256()),
#                 salt_length=padding.PSS.MAX_LENGTH
#             ),
#             hashes.SHA256()
#         )
#         print(f"Message signed successfully for {student_id}.")
#         return signature

#     except Exception as e:
#         print(f"Error signing message for {student_id}: {e}")
#         return None

# # Example: Sign a message and save to `signature.bin`
# if __name__ == "__main__":
#     student_id = "Student2"  # Replace with actual student ID
#     message = b"Authenticate Student2"  # Replace with actual authentication data

#     # Generate digital signature
#     signature = sign_message(student_id, message)

#     if signature:
#         # Save signature to a binary file
#         with open("signature.bin", "wb") as sig_file:
#             sig_file.write(signature)
#         print("Signature saved to 'signature.bin'.")

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
import os

def sign_message(student_id, message):
    """
    Sign a message using the student's private key stored in the 'keys' folder.

    Args:
        student_id (str): The ID of the student.
        message (bytes): The message to be signed.

    Returns:
        bytes: The digital signature or None if an error occurs.
    """
    try:
        #  Load private key from the 'keys' folder
        private_key_path = f"keys/{student_id}_private_key.pem"

        # Check if private key exists
        if not os.path.exists(private_key_path):
            print(f"❌ Private key not found for student: {student_id}")
            return None

        # Load the private key from the correct path
        with open(private_key_path, "rb") as private_file:
            private_key = serialization.load_pem_private_key(
                private_file.read(),
                password=None
            )

        #  Sign the message using PSS padding and SHA256
        signature = private_key.sign(
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        
        print(f"✅ Message signed successfully for {student_id}.")
        return signature

    except Exception as e:
        print(f"❌ Error signing message for {student_id}: {e}")
        return None

# Example: Sign a message and save to `signatures/signature.bin`
if __name__ == "__main__":
    student_id = "Student2"  # Replace with the correct student ID
    message = b"Authenticate Student2"  # Replace with the actual authentication data

    # Generate digital signature
    signature = sign_message(student_id, message)

    if signature:
        #  Save signature in the 'signatures' folder
        os.makedirs("signatures", exist_ok=True)
        signature_path = f"signatures/{student_id}_signature.bin"

        with open(signature_path, "wb") as sig_file:
            sig_file.write(signature)

        print(f"✅ Signature saved to '{signature_path}'.")
    else:
        print("❌ Failed to create signature.")
