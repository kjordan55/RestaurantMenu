import os
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import re

class BackButton(tk.Button):
    def __init__(self, master, callback):
        super().__init__(master, text="Back", command=callback)
        self.pack(pady=20)

class WelcomePage:
    def __init__(self, root, show_menu_callback):
        self.root = root
        self.show_menu_callback = show_menu_callback

        self.welcome_label = tk.Label(root, text="Welcome to Our Restaurant!", font=('Helvetica', 16))
        self.welcome_label.pack(pady=20)

        # Display current time
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_label = tk.Label(root, text=f"Current Time: {current_time}", font=('Helvetica', 12))
        self.time_label.pack()

        # Path to the image file
        image_path = os.path.join("dining-7000638_1280.gif")

        if os.path.exists(image_path):
            self.open_image = tk.PhotoImage(file=image_path)
            self.image_label = tk.Label(root, image=self.open_image)
            self.image_label.pack(pady=20)
        else:
            print("Image file not found.")

        self.menu_button = tk.Button(root, text="See Today's Menu", command=self.on_menu_button_click)
        self.menu_button.pack(pady=20)

    def on_menu_button_click(self):
        # Call the show_menu_callback
        self.show_menu_callback()

        # Destroy the image label
        if hasattr(self, 'image_label'):
            self.image_label.destroy()

        # Disable and hide the "See Today's Menu" button after it's pressed
        self.menu_button.config(state=tk.DISABLED)
        self.menu_button.pack_forget()

    def show_menu(self):
        self.show_menu_callback()
        # Disable and hide the "See Today's Menu" button after it's pressed
        self.menu_button.config(state=tk.DISABLED)
        self.menu_button.pack_forget()

class MainMenuPage(WelcomePage):
    def __init__(self, root, show_menu_callback):
        super().__init__(root, show_menu_callback)

class OrderSummaryPage:
    def __init__(self, root, items, total_price, show_payment_page_callback, reset_callback):
        self.root = root
        self.items = items
        self.total_price = total_price
        self.show_payment_page_callback = show_payment_page_callback
        self.reset_callback = reset_callback

        drink_image_path = os.path.join("drink.png")
        if os.path.exists(drink_image_path):
            drink_image = tk.PhotoImage(file=drink_image_path)
            drink_label = tk.Label(root, image=drink_image)
            drink_label.image = drink_image  # Keep a reference to avoid garbage collection
            drink_label.pack(pady=20)
        else:
            print("Drink image file not found.")

        self.title_label = tk.Label(root, text="Order Summary", font=('Helvetica', 16))
        self.title_label.pack(pady=20)

        for item_info in items:
            item_label = tk.Label(root, text=f"{item_info['name']} - ${item_info['price']:.2f}\n{item_info['description']}", font=('Helvetica', 12))
            item_label.pack()

        total_label = tk.Label(root, text=f"Total: ${total_price:.2f}", font=('Helvetica', 14))
        total_label.pack(pady=20)

        pay_now_button = tk.Button(root, text="Pay Now", command=self.show_payment_page_callback)
        pay_now_button.pack()


    def reset(self):
        # Call the reset callback to restart the application
        self.reset_callback()

class PaymentPage:
    def __init__(self, root, show_payment_confirmation_callback, reset_callback):
        self.root = root
        self.show_payment_confirmation_callback = show_payment_confirmation_callback
        self.reset_callback = reset_callback

        self.title_label = tk.Label(root, text="Enter Payment Information", font=('Helvetica', 16))
        self.title_label.pack(pady=20)

        # Entry fields for user information
        self.first_name_label = tk.Label(root, text="First Name:")
        self.first_name_label.pack()
        self.first_name_entry = tk.Entry(root)
        self.first_name_entry.pack()

        self.last_name_label = tk.Label(root, text="Last Name:")
        self.last_name_label.pack()
        self.last_name_entry = tk.Entry(root)
        self.last_name_entry.pack()

        self.phone_number_label = tk.Label(root, text="Phone Number:")
        self.phone_number_label.pack()
        self.phone_number_entry = tk.Entry(root)
        self.phone_number_entry.pack()

        self.email_label = tk.Label(root, text="Email Address:")
        self.email_label.pack()
        self.email_entry = tk.Entry(root)
        self.email_entry.pack()

        self.card_number_label = tk.Label(root, text="Card Number")
        self.card_number_label.pack()
        self.card_number_entry = tk.Entry(root)
        self.card_number_entry.pack()

        self.card_expire_label = tk.Label(root, text="Card Expire MM/YY")
        self.card_expire_label.pack()
        self.card_expire_entry = tk.Entry(root)
        self.card_expire_entry.pack()

        self.card_security_label = tk.Label(root, text="Security Code")
        self.card_security_label.pack()
        self.card_security_entry = tk.Entry(root)
        self.card_security_entry.pack()

        confirm_button = tk.Button(root, text="Confirm Order", command=self.confirm_order)
        confirm_button.pack()

    def confirm_order(self):
        # Get entered information
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        phone_number = self.phone_number_entry.get()
        email = self.email_entry.get()
        card_number = self.card_number_entry.get()
        card_expire = self.card_expire_entry.get()
        card_security = self.card_security_entry.get()

        # Validate first name and last name (only alphabet characters allowed)
        if not first_name.isalpha() or not last_name.isalpha():
            messagebox.showerror("Error", "Please enter valid alphabet characters for First Name and Last Name.")
            return

        # Validate phone number (only numeric characters allowed, length between 10 and 11)
        if not phone_number.isdigit() or not (10 <= len(phone_number) <= 11):
            messagebox.showerror("Error", "Please enter a valid phone number with only numeric characters, between 10 and 11 digits.")
            return

        # Validate email address
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messagebox.showerror("Error", "Please enter a valid email address.")
            return

        # Validate card number
        if not card_number.isdigit() or not (16 <= len(card_number) <= 17):
            messagebox.showerror("Error", "Please enter a valid 16 digit card number.")
            return

        # Validate card expire
        if "/" not in card_expire or not (5 <= len(card_expire) <= 6):
            messagebox.showerror("Error", "Please enter a valid expiration ex: 05/28.")
            return

        # Validate card security
        if not (3 <= len(card_security) <= 5):
            messagebox.showerror("Error", "Please enter a valid security code ex: 123.")
            return

        # Call the callback function to show payment confirmation
        self.show_payment_confirmation_callback(first_name, last_name, phone_number, email)

    def destroy_current_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root.destroy()

    def reset(self):
        self.destroy_current_menu()

        # Create a new instance of the RestaurantApp class
        new_app = RestaurantApp(self.root)


class RestaurantApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Restaurant Menu Viewer")

        self.current_menu = None
        self.order_total = 0.0
        self.order_items = []  # To store the items added to the order
        self.total_label = tk.Label(root, text="Total: $0.00", font=('Helvetica', 14))

        self.show_welcome()

    def show_welcome(self):
        if self.current_menu:
            self.current_menu.pack_forget()

        self.welcome_page = WelcomePage(self.root, self.show_menu)

    def show_menu(self, existing_order_items=None, existing_order_total=None):
        if self.current_menu:
            self.current_menu.pack_forget()

        if existing_order_items is not None:
            self.order_items = existing_order_items
        if existing_order_total is not None:
            self.order_total = existing_order_total

        if datetime.now().hour < 12:
            menu_title = "Breakfast"
            items = [
                {
                    "name": "Eggs",
                    "price": 3.99,
                    "description": "Scrambled, fried, or poached eggs"
                },
                {
                    "name": "Bacon",
                    "price": 4.99,
                    "description": "Crispy strips of bacon"
                },
                {
                    "name": "Toast",
                    "price": 2.99,
                    "description": "White or whole wheat, buttered"
                },
                # Add more breakfast items here
            ]
        elif datetime.now().hour < 18:
            menu_title = "Lunch"
            items = [
                {
                    "name": "Burger",
                    "price": 6.99,
                    "description": "Juicy beef patty with toppings"
                },
                {
                    "name": "Salad",
                    "price": 5.99,
                    "description": "Fresh greens with dressing"
                },
                {
                    "name": "Sandwich",
                    "price": 4.99,
                    "description": "Classic sandwich varieties"
                },
                # Add more lunch items here
            ]
        else:
            menu_title = "Dinner"
            items = [
                {
                    "name": "Steak",
                    "price": 12.99,
                    "description": "Grilled to perfection"
                },
                {
                    "name": "Fish",
                    "price": 10.99,
                    "description": "Freshly caught, seasoned and baked"
                },
                {
                    "name": "Chicken",
                    "price": 9.99,
                    "description": "Tender and succulent"
                },
                # Add more dinner items here
            ]

        self.current_menu = tk.Frame(self.root)
        self.current_menu.pack(pady=20)


        title_label = tk.Label(self.current_menu, text=f"{menu_title} Menu", font=('Helvetica', 16))
        title_label.pack()

        # Display drink image
        drink_image_path = os.path.join("drink.png")
        if os.path.exists(drink_image_path):
            drink_image = tk.PhotoImage(file=drink_image_path)
            drink_label = tk.Label(self.current_menu, image=drink_image)
            drink_label.image = drink_image  # Keep a reference to avoid garbage collection
            drink_label.pack(pady=20)

        for item_info in items:
            item_label = tk.Label(self.current_menu, text=f"{item_info['name']} - ${item_info['price']:.2f}\n{item_info['description']}", font=('Helvetica', 12))
            item_label.pack()

            # Add "Add to Order" button for each item
            add_to_order_button = tk.Button(self.current_menu, text="Add to Order", command=lambda item_info=item_info: self.add_to_order(item_info))
            add_to_order_button.pack()

        # Display total label
        self.total_label.pack()

        # Add "Send Order" button
        send_order_button = tk.Button(self.current_menu, text="Send Order", command=self.send_order)
        send_order_button.pack()

        clear_order_button = tk.Button(self.current_menu, text="Clear Order", command=self.clear_order)
        clear_order_button.pack()

        #back button
        back_button = BackButton(self.current_menu, self.show_welcome)

        # If there's an existing order, add it to the current order
        if existing_order_items and existing_order_total:
            self.order_items.extend(existing_order_items)
            self.order_total += existing_order_total

            # Update total label
            self.total_label.config(text=f"Total: ${self.order_total:.2f}")

    def add_to_order(self, item_info):
        print(f"{item_info['name']} added to the order!")
        self.order_items.append(item_info)
        self.order_total += item_info['price']

        # Update total label
        self.total_label.config(text=f"Total: ${self.order_total:.2f}")

    def clear_order(self):
        print("Cleared the order!")
        self.order_items.clear()
        self.order_total = 0

        # Update total label
        self.total_label.config(text=f"Total: ${self.order_total:.2f}")

    def send_order(self):
        confirmation = messagebox.askquestion("Send Order", "Are you sure you want to send the order?")
        if confirmation == 'yes':
            print("Order Sent!")

            # Display order summary page
            self.show_order_summary()
        else:
            # Go back to the menu
            self.show_menu()

    def show_order_summary(self):

        # Hide the current menu
        self.destroy_current_menu()

        # Create and display the order summary page
        order_summary_page = OrderSummaryPage(
            self.root,
            self.order_items,
            self.order_total,
            self.show_payment_page,
            self.reset_app)
        self.current_menu = order_summary_page


    def show_payment_page(self):
        # Display the payment page
        payment_window = tk.Toplevel(self.root)

        payment_page = PaymentPage(
            payment_window,
            self.show_payment_confirmation,
            self.reset_app)
        self.current_menu = payment_page

    def destroy_current_menu(self):
        if self.current_menu:
            self.current_menu.destroy()

    def show_payment_confirmation(self, first_name, last_name, phone_number, email):
        # Placeholder for payment processing
        # Print the entered information (replace this with actual payment processing)
        print("Payment Information:")
        print(f"First Name: {first_name}")
        print(f"Last Name: {last_name}")
        print(f"Phone Number: {phone_number}")
        print(f"Email Address: {email}")

        # Display a message indicating that the payment was successful
        messagebox.showinfo("Payment", "Payment successful! Thank you for your order.")

    # Reset the application
        self.reset_app()
        root = tk.Tk()
        app = RestaurantApp(root)
        root.mainloop()

    def reset_app(self):
     self.root.destroy()

if __name__ == "__main__":
  root = tk.Tk()
  app = RestaurantApp(root)
  root.mainloop()