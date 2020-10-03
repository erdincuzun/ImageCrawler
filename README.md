# ImageCrawler
This crawler downloads the images and extracts features from these images for use in machine learning. This project is derived from the <a href="https://github.com/erdincuzun/REGEXN" target="_blank">REGEXN project</a>.

# Usage
It is enough to prepare the rule file and say hello crawler:)

##Rule File
Simply enter the following information in the Rule file. You can use CSS selectors for HTML element selection. Let's start:
```json
{
   "project_name": "EnterYourProjectName",
   "web_site": "https://urlofWebsite/",
   "seeds": [
	  "seeds1",
	  "seeds2"
   ],
   "type": "selenium:lxml", #parser configuration
   "wait": 1, #wait seconds between two page
   "browser": "chrome", #your browser
   "driver": "drivers/chromium/chromedriver.exe", #your driver, you can use different drivers
   "result_file": "output.text", #for text extraction
   "sitemap": [
      {
         "page": "Mainpage", #means link page
         "detection": {
            "url": "unique values from web site to solve main page" 
         },
         "data_extraction": [{ #get data
               "parent_layout": "*", #seacrh all pages
               "extraction_rules": [
                  {
                     "name": "Image",
                     "selector": "img" #get all images - CSS selector
                  }
               ]
            }],
         "link_extraction": [ # get link
			     {
               "parent_layout": "header h1", #get header h1 - CSS selector (you can determine your layout, or layouts for extraction)
               "selector": "a" #get hrefs - CSS selector
            }
         ]
      },
      {
         "page": "Datapage", #sub web pages
         "detection": {
            "url": "noticia/" #url contains
         },
         "data_extraction": [
            {
               "parent_layout": "*", #all web page
               "extraction_rules": [
                  {
                     "name": "Image",
                     "selector": "img" # img extraction
                  }
               ]
            }
         ],
         "link_extraction": [] #no get hrefs
      }
   ]
}
```
An example:
```json
{
   "project_name": "20minutos",
   "web_site": "https://www.20minutos.es/",
   "seeds": [
	  "https://www.20minutos.es/nacional/7/",
	  "https://www.20minutos.es/nacional/6/",
	  "https://www.20minutos.es/nacional/5/",
	  "https://www.20minutos.es/nacional/4/",
	  "https://www.20minutos.es/nacional/3/",
	  "https://www.20minutos.es/nacional/2/"
   ],
   "type": "selenium:lxml",
   "wait": 1,
   "browser": "chrome",
   "driver": "drivers/chromium/chromedriver.exe",
   "result_file": "output.text",
   "sitemap": [
      {
         "page": "Mainpage",
         "detection": {
            "url": "nacional/"
         },
         "data_extraction": [{
               "parent_layout": "*",
               "extraction_rules": [
                  {
                     "name": "Image",
                     "selector": "img"
                  }
               ]
            }],
         "link_extraction": [
			{
               "parent_layout": "header h1",
               "selector": "a"
            }
         ]
      },
      {
         "page": "Datapage",
         "detection": {
            "url": "noticia/"
         },
         "data_extraction": [
            {
               "parent_layout": "*",
               "extraction_rules": [
                  {
                     "name": "Image",
                     "selector": "img"
                  }
               ]
            }
         ],
         "link_extraction": []
      }
   ]
}
```
This file needs to be adjusted according to the website. You may not want unnecessary links and sections by using the CSS selector here. Let's start the crawler now.



