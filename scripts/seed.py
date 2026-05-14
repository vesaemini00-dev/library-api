import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import date, timedelta
from app.database import SessionLocal
from app import models

def seed():
    db = SessionLocal()

    # Clear existing data
    db.query(models.Loan).delete()
    db.query(models.BookAuthor).delete()
    db.query(models.Book).delete()
    db.query(models.Author).delete()
    db.query(models.Category).delete()
    db.query(models.Member).delete()
    db.commit()

    # ─── CATEGORIES ──────────────────────────────────────────────────
    categories = [
        models.Category(name="Fiction"),
        models.Category(name="Science"),
        models.Category(name="History"),
        models.Category(name="Technology"),
        models.Category(name="Philosophy"),
    ]
    db.add_all(categories)
    db.commit()

    fiction, science, history, technology, philosophy = categories

    # ─── AUTHORS ─────────────────────────────────────────────────────
    authors = [
        models.Author(full_name="George Orwell", country="UK"),
        models.Author(full_name="Yuval Noah Harari", country="Israel"),
        models.Author(full_name="Frank Herbert", country="USA"),
        models.Author(full_name="Carl Sagan", country="USA"),
        models.Author(full_name="J.R.R. Tolkien", country="UK"),
        models.Author(full_name="Stephen Hawking", country="UK"),
        models.Author(full_name="Malcolm Gladwell", country="Canada"),
        models.Author(full_name="Aldous Huxley", country="UK"),
        models.Author(full_name="Isaac Asimov", country="USA"),
        models.Author(full_name="Hannah Arendt", country="Germany"),
    ]
    db.add_all(authors)
    db.commit()

    orwell, harari, herbert, sagan, tolkien, hawking, gladwell, huxley, asimov, arendt = authors

    # ─── BOOKS ───────────────────────────────────────────────────────
    books = [
        models.Book(title="1984", isbn="978-0451524935", published_year=1949, total_copies=4, category_id=fiction.id),
        models.Book(title="Animal Farm", isbn="978-0451526342", published_year=1945, total_copies=3, category_id=fiction.id),
        models.Book(title="Sapiens", isbn="978-0062316097", published_year=2011, total_copies=5, category_id=history.id),
        models.Book(title="Homo Deus", isbn="978-0062464316", published_year=2015, total_copies=3, category_id=history.id),
        models.Book(title="Dune", isbn="978-0441013593", published_year=1965, total_copies=4, category_id=fiction.id),
        models.Book(title="Cosmos", isbn="978-0345539434", published_year=1980, total_copies=3, category_id=science.id),
        models.Book(title="The Lord of the Rings", isbn="978-0618640157", published_year=1954, total_copies=4, category_id=fiction.id),
        models.Book(title="A Brief History of Time", isbn="978-0553380163", published_year=1988, total_copies=3, category_id=science.id),
        models.Book(title="The Hobbit", isbn="978-0547928227", published_year=1937, total_copies=4, category_id=fiction.id),
        models.Book(title="Outliers", isbn="978-0316017930", published_year=2008, total_copies=3, category_id=technology.id),
        models.Book(title="Brave New World", isbn="978-0060850524", published_year=1932, total_copies=3, category_id=fiction.id),
        models.Book(title="Foundation", isbn="978-0553293357", published_year=1951, total_copies=4, category_id=science.id),
        models.Book(title="The Origins of Totalitarianism", isbn="978-0156701532", published_year=1951, total_copies=2, category_id=philosophy.id),
        models.Book(title="Pale Blue Dot", isbn="978-0345376596", published_year=1994, total_copies=3, category_id=science.id),
        models.Book(title="The Tipping Point", isbn="978-0316346627", published_year=2000, total_copies=3, category_id=technology.id),
        models.Book(title="I, Robot", isbn="978-0553294385", published_year=1950, total_copies=3, category_id=science.id),
        models.Book(title="The Grand Design", isbn="978-0553840926", published_year=2010, total_copies=2, category_id=science.id),
        models.Book(title="Thinking Fast and Slow", isbn="978-0374533557", published_year=2011, total_copies=3, category_id=philosophy.id),
        models.Book(title="The Silmarillion", isbn="978-0618391110", published_year=1977, total_copies=2, category_id=fiction.id),
        models.Book(title="Nexus", isbn="978-0062316110", published_year=2023, total_copies=3, category_id=history.id),
    ]
    db.add_all(books)
    db.commit()

    (b1984, banimal, bsapiens, bhomodeus, bdune, bcosmos, blotr, bbriefhistory,
     bhobbit, boutliers, bbrave, bfoundation, borigins, bpaledot, btipping,
     birobot, bgrand, bthinking, bsilmarillion, bnexus) = books

    # ─── BOOK-AUTHOR LINKS ───────────────────────────────────────────
    b1984.authors = [orwell]
    banimal.authors = [orwell]
    bsapiens.authors = [harari]
    bhomodeus.authors = [harari]
    bnexus.authors = [harari]
    bdune.authors = [herbert]
    bcosmos.authors = [sagan]
    bpaledot.authors = [sagan]
    blotr.authors = [tolkien]
    bhobbit.authors = [tolkien]
    bsilmarillion.authors = [tolkien]
    bbriefhistory.authors = [hawking]
    bgrand.authors = [hawking, harari]   # multiple authors
    boutliers.authors = [gladwell]
    btipping.authors = [gladwell]
    bbrave.authors = [huxley]
    bfoundation.authors = [asimov, sagan]  # multiple authors
    birobot.authors = [asimov]
    borigins.authors = [arendt]
    bthinking.authors = [sagan, arendt]  # multiple authors
    db.commit()

    # ─── MEMBERS ─────────────────────────────────────────────────────
    members = [
        models.Member(full_name="Alice Johnson", email="alice@email.com", join_date=date(2023, 1, 10), is_active=True),
        models.Member(full_name="Bob Smith", email="bob@email.com", join_date=date(2023, 2, 15), is_active=True),
        models.Member(full_name="Carol White", email="carol@email.com", join_date=date(2023, 3, 20), is_active=True),
        models.Member(full_name="David Brown", email="david@email.com", join_date=date(2023, 4, 5), is_active=True),
        models.Member(full_name="Eva Green", email="eva@email.com", join_date=date(2023, 5, 12), is_active=True),
        models.Member(full_name="Frank Miller", email="frank@email.com", join_date=date(2023, 6, 18), is_active=False),
        models.Member(full_name="Grace Lee", email="grace@email.com", join_date=date(2023, 7, 22), is_active=True),
        models.Member(full_name="Henry Wilson", email="henry@email.com", join_date=date(2023, 8, 30), is_active=True),
        models.Member(full_name="Isla Davis", email="isla@email.com", join_date=date(2023, 9, 14), is_active=True),
        models.Member(full_name="Jack Taylor", email="jack@email.com", join_date=date(2023, 10, 25), is_active=True),
    ]
    db.add_all(members)
    db.commit()

    alice, bob, carol, david, eva, frank, grace, henry, isla, jack = members

    # ─── LOANS ───────────────────────────────────────────────────────
    today = date.today()

    loans = [
        # Returned loans
        models.Loan(member_id=alice.id, book_id=b1984.id, loan_date=date(2024,1,1), due_date=date(2024,1,15), return_date=date(2024,1,14)),
        models.Loan(member_id=alice.id, book_id=bsapiens.id, loan_date=date(2024,2,1), due_date=date(2024,2,15), return_date=date(2024,2,13)),
        models.Loan(member_id=bob.id, book_id=bdune.id, loan_date=date(2024,1,5), due_date=date(2024,1,20), return_date=date(2024,1,18)),
        models.Loan(member_id=bob.id, book_id=blotr.id, loan_date=date(2024,2,10), due_date=date(2024,2,25), return_date=date(2024,2,24)),
        models.Loan(member_id=carol.id, book_id=bbrave.id, loan_date=date(2024,3,1), due_date=date(2024,3,15), return_date=date(2024,3,14)),
        models.Loan(member_id=carol.id, book_id=bfoundation.id, loan_date=date(2024,3,20), due_date=date(2024,4,5), return_date=date(2024,4,3)),
        models.Loan(member_id=david.id, book_id=bcosmos.id, loan_date=date(2024,4,1), due_date=date(2024,4,15), return_date=date(2024,4,12)),
        models.Loan(member_id=eva.id, book_id=boutliers.id, loan_date=date(2024,4,10), due_date=date(2024,4,25), return_date=date(2024,4,22)),
        models.Loan(member_id=grace.id, book_id=birobot.id, loan_date=date(2024,5,1), due_date=date(2024,5,15), return_date=date(2024,5,13)),
        models.Loan(member_id=henry.id, book_id=bhobbit.id, loan_date=date(2024,5,10), due_date=date(2024,5,25), return_date=date(2024,5,23)),
        models.Loan(member_id=isla.id, book_id=bthinking.id, loan_date=date(2024,6,1), due_date=date(2024,6,15), return_date=date(2024,6,14)),
        models.Loan(member_id=jack.id, book_id=bpaledot.id, loan_date=date(2024,6,10), due_date=date(2024,6,25), return_date=date(2024,6,23)),

        # Active loans (return_date = None)
        models.Loan(member_id=alice.id, book_id=bhomodeus.id, loan_date=today - timedelta(days=5), due_date=today + timedelta(days=9), return_date=None),
        models.Loan(member_id=bob.id, book_id=bbriefhistory.id, loan_date=today - timedelta(days=3), due_date=today + timedelta(days=11), return_date=None),
        models.Loan(member_id=carol.id, book_id=b1984.id, loan_date=today - timedelta(days=7), due_date=today + timedelta(days=7), return_date=None),
        models.Loan(member_id=david.id, book_id=bdune.id, loan_date=today - timedelta(days=2), due_date=today + timedelta(days=12), return_date=None),
        models.Loan(member_id=grace.id, book_id=bsapiens.id, loan_date=today - timedelta(days=4), due_date=today + timedelta(days=10), return_date=None),
        models.Loan(member_id=henry.id, book_id=bnexus.id, loan_date=today - timedelta(days=1), due_date=today + timedelta(days=13), return_date=None),

        # Overdue loans (due_date in past, return_date = None)
        models.Loan(member_id=isla.id, book_id=borigins.id, loan_date=today - timedelta(days=30), due_date=today - timedelta(days=16), return_date=None),
        models.Loan(member_id=jack.id, book_id=bgrand.id, loan_date=today - timedelta(days=25), due_date=today - timedelta(days=11), return_date=None),
        models.Loan(member_id=alice.id, book_id=btipping.id, loan_date=today - timedelta(days=20), due_date=today - timedelta(days=6), return_date=None),
        models.Loan(member_id=bob.id, book_id=bsilmarillion.id, loan_date=today - timedelta(days=35), due_date=today - timedelta(days=21), return_date=None),
        models.Loan(member_id=carol.id, book_id=blotr.id, loan_date=today - timedelta(days=28), due_date=today - timedelta(days=14), return_date=None),
        models.Loan(member_id=david.id, book_id=banimal.id, loan_date=today - timedelta(days=22), due_date=today - timedelta(days=8), return_date=None),

        # More returned loans to reach 30+
        models.Loan(member_id=eva.id, book_id=bfoundation.id, loan_date=date(2024,7,1), due_date=date(2024,7,15), return_date=date(2024,7,13)),
        models.Loan(member_id=frank.id, book_id=bcosmos.id, loan_date=date(2024,7,5), due_date=date(2024,7,20), return_date=date(2024,7,18)),
        models.Loan(member_id=grace.id, book_id=bthinking.id, loan_date=date(2024,8,1), due_date=date(2024,8,15), return_date=date(2024,8,14)),
        models.Loan(member_id=henry.id, book_id=birobot.id, loan_date=date(2024,8,10), due_date=date(2024,8,25), return_date=date(2024,8,23)),
        models.Loan(member_id=isla.id, book_id=boutliers.id, loan_date=date(2024,9,1), due_date=date(2024,9,15), return_date=date(2024,9,14)),
        models.Loan(member_id=jack.id, book_id=bbrave.id, loan_date=date(2024,9,10), due_date=date(2024,9,25), return_date=date(2024,9,23)),
        models.Loan(member_id=alice.id, book_id=bpaledot.id, loan_date=date(2024,10,1), due_date=date(2024,10,15), return_date=date(2024,10,13)),
    ]
    db.add_all(loans)
    db.commit()

    print(f"✅ Seeded {len(categories)} categories")
    print(f"✅ Seeded {len(authors)} authors")
    print(f"✅ Seeded {len(books)} books")
    print(f"✅ Seeded {len(members)} members")
    print(f"✅ Seeded {len(loans)} loans")
    db.close()

if __name__ == "__main__":
    seed()