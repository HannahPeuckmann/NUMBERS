from rasa_nlu import training_data
from rasa_nlu.model import Interpreter, Trainer
from rasa_nlu.training_data import load_data
from rasa_nlu import config

training_data = load_data('train_data.md')
trainer = Trainer(config.load("config.yml"))
trainer.train(training_data)
model_directory = trainer.persist('rasa_model')

interpreter = Interpreter.load("rasa_model/default/model_nlu")

print(interpreter.parse(u"12 34 28 2"))
print("\n")
print(interpreter.parse(u"wiederholen bitte"))
print("\n")
print(interpreter.parse(u"nein falsch"))
print("\n")
print(interpreter.parse(u"127"))
print("\n")
print(interpreter.parse(u"Hans ist ein Kaesebrot"))
