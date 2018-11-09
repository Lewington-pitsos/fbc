import sys
import time
import random
from likers import steps
from likers import save
from lep.selenium import setup
from facebook import db

database = db.db()
suppliers = database.get_suppliers()

driver = setup.moz()

user_email = "idof@live.com.au"
user_password = "q1as1z2qwe2"
steps.login(driver, user_email, user_password)

for supplier in suppliers:
    supplier_id, page_name, page_id = supplier

    if supplier_id not in [2]:

        likers_url = "https://m.facebook.com/search/{}/likers".format(page_id)

        driver.get(likers_url)

        database = db.db()
        supplier_id = database.save_supplier(page_name, page_id)

        while True:
            try:
                likers = steps.get_likers(driver)
                for liker in likers:
                    database.save_like(liker, supplier_id)
            except Exception as e:
                print(e)
                database.rollback()
                continue
                
            warning = steps.get_facebook_warning(driver)
            if warning:
                print("Looks like they're onto us. Time to stop.")
                break

            success = steps.get_next_likers(driver)
            if not success:
                print("looks like we reached the end")
                break

            time.sleep(1)

        print("Finished with: {}".format(page_name))
