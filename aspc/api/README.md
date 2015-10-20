# ASPC API

A standardized way to access ASPC features. Currently there is only an API for the Menu. 
In order to use the API, you must first obtain an access token using your 5C CAS credentials.

## Example

### 1) Retrieve auth token

#### Request (application/json)

```
curl -d "username=admin&password=aspc" https://aspc.pomona.edu/api/auth/
```

Note this will leave your password in the command line history: delete the above line from your `~/.bash_history` to remove.

#### Response 200 (application/json)

```
{
    "token":"83056d12c23f007d1d2ad7d2713b776d4644c21c"
}
```

### 2) Access menu endpoint

#### Request (GET)

```
curl -H "Authorization: Token 83056d12c23f007d1d2ad7d2713b776d4644c21c" https://aspc.pomona.edu/api/menu/
```

#### Response 200 (application/json)

```
    [
        {
            "day": "fri",
            "dining_hall": "cmc",
            "food_items": "[\"Breakfast Selections\", \"Scrambled Eggs\\nCheese & Bacon Eggs\\nTurkey Bacon & Sausage Patties\\nChorizo & Cheese Quesadilla\", \"Oatmeal & Grits\\nWaffles\\nHash Browns \\nCranberry & Apple Cinnamon Muffins\", \"Make Your Own Waffle Station\"]",
            "id": 11,
            "meal": "breakfast"
        },
        {
            "day": "fri",
            "dining_hall": "cmc",
            "food_items": "[\"Chocolate Chip Cookies\\nCinnamon Roll Cheesecake Cookies\\nPina Colada Bar\\nLemon Blueberry Pound Cake\", \"Red Velvet Cake\\nVegan Banana Cream Pie\\nMade Without Gluten Rochers\"]",
            "id": 13,
            "meal": "dessert"
        }, ...
    ]
```

## Authorization [/api/auth/]

#### Request (application/json)
```
    {
        "username": "your_usernmae",
        "password": "your_password"
    }
```
    
#### Response 200 (application/json)
```
    {
        "token": "83456d12c23f007d1d2ad7d2713b776d4644c21c"
    }
```

## Menu

###  All Menus [/api/menu/]

Lists all menus

#### Request (GET)

    + Headers
        Authorization: Token 83456d12c23f007d1d2ad7d2713b776d4644c21c

#### Response 200 (application/json)

    [
        {
            "day": "fri",
            "dining_hall": "cmc",
            "food_items": "[\"Breakfast Selections\", \"Scrambled Eggs\\nCheese & Bacon Eggs\\nTurkey Bacon & Sausage Patties\\nChorizo & Cheese Quesadilla\", \"Oatmeal & Grits\\nWaffles\\nHash Browns \\nCranberry & Apple Cinnamon Muffins\", \"Make Your Own Waffle Station\"]",
            "id": 11,
            "meal": "breakfast"
        },
        {
            "day": "fri",
            "dining_hall": "cmc",
            "food_items": "[\"Chocolate Chip Cookies\\nCinnamon Roll Cheesecake Cookies\\nPina Colada Bar\\nLemon Blueberry Pound Cake\", \"Red Velvet Cake\\nVegan Banana Cream Pie\\nMade Without Gluten Rochers\"]",
            "id": 13,
            "meal": "dessert"
        }, ...
    ]

###  Menus By Dining Hall [/api/menu/dining_halls/{dining_hall}/]

Lists all menus by a specific dining hall

#### Parameters

+ dining_hall (enum[string])

    Name of the dining hall

    + Members
        + frary
        + frank
        + cmc
        + mudd
        + scripps
        + oldenborg

#### Request (GET)

    + Headers
        Authorization: Token 83456d12c23f007d1d2ad7d2713b776d4644c21c

#### Response 200 (application/json)

    [
        {
            "day": "fri",
            "dining_hall": "cmc",
            "food_items": "[\"Breakfast Selections\", \"Scrambled Eggs\\nCheese & Bacon Eggs\\nTurkey Bacon & Sausage Patties\\nChorizo & Cheese Quesadilla\", \"Oatmeal & Grits\\nWaffles\\nHash Browns \\nCranberry & Apple Cinnamon Muffins\", \"Make Your Own Waffle Station\"]",
            "id": 11,
            "meal": "breakfast"
        },
        {
            "day": "fri",
            "dining_hall": "cmc",
            "food_items": "[\"Chocolate Chip Cookies\\nCinnamon Roll Cheesecake Cookies\\nPina Colada Bar\\nLemon Blueberry Pound Cake\", \"Red Velvet Cake\\nVegan Banana Cream Pie\\nMade Without Gluten Rochers\"]",
            "id": 13,
            "meal": "dessert"
        }, ...
    ]

###  Menus By Day [/api/menu/day/{day}/]

Lists all menus by a specific day of the week

#### Parameters

+ day (enum[string])

    Name of the day of the week

    + Members
        + mon
        + tue
        + wed
        + thu
        + fri
        + sat
        + sun

#### Request (GET)

    + Headers
        Authorization: Token 83456d12c23f007d1d2ad7d2713b776d4644c21c

#### Response 200 (application/json)

    [
        {
            "day": "fri",
            "dining_hall": "cmc",
            "food_items": "[\"Breakfast Selections\", \"Scrambled Eggs\\nCheese & Bacon Eggs\\nTurkey Bacon & Sausage Patties\\nChorizo & Cheese Quesadilla\", \"Oatmeal & Grits\\nWaffles\\nHash Browns \\nCranberry & Apple Cinnamon Muffins\", \"Make Your Own Waffle Station\"]",
            "id": 11,
            "meal": "breakfast"
        },
        {
            "day": "fri",
            "dining_hall": "cmc",
            "food_items": "[\"Chocolate Chip Cookies\\nCinnamon Roll Cheesecake Cookies\\nPina Colada Bar\\nLemon Blueberry Pound Cake\", \"Red Velvet Cake\\nVegan Banana Cream Pie\\nMade Without Gluten Rochers\"]",
            "id": 13,
            "meal": "dessert"
        }, ...
    ]

###  Menus By Dining Hall and Day [/api/menu/dining_hall/{dining_hall}/day/{day}/]

Lists all menus by dining hall and a specific day of the week

#### Parameters

+ dining_hall (enum[string])

    Name of the dining hall

    + Members
        + frary
        + frank
        + cmc
        + mudd
        + scripps
        + oldenborg
        
+ day (enum[string])

    Name of the day of the week

    + Members
        + mon
        + tue
        + wed
        + thu
        + fri
        + sat
        + sun

#### Request (GET)

    + Headers
        Authorization: Token 83456d12c23f007d1d2ad7d2713b776d4644c21c

#### Response 200 (application/json)

    [
        {
            "day": "fri",
            "dining_hall": "cmc",
            "food_items": "[\"Breakfast Selections\", \"Scrambled Eggs\\nCheese & Bacon Eggs\\nTurkey Bacon & Sausage Patties\\nChorizo & Cheese Quesadilla\", \"Oatmeal & Grits\\nWaffles\\nHash Browns \\nCranberry & Apple Cinnamon Muffins\", \"Make Your Own Waffle Station\"]",
            "id": 11,
            "meal": "breakfast"
        },
        {
            "day": "fri",
            "dining_hall": "cmc",
            "food_items": "[\"Chocolate Chip Cookies\\nCinnamon Roll Cheesecake Cookies\\nPina Colada Bar\\nLemon Blueberry Pound Cake\", \"Red Velvet Cake\\nVegan Banana Cream Pie\\nMade Without Gluten Rochers\"]",
            "id": 13,
            "meal": "dessert"
        }, ...
    ]
    
###  Menus By Dining Hall, Day, and Meal [/api/menu/dining_hall/{dining_hall}/day/{day}/meal/{meal}/]

Find a menu with a specific dining hall, specific day of the week, and meal

#### Parameters

+ meal (enum[string])

    Name of the dining hall

    + Members
        + breakfast
        + lunch
        + dinner
        
+ dining_hall (enum[string])

    Name of the dining hall

    + Members
        + frary
        + frank
        + cmc
        + mudd
        + scripps
        + oldenborg
        
+ day (enum[string])

    Name of the day of the week

    + Members
        + mon
        + tue
        + wed
        + thu
        + fri
        + sat
        + sun

#### Request (GET)

    + Headers
        Authorization: Token 83456d12c23f007d1d2ad7d2713b776d4644c21c

#### Response 200 (application/json)

    {
        "day": "fri",
        "dining_hall": "cmc",
        "food_items": "[\"Breakfast Selections\", \"Scrambled Eggs\\nCheese & Bacon Eggs\\nTurkey Bacon & Sausage Patties\\nChorizo & Cheese Quesadilla\", \"Oatmeal & Grits\\nWaffles\\nHash Browns \\nCranberry & Apple Cinnamon Muffins\", \"Make Your Own Waffle Station\"]",
        "id": 11,
        "meal": "breakfast"
    }