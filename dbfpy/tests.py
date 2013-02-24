# -*- encoding: utf-8 -*-

import sys
import datetime
import unittest

sys.path.append('.')

from dbfpy import dbf


class TestBasic(unittest.TestCase):

    def test(self):
        test_filename = "test.dbf"

        db = dbf.Dbf(test_filename, new=True)
        rec_fields = ['NAME', 'SURNAME', 'INITIALS', 'BIRTHDATE']
        db.addField(
            ("NAME", "C", 15),
            ("SURNAME", "C", 25),
            ("INITIALS", "C", 10),
            ("BIRTHDATE", "D"),
        )

        ## fill DBF with some records

        expected_data = [
            ("John", "Miller", "JM", 
                (1980, 1, 2), datetime.date(1980, 1, 2)),
            ("Andy", "Larkin", "AL", 
                datetime.date(1981, 2, 3), datetime.date(1981, 2, 3)),
            ("Bill", "Clinth", "", 
                datetime.date(1982, 3, 4), datetime.date(1982, 3, 4)),
            ("Bobb", "McNail", "", 
                "19830405", datetime.date(1983, 4, 5)),
        ]

        for name, surname, initials, birthdate, _ in expected_data:
            rec = db.newRecord()
            rec["NAME"] = name
            rec["SURNAME"] = surname
            rec["INITIALS"] = initials
            rec["BIRTHDATE"] = birthdate
            rec.store()
        db.close()

        ## read DBF and print records

        db = dbf.Dbf(test_filename)
        data = list(db)
        
        self.assertEqual(len(data), len(expected_data))

        for exp_rec, _rec in zip(expected_data, data):
            exp_rec = exp_rec[:-2] + exp_rec[-1:]
            rec = tuple(_rec[f] for f in rec_fields)
            self.assertEqual(exp_rec, rec)

        ## change record

        rec = db[2]
        rec["INITIALS"] = "BC"
        rec.store()
        #del rec

        # TODO


if __name__ == '__main__':
    unittest.main()



