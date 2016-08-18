# FatHen.co
Visit Fat Hen on [fathen.co](http://www.fathen.co/)

Fat Hen is a project by Davis Crain as his final project for The Iron Yard Backend Engineering class in Greenville, SC.

You can learn more about Davis at [dhcrain.com](https://dhcrain.com/).

#### Feature Set:
__Non Logged in users can__
- Search for farmers market
- See what vendors are at each farmers market
- See the 7 day forecast for farmers markets locations
- Read reviews and status updates
- Contact me to claim listings or for any reason.

__Logged In users can (all the above plus….)__
- Review a farmers market - Comment and rate 1 to 5
- Review a vendor - comment and rate 1 to 5
- Favorite a farmers market
- Favorite a vendor
- Add vendors and farmers markets
- Profile page with:
    - List of favorite farmers markets
    - List of favorite vendors
    - Culminated status statuses of vendors and farmers markets, chronologically.

__Farmers Market Owners can:__
- Update status with picture
- Claim if they will have the market this week
- Update information
- Update pictures
- Add vendors

__Vendor Owners can:__
- Update status with picture
- Claim if they will be present at the market
- Update information
- Update pictures
- All farmers markets in South Carolina from [South Carolina Dept. of Agriculture](South Carolina Dept. of Agriculture)
- Vendors at [TD Saturday Market](http://www.saturdaymarketlive.com/) & [Travelers Rest Farmers Market](http://travelersrestfarmersmarket.com/) from their websites.


#### Technology Used:
- Django 1.9.7
- Python 3.5.1
- Django REST API framework 3.4.1
- Heroku
- PostgreSQL
- AWS S3 - Static assets and media uploads
- [Django-review](https://github.com/bitmazk/django-review) for the reviews and averaging of scores. _(I would not use this next time, it can make it challenging to work with the data.)_
- [forecast.io API](https://developer.forecast.io/) - for 7 day forecast at farmers market locations
- Google Maps API embed
- Foundation CSS framework
- FontAwesome

#### Long Term Wish List:
- Mobile! responsive web site and/or App
- Weekly email of status updates to users of favorites
- Link to social media for vendors to be able to dual post
- Send a text to vendors to check in for the week
- Search for a farmers market by Zip code radius
- Display all farmers markets on a map
- Expand to other states, NC first
- OAuth - Sign in with Google, Facebook, and Twitter
