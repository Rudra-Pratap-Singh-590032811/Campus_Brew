import json, os, re
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
with open(os.path.join(BASE,'data','cafe_data.json'),encoding='utf-8') as f: CAFE=json.load(f)
DAYS = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
ALLERGY_TERMS = ['allerg','gluten','nut','peanut','dairy','milk','egg','celiac','coeliac','lactose','soy','sesame','shellfish','safe to eat','cross contact','cross-contact','intoleran','anaphylax','wheat']

def matches(q,item):
    name=item['name'].lower()
    return name in q or (name=='cafe latte' and 'latte' in q) or (name=='veg grilled sandwich' and 'sandwich' in q) or (name=='lemon iced tea' and 'iced tea' in q)

def respond(message):
    q=(message or '').strip()
    if not q: return 'Please type a question about opening hours, menu, allergens, or location.'
    l=q.lower()
    items=[x for x in CAFE['menu'] if matches(l,x)]
    allergen=any(term in l for term in ALLERGY_TERMS)
    if allergen:
        if items:
            detail=' '.join(f"{x['name']}: {', '.join(x['allergens']) if x['allergens'] else 'no allergens listed in the current data'}." for x in items)
        elif 'vegan' in l or 'vegetarian' in l:
            detail='Dietary labels are not proof of allergen safety.'
        else:
            detail='Please name a menu item so I can share its listed allergens. I cannot confirm an item is safe for your allergy.'
        return detail+' IMPORTANT: '+CAFE['allergen_notice']
    if 'vegan' in l or 'vegetarian' in l:
        kind='vegan' if 'vegan' in l else 'vegetarian'
        found=[f"{x['name']} (₹{x['price']})" for x in CAFE['menu'] if kind in x['dietary']]
        return f"Listed {kind} options: "+(', '.join(found) if found else 'none in the current data')+'. For allergy safety, ask café staff about ingredients and cross-contact.'
    if any(k in l for k in ['hour','open','close','timing','time','schedule']):
        for day in DAYS:
            if re.search(r'\b'+day+r'\b',l):
                d=day.capitalize();return f"On {d}, {CAFE['cafe_name']} is open {CAFE['hours'][d]}. These are published sample hours; confirm holiday changes with staff."
        return 'Opening hours (sample schedule; holiday hours may differ):\n'+'\n'.join(f'• {d}: {h}' for d,h in CAFE['hours'].items())
    if any(k in l for k in ['where','location','located','address','find you','directions','contact','phone']):
        return f"Our sample café location is {CAFE['location']}. Sample contact: {CAFE['contact']}. Please replace these demonstration details with real café information before public use."
    if any(k in l for k in ['menu','food','drink','coffee','tea','price','cost','sandwich','wrap','brownie','espresso','cappuccino','latte','chai','dessert','order','buy']):
        if items:
            return ' '.join(f"{x['name']} costs ₹{x['price']}. Listed allergens: {', '.join(x['allergens']) if x['allergens'] else 'none listed (not a safety guarantee)'}." for x in items)
        return 'Current sample menu:\n'+'\n'.join(f"• {x['name']} — ₹{x['price']}" for x in CAFE['menu'])+'\nPrices are sample data for this project.'
    if re.search(r'\b(hi|hello|hey|good morning|good evening)\b',l):
        return f"Hi! Welcome to {CAFE['cafe_name']}. I can help with our menu, opening hours, location, and listed allergens."
    if any(k in l for k in ['thank','bye']):return 'You’re welcome! Have a great day.'
    return 'I don’t have verified information for that question. I can help with opening hours, menu, listed allergens, and location. Please ask café staff for anything else.'
