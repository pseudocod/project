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
    if db.query(Role).first():
        return

    # ── Roles ────────────────────────────────────────────────────────────────
    role_admin = Role(name="admin")
    role_customer = Role(name="customer")
    db.add_all([role_admin, role_customer])
    db.flush()

    # ── Addresses ────────────────────────────────────────────────────────────
    addr_admin = Address(street="Str. Independentei 1", city="Bucharest", state="Ilfov", postal_code="010101", country="Romania")
    addr_alice = Address(street="Str. Florilor 22", city="Cluj-Napoca", state="Cluj", postal_code="400001", country="Romania")
    addr_bob = Address(street="Bd. Unirii 5", city="Timisoara", state="Timis", postal_code="300001", country="Romania")
    addr_diana = Address(street="Aleea Trandafirilor 3", city="Brasov", state="Brasov", postal_code="500001", country="Romania")
    addr_elena = Address(street="Calea Victoriei 100", city="Bucharest", state="Ilfov", postal_code="010063", country="Romania")
    addr_florin = Address(street="Str. Mihai Eminescu 7", city="Iasi", state="Iasi", postal_code="700001", country="Romania")
    addr_ship1 = Address(street="Str. Libertatii 9", city="Iasi", state="Iasi", postal_code="700002", country="Romania")
    addr_ship2 = Address(street="Bd. Decebal 14", city="Cluj-Napoca", state="Cluj", postal_code="400002", country="Romania")
    db.add_all([addr_admin, addr_alice, addr_bob, addr_diana, addr_elena, addr_florin, addr_ship1, addr_ship2])
    db.flush()

    # ── Users ────────────────────────────────────────────────────────────────
    admin = User(email="admin@gencstore.com", first_name="Admin", last_name="Genc", phone="0700000001", password=password_hash.hash("Admin@1234"), role_id=role_admin.id, address_id=addr_admin.id)
    alice = User(email="alice@example.com", first_name="Alice", last_name="Popescu", phone="0700000002", password=password_hash.hash("Alice@1234"), role_id=role_customer.id, address_id=addr_alice.id)
    bob = User(email="bob@example.com", first_name="Bob", last_name="Ionescu", phone="0700000003", password=password_hash.hash("Bob@1234"), role_id=role_customer.id, address_id=addr_bob.id)
    jason = User(email="jason@example.com", first_name="Jason", last_name="Popescu", phone="0700000004", password=password_hash.hash("Jason@1234"), role_id=role_customer.id, address_id=None)
    charlie = User(email="charlie@example.com", first_name="Charlie", last_name="Ionescu", phone="0700000005", password=password_hash.hash("Charlie@1234"), role_id=role_customer.id, address_id=None)
    diana = User(email="diana@example.com", first_name="Diana", last_name="Muresan", phone="0700000010", password=password_hash.hash("Diana@1234"), role_id=role_customer.id, address_id=addr_diana.id)
    elena = User(email="elena@example.com", first_name="Elena", last_name="Constantin", phone="0700000011", password=password_hash.hash("Elena@1234"), role_id=role_customer.id, address_id=addr_elena.id)
    florin = User(email="florin@example.com", first_name="Florin", last_name="Popa", phone="0700000012", password=password_hash.hash("Florin@1234"), role_id=role_customer.id, address_id=addr_florin.id)
    extra_users = [
        User(email="george@example.com", first_name="George", last_name="Stan", phone="0700000013", password=password_hash.hash("George@1234"), role_id=role_customer.id),
        User(email="horia@example.com", first_name="Horia", last_name="Dinu", phone="0700000014", password=password_hash.hash("Horia@1234"), role_id=role_customer.id),
        User(email="ioana@example.com", first_name="Ioana", last_name="Rusu", phone="0700000015", password=password_hash.hash("Ioana@1234"), role_id=role_customer.id),
        User(email="julian@example.com", first_name="Julian", last_name="Mihai", phone="0700000016", password=password_hash.hash("Julian@1234"), role_id=role_customer.id),
        User(email="karina@example.com", first_name="Karina", last_name="Gheorghe", phone="0700000017", password=password_hash.hash("Karina@1234"), role_id=role_customer.id),
        User(email="liviu@example.com", first_name="Liviu", last_name="Stoica", phone="0700000018", password=password_hash.hash("Liviu@1234"), role_id=role_customer.id),
        User(email="maria@example.com", first_name="Maria", last_name="Moldovan", phone="0700000019", password=password_hash.hash("Maria@1234"), role_id=role_customer.id),
        User(email="nicu@example.com", first_name="Nicu", last_name="Serban", phone="0700000020", password=password_hash.hash("Nicu@1234"), role_id=role_customer.id),
        User(email="oana@example.com", first_name="Oana", last_name="Lungu", phone="0700000021", password=password_hash.hash("Oana@1234"), role_id=role_customer.id),
        User(email="petru@example.com", first_name="Petru", last_name="Nistor", phone="0700000022", password=password_hash.hash("Petru@1234"), role_id=role_customer.id),
        User(email="raluca@example.com", first_name="Raluca", last_name="Costea", phone="0700000023", password=password_hash.hash("Raluca@1234"), role_id=role_customer.id),
        User(email="silviu@example.com", first_name="Silviu", last_name="Badea", phone="0700000024", password=password_hash.hash("Silviu@1234"), role_id=role_customer.id),
        User(email="teodora@example.com", first_name="Teodora", last_name="Matei", phone="0700000025", password=password_hash.hash("Teodora@1234"), role_id=role_customer.id),
        User(email="ulise@example.com", first_name="Ulise", last_name="Coman", phone="0700000026", password=password_hash.hash("Ulise@1234"), role_id=role_customer.id),
        User(email="veronica@example.com", first_name="Veronica", last_name="Tudor", phone="0700000027", password=password_hash.hash("Veronica@1234"), role_id=role_customer.id),
        User(email="xenia@example.com", first_name="Xenia", last_name="Florea", phone="0700000028", password=password_hash.hash("Xenia@1234"), role_id=role_customer.id),
        User(email="zoran@example.com", first_name="Zoran", last_name="Dumitrescu", phone="0700000029", password=password_hash.hash("Zoran@1234"), role_id=role_customer.id),
    ]
    db.add_all([admin, alice, bob, jason, charlie, diana, elena, florin, *extra_users])
    db.flush()

    # ── Categories ───────────────────────────────────────────────────────────
    electronics = Category(name="Electronics", description="Gadgets, devices, and accessories", created_by=admin.id)
    clothing = Category(name="Clothing", description="Apparel for all seasons", created_by=admin.id)
    books = Category(name="Books", description="Fiction, non-fiction, and technical literature", created_by=admin.id)
    home_garden = Category(name="Home & Garden", description="Everything for your home and outdoor space", created_by=admin.id)
    sports = Category(name="Sports & Fitness", description="Equipment and gear for an active lifestyle", created_by=admin.id)
    beauty = Category(name="Beauty & Health", description="Skincare, haircare, and wellness products", created_by=admin.id)
    db.add_all([electronics, clothing, books, home_garden, sports, beauty])
    db.flush()

    # ── Products ─────────────────────────────────────────────────────────────
    # Electronics
    laptop = Product(name="UltraBook Pro 14", description="Lightweight laptop with 14-inch IPS display, Intel Core i7, fast SSD storage.", price=Decimal("3499.99"), stock_quantity=15, category_id=electronics.id, created_by=admin.id)
    headphones = Product(name="SoundMax Wireless", description="Over-ear noise-cancelling headphones with 30-hour battery life.", price=Decimal("449.99"), stock_quantity=40, category_id=electronics.id, created_by=admin.id)
    smartwatch = Product(name="SmartWatch X1", description="Fitness and health tracking smartwatch with AMOLED display and GPS.", price=Decimal("799.99"), stock_quantity=25, category_id=electronics.id, created_by=admin.id)
    monitor = Product(name='4K Monitor 27"', description="27-inch 4K UHD IPS monitor with 144Hz refresh rate and USB-C connectivity.", price=Decimal("1899.99"), stock_quantity=10, category_id=electronics.id, created_by=admin.id)
    keyboard = Product(name="Mechanical Keyboard RGB", description="Tenkeyless mechanical keyboard with Cherry MX switches and per-key RGB lighting.", price=Decimal("349.99"), stock_quantity=30, category_id=electronics.id, created_by=admin.id)
    # Discontinued / inactive product (edge case)
    old_tablet = Product(name="TabMax 10 (Discontinued)", description="10-inch tablet — no longer produced.", price=Decimal("599.99"), stock_quantity=0, is_active=False, category_id=electronics.id, created_by=admin.id)

    # Clothing
    tshirt = Product(name="Classic Cotton T-Shirt", description="100% cotton unisex t-shirt, available in multiple colors and sizes.", price=Decimal("59.99"), stock_quantity=200, category_id=clothing.id, created_by=admin.id)
    jacket = Product(name="Winter Puffer Jacket", description="Warm, water-resistant puffer jacket for cold weather.", price=Decimal("299.99"), stock_quantity=50, category_id=clothing.id, created_by=admin.id)
    shorts = Product(name="Running Shorts", description="Lightweight moisture-wicking shorts for running and gym workouts.", price=Decimal("79.99"), stock_quantity=120, category_id=clothing.id, created_by=admin.id)
    jeans = Product(name="Denim Slim Fit Jeans", description="Classic slim-fit denim jeans with stretch fabric for comfort.", price=Decimal("149.99"), stock_quantity=75, category_id=clothing.id, created_by=admin.id)
    sweater = Product(name="Merino Wool Sweater", description="Fine merino wool crewneck sweater, soft and breathable.", price=Decimal("199.99"), stock_quantity=3, category_id=clothing.id, created_by=admin.id)  # low stock edge case

    # Books
    novel = Product(name="The Silent Algorithm", description="A sci-fi thriller about AI consciousness and the ethics of sentient machines.", price=Decimal("39.99"), stock_quantity=80, category_id=books.id, created_by=admin.id)
    clean_code = Product(name="Clean Code", description="A handbook of agile software craftsmanship by Robert C. Martin.", price=Decimal("89.99"), stock_quantity=60, category_id=books.id, created_by=admin.id)
    atomic_habits = Product(name="Atomic Habits", description="Practical strategies for building good habits and breaking bad ones.", price=Decimal("49.99"), stock_quantity=100, category_id=books.id, created_by=admin.id)
    dune = Product(name="Dune", description="Epic sci-fi novel by Frank Herbert set on the desert planet Arrakis.", price=Decimal("44.99"), stock_quantity=55, category_id=books.id, created_by=admin.id)

    # Home & Garden
    cutting_board = Product(name="Bamboo Cutting Board Set", description="Set of 3 premium bamboo cutting boards in different sizes.", price=Decimal("129.99"), stock_quantity=45, category_id=home_garden.id, created_by=admin.id)
    plant_pot = Product(name="Ceramic Plant Pot Set", description="Set of 4 minimalist ceramic pots with drainage holes and bamboo trays.", price=Decimal("179.99"), stock_quantity=35, category_id=home_garden.id, created_by=admin.id)
    desk_lamp = Product(name="LED Desk Lamp", description="Adjustable LED desk lamp with touch dimmer and USB charging port.", price=Decimal("149.99"), stock_quantity=0, category_id=home_garden.id, created_by=admin.id)  # out of stock edge case

    # Sports & Fitness
    yoga_mat = Product(name="Yoga Mat Premium", description="Non-slip 6mm thick yoga mat with alignment lines and carrying strap.", price=Decimal("139.99"), stock_quantity=60, category_id=sports.id, created_by=admin.id)
    resistance_bands = Product(name="Resistance Bands Set", description="Set of 5 latex resistance bands in varying strengths, includes carry bag.", price=Decimal("89.99"), stock_quantity=90, category_id=sports.id, created_by=admin.id)
    water_bottle = Product(name="Insulated Water Bottle 1L", description="Stainless steel double-wall insulated bottle, keeps drinks cold 24h / hot 12h.", price=Decimal("69.99"), stock_quantity=150, category_id=sports.id, created_by=admin.id)

    # Beauty & Health
    serum = Product(name="Vitamin C Brightening Serum", description="10% Vitamin C serum with hyaluronic acid for radiant, even-toned skin.", price=Decimal("119.99"), stock_quantity=70, category_id=beauty.id, created_by=admin.id)
    shampoo = Product(name="Natural Shampoo Bar", description="Zero-waste solid shampoo bar with argan oil and keratin, 80 washes.", price=Decimal("34.99"), stock_quantity=200, category_id=beauty.id, created_by=admin.id)

    db.add_all([
        laptop, headphones, smartwatch, monitor, keyboard, old_tablet,
        tshirt, jacket, shorts, jeans, sweater,
        novel, clean_code, atomic_habits, dune,
        cutting_board, plant_pot, desk_lamp,
        yoga_mat, resistance_bands, water_bottle,
        serum, shampoo,
    ])
    db.flush()

    # ── Product Images (placeholder URLs via placehold.co) ───────────────────
    # Format: https://placehold.co/600x400/BGCOLOR/TEXTCOLOR?text=Label
    db.add_all([
        # Electronics
        ProductImage(product_id=laptop.id,      image_path="https://placehold.co/600x400/1a1a2e/ffffff?text=UltraBook+Pro+14"),
        ProductImage(product_id=laptop.id,      image_path="https://placehold.co/600x400/16213e/ffffff?text=UltraBook+Side+View"),
        ProductImage(product_id=headphones.id,  image_path="https://placehold.co/600x400/0f3460/ffffff?text=SoundMax+Wireless"),
        ProductImage(product_id=headphones.id,  image_path="https://placehold.co/600x400/0f3460/ffffff?text=SoundMax+Folded"),
        ProductImage(product_id=smartwatch.id,  image_path="https://placehold.co/600x400/533483/ffffff?text=SmartWatch+X1"),
        ProductImage(product_id=smartwatch.id,  image_path="https://placehold.co/600x400/533483/ffffff?text=SmartWatch+Band"),
        ProductImage(product_id=monitor.id,     image_path="https://placehold.co/600x400/2b2d42/ffffff?text=4K+Monitor+27in"),
        ProductImage(product_id=keyboard.id,    image_path="https://placehold.co/600x400/212529/ffffff?text=Mechanical+Keyboard"),
        ProductImage(product_id=keyboard.id,    image_path="https://placehold.co/600x400/212529/ffffff?text=Keyboard+RGB+Glow"),
        ProductImage(product_id=old_tablet.id,  image_path="https://placehold.co/600x400/adb5bd/ffffff?text=TabMax+10"),
        # Clothing
        ProductImage(product_id=tshirt.id,      image_path="https://placehold.co/600x400/ffffff/333333?text=T-Shirt+White"),
        ProductImage(product_id=tshirt.id,      image_path="https://placehold.co/600x400/222222/ffffff?text=T-Shirt+Black"),
        ProductImage(product_id=tshirt.id,      image_path="https://placehold.co/600x400/3a86ff/ffffff?text=T-Shirt+Blue"),
        ProductImage(product_id=jacket.id,      image_path="https://placehold.co/600x400/343a40/ffffff?text=Puffer+Jacket"),
        ProductImage(product_id=jacket.id,      image_path="https://placehold.co/600x400/023e8a/ffffff?text=Puffer+Jacket+Navy"),
        ProductImage(product_id=shorts.id,      image_path="https://placehold.co/600x400/2dc653/ffffff?text=Running+Shorts"),
        ProductImage(product_id=jeans.id,       image_path="https://placehold.co/600x400/3d5a80/ffffff?text=Slim+Fit+Jeans"),
        ProductImage(product_id=sweater.id,     image_path="https://placehold.co/600x400/b5838d/ffffff?text=Merino+Sweater"),
        ProductImage(product_id=sweater.id,     image_path="https://placehold.co/600x400/6b4226/ffffff?text=Merino+Sweater+Brown"),
        # Books
        ProductImage(product_id=novel.id,       image_path="https://placehold.co/400x600/0d0d0d/00ffcc?text=The+Silent+Algorithm"),
        ProductImage(product_id=clean_code.id,  image_path="https://placehold.co/400x600/f8f9fa/212529?text=Clean+Code"),
        ProductImage(product_id=atomic_habits.id, image_path="https://placehold.co/400x600/ffd60a/000000?text=Atomic+Habits"),
        ProductImage(product_id=dune.id,        image_path="https://placehold.co/400x600/c77dff/0d0221?text=Dune"),
        # Home & Garden
        ProductImage(product_id=cutting_board.id, image_path="https://placehold.co/600x400/a0785a/ffffff?text=Bamboo+Cutting+Board"),
        ProductImage(product_id=plant_pot.id,   image_path="https://placehold.co/600x400/e9c46a/333333?text=Ceramic+Plant+Pots"),
        ProductImage(product_id=plant_pot.id,   image_path="https://placehold.co/600x400/264653/ffffff?text=Plant+Pots+Styled"),
        ProductImage(product_id=desk_lamp.id,   image_path="https://placehold.co/600x400/f4f1de/333333?text=LED+Desk+Lamp"),
        # Sports & Fitness
        ProductImage(product_id=yoga_mat.id,    image_path="https://placehold.co/600x400/8ecae6/333333?text=Yoga+Mat+Premium"),
        ProductImage(product_id=resistance_bands.id, image_path="https://placehold.co/600x400/06d6a0/ffffff?text=Resistance+Bands"),
        ProductImage(product_id=water_bottle.id, image_path="https://placehold.co/600x400/457b9d/ffffff?text=Insulated+Bottle"),
        ProductImage(product_id=water_bottle.id, image_path="https://placehold.co/600x400/1d3557/ffffff?text=Bottle+Black+Edition"),
        # Beauty & Health
        ProductImage(product_id=serum.id,       image_path="https://placehold.co/600x400/ffe8d6/8b5e3c?text=Vitamin+C+Serum"),
        ProductImage(product_id=shampoo.id,     image_path="https://placehold.co/600x400/ccd5ae/555555?text=Shampoo+Bar"),
    ])
    db.flush()

    # ── Product Attributes ───────────────────────────────────────────────────
    attr_color_black = ProductAttribute(name="color", value="black")
    attr_color_white = ProductAttribute(name="color", value="white")
    attr_color_blue = ProductAttribute(name="color", value="blue")
    attr_color_navy = ProductAttribute(name="color", value="navy")
    attr_color_silver = ProductAttribute(name="color", value="silver")
    attr_color_green = ProductAttribute(name="color", value="green")
    attr_size_xs = ProductAttribute(name="size", value="xs")
    attr_size_s = ProductAttribute(name="size", value="s")
    attr_size_m = ProductAttribute(name="size", value="m")
    attr_size_l = ProductAttribute(name="size", value="l")
    attr_size_xl = ProductAttribute(name="size", value="xl")
    attr_size_xxl = ProductAttribute(name="size", value="xxl")
    attr_ram_16 = ProductAttribute(name="ram", value="16gb")
    attr_ram_32 = ProductAttribute(name="ram", value="32gb")
    attr_storage_512 = ProductAttribute(name="storage", value="512gb")
    attr_storage_1tb = ProductAttribute(name="storage", value="1tb")
    attr_switch_red = ProductAttribute(name="switch", value="cherry-mx-red")
    attr_switch_blue = ProductAttribute(name="switch", value="cherry-mx-blue")
    attr_band_black = ProductAttribute(name="band_color", value="black")
    attr_band_white = ProductAttribute(name="band_color", value="white")
    attr_band_coral = ProductAttribute(name="band_color", value="coral")
    db.add_all([
        attr_color_black, attr_color_white, attr_color_blue, attr_color_navy,
        attr_color_silver, attr_color_green,
        attr_size_xs, attr_size_s, attr_size_m, attr_size_l, attr_size_xl, attr_size_xxl,
        attr_ram_16, attr_ram_32, attr_storage_512, attr_storage_1tb,
        attr_switch_red, attr_switch_blue,
        attr_band_black, attr_band_white, attr_band_coral,
    ])
    db.flush()

    db.add_all([
        # Laptop
        ProductAttributeLink(product_id=laptop.id, attribute_id=attr_color_black.id),
        ProductAttributeLink(product_id=laptop.id, attribute_id=attr_color_silver.id),
        ProductAttributeLink(product_id=laptop.id, attribute_id=attr_ram_16.id),
        ProductAttributeLink(product_id=laptop.id, attribute_id=attr_ram_32.id),
        ProductAttributeLink(product_id=laptop.id, attribute_id=attr_storage_512.id),
        ProductAttributeLink(product_id=laptop.id, attribute_id=attr_storage_1tb.id),
        # Headphones
        ProductAttributeLink(product_id=headphones.id, attribute_id=attr_color_black.id),
        ProductAttributeLink(product_id=headphones.id, attribute_id=attr_color_white.id),
        # SmartWatch
        ProductAttributeLink(product_id=smartwatch.id, attribute_id=attr_band_black.id),
        ProductAttributeLink(product_id=smartwatch.id, attribute_id=attr_band_white.id),
        ProductAttributeLink(product_id=smartwatch.id, attribute_id=attr_band_coral.id),
        # Keyboard
        ProductAttributeLink(product_id=keyboard.id, attribute_id=attr_color_black.id),
        ProductAttributeLink(product_id=keyboard.id, attribute_id=attr_color_white.id),
        ProductAttributeLink(product_id=keyboard.id, attribute_id=attr_switch_red.id),
        ProductAttributeLink(product_id=keyboard.id, attribute_id=attr_switch_blue.id),
        # T-Shirt
        ProductAttributeLink(product_id=tshirt.id, attribute_id=attr_color_black.id),
        ProductAttributeLink(product_id=tshirt.id, attribute_id=attr_color_white.id),
        ProductAttributeLink(product_id=tshirt.id, attribute_id=attr_color_blue.id),
        ProductAttributeLink(product_id=tshirt.id, attribute_id=attr_size_xs.id),
        ProductAttributeLink(product_id=tshirt.id, attribute_id=attr_size_s.id),
        ProductAttributeLink(product_id=tshirt.id, attribute_id=attr_size_m.id),
        ProductAttributeLink(product_id=tshirt.id, attribute_id=attr_size_l.id),
        ProductAttributeLink(product_id=tshirt.id, attribute_id=attr_size_xl.id),
        # Jacket
        ProductAttributeLink(product_id=jacket.id, attribute_id=attr_color_black.id),
        ProductAttributeLink(product_id=jacket.id, attribute_id=attr_color_navy.id),
        ProductAttributeLink(product_id=jacket.id, attribute_id=attr_size_s.id),
        ProductAttributeLink(product_id=jacket.id, attribute_id=attr_size_m.id),
        ProductAttributeLink(product_id=jacket.id, attribute_id=attr_size_l.id),
        ProductAttributeLink(product_id=jacket.id, attribute_id=attr_size_xl.id),
        # Running Shorts
        ProductAttributeLink(product_id=shorts.id, attribute_id=attr_color_black.id),
        ProductAttributeLink(product_id=shorts.id, attribute_id=attr_color_blue.id),
        ProductAttributeLink(product_id=shorts.id, attribute_id=attr_color_green.id),
        ProductAttributeLink(product_id=shorts.id, attribute_id=attr_size_s.id),
        ProductAttributeLink(product_id=shorts.id, attribute_id=attr_size_m.id),
        ProductAttributeLink(product_id=shorts.id, attribute_id=attr_size_l.id),
        ProductAttributeLink(product_id=shorts.id, attribute_id=attr_size_xl.id),
        # Jeans
        ProductAttributeLink(product_id=jeans.id, attribute_id=attr_color_blue.id),
        ProductAttributeLink(product_id=jeans.id, attribute_id=attr_color_black.id),
        ProductAttributeLink(product_id=jeans.id, attribute_id=attr_size_s.id),
        ProductAttributeLink(product_id=jeans.id, attribute_id=attr_size_m.id),
        ProductAttributeLink(product_id=jeans.id, attribute_id=attr_size_l.id),
        ProductAttributeLink(product_id=jeans.id, attribute_id=attr_size_xl.id),
        ProductAttributeLink(product_id=jeans.id, attribute_id=attr_size_xxl.id),
        # Sweater
        ProductAttributeLink(product_id=sweater.id, attribute_id=attr_size_m.id),
        ProductAttributeLink(product_id=sweater.id, attribute_id=attr_size_l.id),
        # Water Bottle
        ProductAttributeLink(product_id=water_bottle.id, attribute_id=attr_color_black.id),
        ProductAttributeLink(product_id=water_bottle.id, attribute_id=attr_color_silver.id),
        ProductAttributeLink(product_id=water_bottle.id, attribute_id=attr_color_blue.id),
    ])
    db.flush()

    # ── Cart Entries ─────────────────────────────────────────────────────────
    db.add_all([
        CartEntry(user_id=alice.id,   product_id=laptop.id,      quantity=1),
        CartEntry(user_id=alice.id,   product_id=tshirt.id,      quantity=2),
        CartEntry(user_id=alice.id,   product_id=serum.id,       quantity=1),
        CartEntry(user_id=bob.id,     product_id=headphones.id,  quantity=1),
        CartEntry(user_id=bob.id,     product_id=yoga_mat.id,    quantity=1),
        CartEntry(user_id=jason.id,   product_id=clean_code.id,  quantity=1),
        CartEntry(user_id=jason.id,   product_id=atomic_habits.id, quantity=1),
        CartEntry(user_id=diana.id,   product_id=smartwatch.id,  quantity=1),
        CartEntry(user_id=diana.id,   product_id=resistance_bands.id, quantity=2),
        CartEntry(user_id=florin.id,  product_id=keyboard.id,    quantity=1),
        CartEntry(user_id=florin.id,  product_id=monitor.id,     quantity=1),
        CartEntry(user_id=charlie.id, product_id=shampoo.id,     quantity=3),
    ])
    db.flush()

    # ── Orders (all statuses covered) ────────────────────────────────────────
    order_delivered = Order(user_id=alice.id, payment_type="card", status="delivered", shipping_address_id=addr_alice.id, billing_address_id=addr_alice.id)
    order_pending = Order(user_id=bob.id, payment_type="cash", status="pending", shipping_address_id=addr_ship1.id, billing_address_id=addr_bob.id)
    order_confirmed = Order(user_id=diana.id, payment_type="card", status="confirmed", shipping_address_id=addr_diana.id, billing_address_id=addr_diana.id)
    order_in_delivery = Order(user_id=elena.id, payment_type="card", status="in_delivery", shipping_address_id=addr_ship2.id, billing_address_id=addr_elena.id)
    order_completed = Order(user_id=florin.id, payment_type="card", status="completed", shipping_address_id=addr_florin.id, billing_address_id=addr_florin.id)
    order_cancelled = Order(user_id=jason.id, payment_type="cash", status="cancelled", shipping_address_id=None, billing_address_id=None)
    order_returned = Order(user_id=charlie.id, payment_type="card", status="returned", shipping_address_id=addr_ship1.id, billing_address_id=addr_ship1.id)
    # Alice second order
    order_alice2 = Order(user_id=alice.id, payment_type="card", status="completed", shipping_address_id=addr_alice.id, billing_address_id=addr_alice.id)
    db.add_all([order_delivered, order_pending, order_confirmed, order_in_delivery, order_completed, order_cancelled, order_returned, order_alice2])
    db.flush()

    db.add_all([
        # order_delivered: alice bought t-shirt + novel
        OrderItem(order_id=order_delivered.id, product_id=tshirt.id, name=tshirt.name, quantity=3, price_per_piece=tshirt.price),
        OrderItem(order_id=order_delivered.id, product_id=novel.id, name=novel.name, quantity=1, price_per_piece=novel.price),
        # order_pending: bob buying headphones + yoga mat
        OrderItem(order_id=order_pending.id, product_id=headphones.id, name=headphones.name, quantity=1, price_per_piece=headphones.price),
        OrderItem(order_id=order_pending.id, product_id=yoga_mat.id, name=yoga_mat.name, quantity=1, price_per_piece=yoga_mat.price),
        # order_confirmed: diana buying smartwatch
        OrderItem(order_id=order_confirmed.id, product_id=smartwatch.id, name=smartwatch.name, quantity=1, price_per_piece=smartwatch.price),
        OrderItem(order_id=order_confirmed.id, product_id=resistance_bands.id, name=resistance_bands.name, quantity=2, price_per_piece=resistance_bands.price),
        # order_in_delivery: elena buying books
        OrderItem(order_id=order_in_delivery.id, product_id=clean_code.id, name=clean_code.name, quantity=1, price_per_piece=clean_code.price),
        OrderItem(order_id=order_in_delivery.id, product_id=atomic_habits.id, name=atomic_habits.name, quantity=1, price_per_piece=atomic_habits.price),
        OrderItem(order_id=order_in_delivery.id, product_id=dune.id, name=dune.name, quantity=1, price_per_piece=dune.price),
        # order_completed: florin bought laptop + keyboard
        OrderItem(order_id=order_completed.id, product_id=laptop.id, name=laptop.name, quantity=1, price_per_piece=laptop.price),
        OrderItem(order_id=order_completed.id, product_id=keyboard.id, name=keyboard.name, quantity=1, price_per_piece=keyboard.price),
        # order_cancelled: jason cancelled (jeans + jacket)
        OrderItem(order_id=order_cancelled.id, product_id=jeans.id, name=jeans.name, quantity=1, price_per_piece=jeans.price),
        OrderItem(order_id=order_cancelled.id, product_id=jacket.id, name=jacket.name, quantity=1, price_per_piece=jacket.price),
        # order_returned: charlie returned shampoo bars
        OrderItem(order_id=order_returned.id, product_id=shampoo.id, name=shampoo.name, quantity=4, price_per_piece=shampoo.price),
        # order_alice2: alice's second completed order (monitor + serum)
        OrderItem(order_id=order_alice2.id, product_id=monitor.id, name=monitor.name, quantity=1, price_per_piece=monitor.price),
        OrderItem(order_id=order_alice2.id, product_id=serum.id, name=serum.name, quantity=2, price_per_piece=serum.price),
    ])

    db.commit()
    print("Database seeded with mock data.")