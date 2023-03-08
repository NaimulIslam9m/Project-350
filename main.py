from username_checker import find_username
from username_generator import username_generator

from colorama import init
import asyncio, os


def search_by_email(email: str):
    os.system(f"ghunt email {email} | tail +13")
    print("\n🔥 DONE 🔥")


if __name__ == "__main__":
    init()

    print("\nWelcome to OSINT Zone. This is a demo of Project 350.")

    while True:
        print("\n\nAvailable Options:")
        print("\t1. Search through username")
        print("\t2. Search through email")
        print("\t3. Generate probable username")
        print("\t4. Quit")

        option = input("\nEnter Option (default 1):")

        if option == "1" or option == "":
            username = input("Enter Target Username: ")
            asyncio.run(find_username(username=username))
        elif option == "2":
            email = input("Enter Target Email: ")
            search_by_email(email)
        elif option == "3":
            fname = input("Enter First Name: ")
            mname = input("Enter Middle Name: ")
            lname = input("Enter Last Name: ")

            username_generator(first_name=fname, middle_name=mname, last_name=lname)
        elif option == "4":
            exit(0)
        else:
            print("Invalid Option")

        print("➖" * 85)
