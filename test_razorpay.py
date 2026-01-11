try:
    import razorpay
    print("Razorpay imported successfully.")
    
    import os
    from dotenv import load_dotenv

    load_dotenv()
    
    # Use keys from config
    KEY_ID = os.environ.get('RAZORPAY_KEY_ID')
    KEY_SECRET = os.environ.get('RAZORPAY_KEY_SECRET')
    
    client = razorpay.Client(auth=(KEY_ID, KEY_SECRET))
    print("Razorpay client initialized.")
    
    # Try to create a dummy order
    data = { "amount": 100, "currency": "INR", "receipt": "test_receipt" }
    order = client.order.create(data=data)
    print("Test order created successfully:")
    print(order)

except ImportError as e:
    print(f"ImportError: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
    import traceback
    traceback.print_exc()
