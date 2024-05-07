from flask import Flask, jsonify, request
app = Flask(__name__)
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

"""Defining the database for characters"""    
class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)
    background = db.Column(db.String(64), nullable=False)
    race = db.Column(db.String(32), nullable=False)

    char_stats = db.relationship('Stats', backref='character', uselist=False, lazy=True)
    char_actions = db.relationship('Actions', backref='character', uselist=False, lazy=True)
    char_items = db.relationship('Items', backref='character', lazy=True)
    def __repr__(self):
        return f"{self.name} - {self.race} - {self.background} - {self.char_stats} - {self.char_actions} - {self.char_items}"
    
"""Defing the database for character stats"""
class Stats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    health_points = db.Column(db.Integer, nullable=False)
    action_points = db.Column(db.Integer, nullable=False)
    mana_points = db.Column(db.Integer, nullable=False)
    speech = db.Column(db.Integer, nullable=False)
    sneak = db.Column(db.Integer, nullable=False)
    melee = db.Column(db.Integer, nullable=False)
    ranged = db.Column(db.Integer, nullable=False)
    magic = db.Column(db.Integer, nullable=False)
    toughness = db.Column(db.Integer, nullable=False)
    stamina = db.Column(db.Integer, nullable=False)

    character_id = db.Column(db.Integer, db.ForeignKey('character.id'), nullable=True)

    def __repr__(self):
        return f"{self.health_points} - {self.action_points} - {self.mana_points}"

"""Defining the database for actions"""
class Actions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    move = db.Column(db.Boolean, nullable=False)
    attack = db.Column(db.Boolean, nullable=False)
    explore = db.Column(db.Boolean, nullable=False)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'), nullable=True)

    def __repr__(self):
        return f"{self.move} - {self.attack} - {self.explore}"

"""Defining the database for items"""
class Items(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=False, nullable=False)
    description = db.Column(db.String(128))
    affect = db.Column(db.String(16), unique=False, nullable=True)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'), nullable=True)

    def __repr__(self):
        return f"{self.name} - {self.description} - {self.affect}"
    
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return 'yes?'

@app.route('/characters')
def get_chars():
    characters = Character.query.all()
    output = []
    for character in characters:
        items = []
        stats = {
            'health_points': character.char_stats.health_points,
            'action_points': character.char_stats.action_points,
            'mana_points': character.char_stats.mana_points,
            'speech': character.char_stats.speech,
            'sneak': character.char_stats.sneak,
            'melee': character.char_stats.melee,
            'ranged': character.char_stats.ranged,
            'magic': character.char_stats.magic,
            'toughness': character.char_stats.toughness,
            'stamina': character.char_stats.stamina
        }
        actions = {
            'move': character.char_actions.move,
            'attack': character.char_actions.attack,
            'explore': character.char_actions.explore
        }
        for item in character.char_items:
            items.append({
                'name': item.name,
                'description': item.description,
                'affect': item.affect
            })

        character_data = {
            'name': character.name,
            'background': character.background,
            'race' : character.race,
            'stats': stats,
            'actions': actions,
            'items': items
        }

        output.append(character_data)

    return jsonify(output)

@app.route('/characters/<id>')
def get_char(id):
    characters = Character.query.all()
    for char in characters:
        if (char.name).upper() == id.upper():
            character = char
    items = []
    stats = {
        'health_points': character.char_stats.health_points,
        'action_points': character.char_stats.action_points,
        'mana_points': character.char_stats.mana_points,
        'speech': character.char_stats.speech,
        'sneak': character.char_stats.sneak,
        'melee': character.char_stats.melee,
        'ranged': character.char_stats.ranged,
        'magic': character.char_stats.magic,
        'toughness': character.char_stats.toughness,
        'stamina': character.char_stats.stamina
        }
    actions = {
        'move': character.char_actions.move,
        'attack': character.char_actions.attack,
        'explore': character.char_actions.explore
    }
    for item in character.char_items:
        items.append({
            'name': item.name,
            'description': item.description,
            'affect': item.affect
        })

    character_data = {
        'name': character.name,
        'background': character.background,
        'race' : character.race,
        'stats': stats,
        'actions': actions,
        'items': items
    }


    return jsonify(character_data)

@app.route("/characters/<id>", methods=['DELETE'])
def delete_char(id):
    characters = Character.query.all()
    for character in characters:
        if (character.name).upper() == id.upper():
            db.session.delete(character)
            db.session.commit()
            return {"message": "character deleted"}
    return {"error": "not found"}

@app.route("/characters", methods=['POST'])
def add_char():
    data = request.json
    new_name = data['name']
    new_race = data['race']
    new_bg = data['background']
    new_stats = data['stats']
    characters = Character.query.all()
    for character in characters:
        if new_name == character.name:
            return {"message": "CHARACTER ALREADY MADE"}
    new_char = Character(name=new_name, background=new_bg, race=new_race)
    db.session.add(new_char)
    db.session.commit()

    actions = Actions(move=True, attack=True, explore=True, character=new_char)
    db.session.add(actions)
    db.session.commit()

    stats = Stats(health_points=10, action_points=10,mana_points=10,speech=new_stats['speech'],sneak=new_stats['sneak'],melee=new_stats['melee'],ranged=new_stats['ranged'],magic=new_stats['magic'],toughness=new_stats['toughness'],stamina=new_stats['stamina'], character=new_char)
    db.session.add(stats)
    db.session.commit()

    return{"message": "character added"}

if __name__ == "__main__":
    app.run(debug=True)
