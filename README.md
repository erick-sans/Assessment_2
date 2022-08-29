# Holiday Manager Assessment

This repository contains Python code for initiating and maintaining a dynamic holidays list. 

Features include:
    
    1. Reading starter holidays from a json file and creating holiday object instances from those holidays.

    2. Scraping a website for all holidays and associated dates between 2020 and 2024 to add to the holiday list object

    3. Interactive menu to add and remove holidays from the holiday list object

    4. A choice to export the holiday list object out as a json file

    5. Awareness of save-state changes so work isn't lost

# How to Use:

Ensure that the starter holidays.json file is in the same directory as the holiday manager. An api key for the Visual Crossing Timeline Weather API must be provided in config.py to successfully scrape weather information. 

The plans folder contains a brainstormed napkin drawing of the program's flow.