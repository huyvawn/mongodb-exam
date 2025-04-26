from pymongo import MongoClient
from tabulate import tabulate
import datetime

# Connect to MongoDB
def connect_to_mongodb():
    try:
        client = MongoClient('mongodb://localhost:27017/')
        db = client['eShop']
        order_collection = db['OrderCollection']
        print("Successfully connected to MongoDB!")
        return order_collection
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None

# 2. Insert documents into OrderCollection
def insert_many_orders(order_collection):
    try:
        orders = [
            {
                "orderid": 1,
                "products": [
                    {
                        "product_id": "quanau",
                        "product_name": "quan au",
                        "size": "XL",
                        "price": 10,
                        "quantity": 1
                    },
                    {
                        "product_id": "somi",
                        "product_name": "ao so mi",
                        "size": "XL",
                        "price": 10.5,
                        "quantity": 2
                    }
                ],
                "total_amount": 31,
                "delivery_address": "Hanoi"
            },
            {
                "orderid": 2,
                "products": [
                    {
                        "product_id": "somi",
                        "product_name": "ao so mi",
                        "size": "L",
                        "price": 9.5,
                        "quantity": 2
                    },
                    {
                        "product_id": "quanau",
                        "product_name": "quan au",
                        "size": "L",
                        "price": 9,
                        "quantity": 1
                    }
                ],
                "total_amount": 28,
                "delivery_address": "Ho Chi Minh"
            },
            {
                "orderid": 3,
                "products": [
                    {
                        "product_id": "somi",
                        "product_name": "ao so mi",
                        "size": "S",
                        "price": 7.5,
                        "quantity": 2
                    },
                    {
                        "product_id": "quanau",
                        "product_name": "quan au",
                        "size": "L",
                        "price": 9,
                        "quantity": 1
                    }
                ],
                "total_amount": 24,
                "delivery_address": "Hanoi"
            }
        ]

        result = order_collection.insert_many(orders)
        
        print(f" {len(result.inserted_ids)} orders have been inserted!")
        return result.inserted_ids
    except Exception as e:
        print(f"Encountered errors trying to insert orders: {e}")
        return None

# 3. Edit delivery_address by orderid
def edit_delivery_address(order_collection, order_id, edited_address):
    try:
        result = order_collection.update_one(
            {"orderid": order_id},
            {"$set": {"delivery_address": edited_address}}
        )
        
        if result.matched_count > 0:
            print(f"Updated delivery address for order {order_id} !")
        else:
            print(f"No order found with ID: {order_id}")
        
        return result.modified_count
    except Exception as e:
        print(f"Error updating address: {e}")
        return 0

# 4. Remove an order
def remove_order(order_collection, order_id):
    try:
        result = order_collection.delete_one({"orderid": order_id})
        
        if result.deleted_count > 0:
            print(f"Deleted order with ID: {order_id}!")
        else:
            print(f"No order found with ID: {order_id}")
        
        return result.deleted_count
    except Exception as e:
        print(f"Error deleting order: {e}")
        return 0

# 5. Read all orders
def display_all_orders(order_collection):
    try:
        orders = order_collection.find()
        table_data = []
        row_num = 1
        
        for order in orders:
            for product in order['products']:
                product_total = product['price'] * product['quantity']
                table_data.append([
                    row_num,
                    product['product_name'],
                    product['price'],
                    product['quantity'],
                    product_total
                ])
                row_num += 1

        headers = ["No", "Product name", "Price", "Quantity", "Total"]
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
        
        return table_data
    except Exception as e:
        print(f"Exception: {e}")
        return []

# 6. Calculate total amount
def calculate_total_amount_for_order(order_collection, order_id):
    try:
        order = order_collection.find_one({"orderid": order_id}, {"products": 1})
        
        if order:
            total = 0
            for product in order['products']:
                total += product['price'] * product['quantity']
            
            print(f"Calculated total amount for order {order_id}: ${total}")
            return total
        else:
            print(f"No order found with ID: {order_id}")
            return 0
    except Exception as e:
        print(f"Error calculating total amount: {e}")
        return 0

# 7. Count products with product_id equal to "somi"
def count_product_id(order_collection, product_id):
    try:
        pipeline = [
            {"$unwind": "$products"}, 
            {"$match": {"products.product_id": product_id}},  
            {"$group": {"_id": None, "count": {"$sum": "$products.quantity"}}} 
        ]
        
        result = list(order_collection.aggregate(pipeline))
        
        if result:
            count = result[0]["count"]
            print(f"Total quantity of product '{product_id}': {count}")
            return count
        else:
            print(f"No products found with product_id '{product_id}'")
            return 0
    except Exception as e:
        print(f"Error counting products: {e}")
        return 0

def main():
    # Connect to MongoDB
    order_collection = connect_to_mongodb()
    
    if order_collection:
        order_collection.drop()

        print("\n--- INSERTING ORDERS ---")
        insert_many_orders(order_collection)
        
        print("\n--- DISPLAYING ALL ORDERS ---")
        display_all_orders(order_collection)
        
        print("\n--- UPDATING DELIVERY ADDRESS ---")
        edit_delivery_address(order_collection, 2, "Da Nang")
        
        print("\n--- REMOVING ORDER ---")
        remove_order(order_collection, 3)
        
        print("\n--- DISPLAYING UPDATED ORDERS ---")
        display_all_orders(order_collection)
        
        print("\n--- CALCULATING TOTAL AMOUNT ---")
        calculate_total_amount_for_order(order_collection, 1)
        
        print("\n--- COUNTING PRODUCTS SOMI ---")
        count_product_id(order_collection, "somi")

if __name__ == "__main__":
    main()