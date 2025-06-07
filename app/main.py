import streamlit as st

st.title("Cold Email Generator")    
url_input = st.text_input("Enter the URL of the company you want to target")
submit_button = st.button("Submit")
if submit_button:
    if url_input:
        st.write(f"Generating cold email for {url_input}...")
        # Here you would call your email generation function
        # For example: email_content = generate_email(url_input)
        # st.write(email_content)
    else:
        st.error("Please enter a valid URL.")