from bs4 import BeautifulSoup as bs

def get_product_params(html, url : str) -> dict:
    soup = bs(html, "html.parser")
    
    params = {
        "name" : "",
        "brend" : "",
        "url" : "",
        "photo-urls" : "",
        "description" : "" 
    }
    
    #name
    try:
        name = soup.find("h1").getText()
        params["name"] = name
    except Exception as err:
        print(err)
    
    #brend
    try:
        spec_panel = soup.find("div", attrs={"data-widget" : "webCharacteristics"} )
        specs = spec_panel.find_all("dl")
        for spec in specs:
            if spec.find("span").getText() == "Бренд":
                params["brend"] = spec.find("a").getText()
            
    except Exception as err:
        print(err)
    
    #photos
    try:

        photos = []
        gallery = soup.find("div", attrs= {"data-widget" : "webGallery"}).find_all("img")
        for image in gallery:
            link = image.get("src")
            photos.append(link.replace("/wc50/", "/wc700/"))
        params["photo-urls"] = ", ".join(photos) 
 
    except Exception as err:
        print(err)
    
    #description 
    try:
        description_panels = soup.find_all("div", id = "section-description")
        text_array = []
        
        for panel in description_panels:
            tags = []
            tags += panel.find_all("div")
            tags += panel.find_all("p")
            for tag in tags :
                
                try:
                    tag_text = tag.get_text()
                    
                    if tag_text is not None and tag_text != "":
                        if tag_text not in text_array:
                            text_array.append(tag_text)
                except:
                    continue
                
                    
            # p_tags= panel.find_all("p")
            # for tag in p_tags:
            #     if tag.getText() != "" and tag.getText() != None:
            #         text += tag.getText()
            #         text += "; "
            
        params["description"] = "; ".join(text_array)
            
    except Exception as err: 
        print(err)
        
    params["url"] = url
    return params
        
   