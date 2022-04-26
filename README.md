TelloBeep
===============

Python bot for instagram spotted automation.

![Bez nazwy](https://user-images.githubusercontent.com/64653975/165394379-fb71a55f-35df-40e4-bd22-47498c765fd0.png)



screenshot of [onefetch tool](https://github.com/o2sh/onefetch)
# What is it?
TelloBeep is python bot which scrapes [tellonym] (https://tellonym.me) webpage, creates image and publishes it on instagram. Also notifications are send on discord channel. All data is stored in sqlite. Bot has built in censorship which helps in keeping page "clean". Up to now you can manage bot with http page made in flask.

# Why?
We have created this bot because most of our school's spotteds died out because admins laziniess. Due lack of time, bot helps to create community with as small amount of time as it is possible. 

# How to run it
```bash
#download repo and requirements
git clone https://github.com/gl00man/TelloBeep
pip3 install -r requirements.txt

#customization
*customize config.json*
*customize swears_list.txt*
pyton3 init.py -l <admin username> -p <admin password>

#and run bot
python3 run.py
```

# Customization
json file explained
```bash

{
    "AUTORUN" = use protection against spamming,
    "BAD_WORDS" = file location of censorship key file,
    "LOG_FILE" = file location of log file,
    "CAPTION" = post content on instagram,
    "LOGIN_TELLONYM" = tellonym login,
    "PASSWORD_TELLONYM": tellonym password,
    "LOGIN_INSTAGRAM": instagram login,
    "PASSWORD_INSTAGRAM": instagram password,
    "TEXT_footer": footer added to the generated post,
    "TIMEZONE": timezone add/substract hours,
    "colorBackground": list of colors in hex (e.g. ["#fafafa", "2a4a6a"]),
    "colorText": font color,
    "extension": generated image extension,
    "font_footer_name": file/name of font in footer,
    "font_footer_size": font size of footer,
    "footer_position_ratio": footer position ration ,
    "fontname": file/name of font in text main text,
    "fontsize": fontsize of content,
    "footer_height": height of footer,
    "header_position_ratio": footer position ratio,
    "header_font_size": fontsize of header,
    "POST_RATIO_WARNING": send warning when count of posts is equal,
    "POST_RATIO_ALERT": stop sending posts on instagram when ratio is higher or equal,
    "image_path": logo path/name
    "image_size": [
        height of logo,
        width of logo
    ],
    "logo_X_ratio":location of logo on image,
    "logo_Y_ratio":location of logo on image,
    "insta_res": [
        output immage height,
        output immage width
    ],
    "margin": { = margins of image
        "top": ,
        "right": ,
        "bottom": ,
        "left": 
    },
    "out_image_path": path to direcotry where to save images,
    "out_image_path_BACKUP": if first direcotry not found, try to save here,
    "outline_thickness": outline thickness of image(default 0),
    "swears_list": add list of badwords,
    "thumb_path": path where to save thumbnails ,
    "thumb_res": [ thumbnails resolution
        height,
        width
    ],
    "token_file": token file path,
    "word_break": count of words per line,
    "DISCORD_CHANNEL_ID": id of channel where to send notifications,
    "DISCORD_TOKEN":discord bot token
}

```


# Autorhs
[RandomGuy90](https://github.com/RandomGuy090)

    discord: RandomGuy90#5264
    
[glooman](https://github.com/gl00man/)

# Contributions
Have you found a bug, or just want to improve my retarded code?

Feel free to use and edit this bot. You can easily create pull requests and open new issues. We really encorauge you to contact and develop this repo with us!

# How does it look like?
some of automatically created images:

![image](https://user-images.githubusercontent.com/64653975/165390756-22642e81-5cf8-4477-8057-f39f08fb7734.png)

![image](https://user-images.githubusercontent.com/64653975/165390826-d0dbaaaa-1769-4174-abbe-5d1710377732.png)

![20220210170342_4907981514](https://user-images.githubusercontent.com/64653975/165390900-4e8257e3-f78c-4ba8-852d-01aeb2ae3588.jpg)

![20220426215730_5290619073](https://user-images.githubusercontent.com/64653975/165391151-bc36e0b0-9167-46a0-b980-a6c1fc5c3c52.jpg)

![image](https://user-images.githubusercontent.com/64653975/165391344-c4f4059d-3c04-4b48-9554-c2073df9c9e5.png)

automated blocade caused by too many posts

![image](https://user-images.githubusercontent.com/64653975/165391459-a82c0a4a-1d20-4448-b37a-8f131e2c5860.png)

discord notifications
![image](https://user-images.githubusercontent.com/64653975/165391622-84b938ed-18c3-4edc-9889-372d78f71044.png)

logs:
![image](https://user-images.githubusercontent.com/64653975/165391819-a386f43e-a9bd-4dbe-b528-9bb39a46ec80.png)

admin pannel:
![image](https://user-images.githubusercontent.com/64653975/165392505-b93040a5-b288-4207-a4d8-1331e31b33c2.png)

![[Pasted image 20220426231043.png]]


