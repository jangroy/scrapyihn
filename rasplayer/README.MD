Rasplayer scraper
=================

[TOC]

# Rationale
This project is based on the open source project [Scrapy](https://docs.scrapy.org)
There is only one Scrapy project called Rasplayer. Under this project there will be multiple spiders.
This project is meant to be used in conjunction with Rasplayer Frames Controllers, and with the **spider-frames-controller** project

# Scraper server
The server needs to run Splash, Scrapyd, and spider-frames-controller

## Splash
Run ```./run-splash.sh``` (needs Docker)

## Scrapyd
Run ```scrapyd``` (see [Scrapyd](https://scrapyd.readthedocs.io/en/stable/)

## Spider-frames-controller
Run ```[path-to-spider-frames-controller]/scheduler-index.js```

# Scraping
In order to use this scraper with Rasplayer, the following steps must be followed:

1. [Create a spider](#create-a-spider)
2. [Test the spider](#test-the-spider)
3. [Deploy the spider](#deploy-the-spider)
2. [Create a frames controller](#create-a-frames-controller). Set it as inactive
3. [Set spider id on frame controller](#set-spider-id-on-frame-controller)
4. Set the frames controller as active
5. [Add the spider to DB](#add-the-spider-to-db)

It is recommended to install the extension [selector gadget](http://selectorgadget.com/)
on the browser

## Create a spider
[see docs](https://doc.scrapy.org/en/1.2/topics/spiders.html)

In order to create a spider, a new file has to be added to *rasplayer/spiders*
The file name should be the same as the spider, with low dashes instead of normal dashes.
You can create a spider on your own but it is **strongly recommended** that a template is used instead

### Two templates to scrape the web
The recommended way to create a spider is to copy a template file and paste it into *rasplayer/spiders* with the new spider name.
There are two templates that should suffice for most of the situations
All the templates support the following attributes:

###### name (required)
: A string indicating spider name. Same as the file but replacing *-* with *_*.
  So for a spider's file my_spider.py, the name should be *my-spider*
  Also referred as spider id

###### allowed_domains (required)
: An array with the domains the spider is allowed to follow. It will never scrape contents out of the indicated domains

###### start_urls (required)
: An array with the urls to scrape.

###### items_selector (required)
A selector that matches a collection of items on the index page.

**String** A css selector, ie: ```'tr.yvr-flights__row:not(.yvr-flights__row--hidden):not(.yvr-flights__row--button)'```

**Function:** Gets as an argument a response.
 All the [Selectors](https://doc.scrapy.org/en/1.2/topics/selectors.html) can be used with the response:

- response.css(css-string)
- response.xpath(xpath-string)
- response.css(css-string).xpath(xpath-string)

###### loader
A custom [Item Loader](https://doc.scrapy.org/en/1.2/topics/loaders.html#declaring-item-loaders)
If no loader is provided, a default loader is used:

```python
class DefaultLoader(ItemLoader):
    default_input_processor = MapCompose(remove_tags, unicode.strip)
    default_output_processor = TakeFirst()

    image_urls_out = MapCompose(get_full_url)
    file_urls_out = MapCompose(get_full_url)
    # image_urls_out = Identity()
```
On the default loader, the default output processor for every item is to return the first one.
If multiple values are desired for one attribute, the output processor must be overriden.

If a loader is provided, it is recommended that it inherits from the DefaultLoader:

```python
from defaults import DefaultLoader

class MyLoader(DefaultLoader)
    timestamp_in = MapCompose(remove_tags, unicode.strip, str_date_to_str)
```

###### next_page_url_selector
A selector that matches the next page url selector.
If multiple items are selected, it takes the first one.

Same format as [items_selector](#items_selector-required),
but it has to select the attribute that contains the url. ie: ```.page-arrow.page-next .page-arrow-link::attr(href)```


###### pages_limit
Maximum limit number of total pages to be scraped

###### items_per_page_limit
Maximum limit number of items that should be extracted per page.
**Note**: If you only scrape one page, use this instead of *items_limit*

###### items_limit
Maximum number of total items to be scraped.

It is recommended NOT TO USE IT, and use *items_per_page_limit* instead.
The reason is that it creates VERY VERBOSE LOGS.
Also, the items are extracted, and then dropped.

###### partition_size
Used when 1 media should receive multiple items

It defaults to 1 if not given, and each item will be found under *item* on the *EJS* template.

If given, and more than 1, each item will be found under *items* on the EJS template,
and it will contain *partition_size* number of sub-items


#### index template
Use this template when you want to scrape information from a list of items,
and all the information needed for each item is on that list

###### attrs
A dictionary of attributes. The key will be the item attribute name,
and the value can be either a string (a css selector), or a function that gets
as an argument an [item loader](https://doc.scrapy.org/en/1.2/topics/loaders.html) object.
Item loaders have the functions:

- add_css(attr-name, css-selector-string)
- add_xpath(attr-name, xpath-selector-string)
- add_value(attr-name, value-string/number)
- nested_css(css-selector-string)
- nested_xpath(xpath-selector-string)

An attribute function can call a bunch of values to the attribute by calling multiple times loader functions

##### index-item example
Use this template when you want to scrape information from a list of items,
but in order to retrieve all the information for each item, a link to a new page for each item
hast to be followed.

###### item_url_selector
Selects the url to follow for each item.
Is relative to the item found using [items_selector](#items_selector-required),
and uses the same format (a css selector or a function). ie: ```'a.url::attr(href)'```

###### index_attrs
Selects the attributes for the item on the index page.
Results will be merged with [item_attrs](#item_attrs) for each item.

Same format as [attrs](#attrs)

###### item_attrs
Selects the attributes for the item on the item page.
Results will be merged with [index_attrs](#index_attrs) for each item

Same format as [attrs](#attrs)

## Test the spider
Once you created the spider, you can test it running the command
```
$ ./test-spider.sh
```
It will run the spider without running the frames controller, and will output the retrieved
items into *jsons/[spider-name].json*

You must then check logs for errors, and make sure that the retrieved items are as expected
(the items in the JSON are not partitioned yet, and not processed by scripts tho)

## Deploy the spider
To deploy the spider into the **Scrapy server**, run the command
```
$ ./deploy.sh
```
from the project folder. (Scraper server must be running scrapyd)

Every time a change is made on the spider, it needs to be re-deployed again.

## Create a frames controller
Create the frames controller using the legacy API.
Set it as inactive so main frames controller process don't process it.

## Set spider id on frame controller (manually only for now)
Add a spiderId into the frame controller on DB.

To figure out the frame controller id on DB:

1. go to *firebase/clients/[client-id]/framesControllers*
2. Open another browser window with *firebase/framesControllers*
3. Look at all the frames controllers in (1) on the list on (2) and looking at the name attribute

## Add the spider to db
Add an object in *firebase/spiders/spider-name* like

```javascript
{active: true, interval: 5}
```

The interval is given in minutes.

# Processing the items with scripts
If there is any operation that must be performed with the whole collection of items (like sorting),
or you want to modify the items in a more flexible way using javascript instead, you can add a script
to the frame controller.

## Create the script
Create a script in the folder *scripts*. You can give it any name, but it is recommended that the name contains
the name of the spider: for a spider called *yvr-arrivals*, a good name would be *yvr-arrivals-sort-asc.js*, for example.

The script must contain one function called run that gets one argument, items, and returns them processed.
```javascript
function run(items) {
    return _.sortBy(items, ['timestamp']);
}
module.exports = {
    run: run
};
```
## Add the script to the frames controller
Go to *firebase/clients/[clientId]/framesControllers/frameControllerId and add an attribute
**script** with the name of the script as a value (without the .js extension). ie: *yvr-arrivals-sort-asc*