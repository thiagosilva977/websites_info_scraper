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

### Running local
``` websites_scraper/main.py --arguments``` 

### Docker
#### Pull Image
`docker pull thiago977/websites_info_scraper:latest`
#### Run
`docker run thiago977/websites_info_scraper:latest scrape-url --arguments`

Example: 
```docker run thiago977/websites_info_scraper:latest scrape-url --url="https://www.zendesk.com.br/blog/contact-us-page/,https://quataalimentos.com.br/fale-conosco/,https://www.estadao.com.br/fale-conosco" --output-path="/home"```




