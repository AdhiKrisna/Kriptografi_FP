import streamlit as st
from functions.text_encrypt_decrypt import super_encrypt, super_decrypt
from functions.steganography_encryption import encode_image,  decode_image
from functions.file_encrypt import encrypt_file, decrypt_file
import connection as cn
from Crypto.Random import get_random_bytes
import base64
import os

def dashboard(page):
    col1, col2, col3 = st.columns([5, 1, 15])
    if page == "Kotak Pandora":
        with col3:
            st.title("Message Cryptography using Rail Fence and ECC (Elliptic Curve Cryptography)")
            tab1, tab2 = st.tabs(["Encrypt", "Decrypt"])
            with tab1:
                st.header("Text Encrypt")
                message = st.text_area("Input Plain Text Message")
                railKey = st.number_input(label='Rail and Fence Key', min_value=2, max_value=1000, value=2)  
                if st.button("Encrypt"):
                    if message == "":
                        st.error("Please input a message.")
                        st.stop()
                    with st.expander(":green[See Result]"):
                        super_encrypted, space_positions = super_encrypt(message, railKey)
                        st.subheader(f"Encrypted Message: ")
                        st.write(f":green[{super_encrypted}]")
                        st.code(f"{super_encrypted}", language='text', line_numbers=True)
                        st.subheader(f"Please copy the encrypted message for decryption.")
            with tab2:
                st.header("Text Decrypt")
                encryptedText = st.text_area("Input Encrypted Message")
                railKey = st.number_input(label='Rail and Fence Key Decrypt', min_value=2, max_value=1000, value=2)  
                # spacePosition = st.text_input("Input Space Positions")
                if st.button("Decrypt"):
                    with st.expander(":green[See Result]"):
                        query = cn.run_query("SELECT * FROM messages WHERE encrypted_text = %s;", (encryptedText,), fetch=True)
                        # st.write(query)
                        if query is not None and not query.empty:
                            spacePosition = query['space_position'][0]
                            decrypted_message = super_decrypt(encryptedText, railKey, spacePosition)
                            st.subheader(f"Decrypted Message: ")
                            st.write(f":green[{decrypted_message}]")
                        else:
                            st.error("No data found.")
                            st.stop()
            pass
        with col2:
            None
        with col1:
            st.image("assets/gambar1.png", width=400)
    elif page == "Galeri Stegano":
        col1, col2, col3 = st.columns([15, 1, 5])
        with col1:
            st.title("Image Steganography")
            tab1, tab2 = st.tabs(["Encrypt", "Decrypt"])
            with tab1:
                st.header("Image Encrypt")
                
                # Pilih file untuk dienkripsi
                message = st.text_area("Input Plain Text Message")
                output_image_path = 'encrypted_image.png'
                image_file = st.file_uploader("Upload a cover image", type=["png", "jpg", "jpeg", "webp", "tiff", "bmp", "gif"])
                if message != '' and image_file:
                    # image_file_data = image_file.read()
                    if st.button("Encrypt and Save"):
                        hidden_image_path = encode_image(image_file, output_image_path, message)
                        st.success(f"File has been hidden in image: {hidden_image_path}")
                        with open(hidden_image_path, "rb") as img_file:
                            st.download_button(
                                label="Download Encrypted Image",
                                data=img_file,
                                file_name="encrypted_image.png",
                                mime="image/png"
                            )
            with tab2:
                st.header("Image Decrypt")
                encrypted_image = st.file_uploader("Upload an image to extract data", type=["png"])
                if encrypted_image:
                    if st.button("Decrypt"):
                        with st.expander(":green[See Result]"):
                            try:
                                message = decode_image(encrypted_image)
                                st.success(f"Hidden message: ")
                                st.write(f":green[{message}]")
                            except Exception as e:
                                st.error(f"An error occurred while decrypting the image: {e}")
        with col2:
            None
        with col3:
            st.image("assets/gambar3.png", width=400)
        pass
    elif page == "File Encrypt":
        st.title("File Encryption and Decryption using ChaCha20")
        tab1, tab2 = st.tabs(["Encrypt", "Decrypt"])
        with tab1:
            st.header("File Encrypt")
            file_to_encrypt = st.file_uploader("Upload a file to encrypt", type=["txt", "pdf", "docx", "xlsx", "csv", "png", "jpg", "jpeg"])
            if file_to_encrypt is not None:
                input_data = file_to_encrypt.read()
                file_name = file_to_encrypt.name
                if st.button("Encrypt"):
                    key = get_random_bytes(32)  
                    st.write(":green[Encryption Key (Base64):]")
                    st.write(base64.b64encode(key).decode())
                    encrypted_data = encrypt_file(input_data, key)
                    st.success("File has been encrypted!\n Please save the key and the encrypted bin file to decrypt the file.")
                    
                    # Tombol untuk mengunduh file terenkripsi
                    st.download_button(
                        label="Download Encrypted File",
                        data=encrypted_data,
                        file_name=f"{file_name}.bin",
                        mime="application/octet-stream"
                    )
        with tab2:
            st.header("File Decrypt")
            file_to_decrypt = st.file_uploader("Upload an encrypted file", type=["bin"])
            if file_to_decrypt is not None:
                encrypted_data = file_to_decrypt.read()
                key_input = st.text_input("Input Key (Base64)")
                if key_input:
                    try:
                        # Decode the Base64 input key to bytes
                        key = base64.b64decode(key_input)
                        if len(key) != 32:
                            st.error("The key must be exactly 32 bytes long.")
                        else:
                            if st.button("Decrypt"):
                                decrypted_data = decrypt_file(encrypted_data, key)
                                original_filename = os.path.splitext(file_to_decrypt.name)[0]
                                file_extension = original_filename.split('.')[-1] if '.' in original_filename else "txt"
                                original_filename_ = original_filename.split('.')[0]
                                st.write("File Name: ", original_filename_)
                                st.success("File has been decrypted!")
                                # Tombol untuk mengunduh file yang didekripsi
                                st.download_button(
                                    label="Download Decrypted File",
                                    data=decrypted_data,
                                    file_name=f"{original_filename_}_decrypted.{file_extension}",
                                    mime="text/plain"
                                )
                    except Exception as e:
                        st.error(f"Decryption failed: {e}")
        pass
    
    col1, col2, col3, col4, col5, col6 , col7= st.columns([1, 1, 1,1,1,1,1])
    with col4:
        if st.button(":red[Logout]"):
            st.session_state["is_logged_in"] = False
            st.session_state["username"] = None
            st.write("Logged out successfully.")
            st.rerun()

if __name__ == "__main__":
    dashboard()
    
