import string
import time

MENU = {
    # --- Drinks ---
    # Sorted Price Check: 50, 65, 85, 110, 125, 140
    # Median Root: ~85 or 110. This ensures a tree like: 85 (Left: 65, 50 | Right: 110, 125, 140)
    "Canned Soda / Bottled Water": {"price": 50, "prep_time": 0.5 * 60},
    "Fresh Lemonade": {"price": 65, "prep_time": 2.5 * 60},
    "Brewed Coffee": {"price": 85, "prep_time": 1 * 60},        # Root Candidate
    "Milk Tea (Bubble Tea)": {"price": 110, "prep_time": 4 * 60},
    "Iced Coffee": {"price": 125, "prep_time": 2.5 * 60},
    "Fruit Shake (Banana)": {"price": 140, "prep_time": 3.5 * 60}, # Raised to be unique

    # --- Street Food ---
    # Sorted Price Check: 20, 25, 30, 35, 45, 50, 70
    # Median Root: 35. Left: 20, 25, 30. Right: 45, 50, 70.
    "Kwek-Kwek": {"price": 20, "prep_time": 1 * 60},
    "Turon": {"price": 25, "prep_time": 0.5 * 60},
    "Grilled Hotdog": {"price": 30, "prep_time": 2.5 * 60},
    "Pork BBQ Stick": {"price": 35, "prep_time": 1.5 * 60},     # Root Candidate
    "Siomai (Steamed)": {"price": 45, "prep_time": 1 * 60},     # Raised to be unique
    "Fish Balls / Kikiam": {"price": 50, "prep_time": 1 * 60},  # Raised to be unique
    "French Fries": {"price": 70, "prep_time": 3.5 * 60},

    # --- Simple Meals ---
    # Sorted Price Check: 70, 100, 120, 135, 150, 185
    # Median Root: 120. Left: 70, 100. Right: 135, 150, 185.
    "Lugaw / Congee (with toppings)": {"price": 70, "prep_time": 1.5 * 60},
    "Pancit Canton (Stir-fry)": {"price": 100, "prep_time": 5 * 60},
    "Basic Burger": {"price": 120, "prep_time": 6.5 * 60},      # Root Candidate
    "Grilled Cheese Sandwich": {"price": 135, "prep_time": 5.5 * 60}, # Raised to be unique
    "Tapsilog": {"price": 150, "prep_time": 6 * 60},
    "Pasta (Simple sauce)": {"price": 185, "prep_time": 6 * 60},

    # --- Baked Goods ---
    # Sorted Price Check: 20, 35, 55, 75, 90, 110
    # Median Root: ~75. Left: 20, 35, 55. Right: 90, 110.
    "Cheese Pandesal": {"price": 20, "prep_time": 0.5 * 60},
    "Banana Cue": {"price": 35, "prep_time": 0.5 * 60},
    "Chocolate Chip Cookie": {"price": 55, "prep_time": 0.5 * 60},
    "Brownie Square": {"price": 75, "prep_time": 0.5 * 60},    # Root Candidate
    "Leche Flan (Small)": {"price": 90, "prep_time": 1 * 60},
    "Halo-Halo (Basic)": {"price": 110, "prep_time": 4 * 60},
}


class Node:
    def __init__(self, order_items, code, total_price, total_prep_time, estimated_wait):
        self.order_items = order_items #list of item names
        self.code = code
        self.total_price = total_price
        self.total_prep_time = total_prep_time #prep time for THIS order
        self.estimated_wait = estimated_wait   #wait time until THIS order starts
        self.next = None

class Queue:
    def __init__(self):
        self.head = None
        self.tail = None
        self.letter_index = 0
        self.number_counter = 1
        self.MENU = MENU
        self.total_wait_in_queue = 0 #total prep time of all orders in line

    def generate_code(self):
        letter = string.ascii_uppercase[self.letter_index]
        code = f"{letter}{self.number_counter:02d}"

        #increment for next code
        self.number_counter += 1
        if self.number_counter > 99:
            self.number_counter = 1
            self.letter_index += 1
            if self.letter_index >= len(string.ascii_uppercase):
                self.letter_index = 0
        return code

    def enqueue(self, order_dict): #parameter is now 'order_dict'
        code = self.generate_code()
        
        total_price = 0
        total_prep_time = 0
        order_items_list = [] #to store full item details
        
        #loop through the dictionary, e.g., {"Iced Coffee": 2, "Tapsilog": 1}
        for name, quantity in order_dict.items():
            item_details = self.MENU.get(name)
            if item_details and quantity > 0:
                #multiply price and prep time by the quantity
                total_price += item_details["price"] * quantity
                total_prep_time += item_details["prep_time"] * quantity
                #store the quantity in the list
                order_items_list.append({"name": name, "price": item_details["price"], "quantity": quantity})
        estimated_wait = self.total_wait_in_queue + total_prep_time

        self.total_wait_in_queue += total_prep_time
        
        new_node = Node(order_items_list, code, total_price, total_prep_time, estimated_wait)
        
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
            
        return {"code": code, "total": total_price, "wait": estimated_wait}

    def dequeue(self):
        if self.head is None:
            return None
            
        removed = self.head
        self.head = self.head.next
        
        if self.head is None:
            self.tail = None
        
        #remove this order's prep time from the total queue time
        removed_prep_time = removed.total_prep_time
        self.total_wait_in_queue -= removed_prep_time

        #update waiting times for all remaining orders
        current = self.head
        while current:
            current.estimated_wait -= removed_prep_time
            if current.estimated_wait < 0:
                current.estimated_wait = 0 #should not happen, but a good safety net
            current = current.next
            
        return {'order_items': removed.order_items, 'code': removed.code}

    def display(self):
        current = self.head
        items_in_queue = []
        while current:
            #format waiting time to minutes/seconds
            mins, secs = divmod(current.estimated_wait, 60)
            wait_str = f"{int(mins)}m {int(secs)}s"
            
            items_in_queue.append({
                'order_items': current.order_items, 
                'code': current.code,
                'total_price': current.total_price,
                'waiting_time': wait_str
            })
            current = current.next
        return items_in_queue