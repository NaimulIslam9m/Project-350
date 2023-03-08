from username_checker import find_username
from username_generator import username_generator

from colorama import init
import asyncio, os, json
import streamlit as st

file = open("data.json")
searchData = json.load(file)


def search_by_email(email: str):
    st.text(os.popen(f"ghunt email {email} | tail +13").read() + "\n🔥 DONE 🔥")


if __name__ == "__main__":
    init()

    st.title("Welcome to OSINT Zone.\nThis is a demo of Project 350.\n")

    tab1, tab2, tab3 = st.tabs(["Username", "Username Gen", "Email"])

    with tab1:
        st.subheader("Search through Username")
        username = st.text_input("", "username")
        if st.button("Start 1"):
            st.text(
                f"\n\n🔍 Searching '{username}' across {len(searchData['sites'])} social networks\n"
            )
            st.text(os.popen(f"python3 username_checker.py {username}").read())

    with tab2:
        st.subheader("Generate probable Username")
        fname = st.text_input("Enter First Name: ", "Robert").title()
        mname = st.text_input("Enter Middle Name: ", "Dairy").title()
        lname = st.text_input("Enter Last Name: ", "Junior").title()
        if st.button("Start 3"):
            username_generator(first_name=fname, middle_name=mname, last_name=lname)

    with tab3:
        st.subheader("Search through Email")
        email = st.text_input("", "naimul9m@gmail.com").title()
        if st.button("Start 2"):
            search_by_email(email)
