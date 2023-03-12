<!-- PROJECT LOGO -->
<br />
<div align="center">

  <h3 align="center">websites_info_scraper</h3>

  <p align="center">
    Collects information specific to website URLs.
    <br/>
    <a href="https://github.com/thiagosilva977/webscraping-docker-template/issues">Report Bug</a>
    ·
    <a href="https://github.com/thiagosilva977/webscraping-docker-template/pulls">Request Feature</a>
  </p>
</div>


## Project Description

Application that, given a list of website URLs as input, visits them
and finds, extracts and outputs the website's url, logo url, icon url and all phone numbers present on the websites.

## Getting Started
Arguments
- **--url** - Single URL or list of urls (separated by comma "," or just a string list "["item1","item2"]")
- **--output-path** - Local path to save the output files

If you didn't pass any argument, the program will use the testing parameters.

### Running local
``` websites_scraper/main.py --arguments``` 

### Docker
#### Pull Image
`docker pull thiago977/websites_info_scraper:latest`
#### Run
```docker run thiago977/websites_info_scraper:latest scrape-url --arguments```

Example: 
```docker run thiago977/websites_info_scraper:latest scrape-url --url="https://www.zendesk.com.br/blog/contact-us-page/,https://quataalimentos.com.br/fale-conosco/,https://www.estadao.com.br/fale-conosco" --output-path="/home"```

#### Create parameters
I just added an option to search on google and get some urls to use as input. 
```docker run thiago977/websites_info_scraper:latest create-parameters```

## Results
- [Example of collected data](https://github.com/thiagosilva977/websites_info_scraper/blob/fb23caf20c8285a4dd8e71dcaf2716fe7bc49616/assets/first_results.json)

## Annotations
### Next improvements
- Better precision on parsing phone numbers
- More input parameters to customize the configs
- Better documentation
### Time report
![image](https://user-images.githubusercontent.com/11250089/224531255-6ff82cef-acd1-4170-8e92-b2aa0ff5ef8f.png)


