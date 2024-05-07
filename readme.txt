default_character = Character(name='default', background='default_bg')
db.session.add(default_character)
db.session.commit()
item1 = Items(name='Sword', description='Its a sword', affect=None, character=default_character)
item2 = Items(name='Shield', description='Its a shield', affect=None, character=default_character)
db.session.add_all([item1, item2])
db.session.commit()
actions = Actions(move=True, attack=True, explore=True, character=default_character)
db.session.add(actions)
db.session.commit()
stats = Stats(health_points=10, action_points=10,mana_points=10,speech=10,sneak=10,melee=10,ranged=10,magic=10,toughness=10,stamina=10, character=default_character)
db.session.add(stats)
db.session.commit()
Enter venv:
    in terminal:
        cd ./cs361/a05/api
        source ./.venv/bin/activate

Exit venv:
    in terminal:
        deactivate

Start flask:
    in terminal:
        export FLASK_APP=server.py
        export FLASK_ENV=development
        flask run