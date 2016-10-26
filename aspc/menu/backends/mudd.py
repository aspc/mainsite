from selenium import webdriver

class MuddBackend(object):
    def __init__(self):
        self.selenium = webdriver.PhantomJS()
        self.homepage_url = "https://hmc.sodexomyway.com/dining-choices/index.html"
        self.menus = {
            'Monday': {}, # Each day dict contains key value pairs as meal_name, [fooditems]
            'Tuesday': {},
            'Wednesday': {},
            'Thursday': {},
            'Friday': {},
            'Saturday': {},
            'Sunday': {}
        }
        try:
            self.menu_url = self.get_menu_url()
        except:
            self.link_unavailable()
            return
    
    def get_menu_url(self):
        self.selenium.get(self.homepage_url)
        link_container = self.selenium.find_element_by_class_name("accordionBody")
        link = link_container.find_element_by_tag_name("a")
        return link.get_attribute("href")        
    
    def link_unavailable(self):
        print "Error: Menu link currently unavailable from website"
    
    def get_hours(self):
        """
        returns hours of operation
        """
        self.selenium.get(self.homepage_url)
        hours_element = self.selenium.find_element_by_id("ui-accordion-accordion_3543-panel-1")
        return hours_element.get_attribute("innerText")
    
    def get_day_menu(self):
        """
        fetches menu data for a specific day in a returned dict of
        format meal_name: [fooditems]
        """
        #Breakfast,Lunch,Dinner on wkdays, Lunch,Dinner on wknds
        mealname_list = []
        mealname_data = self.selenium.find_elements_by_tag_name("h2")
        for meal in mealname_data:
            mealname_list.append(meal.get_attribute("innerText").lower())
        
        full_day_menu = {} #menu data with all meals and food items for specific day
        mealtable_data = self.selenium.find_elements_by_tag_name("table")
        index = 0 #use to match mealtable to the above mealname list
        for mealtable in mealtable_data:
            meal_menu = [] #[fooditems] for the specific meal
            menu_data = mealtable.find_elements_by_tag_name("tr")
            for row_item in menu_data:
                #This extracts categories, uncomment if desired
                """
                if food_item.get_attribute("class") == "category":
                    print food_item.get_attribute("innerText")
                """
                #extract only food names to add to menu list
                food_type = row_item.get_attribute("class")
                if "product" in food_type:
                    food_item = row_item.find_element_by_tag_name("td").get_attribute("innerText")
                    #uncomment if this is a desired feature...
                    """
                    #add vegetarian, vegan, mindful tags if applicable
                    tags = " ("
                    if "vegetarian" in food_type:
                        tags += "V,"
                    if "vegan" in food_type:
                        tags += "VG,"
                    if "mindful" in food_type:
                        tags += "M,"
                    if tags != " (":
                        tags = tags[:-1] +")" #remove extra comma and add )
                        food_item += tags
                    """
                    meal_menu.append(food_item)
            full_day_menu[mealname_list[index]] = meal_menu
            index += 1
        return full_day_menu
    
    def update_progress(self,day_name):
        print "Scraped Mudd-" + day_name
        
    def print_timeout_error(self):
        print "Error: Mudd's website likely timed out or sent a bad response. Returning days that were successfully scraped."
        
    def menu(self):
        """
        Returns menu for this week
        """
        try:
            self.selenium.get(self.menu_url)
        except:
            self.print_timeout_error()
            return self.menus
        
        #toggle through each day's button and scrape the updated menu.
        #skip if button not found (in case of shorter week)
        for i in range(7):
            try:
                all_buttons = self.selenium.find_elements_by_xpath('//a[@href="javascript:void(0)"]')
                for button in all_buttons:
                    menu_button = button.get_attribute("onclick")
                    if menu_button == "changeTab(%d)"%(i):
                        day_name = button.get_attribute("innerHTML")
                        button.click()
                        self.menus[day_name] = self.get_day_menu()
                        self.update_progress(day_name)
                        break
            except:
                self.print_timeout_error()
                return self.menus
        return self.menus    