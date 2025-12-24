from app import create_app, db
from app.models import User, Category, Product, ProductVariant

app = create_app()

def seed_database():
    with app.app_context():
        print("Seeding database...")
        
        # Create categories
        categories_data = [
            {'name': 'Georgette', 'image_url': 'https://pub-35faf01d0bac49249f374189fd3a24d9.r2.dev/images/1766490299278-320015ca-346f-4690-a846-aa31309931de.png'},
            {'name': 'Net', 'image_url': 'https://image2url.com/images/1766487547602-33d81f76-4677-4615-8767-8e6fac6b8343.jpg'},
            {'name': 'Velvet', 'image_url': 'https://image2url.com/images/1766487988493-1d1eaffe-c73a-438e-9aea-78b73e2983c5.jpeg'},
            {'name': 'Crepe', 'image_url': 'https://image2url.com/images/1766485355978-8d162319-dba2-44e3-a190-10f73a5ba164.jpeg'},
            {'name': 'Satin', 'image_url': 'https://image2url.com/images/1766488211188-7f1b6193-9573-4103-8d24-73ae26b3a436.jpg'},
            {'name': 'Rayon', 'image_url': 'https://image2url.com/images/1766487320410-26647f96-bd56-45de-b1d4-14ea4b1c8887.jpg'},
            {'name': 'Shimmer', 'image_url': 'https://image2url.com/images/1766487435912-21d07520-2c1b-44a2-84b3-a74f985d5c0b.jpeg'},
            {'name': 'Santoon', 'image_url': 'https://image2url.com/images/1766488976721-231ce777-a4ba-452d-a4e0-91c0f73ffd43.png'},
        ]
        
        for cat_data in categories_data:
            category = Category.query.filter_by(name=cat_data['name']).first()
            if not category:
                category = Category(**cat_data)
                db.session.add(category)
            else:
                category.image_url = cat_data['image_url']
        
        db.session.commit()
        print("Categories created.")
        
        # Color list for variants
        COLORS = [
            ("Red", "#FF0000"), ("Blue", "#0000FF"), ("Green", "#008000"), ("Yellow", "#FFFF00"), 
            ("Orange", "#FFA500"), ("Purple", "#800080"), ("Pink", "#FFC0CB"), ("Brown", "#A52A2A"), 
            ("Black", "#000000"), ("White", "#FFFFFF"), ("Gray", "#808080"), ("Cyan", "#00FFFF"), 
            ("Magenta", "#FF00FF"), ("Lime", "#00FF00"), ("Maroon", "#800000"), ("Navy", "#000080"), 
            ("Olive", "#808000"), ("Teal", "#008080"), ("Silver", "#C0C0C0"), ("Gold", "#FFD700"),
            ("Beige", "#F5F5DC"), ("Ivory", "#FFFFF0"), ("Khaki", "#F0E68C"), ("Lavender", "#E6E6FA"),
            ("Coral", "#FF7F50"), ("Crimson", "#DC143C"), ("Indigo", "#4B0082"), ("Mint", "#F5FFFA"),
            ("Peach", "#FFDAB9"), ("Plum", "#DDA0DD"), ("Sky Blue", "#87CEEB"), ("Tan", "#D2B48C"),
            ("Turquoise", "#40E0D0"), ("Violet", "#EE82EE"), ("Slate", "#708090"), ("Emerald", "#50C878"),
            ("Rose", "#FF007F"), ("Orchid", "#DA70D6"), ("Chocolate", "#D2691E"), ("Salmon", "#FA8072"),
            ("Aqua", "#00FFFF"), ("Azure", "#F0FFFF"), ("Bisque", "#FFE4C4"), ("Linen", "#FAF0E6"),
            ("Thistle", "#D8BFD8")
        ]
        
        # Create sample products
        categories = Category.query.all()
        
        sample_products_base = [
            {
                'name': 'Premium Georgette Fabric',
                'description': 'Lightweight and flowing georgette fabric perfect for sarees and dresses.',
                'base_price': 250.00,
                'fabric_type': 'Georgette',
                'width': '44 inches',
                'category_name': 'Georgette',
                'image': 'https://pub-35faf01d0bac49249f374189fd3a24d9.r2.dev/images/1766490299278-320015ca-346f-4690-a846-aa31309931de.png'
            },
            {
                'name': 'Soft Net Fabric',
                'description': 'Delicate net fabric ideal for embroidery work and lehengas.',
                'base_price': 180.00,
                'fabric_type': 'Net',
                'width': '58 inches',
                'category_name': 'Net',
                'image': 'https://image2url.com/images/1766487547602-33d81f76-4677-4615-8767-8e6fac6b8343.jpg'
            },
            {
                'name': 'Luxurious Velvet',
                'description': 'Rich and smooth velvet fabric for premium garments.',
                'base_price': 450.00,
                'fabric_type': 'Velvet',
                'width': '44 inches',
                'category_name': 'Velvet',
                'image': 'https://image2url.com/images/1766487988493-1d1eaffe-c73a-438e-9aea-78b73e2983c5.jpeg'
            },
            {
                'name': 'Elegant Satin',
                'description': 'Smooth and shiny satin fabric for elegant wear.',
                'base_price': 320.00,
                'fabric_type': 'Satin',
                'width': '44 inches',
                'category_name': 'Satin',
                'image': 'https://image2url.com/images/1766488211188-7f1b6193-9573-4103-8d24-73ae26b3a436.jpg'
            },
            {
                'name': 'Premium Crepe Fabric',
                'description': 'Textured and versatile crepe fabric suitable for all-season wear.',
                'base_price': 280.00,
                'fabric_type': 'Crepe',
                'width': '44 inches',
                'category_name': 'Crepe',
                'image': 'https://image2url.com/images/1766485355978-8d162319-dba2-44e3-a190-10f73a5ba164.jpeg'
            },
            {
                'name': 'Soft Rayon Fabric',
                'description': 'Breathable and soft rayon fabric, perfect for summer outfits.',
                'base_price': 150.00,
                'fabric_type': 'Rayon',
                'width': '44 inches',
                'category_name': 'Rayon',
                'image': 'https://image2url.com/images/1766487320410-26647f96-bd56-45de-b1d4-14ea4b1c8887.jpg'
            },
            {
                'name': 'Glimmering Shimmer',
                'description': 'Sparkling shimmer fabric for festive and party wear.',
                'base_price': 350.00,
                'fabric_type': 'Shimmer',
                'width': '44 inches',
                'category_name': 'Shimmer',
                'image': 'https://image2url.com/images/1766487435912-21d07520-2c1b-44a2-84b3-a74f985d5c0b.jpeg'
            },
            {
                'name': 'Plain Santoon',
                'description': 'Smooth santoon fabric ideal for lining and basic garments.',
                'base_price': 120.00,
                'fabric_type': 'Santoon',
                'width': '44 inches',
                'category_name': 'Santoon',
                'image': 'https://image2url.com/images/1766488976721-231ce777-a4ba-452d-a4e0-91c0f73ffd43.png'
            },
        ]
        
        for base_data in sample_products_base:
            product = Product.query.filter_by(name=base_data['name']).first()
            category = next(c for c in categories if c.name == base_data['category_name'])
            
            if not product:
                product = Product(
                    name=base_data['name'],
                    description=base_data['description'],
                    base_price=base_data['base_price'],
                    fabric_type=base_data['fabric_type'],
                    width=base_data['width'],
                    category_id=category.id
                )
                db.session.add(product)
                db.session.flush()
            else:
                product.description = base_data['description']
                product.base_price = base_data['base_price']
                product.fabric_type = base_data['fabric_type']
                product.width = base_data['width']
                product.category_id = category.id
            
            # Add/Update 45 color variants for this product
            for color_name, hex_code in COLORS:
                variant = ProductVariant.query.filter_by(product_id=product.id, color_name=color_name).first()
                variant_image_url = f"{base_data['image']}?color={color_name.replace(' ', '_')}"
                if not variant:
                    variant = ProductVariant(
                        product_id=product.id,
                        color_name=color_name,
                        hex_code=hex_code,
                        image_url=variant_image_url
                    )
                    db.session.add(variant)
                else:
                    variant.image_url = variant_image_url
                    variant.hex_code = hex_code
        
        db.session.commit()
        print(f"Products created/updated.")
        print(f"Variants created/updated: {ProductVariant.query.count()} total")
        print("Database seeded successfully!")
        print(f"Sample products created: {Product.query.count()} total products")
        print(f"Sample variants created: {ProductVariant.query.count()} total variants")
        print("Database seeded successfully!")

if __name__ == '__main__':
    seed_database()
