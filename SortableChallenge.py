#! /usr/bin/env python
#######################################################################################################################
# SortableChallenge.py
# June 10, 2016 - Danilo Fiorenzano
#
# This code addresses the programming challenge issued by Sortable (http://sortable.com/challenge/). It can be run
# under either Python 2.x or 3.x. It assumes availability of the files "listings.txt" and "products.txt" in the same
# location it runs from.
#
# Description of chosen algorithm:
# Product and listing files are read into memory and allocated into lists of standard Python dictionaries, using
# the standard json module. The resulting lists are then sorted by manufacturer + product name and processed ("merged")
# together as follows.
#
# The lists are scanned linearly "side by side" keeping two numeric indexes into them, initialized to point at
# the beginning of each list. For each product, we scan the listings until matching the product manufacturer,
# and then looking for a match on product name. For each positive match, we store the relevant data in a result
# list for later output at exit.
#
# The algorithm relies on the sorting steps executed earlier to recognize when it is time to move to the next product,
# while preserving the current position in the listings table. It ends once we have exhausted the list of products, or
# we run out of product listings to examine. Execution time grows linearly in O(n) fashion where n is the number of
# product listings.
#
# Matches are detected using a simple substring search. This appears to yield rather accurate results given the nature
# of the data being processed and the preparatory sorting steps ("Canon" will match "Canon Canada", "Agfa" will match
# "AgfaPhoto" etc), but may fail to recognize product matches where their names are formulated with missing spaces or
# other separators ("110 IS" won't match "110IS").  Further improvements to this logic should be feasible.
#######################################################################################################################

import json

decoder = json.JSONDecoder()
encoder = json.JSONEncoder()

# Read/decode products file and sort the resulting dict by manufacturer + product name (lowercase).
# We replace underscores with spaces in the product name to more conveniently match it later in product listings.
products = []
with open("products.txt") as p:
    for line in p:
        product = decoder.decode(line)
        product["product_name"] = product["product_name"].replace("_", " ")
        products.append(product)
products.sort(key=lambda p: (p["manufacturer"] + "||" + p["product_name"]).lower())

# Read/decode listings and sort them the same way. No special character substitution is performed.
listings = []
with open("listings.txt") as l:
    for line in l:
        listing = decoder.decode(line)
        listings.append(listing)
listings.sort(key=lambda l: (l["manufacturer"] + "||" + l["title"]).lower())

output = []
px = lx = 0
try:
    for px in range(len(products)):
        p = products[px]
        p_listings = []
        brand = p["manufacturer"].lower()
        name = p["product_name"].lower()

        # Find where listings for this brand begin
        while listings[lx]["manufacturer"].lower() < brand:
            lx += 1

        if brand in listings[lx]["manufacturer"].lower():
            # found a matching brand, now scan listings for it looking for our product
            while brand in listings[lx]["manufacturer"].lower() and listings[lx]["title"].lower() < name:
                lx += 1

            # fetch all following listings for this product
            while name in listings[lx]["title"].lower():
                p_listings.append(listings[lx])
                lx += 1

            # save what we found, if anything at all
            if p_listings:
                output_entry = {"product_name": p["product_name"].replace(' ', '_'), "listings": p_listings}
                output.append(output_entry)
except IndexError:
    # just in case we increment lx past the last listing (won't happen with the distributed data files)
    pass
finally:
    with open("output.txt", "w") as o:
        for output_entry in output:
            line = encoder.encode(output_entry)
            o.write(line + "\n")
        print("Done, matches written to output.txt.")

# EOF
