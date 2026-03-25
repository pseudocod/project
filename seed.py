from decimal import Decimal
from sqlalchemy.orm import Session
from pwdlib import PasswordHash

from src.db.schema import (
    Role,
    Address,
    User,
    Category,
    Product,
    ProductImage,
    ProductAttribute,
    ProductAttributeLink,
    CartEntry,
    Order,
    OrderItem,
)

password_hash = PasswordHash.recommended()


def seed_database(db: Session) -> None:
    if db.query(User).first():
        return

    role_admin = Role(name="admin")
    role_customer = Role(name="customer")
    db.add_all([role_admin, role_customer])
    db.flush()

    addr_admin = Address(
        street="Str. Independentei 1",
        city="Bucharest",
        state="Ilfov",
        postal_code="010101",
        country="Romania",
    )
    addr_alice = Address(
        street="Str. Florilor 22",
        city="Cluj-Napoca",
        state="Cluj",
        postal_code="400001",
        country="Romania",
    )
    addr_bob = Address(
        street="Bd. Unirii 5",
        city="Timisoara",
        state="Timis",
        postal_code="300001",
        country="Romania",
    )
    addr_shipping = Address(
        street="Str. Libertatii 9",
        city="Iasi",
        state="Iasi",
        postal_code="700001",
        country="Romania",
    )
    db.add_all([addr_admin, addr_alice, addr_bob, addr_shipping])
    db.flush()

    admin = User(
        email="admin@gencstore.com",
        first_name="Admin",
        last_name="Genc",
        phone="0700000001",
        password=password_hash.hash("Admin@1234"),
        role_id=role_admin.id,
        address_id=addr_admin.id,
    )
    alice = User(
        email="alice@example.com",
        first_name="Alice",
        last_name="Popescu",
        phone="0700000002",
        password=password_hash.hash("Alice@1234"),
        role_id=role_customer.id,
        address_id=addr_alice.id,
    )
    bob = User(
        email="bob@example.com",
        first_name="Bob",
        last_name="Ionescu",
        phone="0700000003",
        password=password_hash.hash("Bob@1234"),
        role_id=role_customer.id,
        address_id=addr_bob.id,
    )
    db.add_all([admin, alice, bob])
    db.flush()

    electronics = Category(
        name="Electronics", description="Gadgets, devices, and accessories"
    )
    clothing = Category(name="Clothing", description="Apparel for all seasons")
    books = Category(
        name="Books", description="Fiction, non-fiction, and technical literature"
    )
    db.add_all([electronics, clothing, books])
    db.flush()

    laptop = Product(
        name="UltraBook Pro 14",
        description="Lightweight laptop with 14-inch display",
        price=Decimal("3499.99"),
        stock_quantity=15,
        category_id=electronics.id,
    )
    headphones = Product(
        name="SoundMax Wireless",
        description="Over-ear noise-cancelling headphones",
        price=Decimal("449.99"),
        stock_quantity=40,
        category_id=electronics.id,
    )
    tshirt = Product(
        name="Classic Cotton T-Shirt",
        description="100% cotton unisex t-shirt",
        price=Decimal("59.99"),
        stock_quantity=200,
        category_id=clothing.id,
    )
    jacket = Product(
        name="Winter Puffer Jacket",
        description="Warm and water-resistant jacket",
        price=Decimal("299.99"),
        stock_quantity=50,
        category_id=clothing.id,
    )
    novel = Product(
        name="The Silent Algorithm",
        description="A sci-fi thriller about AI consciousness",
        price=Decimal("39.99"),
        stock_quantity=80,
        category_id=books.id,
    )
    db.add_all([laptop, headphones, tshirt, jacket, novel])
    db.flush()

    db.add_all(
        [
            ProductImage(
                product_id=laptop.id, image_path="/images/products/ultrabook_pro_14.jpg"
            ),
            ProductImage(
                product_id=headphones.id,
                image_path="/images/products/soundmax_wireless.jpg",
            ),
            ProductImage(
                product_id=tshirt.id,
                image_path="/images/products/classic_tshirt_white.jpg",
            ),
            ProductImage(
                product_id=tshirt.id,
                image_path="/images/products/classic_tshirt_black.jpg",
            ),
            ProductImage(
                product_id=jacket.id,
                image_path="/images/products/winter_puffer_jacket.jpg",
            ),
            ProductImage(
                product_id=novel.id,
                image_path="/images/products/the_silent_algorithm.jpg",
            ),
        ]
    )
    db.flush()

    attr_color_black = ProductAttribute(name="color", value="black")
    attr_color_white = ProductAttribute(name="color", value="white")
    attr_size_m = ProductAttribute(name="size", value="m")
    attr_size_l = ProductAttribute(name="size", value="l")
    attr_size_xl = ProductAttribute(name="size", value="xl")
    attr_ram_16 = ProductAttribute(name="ram", value="16gb")
    attr_ram_32 = ProductAttribute(name="ram", value="32gb")
    attr_storage_512 = ProductAttribute(name="storage", value="512gb")
    db.add_all(
        [
            attr_color_black,
            attr_color_white,
            attr_size_m,
            attr_size_l,
            attr_size_xl,
            attr_ram_16,
            attr_ram_32,
            attr_storage_512,
        ]
    )
    db.flush()

    db.add_all(
        [
            ProductAttributeLink(
                product_id=laptop.id, attribute_id=attr_color_black.id
            ),
            ProductAttributeLink(product_id=laptop.id, attribute_id=attr_ram_16.id),
            ProductAttributeLink(product_id=laptop.id, attribute_id=attr_ram_32.id),
            ProductAttributeLink(
                product_id=laptop.id, attribute_id=attr_storage_512.id
            ),
            ProductAttributeLink(
                product_id=headphones.id, attribute_id=attr_color_black.id
            ),
            ProductAttributeLink(
                product_id=headphones.id, attribute_id=attr_color_white.id
            ),
            ProductAttributeLink(
                product_id=tshirt.id, attribute_id=attr_color_black.id
            ),
            ProductAttributeLink(
                product_id=tshirt.id, attribute_id=attr_color_white.id
            ),
            ProductAttributeLink(product_id=tshirt.id, attribute_id=attr_size_m.id),
            ProductAttributeLink(product_id=tshirt.id, attribute_id=attr_size_l.id),
            ProductAttributeLink(product_id=tshirt.id, attribute_id=attr_size_xl.id),
            ProductAttributeLink(
                product_id=jacket.id, attribute_id=attr_color_black.id
            ),
            ProductAttributeLink(product_id=jacket.id, attribute_id=attr_size_l.id),
            ProductAttributeLink(product_id=jacket.id, attribute_id=attr_size_xl.id),
        ]
    )
    db.flush()

    # ------------------------------------------------------------------
    # Cart entries (Alice has items in cart)
    # ------------------------------------------------------------------
    db.add_all(
        [
            CartEntry(user_id=alice.id, product_id=laptop.id, quantity=1),
            CartEntry(user_id=alice.id, product_id=tshirt.id, quantity=2),
            CartEntry(user_id=bob.id, product_id=headphones.id, quantity=1),
        ]
    )
    db.flush()

    order1 = Order(
        user_id=alice.id,
        payment_type="card",
        status="delivered",
        shipping_address_id=addr_alice.id,
        billing_address_id=addr_alice.id,
    )
    order2 = Order(
        user_id=bob.id,
        payment_type="cash",
        status="pending",
        shipping_address_id=addr_shipping.id,
        billing_address_id=addr_bob.id,
    )
    db.add_all([order1, order2])
    db.flush()

    db.add_all(
        [
            OrderItem(
                order_id=order1.id,
                product_id=tshirt.id,
                name=tshirt.name,
                quantity=3,
                price_per_piece=tshirt.price,
            ),
            OrderItem(
                order_id=order1.id,
                product_id=novel.id,
                name=novel.name,
                quantity=1,
                price_per_piece=novel.price,
            ),
            OrderItem(
                order_id=order2.id,
                product_id=headphones.id,
                name=headphones.name,
                quantity=1,
                price_per_piece=headphones.price,
            ),
        ]
    )

    db.commit()
    print("Database seeded with mock data.")
