from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_setup import Categories, Lineage, User, Items, Base
from passlib.apps import custom_app_context as pwd_context
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy import create_engine, asc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


engine = create_engine('sqlite:///itemCatalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes,  you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()
str64 = pwd_context.encrypt("admin")
Us1 = User(id="1", username="admin",  password_hash=str64, 
           email="gabor.dubniczki@ge.com")
session.add(Us1)
session.commit()
Cat1 = Categories(id="1",
                  name="Main Categories", user=Us1)
session.add(Cat1)
session.commit()
Cat2 = Categories(id="2",
                  user=Us1,
                  name="Engines")
session.add(Cat2)
session.commit()
Cat3 = Categories(id="3",
                  user=Us1,
                  name="Mopar")
session.add(Cat3)
session.commit()
Cat4 = Categories(id="4",
                  user=Us1,
                  name="FoMoCo")
session.add(Cat4)
session.commit()
Cat5 = Categories(id="5",
                  user=Us1,
                  name="GM")
session.add(Cat5)
session.commit()
Cat6 = Categories(id="6",
                  user=Us1,
                  name="Small Blocks")
session.add(Cat6)
session.commit()
Cat7 = Categories(id="7",
                  user=Us1,
                  name="Big Blocks")
session.add(Cat7)
session.commit()
Cat8 = Categories(id="8",
                  user=Us1,
                  name="Small Blocks")
session.add(Cat8)
session.commit()
Cat9 = Categories(id="9",
                  user=Us1,
                  name="Big Blocks")
session.add(Cat9)
session.commit()
Cat10 = Categories(id="10",
                   user=Us1,
                   name="Small Blocks")
session.add(Cat10)
session.commit()
Cat11 = Categories(id="11",
                   user=Us1,
                   name="Big Blocks")
session.add(Cat11)
session.commit()
Cat12 = Categories(id="12",
                   user=Us1,
                   name="Intake Manifolds")
session.add(Cat12)
session.commit()
Cat13 = Categories(id="13",
                   user=Us1,
                   name="Low Rise")
session.add(Cat13)
session.commit()
Cat14 = Categories(id="14",
                   user=Us1,
                   name="High Rise")
session.add(Cat14)
session.commit()
Cat15 = Categories(id="15",
                   user=Us1,
                   name="Single Plane")
session.add(Cat15)
session.commit()
Cat16 = Categories(id="16",
                   user=Us1,
                   name="Dual Plane")
session.add(Cat16)
session.commit()
Cat17 = Categories(id="17",
                   user=Us1,
                   name="Single Plane")
session.add(Cat17)
session.commit()
Cat18 = Categories(id="18",
                   user=Us1,
                   name="Dual Plane")
session.add(Cat18)
session.commit()
Cat19 = Categories(id="19",
                   user=Us1,
                   name="Cross Ram")
session.add(Cat19)
session.commit()
Cat20 = Categories(id="20",
                   user=Us1,
                   name="Carbs")
session.add(Cat20)
session.commit()
Cat21 = Categories(id="21",
                   user=Us1,
                   name="2 barrel")
session.add(Cat21)
session.commit()
Cat22 = Categories(id="22",
                   user=Us1,
                   name="4 barrel")
session.add(Cat22)
session.commit()
Cat23 = Categories(id="23",
                   user=Us1,
                   name="6 pack")
session.add(Cat23)
session.commit()
Cat24 = Categories(id="24",
                   user=Us1,
                   name="EFI")
session.add(Cat24)
session.commit()
Lin1 = Lineage(id="1", parent_id="1", child_id="2")
session.add(Lin1)
session.commit()
Lin2 = Lineage(id="2", parent_id="1", child_id="12")
session.add(Lin2)
session.commit()
Lin3 = Lineage(id="3", parent_id="1", child_id="20")
session.add(Lin3)
session.commit()
Lin4 = Lineage(id="4", parent_id="1", child_id="24")
session.add(Lin4)
session.commit()
Lin5 = Lineage(id="5", parent_id="2", child_id="3")
session.add(Lin5)
session.commit()
Lin6 = Lineage(id="6", parent_id="2", child_id="4")
session.add(Lin6)
session.commit()
Lin7 = Lineage(id="7", parent_id="2", child_id="5")
session.add(Lin7)
session.commit()
Lin8 = Lineage(id="8", parent_id="3", child_id="6")
session.add(Lin8)
session.commit()
Lin9 = Lineage(id="9", parent_id="3", child_id="7")
session.add(Lin9)
session.commit()
Lin10 = Lineage(id="10", parent_id="4", child_id="8")
session.add(Lin10)
session.commit()
Lin11 = Lineage(id="11", parent_id="4", child_id="9")
session.add(Lin11)
session.commit()
Lin12 = Lineage(id="12", parent_id="5", child_id="10")
session.add(Lin12)
session.commit()
Lin13 = Lineage(id="13", parent_id="5", child_id="11")
session.add(Lin13)
session.commit()
Lin14 = Lineage(id="14", parent_id="12", child_id="13")
session.add(Lin14)
session.commit()
Lin15 = Lineage(id="15", parent_id="12", child_id="14")
session.add(Lin15)
session.commit()
Lin16 = Lineage(id="16", parent_id="13", child_id="15")
session.add(Lin16)
session.commit()
Lin17 = Lineage(id="17", parent_id="13", child_id="16")
session.add(Lin17)
session.commit()
Lin18 = Lineage(id="18", parent_id="14", child_id="17")
session.add(Lin18)
session.commit()
Lin19 = Lineage(id="19", parent_id="14", child_id="18")
session.add(Lin19)
session.commit()
Lin20 = Lineage(id="20", parent_id="14", child_id="19")
session.add(Lin20)
session.commit()
Lin21 = Lineage(id="21", parent_id="20", child_id="21")
session.add(Lin21)
session.commit()
Lin22 = Lineage(id="22", parent_id="20", child_id="22")
session.add(Lin22)
session.commit()
Lin23 = Lineage(id="23", parent_id="20", child_id="23")
session.add(Lin23)
session.commit()
Item1 = Items(id="1",
              user=Us1,
              name="Dodge LA 318",
              price="250 USD", category_id="6",
              description="Small Block ")
session.add(Item1)
session.commit()
Item2 = Items(id="2",
              user=Us1,
              name="Dodge LA 340",
              price="400 USD",
              category_id="6",
              description="Small Block ")
session.add(Item2)
session.commit()
Item3 = Items(id="3",
              user=Us1,
              name="Dodge B 383",
              price="1200 USD",
              category_id="7",
              description="Big Block")
session.add(Item3)
session.commit()
Item4 = Items(id="4",
              user=Us1,
              name="Dodge B 400",
              price="1500 USD",
              category_id="7",
              description="Big Block")
session.add(Item4)
session.commit()
Item5 = Items(id="5",
              user=Us1,
              name="Dodge RB 426 ",
              price="2000 USD",
              category_id="7",
              description="Big Block")
session.add(Item5)
session.commit()
Item6 = Items(id="6",
              user=Us1,
              name="Dodge RB 440",
              price="12000 USD",
              category_id="7",
              description="Big Block")
session.add(Item6)
session.commit()
Item7 = Items(id="7",
              user=Us1,
              name="Dodge 426 Hemi",
              price="35000 USD",
              category_id="7",
              description="Hemi")
session.add(Item7)
session.commit()
Item8 = Items(id="8",
              user=Us1,
              name="Chevy 265 Turbo Fire",
              price="1200 USD",
              category_id="10",
              description="Small Block ")
session.add(Item8)
session.commit()
Item9 = Items(id="9",
              user=Us1,
              name="Chevy 283 Turbo Fire",
              price="1500 USD",
              category_id="10",
              description="Small Block ")
session.add(Item9)
session.commit()
Item10 = Items(id="10",
               user=Us1,
               name="Chevy 307 Turbo Fire",
               price="1800 USD",
               category_id="10",
               description="Small Block ")
session.add(Item10)
session.commit()
Item11 = Items(id="11",
               user=Us1,
               name="Chevy 302 SCCA",
               price="1200 USD",
               category_id="10",
               description="Small Block ")
session.add(Item11)
session.commit()
Item12 = Items(id="12",
               user=Us1,
               name="Chevy 327 L84",
               price="1500 USD",
               category_id="10",
               description="Small Block ")
session.add(Item12)
session.commit()
Item13 = Items(id="13",
               user=Us1,
               name="Chevy 327 L79",
               price="1800 USD",
               category_id="10",
               description="Small Block ")
session.add(Item13)
session.commit()
Item14 = Items(id="14",
               user=Us1,
               name="Chevy 358",
               price="1800 USD",
               category_id="11",
               description="Big Block")
session.add(Item14)
session.commit()
Item15 = Items(id="15",
               user=Us1,
               name="Chevy 396",
               price="2100 USD",
               category_id="11",
               description="Big Block")
session.add(Item15)
session.commit()
Item16 = Items(id="16",
               user=Us1,
               name="Chevy 409",
               price="2550 USD",
               category_id="11",
               description="Big Block")
session.add(Item16)
session.commit()
Item17 = Items(id="17",
               user=Us1,
               name="Chevy 427 Z11",
               price="3225 USD",
               category_id="11",
               description="Big Block")
session.add(Item17)
session.commit()
Item18 = Items(id="18",
               user=Us1,
               name="Chevy 427 L88",
               price="4225 USD",
               category_id="11",
               description="Big Block")
session.add(Item18)
session.commit()
Item19 = Items(id="19",
               user=Us1,
               name="Chevy 454 LS4",
               price="5725 USD",
               category_id="11",
               description="Big Block")
session.add(Item19)
session.commit()
Item20 = Items(id="20",
               user=Us1,
               name="Chevy 454 LS5",
               price="8025 USD",
               category_id="11",
               description="Big Block")
session.add(Item20)
session.commit()
Item21 = Items(id="21",
               user=Us1,
               name="Chevy 454 LS6",
               price="11525 USD",
               category_id="11",
               description="Big Block")
session.add(Item21)
session.commit()
Item22 = Items(id="22",
               user=Us1,
               name="Ford 289",
               price="1200 USD",
               category_id="8",
               description="Small Block ")
session.add(Item22)
session.commit()
Item23 = Items(id="23",
               user=Us1,
               name="Ford 351 Windsor",
               price="1500 USD",
               category_id="8",
               description="Small Block ")
session.add(Item23)
session.commit()
Item24 = Items(id="24",
               user=Us1,
               name="Ford 427",
               price="2000 USD",
               category_id="9",
               description="Big Block")
session.add(Item24)
session.commit()
Item25 = Items(id="25",
               user=Us1,
               name="Ford 428",
               price="2500 USD",
               category_id="9",
               description="Big Block")
session.add(Item25)
session.commit()
Item26 = Items(id="26",
               user=Us1,
               name="Ford 429",
               price="4000 USD",
               category_id="9",
               description="Big Block")
session.add(Item26)
session.commit()
Item27 = Items(id="27",
               user=Us1,
               name="Ford 429 SOHC",
               price="20000 USD",
               category_id="9",
               description="Big Block")
session.add(Item27)
session.commit()
Item28 = Items(id="28",
               user=Us1,
               name="Edelbrock 5001",
               price="201 USD",
               category_id="15",
               description="""Intake Manifold,  Torker II,  Single Plane,
               Aluminum,  Natural,  Square Bore,  Chevy,
               Small Block,  Each""")
session.add(Item28)
session.commit()
Item29 = Items(id="29",
               user=Us1,
               name="Edelbrock 2701",
               price="150 USD",
               category_id="16",
               description="""Intake Manifold,  Performer EPS,  Dual Plane,
                           Aluminum,  Natural,  Square Bore,  Chevy,
                           Small Block,  Each""")
session.add(Item29)
session.commit()
Item30 = Items(id="30",
               user=Us1,
               name="Edelbrock 2925",
               price="330 USD",
               category_id="17",
               description="""Edelbrock 2925 - Edelbrock Super Victor
                           Intake Manifolds""")
session.add(Item30)
session.commit()
Item31 = Items(id="31",
               user=Us1,
               name="Edelbrock 7101",
               price="330 USD",
               category_id="18",
               description="""Edelbrock 7101 Sbc 1955-86 Intake Manifold
                           Performer Rpm Dual Plane""")
session.add(Item31)
session.commit()
Item32 = Items(id="32",
               user=Us1,
               name="Edelbrock 7141",
               price="1280 USD",
               category_id="19",
               description="""Edelbrock Cross-Ram LS3 intake
                           manifolds are ideal for anyone looking
                           to combine great looks and outstanding
                           performance between 1,  500 - 7,  000 rpm.""")
session.add(Item32)
session.commit()
Item33 = Items(id="33",
               user=Us1,
               name="Rochester 2GC",
               price="120 USD",
               category_id="21",
               description="285 CFM")
session.add(Item33)
session.commit()
Item34 = Items(id="34",
               user=Us1,
               name="Holley Classic 4160",
               price="350 USD",
               category_id="22",
               description="600 CFM")
session.add(Item34)
session.commit()
Item35 = Items(id="35",
               user=Us1,
               name="Holley Classic 2300",
               price="1000 USD",
               category_id="23",
               description="1350 CFM")
session.add(Item35)
session.commit()


print "added the items to the itemCatalog! Rock the kashbah"
