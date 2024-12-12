import json

class Contact:
    def __init__(self, contact_name, phone_number, postal_address):
        self.contact_name = contact_name
        self.phone_number = phone_number
        self.postal_address = postal_address

    def __repr__(self):
        return f"Contact Name: {self.contact_name}, Phone Number: {self.phone_number}, Address: {self.postal_address}"

    def to_dict(self):
        return {
            "contact_name": self.contact_name,
            "phone_number": self.phone_number,
            "postal_address": self.postal_address
        }

    @staticmethod
    def from_dict(data):
        return Contact(data["contact_name"], data["phone_number"], data["postal_address"])

class ContactsApp:
    def __init__(self, storage_file="contacts.json"):
        self.contacts_data = {}
        self.storage_file = storage_file
        self.load_contacts()

    def load_contacts(self):
        try:
            with open(self.storage_file, "r") as file:
                contacts = json.load(file)
                self.contacts_data = {name: Contact.from_dict(details) for name, details in contacts.items()}
        except FileNotFoundError:
            self.contacts_data =  {}

    def save_contacts(self):
        with open(self.storage_file, "w") as file:
            contacts = {name: contact.to_dict() for name, contact in self.contacts_data.items()}
            json.dump(contacts, file)

    def add_new_contact(self, contact_name, phone_number, postal_address):
        if contact_name in self.contacts_data:
            print("this contact already exists in the database.")
        else:
            self.contacts_data[contact_name] = Contact(contact_name, phone_number, postal_address)
            self.save_contacts()
            print(f"contact '{contact_name}' has been successfully added.")

    def remove_contact(self, contact_name):
        if contact_name in self.contacts_data:
            del self.contacts_data[contact_name]
            self.save_contacts()
            print(f"contact '{contact_name}' has been successfully removed.")
        else:
            print("the contact was not found in the database.")

    def search_contacts(self, search_term):
        matching_results = [
            contact for contact in self.contacts_data.values()
            if search_term.lower() in contact.contact_name.lower() \
               or search_term in contact.phone_number \
               or search_term.lower() in contact.postal_address.lower()
        ]
        if matching_results:
            print("search results:")
            for contact in matching_results:
                print(contact)
        else:
            print("no matches found for the search term.")

    def show_all_contacts(self):
        if not self.contacts_data:
            print("the contact list is currently empty.")
        else:
            print("complete contact list:")
            for contact in self.contacts_data.values():
                print(contact)

#menu system for the user to interact with

def main():
    app_instance = ContactsApp()
    while True:
        print("\n--- welcome to the contacts manager ---")
        print("1. add a new contact")
        print("2. remove an existing contact")
        print("3. search for a contact")
        print("4. display all contacts")
        print("5. exit the application")

        user_choice = input("please choose an option (1-5): ")

        if user_choice == "1":
            contact_name = input("enter contact name: ")
            phone_number = input("enter phone number: ")
            postal_address = input("enter postal address: ")
            app_instance.add_new_contact(contact_name, phone_number, postal_address)
        elif user_choice == "2":
            contact_name = input("enter the contact name to remove: ")
            app_instance.remove_contact(contact_name)
        elif user_choice == "3":
            search_term = input("enter the search term (name, phone, or address): ")
            app_instance.search_contacts(search_term)
        elif user_choice == "4":
            app_instance.show_all_contacts()
        elif user_choice == "5":
            print("thank you for using the contacts manager. goodbye!")
            break
        else:
            print("invalid option. please try again.")

if __name__ == "__main__":
    main()
