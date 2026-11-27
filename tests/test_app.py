import sys,os
sys.path.insert(0,os.path.join(os.path.dirname(os.path.dirname(__file__)),'app'))
from chatbot import respond
from app import app

def test_hours(): assert 'Sunday' in respond('What are your Sunday hours?')
def test_location(): assert 'Student Activity Centre' in respond('Where are you located?')
def test_menu(): assert 'Espresso' in respond('Show menu')
def test_price(): assert '₹140' in respond('How much is Cappuccino?')
def test_allergen_safety(): assert 'cannot guarantee' in respond('I have a milk allergy, is cappuccino safe?')
def test_unknown_no_hallucination(): assert 'don’t have verified information' in respond('Do you have live music tonight?')
def test_vegan(): assert 'Espresso' in respond('What is vegan?')
def test_egg_warning(): assert 'egg' in respond('Does chocolate brownie contain egg?')
def test_no_fake_live_hours(): assert 'sample' in respond('What time do you open?').lower()
def test_api_info():
    r=app.test_client().get('/api/info'); assert r.status_code==200 and len(r.json['menu'])==8
def test_api_chat_and_history():
    c=app.test_client(); r=c.post('/api/chat',json={'message':'Show menu'}); assert r.status_code==200
    cid=r.json['conversation_id']; h=c.get('/api/history/'+cid); assert len(h.json['messages'])==2
    r2=c.post('/api/chat',json={'message':'Where are you?','conversation_id':cid}); assert r2.json['conversation_id']==cid
    assert len(c.get('/api/history/'+cid).json['messages'])==4

def test_empty_chat_rejected(): assert app.test_client().post('/api/chat',json={'message':' '}).status_code==400
def test_feedback(): assert app.test_client().post('/api/feedback',json={'rating':'helpful','message':'good'}).status_code==200
def test_health(): assert app.test_client().get('/api/health').json['status']=='ok'
