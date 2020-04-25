
"""Utility file to seed data to database from seed_data"""

from model import connect_to_db, db, Weekly_Rec
from server import app


def load_weekly_recs(weekly_recs_filename):
    """Load weekly recs from u.recs into database."""

    print("Weekly Recs")

    Weekly_Rec.query.delete()

    # Read u.activity file and insert data
    for row in open(weekly_recs_filename):
        row = row.rstrip()
        print(row)
        id, message = row.split("|")

        weekly_rec = Weekly_Rec(id=id,
                                message=message)
        db.session.add(weekly_rec)

    db.session.commit()


#------------------------------------------------------------------------------#
if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    weekly_recs_filename = "RawData/u.recs"

    load_weekly_recs(weekly_recs_filename)
    
    print('All done!')
#------------------------------------------------------------------------------#