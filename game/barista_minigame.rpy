init python:
    # Timing
    barista_total_duration = 0
    barista_time = 0
    start_order_time = 0

    # Current cup attributes
    cup_attributes = {
        "coffee": 0,
        "sugar": 0,
        "milk": 0,
        "ice": 0
    }
    
    # Order variables
    order_num = 0
    order_attributes = {
        "coffee": 0,
        "sugar": 0,
        "milk": 0,
        "ice": 0
    }
    order_price = 0
    order_tip_range = [0, 10000]

    # Money
    total_money = 0

    def start_barista_minigame(dur=120, tip_range=[0,5000]):
        order_tip_range = tip_range
        start_timer(dur)
        generate_order()
        reset_cup_attributes()

    def start_timer(dur):
        global barista_total_duration, barista_time
        barista_total_duration = dur
        barista_time = 0
    
    def update_timer():
        global barista_time, barista_total_duration
        barista_time += 1
        if(barista_time >= barista_total_duration):
            renpy.notify(f"Time's up!")

    def generate_order(base_price = 20000):
        global order_price, order_attributes, order_num
        order_attributes["coffee"] = renpy.random.randint(1, 3)
        order_attributes["sugar"] = renpy.random.randint(0, 3)
        order_attributes["milk"] = renpy.random.randint(0, 3)
        order_attributes["ice"] = renpy.random.randint(0, 3)
        # order_price = renpy.random.randint(price_range[0], price_range[1])
        order_price = base_price
        order_num += 1
        start_order_time = barista_time

    def check_order():
        for attr, value in order_attributes.items():
            if cup_attributes[attr] != value:
                return False
        return True

    # Reset the cup attributes
    def reset_cup_attributes():
        global cup_attributes
        cup_attributes["coffee"] = 0
        cup_attributes["sugar"] = 0
        cup_attributes["milk"] = 0
        cup_attributes["ice"] = 0
        cup.set_child("Barista/Objects/Cup.png")

    # Updating the cup attributes (add coffee, sugar, etc)
    def update_cup(dragged_name):
        if dragged_name == "coffee":
            cup_attributes["coffee"] += 1
        elif dragged_name == "sugar":
            cup_attributes["sugar"] += 1
        elif dragged_name == "milk":
            cup_attributes["milk"] += 1
        elif dragged_name == "ice":
            cup_attributes["ice"] += 1

        if cup_attributes["coffee"] >= 1:
            if cup_attributes["ice"] >= 1:
                cup.set_child("Barista/Objects/CupCoffeeIce.png")
            else:
                cup.set_child("Barista/Objects/CupCoffee.png")

        renpy.notify(f"Added {dragged_name} to the cup!")

    # This basically handle the drop event when an ingredient is dragged then dropped
    def ingredient_drop(dragged_items, dropped_on):
        if dropped_on is not None:
            if dropped_on.drag_name == "cup":
                # if the dragged item is dropped on the cup, update the cup attributes
                update_cup(dragged_items[0].drag_name)
        
        # put the item back to its initial position
        dragged_items[0].snap(dragged_items[0].style.xpos, dragged_items[0].style.ypos)
    
    def ingredient_drag(dragged_items, dropped_on):
        global active_drag
        active_drag = dragged_name
    
    def serve_cup():
        global total_money, order_price, order_num
        if check_order():
            total_money += order_price
        # order_price = renpy.random.randint(price_range[0], price_range[1])
            tip = (renpy.random.randint(order_tip_range[0], order_tip_range[1]) // 1000) * 1000
            total_money += tip

            renpy.notify(f"Order served successfully! (+ Tip: {tip}!)")
            
            reset_cup_attributes()
            generate_order()
        else:
            renpy.notify("Order not correct! Try again.")

    def trash_cup():
        reset_cup_attributes()

screen barista_minigame:
    # Background and drag zone
    add "Barista/Background/Barista_Background_3.png"

    # Display cup attributes
    frame:
        align (0.9, 0.1)
        background "#00000080"
        padding (10, 10)
        vbox:
            for attr, value in cup_attributes.items():
                text f"{attr.capitalize()}: {value}" color "#ffffff"
    
    frame:
        align (0.05, 0.52)
        background "#FFFFFF00"
        padding (10, 10)
        vbox:
            text f"Order #{order_num}:" color "#000000" size 24 bold True
            for attr, value in order_attributes.items():
                text f"{attr.capitalize()}: {value}" color "#000000" size 24
            
            text f"\n Money: Rp.{total_money}" color "#000000" size 24
    
    frame:
        xysize(350, 100)
        background None
        text "Time:" color "#000000"
        bar:
            xalign 1.2
            value barista_total_duration - barista_time
            range barista_total_duration
            xsize 250
    timer 1.0 action Function(update_timer) repeat True

    imagebutton:
        action Function(trash_cup)
        idle "Barista/Buttons/TrashBTN.png"
        xpos 1300
        ypos 880

    imagebutton:
        action Function(serve_cup)
        idle "Barista/Buttons/ServeBTN.png"
        xpos 1600
        ypos 880
    
    add ingredients_draggroup

define coffee = Drag(d="Barista/Ingredients/CoffeeBeans.png", drag_name="coffee", dragged=ingredient_drop, droppable=False, drag_raise=True, pos=(450, 650))
define sugar = Drag(d="Barista/Ingredients/SugarSpoon.png", drag_name="sugar", dragged=ingredient_drop, droppable=False, drag_raise=True, pos=(350, 800)) 
define milk = Drag(d="Barista/Ingredients/Milk.png", drag_name="milk", dragged=ingredient_drop, droppable=False, drag_raise=True, pos=(800, 700))
define ice = Drag(d="Barista/Ingredients/IceCubes.png", drag_name="ice", dragged=ingredient_drop, droppable=False, drag_raise=True, pos=(1000, 650))
define cup = Drag(d="Barista/Objects/Cup.png", drag_name="cup", pos=(1500, 550), draggable=False, droppable=True)
define ingredients_draggroup = DragGroup(coffee, sugar, milk, ice, cup)


