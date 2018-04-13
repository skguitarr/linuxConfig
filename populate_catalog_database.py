from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Items, User
 
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)
session = DBSession()

#Add initial users
user1 = User(id=1, username="garyoldman", email="goldman@gmail.com")
user2 = User(id=2, username="cchristian", email="charliechristian@gmail.com")
user3 = User(id=3, username="djangoreinhardt", email="djangoreinhardt@gmail.com")
session.add(user1)
session.add(user2)
session.add(user3)
session.commit()

#Setup Gibson category
category1 = Category(name = "Gibson")
session.add(category1)
session.commit()

item1 = Items(name = "Hummingbird", description = "Acoustic guitar. Popular in country music.",   category_id = category1.id, user_id=1)
session.add(item1)
session.commit()

item2 = Items(name = "Hummingbird Pro", description = "Acoustic guitar. Popular in country music.",   category_id = category1.id, user_id=1)
session.add(item2)
session.commit()

item3 = Items(name = "SG", description = "Hard rocking classic.",   category_id = category1.id, user_id=1)
session.add(item3)
session.commit()

item4 = Items(name = "Les Paul Classic", description = "The quintessential classic rock guitar with amazing tone!",   category_id = category1.id, user_id=1)
session.add(item4)
session.commit()

item5 = Items(name = "Les Paul Studio", description = "Studio version of the Les Paul Classic!",   category_id = category1.id, user_id=1)
session.add(item5)
session.commit()

item6 = Items(name = "Les Paul Jr", description = "More affordable version of the Les Paul Classic.  1 P-90 pickup with amazing tone!",   category_id = category1.id, user_id=1)
session.add(item6)
session.commit()

#Setup Fender category
category1 = Category(name = "Fender")
session.add(category1)
session.commit()

item1 = Items(name = "Stratocaster", description = "Rock guitar classic. Guitar of choice of legends such as Jimi Hendrix, Eric Clapton, and many more!",   category_id = category1.id, user_id=1)
session.add(item1)
session.commit()

item2 = Items(name = "Telecaster", description = "Country music electic goto guitar!  Used by greats such as Waylon Jennings and Bruce Springsteen.",   category_id = category1.id, user_id=1)
session.add(item2)
session.commit()

item3 = Items(name = "Jaguar", description = "Jazzy sounds with many tone options. Made popular again by Curt Kobain in the 90s.",   category_id = category1.id, user_id=1)
session.add(item3)
session.commit()

#Setup Martin category
category1 = Category(name = "Martin")
session.add(category1)
session.commit()

item1 = Items(name = "Dreadknought Classic", description = "Acoustic guitar. Popular in all styles of music.",   category_id = category1.id, user_id=1)
session.add(item1)
session.commit()

item2 = Items(name = "DM100", description = "Acoustic guitar.",   category_id = category1.id, user_id=1)
session.add(item2)
session.commit()

#Setup Music Man category
category1 = Category(name = "Music Man")
session.add(category1)
session.commit()

item1 = Items(name = "Axis Pro", description = "Perfect for rock music.  Designed by Eddie Van Halen.",   category_id = category1.id, user_id=2)
session.add(item1)
session.commit()

item2 = Items(name = "Stingray", description = "Great for all styles of music!",   category_id = category1.id, user_id=2)
session.add(item2)
session.commit()

item3 = Items(name = "Steve Lukather", description = "Designed by the Toto lead guitarist himself and member of the Ringo Starr All-Star band!",   category_id = category1.id, user_id=2)
session.add(item3)
session.commit()

#Setup PRS category
category1 = Category(name = "PRS")
session.add(category1)
session.commit()

item1 = Items(name = "McCarty", description = "Don't pick it up because you'll want to buy this one for sure.",   category_id = category1.id, user_id=2)
session.add(item1)
session.commit()

item2 = Items(name = "Custom 22", description = "Electric guitar with 22 frets.",   category_id = category1.id, user_id=2)
session.add(item2)
session.commit()

item3 = Items(name = "Custom 24", description = "Electric guitar with 24 frets.",   category_id = category1.id, user_id=2)
session.add(item3)
session.commit()

print "added menu items!"
