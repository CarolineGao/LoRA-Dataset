# This is Ontology - Food. 
import owlready2
from owlready2 import *
from itertools import chain
import rdflib
#import sparql
from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import Graph, Literal, RDF, URIRef
from rdflib.namespace import FOAF, XSD
graph = default_world.as_rdflib_graph()

onto = get_ontology("http://test.org/onto.owl")

def getOnto():
    with onto:
        
        # Concept 
        class Food(Thing):
            pass
        class Vegetable(Food):
            pass
        class Fruit(Food):
            pass
        class Meat(Food):
            pass  
        class Fish(Food):
            pass
        class Grain(Food):
            pass
        class Dairy(Food):
            pass    
        class Poultry(Food):
            pass 
        
        class Tool(Thing):
            pass
        class Kitchenware(Tool):
            pass
        class Tableware(Tool):
            pass

        
        # Properties
        class Color(Thing):
            pass    
        class Shape(Thing):
            pass 
        class Taste(Thing):
            pass 
        class Nutrition(Thing):
            pass  
        class Country(Thing):
            pass   
        class Recipe(Thing):
            pass

        class Category(Thing):
            pass
        class Edible(Thing):
            pass
        class Dietary_method(Thing):
            pass
        class Function(Thing):
            pass
        class Ground(Thing):
            pass
        class Seed(Thing):
            pass
            

        # Role - Relationship   
        class has_color(ObjectProperty):
            domain    = [Food]
            range     = [Color]   
        class has_shape(ObjectProperty):
            domain    = [Tool]
            range     = [Shape] 
        class has_taste(ObjectProperty):
            domain    = [Food]
            range     = [Taste]
        class has_nutrition(ObjectProperty):
            domain    = [Food]
            range     = [Nutrition]   
        class original_from(ObjectProperty):
            domain    = [Food]
            range     = [Country]
        class is_ingredient_of(ObjectProperty):
            domain = [Food]
            range  = [Recipe]
        class has_ingredient(ObjectProperty):
            domain = [Recipe]
            range = [Food]   
        class is_category_of(ObjectProperty):
            domain = [Food]
            range  = [Category]  
        class has_edible_part(ObjectProperty):
            domain = [Food]
            range  = [Edible]
        class has_child_food(ObjectProperty):
            domain = [Food]
            range  = [Food] 
        class is_cousin_to(ObjectProperty):
            domain = [Food]
            range  = [Food] 
        class has_seed_inside(ObjectProperty):
            domain = [Food]
            range  = [Seed] 
        class has_dietary_method(ObjectProperty):
            domain = [Food]
            range  = [Dietary_method]
        class has_function(ObjectProperty):
            domain    = [Tool]
            range     = [Function]  
        class has_sub_function(ObjectProperty):
            domain = [Tool]
            range  = [Tool]      
        class is_growing(ObjectProperty):
            domain = [Food]
            range  = [Ground] 
        
        
        # Color 
        green = Color('green')
        red = Color('red')
        yellow = Color('yellow')
        white = Color('white')
        purple = Color('purple')
        orange = Color('orange')
        gray = Color('gray')
        brown = Color('brown')
        
        # Shape 
        long = Shape('long')  # eggplant , asparagus
        round = Shape('round')  # eggplant
        blocky= Shape('blocky')    # 块状 shape: capsicum 
        pointy= Shape('pointy')    # 尖尖的 shape: pepper, chilli  
        pear_shaped= Shape('pear_shaped')  # shape: eggplant, avocado
        conical= Shape('conical')  # shape: carrot  锥
        # cone= Shape('cone')  # asparagus  锥体  duplicate of conical
        cylindrical= Shape('cylindrical')   # 圆柱形 leek
        circular = Shape('circular')  # 圆
        # solid = Shape('solid')
        liquid = Shape('liquid')
        oblate= Shape('oblate')  #扁圆
        
        
        # Taste 
        
        bitter = Taste('bitter')
        fishy = Taste('fishy')
        fruity = Taste('fruity')
        grassy = Taste('grassy')
        herbal = Taste('herbal')
        juicy = Taste('juicy')
        sweet = Taste('sweet')
        sour = Taste('sour')
        salty = Taste('salty')
        spicy = Taste('spicy')
        pungent = Taste('pungent') # 辛辣的
        meaty = Taste('meaty')
        woody = Taste('woody')
        crisp= Taste('crisp')
        tart = Taste('tart')
        

        # Nutrition 营养元素
        protein = Nutrition('protein')
        fat = Nutrition('fat')
        calories = Nutrition('calories')
        vitamin_A= Nutrition('vitamin_A')
        vitamin_B= Nutrition('vitamin_B')
        vitamin_K = Nutrition('vitamin_K')
        vitamin_C = Nutrition('vitamin_C')
        vitamin_D = Nutrition('vitamin_D')
        vitamin_E = Nutrition('vitamin_E')
        carotenoids = Nutrition('carotenoids') #类胡萝卜素 In many vegetables but high in carrots, pumpkin and green leafy vegetables
        lycopene = Nutrition('lycopene') # 番茄红素 Tomatoes, watermelon
        lutein = Nutrition('lutein')  # 叶黄素 spinach, silverbeet, lettuce; sweet corn
        glucosinolates = Nutrition('glucosinolates') # 芥子油苷-可以通过促进对致癌物进行解毒的酶来降低患某些类型癌症的风险。broccoli, cauliflower, cabbage,
        flavonoids = Nutrition('flavonoids') # 类黄酮 beans, onions, leafy vegetables, tomatoes
        phenolic_acids = Nutrition('phenolic_acids')# 酚酸 In most vegetables but especially potatoes
        anthocyanins=Nutrition('anthocyanins') #花青素 Red, blue/purple vegetables – eggplant
        allium_sulphur_compounds=Nutrition('allium_sulphur_compounds')   # 葱硫化合物 Garlic, leeks, onions, chives
        capsaicinoids=Nutrition('capsaicinoids') #辣椒素类 Capsicums, chillis
        potassium = Nutrition('potassium') # 钾
        fiber= Nutrition('fiber') # 纤维
        carbohydrates= Nutrition('carbohydrates') # 碳水化合物
        iron= Nutrition('iron')
        calcium= Nutrition('calcium') # 钙
        carotene = Nutrition('carotene') # 胡萝卜素
        sugar = Nutrition('sugar')
        carbs = Nutrition('carbs')
        water = Nutrition('water')
        magnesium = Nutrition('magnesium')
        manganese = Nutrition('manganese')
        copper = Nutrition('copper')
        phosphorus = Nutrition('phosphorus')
        sodium = Nutrition('sodium')
        choline = Nutrition('choline')
        
        
        # Country 
        china = Country('china')
        canada = Country('canada')
        mexico = Country('mexico')
        america = Country('america')
        italy= Country('italy')
        egypt = Country('egypt')
        india = Country('india')
        europe = Country('europe')
        asia = Country('asia')
        france=Country('france')
        mediterranean=Country('mediterranean')

        # Category   
        flower_vegetables= Category('flowers_vegetables')
        fruit_vegetables= Category('fruits_vegetables')
        fungi_vegetables= Category('fungis_vegetables')  # 菌类
        leaves_vegetables= Category('leaves_vegetables')
        root_vegetables= Category('roots_vegetables')
        seed_vegetables= Category('seeds_vegetables') 
        bulb_vegetables= Category('bulbs_vegetables')  # 茎蔬菜
        stem_vegetables= Category('stems_vegetables')   # 茎蔬菜
        tuber_vegetables= Category('tubers_vegetables')  # 块茎蔬菜  
        herbs = Category('herbs')
        
        # Edible
        flowers= Edible('flowers')
        fruits= Category('fruits')
        fungi= Category('fungi') # 菌类
        leaves= Category('leaves')
        roots= Category('roots')
        seeds= Category('seeds')
        stalks= Category('stalks')
        bulbs= Category('bulbs')
        stems= Category('stem')
        tubers= Category('tubers') 
        
        # Dietary_method
        raw = Dietary_method('raw')
        cooked = Dietary_method('cooked')
        raw_and_cooked = Dietary_method('raw_and_cooked')

        
        # Seed
        seed = Seed('seed')
        
        # Recipe 
        juice = Recipe('juice')  # 果汁
        vegetable_juice = Recipe('vegetable_juice')
        fruit_juice = Recipe('fruit_juice')
        cake = Recipe('cake')
        salad = Recipe('salad')
        stir_fry = Recipe('stir_fry')
        pungent_meal = Recipe('pungent_meal')
        spicy_meal = Recipe('spicy_meal')
        fruit_salad = Recipe('fruit_salad')
        grilled_vegetables = Recipe('grilled_vegetables')
        vegetable_curry = Recipe('vegetable_curry')
        fruit_smoothie = Recipe('fruit_smoothie')
        fried_egg = Recipe('fried_egg')
        boil_egg = Recipe('boil_egg')
        steam_egg = Recipe('steam_egg')
        smoothie = Recipe('smoothie')
        

        # Function 
        fry = Function('fry')
        boil = Function('boil')
        drinking = Function('drinking')
    #     poking = Function('poking')
    #     stabbing = Function('stabbing')
        cutting = Function('cutting')
        servefood = Function('servefood')
        
        
        # Ground
        on_ground = Ground('on_ground')
        above_ground = Ground('above_ground')
        under_ground = Ground('under_ground')
        
        
        # Vegetables 蔬菜实例
        
        carrot = Vegetable("carrot", has_shape=[long, conical, cylindrical], has_color=[yellow, orange], has_nutrition=[carotene, fiber, vitamin_A, carotenoids, calcium, potassium, vitamin_C], has_taste=[sweet,woody, crisp], has_edible_part=[roots], is_category_of=[root_vegetables], is_ingredient_of=[vegetable_juice, salad, stir_fry, vegetable_curry, cake, vegetable_curry], has_dietary_method=[raw_and_cooked], is_growing=[under_ground])
        eggplant= Vegetable("eggplant", has_shape=[long, pear_shaped], has_color=[purple], has_nutrition=[anthocyanins, iron, fiber, vitamin_B], has_edible_part=[fruits], has_seed_inside=[seed], is_category_of=[fruit_vegetables], original_from=[asia], is_growing=[above_ground], is_ingredient_of=[stir_fry, grilled_vegetables])
        cucumber = Vegetable("cucumber", has_shape=[long, cylindrical], has_color=[green], has_nutrition=[potassium, fiber, vitamin_C], has_taste=[juicy, crisp], has_edible_part=[fruits], has_seed_inside=[seed], is_category_of=[fruit_vegetables], is_ingredient_of=[vegetable_juice, salad], has_dietary_method=[raw_and_cooked], is_growing=[above_ground])  
        
        zucchini = Vegetable("zucchini", has_shape=[long, cylindrical], has_color=[green], has_nutrition=[vitamin_A, vitamin_B, vitamin_C, carbohydrates], has_edible_part=[fruits, leaves], has_seed_inside=[seed], is_category_of=[fruit_vegetables], is_ingredient_of=[grilled_vegetables], has_dietary_method=[cooked], is_growing=[above_ground])  
        
        # 西葫芦
        
        potato = Vegetable("potato", has_shape=[round],has_color=[yellow, white], has_nutrition=[protein, carbohydrates, fiber, vitamin_C, potassium, phenolic_acids], has_taste=[sweet], has_edible_part=[tubers], is_category_of=[tuber_vegetables],original_from=[america], has_dietary_method=[cooked], is_growing=[under_ground])
        pumpkin = Vegetable("pumpkin", has_shape=[round],has_color=[yellow, orange], has_nutrition=[carotenoids, vitamin_A, fiber], has_taste=[sweet], original_from=[mexico, america], has_edible_part=[fruits], has_seed_inside=[seed], is_category_of=[fruit_vegetables], has_dietary_method=[raw_and_cooked], is_growing=[above_ground])

        # 菌菇类
        mushroom = Vegetable("mushroom", has_shape=[round], has_color=[gray], has_nutrition=[iron, vitamin_D, vitamin_B, potassium, copper, phosphorus], has_edible_part=[fungi], is_category_of=[fungi_vegetables], original_from=[france, europe], has_dietary_method=[cooked], is_growing=[above_ground], is_ingredient_of=[stir_fry, grilled_vegetables])
        
        # 绿叶蔬菜类
        lettuce = Vegetable("lettuce", has_shape=[round], has_color=[green], has_nutrition=[lutein, vitamin_C, potassium], has_taste=[grassy], original_from=[egypt, asia], has_edible_part=[leaves],is_category_of=[leaves_vegetables], has_dietary_method=[raw], is_growing=[on_ground], is_ingredient_of=[salad]) 
        cabbage = Vegetable("cabbage", has_shape=[round], has_color=[green], has_nutrition=[vitamin_C, calcium, fiber, glucosinolates], has_edible_part=[leaves],is_category_of=[leaves_vegetables], original_from=[europe], has_dietary_method=[cooked], is_growing=[on_ground])
        broccoli = Vegetable("broccoli", has_color=[green], has_nutrition=[vitamin_A, vitamin_C, calcium, iron, protein], has_edible_part=[flowers],is_category_of=[flower_vegetables], is_ingredient_of=[stir_fry], has_dietary_method=[raw_and_cooked], is_growing=[on_ground])
        asparagus= Vegetable("asparagus", has_shape=[conical, long], has_color=[green], has_nutrition=[vitamin_C, vitamin_K, protein], has_edible_part=[stems], is_category_of=[stem_vegetables], original_from=[europe, asia], has_dietary_method=[cooked], is_growing=[on_ground])
        
        # 辣椒类
        capsicum = Vegetable("capsicum", has_shape=[blocky], has_color=[green, red, yellow], has_nutrition=[capsaicinoids, vitamin_C, vitamin_B], has_taste=[spicy, crisp, sweet], has_edible_part=[fruits], has_seed_inside=[seed],is_category_of=[fruit_vegetables], has_dietary_method=[raw_and_cooked], is_growing=[above_ground], is_ingredient_of = [spicy_meal])
        pepper = Vegetable("pepper", has_shape=[pointy, long], has_color=[green, red, yellow], has_nutrition=[capsaicinoids, vitamin_C, vitamin_B], has_taste=[spicy], has_edible_part=[fruits], has_seed_inside=[seed],is_category_of=[fruit_vegetables], has_dietary_method=[raw_and_cooked], is_growing=[above_ground], is_ingredient_of = [spicy_meal])
        chilli = Vegetable("chilli", has_shape=[pointy, long], has_color=[green, red, yellow], has_nutrition=[capsaicinoids, vitamin_C, vitamin_B], has_taste=[spicy], has_edible_part=[fruits], has_seed_inside=[seed],is_category_of=[fruit_vegetables], has_dietary_method=[raw_and_cooked], is_growing=[above_ground], is_ingredient_of = [spicy_meal])
        
        # 葱蒜类
        onion = Vegetable("onion", has_shape=[round], has_color=[white, purple, brown], has_nutrition=[allium_sulphur_compounds, flavonoids, vitamin_C], has_taste=[pungent], has_edible_part=[bulbs],is_category_of=[bulb_vegetables], has_dietary_method=[raw_and_cooked], is_growing=[under_ground], is_ingredient_of=[salad, grilled_vegetables, pungent_meal, stir_fry])
        springonion = Vegetable("springonion", has_shape=[long], has_color=[white, green], has_nutrition=[vitamin_C, allium_sulphur_compounds, vitamin_B, iron], has_taste=[pungent], has_edible_part=[stalks],is_category_of=[bulb_vegetables], has_dietary_method=[raw_and_cooked], is_growing=[on_ground]) 
        garlic = Vegetable("garlic", has_shape=[round], has_color=[white], has_nutrition=[allium_sulphur_compounds, manganese, vitamin_B],has_taste=[pungent], has_edible_part=[bulbs], has_seed_inside=[seed],is_category_of=[bulb_vegetables], is_ingredient_of=[stir_fry, pungent_meal], has_dietary_method=[raw_and_cooked], is_growing=[under_ground])
        leek = Vegetable("leek", has_shape=[long, cylindrical], has_color=[green], has_nutrition=[allium_sulphur_compounds, iron, vitamin_C, vitamin_B, manganese], has_taste=[pungent], has_edible_part=[stalks],is_category_of=[bulb_vegetables], has_dietary_method=[raw_and_cooked], is_growing=[on_ground], is_ingredient_of=[pungent_meal])
        parsley = Vegetable("parsley", has_color=[green], has_nutrition=[vitamin_C, vitamin_A, iron, vitamin_B], has_taste=[herbal, woody], has_edible_part=[leaves, stalks],is_category_of=[leaves_vegetables, herbs], original_from=[mediterranean], has_dietary_method=[raw_and_cooked], is_growing=[on_ground])
        
        # orange_pumpkin = Vegetable("orange_pumpkin", has_shape=[oblate],has_color=[orange], has_nutrition=[carotenoids, vitamin_A, fiber], has_taste=[sweet], original_from=[america], has_edible_part=[fruits], has_seed_inside=[seed], is_category_of=[fruit_vegetables], has_dietary_method=[raw_and_cooked], is_growing=[above_ground])
        # yellow_pumpkin = Vegetable("yellow_pumpkin", has_shape=[round],has_color=[yellow], has_nutrition=[carotenoids, vitamin_A, fiber], has_taste=[sweet], original_from=[america], has_edible_part=[fruits], has_seed_inside=[seed], is_category_of=[fruit_vegetables], has_dietary_method=[raw_and_cooked], is_growing=[above_ground])
        # pumpkin = Vegetable("pumpkin",has_child_food=[orange_pumpkin, yellow_pumpkin])
        

    
        # Fruit 水果实例
        
        # grape_tomato = Fruit("grape_tomato", has_shape=[round], has_color=[red], has_taste=[juicy, sweet], has_nutrition=[lycopene, flavonoids, vitamin_C],has_edible_part=[fruits], has_seed_inside=[seed], is_category_of=[fruit_vegetables], original_from=[america], has_dietary_method=[raw_and_cooked], is_growing=[above_ground])
        tomato = Fruit("tomato", has_shape=[round], has_color=[red], has_taste=[juicy, sweet], has_nutrition=[lycopene, flavonoids, vitamin_C],has_edible_part=[fruits], has_seed_inside=[seed], is_category_of=[fruit_vegetables], has_dietary_method=[raw_and_cooked], is_growing=[above_ground], is_ingredient_of=[vegetable_juice, salad, grilled_vegetables,vegetable_curry])

    #     Fruit 水果实例 - 以下水果已经确认blender里面有object  
        apple = Fruit("apple", has_color=[green, red], has_taste=[sweet, fruity, tart], is_ingredient_of=[cake, fruit_juice, fruit_salad, fruit_smoothie, smoothie], has_shape =[round], has_nutrition=[sugar, fiber, vitamin_C, potassium, carbs, water], has_seed_inside=[seed])
        banana = Fruit("banana", has_shape=[long], has_color=[yellow], has_taste=[sweet, fruity], is_ingredient_of=[cake, fruit_salad, fruit_smoothie, smoothie], has_nutrition=[vitamin_B, fiber, potassium, magnesium, vitamin_C, sugar, manganese], has_seed_inside=[seed])
        orange = Fruit("orange", has_color=[orange], has_taste=[sweet, sour, juicy, fruity], is_ingredient_of=[fruit_juice, fruit_salad, fruit_smoothie, smoothie], has_shape=[round], has_nutrition=[sugar, fiber, vitamin_C, potassium, carbs, water, calcium], has_seed_inside=[seed])
        lemon = Fruit("lemon", has_color=[yellow], has_taste=[sweet, sour, juicy, fruity], original_from=[china], is_ingredient_of=[juice], has_shape=[round], has_nutrition=[sugar, fiber, vitamin_C, potassium, carbs, water, vitamin_B], has_seed_inside=[seed])
        plum = Fruit("plum", has_color=[purple], has_taste=[sweet, sour, juicy, fruity], original_from=[china], has_shape=[round], has_nutrition=[calories, carbs, fiber, sugar, vitamin_A, vitamin_C, vitamin_K, potassium, manganese], has_seed_inside=[seed])
        lime = Fruit("lime", has_color=[green], has_taste=[sweet, sour, juicy, fruity], original_from=[china], has_shape=[round], has_nutrition=[calories, carbs, fiber, vitamin_C, iron, calcium, vitamin_B, potassium], has_seed_inside=[seed])
        watermelon = Fruit("watermelon", has_color=[green, red], has_taste=[sweet, juicy, fruity], is_ingredient_of=[fruit_juice, fruit_salad, fruit_smoothie, smoothie], has_nutrition=[calories, carbs, fiber, sugar, vitamin_A, vitamin_C, potassium, magnesium], has_seed_inside=[seed])
        pear = Fruit("pear", has_color=[green, yellow], has_taste=[juicy, sweet, fruity], has_shape=[pear_shaped], is_ingredient_of=[fruit_juice, fruit_salad], has_nutrition=[calories, carbs, fiber, vitamin_C, vitamin_K, potassium, copper], has_seed_inside=[seed])
        grape = Fruit("grape", has_color=[green], has_taste=[juicy, sweet, fruity], is_ingredient_of=[fruit_juice, fruit_salad], has_shape=[round], has_nutrition=[calories, carbs, fiber, copper, vitamin_K, vitamin_B, potassium, vitamin_C, manganese, vitamin_E], has_seed_inside=[seed])
 
        avocado = Fruit("avocado", has_shape=[pear_shaped], has_color=[green], has_nutrition=[protein, fat, vitamin_A], original_from=[mexico, america], has_edible_part=[fruits], has_seed_inside=[seed], is_category_of=[fruit_vegetables], has_dietary_method=[raw], is_growing=[above_ground], is_ingredient_of=[smoothie] )
        
    #     Fruit 水果实例 - 以下水果未确认blender里面有object
        
        # kiwifruit = Fruit("kiwifruit", has_shape=[round], has_color=[green], original_from=[china], is_ingredient_of=[fruit_salad])
        # strawberry = Fruit("strawberry", has_color=[red], has_taste=[sweet])
        # pineapple = Fruit("pineapple", has_color=[yellow], has_taste=[sweet], is_ingredient_of=[fruit_juice, fruit_salad])
        # cherry = Fruit("cherry", has_color=[red], has_taste=[sweet, fruity], has_shape=[round])
        # green_apple = Fruit("green_apple", has_color=[green], has_taste=[sweet], original_from=[america])
        # red_apple = Fruit("red_apple", has_color=[red], has_taste=[sweet], original_from=[america])
        # golden_delicious = Fruit("golden_delicious", has_color=[yellow], has_taste=[sweet], original_from=[america])
        # gala = Fruit("gala", has_color=[red], has_taste=[sweet], original_from=[america])
        # mandarin = Fruit("mandarin", has_color=[yellow], has_taste=[sweet, juicy])
        # apple = Fruit("apple", has_child_food=[green_apple, red_apple, golden_delicious, gala])
        # orange = Fruit("apple", has_child_food=[mandarin])
        # Add more fruits with simplified relations
        # mango = Fruit("mango",
        #     has_color=[yellow, orange],
        #     has_taste=[sweet, fruity],
        #     is_ingredient_of=[fruit_salad, smoothie],
        #     has_shape=[round],
        #     has_nutrition=[vitamin_A, vitamin_C, fiber, sugar]
        # )

        # pineapple = Fruit("pineapple",
        #     has_color=[yellow],
        #     has_taste=[sweet, sour, fruity],
        #     is_ingredient_of=[fruit_salad, smoothie],
        #     has_shape=[round],
        #     has_nutrition=[vitamin_C, vitamin_B, fiber, sugar]
        # )

        # strawberry = Fruit("strawberry",
        #     has_color=[red],
        #     has_taste=[sweet, fruity],
        #     is_ingredient_of=[fruit_salad, smoothie],
        #     has_shape=[conical],
        #     has_nutrition=[vitamin_C, manganese, fiber, sugar]
        # )

        # kiwifruit = Fruit("kiwifruit",
        #     has_color=[brown, green],
        #     has_taste=[sour, sweet, fruity],
        #     is_ingredient_of=[fruit_salad, smoothie],
        #     has_shape=[round],
        #     has_nutrition=[vitamin_C, vitamin_K, fiber, sugar]
        # )

        # raspberry = Fruit("raspberry",
        #     has_color=[red],
        #     has_taste=[sweet],
        #     is_ingredient_of=[fruit_salad, smoothie],
        #     has_shape=[round],
        #     has_nutrition=[vitamin_C, manganese, fiber, sugar]
        # )



        egg = Poultry("egg", has_color=[brown], has_nutrition=[protein, calories, fat, sodium, choline, vitamin_B, phosphorus], is_ingredient_of = [fried_egg, boil_egg, steam_egg])
        
    #       Dairy 奶制品实例 - blender中存在对应object
        yoghurt = Dairy("yoghurt", has_taste=[sweet], has_nutrition=[protein, fat, calcium, vitamin_A, vitamin_B, phosphorus], is_ingredient_of=[fruit_smoothie, smoothie])
        cheese = Dairy("cheese", has_color=[yellow], has_taste=[salty], has_nutrition=[protein, fat, calcium, vitamin_A, vitamin_B, phosphorus])
        milk = Dairy("milk", has_color=[white], has_nutrition=[protein, fat, vitamin_A, vitamin_B, phosphorus], has_taste = [sweet], is_ingredient_of=[smoothie, fruit_smoothie])
      

        
    #     Meat 肉类实例 - blender中暂无对应object
        beef = Meat("beef", has_taste=[meaty], has_color=[red])
        # chicken = Meat("chicken", has_taste=[meaty], has_color=[white])
        lamb = Meat("lamb", has_taste=[meaty], has_color=[red])
        pork = Meat("pork", has_taste=[meaty], has_color=[red])
        
        # salmon = Fish("salmon", has_taste=[fishy], has_nutrition=[fat, protein])
        # shrimp = Fish("shrimp", has_taste=[fishy], has_nutrition=[protein])
        # squid = Fish("squid", has_taste=[fishy], has_nutrition=[protein])
        
        
        # rice = Grain("rice", has_shape=[round, long])
        # noodle = Grain("noodle", has_shape=[long])
        # pasta = Grain("pasta", has_shape=[round, long])
        bread = Grain("bread", has_shape=[long])
        # corn = Grain("corn", has_color=[yellow], original_from=[america])
        
        
        pan = Kitchenware('pan', has_function=[fry], has_color=[red])   
        pot = Kitchenware('pot', has_function=[boil], has_color=[red])  
        # chopping_board = Kitchenware('chopping_board', has_function=[cutting])  

        # spoon = Tableware('spoon', has_function=[drinking])
        # # fork = Tableware('fork', has_function=[poking, stabbing])
        # knife = Tableware('knife', has_function=[cutting])
        # plate = Tableware('plate', has_function=[servefood], has_shape=[circular], has_sub_function=[chopping_board])
    
        # Recipe
        vegetable_juice = Recipe('vegetable_juice', has_ingredient=[carrot, tomato, cucumber])
        fruit_juice = Recipe('fruit_juice', has_ingredient=[apple, orange, lemon, watermelon, grape, pear,lemon, lime])
        cake = Recipe('cake', has_ingredient=[apple, banana, carrot, lemon, lime])
        salad = Recipe('salad', has_ingredient=[lettuce, cucumber, tomato, carrot, onion, avocado, broccoli])
        stir_fry = Recipe('stir_fry', has_ingredient=[broccoli, carrot, onion,mushroom, eggplant, zucchini, asparagus])
        pungent_meal = Recipe('pungent_meal', has_ingredient=[onion, garlic, leek])
        spicy_meal = Recipe('spicy_meal', has_ingredient=[capsicum, chilli])
        fruit_salad = Recipe('fruit_salad', has_ingredient=[apple, banana, orange, grape, watermelon])
        grilled_vegetables = Recipe('grilled_vegetables', has_ingredient=[eggplant, zucchini, capsicum, mushroom, asparagus])
        fruit_smoothie = Recipe('fruit_smoothie', has_ingredient=[milk, yoghurt, banana, apple, orange, watermelon, lemon, lime])
        vegetable_curry = Recipe('vegetable_curry', has_ingredient=[potato, carrot, tomato])
        smoothie = Recipe('smoothie', has_ingredient=[milk, yoghurt, avocado, banana, apple, orange, lemon, lime])

        print('ok-onto6')
        
    return onto   
    
getOnto()
   