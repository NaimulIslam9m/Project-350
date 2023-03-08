import streamlit as st


def username_generator(first_name: str, middle_name: str, last_name: str):
    import sys
    import os.path

    given_name = first_name + " " + middle_name + " " + last_name

    # remove anything in the name that aren't letters or spaces
    name = "".join([c for c in given_name if c == " " or c.isalpha()])
    tokens = name.lower().split()

    fname = tokens[0]
    mname = ""
    lname = ""

    if len(tokens) == 2:
        lname = tokens[-1]
    elif len(tokens) == 3:
        mname = tokens[1]
        lname = tokens[2]

    # create possible usernames
    st.text("\n\n⚙ Generating Possible Usernames:\n")

    st.text("[+] " + fname + mname + lname)  # johndoe
    st.text("[+] " + lname + fname)  # doejohn
    st.text("[+] " + fname + "." + lname)  # john.doe
    st.text("[+] " + lname + "." + fname)  # doe.john
    st.text("[+] " + lname + fname[0])  # doej
    st.text("[+] " + fname[0] + lname)  # jdoe
    st.text("[+] " + lname[0] + fname)  # djoe
    st.text("[+] " + fname[0] + "." + lname)  # j.doe
    st.text("[+] " + lname[0] + "." + fname)  # d.john
    st.text("[+] " + fname)  # john
    st.text("[+] " + lname)  # joe

    if mname != "":
        st.text("[+] " + lname + fname[0] + mname[0])  # doej
        st.text("[+] " + fname[0] + mname[0] + lname)  # jdoe
        st.text("[+] " + fname[0] + mname[0] + "." + lname)  # j.doe
